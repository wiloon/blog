---
title: Linear 使用笔记
author: "-"
date: 2026-06-21T06:45:22+08:00
lastmod: 2026-06-28T11:21:06+08:00
url: linear-usage
categories:
  - agile
tags:
  - linear
  - kanban
  - remix
  - AI-assisted
---

## 背景

选型结论见 [看板工具选型](./kanban-tool-selection.md)，最终选用 Linear。本文记录日常使用中的操作与快捷键，随用随补。

## 视图与布局

### 列表 / 看板切换

在 Issue 视图（Backlog、All issues 等支持布局切换的页面）：

- macOS：`⌘ B` 在列表与看板之间切换
- Windows / Linux：`Ctrl B`

若某个视图默认想用看板：先切到看板布局 → 右上角 **Display options** → **Set as default**。该设置只对当前视图生效，不能全局默认。

### Display options

- macOS：`⇧ V` 打开 Display options
- 看板可按 Status、Assignee、Project、Priority、Cycle 分组

## 导航

| 操作 | macOS | 说明 |
| ---- | ----- | ---- |
| 打开搜索 | `/` | 全局搜索 |
| 新建 Issue | `C` | 快速创建 |
| 我的 Issues | `G` `A` | Go → My issues |
| Backlog | `G` `B` | |
| 看板页 | `G` `D` | Go → Board |
| Inbox | `G` `I` | |

（`G` 开头的是组合键：先按 `G`，松手后再按第二个字母。）

## Issue 操作

| 操作 | macOS |
| ---- | ----- |
| 打开 Issue | `O` `I` |
| 编辑 | `E` |
| 改状态 | `S` |
| 改优先级 | `P` |
| 指派给自己 | `I` |
| 复制 Issue ID | `⌘ .` |
| 复制 git 分支名 | `⇧ ⌘ .` |

## 工作流：状态语义与 Todo 上限

个人使用时，关键不是状态名字本身，而是给每个状态约定清晰的语义，让看板「一眼看出最近要做什么」。我的约定如下。

| 状态 | 语义 | 放什么 |
| ---- | ---- | ---- |
| In Progress | 正在做 | 当前主线，同一时间尽量只放 1 个 |
| Todo | 本周期承诺要做、可勾掉 | 本周 / 下周确定的具体任务 |
| Backlog | 以后做 / 条件触发 / 想法 | 其它全部 |
| Done / Canceled | 已完成 / 不做了 | 归档 |

配套几条习惯：

- **硬截止一律写 Due date**：即使任务在 Backlog，到期 Linear 也会提醒，所以「沉进 Backlog」不等于「忘掉」。这是敢往 Backlog 放东西的前提。
- **Todo 控制在 5 条以内**：超过就失去「近期聚焦」的意义，应该把不紧急的挪回 Backlog。
- **主线放 In Progress**：天天推进的长期事项（如某门技术的学习）放 In Progress，和一次性任务区分开。
- **依赖用 blocks 关系**：有先后顺序的任务（如「先 A 后 B」）用 Linear 的 blocks / blocked by 建立正式关系，而不是只写在描述里，这样即便都在 Backlog 也能看出顺序。

排序上按 Priority（紧急度）而非手动拖拽，避免批量更新时打乱顺序。

## Cycle（迭代周期）

Cycle 是 Linear 内置的「迭代 / Sprint」机制，用来把工作按固定时间窗（常见 1 周或 2 周）切片。它是 Linear 官方方法论（The Linear Method）的核心实践之一——Linear 团队自己就靠短周期 + 硬截止保持交付节奏，所以这套机制在产品里打磨得很成熟。

它和 Todo/Backlog 解决的是不同维度的问题：

- **Status（状态）** 回答「这件事处于什么阶段」
- **Cycle（周期）** 回答「这件事打算在哪一段时间做」

### 核心概念

- **固定时长**：在团队设置里开启 Cycle 后，Linear 按设定的周期长度（如每周一开始、为期 1 周）自动滚动创建。
- **本周期 = 承诺范围**：每个周期开始时，把这一周期打算完成的 Issue 拉进 Current Cycle，相当于「这一周的承诺清单」。
- **自动滚动**：周期结束时，未完成的 Issue 可以自动顺延到下一个周期，避免手动搬运。
- **进度与速率**：Linear 会统计每个周期的完成情况（burndown、velocity），帮助判断自己每周能吃下多少任务。
- **硬截止**：Cycle 的精髓是「到点就切」——没做完的滚到下周期，而不是延长本周期。这种硬截止逼着你做范围取舍，而不是无限期拖延。

### Cooldown（冷却期）

Cooldown 是周期之间的一段可配置缓冲（0–7 天），夹在「上一周期结束」与「下一周期开始」之间。它不是放假，而是给固定节奏留出一段「非交付」时间：

- 跑回顾（retro），不占用下个周期的第一天
- 处理技术债、零散小修、做实验（类似 Google 的 20% 时间，但写进了节奏里，而非临时福利）
- 整理 backlog，让规划不挤占执行时间

冷却期内不能把 Issue 分配到周期。经验值：2 周周期配 1–2 天，4 周配 2–3 天；短周期不建议超过 3 天，否则节奏被打断。常见误区是设 0 天，导致回顾和规划被压在同一时段，规划往往被压缩。个人单人、1 周周期可以先设 0，体验后再调。

一个真实例子：在一些团队里，cooldown 会被排成固定的「非开发周」。我经历过的一个项目，scrum master 在一个月的迭代周期结束后，会专门留出一周不排开发任务，用来做回顾、还技术债、整理与学习。当时不知道这套安排有名字，后来才明白它正是 cooldown 理论的落地——把「收尾 + 喘息」写进节奏本身，而不是靠加班硬接下一轮迭代。

### 个人使用要不要上 Cycle

- **不上 Cycle**：靠 In Progress / Todo / Backlog 三档 + Due date，已经能覆盖「最近做什么」。轻量、零维护，适合任务量不大的个人场景。
- **上 Cycle**：如果希望有「每周固定节奏 + 完成度回顾」，可以开启周 Cycle，每周一把 Todo 里要做的拉进 Current Cycle，周末看完成率。代价是多一层每周的整理动作。

我的取舍：本来打算个人任务先用三档状态 + Due date，但 Cycle 是 Linear 官方推崇的核心实践、风险低，干脆直接上手体验。最终启用了 **1 周 Cycle**（周一起始、cooldown 0），把当前任务拉进当周 cycle 试运行，按 2–3 周的完成率再决定是否长期保留。

### 启用方式

两条路：

- **UI（推荐）**：Settings → Teams → 选择 team → Cycles，设定周期长度、起始日、cooldown 后启用。
- **API（可脚本化）**：用 Personal API Key 调 GraphQL `teamUpdate` mutation，设 `cyclesEnabled: true`、`cycleDuration`、`cycleStartDay`、`cycleCooldownTime` 等字段。适合想把配置写进脚本、可重放的场景。

启用后看板 / Display options 里就能按 Cycle 分组；issue 可通过 `cycle` 字段加入指定周期。

## 参考

- [Board layout – Linear Docs](https://linear.app/docs/board-layout)
- [Display options – Linear Docs](https://linear.app/docs/display-options)
- [Cycles – Linear Docs](https://linear.app/docs/cycles)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | ---- | ---- |
| 2026-06-28 | 新增「工作流：状态语义与 Todo 上限」「Cycle（迭代周期）」两节 | 沉淀个人 Linear 使用约定，并补充对 Cycle 的理解 |
| 2026-06-28 | Cycle 一节补充 cooldown（冷却期）、硬截止，并说明 Cycle 是 Linear 官方最佳实践 | 补全对 Cycle 机制的理解 |
| 2026-06-28 | cooldown 小节补充一个真实团队的「非开发周」例子 | 用亲历经验印证 cooldown 理论 |
| 2026-06-28 | 「个人取舍」改为已采用 1 周 Cycle；启用方式补 API（GraphQL teamUpdate）路径 | 实际启用 Cycle 后同步实操 |
