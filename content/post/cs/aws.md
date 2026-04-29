---
title: AWS 使用笔记
date: 2026-04-29T09:16:27+08:00
categories:
  - cloud
tags:
  - aws
  - remix
  - AI-assisted
---

## 用户管理最佳实践

AWS 官方推荐：日常操作不使用 root 用户，改用 IAM 用户。

### Root 用户

只用于以下场景，用完即退出：

- 创建 AWS 账户
- 设置账单和账户信息
- 创建第一个 IAM admin 用户

建议为 root 用户开启 MFA，日常锁起来不用。

### IAM Admin 用户（日常使用）

对于个人用户，创建一个附加 `AdministratorAccess` 策略的 IAM 用户即可满足绝大多数需求。

`AdministratorAccess` 几乎等同于 root 权限，但不包括账单管理和关闭账户，日常管理 EC2、S3、RDS 等资源完全够用。

**创建步骤：**

1. 以 root 登录 → IAM → 创建用户（如 `admin`）
1. 附加托管策略：`AdministratorAccess`
1. 为该用户开启 MFA
1. 创建 Access Key 用于 CLI

之后退出 root，以后只用 `admin` 用户登录控制台和操作 CLI。

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
