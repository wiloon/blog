# Spec: 2026 W25

| 字段     | 值                                       |
| -------- | ---------------------------------------- |
| 状态     | ready-to-write                           |
| 交付物   | `content/post/career/weekly-2026-w25.md` |
| Hugo url | `weekly-2026-w25`                        |
| 标题     | 2026 W25                                 |
| 分类     | career                                   |

---

## 验收清单

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签（SDD）：`original`、`AI-assisted` + 内容标签；无 `remix`、`reprint`

---

## A. 原始素材

> **AI 禁止修改本章节任何内容。** 以下是作者的原始输入，可能是语音转文字或意识流记录，结构不完整、语言口语化均可。每次补充时新增带日期的子节。

### 2026-06-15
收到一个新的投递简历的邀约，本周的时间预计主要会花在准备简历和准备有可能的未来的面试，其它 homelab的改造暂停，公司刻章下周再说
### 2026-06-16

- 在 blog 的 agile.md 里记录了 "Speed over Perfection" 这个概念，这是在一个新的 JD 里接触到的概念，觉得值得记录下来。

### 2026-06-17
更新了写简历的流程，昨天跟同事聊 AI 的使用，聊到 AI 交互的最佳实践，聊了 SDD 工作流用在开发我的开源项目的时候用到的SDD 的方式，然后我在写新的简历的时候大脑里面触发了刚聊过的这个 SDD 流程，就想到其实 SDD 不只是写代码，写 blog,应该也可以写简历，又因为我之前投递过的某一份简历跟这次的新职位 的简历有很多重叠的部分，所以目前的想法是以旧简历为基础，参考新的职位描述，在旧简历的基础上修改，我和 AI 先写了一个 spec，列出了旧简历和新职位描述的差异，然后我根据这些差异到我的工作经历里去挖掘对应的经历，把详细的故事写在我个人的 profile里，再回到 spec里标注这些差异可以参考哪些内容，最后再让 AI 根据 spec 生成新的简历。这个流程感觉非常好，既有系统性又有针对性，效率也很高，感觉以后写简历都可以用这个流程了，但愿这个新机会能顺利。这样近期就不用再写简历了。能多花点时间折腾 homelab了。

另外某些事情只是做过，只是学习过，不同于跟别人分享过，大脑在输入和操作的场景下，跟大脑在组织语言输出的场景下，应该是有差异的，信息在加工过然后输出的过程中，会有不同的记忆， 这些输出过的内容更能关联到当前遇到的问题，记忆可能也更清晰一些，所以还是要经常记录，经常跟人类聊天，交流新的想法，新的概念，新的工具，这样在需要的时候就能更快的从记忆里提取相关的信息来解决问题了。比如这次更新写简历的流程，因为我很早就在用SDD的方式 写代码， 写 blog,但是从来没想到用 SDD来写简历， 直到昨天跟前同事聊完这个话题，才突然想到这个流程也可以用在写简历上，这个就是一个很好的例子，说明了输出的过程是对记忆的一种加工和强化，这样在需要的时候就能更快的提取相关的信息来解决问题了。

未来要做的一件事情，暂时在个人blog 上加个链接用来放 “一人公司”的管理文档，比如每天早上跑步之类的 -_-,还有时间分配的问题

### 2026-06-23

周初计划主要写简历、其它事情暂缓。简历写完后开始梳理 Java 相关文档；又因为实际操作能更好帮助理解文档，所以打算给 enx 加 Java 后端作 playground；又因为 enx 有长期未合并的分支，所以先测试和合并 Cognito 分支，再开新分支做 Java 后端。

---

## B. AI 审阅 · 问答

> **规则：**
>
> - AI 只在此处末尾追加新 Round，**不修改已有 Round 的任何内容**
> - 每轮结束时 AI 判断信息是否充分，若充分则写"建议进入 ready-to-write"，**状态由作者手动更新**
> - 作者在"作者回答"下填写，完成后通知 AI 继续下一轮或输出正文

### Round 1 — 2026-06-23

**Q1：** 6/22 `enx-api-java` 相关 commit 是否写入 W25 正文？

**A1：** 与前面 enx 工作相关，W25 可写「产生给 enx 加一个 Java 后端」的想法与动机；6/22 的实际动手（脚手架、部署等）放到 W26 周记。因为最近在看的一个职位是JAVA相关的，所以 enx作为我的个人的 playground，我练习或者学习java相关的内部要有实际操作的项目

**Q2：** 招聘/简历段落如何脱敏？写到什么程度？

**A2：** 脱敏处理——只说收到了投递简历的邀请；简要描述准备简历的过程：为写新职位简历又去挖掘了过去职业生涯的事例写进简历。可写 markdown → PDF 输出流程：第一次用正规排版工具输出简历；此前 VS Code / Cursor「Preview → 浏览器打开 → 打印 PDF」因软件更新走不通，跟 AI 聊了几轮后选了现在的 pandoc 流程。

**Q3：** blog Java 文档整理在周记里怎么呈现？

**A3：** 因投递的是 Java 职位，所以在梳理过去整理的 Java 相关文档。正文不写具体 Java 领域知识，只关联几篇有代表性的文章即可（不必全列）。

**AI 判断：** 写作约束已明确，**建议进入 ready-to-write**（状态由作者手动更新）。

---

## C. 批注

> AI 在生成正文过程中发现的歧义或待确认项，记录于此，供作者参考。

### 写作约束（作者确认 · 2026-06-23）

**本周叙事链（正文建议按时间线串起来）**

1. 周初：收到投递简历邀请，计划本周主攻简历，homelab 等暂缓
2. 周中：SDD 式写简历、挖掘职业事例、搭建 pandoc PDF 流水线
3. 简历收尾后：梳理 blog 既有 Java 文档（投递 Java 职位）
4. 梳理过程中：想到实际操作有助理解 → 决定给 enx 加 Java 后端作 playground
5. 动手前：enx 有长期未合并的 Cognito 分支 → 先测试、合入 main，再开 Java 后端分支（6/22 实施见 W26）

**禁止包含（Do NOT）**

- 公司名、职位编号、内推/HR 细节、`J68476`、`fidelity-dalian` 等仓库路径
- Java 技术细节展开
- 6/22 `enx-api-java` 脚手架与部署实施细节（属 W26）
- A 节「但愿顺利」可保留期待语气，不写投递结果或面试进展

**招聘 / 简历（脱敏）**

- 不出现公司名、职位编号、内推细节等可识别信息
- 可写：收到投递简历邀请；SDD 式准备流程（spec → profile 挖故事 → 生成简历）；挖掘职业生涯事例
- 可写：markdown → pandoc → PDF 流水线；动机是 Preview/打印 PDF 旧流程失效，与 AI 讨论后选型
- 内链：[markdown-to-pdf-pandoc-xelatex.md](../../content/post/development/markdown-to-pdf-pandoc-xelatex.md)（示例已脱敏，可安全引用）
- 挖掘事例示例内链（可选）：[iot-third-party-data-push.md](../../content/post/career/iot-third-party-data-push.md)

**Java 文档整理**

- 动机：简历完成后，因投递 Java 职位梳理既有 blog Java 文档
- 正文只链 2–4 篇代表性文章，不展开 Java 知识。候选：
  - [java-knowledge-map.md](../../content/post/language/java/java-knowledge-map.md)（总览）
  - [java-version-history.md](../../content/post/language/java/java-version-history.md)（版本脉络）
  - [jvm.md](../../content/post/language/java/jvm.md) 或 [hotspot.md](../../content/post/language/java/hotspot.md)（运行时）
  - 任选一篇本周新拆/重写的即可，如 [graalvm.md](../../content/post/language/java/graalvm.md)

**enx**

- 动机：Java 职位 + enx 作 playground 练手；实际操作帮助理解正在梳理的文档
- W25 叙事：Cognito 分支分叉已久 → 测试至可用 → 合入 main（避免与后续 Java 后端分支合并冲突）→ Homelab CI/CD 部署跑通 → 产生/确认 Java 后端方向
- 技术细节内链：[enx-api-homelab-cicd.md](../../content/post/cloud/enx-api-homelab-cicd.md)
- **不写** 6/22 脚手架、Tekton、`deployment-java` 等实施细节 → 见 W26 Spec

**其它**

- homelab descheduler、域名方案暂缓：一句带过（6/18 descheduler 可写为简历主线之外的零星维护）
- A 节 6/17 SDD 泛化感悟、输出强化记忆：保留，可独立小节
- 公司刻章推迟、未来 blog 链「一人公司」管理文档：按 A 节原话或略写
- 6/16 补写 [W24 周记](../../content/post/career/weekly-2026-w24.md)：开篇一句 meta 即可
- Speed over Perfection（[agile.md](../../content/post/cs/agile.md)）：可选一句，正文写「看职位描述时」不写 JD

---

## D. Commit 整理（AI）

> 统计范围：ISO 2026-W25（6/15 周一 — 6/21 周日）。6/22 commit 仅作边界参考（实施细节归 W26）。
>
> 来源：`blog`、`w10n-config`、`enx` 三仓库 `git log`。

### 总览

| 主题 | 大致时间 | 涉及仓库 |
| --- | --- | --- |
| 招聘 / 简历（脱敏叙述） | 6/15–6/21 | w10n-config、blog |
| Java 知识图谱整理（面试准备） | 6/19–6/21 | blog、w10n-config |
| enx 认证与 Homelab 部署 | 6/20–6/21 | enx、w10n-config、blog |
| K8s Homelab 运维（descheduler 等） | 6/18 | w10n-config、blog |
| 一人公司 / 工具选型 | 6/15–6/17 | blog、w10n-config |
| enx Java 后端（想法，实施见 W26） | 6/21 周末 | enx、w10n-config |

---

### 招聘与简历（本周主线 · 正文脱敏）

与 A 节 6/15、6/17 素材一致：收到投递简历邀请后，本周大量 commit 围绕 SDD 式简历流程。

**w10n-config `resume/`**（正文不暴露路径/编号）

- 6/16：新建 resume TASK-SPEC；录入 JD、prep 笔记；从 profile stories 挖掘素材
- 6/17–6/19：多轮迭代中英文简历；补充面试问题笔记；统一文件命名
- 6/19–6/20：搭建 markdown → PDF 流水线（pandoc、LaTeX 模板、表格行规则）；生成并迭代 PDF

**blog**

- 6/16：`agile.md` 补充「Speed over Perfection」；新建 `workflow-engine.md`；开始写 W25 Spec
- 6/17：职业项目 `iot-third-party-data-push.md`（配合简历素材）
- 6/19–6/21：大规模 Java 文章拆分/重写（见下节），与面试知识准备强相关

6/22 仍有 resume PDF 相关 commit，若流水线叙述未写完可略带一句「翌日继续调排版」；细节不展开。

---

### Java 文档梳理（正文只关联，不讲知识）

6/19–6/21 blog 连续多天 commit，动机：投递 Java 职位，梳理既有 Java 文档。正文合并为一段 + 链 2–4 篇代表文章（见 C 节候选列表），不展开具体技术点：

| 日期 | 代表变更 |
| --- | --- |
| 6/19 | 注解、泛型、JNI、Project Panama、JDK 25/26、缓存一致性等新/拆文 |
| 6/20 | JVM/HotSpot 拆分；JDK 版本史整合（`jdk-5/7/8/9/17` 等）；内部类、断言、lambda |
| 6/21 | 函数式接口、Servlet 生命周期、forward/redirect；GraalVM、Spring AOT、Buildpacks 容器打包；JPMS 重命名等 |

**w10n-config 侧配套**：6/20 `java-playground` GitHub 仓库 OpenTofu；6/21 workstation 安装 JDK Ansible playbook。

---

### enx 项目

**enx 仓库**

- 6/21：合并 PR #4 `email-registration` — AWS Cognito 认证、邮箱注册、Chrome 扩展 Cognito 登录、enx-ui 认证流程与 E2E 测试等（单 commit 体量很大，开发周期跨多周，但合入点在本周日）

**w10n-config 部署与基础设施**

- 6/20–6/21：Tekton 流水线迭代（`pipeline-build-enx-api`、`enx-ui`）；多次更新 k8s deployment 镜像 tag
- 6/21：`enx google auth` — AWS OpenTofu Cognito 配置、Chrome OAuth handoff 文档；workstation 安装 otty

**blog**

- 6/21：新建 `enx-api-homelab-cicd.md`；更新 `kanban-tool-selection.md`；新建 `linear-usage.md`

**W25 正文叙事**（见 C 节「本周叙事链」）：Cognito 分支测试合 main → Homelab 部署 → 确认 Java 后端 playground 方向。不写 6/22 实施。

---

### Homelab / 基础设施（非 enx）

| 日期 | 内容 |
| --- | --- |
| 6/15 | 域名迁移方案 `TASK-SPEC-domain-migration-wiloon-lab.md` 大幅扩充（作者笔记：因面试准备暂缓） |
| 6/18 | K8s descheduler（ArgoCD Application、topology spread 组件、多 workload kustomize 调整）；k8s-50 节点内存升至 8G |
| 6/19 | macOS WireGuard 双配置（LAN/WAN）渲染模板 |
| 6/16 | `ops/biz/README.md`；`ops/finance/` 理财文档（分配模型、京东小金保等） |

**blog**：6/18 `k8s.md` 补充 descheduler 说明。

---

### 一人公司与个人运营

- 6/15：blog `one-person-company.md` 润色；`kanban-tool-selection.md` 发布
- 6/17：A 节已记录 SDD 写简历感悟；blog 侧 workflow-engine、third-party-data-push 与职业叙事交叉

---

### 其他 blog 小改动

- 6/16：补写 W24 周记（`weekly-2026-w24.md`）；删除重复文档
- 6/19：`brew.md` 小更新
- 6/21：`linear-usage.md`（Linear 使用记录，与看板选型呼应）

---

### 周记正文建议结构（已确认）

开篇可一句：补写了 [W24 周记](../../content/post/career/weekly-2026-w24.md)。

1. **投递邀请与简历准备**（脱敏）— 周初计划 → SDD 流程 → 挖掘职业事例（可链 iot-third-party-data-push）→ pandoc PDF 流水线（链 markdown-to-pdf 一文）
2. **Java 文档梳理** — 简历完成后动机 + 2–4 篇代表文章内链，不写 Java 知识
3. **enx** — Cognito 分支合 main 的缘由与过程 + Homelab 部署（链 enx-api-homelab-cicd）；Java 后端 playground 想法
4. **Homelab 零星** — descheduler、域名方案暂缓（一句）
5. **思考** — A 节 6/17 SDD 泛化、输出强化记忆；可选：Speed over Perfection（agile.md）

**状态：** ready-to-write。
