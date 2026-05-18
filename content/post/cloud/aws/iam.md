---
title: AWS IAM
author: "-"
date: 2026-05-18T17:11:00+08:00
url: aws-iam
categories:
  - cloud
tags:
  - aws
  - iam
  - AI-assisted
---

## 核心概念

IAM（Identity and Access Management）是 AWS 的权限管理服务，控制"谁能对哪些资源做什么操作"。

| 概念                 | 说明                                               |
|----------------------|----------------------------------------------------|
| **User**             | 人用的账号，有固定 Access Key，用于控制台登录或 CLI  |
| **Group**            | 用户组，把多个 User 归组，统一附加策略               |
| **Role**             | 权限载体，定义"能做什么"，不能直接登录，由主体 assume |
| **Policy**           | 权限策略（JSON），附加到 User/Group/Role 上           |
| **Instance Profile** | 专用于 EC2 的 Role 容器，EC2 通过它携带 Role        |

## User vs Role

**User**：人或应用持有的固定身份，有长期有效的 Access Key。适合人工操作、CI/CD 等场景。

**Role**：临时身份，被某个主体（EC2、Lambda、另一个账号）"扮演"（assume）后获得临时凭证（15 分钟 ~ 12 小时有效）。不绑定固定密钥，安全性更高。

## Instance Profile（EC2 专用）

EC2 实例不能直接绑定 IAM Role，必须通过 **Instance Profile** 作为中间层：

```
EC2 实例
  └─ Instance Profile（容器）
       └─ IAM Role
            └─ 权限策略（Policy）
```

EC2 启动后通过 IMDS（实例元数据服务，`169.254.169.254`）自动获取 Role 的临时凭证，`aws` CLI 和各语言 SDK 会自动读取，无需 `aws configure`。

实践中 Instance Profile 和 Role 通常一一对应，用 OpenTofu/Terraform 创建时成对出现：

```hcl
resource "aws_iam_role" "ec2_tokyo" {
  name = "ec2-tokyo-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_tokyo" {
  name = "ec2-tokyo-profile"
  role = aws_iam_role.ec2_tokyo.name
}
```

## Policy 结构

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

- `Effect`：`Allow` 或 `Deny`
- `Action`：AWS 操作，格式为 `服务:操作`（如 `s3:PutObject`）
- `Resource`：ARN，指定作用范围，`*` 表示所有资源

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

## 常用 CLI 命令

```bash
# 查看当前身份
aws sts get-caller-identity

# 列出所有 IAM 用户
aws iam list-users

# 列出所有 Role
aws iam list-roles

# 查看 Role 绑定的策略
aws iam list-attached-role-policies --role-name ec2-tokyo-role

# 查看 Instance Profile
aws iam get-instance-profile --instance-profile-name ec2-tokyo-profile
```
