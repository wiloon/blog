---
title: "Graph Engineering：Python + LangGraph + Claude Code"
author: "-"
date: 2026-07-24T15:08:44+08:00
lastmod: 2026-07-30T12:16:38+08:00
url: graph-engineering-practice
categories:
  - AI
tags:
  - AI
  - langgraph
  - claude-code
  - agent
  - original
  - AI-assisted
---

## 从 Prompt 到 Graph

AI 驱动开发大致走过几条主线：Prompt Engineering 解决「怎么说清楚」；Context Engineering（含 RAG）解决「给模型看什么」；Loop Engineering 解决「让 Agent 自我修正」——给一个任务，改代码、跑测试，失败了再继续修。

复杂业务里，单 Agent 的 Prompt Loop 很快会顶到天花板。Graph Engineering（图工程）把流程拆成有向图：节点专职分工，边负责确定性控制流，AI 只承担局部推理与代码生成。下面按「为什么需要 → 怎么划职责 → 怎么落地」写一版可落地的骨架。

不想额外起 Python 主控、只在 Claude Code 里管多阶段任务时，见 [Graph Engineering：纯 Claude Code 实现](./graph-engineering-claude-code.md)。

## 为什么需要 Graph Engineering

Loop Engineering 在「单任务、短轮次」时很好用。一旦任务变长、角色变多，常见会撞上三类问题。

### 上下文污染（Context Pollution）

循环次数上去后，会话里堆满历史报错、半成品 diff、无效尝试。模型要在噪声里找有效信号，表现会越来越差：重复改同一处、忽略刚写过的约束、或「修 A 弄坏 B」。根因往往不是模型突然变笨，而是上下文被污染了。

### 缺乏确定性控制（Nondeterminism）

若下一步完全由 LLM 在 Context 里自行决定，容易陷入死循环：同一失败路径反复尝试，或越改越散。控制流（何时重试、何时换策略、何时中止）若也交给模型，系统就缺少可预期的停机条件。

### 职责模糊

让同一个 Agent 同时做架构规划、写前后端、跑单测、做 Code Review，等于把多种能力边界揉进一次长会话。结果常常是：规划被实现细节冲淡，实现被 review 口径扯偏，测试结论又被前序噪声干扰。

Graph Engineering 的应对方式很直接：用有向图把复杂流程解耦为专职节点（Nodes）；把控制流交还给确定性的代码（Edges）；只把局部推理与代码生成交给 AI。

## Graph Engineering 在说什么

可以把它看成三层分工：

| 层 | 谁负责 | 典型内容 |
| ---- | ------ | -------- |
| 控制流 | 确定性代码（图的边、条件分支） | 成功/失败路由、最大重试、强制中止 |
| 专职节点 | 窄职责的 Agent 或纯代码步骤 | 后端实现、前端改动、重构、跑测 |
| 局部推理 | 单次短上下文里的 LLM 调用 | 读相关文件、生成补丁、解释失败原因 |

图不是为了「看起来高级」，而是为了把「该不该继续」和「这一步该谁做」从 Prompt 里抽出来，变成可审查、可测试的代码。

## 架构：指挥官、执行者与 quality gate

一套相对稳的 Graph Engineering 系统，通常明确区分三类角色。

### 指挥官：LangGraph（Python 主控）

主控进程用 Python + [LangGraph](./langgraph.md) 描述状态机：节点之间怎么连、失败时走哪条边、状态里存什么（任务描述、当前失败摘要、产物路径等）。指挥官自己尽量少「写业务代码」，而是调度与裁决。

### 执行者：Claude Code 子进程

需要写代码、改仓库、做局部重构时，由主控调起 [Claude Code](./claude-code.md) 进程。不同节点对应不同职责，例如：

- 进程 A：后端逻辑
- 进程 B：前端或跨层重构

关键点是：每个执行者拿到的是窄任务 + 干净（或刻意裁剪过）的上下文，而不是整段污染后的长对话。一次节点跑完，主控只回收结果摘要与必要产物，再进入下一节点。

### quality gate：纯代码步骤（如 pytest）

「硬闸门」不是 AI agent 领域里固定的中文术语；英文更常见的说法是 quality gate（质量闸门），agent engineering 材料里也会写成 verification gate 或 deterministic gate。含义接近：不经过模型裁决、对同一输入给出可重复的 pass/fail，用来挡住「Agent 自称做完了」这类不可信结论。文中的「硬」强调 blocking——失败就不能往下走，而不是 LLM review 那种可商量的 soft check。

测试、lint、类型检查、构建这类步骤不要再「请模型判断是否通过」。用确定性命令跑，exit code 写进图状态，由边决定：通过则前进，失败则回到指定修复节点，或达到上限后失败退出。

示意如下：

```text
                  +-----------------------------------+
                  |   LangGraph (Python 主控进程)     |
                  +-----------------------------------+
                     /              |              \
      (node: spawn)          (node: code)       (node: spawn)
                    /               |               \
                   v                v                v
      +-------------------+   +-----------+   +-------------------+
      | Claude Code 进程 A|   | pytest    |   | Claude Code 进程 B|
      |  (backend)        |   | (quality  |   |  (frontend/refactor)|
      |                   |   |  gate)    |   |                   |
      +-------------------+   +-----------+   +-------------------+
```

边（Edges）上写清规则，例如：pytest 失败 → 带「失败摘要」回到修复节点；连续失败 N 次 → END；通过 → 进入下一专职节点。模型不再负责「我觉得可以再试一次」。

## 落地时要注意的几件事

### 节点边界按职责切，不按「再问一句」切

切图的依据是能力边界：规划 / 实现 / 验证 / 审查。不要为了多一次 LLM 调用就多一个节点；节点太多会把状态机本身变成负担。

### 上下文按节点重置，只传递摘要

对抗 Context Pollution 的主手段是：节点之间不默认继承完整对话。主控状态里保留结构化字段（目标、约束、上一次失败的精简日志、相关文件路径），执行者启动时重新组装 prompt。需要历史时，显式写入状态，而不是依赖聊天窗口滚动条。

### 控制流写在边里，写进代码

重试次数、是否允许改测试、是否允许扩大改动范围，都应是图配置或 Python 条件，而不是塞进 system prompt 指望模型遵守。LLM 适合在节点内做局部决策；全局编排应可静态阅读。

### quality gate 尽量不可旁路

若「测试失败也能继续」完全由模型口头决定，quality gate 就失效了。失败路径可以回到修复节点，但「什么叫通过」必须由命令与断言定义。

### 与 Loop、Harness 的关系

Loop Engineering 仍然有用：它往往落在某一个修复节点内部（改 → 测 → 再改）。Graph Engineering 管的是节点之外的编排。验证侧可以和 [Harness Engineering](./harness-engineering.md) 互补：图决定何时跑 harness；harness 决定「完成」的客观标准。

## 小结

Graph Engineering 不是换一个更炫的 Agent 框架口号，而是一次职责回迁：把控制流从 Context 里拿回确定性代码，把长对话拆成专职短任务，把通过与否交给 quality gate。Python + LangGraph 负责画图与调度，Claude Code 负责窄范围内的改动，pytest 一类步骤负责说「停」或「过」。单任务 Loop 仍然可以嵌在节点里；一旦业务需要多角色、长流程、可预期停机，就该把 Loop 放进 Graph，而不是让 Graph 退化成一个更大的 Loop。

https://www.aibuilderclub.com/blog/graph-engineering-guide-2026
https://www.eigent.ai/blog/graph-engineering-ai-agents
https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph
https://theaioperator.io/p/what-is-graph-engineering-a-field


## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-26 | 将「硬闸门」统一为 quality gate，并补充 verification / deterministic gate 口径说明 | 对齐 AI agent 领域更常见的英文术语 |
| 2026-07-28 | 新增「只用 Claude Code、不接 LangGraph 时怎么办」，写明轻量（任务队列当 DAG）与重量（子代理 + 独立工作树 + 状态文件）两种落地方案及切换条件 | 实践中用轻量方案跑完一个多阶段任务后，需要把两种方案的边界与取舍记录下来 |
| 2026-07-30 | 将「纯 Claude Code」实现拆至独立文章；本篇只保留 Python + LangGraph 主控路径；标签改回 Spec 要求的 `original` | 两种落地路径主题独立，便于单独检索与维护 |
