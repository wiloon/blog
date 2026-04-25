---
title: MCP (Model Context Protocol) 是什么
author: "-"
date: 2026-04-25T19:53:49+08:00
url: mcp
categories:
  - AI
tags:
  - mcp
  - AI
  - remix
  - AI-assisted
---

## MCP 是什么

MCP（Model Context Protocol，模型上下文协议）是一个开源标准协议，用于将 AI 应用与外部系统连接起来。

可以把 MCP 理解为 **AI 应用的 USB-C 接口**。就像 USB-C 为电子设备提供了标准化的连接方式，MCP 为 AI 应用与外部系统的连接提供了统一标准。

有了 MCP，Claude、ChatGPT 等 AI 应用可以连接到：

- **数据源**：本地文件、数据库
- **工具**：搜索引擎、计算器、代码执行环境
- **工作流**：自定义 prompt 模板、业务系统

## MCP 解决了什么问题

### 问题背景

在 MCP 出现之前，每个 AI 应用如果想连接外部工具或数据源，都需要为每种组合单独开发集成代码。这导致：

- **重复开发**：A 工具想接 GitHub，B 工具也想接 GitHub，各自写一套
- **维护成本高**：N 个 AI 应用 × M 个外部工具 = N×M 个集成要维护
- **互不兼容**：为 Claude 写的插件不能直接用在 ChatGPT 上

### MCP 的解决方案

MCP 引入了统一的 Client-Server 架构：

- **MCP Server**：外部工具/数据源的提供方，按照 MCP 协议暴露能力
- **MCP Client**：AI 应用（如 Claude、VS Code Copilot），按照协议调用 Server

这样只需要：

- 工具提供方实现一次 MCP Server
- AI 应用实现一次 MCP Client
- 双方就能互联互通，无需额外适配

### 解决的核心痛点

| 痛点 | MCP 的解法 |
| --- | --- |
| 集成碎片化 | 统一协议，一次实现到处复用 |
| 上下文割裂 | AI 可主动拉取外部数据作为上下文 |
| 工具调用不标准 | 定义了 Tools/Resources/Prompts 三种标准原语 |
| 生态封闭 | 开源协议，各厂商平等接入 |

## MCP 能做什么

- AI Agent 访问 Google Calendar、Notion，成为个人助理
- Claude Code 根据 Figma 设计稿生成完整 Web 应用
- 企业聊天机器人连接多个数据库，让用户用自然语言分析数据
- AI 在 Blender 中生成 3D 模型并控制 3D 打印机输出

## MCP 的架构

```
AI 应用 (MCP Client)
        │  MCP 协议 (JSON-RPC over stdio/SSE/HTTP)
        ▼
MCP Server（文件系统 / 数据库 / GitHub / Slack / ...）
```

MCP 协议基于 JSON-RPC 2.0，支持三种传输方式：

- `stdio`：本地进程通信，适合本机工具
- `SSE`：服务器推送事件，适合远程 HTTP 服务
- `Streamable HTTP`：新版推荐方式

## 生态支持

MCP 已被广泛支持：

- **AI 助手**：Claude、ChatGPT
- **开发工具**：VS Code (GitHub Copilot)、Cursor、JetBrains

## 参考

- <https://modelcontextprotocol.io/introduction>
- <https://code.visualstudio.com/docs/copilot/chat/mcp-servers>
- <https://code.visualstudio.com/mcp>
