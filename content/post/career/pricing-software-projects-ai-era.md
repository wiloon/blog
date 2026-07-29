---
title: "Pricing Software Projects in the AI Era 人天报价为什么不够用了"
author: "-"
date: 2026-07-29T13:57:29+08:00
lastmod: 2026-07-29T13:57:29+08:00
url: pricing-software-projects-ai-era
categories:
  - career
tags:
  - career
  - AI
  - pricing
  - freelance
  - remix
  - AI-assisted
---

最近在给一个需求做报价——一个多语言文档批量 QA 校验工具，需求分析花了好几轮问答才敲定范围，接下来要报价的时候，我在想一个问题：这活基本是 AI 辅助写完的，按传统的人天/人月去算，好像已经不太对了。

## 问题：人天为什么在 AI 辅助场景下失灵

人天报价能成立，前提是"1 人天 ≈ 一定量的产出"这个换算关系大致稳定。AI 辅助开发把这个关系打破了：

- **产出和投入的人天数脱钩**。同样的功能，AI 辅助下可能几小时就写完测试都带上了，人天数骤降，但功能本身的价值（能不能用、值多少钱）并没有跟着降。继续按人天报价，要么报太低把自己的溢价空间搭进去，要么硬凑人天数撑报价，两边都别扭。
- **计时计费本身有激励错位**。如果按小时/人天计费，乙方反而有动机把项目拖久一点——多算的工时里，有多少是"AI 生成代码但按人类费率计费"，这跟"用 AI 提效"的初衷是反的。这个问题不是我一个人瞎想的，查了一圈资料，行业里已经在明确讨论这一点（见文末参考链接）。

## 顺带想到的：按 token 成本定价，行不行

报价的时候，我最初想的是一个"看起来很公平"的方案：按这次任务实际花的 token 成本 × 一个系数，再加上需求分析、架构、管理费这些固定项。想清楚之后放弃了，原因：

1. **token 成本和交付价值脱节**。这次需求如果全靠 AI 辅助实现，token 花费可能就几十到一百多美元，但业务价值（省下的人工审校时间、给客户的报价空间）可能是这个数字的几十倍。按 token 成本定价会严重低估真正值钱的部分——需求澄清、边界判断、架构决策、验收测试，这些环节 token 消耗很少，但最耗专业判断。
2. **和计时计费一样的激励错位**。按 token 成本加成收费，等于鼓励自己多跑几轮、多重试、多探索——消耗越多赚得越多，这跟"用 AI 提高效率、把省下来的时间还给客户"的初衷正好相反。
3. **不可审计、不稳定**。token 单价随模型和厂商定价经常变，客户也很难验证实际花了多少 token，容易从"怎么定价"变成"信任问题"。

token 成本定价比较适用的场景，是那种极度机械、高重复量、判断空间很小的活（批量格式转换），成本约等于工作量。判断空间大的定制开发不属于这一类。

## 常见的软件项目报价模式

整理下来，常见的几种模式：

| 模式                         | 说明                                    | 适合场景                   |
|-----------------------------|-------------------------------------- --|--------------------------|
| 固定价（Fixed price）         | 范围定死后报一口价，风险在乙方              | 需求已经问清楚、边界明确的项目 |
| 人天/人月（Time & Materials） | 按实际投入时间 × 日费率结算，风险在甲方      | 需求会持续演进、探索性强的项目 |
| 里程碑付款                    | 固定价拆成几个阶段验收付款                 | 周期较长、双方都想控风险的项目 |
| 价值定价（Value-based）       | 按项目给客户带来的业务价值定价，不看成本      | 能算清 ROI 的项目           |
| 结果导向（Outcome-based）     | 只在结果达成时收费（比如按处理成功的记录数）  | 高度可量化、重复度高的流程     |
| 订阅/维护费                   | 功能上线后按月收运维/迭代费                | 长期合作、持续迭代的项目      |

## 查资料确认的方向：行业在往固定价 + 里程碑走

搜了一圈 2026 年的行业讨论，结论跟自己想的方向一致：**固定价、里程碑验收正在取代小时/人天计费，成为 AI 辅助开发场景下的默认模式**。几个关键说法：

- 固定价外包合约本质是"范围定死、验收标准写清楚、变更走流程另计费"——这正是需求分析阶段要干的事。
- 有研究认为，结果导向/固定价项目总成本比按小时计费低 20%-40%，因为按小时计费天然鼓励拖时间，固定价则鼓励用 AI 提效——省下来的时间直接变成自己的利润。
- 复杂项目不建议只开一次会就报固定价，容易报错；更稳妥的做法是先把 discovery/需求分析阶段单独定价，摸清范围后再对实现阶段报固定价。
- 成熟的团队很少只用一种模式，通常是"基础阶段固定价 + 探索性工作按人天 + 长期运营叠加价值定价"的组合。

## 报价框架

结合这次的实际情况，几条原则：

1. **人天不是拿来对外报价的单位，是拿来对内核算成本的工具**。自己心里用"AI 辅助后的实际工时"估成本、算利润率，但对外报的是"这个范围多少钱、什么时候交付、验收标准是什么"，不暴露人天数或 token 数。
2. **需求分析单独定价**，哪怕这部分自己用 AI 很快能问清楚（这次为了敲定范围来回聊了四轮）。把这部分的专业价值单独体现出来，不要因为"反馈快"就顺带打折。
3. **范围明确的功能按固定价，按里程碑拆分收款**。比如这次的需求，可以拆成"代码类检查规则实现"→"LLM 类检查实现"→"术语库管理与联调"三个节点，每个节点独立报价、独立验收，双方风险都可控。
4. **把"用 AI 更快"当成竞争力，不是要透明化的成本项**。报价可以比传统方式更有竞争力、交期更短，但不需要主动解释成本构成——这是差异化优势，不是义务披露的信息。

这一次那个多语言 Excel QA 项目，按范围粗估大概 10-13 人天量级（内部核算用），最终会按上面第 3 条拆成几个里程碑去报固定价，而不是直接把人天数乘单价报给客户。

## 参考链接

- [Fixed-Price vs. Hourly Software Development: Why AI Just Made This Choice Obvious](https://medium.com/@ailoittetech/fixed-price-vs-hourly-software-development-why-ai-just-made-this-choice-obvious-8f693979b2bd)
- [The Death of the Hourly Software Agency (And What Replaces It)](https://medium.com/@ailoittetech/the-death-of-the-hourly-software-agency-and-what-replaces-it-6e999a2662d3)
- [AI-Era Agency Pricing Models: A 2026 Decision Guide](https://www.digitalapplied.com/blog/ai-agency-pricing-models-2026-decision-guide)
- [Software Development Pricing Models: Fixed Price vs. T&M vs. Value-Based](https://tblocks.com/articles/software-development-pricing-models/)
- [AI Agent Pricing Models Explained (2026)](https://pickaxe.co/post/ai-agent-pricing-models)
- [Custom AI Development Pricing Models: How Agencies Bill in 2026](https://semnexus.com/custom-ai-development-pricing-models/)
