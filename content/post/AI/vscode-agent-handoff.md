---
title: VSCode Agent Handoff：将会话移交给另一个 Agent
author: "-"
date: 2026-04-03T10:22:10+08:00
url: vscode-agent-handoff
categories:
  - AI
tags:
  - vscode
  - agent
  - AI-assisted
---

## 什么是 "Hand off a session to another agent"

VSCode 中的 **Hand off a session to another agent** 功能允许你将当前与 AI agent 的对话会话（包括完整的上下文和历史记录）移交给另一个 agent 继续处理。

这个功能出现在 VSCode Copilot 的 agent 模式下，当你需要从本地 agent 切换到云端 agent（或反向切换）时使用。

## 为什么要切换 Agent，而不是在主 Agent 里继续做？

这是一个很好的问题。在以下几种场景中，切换 agent 是有意义的：

### 1. Token 预算耗尽

每个 agent 会话有 token 限制，当 token 预算快用完时，当前 agent 会发起 handoff，将上下文传递给新的 agent，从而绕过单次会话的 token 限制，继续完成任务。

### 2. 利用不同 Agent 的能力

- **本地 Agent**：运行速度快，适合简单的代码编辑、文件操作
- **云端 Agent**：计算能力更强，适合复杂推理、大规模代码分析

当任务变得复杂时，切换到云端 agent 可以获得更强的处理能力。

### 3. 并行工作流

在某些工作流中，可以让多个 agent 并行处理不同的子任务，而不是让一个 agent 串行完成所有事情。

## 如何将上下文传递给下一个 Agent

当你在 VSCode 中点击 agent 选择下拉列表时，会看到 Local 和 Cloud 等选项。切换时，VSCode 会自动将当前会话的上下文（包括对话历史、代码上下文、当前状态等）打包传递给新的 agent。

**操作步骤：**

1. 在 Copilot Chat 面板中，点击 agent 选择下拉列表
2. 选择目标 agent（如从 Local 切换到 Cloud）
3. VSCode 会自动将上下文序列化并传递
4. 新的 agent 会基于完整的历史上下文继续工作

## 云端 Agent 开始工作后，GitHub 页面上的对话还有效吗？

这是一个关于 **GitHub Copilot Coding Agent**（云端 agent）工作机制的重要问题。

### 工作机制

当你通过 GitHub 页面（Issue 或 PR）触发云端 agent 开始工作后：

- **云端 agent 在独立的沙盒环境中运行**，它有自己的代码仓库克隆和执行环境
- **GitHub 页面的对话框** 可以继续使用，但这是一个**新的独立会话**，与云端 agent 正在执行的任务是**相互独立的**

### 是否同步？

**不是同步的。** 具体来说：

- 云端 agent 正在执行的任务（如修改代码、提交 PR）是**异步进行**的
- 你在 GitHub 页面新开的对话是一个**全新的 agent 实例**，不共享云端 agent 的运行状态
- 云端 agent 完成工作后会通过 **PR 或 Issue 评论**的形式反馈结果

### 这个对话框还可以交互吗？

**可以，但要注意：**

1. 你可以继续在 GitHub 页面的对话框中提问或发布新的任务
2. 但这会启动一个新的 agent 实例，而不是与当前正在执行的云端 agent 实时交互
3. 如果你想对正在运行的云端 agent 任务进行干预，需要等待它完成当前任务后，通过 PR 评论等方式进行后续指导

### 类比理解

可以把云端 agent 想象成一个**在后台工作的程序员**：

- 你给了他一个任务（触发 agent）
- 他在自己的工位上工作（独立沙盒）
- 你可以继续去找其他人（新的 agent 实例）聊别的事
- 但你无法实时看到他的工作状态，只能等他完成后提交成果（PR/评论）

## 总结

| 特性 | 说明 |
|------|------|
| 上下文传递 | Handoff 时自动传递完整历史 |
| 云端 agent 是否实时交互 | 否，异步执行 |
| GitHub 对话框是否可用 | 可用，但会启动新的 agent 实例 |
| 与运行中的云端 agent 同步 | 不同步，相互独立 |
