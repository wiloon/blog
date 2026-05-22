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
└── specs/
    └── {slug}.md       # 文章 Spec（你维护）

content/post/.../{slug}.md   # Hugo 交付物（AI 在 Spec 基础上输出/改稿）
```

- **Spec 文件名** 与交付物 **slug** 一致（如 `exploration.md`）。
- Spec 内用表格字段记录：`url`、`title`、交付物路径、状态（draft / published）。

## Spec 不会出现在最终 Blog 里

**是的，Spec 不会被 Hugo 渲染为公开页面。**

原因：

1. Hugo 只发布 **`content/`** 目录下的页面（本站为 `content/post/` 等）；**`.ai/` 在仓库根目录，不在 content 内**。
2. 未配置 `module.mounts` 将 `.ai` 挂载进站点。
3. CI / 本地 `hugo` 构建不会把 `.ai/specs/` 当作文章编译。

因此：Spec 可写内部备注、验收清单、敏感口径说明；读者只能看到 `content/post/` 里的交付物。

> 若将来把 Spec 误放到 `content/post/` 下，**会**被当成文章发布——请勿这样做。

## Spec 建议结构（模板）

新建 Spec 时可复制以下骨架（作者填写）：

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

1. **先读** 对应 `.ai/specs/{slug}.md`，再读或改 `content/post/.../{slug}.md`。
2. **以 Spec 为准**：§必须包含 / §禁止包含 优先于 AI 自行发挥；与 Spec 冲突时，**以 Spec 为准** 或向作者确认。
3. **仍遵守** [AGENTS.md](../AGENTS.md) 中博客文章规则（文件名、`url`、`categories`、`lastmod`、`tags`、MD025、表格与代码块等）。Spec 可补充、不可削弱 AGENTS 底线。
4. **润色范围**：语句、段落衔接、Markdown 格式、结构对齐 Spec 大纲；**不编造** Spec 未允许的事实（金额、承诺、客户名等）。交付物 **默认少用加粗**（`**...**`）；若 Spec 有 §格式，以 Spec 为准；无 §格式 时不为扫读而给日期、主题词、清单项等加粗。
5. **完成后**：按 Spec §验收清单逐项核对；在回复中简要说明已满足 / 未满足项。
6. **更新 Spec**：仅当作者明确要求「同步 spec」或「把 xx 写进 spec」时修改 `.ai/specs/`；改交付物后 **不要** 默认改 Spec。
7. **标签（SDD 专用）**：见下文 §标签；与 AGENTS 默认的 `remix` 流程不同。

**无 Spec 的文章**：仍按 AGENTS.md 常规流程；不强制 SDD。

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

**编辑已有 SDD 交付物**：只更新 `lastmod`；保持 `original` + `AI-assisted`；若误有 `remix` / `reprint` 须删除。

Spec §验收清单中应写明标签要求（见 [specs/_template.md](specs/_template.md)）。

## 作者修订流程

1. 只改 Spec（需求、禁区、结构）。
2. 让 AI「按 `.ai/specs/{slug}.md` 更新交付物」。
3. 自己通读交付物 + 勾 Spec 验收清单。
4. 对外发布前确认：交付物 front matter 与 Spec 表中 `title` / `url` 一致。

## 与 AGENTS.md 的关系

- **AGENTS.md**：所有博客改动的通用规则（含 front matter、标签、Markdown lint）。
- **article-sdd.md（本文件）**：Spec 驱动写作的流程与 AI 边界。
- **`.ai/specs/{slug}.md`**：单篇文章的需求与验收。

三者同时生效；冲突时：**单篇 Spec > AGENTS.md 通用规则** 仅适用于该 Spec 已明确写明的例外，且须在 Spec 中写清楚。
