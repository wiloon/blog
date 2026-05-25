---
title: Spec-Driven Development 与 Vibe Coding
author: "-"
date: 2026-05-24T14:24:06+08:00
lastmod: 2026-05-24T14:31:44+08:00
url: spec-driven-development
categories:
  - AI
tags:
  - AI
  - remix
  - AI-assisted
---

## 什么是 Spec-Driven Development

**Spec-Driven Development（SDD，规格驱动开发）** 是一种 AI 辅助开发方法论：开发者在让 AI 写代码之前，先把需求、边界和验收标准写成结构化的规格说明（Spec），AI 再依据 Spec 生成、修改或引导实现。

Spec 可以是自然语言文档，也可以带接口签名、数据模型、约束条件等结构化片段。核心不是格式，而是 **先定义「完成」长什么样，再让 AI 动手**。

典型 Spec 会回答：

- 要做什么、不做什么
- 输入输出与接口契约
- 边界条件与错误处理
- 验收标准（怎样算通过）

## SDD 与 Vibe Coding 的关系

SDD 和 **Vibe Coding** 关联很强，但方向相反——它们描述的是同一条 AI 协作光谱的两端。

| 维度 | Vibe Coding | SDD |
| ---- | ----------- | --- |
| 输入方式 | 口语化、即兴描述 | 结构化 Spec |
| 意图传递 | 让 AI 猜 | 显式定义边界 |
| 可追溯性 | 低，依赖对话历史 | 高，Spec 可版本管理 |
| 适合场景 | 原型、探索、一次性脚本 | 功能迭代、协作、长期维护 |
| 出错模式 | 方向对但细节偏、隐性假设 | 前期写 Spec 有成本 |

**Vibe Coding** 指用自然、随意的语言驱动 AI 写代码，强调「跟着感觉走」——描述大概想要什么，让模型自行补全细节。Andrej Karpathy 在 2025 年推广了这个说法。它上手快，适合快速验证想法。

**SDD** 则是把 Vibe Coding 里隐含在对话中的假设，提前外化成可审查的文档。不是否定 Vibe Coding，而是在需要 **可重复、可验收、可交接** 时，把协作方式从「猜」升级为「对齐」。

更实用的做法不是二选一，而是分阶段组合——中间有一层 **Vibe-to-Spec**：用 Vibe Coding 的方式和 AI 一起把 Spec 写出来。

## Vibe-to-Spec：用 Vibe 写 Spec，再按 Spec 编码

需求一开始往往是模糊的。如果直接让 AI 写代码，隐性假设会立刻变成代码里的默认值；如果一开始就要求完整 Spec，又容易卡在「不知道该怎么写」。

更好的实践是 **三阶段**：

```text
Vibe 探索 → Vibe-to-Spec（协作写 Spec）→ SDD 编码
```

1. **Vibe 探索**（可选）：快速原型或对话，确认方向可行、边界大致在哪
2. **Vibe-to-Spec**：用口语和 AI 多轮对话，把模糊需求逐渐细化、固化成一份 Spec
3. **SDD 编码**：Spec 经 review 稳定后，再让 AI 严格按 Spec 实现

第 2 步是关键。此时你和 AI 讨论的对象是 **Spec 文档本身**，不是代码。AI 可以帮你补全边界 case、列出接口字段、起草验收清单；你负责纠正方向、删掉不该有的范围、确认最终口径。对话可以 vibe，产出必须是结构化的。

### 什么时候 Spec 算「稳定」

可以开始编码的信号：

- 目标、范围、不包含项三者不再来回改
- 接口或行为描述足够具体，能写出测试用例
- 你自己通读一遍，没有「这里 AI 可能理解错」的歧义
- 如有协作者，对方 review 过（或至少你刻意用「fresh eyes」再过一遍）

未稳定前，继续 Vibe-to-Spec，不要开写实现。

### 和「Vibe 直接写代码」的区别

| | Vibe 直接编码 | Vibe-to-Spec → SDD 编码 |
| ---- | ------------- | ----------------------- |
| 对话对象 | 代码 | Spec 文档 |
| 模糊需求的代价 | 立刻固化进实现，改起来贵 | 改 Spec 便宜，编码前对齐 |
| AI 的角色 | 猜意图 + 写代码 | 先协助澄清意图，再按契约写代码 |
| 适合 | 一次性脚本、15 分钟验证 | 要进主分支、要维护的功能 |

一句话：**Vibe Coding 解决「想法从哪来」；Vibe-to-Spec 解决「想法怎么对齐」；SDD 解决「对齐后怎么可靠交付」。**

## 为什么 AI 时代更需要 SDD

LLM 没有持久记忆，每次对话上下文有限，且倾向于「补全一个看起来合理的答案」。在这种特性下：

- 口语描述里的省略，会被 AI 用默认值填充——而这些默认值往往不是你想要的
- 多轮对话后，早期约束容易被稀释
- 没有 Spec，很难判断生成物是「做对了」还是「看起来对了」

SDD 把 **隐性意图变成显性契约**，让人和 AI 在同一份文本上对齐，而不是各自脑补。

## Spec 写什么

复杂任务才需要完整 Spec；小改动可以只用几段文字。一个够用的 Task Spec 通常包含：

```markdown
## 目标
实现用户登录 API，支持邮箱 + 密码。

## 范围
- 包含：POST /api/login、JWT 签发、错误码
- 不包含：注册、OAuth、刷新 token

## 接口
POST /api/login
Body: { "email": string, "password": string }
200: { "token": string }
401: 凭证无效

## 约束
- 密码不得明文记录
- 响应时间 P99 < 200ms（单实例）

## 验收
- [ ] 正确凭证返回 JWT
- [ ] 错误凭证返回 401
- [ ] 单元测试覆盖边界 case
```

Spec 里的接口契约、边界条件，可以直接转化为测试用例——这也是 SDD 与 [Harness Engineering](harness-engineering) 衔接的地方。

## 基本工作流

```text
Vibe 探索（可选）→ Vibe-to-Spec → Review → AI 按 Spec 实现 → 测试验收 → 下一轮
```

1. **Vibe-to-Spec**：和 AI 对话，把需求收敛成 Spec（目标、范围、验收清单）
2. **Review**：确认 Spec 稳定；不稳定就继续改 Spec，不写代码
3. **AI 实现**：把 Spec 作为 prompt 或项目文档提供给 AI
4. **验证**：用测试或 checklist 对照 Spec，不接受「看起来差不多」
5. **记录进度**：哪些 Spec 已实现、哪些在进行中（可配合状态锚点）
6. **迭代**：下一个 Spec 基于当前稳定基线继续

这与 TDD 有相似之处：都是先定义「完成」的标准。差别在于 SDD 的「测试」往往是自然语言规格 + 自动化测试的组合，且 Spec 同时服务于人和 AI。

## 与 Harness Engineering 的分工

SDD 和 Harness Engineering 覆盖 AI 辅助开发闭环的不同侧：

- **SDD（输入侧）**：用 Spec 告诉 AI「要做什么、边界在哪」
- **Harness Engineering（验证侧）**：用测试套件、状态锚点、项目约定确认「做得对不对、能不能安全演进」

完整闭环：

```text
Spec（SDD）→ AI 生成实现 → Test Harness 验证 → 状态锚点记录进度 → 下一轮 Spec
```

详见 [Harness Engineering 与状态锚点](harness-engineering)。

## 何时用哪种方式

| 场景 | 建议 |
| ---- | ---- |
| 15 分钟的小脚本、一次性数据处理 | Vibe Coding 足够 |
| 新功能、多人协作、要进主分支 | Vibe-to-Spec → Review → SDD 编码 |
| 需求模糊、方案未定 | Vibe 探索 → Vibe-to-Spec，稳定后再编码 |
| 需求清晰、边界明确 | 直接写 Spec 或小幅 Vibe-to-Spec |
| 已有测试和文档的成熟项目 | SDD + Harness，Spec 粒度可以更小 |

不必教条。关键是分清当前在做什么：**探索想法、对齐 Spec，还是按 Spec 交付**——三者对应 Vibe、Vibe-to-Spec、SDD 编码。

## 与博客「文章 SDD」的区别

本仓库还有一套 **文章 SDD**（Spec-Driven Writing）：作者在 `.ai/specs/` 写文章 Spec，AI 润色后输出 `content/post/` 下的交付物。那是 **写作流程**，不是软件开发方法论。

| | 软件开发 SDD | 文章 SDD |
| ---- | ------------ | -------- |
| 对象 | 代码、功能、接口 | 博客文章 |
| Spec 位置 | 项目内 `docs/tasks/` 等 | `.ai/specs/` |
| 交付物 | 可运行的实现 + 测试 | Hugo 文章 |

名字相同，思路相通（先 Spec、后产出），但场景和工具链不同。

## 总结

SDD 和 Vibe Coding 不是非此即彼。日常更顺的路径往往是：**用 Vibe 和 AI 一起把 Spec 写清楚，Review 稳定后再编码**。Vibe 负责降低起步摩擦和对齐成本；SDD 负责把对齐结果变成可验收的交付。配合 Harness Engineering 的验证侧，形成 **探索 → Vibe-to-Spec → 实现 → 验证** 的完整链路。
