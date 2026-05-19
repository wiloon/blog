---
title: AWS EventBridge Scheduler
author: "-"
date: 2026-05-18T20:00:00+08:00
lastmod: 2026-05-19T10:40:37+08:00
url: aws-eventbridge-scheduler
categories:
  - cloud
tags:
  - aws
  - eventbridge
  - remix
  - AI-assisted
---

## 概述

EventBridge Scheduler 是 AWS 托管的定时任务服务，可以在指定时间或按固定频率触发各种 AWS 目标（Lambda、ECS Task、SNS、SQS 等），无需管理服务器。

与老版本的 **EventBridge Rules（Cron Rules）** 相比，Scheduler 是独立的服务，功能更强：

| 特性           | EventBridge Rules | EventBridge Scheduler     |
|----------------|-------------------|---------------------------|
| 时区支持       | 仅 UTC            | 支持任意时区              |
| 一次性调度     | 不支持            | 支持                      |
| 灵活速率表达式 | 有限              | 支持 `rate`、`cron`、一次性 |
| 目标数         | 每条规则最多 5 个 | 每个 Schedule 1 个        |
| 错误重试       | 无内置重试        | 支持重试策略和死信队列（见 [AWS SQS](/aws-sqs)） |
| 时间窗口       | 无                | 支持弹性时间窗口          |

## 核心概念

### Schedule 类型

| 类型         | 说明                 | 示例                              |
|--------------|----------------------|-----------------------------------|
| **Rate**     | 固定间隔重复         | `rate(5 minutes)`                 |
| **Cron**     | Cron 表达式，支持时区 | `cron(0 2 * * ? *)` 每天凌晨 2 点 |
| **One-time** | 指定某个时刻执行一次 | `2026-06-01T00:00:00`             |

### Schedule Group

Schedule 的逻辑分组，用于统一管理（打标签、批量删除）。默认分组为 `default`。

### Flexible Time Window（弹性时间窗口）

允许任务在指定时间后的一个窗口内任意时刻触发，有助于分散负载、避免整点突刺。

```
flexibleTimeWindow:
  mode: FLEXIBLE
  maximumWindowInMinutes: 15
```

## 权限模型

Scheduler 需要一个 IAM Role 来代表它调用目标服务，该 Role 的信任策略需允许 `scheduler.amazonaws.com` Assume：

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "scheduler.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

Role 附加的权限策略需包含目标操作，例如调用 Lambda：

```json
{
  "Effect": "Allow",
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:ap-northeast-1:123456789012:function:my-function"
}
```

## OpenTofu / Terraform 配置

### 完整示例：每天触发 Lambda

```hcl
# IAM Role for Scheduler
resource "aws_iam_role" "scheduler" {
  name = "eventbridge-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "scheduler.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "scheduler_lambda" {
  role = aws_iam_role.scheduler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = aws_lambda_function.my_func.arn
    }]
  })
}

# Schedule Group（可选，使用默认 group 时省略）
resource "aws_scheduler_schedule_group" "default" {
  name = "my-app-schedules"
}

# Schedule
resource "aws_scheduler_schedule" "daily_job" {
  name       = "daily-backup"
  group_name = aws_scheduler_schedule_group.default.name

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(0 18 * * ? *)"   # UTC 18:00 = 北京时间 02:00
  schedule_expression_timezone = "Asia/Tokyo"            # 直接用时区写法更直观

  target {
    arn      = aws_lambda_function.my_func.arn
    role_arn = aws_iam_role.scheduler.arn

    input = jsonencode({
      action = "backup"
    })

    retry_policy {
      maximum_retry_attempts       = 3
      maximum_event_age_in_seconds = 3600
    }
  }
}
```

### 一次性调度示例

```hcl
resource "aws_scheduler_schedule" "one_time" {
  name = "migration-trigger"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "at(2026-06-01T02:00:00)"

  target {
    arn      = aws_lambda_function.migrate.arn
    role_arn = aws_iam_role.scheduler.arn
  }
}
```

## 常用 CLI 命令

```bash
# 列出所有 Schedule
aws scheduler list-schedules

# 查看某个 Schedule 详情
aws scheduler get-schedule --name daily-backup

# 列出 Schedule Group
aws scheduler list-schedule-groups

# 手动触发（Scheduler 本身不支持手动触发，可直接调用 Lambda 测试）
aws lambda invoke --function-name my-function /tmp/output.json
```

## Cron 表达式说明

EventBridge 使用 6 字段 Cron（与标准 5 字段略有不同）：

```
cron(分 时 日 月 星期 年)
```

| 字段 | 范围            | 特殊字符        |
|------|-----------------|-----------------|
| 分钟 | 0-59            | `, - * /`       |
| 小时 | 0-23            | `, - * /`       |
| 日期 | 1-31            | `, - * ? / L W` |
| 月份 | 1-12 或 JAN-DEC | `, - * /`       |
| 星期 | 1-7 或 SUN-SAT  | `, - * ? / L #` |
| 年份 | 1970-2199       | `, - * /`       |

> **注意**：日期和星期不能同时指定，必须有一个用 `?` 占位。

常用示例：

```
cron(0 2 * * ? *)      # 每天 02:00（UTC）
cron(0/30 * * * ? *)   # 每 30 分钟
cron(0 9 ? * MON-FRI *) # 工作日每天 09:00
cron(0 0 1 * ? *)      # 每月 1 日 00:00
```

## 费用

- **免费额度**：每月前 1,400,000 次调用免费
- **超出部分**：$1.00 / 百万次调用

对于低频定时任务（如每天一次备份），基本不产生费用。

## 参考

- [EventBridge Scheduler 官方文档](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html)
- [Terraform aws_scheduler_schedule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule)
