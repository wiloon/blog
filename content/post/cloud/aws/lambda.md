---
title: AWS Lambda
author: "-"
date: 2026-05-19T17:23:40+08:00
lastmod: 2026-05-19T17:23:40+08:00
url: aws-lambda
categories:
  - cloud
tags:
  - aws
  - lambda
  - serverless
  - remix
  - AI-assisted
---

## 概述

**AWS Lambda** 是无服务器（Serverless）计算服务：上传函数代码，由 AWS 按事件触发执行，按实际运行时长计费，无需管理虚拟机。

适合短任务、事件驱动、低频定时作业（配合 [EventBridge Scheduler](/aws-eventbridge-scheduler)）、轻量 API（API Gateway）、消息消费（SQS / SNS）等场景。不适合长时间常驻进程或持续高 CPU 负载。

## 核心概念

| 概念 | 说明 |
| ---- | ---- |
| **Function** | 一个部署单元：代码 + 运行时 + 配置（内存、超时、环境变量） |
| **Handler** | 入口函数名，格式 `文件名.函数名`，如 `lambda_function.handler` |
| **Runtime** | 运行环境，如 `python3.13`、`nodejs22.x` |
| **Execution Role** | Lambda **扮演**的 IAM Role，决定函数内能调用哪些 AWS API |
| **Event** | 触发时传入的 JSON 载荷（Scheduler、SNS、API Gateway 等格式不同） |
| **Context** | 运行时元数据（剩余超时时间、请求 ID 等） |
| **Resource-based policy** | 挂在函数上的策略，声明**谁可以调用**本函数（`aws_lambda_permission`） |

## ARN 格式

函数 ARN 示例：

```text
arn:aws:lambda:ap-northeast-1:123456789012:function:enx-api-backup
```

版本与别名会追加后缀（`:1`、`:prod`）；日常在 Scheduler、SNS 订阅里通常用**未限定版本**的函数 ARN。

## 权限模型（两层）

Lambda 涉及两类 IAM，容易混淆：

| 类型 | 谁配置 | 解决什么问题 |
| ---- | ------ | ------------ |
| **Execution Role** | 函数自身 `role` 字段 | 函数**出站**能做什么（写日志、调 SSM、读 S3） |
| **Resource policy** | `aws_lambda_permission` 等 | **谁可以调用**这个函数（Scheduler、SNS、API Gateway） |

```text
EventBridge Scheduler ──(resource policy: lambda:InvokeFunction)──► Lambda
                                                                      │
                                                                      ▼
                                                            Execution Role
                                                            (ssm:SendCommand, logs:PutLogEvents, …)
                                                                      │
                                                                      ▼
                                                                   EC2 / SSM / …
```

- **Execution Role** 信任策略 Principal 为 `lambda.amazonaws.com`（见 [AWS IAM](/aws-iam)）
- **调用方**（如 Scheduler）还需要自己的 Role 带 `lambda:InvokeFunction`；函数侧通常再加一条 `aws_lambda_permission` 限定 `source_arn`

## Handler 约定

以 Python 为例，入口签名固定为 `handler(event, context)`：

```python
def handler(event, context):
  # event：调用方传入的 JSON（Scheduler 的 input、SNS 的 Records 等）
  # context：剩余毫秒数 context.get_remaining_time_in_millis() 等
  return {"status": "ok"}
```

- 同步调用：返回值会回传给调用方
- 异步调用：返回值无意义；失败走重试 / DLQ（见 [AWS SQS](/aws-sqs)）
- 超时或未捕获异常：Lambda 记为失败，CloudWatch 有 `Errors` 指标和日志

## 常见触发方式

| 触发源 | 典型用途 | 相关笔记 |
| ------ | -------- | -------- |
| **EventBridge Scheduler** | 定时任务 | [EventBridge Scheduler](/aws-eventbridge-scheduler) |
| **SNS** | 告警转发（邮件旁路 Telegram 等） | [AWS SNS](/aws-sns) |
| **SQS** | 队列消费、异步解耦 | [AWS SQS](/aws-sqs) |
| **API Gateway / ALB** | HTTP API | — |
| **S3 / DynamoDB 等** | 对象上传、表变更 | — |

同一函数可被多个触发源订阅；每次调用是独立并发执行（受账户并发上限约束）。

## 实践：定时备份 + SNS 通知

东京 EC2 上的 `w10n-config` 栈里有两个 Lambda：

| 函数 | 作用 |
| ---- | ---- |
| `enx-api-backup` | Scheduler 每周触发 → [SSM Run Command](/aws-systems-manager) 在 EC2 跑备份脚本 |
| `sns-telegram-notify` | SNS Topic 订阅 → 把告警推到 Telegram（可选） |

链路示意：

```text
Scheduler (cron 周日 03:00 UTC)
  → enx-api-backup (120s timeout)
       → SSM send_command + 轮询 GetCommandInvocation
  → 失败时 Scheduler DLQ → CloudWatch Alarm → SNS → 邮件 / Telegram Lambda

SNS (enx-api-backup-alerts)
  ├─ email
  └─ lambda: sns-telegram-notify
```

`enx-api-backup` 核心逻辑（节选）：用 Execution Role 调 SSM，并在超时前轮询命令状态：

```python
def handler(event, context):
    instance_id = os.environ["EC2_INSTANCE_ID"]
    ssm = boto3.client("ssm")
    resp = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": ["/usr/local/bin/enx-api-backup.sh"]},
    )
    # … 轮询 get_command_invocation 直到 Success / Failed …
```

注意：**Scheduler 的 DLQ** 只收纳「调 Lambda 失败」；Lambda 已成功返回但 SSM/脚本失败，不会进 Scheduler DLQ，需在函数内抛错或另设告警。

## OpenTofu 要点

```hcl
# Execution Role
resource "aws_iam_role" "lambda_enx_backup" {
  name = "lambda-enx-backup-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_cloudwatch_log_group" "lambda_enx_backup" {
  name              = "/aws/lambda/enx-api-backup"
  retention_in_days = 30
}

resource "aws_lambda_function" "enx_backup" {
  function_name    = "enx-api-backup"
  role             = aws_iam_role.lambda_enx_backup.arn
  runtime          = "python3.13"
  handler          = "lambda_function.handler"
  filename         = data.archive_file.enx_api_backup.output_path
  source_code_hash = data.archive_file.enx_api_backup.output_base64sha256
  timeout          = 120

  environment {
    variables = {
      EC2_INSTANCE_ID = aws_instance.ec2_tokyo.id
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda_enx_backup]
}

# 允许 Scheduler 调用（resource-based policy）
resource "aws_lambda_permission" "scheduler_enx_backup" {
  statement_id  = "AllowEventBridgeScheduler"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.enx_backup.function_name
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.enx_backup.arn
}
```

部署代码常用 `archive_file` 把 `lambda_function.py` 打成 zip；改代码后 `source_code_hash` 变化会触发函数更新。

SNS 触发 Lambda 时同样需要 `aws_lambda_permission`（`principal = "sns.amazonaws.com"`）+ `aws_sns_topic_subscription`（`protocol = "lambda"`）。

## 日志与排错

Lambda 自动把 stdout / stderr 写到 CloudWatch Logs，Log group 名为 `/aws/lambda/<函数名>`（见 [CloudWatch](/aws-cloudwatch)）。

```bash
# 手动同步调用（测试）
aws lambda invoke \
  --region ap-northeast-1 \
  --function-name enx-api-backup \
  /tmp/out.json && cat /tmp/out.json

# 查看配置
aws lambda get-function-configuration --function-name enx-api-backup

# 跟踪日志
aws logs tail /aws/lambda/enx-api-backup --since 1h --follow
```

## 配置建议

| 项 | 说明 |
| -- | ---- |
| **timeout** | 设为略大于最坏情况耗时；轮询 SSM 时要留余量 |
| **memory** | 影响 CPU 配额；默认 128 MB 对轻量脚本够用，可按冷启动与耗时调高 |
| **环境变量** | 非机密配置（实例 ID）；密钥用 Secrets Manager / SSM Parameter Store |
| **Log retention** | 预建 Log group 并设 `retention_in_days`，避免日志无限堆积 |
| **并发** | 账户有区域并发上限；预留并发可保证关键函数不被挤占（额外费用） |

## 计费（概要）

- **请求**：按调用次数
- **持续时间**：按 GB-秒（内存 × 执行时间）
- **免费档**：每月有一定请求量与 GB-秒（具体见官网，低频 homelab 任务通常可忽略）

Scheduler、SSM、S3 等**其它服务**另计，不算在 Lambda 账单条目里。

## 参考

- [AWS Lambda 官方文档](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Lambda 权限模型](https://docs.aws.amazon.com/lambda/latest/dg/lambda-permissions.html)
- [Terraform aws_lambda_function](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function)
