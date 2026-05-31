---
title: AWS 存储服务
author: "-"
date: 2026-05-18T13:57:00+08:00
url: aws-storage
categories:
  - cloud
tags:
  - AI-assisted
  - aws
  - dynamodb
  - rds
  - remix
  - s3
---

## 概览

| 服务        | 类型                        | 免费额度                     | 最低月费         |
|-------------|-----------------------------|------------------------------|------------------|
| S3          | 对象存储                    | 5 GB（前 12 个月）             | 极低，详见 [S3](./s3.md) |
| EBS         | 块存储                      | 30 GB（前 12 个月）            | 按容量计费       |
| EFS         | 文件存储（NFS）               | 5 GB（前 12 个月）             | 按用量计费       |
| RDS         | 关系型数据库                | db.t3.micro 750h（前 12 个月） | ~$15/月          |
| Aurora      | 关系型数据库（高性能）        | 无                           | ~$30/月起        |
| DynamoDB    | KV / 文档 NoSQL             | 25 GB 存储 + 25 WCU/RCU（永久）| 免费起步         |
| ElastiCache | 内存缓存（Redis / Memcached） | 无                           | ~$15/月          |
| DocumentDB  | 文档数据库（MongoDB 兼容）    | 无                           | ~$30/月起        |
| Keyspaces   | 宽列 NoSQL（Cassandra 兼容）  | 无                           | 按用量计费       |
| Neptune     | 图数据库                    | 无                           | ~$50/月起        |
| Timestream  | 时序数据库                  | 无                           | 按用量计费       |
| OpenSearch  | 全文检索 / 日志分析         | 无                           | ~$20/月起        |
| Redshift    | 数据仓库（OLAP）              | 无                           | ~$180/月起       |
| Athena      | S3 直接查询                 | 无                           | $5/TB 查询数据量 |

---

## NoSQL 数据库（免费首选）

### DynamoDB

AWS 自研全托管 NoSQL，完全 Serverless。

**数据模型：** KV + 文档（JSON），以 Table → Item → Attribute 组织数据

- **Primary Key**：Partition Key 或 Partition Key + Sort Key（复合键）
- **GSI**（Global Secondary Index）：支持非主键属性查询
- **Streams**：捕获变更事件，可触发 Lambda

**核心优势：**
- 完全 Serverless，无需管服务器
- 个位数毫秒延迟，自动水平扩展
- Global Tables 跨区域双向复制
- 与 Lambda、API Gateway 等 AWS 服务深度集成

**适用场景：** 高并发 KV 场景、Serverless 应用、访问模式固定的数据

**不适用：** 需要复杂 JOIN / 聚合查询，事务逻辑复杂

**免费额度（Always Free，永久）：**
- 存储：25 GB（累计总量上限，不是每月额度）
- 读写容量：25 WCU（写）+ 25 RCU（读），即每秒 25 次写、25 次读
- 对个人项目基本永远在免费额度内

### ElastiCache

托管 Redis / Memcached，用于缓存热点数据、Session、排行榜等内存场景。

**费用：** 最小 `cache.t3.micro` 约 **$15/月**

### DocumentDB

兼容 MongoDB API 的文档数据库，适合已有 MongoDB 应用迁移上云。

**费用：** 约 $30/月起

---

## 对象存储

### S3

Amazon Simple Storage Service，对象存储，详见 [AWS S3](./s3.md)。

---

## 块存储 / 文件存储

### EBS（Elastic Block Store）

挂载到 EC2 的块存储，类似本地硬盘。EC2 上运行的应用（包括 SQLite）数据默认存在这里。

- 只能挂载到单个 EC2 实例（部分类型支持多挂载）
- EC2 终止后 EBS 默认保留（可配置随实例删除）
- 支持快照备份到 S3
- **费用**：gp3 约 $0.08/GB/月

### EFS（Elastic File System）

托管 NFS 文件系统，多个 EC2 实例可同时挂载读写，适合共享文件场景。

- 自动扩容，无需预置容量
- 比 EBS 贵约 3 倍
- **费用**：约 $0.30/GB/月

---

## 关系型数据库

### RDS

Amazon Relational Database Service，托管关系型数据库。

支持引擎：PostgreSQL、MySQL、MariaDB、Oracle、SQL Server、Aurora

**核心优势：**
- 数据与计算分离，EC2 实例替换不影响数据
- 自动备份，支持按时间点恢复（PITR）
- Multi-AZ 高可用，主库故障自动切换，RPO 接近 0
- 只读副本分担读流量
- 自动打补丁，无需自己维护数据库软件

**适用场景：** 需要 SQL 和事务、多服务实例共享数据库、从自建 MySQL / PostgreSQL 迁移上云

**费用：** 最小规格 `db.t3.micro` 单 AZ 约 **$15–25/月**，Multi-AZ 翻倍

### Aurora

AWS 自研，兼容 MySQL / PostgreSQL，性能约 5x MySQL。支持 Aurora Serverless v2（按实际使用的 ACU 计费，闲置时缩到极低）。

**费用：** 比 RDS 贵约 20%，但性能更高

---

## 分析 / 搜索 / 时序

### Athena

直接查询存储在 S3 中的数据（CSV、Parquet、JSON 等），无需建表或管服务器。

- 按查询扫描的数据量计费：**$5/TB**
- 适合低频的日志分析、数据探索

### Redshift

列式数据仓库，用于大规模数据分析（OLAP），支持标准 SQL。不适合小项目。

### OpenSearch Service

托管 OpenSearch / Elasticsearch，适合全文检索、日志聚合分析（ELK 替代）。

**费用：** 最小单节点约 **$20/月起**

### Timestream

托管时序数据库，适合 IoT 传感器数据、监控指标存储。

---

## 按场景选型

| 场景                        | 推荐服务               |
|-----------------------------|------------------------|
| 文件备份、静态资源           | S3                     |
| EC2 本地应用数据（SQLite 等） | EBS（默认）              |
| 多实例共享文件              | EFS                    |
| 个人 / 小项目数据库（免费）   | DynamoDB               |
| 传统应用迁移上云            | RDS PostgreSQL / MySQL |
| 高并发 Serverless 应用      | DynamoDB               |
| 缓存 / Session              | ElastiCache Redis      |
| 日志搜索                    | OpenSearch             |
| 低频数据分析                | Athena + S3            |

---

## 与 SQLite 的对比

SQLite 运行在 EC2 本地 EBS 磁盘，适合个人工具或低并发单实例应用，零额外成本。考虑迁移的时机：

| 需求                              | 推荐迁移到      |
|-----------------------------------|-----------------|
| 多实例共享数据库                  | RDS 或 DynamoDB |
| 需要自动备份 / 高可用（RPO 接近 0） | RDS Multi-AZ    |
| 面向多用户，免费优先               | DynamoDB        |
| 需要复杂 SQL 查询                 | RDS PostgreSQL  |
