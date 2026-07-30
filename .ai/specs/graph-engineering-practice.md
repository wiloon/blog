# Spec: 从 Loop 到 Graph Engineering：Python + LangGraph + Claude Code 的工程落地实践

| 字段 | 值 |
| ---- | -- |
| 状态 | draft-written |
| 交付物 | `content/post/AI/graph-engineering-practice.md` |
| Hugo url | `graph-engineering-practice` |
| 标题 | 从 Loop 到 Graph Engineering：Python + LangGraph + Claude Code 的工程落地实践 |
| 分类 | AI |

---

## 验收清单

- [x] 标题、url、分类与 Spec 表一致
- [x] 正文从 `##` 起，无 `#`（MD025）
- [x] 标签（SDD）：`original`、`AI-assisted` + 内容标签；无 `remix`、`reprint`

---

## A. 原始素材

> **AI 禁止修改本章节任何内容。** 以下是作者的原始输入。

### 2026-07-24

> 在 AI 驱动开发的范式演进中，我们经历了从 **Prompt Engineering**（提示词）到 **Context Engineering**（上下文/RAG），再到 **Loop Engineering**（单循环）的探索。
> 如今，**Graph Engineering（图工程）** 正在成为构建可靠、可扩展 AI Agent 系统的核心架构范式。

---

## 一、 为什么我们需要 Graph Engineering？

在单 Agent 时代，**Loop Engineering** 解决的是“让 AI 自我修正”的问题——给 Agent 一个任务，让它修改代码、跑测试，失败了再继续修。

但在复杂的实际业务场景中，单一 Prompt Loop 很快会遇到瓶颈：

1. **上下文污染（Context Pollution）**：随着循环次数增加，会话中充斥着大量的历史报错日志和无效尝试，导致 LLM 变得越来越“笨”。
2. **缺乏确定性控制（Nondeterminism）**：完全依靠 LLM 在 Context 内部决定下一步行动，极易陷入无限死循环或越改越乱。
3. **职责模糊**：让同一个 Agent 既做架构规划、又写前后端代码、还跑单测和 Code Review，超出其能力边界。

**Graph Engineering（图工程）** 的本质是：**用有向图（Directed Graph）将复杂流程解耦为专职节点（Nodes），将控制流（Control Flow）交还给确定性的代码（Edges），只将局部推理与代码生成交给 AI。**

---

## 二、 架构设计与职责划分

一套稳定的 Graph Engineering 系统，应当明确区分**指挥官、执行者与硬闸门**：

```text
                  +-----------------------------------+
                  |   LangGraph (Python 主控进程)     |
                  +-----------------------------------+
                     /              |              \
      (节点 1: Python 调起)  (节点 2: 纯代码)   (节点 3: Python 调起)
                    /               |               \
                   v                v                v
      +-------------------+   +-----------+   +-------------------+
      | Claude Code 进程 A|   | pytest    |   | Claude Code 进程 B|
      |  (负责后端逻辑)   |   | (硬闸门)  |   |  (负责前端/重构)  |
      +-------------------+   +-----------+   +-------------------+
```

---

## B. AI 审阅 · 问答

（本轮作者直接要求输出正文；素材仅有 §A 两节，正文在素材基础上补全了落地注意与小结，未编造具体项目案例。）

---

## C. 批注

---

## 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-07-24 | 初版素材；Phase 4 输出正文，状态 → draft-written |
| 2026-07-30 | 交付物将「纯 Claude Code」路径拆至 `content/post/AI/graph-engineering-claude-code.md`；本 Spec 交付物只保留 Python + LangGraph 主控路径（§A 素材未改） |
