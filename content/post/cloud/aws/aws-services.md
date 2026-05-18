---
title: AWS 服务使用记录
author: "-"
date: 2026-05-06T09:28:36+08:00
url: aws-services
categories:
  - cloud
tags:
  - aws
  - remix
  - AI-assisted
---

## EC2

Amazon Elastic Compute Cloud，虚拟机服务。按需启动 Linux/Windows 实例，支持多种规格（Instance Type）。常用于部署应用服务器、代理节点等。

## S3

Amazon Simple Storage Service，对象存储服务。用于存储文件、静态资源、备份等，支持生命周期策略和版本控制。

## Cognito

**Cognito** /kɒɡˈniːtoʊ/

Amazon Cognito，用户身份和访问管理服务。提供用户注册、登录、多因素认证（MFA）、OAuth 2.0 / OpenID Connect 集成等功能。分为两个核心概念：

- **User Pool**：管理用户的注册、登录、密码策略、邮件/短信验证
- **Identity Pool**：为已认证用户颁发临时 AWS 凭证，授权访问其他 AWS 服务（如 S3、DynamoDB）
