---
title: AWS SQS
author: "-"
date: 2026-05-19T10:39:56+08:00
lastmod: 2026-05-19T10:54:51+08:00
url: aws-sqs
categories:
  - cloud
tags:
  - AI-assisted
  - aws
  - remix
  - sqs
---

## 概述

Amazon Simple Queue Service（SQS）是 AWS 的**托管消息队列**：生产者把消息发到队列，消费者拉取并处理。无需自建 RabbitMQ/Kafka 集群，按 API 请求量计费。

常见用途：

- 服务之间**异步解耦**（下单后发消息，库存服务慢慢处理）
- **削峰填谷**（突发流量先排队，Worker 按能力消费）
- 作为其它服务的 **Dead Letter Queue（死信队列，DLQ）**，收纳处理失败的消息

## 核心概念

| 概念 | 说明 |
| ---- | ---- |
| **Queue** | 队列本身，有唯一 URL |
| **Message** | 一条消息，最大 1 MiB（超大 payload 可配合 S3） |
| **Producer** | 发送方，调用 `SendMessage` |
| **Consumer** | 接收方，调用 `ReceiveMessage`，处理完后 `DeleteMessage` |
| **Visibility Timeout** | 消息被某消费者取走后，在超时时间内对其它消费者不可见；超时未删除则重新可见，可被再次处理 |

### 标准队列 vs FIFO 队列

| 类型 | 特点 | 适用场景 |
| ---- | ---- | -------- |
| **Standard** | 至少一次投递、可能乱序、吞吐量高 | 大多数场景；**DLQ 通常用标准队列** |
| **FIFO** | 严格顺序、恰好一次（需配置）、吞吐量较低 | 订单、账务等强顺序场景 |

> EventBridge Scheduler、Lambda 等配置的 DLQ，一般使用 **标准队列**。

## 计费与免费额度

SQS **没有队列月租**，按 **API 请求次数** 计费：

- **永久免费档**：每月 **100 万次** SQS 请求（各区域合计，不结转）
- **超出后**（标准队列，东京等区域参考价）：约 **$0.40 / 百万次** 请求

计费细节：

- 每条 API（发送、接收、删除等）都算请求
- 消息体按 **每 64 KB 计 1 次请求**（1 MiB 消息 ≈ 16 次）
- **同区域内**收发消息，一般**不收数据传输费**
- **空队列、无 API 调用** → 基本 **$0**

低频失败进 DLQ（例如每周备份失败几次）几乎总在免费额度内。

参考：[Amazon SQS Pricing](https://aws.amazon.com/sqs/pricing/)

## 常用 CLI

```bash
# 列出队列
aws sqs list-queues

# 创建标准队列
aws sqs create-queue --queue-name my-queue

# 发送消息
aws sqs send-message \
  --queue-url "https://sqs.ap-northeast-1.amazonaws.com/123456789012/my-queue" \
  --message-body '{"action":"backup"}'

# 接收消息（长轮询建议加 --wait-time-seconds）
aws sqs receive-message --queue-url "<queue-url>" --max-number-of-messages 1

# 删除已处理的消息（需带上 ReceiptHandle）
aws sqs delete-message --queue-url "<queue-url>" --receipt-handle "<handle>"

# 查看队列属性（含 DLQ 配置）
aws sqs get-queue-attributes --queue-url "<queue-url>" --attribute-names All
```

## OpenTofu 示例

### 创建标准队列

```hcl
resource "aws_sqs_queue" "my_queue" {
  name                      = "my-app-queue"
  message_retention_seconds = 345600 # 4 天，默认也是 4 天
  visibility_timeout_seconds = 30
}
```

### 发送权限（给 Lambda / EC2 等）

```hcl
resource "aws_sqs_queue_policy" "my_queue" {
  queue_url = aws_sqs_queue.my_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { AWS = aws_iam_role.worker.arn }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.my_queue.arn
    }]
  })
}
```

## Dead Letter Queue（死信队列）

### 是什么？

**DLQ 不是独立 AWS 产品**，而是一种模式：当消息**多次处理仍失败**（或上游服务投递失败且重试耗尽）时，把消息转存到**另一个队列**（几乎都是 SQS），避免静默丢失，便于排查和补跑。

```text
正常路径：  生产者 → 主队列 → 消费者处理 → 删除消息

DLQ 路径：  处理失败 / 上游重试耗尽 → 死信队列（SQS）→ 人工或 Lambda 再处理
```

### 和重试策略的关系

以 [EventBridge Scheduler](./eventbridge-scheduler.md) 为例：

| 机制 | 作用 |
| ---- | ---- |
| **Retry policy** | 调用 Lambda **暂时失败**时自动重试（如限流） |
| **DLQ** | 重试仍失败后，把失败详情 **写入 SQS** |

未配置 DLQ 时，最终失败的消息会被**丢弃**，只能靠 CloudWatch 指标排查。DLQ 有消息后通知人类需配合 [CloudWatch Alarm](./cloudwatch.md) → SNS，见该文「DLQ 有消息时邮件告警」一节。

### 哪些服务可以用 SQS 当 DLQ？

| 来源 | 说明 |
| ---- | ---- |
| **EventBridge Scheduler** | 调用 target 失败且重试耗尽 |
| **EventBridge 总线 Rules** | 事件投递 target 失败 |
| **Lambda** | 异步调用失败、或事件源映射失败 |
| **SQS 主队列** | 消费者多次收不到 `DeleteMessage`，超过 `maxReceiveCount` 后转入 DLQ |

### OpenTofu：Scheduler + DLQ 示例

```hcl
# 死信队列
resource "aws_sqs_queue" "scheduler_dlq" {
  name = "enx-api-backup-scheduler-dlq"
}

# Scheduler 侧：允许向 DLQ 发消息
resource "aws_sqs_queue_policy" "scheduler_dlq" {
  queue_url = aws_sqs_queue.scheduler_dlq.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "AllowEventBridgeScheduler"
      Effect = "Allow"
      Principal = { Service = "scheduler.amazonaws.com" }
      Action   = "sqs:SendMessage"
      Resource = aws_sqs_queue.scheduler_dlq.arn
      Condition = {
        ArnEquals = {
          "aws:SourceArn" = aws_scheduler_schedule.enx_backup.arn
        }
      }
    }]
  })
}

resource "aws_scheduler_schedule" "enx_backup" {
  name = "enx-api-backup-weekly"
  # ... schedule_expression 等省略 ...

  target {
    arn      = aws_lambda_function.enx_backup.arn
    role_arn = aws_iam_role.scheduler_enx_backup.arn

    retry_policy {
      maximum_retry_attempts       = 3
      maximum_event_age_in_seconds = 3600
    }

    dead_letter_config {
      arn = aws_sqs_queue.scheduler_dlq.arn
    }
  }
}
```

> **注意**：Scheduler 的 DLQ 收纳的是 **Invoke Lambda 失败** 的投递；若 Lambda 已成功返回但后续 SSM/脚本失败，不会进这条 DLQ。

### SQS 主队列自己的 DLQ（Redrive）

主队列处理失败时，也可配置 **Redrive Policy**，超过 `maxReceiveCount` 后消息进入 DLQ：

```hcl
resource "aws_sqs_queue" "dlq" {
  name = "my-app-dlq"
}

resource "aws_sqs_queue" "main" {
  name = "my-app-main"

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount       = 3
  })
}
```

### 排查 DLQ 里的消息

```bash
# 查看 DLQ 深度（积压条数）
aws sqs get-queue-attributes \
  --queue-url "<dlq-url>" \
  --attribute-names ApproximateNumberOfMessages

# 拉取一条失败消息（勿在生产随意 delete，先看清内容）
aws sqs receive-message --queue-url "<dlq-url>"
```

DLQ 消息体通常包含错误码、`RETRY_ATTEMPTS`、`EXHAUSTED_RETRY_CONDITION` 等字段，便于对照 Scheduler / Lambda 日志。

## 实践建议

1. **重要异步任务**（备份、计费、通知）建议同时配置 **重试 + DLQ**，不要只靠重试。
2. **不要对空 DLQ 高频轮询**，空轮询也会消耗 SQS 请求配额。
3. DLQ 要有**处理策略**：告警 + 人工排查，或 Lambda 定期消费并告警。
4. 与 Scheduler 相关配置见 `w10n-config` 中 `aws/opentofu/ec2-tokyo/lambda.tf`。

## 参考

- [Amazon SQS 开发者指南](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [Amazon SQS 定价](https://aws.amazon.com/sqs/pricing/)
- [EventBridge Scheduler 配置 DLQ](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets.html)
- [Terraform aws_sqs_queue](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sqs_queue)
