---
title: 2026 W23
author: "-"
date: 2026-06-05T15:09:27+08:00
lastmod: 2026-06-05T15:33:23+08:00
url: weekly-2026-w23
categories:
  - career
tags:
  - weekly
  - original
  - AI-assisted
---

这篇周报合并了第 22、23 两周，因为上篇 [裁员之后，我的一些探索](./exploration.md) 发布后一直没写新的，正好把两周攒在一起记录一下。

## W22：研究 QuantDinger，部署量化交易环境

这两周主要在折腾 [QuantDinger](https://github.com/wiloon/QuantDinger)，一个开源的量化交易平台。

### 为什么要改造 MT5 接入方式

QuantDinger 原本直接通过 Python 库调用 MT5，但 MT5 只能运行在 Windows 环境里，而我的 homelab 主力是跑在 k8s 上的 Linux 容器。直接依赖 MT5 Python 库意味着后端必须跑在 Windows 上，这和 k8s 部署的思路不兼容。

于是我 fork 了上游仓库，在 `feat/mt5-thin-gateway` 分支上做了一个改造：把后端对 MT5 的直接函数调用拆成 RESTful API——新增了一个独立的 `mt5_gateway` 服务（Python + Flask），部署在 Windows PC 上，和 MT5 进程跑在同一台机器；k8s 里的后端通过 HTTP 调用这个 gateway，不再直接依赖 MT5 环境。

主要改动集中在几个地方：

- 新增 `mt5_gateway/` 目录，包含独立的 Flask 应用和访问日志模块
- 后端新增 `gateway_client.py`，封装对 gateway 的 HTTP 调用
- `execution.py`、`factory.py` 等调用路径对应调整
- 补充了若干单元测试（`test_mt5_factory_gateway.py` 等）

目前 homelab 部署已经跑通，可以正常下单。策略部分还在调试——外汇交易有不少领域知识我不熟悉，接下来打算补一补这块。如果 homelab 测试稳定，计划向上游提 PR。

### k8s 部署

写了 Ansible playbook 把 mt5_gateway 自动化部署到 Windows PC 上，k8s 侧对应更新了配置，让后端能找到 gateway 的地址。顺带也修了几个 k8s 节点的 DNS 配置问题。

另外这周还把 [Java Knowledge Map](../language/java/java-knowledge-map.md) 的内容整理了一下，作为职业经历回顾的补充背景资料。

## W23：准备面试，整理项目经历

W23 出现了一些有可能的面试机会，就把重心切换到准备面试上，QuantDinger 的探索暂停了一周。

简历里列的项目经历，在一小时的面试里很难逐一讲完。所以我把几个项目故事写成了单独的 blog 文章，面试官感兴趣的话可以到我的 blog 里看；这样面试时不需要花太多时间铺垫，面试时间有限，临场发挥也不一定稳定, 省下时间可以聊些其它的感兴趣的内容。

这周整理的几篇：

- [Android APK 安全评估项目回顾（2014）](./android-apk-security-assessment.md)
- [物联网平台协议解析服务生产环境 OOM：MySQL 迁移 InfluxDB（2017）](./iot-protocol-oom-mysql-influxdb.md)
- [Rule Status 字段的设计取舍（2022）](./rule-status-field-design.md)
- [Committer 服务分布式锁设计（2023）](./committer-lock.md)
- [Conflict Check（2024）](./conflict-check.md)

这些文章写下来也是对自己过去职业经历的一次整理和记录。另外，如果有哪位老板对我感兴趣的话，也可以从这些文档里快速的对我有一个了解。
