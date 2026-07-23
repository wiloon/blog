---
title: "Agent Token Routing: 本地匹配、缓存与模型分层"
author: "-"
date: 2026-07-23T00:30:26+08:00
lastmod: 2026-07-23T00:30:26+08:00
url: agent-token-routing
categories:
  - AI
tags:
  - ai-agent
  - token
  - cache
  - intent
  - remix
  - AI-assisted
---

## 问题

聊天类 Agent 里，不少问答是相对固定的模式：营业时间、退款入口、帮助说明、菜单选项等。若一律调用大模型，既费 token，又容易把标准话术写飘。

常见做法有两种：

1. 正则或规则匹配用户输入，命中则返回固定回答
1. 在模型前加缓存，对特定提示词返回已有内容

这两层有用，但不够。省 token 的核心不是「再找一种缓存技巧」，而是做分层路由：能确定性处理的绝不进模型。

## 分层路由

```text
用户输入
  → L0 本地确定性匹配（规则 / FAQ / 按钮 / 命令）
  → L1 轻量意图分类（小模型 / embedding / 关键词）
  → L2 提示词 / 响应缓存（相同或近似请求）
  → L3 完整 LLM（复杂推理、开放对话、工具编排）
```

每一层命中就短路返回；只有前面都 miss 才往下走。

| 层 | 手段 | 适用场景 | 省什么 |
| ---- | ---- | ---- | ---- |
| L0 本地匹配 | 正则、精确字符串、按钮 payload、slash 命令、状态机固定选项 | 话术固定、歧义低、可穷举 | 零 LLM 成本 |
| L1 轻量分类 | 小分类模型、embedding 相似度、关键词 + 规则 | 说法多变但意图有限 | 用便宜模型代替大模型 |
| L2 缓存 | 精确 cache key、semantic cache、prompt prefix cache | 输入或 system prompt 重复率高 | 省重复推理 |
| L3 LLM | 完整对话 / function calling | 开放问答、多步推理、需工具、强个性化 | 正确性优先 |

## L0：本地匹配

适合：

- 「查快递」「人工客服」「营业时间」等有限意图
- 菜单 / 按钮点选（没有自由文本）
- 流程某一步只能选 A / B / C（状态机）
- 命令式输入：`/help`、`/reset`、`订单号:xxx`

不适合：同义改写很多、需要理解上下文指代（「那个」「再退一次」）。

实践上，精确匹配与结构化输入优先于正则；正则只覆盖高确定性、低变化的口语。

## L1：轻量意图

比纯正则稳，比大模型便宜：

- Embedding 检索 FAQ：问句 → 向量 → 相似度超过阈值 → 返回标准答案
- 小分类模型 / 蒸馏意图模型：只输出 `intent_id`，再走模板或工具
- 关键词 + 否定规则：快速筛「明显是 FAQ」的流量

这层回答的是「这是哪一类问题」，不是「怎么写一段漂亮回复」。意图识别与槽位填充的细节见 [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)。

## L2：缓存

分清三种，不要混用：

1. **精确响应缓存**  
   `hash(规范化后的 user + 关键上下文)` → 答案。适合完全相同的问法、工具结果未变、无个性化。

1. **语义缓存（Semantic Cache）**  
   问句 embedding 近邻命中 → 复用旧回答。适合 FAQ、文档问答；不适合强时效（股价、库存）和强个性化（「我的订单」）。

1. **Prompt / KV Prefix Cache**（厂商侧）  
   长 system prompt、固定工具 schema 复用。省的是输入侧重复，不是「固定问答短路」；和业务 FAQ 缓存是不同层。

经验阈值：语义缓存相似度通常要很高（如 0.92–0.98），并加 TTL 与业务标签（用户 / 租户 / 数据版本），避免答错。

## L3：必须走模型

- 多轮指代、开放闲聊、需要推理
- 要抽槽位再调工具（查「我上周那笔退款」）
- 政策 / 合规话术不能错，但表述变化极大（可：小模型分类 + 大模型润色，或模板填槽）
- 创造性、总结、对比、代码等

工具调用与 Function Calling 见 [Function Calling](./agent-function-calling.md) 与 [Tool Calling Patterns](./agent-tool-calling-patterns.md)。

## 其它常见方案

1. **模板 + 槽位填充**  
   意图确定后用模板：`您的订单 {{id}} 状态是 {{status}}`；只对抽槽调小模型或规则，正文不生成。

1. **状态机 / 流程图 Agent**  
   客服、开户、报障：节点上选项固定，只有「自由描述故障」节点才调 LLM。

1. **RAG 检索后直接返文档片段**  
   高置信命中时可不生成，只返回标准条文 / 卡片；低置信再 LLM 总结。

1. **两阶段：分类用小、生成用大（或干脆不生成）**  
   `intent = small_model(x)`；若 intent 属于 FAQ → 模板；否则 → 大模型。

1. **级联（cascade）**  
   先小模型答；置信度低再 escalate 到大模型。

1. **工具结果缓存**  
   天气、汇率、配置查询：缓存的是 tool output，不是 LLM 文案，往往更安全。

1. **预计算常见路径**  
   对高频意图离线生成标准回复，上线只做路由。

## 决策规则

```text
能用按钮/命令/状态机穷举？     → L0，不调模型
说法多但答案标准（FAQ）？     → embedding/FAQ 检索；高置信直接返
只要意图标签就能办？         → 小分类器 + 模板/工具
system/工具定义很长且重复？   → 用厂商 prefix/KV cache
同一用户/同一问句短时重复？   → 精确响应缓存
问的是「我的数据」且会变？   → 不要语义缓存答案；最多缓存 tool 结果
开放、多步、要推理？         → L3 完整 LLM
```

简要对照：

- **本地匹配**：确定性高、枚举得完、错答代价大（直接给错政策不如不答）
- **缓存**：重复率高、答案稳定、可失效
- **模型**：歧义、个性化、组合推理、工具编排

## 实践建议

1. 默认管道：L0 → L1 → L2 → L3，每层打点（命中率、错误率、token）
1. FAQ / 固定话术不要让大模型即兴写；标准答案进知识库或模板，模型最多做改写且可关掉
1. 语义缓存只用于公共、稳态内容；用户私有数据走精确 key，或只缓存工具结果
1. 把省 token 和控风险绑在一起：退款规则、法律话术优先模板；闲聊才放生成
1. 先观测再优化：没有命中率和 bad case 回流，缓存和正则都会静默变差
1. 别过早上复杂 semantic cache：多数产品先做「按钮 + FAQ embedding + 精确缓存 + 大模型兜底」就够

一句话：固定模式用路由和模板消掉生成；缓存只消灭重复；模型留给真正不确定的部分。

## 相关文章

- [AI Agent Development](./ai-agent-development.md)
- [Intent Recognition and Slot Filling](./agent-intent-and-slot-filling.md)
- [Function Calling](./agent-function-calling.md)
- [Tool Calling Patterns](./agent-tool-calling-patterns.md)
- [Output Constraint](./agent-output-constraint.md)
