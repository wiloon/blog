---
title: VS Code Agent Hand Off 机制详解
author: "-"
date: 2026-04-03T12:52:43+08:00
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

## 环境间 Hand Off：Local / CLI / Cloud

VS Code 底部状态栏的下拉菜单提供三个运行环境之间的切换：

| 选项 | 含义 |
|---|---|
| **Local** | 当前 VS Code 本地 agent |
| **Copilot CLI** | 移交到终端 `copilot` CLI 继续 |
| **Cloud** | 移交到 GitHub.com 上的云端 agent 继续 |

这是**环境间**的 hand off，与代码层面 `runSubagent` 的 agent-to-agent 调用是两个不同层次的概念。

### Local 与 CLI 的差异

两者功能高度重叠，差异主要在运行环境：

- **CLI** 更适合无图形界面的环境（SSH 远程服务器、CI/CD 脚本、无头环境）
- **Local** 因为有 GUI，展示工具更丰富（diff 视图、文件树、高亮等）
- 如果本地已经开着 VS Code，Local 模式体验更好，没必要切到 CLI

切换到 Cloud 后，VS Code 会把本地改动 push 到一个 `copilot/` 前缀的新分支，云端 agent 在 GitHub 上独立运行，最终通常会开一个 PR。Local 端的对话依然可以继续，两者互不同步、完全独立。

## 什么时候值得切换到云端

切换到云端的核心价值是**异步、长时间、后台运行**——委托出去后可以关掉电脑去做别的事，回来看 PR 结果。

| | Local agent | Cloud agent |
|---|---|---|
| 执行时间 | 受限于 VS Code 保持开启 | 关掉电脑也在跑 |
| 交互方式 | 实时对话 | 异步，看 PR 结果 |
| 适合任务 | 短、需要频繁交互 | 长、可以无人值守 |

### 值得切换到云端的任务

- 耗时的代码生成：生成大量测试用例、重构整个模块、批量处理文件
- 需要等待的操作：跑 CI/CD、等待构建结果、跑测试套件
- 需要 GitHub 集成：直接在仓库开 PR、操作 Issues、跨分支合并

### 不值得切换的任务

- 问一个问题、解释一段代码 → 秒回，不需要
- 改几行代码 → 本地更快，省去 push/PR 流程
- 需要频繁交互确认的任务 → 云端是异步的，来回成本高

## 委托云端前的准备

云端 agent 一旦开始就很难中途纠正，前期确认越清楚越好。

### 委托前应明确的内容

**目标和范围**

- 做什么，**不做什么**（范围边界很关键）
- 涉及哪些文件/目录，不要动哪些

**结束条件**

- 什么状态算"完成"（所有测试通过？文件生成完毕？）
- 遇到不确定的情况是继续猜测还是停下来等待

**关键路径的预选择**

- 有多种实现方案时，提前指定选哪个
- 明确"用方案 A，不要用方案 B"，而不是让它自己决定

**约束条件**

- 不能修改哪些文件
- 使用什么技术栈/版本
- 是否允许安装新依赖

### 为什么云端比本地更需要提前确认

本地 agent 做错了可以实时打断，说"不对，换个方向"。

云端 agent 是异步的，等你发现它跑偏了：

- 可能已经改了几十个文件
- 已经完成了一半但方向是错的
- PR 已经开出来了，还得 close 再重来

### 实践建议

委托前先在 Local 对话里把任务描述推敲清楚，跑一小段试探性的探索，确认方向没问题再 hand off 到云端。把明确好的"任务说明"直接粘贴到委托的 prompt 里。

## Agent Provider：Copilot 与 Claude

### 两个菜单的区别

新建会话时和已有会话时，底部下拉菜单的内容不同：

| 时机 | 菜单底部文字 | 作用 |
|---|---|---|
| 新会话，未开始 | "Learn about agent types..." | 选择用哪个 agent provider |
| 已有 Copilot 会话 | "Learn about agent handoff..." | 在 Copilot 生态内切换运行环境 |

**Claude** 只出现在新会话菜单里，是让你在开始前选择用 Claude 的 agent 体系驱动会话，而不是 hand off 的目标。一旦 Copilot 会话开始，Claude 就不再出现，因为跨 provider 的 hand off 目前不支持。

### Copilot Agent vs Claude Agent 对比

两者都跑在 VS Code 里、都走 Copilot 账单，核心区别是**驱动 agent 的 SDK 不同**：

| | Copilot Agent | Claude Agent |
|---|---|---|
| Agent 引擎 | VS Code 自有 agent 框架 | Anthropic 官方 Claude Agent SDK |
| 系统提示 | GitHub / Microsoft 定义 | Anthropic 定义 |
| 配置文件 | `copilot-instructions.md`、`AGENTS.md` | `CLAUDE.md`、`.claude/agents`、`.claude/skills`、`.claude/settings.json` |
| Slash commands | Copilot 内置命令 | 支持 Claude Code 专有命令：`/compact`、`/agents`、`/hooks` |
| Hooks | Copilot hooks 格式 | Claude Code hooks 格式（PreToolUse、PostToolUse、SessionStart、Stop） |
| MCP 支持 | 支持 | 支持（0.41 加入） |
| 计费 | Copilot 订阅 | Copilot 订阅 |

### 容易混淆的地方

Copilot 本身可以**以 Claude 作为底层推理模型**：

```
Copilot 里切换模型到 Claude Sonnet
    → 界面和工具链是 Copilot 的，推理用 Claude 模型（换发动机）

新会话菜单选 Claude agent provider
    → 工具链换成 Claude 的，但计费仍然走 GitHub Copilot（换驾驶舱，发动机和油费不变）
```

### Claude agent provider 是什么时候加入的

这是 `github.copilot-chat` 扩展 **0.37（2026-02-04）** 版本内置的功能，不需要单独安装任何 Claude 扩展或配置 MCP server，安装了新版 Copilot Chat 即可使用。

changelog 原文：

> **Claude Agent (Preview)** — Delegate tasks to Claude Agent SDK using Copilot subscription models. Uses official Anthropic agent harness.

关键点：
- **Copilot subscription models**：使用 Copilot 订阅的模型额度
- **official Anthropic agent harness**：底层使用 Anthropic 官方的 Claude Agent SDK

### Claude agent provider 的底层实现

选择 Claude agent provider 后，VS Code 并不是直接调用 Anthropic API。实际链路是：

```
Claude Code / Claude agent
  → http://localhost:38041  （VS Code 在本地起的代理）
  → VS Code Language Models API
  → GitHub Copilot
  → Claude 模型（Anthropic 提供推理）
```

VS Code 会注入两个环境变量：

- `ANTHROPIC_BASE_URL=http://localhost:38041`：将 Anthropic API 请求重定向到本地代理
- `ANTHROPIC_AUTH_TOKEN=vscode-lm-xxxxx`：token 以 `vscode-lm-` 开头，是 VS Code LM API 的凭证，不是 Anthropic API key

因此**不需要 Anthropic API key**，账单走的是 GitHub Copilot 订阅。

### 日常建议

已经在用 VS Code + Copilot 的话，直接在 Copilot 里切换模型到 Claude Sonnet 比切换 provider 更简单，工具链不中断。

切换到 Claude agent provider 更适合以下场景：
- 已经有 Claude Code 的配置文件（`CLAUDE.md`、`.claude/` 目录），希望复用这套配置
- 需要 Claude Code 的 hooks 机制（PreToolUse、PostToolUse 等）
- 偏好 Anthropic 定义的 agent 行为和系统提示
