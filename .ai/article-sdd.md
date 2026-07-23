# 文章 SDD（Spec-Driven Writing）

博客部分文章采用 **SDD**：你先写 **Spec**，AI 在 Spec 约束下 **润色并输出** 正文（交付物）。Spec 是需求与验收标准；`content/post/**/*.md` 是交付物。

## 角色分工

| 角色 | 负责 |
| ---- | ---- |
| **作者（你）** | 撰写、修订 `.ai/specs/*.md`：目的、读者、必写/禁写、结构、事实与口径 |
| **AI** | 阅读 Spec + [AGENTS.md](../AGENTS.md)；生成或修改交付物；润色语言；对照 Spec 验收清单自查；**不擅自改写 Spec**（除非你要求同步更新 Spec） |

AI **不得**把 Spec 全文贴进发布文章，也不得把 Spec 当成对外章节发布。

## 目录约定

```text
.ai/
├── README.md           # 索引
├── article-sdd.md      # 本文件：SDD 流程与 AI 约束
├── delivery-style.md   # 交付物共通文风（加粗、默认语气等）
└── specs/
    └── {slug}.md       # 文章 Spec（你维护）

content/post/.../{slug}.md   # Hugo 交付物（AI 在 Spec 基础上输出/改稿）
```

- **Spec 文件名** 与交付物 **slug** 一致（如 `exploration.md`）。
- Spec 内用表格字段记录：`url`、`title`、交付物路径、状态（draft / published）。

### 周记 Spec（跨仓库例外）

周记（`weekly-*.md`）的 Spec 存放在**私有仓库** `w10n-config`，不在本仓库 `.ai/specs/`：

```text
w10n-config/ops/weekly/weekly-2026-wNN.md   # 周记 Spec / 原始素材（私有，无需脱敏）
blog/content/post/career/weekly-2026-wNN.md # 周记交付物（公开成稿）
```

决策依据见 `w10n-config/ops/ADR-0002-weekly-spec-to-private-repo.md`。

| 环节 | 一般 SDD | 周记 |
| ---- | -------- | ---- |
| Spec 位置 | `blog/.ai/specs/{slug}.md` | `w10n-config/ops/weekly/weekly-*.md` |
| 交付物位置 | `blog/content/post/.../{slug}.md` | 不变 |
| 脱敏时机 | 写 Spec 时注意口径 | Spec **不脱敏**；**润色成交付物时**脱敏与内容筛选 |
| Phase 6 提交 | 同仓一次 commit | **两仓分别 commit**（见下文） |

**周记 AI 额外约束**

- 「先读 Spec」指向 `w10n-config/ops/weekly/weekly-*.md`，不是 `blog/.ai/specs/`。
- 交付物**禁止**逐字搬运私有 Spec §A 的敏感细节；只发布作者在 Spec 中标记为「可公开」或经筛选的内容。
- **下一周 Spec 模板（强制）**：处理任意一周周记 Spec 时（补充素材、Phase 3–6、或其它对该 Spec 的操作），必须检查下一周 `w10n-config/ops/weekly/weekly-YYYY-w{NN+1}.md` 是否已存在；若不存在，立刻从 `w10n-config/ops/weekly/_template.md` 生成空 Spec（填元信息 + 该周 7 天日期，状态 `spec-created`，不填 §A 素材）。细则见 `w10n-config/ops/AGENTS.md` §下一周 Spec 模板。

## Spec 不会出现在最终 Blog 里

**是的，Spec 不会被 Hugo 渲染为公开页面。**

原因：

1. Hugo 只发布 **`content/`** 目录下的页面（本站为 `content/post/` 等）；**`.ai/` 在仓库根目录，不在 content 内**。
2. 未配置 `module.mounts` 将 `.ai` 挂载进站点。
3. CI / 本地 `hugo` 构建不会把 `.ai/specs/` 当作文章编译。

因此：Spec 可写内部备注、验收清单、敏感口径说明；读者只能看到 `content/post/` 里的交付物。

> 若将来把 Spec 误放到 `content/post/` 下，**会**被当成文章发布——请勿这样做。

## Spec 建议结构（模板）

新建 Spec 时可复制以下骨架（作者填写）。**状态字段**追踪写作阶段：

```
spec-created → qa-in-progress → draft-written → annotating → published
```

完整模板见 [specs/_template.md](specs/_template.md)，含 §A 原始素材、§B AI 审阅 · 问答、§C 批注三个迭代章节。

简要骨架：

```markdown
# Spec: {文章标题}

| 字段 | 值 |
| ---- | -- |
| 状态 | draft / published |
| 交付物 | `content/post/.../{slug}.md` |
| Hugo url | `{slug}` |
| 标题 | … |
| 分类 | … |

## 1. 目的
## 2. 读者
## 3. 核心信息（必须传达）
## 4. 必须包含（验收清单，checkbox）
## 5. 禁止包含（Do NOT）
## 6. 语气与风格
## 7. 建议结构（大纲）
## 8. 可选 / 后续修订
## 9. 修订流程
## 10. 变更记录

（标签验收见 [specs/_template.md](specs/_template.md) §4。）
```

## AI 处理 Spec 时的强制约束

编辑或生成 **已有 Spec 的交付物** 时，AI **必须**：

1. **先读** 对应 Spec，再读或改 `content/post/.../{slug}.md`。一般文章 Spec 在 `.ai/specs/{slug}.md`；**周记**在 `w10n-config/ops/weekly/weekly-*.md`（见上文 §周记 Spec）。处理周记时**同时检查**下一周空 Spec 是否已生成（见上文「下一周 Spec 模板」）。
2. **以 Spec 为准**：§必须包含 / §禁止包含 优先于 AI 自行发挥；与 Spec 冲突时，**以 Spec 为准** 或向作者确认。
3. **仍遵守** [AGENTS.md](../AGENTS.md) 中博客文章规则（文件名、`url`、`categories`、`lastmod`、`tags`、MD025、表格与代码块等）。Spec 可补充、不可削弱 AGENTS 底线；**全站内容约束**见 [content-constraints.md](content-constraints.md)（如 VPN 命名、代码块注释用英文）。
4. **润色范围**：语句、段落衔接、Markdown 格式、结构对齐 Spec 大纲；**不编造** Spec 未允许的事实（金额、承诺、客户名等）。交付物格式、人称（淡化「我」）与加粗默认遵守 [delivery-style.md](delivery-style.md)；单篇 Spec §格式 / §语气 仅写 **本篇例外**。
5. **完成后**：按 Spec §验收清单逐项核对；在回复中简要说明已满足 / 未满足项。
6. **更新 Spec**：仅当作者明确要求「同步 spec」或「把 xx 写进 spec」时修改 `.ai/specs/`；改交付物后 **不要** 默认改 Spec。
7. **标签（SDD 专用）**：见下文 §标签；与 AGENTS 默认的 `remix` 流程不同。

**无 Spec 的文章**：仍按 AGENTS.md 常规流程；**不**读 delivery-style.md，**不**强制 SDD 标签与文风。

## 标签（SDD 交付物）

SDD 文章由 **作者写 Spec（原创意图与事实）**，AI 仅润色与成稿，交付物视为 **原创内容**，不用 `remix`。

| 标签 | SDD 交付物 |
| ---- | ---------- |
| **`original`** | **必须**（表示原创叙事 / 作者主导的 Spec） |
| **`AI-assisted`** | **必须**（AI 参与润色与输出） |
| **`remix`** | **禁止**（与 `original` 互斥） |
| **`reprint`** | **禁止**（转载文不适用） |

另加与正文相关的技术标签（如 `career`、`AI`）。

**新建 SDD 交付物**：`date` + `lastmod` + `url` + `original` + `AI-assisted` + 内容标签。

**编辑已有 SDD 交付物**：按需更新 `lastmod`（规则同 [AGENTS.md](../AGENTS.md) §更新文章日期：同日不重复更新）；保持 `original` + `AI-assisted`；若误有 `remix` / `reprint` 须删除。

Spec §验收清单中应写明标签要求（见 [specs/_template.md](specs/_template.md)）。

## SDD 写作阶段与 AI 约束

SDD 文章从主题到发布分为六个阶段，Spec 的 `状态` 字段追踪当前所处阶段。

| 阶段 | 状态值 | 触发 | AI 行为 |
| ---- | ------ | ---- | ------- |
| **Phase 1** 创建 Spec | `spec-created` | 作者给定主题，说"帮我创建空白 spec" | 从 `_template.md` 生成空白 Spec，填写已知元信息（url、标题、分类），**不填充内容章节**；作者在 §A 写完原始素材后通知 AI review |
| **Phase 2** 写原始素材 | （无独立状态） | 作者在 §A 写入原始文字 | AI 不参与 |
| **Phase 3** 审阅 · 问答 | `qa-in-progress`（AI 自动设置） | 作者说"review 这个 spec" | 将状态更新为 `qa-in-progress`；读 §A 原始素材 + §B 已有内容，在 §B 末尾追加新 Round；每轮末尾说明是否建议输出正文 |
| **Phase 4** 输出正文 | `draft-written`（AI 自动设置） | 作者说"输出正文"或"按 spec 生成交付物" | 将状态更新为 `draft-written`；综合 §A 原始素材 + §B 所有问答生成交付物 |
| **Phase 5** 批注修改 | `annotating`（AI 自动设置） | 作者在 §C 写批注后说"按批注修改" | 将状态更新为 `annotating`；逐条读 §C，执行完毕后将 `[ ]` 改为 `[done]`；全部完成后提示可进入 Phase 6 发布 |
| **Phase 6** 发布提交 | `published`（AI 自动设置） | 作者说"可以发布了" / "帮我提交" / "git commit" | 将 Spec 状态更新为 `published`；执行 `git add <交付物> <spec>`；`git commit -m "post: <title> (<slug>)"`；**默认不 push**；询问作者是否一起推送。**周记另须**：确认下一周空 Spec 已存在（见上文「下一周 Spec 模板」）；若本步新建了下一周 Spec，一并纳入 `w10n-config` 的 commit |

### Phase 3 核心禁止行为

- **禁止修改 §A 原始素材**，无论内容多混乱或不完整
- **禁止修改已有 Round**，只能在 §B 末尾追加新 Round
- 问题应聚焦于：事实确认、结构模糊、缺失关键信息

### Phase 3 就绪判断

当 §A + §B 所有信息已足以支撑完整输出正文时，在当轮末尾主动提示："信息已充分，建议输出正文"；信息不足时不要在每轮末尾重复提示。

### Phase 5 核心禁止行为

- **禁止删除 §C 批注条目**，已完成的只改 `[ ]` → `[done]`
- 每次修改交付物后按需更新 `lastmod`（东八区时间；若 `lastmod` 已是当天日期则保持不变）

### Phase 6 核心规则

- commit message 格式：`post: <文章标题> (<slug>)`
- `git add` 只含交付物（`content/post/.../{slug}.md`）和对应 Spec（`.ai/specs/{slug}.md`），**不要** `git add .`
- **周记例外**：Spec 在 `w10n-config/ops/weekly/`，交付物在 `blog/`。**两仓分别 commit**：
  - `w10n-config`：`git add ops/weekly/weekly-*.md` → `post: 2026 WNN (weekly-2026-wNN)` 或 `spec: weekly-2026-wNN`
  - `blog`：`git add content/post/career/weekly-*.md` → `post: 2026 WNN (weekly-2026-wNN)`
- **默认只做本地 commit，不 push**；push 必须作者确认或明确要求
- 如果工作区有其他未提交文件，提示作者注意，但不将其包含在本次 commit 中

---

## 作者修订流程

1. 只改 Spec（需求、禁区、结构）。
2. 让 AI「按 `.ai/specs/{slug}.md` 更新交付物」。
3. 自己通读交付物 + 勾 Spec 验收清单。
4. 对外发布前确认：交付物 front matter 与 Spec 表中 `title` / `url` 一致；`title` 须含英文（见 [AGENTS.md](../AGENTS.md) §标题规范）。

## 与 AGENTS.md、delivery-style.md 的关系

- **AGENTS.md**：所有博客改动的通用规则（含 front matter、标签、Markdown lint）。
- **[delivery-style.md](delivery-style.md)**：SDD **交付物正文** 的共通 prose 风格（默认不加粗、不说教等）；各篇 Spec 只写本篇例外。
- **article-sdd.md（本文件）**：Spec 驱动写作的流程与 AI 边界。
- **[content-constraints.md](content-constraints.md)**：全站内容约束（VPN 命名等）。
- **`.ai/specs/{slug}.md`**：单篇文章的需求、验收与 **本篇特有** 语气/格式例外。

冲突时优先级：**单篇 Spec（本篇例外）> delivery-style.md > AGENTS.md**；单篇 Spec 未写明的，以 delivery-style 为准。单篇 Spec 的 **例外** 不得削弱 AGENTS 底线（如 MD025、时区）。
