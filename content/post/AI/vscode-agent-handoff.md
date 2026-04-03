---
title: VS Code Agent Hand Off 机制详解
author: "-"
date: 2026-04-03T10:11:16+08:00
url: vscode-agent-handoff
categories:
  - AI
tags:
  - vscode
  - agent
  - remix
  - AI-assisted
---

## Hand Off 是什么

VS Code Copilot Chat 在 Agent 模式下提供 **"Hand off a session to another agent"** 功能，将当前对话的完整上下文移交给另一个 agent 继续处理。

移交时，接收方 agent 会获得：

- 完整的对话历史记录
- 已收集的文件上下文
- 前一个 agent 的中间结论和工具输出

接收方 agent 可以直接从当前状态继续，而不需要从头重建上下文。

## 与普通切换 Agent 的区别

| | 普通切换 | Hand off |
|---|---|---|
| 上下文 | 丢失，重新开始 | 完整传递 |
| 用途 | 新任务 | 同一任务的延续 |
| 历史记录 | 不带过去 | 带上全部历史 |

## 为什么要切换 Agent，而不是在主 Agent 里继续？

### Fan-out 并行（最核心的理由）

主 agent 收集完上下文后，**同时**把同一份上下文发给多个子 agent 做不同的事：

```
主 agent 分析完代码库
    ├── 子 agent A → 写单元测试
    ├── 子 agent B → 写文档
    └── 子 agent C → 做安全审查
```

主 agent 是单线程的，无法并行处理多个子任务。Fan-out 到多个子 agent 是最强的切换理由。

### 工具权限隔离

不同 agent 有不同的工具集：

- 探索 agent：只读工具，不能写文件（更安全）
- 部署 agent：有 `git push`、`kubectl apply` 权限

主 agent 把"危险操作"推给专门的、可控的子 agent，而不是自己动手。

### 专业化系统提示

Agent 的行为由 system prompt（`.instructions.md`、`AGENTS.md`）决定。切换 agent 本质是**切换专业角色**。同样的上下文，安全审查 agent 和性能优化 agent 关注点完全不同。

### 上下文窗口续命

主 agent 跑了很久，context 快满了。Hand off 时可以带一份**压缩摘要**给新 agent，而不是带全部原始历史，新 agent 在干净的窗口里继续工作。

## 什么时候不需要切换？

任务是线性的、单一责任的、不需要并行时，就没必要切换。切换本身有开销（序列化上下文、启动新 agent），小任务不值得。

## 在 VS Code 中的实现

`runSubagent` 工具是 hand off 的底层实现方式，UI 层面的"Hand off"按钮是其图形化入口。

```
主 agent
  └── runSubagent("Explore", "分析代码库结构")
        └── 返回结果给主 agent 继续处理
```

`AGENTS.md` 里定义的 `Explore` subagent 就是典型例子——主 agent 把"探索代码库"这个子任务 hand off 给 `Explore` agent，等它返回结果后再继续主流程。

## Hand off 是切换到云端了吗？

**不一定**，取决于接收方 agent 使用的模型：

| 接收方 agent | 运行位置 |
|---|---|
| GitHub Copilot（GPT-4o、Claude 等） | ☁️ 云端，推理在 GitHub/Azure 服务器 |
| 本地模型（Ollama、LM Studio） | 💻 本地，推理在自己机器上 |
| 自定义 agent（指向本地 endpoint） | 💻 本地 |

### 实际情况

使用 VS Code 内置的 Copilot Chat 时：

- 默认 agent（`@workspace`、`@github` 等）都是**云端**调用
- Hand off 到另一个内置 agent，仍然是**云端**
- 如果配置了本地模型（`ollama.baseURL`），hand off 到该 agent 则是**本地**

### 上下文传输方式

无论云端还是本地，上下文传输的方式是一样的——把对话历史序列化后通过 API 请求发给下一个 agent。云端 agent 的上下文在 GitHub 服务器处理，不会永久存储（遵循 Copilot 隐私政策）。

> 如果对数据隐私有要求，选用本地模型的 agent 做 hand off，上下文不离开本机。
