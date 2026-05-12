---
title: POSA1 架构模式
author: "-"
date: 2026-05-12T15:34:21+08:00
lastmod: 2026-05-12T15:34:21+08:00
url: posa1-architectural-patterns
categories:
  - Pattern
tags:
  - pattern
  - architecture
  - remix
  - AI-assisted
---

## POSA1 是什么

**《Pattern-Oriented Software Architecture, Volume 1: A System of Patterns》**（简称 POSA1），1996 年出版，作者为 Frank Buschmann、Regine Meunier、Hans Rohnert、Peter Sommerlad、Michael Stal。

POSA1 关注的是**架构模式（Architectural Patterns）**，粒度比 GoF（1994）的 23 种设计模式更大——GoF 解决的是类与对象之间如何协作，POSA1 解决的是整个系统应该如何组织。

|          | GoF（1994）                                 | POSA1（1996）                   |
| -------- | ------------------------------------------- | ------------------------------- |
| 模式级别 | 对象/类设计                                 | 系统/架构                       |
| 典型模式 | Strategy、Observer、Chain of Responsibility | Pipes & Filters、Layers、Broker |
| 解决问题 | 类之间如何协作                              | 整个系统如何组织                |

## POSA1 中的主要模式

### Layers（分层）

将系统分解为若干层，每层只依赖下层，对上层屏蔽实现细节。典型实现：OSI 网络模型、TCP/IP 协议栈、三层架构（表现层 / 业务层 / 数据层）。

### Pipes and Filters（管道-过滤器）

将数据处理拆分为一系列独立的 **Filter**，每个 Filter 负责单一转换，通过 **Pipe** 传递数据。整个系统是可组合的处理管道。

**特征：**

- 每个 Filter 独立，不依赖其他 Filter 的内部状态
- Filter 可以任意组合、复用、替换
- 任何一个 Filter 可以短路，中断后续处理

**经典实现：**

- Unix shell：`cat file | grep foo | sort | uniq`
- Java Servlet `FilterChain`
- Spring Security 的 `SecurityFilterChain`（兼具责任链的短路能力）
- ETL 数据处理管道

**与 GoF 责任链的区别：**

GoF 责任链是"找到一个能处理的就停下"，通常只有一个处理者真正响应；Pipes and Filters 是"每个 Filter 都参与处理，任意一个可以中断"，整体更像流水线而非分拣队列。

### Broker（代理/中介）

解耦分布式系统中的客户端与服务端，通过中间的 Broker 转发请求和响应。典型实现：CORBA、gRPC、消息队列中间件。

### Model-View-Controller（MVC）

将应用分为 Model（数据与业务逻辑）、View（展示）、Controller（协调输入与模型更新）三个角色，降低 UI 与业务逻辑的耦合。GoF 书中也提到 MVC，但 POSA1 将其正式归类为架构模式。

### Microkernel（微内核）

将系统最小核心功能放入内核，其余功能以插件形式扩展。典型实现：操作系统微内核（GNU Hurd）、Eclipse 插件体系、VS Code 扩展机制。

### Reflection（反射）

允许系统在运行时检查和修改自身结构与行为，实现元级别的自适应。Java 反射 API、Spring IoC 容器的 Bean 发现机制均属此类。

## 参考

- Buschmann et al., *Pattern-Oriented Software Architecture Vol.1*, Wiley, 1996
- [维基百科：Architectural pattern](https://en.wikipedia.org/wiki/Architectural_pattern)
