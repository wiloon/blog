---
title: AWS 服务
author: "-"
date: 2026-05-06T09:28:36+08:00
lastmod: 2026-07-05T22:58:23+08:00
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

## Cloud Map

AWS Cloud Map，服务发现（Service Discovery）服务。允许为应用中的任何资源（微服务、数据库、队列、API 端点等）注册自定义名称，并通过 DNS 查询或 API 调用动态解析资源的当前位置（IP 地址、端口、URL 等）。

核心概念：

- **Namespace**：命名空间，资源名称的顶层容器，对应一个 DNS 域（如 `internal.example.com`）或 HTTP 命名空间
- **Service**：服务定义，描述一类资源的注册规则和健康检查策略
- **Service Instance**：实例，具体的资源条目，包含 IP、端口、自定义属性等

主要特性：

- 支持 DNS 和 HTTP API 两种发现方式
- 内置健康检查（Route 53 健康检查 或 自定义健康检查），自动剔除不健康实例
- 与 ECS、EKS、Lambda 深度集成，容器启动/停止时自动注册/注销
- 支持自定义属性（key-value），客户端可按属性过滤实例

典型用场景：微服务架构中，服务间调用不硬编码 IP，而是通过 Cloud Map 查询目标服务的最新地址，实现服务的动态扩缩容和故障转移。

## Route 53

Amazon Route 53，AWS 的 DNS（域名系统）服务。名字来源于 DNS 使用的标准端口号 53。

主要功能：

- **域名注册**：直接在 AWS 购买和管理域名
- **DNS 解析**：将域名解析为 IP 地址，支持 A、AAAA、CNAME、MX、TXT 等记录类型
- **健康检查**：定期探测端点可用性，配合路由策略自动切换流量
- **私有 DNS**：在 VPC 内部创建私有 Hosted Zone，解析内网域名

路由策略：

- **Simple**：简单解析，单条记录
- **Failover**：主备切换，主节点不健康时自动切到备节点
- **Latency**：按延迟就近路由，将用户请求导向延迟最低的区域
- **Geolocation**：按用户地理位置路由
- **Weighted**：按权重分流，常用于灰度发布
- **Multivalue Answer**：返回多条记录并过滤不健康实例，类似简单负载均衡

Route 53 健康检查也被 Cloud Map 用于监控服务实例，不健康的实例会自动从 DNS 响应中剔除。

## ECS

Amazon Elastic Container Service，容器编排服务。用于在 AWS 上运行和管理 Docker 容器，承担类似 Kubernetes 的调度角色。

两种启动模式：

- **EC2 模式**：容器运行在你自己管理的 EC2 实例上，对底层有完全控制权，适合需要自定义操作系统或特殊硬件的场景
- **Fargate 模式**：无服务器模式，AWS 负责底层机器，只需定义容器规格（CPU、内存），按实际使用量计费

核心概念：

- **Cluster**：集群，ECS 资源的逻辑边界
- **Task Definition**：任务定义，描述容器镜像、CPU/内存、环境变量、端口映射等配置，类似 docker-compose 文件
- **Task**：任务，Task Definition 的一次运行实例
- **Service**：服务，维持指定数量的 Task 持续运行，支持滚动更新和负载均衡集成

## EKS

Amazon Elastic Kubernetes Service，托管 Kubernetes 服务。AWS 负责管理 Kubernetes 控制平面（Control Plane）的高可用和版本升级，用户只需管理工作节点（Worker Node）。

与 ECS 的区别：

- EKS 使用标准 Kubernetes API，可移植性更好，适合已有 K8s 经验的团队或需要跨云迁移的场景
- ECS 是 AWS 私有方案，与 AWS 生态集成更紧密，使用更简单

节点模式同样支持 EC2（自管节点）和 Fargate（无服务器）两种。

## Lambda

AWS Lambda，无服务器（Serverless）计算服务。上传代码后，AWS 自动管理运行环境，按函数实际执行次数和执行时长计费，空闲时不产生费用。

主要特点：

- **事件驱动**：由事件触发执行，支持 API Gateway、S3、DynamoDB、SQS、SNS、EventBridge 等多种触发源
- **自动扩缩容**：并发请求增加时自动横向扩展，无需预置容量
- **短生命周期**：单次执行最长 15 分钟，适合轻量任务，不适合长时间运行的进程
- **支持多种运行时**：Node.js、Python、Java、Go、Ruby、.NET 等，也支持自定义容器镜像

典型使用场景：API 后端、定时任务、文件处理（S3 上传触发）、消息队列消费、事件响应等。

## DynamoDB

**DynamoDB** /ˌdaɪnəmoʊ diː biː/（dye-nuh-moh-D-B）

Amazon DynamoDB，AWS 自研的全托管 NoSQL 数据库，支持键值（Key-Value）和文档（Document）两种数据模型。名字来源于 Dynamo，即 Amazon 内部 2007 年发表的分布式存储系统论文（Dynamo: Amazon's Highly Available Key-value Store），DynamoDB 是这套设计思想的托管产品化实现。

核心概念：

- **Table**：表，数据存储的顶层容器，无固定 schema，每行（Item）可以有不同的属性
- **Primary Key**：主键，分两种模式：
  - **Partition Key（分区键）**：单一属性作为主键，决定数据分布到哪个物理分区
  - **Partition Key + Sort Key（分区键 + 排序键）**：复合主键，同一分区键下按排序键排序，支持范围查询
- **Item**：一行数据，类似关系型数据库的行，但每个 Item 的属性集合可以不同
- **Attribute**：属性，类似列，支持字符串、数字、二进制、集合、嵌套 Map/List 等类型

主要特性：

- **无服务器**：不需要管理服务器或分片，容量按需自动扩缩
- **单位数毫秒延迟**：适合高并发、低延迟的读写场景
- **两种容量模式**：On-Demand（按实际读写请求计费）和 Provisioned（预置读写容量单位 RCU/WCU）
- **Global Secondary Index (GSI) / Local Secondary Index (LSI)**：二级索引，支持除主键外的其他查询模式
- **DynamoDB Streams**：捕获表数据变更事件，可触发 Lambda 做异步处理
- **全球表（Global Tables）**：多区域多主复制，实现跨区域低延迟访问和灾备

与关系型数据库的区别：DynamoDB 不支持 JOIN 和复杂事务查询（虽然支持有限的事务操作 TransactWriteItems/TransactGetItems），设计时需要预先规划好访问模式（Access Pattern），通过冗余数据和索引换取查询性能，而不是像关系型数据库那样事后用 JOIN 拼接。

典型使用场景：高并发的用户会话存储、购物车、排行榜、IoT 设备状态、游戏状态存储等对延迟敏感、访问模式相对固定的场景。

## 维护记录

| 时间       | 修改内容                                 | 原因                   |
| ---------- | ---------------------------------------- | ---------------------- |
| 2026-07-05 | 新增 DynamoDB 章节，含发音和核心概念说明 | 补充自研数据库服务介绍 |
