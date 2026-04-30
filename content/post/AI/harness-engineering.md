---
title: Harness Engineering 与状态锚点
author: "-"
date: 2026-04-20T13:03:41+08:00
url: harness-engineering
categories:
  - AI
tags:
  - remix
  - AI-assisted
---

## 什么是 Harness Engineering


AI 领域的 Harness Engineering
是一种针对 AI/LLM 应用的测试评估方法论，核心思想是：

构建 eval 套件（评估集）来衡量 AI 输出质量
建立 regression 检测，防止模型更新后效果变差
用数据驱动方式持续改进 prompt 和模型选择

AI 辅助开发的语境下，Harness Engineering 的核心思想是：

用自动化验证手段构建"安全网"，让你能放心接受或拒绝 AI 生成的代码，而不是靠人工肉眼审查。

harness engineering 的核心流程是：

需求（Requirements） → 明确要做什么
测试套件（Test Harness） → 先写测试，定义"完成"的标准
实现（Implementation） → 写代码让测试通过
验证（Verification） → 所有测试绿灯

Harness Engineering 是一种以"脚手架优先"为核心思想的软件开发方法，尤其在 AI 辅助开发场景下越来越受到关注。

"Harness"（脚手架/支撑框架）这个词借用自工程领域，在软件中指围绕核心系统搭建的一套**结构化支撑层**，包括：

- 明确的文档约定（说明系统当前状态、设计决策）
- 测试框架和实验入口（可快速验证变更）
- 状态记录文件（捕捉项目在某个时间点的快照）
- 接口契约和边界定义

它的目标是让代码库对人和 AI 助手都更"可理解、可修改、可安全演进"。

## 状态锚点是什么

**状态锚点（State Anchor）** 是 Harness Engineering 的核心实践之一。

它是一个显式的文档文件（通常命名为 `harness-state.md`、`project-state.md` 等），用来**在某个时间点精确记录系统的当前状态**，就像 Git commit 对代码的作用，它对"上下文"做了一次快照。

### 典型内容

一个状态锚点文件通常包含：

```markdown
## 当前状态（2026-04-09）

### 已完成
- [x] 核心数据模型定义完毕
- [x] API 接口初版上线

### 进行中
- [ ] 用户认证模块（50%）

### 已知问题
- /api/user 接口在并发场景下偶发 500

### 下一步
- 完成认证模块 → 接入集成测试 → 上线 v0.2
```

## 状态锚点的作用

### 1. 消除"现在在哪"的认知负担

每次回到一个项目，最耗时的事情不是写代码，而是重建上下文："上次做到哪了？""这个模块稳定了吗？""还有什么坑没踩完？"

状态锚点直接回答这些问题，让你和协作者可以**零摩擦地进入工作状态**。

### 2. 给 AI 助手提供精确上下文

当你使用 GitHub Copilot、Claude 等 AI 工具辅助开发时，AI 没有持久记忆，每次对话都是全新的。如果你在对话开始时粘贴或引用 `harness-state.md`，AI 可以立刻理解：

- 项目是什么
- 现在处于哪个阶段
- 哪些部分是稳定的，哪些是危险区域
- 接下来的目标是什么

这比每次用自然语言重新解释项目背景要精准、高效得多。

### 3. 保护已验证的进度

开发过程中，"我已经验证过这个能工作"和"这个我没测过"是完全不同的。状态锚点帮助你**显式区分**：

- 经过验证的稳定部分（可以依赖）
- 正在实验中的部分（可能破坏）
- 已知有问题的部分（需要绕开）

这对 AI 辅助开发尤其重要——它防止 AI 在你不知情的情况下"修复"一个你其实已经刻意保留的行为。

### 4. 支撑增量演进

Harness Engineering 强调**小步推进**。每完成一个里程碑，就更新状态锚点，标记新的稳定基线。这样整个项目的演进路径是清晰、可回溯的，类似于在不稳定的地形上一步一步打下安全桩。

## 如何开始

对于个人开源项目，建议在项目根目录或文档目录创建 `harness-state.md`，内容不需要复杂，保持简洁即可：

```markdown
# Project Harness State

## 日期
2026-04-09

## 项目概览
一句话描述项目是什么。

## 当前稳定基线
列出已经可以工作的核心功能。

## 进行中
当前正在做什么实验。

## 已知问题 / 风险点
需要注意的坑。

## 下一个里程碑
到达下一个稳定状态需要完成什么。
```

在每次重要变更后更新它，把它当成"给未来的自己写的交接文档"。

## 总结

| 概念 | 类比 |
|---|---|
| Harness | 项目周围的安全脚手架 |
| 状态锚点 | 项目在某时刻的上下文快照 |
| 更新状态锚点 | 打下新的稳定桩，向前推进 |

状态锚点的本质是：**把"你脑子里知道的事"外化成结构化文本**，让它成为系统的一部分，而不是只存在于记忆中。

## Harness Engineering 完整体系

Harness Engineering 不只是一个状态锚点文件，而是一套由多个组件构成的完整工程体系：

```text
Harness Engineering 完整体系
├── State Anchor          ✅ AGENT_STATE.md
├── Coding Conventions    ✅ CONVENTIONS.md
├── Project Brief         ✅ AGENTS.md / CLAUDE.md
├── ADR                   ✅ docs/adr/ (8 files)
├── Task Specs            ✅ docs/tasks/ (3 files, 仅复杂任务)
├── Skill Files           ✅ ~/.agents/skills/ (全局复用)
└── Protocol / Design Doc ✅ docs/openclaw-integration.md
```

### State Anchor — `AGENT_STATE.md`

项目当前状态的快照文件，记录已完成的里程碑、进行中的任务、已知风险和下一步计划。详见上文"状态锚点"章节。

### Coding Conventions — `CONVENTIONS.md`

编码约定文件，定义项目的代码风格、命名规范、目录结构、提交信息格式等。让人和 AI 助手在生成代码时都遵循一致的约定，减少审查摩擦。

典型内容：

- 语言/框架版本约定
- 命名风格（camelCase、snake_case 等）
- 目录结构说明
- 禁止使用的模式（anti-patterns）
- 提交信息格式（如 Conventional Commits）

### Project Brief — `AGENTS.md` / `CLAUDE.md`

面向 AI 助手的项目说明文件。在对话开始时被 AI 工具自动读取（如 Claude Code 会自动加载 `CLAUDE.md`），用来让 AI 立刻理解：

- 项目是什么、做什么用
- 技术栈和架构决策
- 重要的开发流程约定
- 禁止 AI 做的事情（如不要自动删除文件、不要修改某个模块等）

### ADR — `docs/adr/`

Architectural Decision Record（架构决策记录），每个重要的设计决策对应一个 Markdown 文件，记录：

- 决策背景和问题陈述
- 考虑过的方案
- 最终选择和理由
- 后续影响

ADR 是团队和 AI 理解「为什么这样设计」的关键依据，防止历史决策被遗忘或被无意覆盖。

### Task Specs — `docs/tasks/`

复杂任务的规格说明文件，仅在任务本身足够复杂时才创建（不要为每个小改动都写）。包含：

- 任务目标和验收标准
- 涉及的模块和接口
- 实现约束（性能要求、兼容性等）
- 测试要求

与 ADR 的区别：ADR 记录「已做的决策」，Task Spec 描述「待完成的任务」。

### Skill Files — `~/.agents/skills/`

技能文件存放在全局目录，可跨项目复用。每个 Skill 是一个专项能力的说明文件，告诉 AI 如何完成特定类型的任务，例如：

- `playwright-e2e-testing/SKILL.md` — 如何写 Playwright 测试
- `architecture/SKILL.md` — 如何做架构决策分析
- `grafana-dashboard/SKILL.md` — 如何在 Grafana 创建看板

放在 `~/.agents/skills/` 而非项目目录，使得同一套技能可以在多个项目中被调用，避免重复维护。

### Protocol / Design Doc — `docs/openclaw-integration.md`

接口协议或设计文档，描述系统与外部服务的集成方式、内部模块间的通信协议、数据格式约定等。比 ADR 更偏向「实现细节的规范」，比 Task Spec 更长期有效。

## 体系的设计原则

这套体系遵循几个核心原则：

**最小化原则**：不是每个项目都需要所有组件。小项目可能只需要 `AGENT_STATE.md` + `AGENTS.md`；只在复杂度真正需要时才引入 ADR、Task Specs 等。

**人机共用**：每个文件对人和 AI 助手都有价值。`CONVENTIONS.md` 对新加入的开发者有用，对 AI 也有用；`AGENT_STATE.md` 帮助人快速恢复上下文，也帮助 AI 定位当前状态。

**外化知识**：把存在于开发者脑中的隐性知识（「这个模块不能改」「当时选这个方案是因为…」）转化为可读取的结构化文档，让其成为代码库的一部分。

**渐进引入**：先从状态锚点开始，感受到价值后再逐步引入其他组件，而不是一次性搭建完整体系。
