---
title: AWS CloudWatch
author: "-"
date: 2026-05-19T10:54:01+08:00
lastmod: 2026-05-19T11:09:49+08:00
url: aws-cloudwatch
categories:
  - cloud
tags:
  - aws
  - cloudwatch
  - remix
  - AI-assisted
---

## 概述

Amazon CloudWatch 是 AWS 的**监控与可观测性**服务：收集指标（Metrics）、写日志（Logs）、配置告警（Alarms）、做看板（Dashboards）。多数 AWS 服务（EC2、Lambda、SQS 等）会**自动**把基础指标推到 CloudWatch，无需自建 Prometheus/Grafana 也能做基础监控。

**CloudWatch Alarm 不是独立产品**，而是 CloudWatch 里的「指标超阈值 → 触发动作」能力，常配合 [SNS](/aws-sns) 发邮件、或触发 Auto Scaling。

## 核心能力

| 能力           | 说明                                     | 典型用途             |
|----------------|----------------------------------------|----------------------|
| **Metrics**    | 时序数据（CPU、队列深度、Lambda 错误次数等） | 看图、设告警          |
| **Alarms**     | 对 metric 设阈值，满足条件时执行动作        | DLQ 有消息 → 发邮件  |
| **Logs**       | 集中存储应用 / Lambda 日志                | `aws logs tail` 排错 |
| **Dashboards** | 把多个 metric 画在一张图                  | 运维看板             |

### Metrics 从哪来？

| 来源                              | 示例                                                                          |
|-----------------------------------|-------------------------------------------------------------------------------|
| **AWS 服务自动上报**              | SQS `ApproximateNumberOfMessagesVisible`、Lambda `Errors`、EC2 `CPUUtilization` |
| **自定义 metric**                 | 应用调用 `PutMetricData` 上报业务指标                                         |
| **Logs Insights / Metric Filter** | 从日志里统计错误行数生成 metric                                               |

基础服务指标通常**不单独收 metric 存储费**；自定义 metric 和高分辨率 metric 会另计费。

### Alarm 怎么工作？

1. 选定 **namespace + metric + dimensions**（例如 `AWS/SQS` + 队列名）
2. 设 **阈值、统计方式、评估周期**（例如 1 分钟内 Maximum ≥ 1）
3. 配置 **Alarm action**（常见：`sns:Publish` 发通知）

状态：`OK` / `ALARM` / `INSUFFICIENT_DATA`。

> Alarm **只负责「发现问题并通知」**，不负责存失败详情；存档仍靠 [SQS DLQ](/aws-sqs) 等组件。

## 计费与免费额度

CloudWatch 按功能分别计费，详见 [CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)。

### 与 Alarm 相关的免费档（永久）

| 项目                        | 免费额度                                                                 |
|-----------------------------|--------------------------------------------------------------------------|
| **标准分辨率 Metric Alarm** | 每月 **10 个 alarm metrics**（直接引用 metric，不用 Metrics Insights 查询） |
| **自动 Dashboard**          | 免费                                                                     |
| **自定义 Dashboard**        | 每月 3 个，每个最多 50 个 metric                                          |

超出免费档后，标准 metric alarm 约 **$0.10 / metric / 月**（区域略有差异）。高分辨率 alarm、Composite alarm、异常检测 alarm 更贵。

### 其它常见计费项（简表）

| 项目                    | 说明                       |
|-------------------------|----------------------------|
| **Logs  ingest / 存储** | 按 GB 计费，有独立免费档    |
| **Logs Insights 查询**  | 按扫描数据量计费           |
| **自定义 metric**       | 按 metric 数量与分辨率计费 |

Homelab 规模（几条 alarm + 偶尔看 Lambda 日志）通常在免费档内。

## 实践：DLQ 有消息时邮件告警

备份任务失败链路与 [EventBridge Scheduler](/aws-eventbridge-scheduler) 配合时，**DLQ 本身不会发邮件**，需要 CloudWatch Alarm 盯队列深度：

```text
Scheduler 调用失败（重试耗尽）
  → 消息进入 SQS DLQ
  → CloudWatch Alarm：ApproximateNumberOfMessagesVisible ≥ 1
  → SNS → 邮件
```

OpenTofu 示例（`w10n-config/aws/opentofu/ec2-tokyo/lambda.tf`）：

```hcl
resource "aws_cloudwatch_metric_alarm" "enx_backup_scheduler_dlq" {
  alarm_name          = "enx-api-backup-scheduler-dlq"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Maximum"
  threshold           = 1
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.enx_backup_alerts.arn]

  dimensions = {
    QueueName = aws_sqs_queue.enx_backup_scheduler_dlq.name
  }
}
```

[SNS](/aws-sns) 邮件订阅首次需在邮箱里 **Confirm subscription**，否则 alarm 触发也收不到信。

## 常用 CLI

```bash
# 列出当前告警
aws cloudwatch describe-alarms --alarm-names enx-api-backup-scheduler-dlq

# 查看某条告警最近状态
aws cloudwatch describe-alarm-history \
  --alarm-name enx-api-backup-scheduler-dlq \
  --max-records 5

# 查看 SQS 队列深度（与 alarm 用的同一 metric）
aws cloudwatch get-metric-statistics \
  --namespace AWS/SQS \
  --metric-name ApproximateNumberOfMessagesVisible \
  --dimensions Name=QueueName,Value=enx-api-backup-scheduler-dlq \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Maximum

# 跟踪 Lambda 日志（Log group 需已存在）
aws logs tail /aws/lambda/enx-api-backup --since 1h
```

## OpenTofu 资源对照

| Terraform 资源                     | 用途                             |
|------------------------------------|----------------------------------|
| `aws_cloudwatch_metric_alarm`      | Metric 阈值告警                  |
| `aws_cloudwatch_log_group`         | 预创建 Log group（如 Lambda 日志） |
| `aws_cloudwatch_dashboard`         | 自定义看板                       |
| `aws_cloudwatch_log_metric_filter` | 从日志提取 metric                |

## 与其它服务的关系

```text
Amazon CloudWatch
├── Metrics   ← EC2 / Lambda / SQS 等自动写入
├── Alarms    → SNS（邮件/短信）、Auto Scaling、EventBridge
├── Logs      ← Lambda、应用、容器
└── Dashboards
```

| 场景         | 用 CloudWatch 做什么                                    |
|--------------|---------------------------------------------------------|
| Lambda 报错  | 看 `/aws/lambda/...` Logs；可对 `Errors` metric 设 alarm |
| 队列积压     | 对 SQS `ApproximateNumberOfMessagesVisible` 设 alarm    |
| 备份失败通知 | DLQ depth alarm → SNS（见上文）                           |
| EC2 磁盘满   | 需装 CloudWatch Agent 上报自定义 metric                 |

## 参考

- [Amazon CloudWatch 文档](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch 定价](https://aws.amazon.com/cloudwatch/pricing/)
- [使用 CloudWatch 告警](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [Terraform aws_cloudwatch_metric_alarm](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_metric_alarm)
