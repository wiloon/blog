---
title: "ADR vs Task Spec：工程文档怎么分工"
author: "-"
date: 2026-06-28T12:05:00+08:00
lastmod: 2026-06-28T12:05:00+08:00
url: adr-vs-task-spec
categories:
  - AI
tags:
  - ADR
  - spec
  - documentation
  - remix
  - AI-assisted
---

## 一句话区别

- **ADR**（Architecture Decision Record，架构决策记录）回答 **「为什么这么定」**——记录一个决策和它的理由，拍板后基本不动。
- **Task Spec**（任务规格）回答 **「要做什么、怎么做、做到什么算完」**——指导一次具体落地，随实施更新，是活文档。

一个朝后看（沉淀已做的决策），一个朝前看（驱动待做的执行）。

## ADR 是什么

ADR 记录一个「架构上重要」的决策：背景、考虑过的方案、最终选择、以及由此带来的后果。它的价值在于把「当初为什么选 A 而不是 B」留存下来，避免几个月后自己或他人重新踩坑、甚至无意推翻。

典型结构（Michael Nygard 的经典五段）：

```markdown
# ADR-0001: 标题

## 状态
Accepted / Proposed / Superseded

## 背景
什么力量/约束逼出了这个决策

## 决策
我们选了什么

## 后果
接受了哪些代价、带来哪些影响
```

关键特性：

- **不可变**：决策变了不要改旧文件，而是新写一条 ADR，引用并标记旧的为 superseded。删除会抹掉历史，正是它要避免的。
- **短小**：通常 200–500 字，只讲决策本身，不写实现细节。
- **进版本库**：和代码放一起（常见 `docs/adr/`），让「为什么」就在工程师能找到的地方。

## Task Spec 是什么

Task Spec 描述一个待完成任务的规格：目标、范围（含「不做什么」）、接口/行为契约、约束、验收标准。它是给「这次要做的事」立一个清晰的「完成」定义，让人和 AI 都按同一份契约推进。

```markdown
## 目标
实现用户登录 API

## 范围
- 包含：POST /api/login、JWT 签发
- 不包含：注册、OAuth

## 约束
- 密码不得明文记录

## 验收
- [ ] 正确凭证返回 JWT
- [ ] 错误凭证返回 401
```

关键特性：

- **活文档**：随实施推进更新状态、勾选验收项，完成后归档。
- **面向执行**：聚焦「怎么做、做到什么程度」，可直接转化为测试用例。
- **复杂才写**：小改动几句话即可，不必为每个任务都立 Spec。

## 核心区别

| 维度 | ADR | Task Spec |
| ---- | ---- | ---- |
| 回答 | 为什么这么定 | 做什么 / 怎么做 / 怎样算完 |
| 时间朝向 | 朝后（已做的决策） | 朝前（待做的执行） |
| 结构 | 背景 / 方案 / 决策 / 后果 | 目标 / 范围 / 约束 / 验收 |
| 生命周期 | 拍板后不可变（变更另开新 ADR） | 活文档，随实施更新后归档 |
| 篇幅 | 短（200–500 字） | 视任务复杂度，可长可短 |
| 典型位置 | `docs/adr/` | `docs/tasks/` 等 |

## 它们是哪个领域的概念

这是容易混淆的地方——ADR、Task Spec、SDD、Harness Engineering 不在同一抽象层级：

| 概念 | 性质 | 来源领域 |
| ---- | ---- | ---- |
| ADR | 具体**文档类型** | 软件架构实践。Michael Nygard 于 2011 年提出，后被 ThoughtWorks 技术雷达列入 Adopt |
| Task Spec | 具体**文档类型** | 软件工程通用规格说明，由来已久 |
| SDD | **方法论** | Spec-Driven Development：先写 spec 再实现，AI 辅助开发时代被重新强调 |
| Harness Engineering | **工程学科 / 体系** | AI agent 领域，2026 年初兴起 |

换句话说：

- **ADR 和 Task Spec 是「文档」**——你手里实际写出来的东西。
- **SDD 是「方法论」**——主张「先把规格（spec）写清楚，再让 AI/人去实现」。Task Spec 是 SDD 流程里的核心产物之一；ADR 不是 SDD 专属，它来自更早的软件架构实践。
- **Harness Engineering 是「学科」**——围绕 AI agent 的可靠性，把 ADR、Task Spec、状态锚点、约定文件（`AGENTS.md`）等都纳入 agent 的「外层 harness / 记忆层」。它的公式是 `Agent = Model + Harness`：模型之外的一切（上下文、工具、约束、反馈）都是 harness。

所以三者是包含关系：**Harness Engineering（学科）⊃ SDD（方法论）⊃ Task Spec / ADR（文档）**。ADR 严格说先于这三者存在，AI 时代被这套体系「收编」进来当作 agent 的长期记忆。

详见本站 [Harness Engineering 与状态锚点](./harness-engineering.md) 与 [Spec-Driven Development 与 Vibe Coding](./spec-driven-development.md)。

## 何时用哪个

| 场景 | 用什么 |
| ---- | ---- |
| 做了个有取舍、将来要解释「为什么」的选择 | ADR |
| 要落地一个有点复杂、需要对齐「完成标准」的任务 | Task Spec |
| 既有取舍又有落地 | 两个都写，分开 |
| 小改动、一次性脚本 | 都不用，提交信息说清即可 |

## 两者如何配合

最自然的用法是**一对组合**：ADR 锁定方向，Task Spec 负责落地。

以本站把任务管理升级为 Linear Cycle 为例：

- **ADR-0001** 记录「为什么采用 1 周 Cycle」——候选方案对比、为什么不选 2 周、承诺方式如何改变。拍板后不动。
- **TASK-SPEC-linear-cycle-adoption** 记录「怎么落地」——要改哪些设置、迁移哪些 issue、成功标准、回滚步骤。随实施打勾更新。

两份用链接互相引用：Spec 顶部「决策依据 → ADR」，ADR 底部「落地 → Spec」。这样「为什么」和「怎么做」各有归属，互不污染：

```text
ADR（为什么 + 拍板，稳定）
   │ 引用
   ▼
Task Spec（怎么做 + 验收，活文档）
   │ 产出
   ▼
实现 + 测试
```

## 小结

- **ADR = 决策的墓碑**：刻下来就不改，要变就立新碑（superseded）。
- **Task Spec = 施工图**：边干边改，完工归档。
- 它们是「文档」；SDD 是「用 spec 驱动实现」的方法论；Harness Engineering 是把这些文档组织成 AI agent 可靠运行环境的学科。
- 实战里常常成对出现：先写 ADR 定方向，再写 Task Spec 管落地。

## 参考

- [Documenting Architecture Decisions – Michael Nygard (2011)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Architecture Decision Record – Martin Fowler](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [ADR GitHub Organization](https://adr.github.io/)
- [Harness engineering for coding agent users – Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)
