---
title: "Matt Pocock 的 Agent Skills 与 Loop Engineering"
author: "-"
date: 2026-09-02T14:18:35+08:00
lastmod: 2026-09-02T14:18:35+08:00
url: matt-pocock-skills
categories:
  - AI
tags:
  - claude-code
  - agent
  - skill
  - loop-engineering
  - workflow
  - remix
  - AI-assisted
---

## 这套 skills 是什么

Matt Pocock（Total TypeScript / aihero.dev 作者）公开了一套面向 AI 编码的 Agent Skills 集合，本质是一组 `SKILL.md` 文件，把「从想法到上线」的工程流程拆成若干可被 Agent 按需加载的步骤。它不是某个 IDE 插件，而是一批可以装进 Claude Code（或其他支持 skill 的 harness）的流程说明。

装好之后目录大致是这样：`~/.claude/skills/` 下一批软链接指向实际的 skill 仓库；`setup-matt-pocock-skills` 是每个仓库跑一次的前置配置（约定 issue tracker、triage 标签、文档布局）；`ask-matt` 是一个路由 skill，用来在记不清该用哪个流程时反查。

## 主流水线：idea → ship

大部分工作走这一条线：

1. **`grill-with-docs`**：用连续追问把模糊的想法逼清楚，过程沉淀进 `CONTEXT.md` 和 ADR。没有工作目录时用 `grill-me`（无状态版）。
2. 如果有些问题必须靠能跑的代码才能回答（状态、业务逻辑、要看的 UI），绕道 **`prototype`** 写一份一次性代码，用 **`handoff`** 在会话之间传递结论。
3. 多会话构建：**`to-spec`** 把对话变成 spec，**`to-tickets`** 拆成一批 tracer-bullet ticket，每个声明自己的阻塞边；然后逐个 **`implement`**，ticket 之间清空上下文。单会话能做完就直接 `implement`。
4. `implement` 内部驱动 **`tdd`**（一次一个红-绿切片），收尾跑 **`code-review`**（Standards + Spec 两轴审查）再提交。

匝道和支线：bug 和请求堆积走 **`triage`**；线上出问题走 **`diagnosing-bugs`**（坚持先有一个已经变红的命令再谈修复）；大到一个会话装不下的模糊工程走 **`wayfinder`**（先画决策地图，产出决策而非交付物，再汇入 `to-spec`）。

## 它用的词汇表

`grilling` 是追问的原语：把设计拆成一棵决策树，按轮次推进，每轮把「前置已定、现在能问」的问题一次性抛出，每个问题附一个推荐答案，事实由 Agent 自己查、决策留给人。

`loop-me` 里另有一套「循环」词汇，注意这里的 loop 和下文 Loop Engineering 的 loop 不是同一个意思：

- **loop**：用户生活里反复出现的模式（一段职业、一周、一个早晨、一件重复的事）。把生活看成循环套循环，能看出哪些活动足够可预测、值得委派。
- **workflow**：一个 loop 的 spec，落在 `workflows/*.md`。
- **trigger**：每次运行的触发方式，事件或定时。
- **checkpoint**：人在环上的确认点。有些 workflow 一个都没有，全自动跑。
- **push right**：把 checkpoint 尽量往后推，让 Agent 先把能做的都做完，人只被打扰一次。
- **brief**：checkpoint 给人看的东西，是决策就绪的摘要（做了什么、为什么、附一个能下钻到产物的链接），不是原始输出。

## 与 Loop Engineering 的关系

[Loop Engineering](./loop-engineering.md) 的核心是：与其人逐步写 prompt、看结果、再发下一条，不如设计一个自动循环系统，定好目标、反馈、验收和停止条件，让 Agent 反复迭代到可验证的完成状态。Matt 这套 skills 就是这个思路的一种「人在环上」的落地。

对应关系大致是：

| Loop Engineering 的概念 | 在这套 skills 里的体现 |
| ---- | ---- |
| 内层验证循环（重试到测试通过） | `tdd` 的红-绿循环、`code-review` 两轴审查、`diagnosing-bugs` 要求先有一个能复现的失败命令 |
| 外层工作流循环（idea → ship） | `grill → to-spec → to-tickets → implement` 主流水线，ticket 之间清空上下文 |
| 把重复模式抽出来再委派 | `loop-me` 的 loop lens：值得委派的循环写成 `workflows/*.md` |
| 上下文管理作为子技能 | smart zone（约 150k token）、phase boundary 上 continue / clear / handoff / subagent / compact 的取舍 |
| 人在环上而非环内 | `checkpoint` / `push right` / `brief` |

人参与的位置从「环内」移到「环前和环上」：环前做判断和决策（写 spec、定验收标准、决定 checkpoint 放哪），环上只在关键节点看一次 brief。

Matt 有一个明确立场：**「重试到测试通过」这类验证循环是好的；「让 Agent 自己改写自己的长期指令并持久化」是危险的**，任何要进入长期上下文的 Agent 自写内容都要人来 review。这套 skills 里大量的 grilling、spec、code-review 环节，正是为了在自主循环里保留这个把关点。

他自己那条「睡觉时出活」的 Ralph 式循环（Agent 按优先级过 backlog、持续跑测试、更新 master PRD、反复提交）之所以敢放手跑，前提也是前面人已经把 spec 和验收标准定清楚了。Ralph 技术本身见 [Loop Engineering](./loop-engineering.md) 里的「Headless 模式与 Ralph 循环」一节。

## 在本站的坐标系里

- [Loop Engineering](./loop-engineering.md)：一个目标反复「改 → 验证 → 再改」。这套 skills 的 `implement` / `tdd` 环节就落在这里。
- [Graph Engineering](./graph-engineering.md)：多角色、多阶段、不同失败路径的编排。`wayfinder` 的决策地图和 `to-tickets` 的阻塞边接近这个层面。
- [Harness Engineering](./harness-engineering.md)：把「完成」表达成客观、可重复的验证信号。`code-review` 和 ticket 的验收条件依赖它。
- [Spec-Driven Development](./spec-driven-development.md)：`grill-with-docs → to-spec` 就是一条 SDD 路径，`CONTEXT.md` 和 ADR 是它的状态锚点，另见 [ADR 与 Task Spec](./adr-vs-task-spec.md)。

## 小结

Matt Pocock 的 skills 不是一个新概念，而是把 Loop Engineering、SDD、Harness Engineering 这些思路串成一条能照着走的流水线：前面用 grilling 逼清楚需求、用 spec 和 ticket 固定范围，后面让 tdd 和验证循环自己收敛，人只在 checkpoint 看 brief。它和 Loop Engineering 的关系是「方法论」和「一套按方法论组织的工具」的关系。
