---
title: AWS SNS
author: "-"
date: 2026-05-19T11:09:49+08:00
lastmod: 2026-05-19T11:20:29+08:00
url: aws-sns
categories:
  - cloud
tags:
  - aws
  - sns
  - remix
  - AI-assisted
---

## 概述

Amazon Simple Notification Service（SNS）是 AWS 的**消息通知**服务，采用发布/订阅（pub/sub）模型：向 **Topic** 发布一条消息，所有 **Subscription** 都会收到。

常见用途：

- [CloudWatch Alarm](/aws-cloudwatch) 触发后发**邮件**、短信
- 应用解耦广播（一个事件通知多个下游）
- 推送到 Lambda、SQS、HTTP 端点

SNS **不负责监控、不负责排队存消息**；它只负责「把通知送出去」。

## 核心概念

| 概念 | 说明 |
| ---- | ---- |
| **Topic** | 主题，消息发布的目标（如 `enx-api-backup-alerts`） |
| **Publisher** | 发布方，调用 `Publish` 把消息发到 Topic |
| **Subscription** | 订阅，声明 Topic 上的消息要发到哪（邮箱、Lambda 等） |
| **Protocol** | 订阅协议：`email`、`sms`、`lambda`、`sqs`、`https` 等 |
| **Endpoint** | 订阅目标地址（邮箱地址、Lambda ARN、队列 ARN 等） |

```text
Publisher（CloudWatch Alarm / 应用 / 其它 AWS 服务）
  → Publish → Topic
                ├─ Subscription: email  → 你的邮箱
                ├─ Subscription: lambda → 触发函数
                └─ Subscription: sqs    → 写入队列
```

## 与 CloudWatch、SQS 的区别

| 服务 | 角色 |
| ---- | ---- |
| **[SQS](/aws-sqs)** | 消息**队列**，消费者拉取；适合异步削峰、DLQ 存档 |
| **CloudWatch** | **监控**与告警；Alarm 触发时不直接发邮件 |
| **SNS** | **通知**；把一条消息**推**给多个订阅者 |

备份失败通知链路：

```text
SQS DLQ（存失败详情）
  → CloudWatch Alarm（发现 DLQ 有消息）
  → SNS Topic（发通知）
  → Email 订阅（人收到邮件）
```

## 邮件订阅注意点

用 `email` 协议时，创建订阅后 AWS 会发一封 **Confirm subscription**，必须点链接确认，否则 Topic 有消息也**收不到邮件**。

订阅未确认前，控制台里状态为 `PendingConfirmation`。

### 同一 Topic 同时发邮件和 Telegram

SNS **没有**原生 `telegram` 协议。可在同一 Topic 上再挂一个 **`lambda` 订阅**，由 Lambda 调用 [Telegram Bot API](https://core.telegram.org/bots/api) 发消息：

```text
CloudWatch Alarm → SNS Topic
                    ├─ email
                    └─ lambda → Telegram
```

Bot Token 放在 `terraform.tfvars`（已 gitignore）或 SSM，**不要写进仓库**。

## 计费与免费额度

按**通知次数**计费，不同协议价格不同。详见 [SNS Pricing](https://aws.amazon.com/sns/pricing/)。

Homelab 常见情况：

| 协议 | 免费档（参考） |
| ---- | -------------- |
| **Email / Email-JSON** | 每月前 **1,000 封** 通常免费 |
| **HTTP/S** | 每月前 100,000 次 |
| **SMS** | 无长期免费档，按条收费 |

每周备份失败才告警几次，**基本不产生费用**。

## OpenTofu 示例

来自 `w10n-config/aws/opentofu/ec2-tokyo/lambda.tf`（CloudWatch Alarm → SNS 邮件）：

```hcl
resource "aws_sns_topic" "enx_backup_alerts" {
  name = "enx-api-backup-alerts"
}

resource "aws_sns_topic_subscription" "enx_backup_alerts_email" {
  topic_arn = aws_sns_topic.enx_backup_alerts.arn
  protocol  = "email"
  endpoint  = "you@example.com"
}

# Alarm 的 alarm_actions 指向 Topic ARN
resource "aws_cloudwatch_metric_alarm" "example" {
  # ...
  alarm_actions = [aws_sns_topic.enx_backup_alerts.arn]
}
```

CloudWatch 向 SNS 发布时，Topic 需允许 `cloudwatch.amazonaws.com` 调用 `sns:Publish`（见同文件 `aws_sns_topic_policy`）。

## 常用 CLI

```bash
# 列出 Topic
aws sns list-topics

# 创建 Topic
aws sns create-topic --name my-alerts

# 订阅邮件（之后去邮箱点确认）
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-northeast-1:123456789012:my-alerts \
  --protocol email \
  --notification-endpoint you@example.com

# 查看某 Topic 的订阅
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:ap-northeast-1:123456789012:my-alerts

# 手动发一条测试（确认订阅后）
aws sns publish \
  --topic-arn arn:aws:sns:ap-northeast-1:123456789012:my-alerts \
  --message "test notification"
```

## 参考

- [Amazon SNS 文档](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [SNS 定价](https://aws.amazon.com/sns/pricing/)
- [Terraform aws_sns_topic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic)
