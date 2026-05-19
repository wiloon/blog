---
title: AWS 使用笔记
author: "-"
date: 2026-04-29T09:16:27+08:00
lastmod: 2026-05-19T16:31:13+08:00
url: aws
categories:
  - cloud
tags:
  - aws
  - remix
  - AI-assisted
---

## ARN（Amazon Resource Name）

ARN 是 **Amazon Resource Name**（亚马逊资源名称）的缩写，用于在 AWS 中唯一标识一项资源。IAM 策略、跨服务授权、Lambda 触发器、备份任务等场景里，经常需要写 ARN 来指定「对哪个资源生效」。

### 基本格式

```text
arn:partition:service:region:account-id:resource
```

常见字段说明：

| 字段 | 说明 |
| ---- | ---- |
| `partition` | 分区，一般为 `aws`；中国区为 `aws-cn`，GovCloud 为 `aws-us-gov` |
| `service` | 服务名，如 `ec2`、`s3`、`iam`、`lambda` |
| `region` | 区域；全局资源（如 IAM 角色）此处为空 |
| `account-id` | 12 位 AWS 账号 ID |
| `resource` | 资源类型与 ID，格式因服务而异 |

示例：

```text
arn:aws:s3:::my-bucket
arn:aws:ec2:ap-northeast-1:123456789012:instance/i-0abcd1234
arn:aws:iam::123456789012:role/MyRole
```

### 精确到哪一级？

ARN 的粒度**取决于资源类型**，不是固定「只到服务」或「只到实例」。

以 EC2 为例：

| 资源 | ARN 示例（示意） | 粒度 |
| ---- | ---- | ---- |
| 某台 EC2 实例 | `arn:aws:ec2:ap-northeast-1:123456789012:instance/i-0abcd1234` | 精确到这一台虚拟机 |
| 某块 EBS 卷 | `arn:aws:ec2:region:account:volume/vol-xxx` | 精确到这一块盘 |
| 某个安全组 | `arn:aws:ec2:region:account:security-group/sg-xxx` | 精确到这一个安全组 |
| 某个 AMI | `arn:aws:ec2:region:account:image/ami-xxx` | 精确到这一张镜像 |

因此：EC2 **实例**的 ARN 会带上 `instance/i-xxxxxxxx`，指向某一台具体 VM，而不是只表示「EC2 这个服务」。S3 桶、Lambda 函数、IAM 角色等同理，各自有独立的 ARN。

### 能否唯一确定一项资源？

在**有 ARN 的资源**上，通常可以认为：在同一 partition（一般为 `aws`）内，ARN 能唯一标识那一项资源。同一账号、同一区域里，两台不同实例的 ARN 一定不同（因为实例 ID 不同）。

需要注意：

- 并非所有 AWS 资源都有 ARN，部分资源需用资源 ID 或名称标识
- 不同 partition（`aws`、`aws-cn` 等）是独立的命名空间
- 不同账号的 ARN 不同；一台 EC2 与其挂载的 EBS、ENI、安全组各自有各自的 ARN

## 常用命令

查看所有区域的资源: ec2 > 左侧菜单 > AWS Global View

```bash
# 配置 CLI（使用 IAM admin 用户的 Access Key）
aws configure

# S3
aws s3 ls s3://obsidian-w10n
aws s3 cp foobar s3://obsidian-w10n
```

[https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

## SAA, Solution Architect Ass
