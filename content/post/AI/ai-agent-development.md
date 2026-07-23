---
title: AI agent development
author: "-"
date: 2026-04-26T14:39:27+08:00
lastmod: 2026-07-23T15:30:26+08:00
url: ai-agent-development
categories:
  - AI
tags:
  - remix
  - AI-assisted
  - ai-agent
  - LLM
aliases:
  - /p4058/
---

## AI Agent 开发的本质

开发 AI Agent 的核心是**将已验证的知识和流程固化成可执行的规则和指令**。

具体来说：

1. **知识固化** - 把专家经验、最佳实践、业务规则编码成 Agent 可以遵循的指令
1. **流程自动化** - 将重复性的决策流程转化为确定性的执行步骤
1. **质量保障** - 通过固化的规则确保每次执行的一致性，避免人为疏忽
1. **迭代优化** - 每次发现新问题或更好的做法，就更新这些"固化的知识"，Agent 的能力随之提升

本质上是把**隐性知识显性化**，把**经验驱动变成规则驱动**。

这也意味着 Agent 的质量上限取决于你固化进去的知识质量。垃圾进，垃圾出；好的经验进，稳定的高质量输出。

### 为什么需要固化知识

LLM 的知识覆盖面极广，解决同一个问题可能有多条路径，但其中只有少部分是最佳实践。具体输出什么内容，很大程度上取决于提示词的质量。

把已验证的解决方案固化到 Agent 里，能让 Agent 在特定领域有更稳定、更优质的表现——相当于给 LLM 划定了一条"黄金路径"，避免它在众多可能性中随机游走。

## 常用技术栈

1. 编程语言

- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）

1. 大语言模型与 API

- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）

1. Web 框架与服务

- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django

1. 数据存储

- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate

1. 消息队列与异步任务

- Celery、RabbitMQ、Kafka

1. 容器与部署

- Docker、Kubernetes
- 云服务：AWS、Azure、GCP

1. 前端交互

- React、Vue.js
- WebSocket、RESTful API

1. 其他

- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana

## Python 调用模型方式

AI Agent 用 Python 开发时，可以调用本地模型或云端模型：

- 本地模型：如 Llama、GPT、transformers，可用 Hugging Face Transformers、llama.cpp 等库加载。
- 云端模型：如 OpenAI、Azure、百度文心、阿里通义，通过 HTTP API 或官方 SDK 远程调用。

选择本地或云端，取决于算力、数据安全、成本和功能需求。两者都支持 Python 调用，代码实现也很方便。

## AI Agent 外层代码与模型调用说明

AI Agent 通常用一种编程语言（如 Python、JavaScript、Go 等）编写外层逻辑代码，负责任务编排、数据处理、接口交互等。
最终核心智能部分是通过调用大语言模型（本地或云端）来实现推理、生成、理解等能力。

外层代码负责"连接"和"控制"，模型负责"智能"。两者结合，才能实现完整的 AI Agent。

## A2A 协议（Agent-to-Agent Protocol）

A2A 协议是一种用于实现 AI Agent 之间通信和协作的标准化协议。它定义了不同 Agent 系统之间如何交换信息、协调任务和共享资源。

### 核心特性

1. **标准化通信**：定义统一的消息格式和交互规范，使不同平台、不同语言开发的 Agent 能够互相通信
1. **任务协调**：支持 Agent 之间的任务分配、委托和结果汇总
1. **能力发现**：Agent 可以查询和发现其他 Agent 的能力和服务
1. **安全认证**：提供身份验证和授权机制，确保通信安全

### 主要应用场景

- **多 Agent 协作**：多个专业 Agent 协同完成复杂任务
- **Agent 编排**：构建 Agent 工作流，实现任务的自动化分发和执行
- **跨平台集成**：连接不同厂商、不同技术栈的 Agent 系统
- **分布式智能**：在分布式环境中实现 Agent 的协同决策

### 相关技术标准

- **MCP (Model Context Protocol)**：用于 Agent 与工具/数据源的连接
- **OpenAI Agents API**：OpenAI 提供的 Agent 通信接口
- **LangGraph**：支持多 Agent 协作的编排框架

A2A 协议使得构建大规模、可扩展的多 Agent 系统成为可能，是 AI Agent 生态系统中的重要基础设施。

## 专题文章

本文是 AI Agent 开发的总览。细节按主题拆到下列文章：

| 主题 | 文章 |
| ---- | ---- |
| Token 分层路由（本地匹配 / 缓存 / 模型） | [Agent Token Routing](./agent-token-routing.md) |
| VSCode 扩展桥接 Copilot 模型 | [VSCode Copilot Model Bridge](./agent-vscode-copilot-bridge.md) |
| 意图识别与槽位填充 | [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md) |
| Function Calling | [Function Calling](./agent-function-calling.md) |
| ReAct 与其它工具调用方式 | [Tool Calling Patterns](./agent-tool-calling-patterns.md) |
| 思维链 CoT | [Chain of Thought (CoT)](./agent-chain-of-thought.md) |
| 输出约束 | [Output Constraint](./agent-output-constraint.md) |
| LangChain | [LangChain](./langchain.md) |
| LlamaIndex | [LlamaIndex](./llamaindex.md) |

相关概念总览另见 [AI Agent](./ai-agent.md)；实践 tip 见 [AI Agent Tips](./ai-agent-tips.md)。

## 术语与缩写对照表

### 核心概念

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **AI Agent** | Artificial Intelligence Agent | 人工智能代理 | 能够感知环境、做出决策并执行动作的智能系统 |
| **LLM** | Large Language Model | 大语言模型 | 在海量文本数据上训练的深度学习模型，如 GPT、Claude |
| **NLU** | Natural Language Understanding | 自然语言理解 | 使计算机理解人类语言含义、意图和上下文的技术 |
| **NLP** | Natural Language Processing | 自然语言处理 | 处理和分析人类语言的计算机技术领域 |

### 协议与标准

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **A2A** | Agent-to-Agent Protocol | 代理间通信协议 | AI Agent 之间通信和协作的标准化协议 |
| **MCP** | Model Context Protocol | 模型上下文协议 | Agent 与工具/数据源连接的标准协议 |
| **LSP** | Language Server Protocol | 语言服务器协议 | 编辑器与语言服务器之间的通信协议 |
| **JSON-RPC** | JSON Remote Procedure Call | JSON 远程过程调用 | 基于 JSON 的远程过程调用协议 |

### AI Agent 技术

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **RAG** | Retrieval-Augmented Generation | 检索增强生成 | 结合检索和生成的 AI 技术，提高答案准确性 |
| **Function Calling** | - | 函数调用 | LLM 识别意图并调用外部函数/工具的能力 |
| **Tool Use** | - | 工具使用 | Agent 调用外部工具完成特定任务的能力 |
| **Slot Filling** | - | 槽位填充 | 从用户输入中提取特定参数的过程 |
| **Intent Recognition** | - | 意图识别 | 识别用户输入意图并分类的过程 |

### 开发框架与工具

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **SDK** | Software Development Kit | 软件开发工具包 | 用于开发特定软件的工具集合 |
| **API** | Application Programming Interface | 应用程序接口 | 不同软件组件之间交互的接口 |
| **WebSocket** | - | 网络套接字 | 支持双向实时通信的网络协议 |
| **SSE** | Server-Sent Events | 服务器推送事件 | 服务器向客户端推送数据的技术 |
| **REST** | Representational State Transfer | 表述性状态转移 | 一种 Web 服务架构风格 |

### 认证与安全

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **OAuth2** | Open Authorization 2.0 | 开放授权 2.0 | 开放的授权标准，允许第三方应用访问资源 |
| **JWT** | JSON Web Token | JSON Web 令牌 | 用于身份验证和信息交换的开放标准 |
| **API Key** | - | API 密钥 | 用于验证 API 调用者身份的密钥 |

### 数据与存储

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **Vector DB** | Vector Database | 向量数据库 | 专门存储和检索向量嵌入的数据库 |
| **Embedding** | - | 嵌入/向量化 | 将文本转换为数值向量的过程 |
| **NoSQL** | Not Only SQL | 非关系型数据库 | 非传统关系型数据库的统称 |

### 部署与运维

| 术语/缩写 | 全称 | 中文释义 | 说明 |
| ---- | ---- | ---- | ---- |
| **CI/CD** | Continuous Integration/Continuous Deployment | 持续集成/持续部署 | 自动化软件开发和部署流程 |
| **K8s** | Kubernetes | - | 容器编排平台（8 代表中间省略的 8 个字母） |
| **Container** | - | 容器 | 轻量级、可移植的软件运行环境 |

### 常见场景术语

| 术语 | 中文释义 | 说明 |
| ---- | ---- | ---- |
| **Prompt Engineering** | 提示词工程 | 设计和优化 LLM 输入提示的技术 |
| **Context Window** | 上下文窗口 | LLM 能够处理的最大输入文本长度 |
| **Token** | 词元/标记 | LLM 处理文本的基本单位 |
| **Temperature** | 温度参数 | 控制 LLM 输出随机性的参数 |
| **Streaming** | 流式输出 | 逐步返回结果而非一次性返回 |
| **Multi-turn Conversation** | 多轮对话 | 支持上下文连续的对话交互 |

## AI Agent 的上下文丢失问题

AI Agent 在工作过程中确实存在**上下文丢失（Context Loss）**的问题，这是当前 Agent 系统的核心挑战之一。

### 问题来源

**1. 上下文窗口有限**

LLM 的上下文窗口（Context Window）有上限（如 Claude 约 200K tokens、GPT-4 约 128K tokens）。当任务执行时间长、对话轮数多，较早的信息会被截断丢弃。

**2. 长任务执行中的信息衰减**

Agent 执行多步骤任务时，早期的决策依据、工具返回结果、用户原始意图可能随着上下文滚动被挤出，导致后续步骤「忘记」前提条件。

**3. 多 Agent 协作中的信息传递损耗**

在 A2A 场景下，Agent 之间传递信息时往往只传摘要或部分结果，细节会丢失。

**4. 模型本身的注意力衰减**

即使信息仍在上下文窗口内，LLM 对较远位置的内容注意力权重也会降低，导致「虽然没丢但实际上忽略了」的情况。

### 常见应对策略

| 策略 | 说明 |
| ---- | ---- |
| **Memory 系统** | 显式维护短期/长期记忆，将重要信息存到外部存储（如文件、数据库） |
| **RAG（检索增强）** | 按需从向量数据库检索相关历史，而非全量塞入上下文 |
| **上下文压缩/摘要** | 定期将旧上下文摘要化，保留关键信息 |
| **状态外化** | 将任务状态、中间结果写入文件或数据库，不依赖上下文传递 |
| **Checkpoint** | 长任务分阶段保存进度，失败可从断点恢复 |
| **结构化指令** | 用强格式（JSON/YAML）规范输出，减少歧义和遗漏 |

### 实际影响与实践建议

这个问题在实践中非常普遍，尤其是以下场景：

- **大型代码库重构**：跨文件的修改依赖早期分析结论
- **长文档处理**：文档前后的信息需要关联理解
- **多步骤工作流**：后续步骤依赖前序步骤的上下文

**实践建议：**

1. **显式记录关键决策**：将重要的中间结论写入文件，不依赖模型记住
1. **任务粒度拆分**：将复杂任务拆成小任务，每个任务都携带必要的上下文
1. **规则文件外置**：把知识和约束写成 `AGENTS.md`、`SKILL.md` 等文件，每次任务都注入
1. **使用 Memory 工具**：利用 `/memories/` 等持久化存储跨会话记忆关键信息

这也是为什么优秀的 Agent 工作流需要显式的规则文件和 Memory 系统——把关键知识「外置」，而不是依赖模型的上下文窗口记忆。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | ---- | ---- |
| 2026-07-23 | 拆分为 hub + 多篇专题；删除重复技术栈草稿段；增加专题索引 | 原文过长、多主题混杂，便于独立检索与维护 |

