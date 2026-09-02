---
title: "Loop Engineering：让 Agent 循环到可验证的完成状态"
author: "-"
date: 2026-07-31T09:01:25+08:00
lastmod: 2026-09-02T14:18:35+08:00
url: loop-engineering
categories:
  - AI
tags:
  - AI
  - loop-engineering
  - claude-code
  - agent
  - remix
  - AI-assisted
---

## 什么是 Loop Engineering

Loop Engineering 是 2026 年上半年在 AI Agent 圈子里逐渐流行的说法。它的核心思路是：与其由人逐步编写 Prompt、检查结果、再发出下一条指令，不如先设计一个自动循环系统，明确目标、检查方式和停止条件，让 Agent 按照「感知 → 行动 → 观察 → 再决策」的过程反复迭代，直到任务达到可验证的完成状态。

每个 Agent 本质上都运行在某种循环中。Loop Engineering 关注的是有意识地设计这个循环，包括：Agent 每轮能看到什么、可以执行什么操作、如何取得反馈、谁负责判断完成，以及什么情况下必须停止。

这个模式可以追溯到 ReAct（Reason + Act）范式：模型推理后采取行动，再根据环境返回的观察结果继续推理。Loop Engineering 将这种「推理—行动—观察—重复」的过程扩展为可控制、可验收的工程流程。

## 与 Prompt Engineering 的区别

| 维度     | Prompt Engineering         | Loop Engineering                       |
| -------- | -------------------------- | -------------------------------------- |
| 人的工作 | 编写当前这一步的指令       | 设计目标、反馈、验证和停止条件         |
| 执行方式 | 通常是一次或少量交互       | 自动进行多轮迭代                       |
| 完成判断 | 人或执行任务的模型临场判断 | 预先定义的检查器或验收条件             |
| 适用场景 | 问答、生成单个结果、短任务 | 自动代码生成、软件维护、多步骤自主任务 |

两者不是替代关系。清晰的 Prompt 仍然是循环中每一步的输入；Loop Engineering 解决的是如何让这些步骤持续运行，并在正确的时机停下来。

## 一个循环需要哪些部分

一个可用的 Loop 通常包含以下要素：

- 目标：最终需要达到的状态，而不只是要执行的动作。
- 行动范围：Agent 可以读取、修改和执行哪些内容。
- 反馈：测试、构建、CI、部署状态或其他环境输出。
- 完成条件：可以重复执行并得到明确结果的验收检查。
- 状态：跨轮次保存的需求、进度、失败摘要和已完成事项。
- 停止条件：成功、达到最大轮次、超时或遇到不可恢复错误。

完成条件应尽量由测试退出码、构建结果、文件状态等客观信号表达，而不是让 Agent 根据自己的回答判断「应该已经完成」。这也是 [Harness Engineering](./harness-engineering.md) 能为 Loop 提供的关键能力：Loop 决定继续还是停止，Harness 提供可重复的验收信号。

## Claude Code 中的 Loop 机制

Claude Code 提供了几种不同层级的循环方式。简单任务可以留在当前会话内，长时间运行或需要隔离上下文的任务可以交给外部脚本。

### `/goal`：循环直到满足完成条件

`/goal` 用于设定一个可验证的完成条件。每轮工作结束后，由独立的小模型检查条件是否满足；如果不满足，Claude Code 会自动开始下一轮，而不需要用户反复输入「继续」。

```text
/goal test/auth 下的测试全部通过，lint 命令退出码为 0，且不要修改其他测试文件；最多运行 20 轮
```

一个合适的 Goal 通常写明：

- 可衡量的终态，例如测试通过、构建成功或目标文件达到指定状态。
- 明确的验证方式，例如 `npm test` 的退出码为 `0`。
- 不允许改变的约束，例如不能删除测试或修改无关模块。
- 最大轮次或时间限制，防止任务无法收敛时持续运行。

在非交互模式中也可以将 `/goal` 交给 `claude -p`：

```bash
claude -p "/goal CHANGELOG.md 包含本周每个已合并 PR 的条目；最多运行 10 轮"
```

它适合需要多轮修复才能收敛的任务，例如迁移调用点直到编译通过、按设计文档实现功能直到验收通过、按体积预算拆分模块，或者逐项处理 Issue 列表。

### `/loop`：按间隔重复执行 Prompt

`/loop` 更适合轮询，而不是持续修改同一个任务。例如每隔五分钟检查一次部署状态：

```text
/loop 5m 检查部署是否完成，并报告结果
```

不给间隔时，Claude Code 可以动态决定下次检查时间；不给 Prompt 时，则执行内置的维护型任务，例如检查未完成工作、PR 评论和 CI 失败。项目还可以通过 `.claude/loop.md` 定义默认循环内容。

会话内的调度任务有数量和存活时间限制：最多保留 50 个任务，递归任务会在 7 天后过期。因此，长期、脱离会话的调度更适合放到 Routines、GitHub Actions 或桌面端定时任务中。

### Headless 模式与 Ralph 循环

Ralph 技术由 Geoffrey Huntley 在 2025 年提出。它使用外部 Shell 循环不断把同一组任务指令交给 Agent，直到完成条件满足，是外部驱动式 Loop Engineering 的典型实现。

Claude Code 可以通过 `claude -p` 以 Headless 模式运行。每次调用都是新的 Context，需求文件和进度文件承担跨轮次状态存储的职责：

```bash
#!/usr/bin/env bash
set -euo pipefail

for iteration in $(seq 1 20); do
  output=$(claude -p "读取 feature-requirements.md 和 progress.txt。
选择一个未完成任务并实现，运行测试，然后更新 progress.txt。
如果所有需求都已通过验证，只输出 <promise>DONE</promise>。" \
    --allowedTools "Read,Edit,Write,Bash" \
    --permission-mode acceptEdits)

  printf '%s\n' "$output"
  if grep -q '<promise>DONE</promise>' <<<"$output"; then
    exit 0
  fi
done

printf '%s\n' "Loop stopped after reaching the iteration limit." >&2
exit 1
```

这个示例刻意设置了 20 轮上限，并根据捕获到的输出判断是否结束。生产脚本还应使用测试或独立检查器复核完成状态，不能只信任 Agent 输出的 `DONE`。

Ralph 循环的几个关键点是：

- 每轮使用干净 Context，减少长会话中的上下文污染。
- 用需求文件、进度文件和 Git 历史保存跨轮次状态。
- 每轮只选择一个范围明确的任务，降低一次修改的复杂度。
- 用测试、lint、类型检查或构建结果定义完成，而不是依赖口头结论。
- 同时设置成功条件与最大轮次，保证循环可以停机。
- 在容器、devcontainer 或独立 Git Worktree 中运行，并限制工具权限和文件范围。

不要为了省去权限配置而直接在主机和主工作区中使用 `--dangerously-skip-permissions`。自动循环会放大错误操作的影响，隔离环境和最小权限比单轮交互更重要。

### Stop Hook：自定义确定性检查

如果基于模型的完成评估不够精确，可以使用 Stop Hook 在每轮结束时执行自定义检查。Hook 可以直接运行测试、读取状态或检查文件，由退出码决定是否允许结束。

`/goal` 可以看作会话范围内预置的、基于 Prompt 的 Stop Hook 封装。自定义 Hook 的优势是可以使用确定性脚本，避免让模型解释一个本来可以由命令直接判断的结果。

### 脱离当前会话的调度

需要在会话关闭后继续执行时，可以按运行环境选择：

- Routines：由云端托管，不依赖本机或当前 Session。
- GitHub Actions：通过 `schedule` 或仓库事件在 CI 中执行。
- 桌面端 Scheduled Tasks：按计划在本机运行，并访问本地文件。

这些机制负责「何时启动」，Goal、Hook 或外部状态机仍然负责「何时算完成」。

## `/goal` 与直接描述任务的差别

核心区别不是 Agent 能否执行任务，而是谁判断完成，以及条件不满足时是否自动进入下一轮。

| 维度       | 直接描述任务           | 使用 `/goal`               |
| ---------- | ---------------------- | -------------------------- |
| 完成标准   | 执行过程中临场判断     | 用户预先定义可验证条件     |
| 判断者     | 执行任务的同一个模型   | 独立的评估模型             |
| 条件不满足 | 通常停下并等待用户继续 | 自动开始下一轮             |
| 交还控制权 | 模型认为完成或不确定时 | 评估器确认完成或触发上限时 |

一两轮可以完成的简单任务不一定需要 `/goal`。当任务必须经历多轮修复，并且不希望人工逐轮确认时，预先声明完成条件的收益才会明显。

## 如何选择

| 需求                                | 机制                       |
| ----------------------------------- | -------------------------- |
| 当前 Session 内持续工作到条件满足   | `/goal`                    |
| 当前 Session 内按固定或动态间隔检查 | `/loop`                    |
| 脱离交互，多轮实现 PRD 中的任务     | Headless 模式 + Ralph 循环 |
| 使用确定性逻辑检查完成状态          | Stop Hook                  |
| 不依赖本机和当前 Session            | Routines 或 GitHub Actions |
| 本机定时访问本地文件                | 桌面端 Scheduled Tasks     |

## 与 Graph Engineering 的关系

Loop Engineering 适合围绕一个目标反复执行「修改 → 验证 → 再修改」。当任务扩大到多个角色、多个阶段和不同失败路径时，可以用 [Graph Engineering](./graph-engineering.md) 管理节点之间的编排，再把 Loop 放进某个需要迭代的节点中。

两者的边界可以概括为：Loop 管理同一任务如何收敛，Graph 管理多个任务和角色如何流转。无论采用哪一种方式，完成条件都应该尽可能由独立、可重复执行的验证机制提供。

## 一套按此组织的工作流

Matt Pocock 的 Agent Skills 集合把 Loop Engineering、Spec-Driven Development 和 Harness Engineering 串成一条从想法到上线的流水线：前面用连续追问逼清需求、用 spec 和 ticket 固定范围，后面让 TDD 和验证循环自己收敛，人只在 checkpoint 看决策就绪的摘要。它是把本文思路组织成可照着走的步骤的一个例子，详见 [Matt Pocock 的 Agent Skills 与 Loop Engineering](./matt-pocock-skills.md)。

## 小结

Loop Engineering 的重点不是让 Agent 无限制地运行，而是把循环设计成一个可观察、可验证、可停止的系统。目标要明确，反馈要及时，状态要能跨轮次保存，验收要尽量确定，权限和运行环境要隔离，同时始终保留失败上限。具备这些条件后，多轮 Agent 才从「反复试一试」变成可管理的工程流程。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-09-02 | 新增「一套按此组织的工作流」小节，链接到 Matt Pocock 的 Agent Skills 一文 | 补充与该 skills 集合的关系 |