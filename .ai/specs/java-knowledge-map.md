# Spec: Java 领域知识关系图（内部链接策略）

| 字段 | 值 |
| ---- | -- |
| 状态 | draft |
| 类型 | **task spec**（站点配置 + 脚本批量改链 + 交付物） |
| 交付物 | `content/post/language/java/java-knowledge-map.md`（触发本 task；**全站**互链一并迁移，见 §4.3） |
| 脚本 | `scripts/migrate-internal-links.py` |
| 站点配置 | `config.toml` |
| Hugo `url` | `java-knowledge-map` |
| 标题 | Java 领域知识关系图 |
| 分类 | `language` |
| 创建日期 | `2026-05-31`（各文 `date`、`lastmod` 本次均勿改） |

---

## 1. 目的

1. **文章**：用关系图 + 索引表串起 Java/JVM 相关专题文，便于从一点跳到专题。
2. **本 task**：将 **Markdown 内链** 从 Hugo permalink（`/hotspot`）改为 **相对 `.md` 路径**（`./hotspot.md`），并启用 Hugo **embedded link render hook**，使：
   - VS Code Markdown 预览 / 源码 Cmd+点击 → 打开对应 `.md`；
   - `hugo` 构建后线上 → 仍解析为正确 permalink（如 `/hotspot/`）。
3. **实现方式**：用 **Python 脚本全站批量替换**（实测约 **35 篇 / ~224 链**），避免手工维护相对路径。

## 2. 读者

- 博客读者：在站点内按主题浏览 Java 知识链。
- 作者 / AI：在仓库内维护索引表，需能在编辑器内直接跳转源码。

## 3. 核心信息（必须传达）

- 知识地图的定位不变：索引 + mermaid 总览，不是各专题的重复讲解。
- 链接策略变更仅影响 **维护体验与构建解析**，不改变文章语义与结构。

## 4. 任务范围

### 4.1 在 scope 内

| # | 任务 | 说明 |
| - | ---- | ---- |
| T1 | `config.toml` 启用 embedded link hook | `[markup.goldmark.renderHooks.link] useEmbedded = "always"` |
| T2 | 编写 `scripts/migrate-internal-links.py` | 见 §5 |
| T3 | 脚本 `--dry-run` → 人工看报告 → `--write` 执行 | 先 **`--file` 单篇试点**（§4.3），线上验证后再 **`--scope all` 全站** |
| T4 | 全站 `hugo` 构建通过 | 含 draft；修复 hook 误解析个案（§8） |
| T5 | 被改文件 front matter（仅标签） | 标签规则见 §5.6；**不**改 `lastmod` |
| T6 | 更新 AI 文档：全站内链规范 | 见 §6；新建 `.ai/internal-links.md`，更新 `AGENTS.md`、`.ai/README.md` |

### 4.2 不在 scope 内

- 不改各文正文语义（mermaid 节点、表格行、段落措辞）。
- 不改代码块 / 纯文本里的 permalink 字面量（如 `` `/hotspot` ``）。

### 4.3 批量改链 scope

**分两步执行**（作者可在线上中间验证）：

| 步骤 | 命令 | 范围 | 说明 |
| ---- | ---- | ---- | ---- |
| **试点** | `--file <path>` | **单篇** `.md` | 先改一篇（默认试点文：`java-knowledge-map.md`），部署线上验证 VS Code + Hugo 跳转 |
| **全站** | `--scope all`（默认） | 全 `content/` | 试点通过后执行；**~35 篇 / ~224 链** |

含 Java 集群及 pattern、cloud、react、maven 等。`--scope java` 仍保留作目录级局部重跑。

**参数优先级**：指定 `--file` 时 **忽略 `--scope`**，只处理该文件内 outbound 链接。

**预期跳过（非 UNRESOLVED）**：`/url` 文档示例（4 处）、静态资源路径（如 `/user/desktop/doge.png`）——计入报告 `SKIPPED`，不要求替换。

---

## 5. Python 脚本规格

**路径**：`scripts/migrate-internal-links.py`

**依赖**：仅 Python 3 标准库（`pathlib`、`re`、`argparse`、`datetime` 等）。

### 5.1 链接匹配

- 匹配 Markdown 内链：`[text](/permalink)`、`[text](/permalink#anchor)`。
- **跳过** fenced code block（`` ``` `` 围住的行）。
- **跳过** 非文章目标（写入 `SKIP_TARGETS`，至少包含）：
  - `/url`（文档示例，如 `maven构建之依赖传递.md`）
  - 明显静态资源路径（如 `/user/desktop/doge.png`）
- **保留** `#anchor` 后缀：`/btrace#foo` → `./btrace.md#foo`。

### 5.2 目标文件解析（permalink → `.md` 路径）

按优先级：

1. **front matter `url`**：扫描 `content/**/*.md`，建索引 `url`（去 leading `/`）→ 文件路径。
2. **slug fallback**：permalink 最后一段与 `{stem}.md` 匹配（例：`/java-gc` → `java-gc.md`，尽管其 `url` 为 `java/gc`）。
3. **重复 `url`**（全站约 32 组）：优先 **非 inbox**；同目录多级候选时优先路径更深、非 draft 的文件。
4. 仍无法解析 → **不替换**，写入报告 `UNRESOLVED`。

### 5.3 相对路径生成

- 自 **当前源文件目录** 计算到目标 `.md` 的 `os.path.relpath`，统一 `/` 分隔。
- 同目录：`./hotspot.md`；跨目录：`../../cs/dcevm-hotswapagent.md`。

### 5.4 CLI

```text
# 单篇试点（部署线上验证）
python3 scripts/migrate-internal-links.py --dry-run --file content/post/language/java/java-knowledge-map.md
python3 scripts/migrate-internal-links.py --write   --file content/post/language/java/java-knowledge-map.md

# 全站（试点通过后）
python3 scripts/migrate-internal-links.py --dry-run [--scope all|java]
python3 scripts/migrate-internal-links.py --write   [--scope all|java]
```

| 选项 | 说明 |
| ---- | ---- |
| `--dry-run` | 只输出报告，不写文件 |
| `--write` | 原地写回；与 `--dry-run` 互斥 |
| `--file PATH` | **仅处理指定一篇**；路径相对仓库根或绝对路径；与 `--scope` 互斥（指定 `--file` 时忽略 scope） |
| `--scope all` | 未指定 `--file` 时的 **默认**；全 `content/` |
| `--scope java` | 未指定 `--file` 时可选；仅 `content/post/language/java/**` + `content/post/cs/**` |

**`--file` 行为**

- 只替换 **该文件内** 的 outbound Markdown 内链；不修改其它文章。
- 目标解析仍扫描 **全站** `content/**/*.md` 建索引（跨目录相对路径需全站 index）。
- 路径不存在或非 `.md` → 报错 exit 1。
- 试点推荐：`content/post/language/java/java-knowledge-map.md`（链多、跨目录齐全）。

**报告内容**（stdout 或 `--report FILE` 可选）：

- 每文件：替换条数、样例（旧 → 新）
- `UNRESOLVED` 列表
- `SKIPPED` 列表

### 5.5 写回规则

- 仅替换链接 destination；**不改** link text、正文其它内容。
- 同一文件无链接变更 → 不 touched。

### 5.6 front matter（`--write` 时）

对每个 **有链接变更** 的文件：

| 字段 | 规则 |
| ---- | ---- |
| `lastmod` | **不修改**（本次仅为链接格式迁移，不算内容修订） |
| `date` | **不修改** |
| `tags` | 已有 `original` → 只确保有 `AI-assisted`，删 `remix`/`reprint`；否则确保有 `remix` + `AI-assisted`，删 `reprint` |
| `java-knowledge-map.md` | SDD 特例：`original` + `AI-assisted` + `java` + `jvm`，无 `remix` |

### 5.7 抽检样例（脚本输出应满足）

自 `java-knowledge-map.md` 出发：

| 原 permalink | 期望相对路径 |
| ------------ | ------------ |
| `/hotspot` | `./hotspot.md` |
| `/dcevm-hotswapagent` | `../../cs/dcevm-hotswapagent.md` |
| `/safepoint` | `../../other/safepoint.md` |
| `/spring-boot` | `./spring/spring-boot.md` |

构建后（Hugo hook）：

| 相对路径 | 期望线上 `href` |
| -------- | --------------- |
| `./hotspot.md` | `/hotspot/` |
| `../../cs/dcevm-hotswapagent.md` | `/dcevm-hotswapagent/` |

---

## 6. AI 文档规格（全站内链规范）

本 task **必须** 落地可执行的 AI/作者规范，结构与 [content-constraints.md](../content-constraints.md) 并列：细则在 `.ai/`，`AGENTS.md` 只保留摘要与链接。

### 6.1 新建 `.ai/internal-links.md`

**必须包含**（章节标题可微调，语义不可缺）：

| 章节 | 内容要点 |
| ---- | -------- |
| 适用范围 | 所有 `content/post/**/*.md`（SDD 与非 SDD） |
| 背景 | `/permalink` 仅 Hugo 线上有效；VS Code 预览需相对 `.md`；embedded hook 在构建时解析回 permalink |
| 写法规则 | 站内互链用 `[text](./relative/target.md)` 或 `../…/target.md`；**禁止**新建 `[text](/permalink)` |
| 路径计算 | 相对 **当前源文件** 目录；跨目录用 `../../`；链到 **目标 `.md` 文件**，不按 front matter `url` 猜路径 |
| Anchor | 保留 `#heading`：`./foo.md#section` |
| 代码块 | fenced code 内的 `` `/hotspot` `` 等字面量 **不** 改为 `.md` |
| 站点配置 | `config.toml` 须 `[markup.goldmark.renderHooks.link] useEmbedded = "always"`；无自定义 `render-link.html` |
| 批量迁移 | 指向 `scripts/migrate-internal-links.py`：`--file` 单篇试点、`--scope all` 全站、`--dry-run` / `--write` |
| AI 改稿 | 新增或修改互链时默认写相对 `.md`；不确定目标文件时用 `find content -name` 查路径 |
| 例外 | 外链 `https://`、静态资源、`/url` 等文档示例不套用 |

### 6.2 更新 `AGENTS.md`

在「检查并更新文章 URL」**之后**（或编辑工作流程清单中）增加 **「站内 Markdown 内链」** 小节：

- 3–5 条核心规则（相对 `.md`、禁 `/permalink`、代码块例外）
- 链接至 [`.ai/internal-links.md`](../.ai/internal-links.md) 全文
- 编辑文章检查清单（§工作流程）增加一项：**站内互链是否为相对 `.md`**

### 6.3 更新 `.ai/README.md`

文档索引表增加一行：

| 文件 | 用途 |
| ---- | ---- |
| [internal-links.md](internal-links.md) | **全站内链**：相对 `.md` + Hugo embedded hook |

### 6.4 可选（本 task 不强制）

- [article-sdd.md](article-sdd.md) 加一句「互链见 internal-links.md」——若 AGENTS 已链出则可省略。

---

## 7. 必须包含（验收清单）

### 站点配置

- [ ] `config.toml` 已添加 `[markup.goldmark.renderHooks.link]`，`useEmbedded = "always"`
- [ ] 项目内 **无** 自定义 `layouts/_markup/render-link.html`
- [ ] `hugo` 全站构建 **exit 0**（误解析个案按 §8 处理）

### 脚本

- [ ] `scripts/migrate-internal-links.py` 存在，符合 §5；支持 `--file`、`--scope all`（默认）
- [ ] `--dry-run --file content/post/language/java/java-knowledge-map.md`：**0 UNRESOLVED**
- [ ] `--write --file …/java-knowledge-map.md` 已执行（试点）；作者可部署线上验证
- [ ] `--dry-run`（默认 scope all）报告：**0 UNRESOLVED**；已知跳过项仅 §4.3（`SKIPPED`）
- [ ] `--write`（默认 scope all）已执行；git diff 仅链接 destination + 标签（如有），**无 `lastmod` 变更**

### 交付物与全站文章

- [ ] `java-knowledge-map.md`：标题、url、分类与 Spec 表一致；MD025；代码块内 permalink 文本未改
- [ ] 全 `content/` 内所有 `[...](/permalink)` 内链（非代码块、非 SKIPPED）已变为相对 `.md`
- [ ] 被改文件标签符合 §5.6；**`lastmod` 未变**
- [ ] `java-knowledge-map.md` 标签：`original`、`AI-assisted`、`java`、`jvm`

### 构建抽检（至少 3 条）

- [ ] `./hotspot.md` → 线上 `/hotspot/`
- [ ] `../../cs/dcevm-hotswapagent.md` → `/dcevm-hotswapagent/`
- [ ] `../../other/safepoint.md` → `/safepoint/`

### AI 文档（T6）

- [ ] `.ai/internal-links.md` 存在，§6.1 各节齐全
- [ ] `AGENTS.md` 已增加站内内链摘要 + 指向 `.ai/internal-links.md`
- [ ] `.ai/README.md` 索引已登记 `internal-links.md`

---

## 8. 禁止包含（Do NOT）

- 不要把 Spec 或脚本报告贴进文章正文。
- 不要用脚本改代码块内文本、外部 `https://` 链接、或 `SKIPPED` 目标。
- 不要改任何文 `date`、**`lastmod`** 字段。
- 不要为迁就链接删改 mermaid 节点或表格行。
- 不要跳过 `--dry-run` 直接 `--write`（全站 ~35 篇，须先看报告）。

---

## 9. 已知风险与处理

| 风险 | 处理 |
| ---- | ---- |
| embedded hook 误解析 `[...](...)` | 全站 `hugo` 构建；报错处 **包进代码块** 或改写，不关闭 hook |
| 已知个案 | `java正则表达式.md` 正则示例；启用 hook 后可能报错 |
| 重复 `url` 指错文 | 脚本 inbox deprioritize；dry-run 人工 spot-check 互链密集文 |
| slug fallback 歧义 | 报告 `AMBIGUOUS`（若多候选同 stem）；不自动替换 |
| VS Code 预览仍失败 | workspace 根为 `blog` 仓库根 |

---

## 10. 语气与风格

- 交付物为 **索引型技术文**，非个人叙事。
- 默认见 [delivery-style.md](../delivery-style.md)；本篇可保留现有 **关系图 + 表格** 结构。

---

## 11. 建议结构（交付物大纲，保持现状）

1. 背景
2. 总览关系图（mermaid）
3. 按主题索引（多级 `###` + 表格）
4. BTrace 相关概念链（精读路径，代码块）
5. 易混淆对照
6. 维护说明

---

## 12. 可选 / 后续修订

- 脚本 `--check` 模式：CI 检测是否仍有 `/permalink` 内链（防回退）。

---

## 13. 修订流程

1. 作者改本 Spec。
2. AI 执行 T1 → T2 → **`--file` 试点**（`java-knowledge-map.md`）→ 作者 **部署线上验证**。
3. 验证通过后：`--scope all` 全站 `--write` → T4–T6，对照 §7 验收。
4. 作者：`hugo server` + VS Code 预览点链抽检。
5. 通过后 Spec 状态改为 `published`。

---

## 14. 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-05-31 | 初版：相对 `.md` 链接 + embedded link hook task spec |
| 2026-05-31 | 纳入 Python 脚本批量改链；Phase B（Java 集群 17 篇）为默认 scope；§5 改为脚本规格 |
| 2026-05-31 | T6：全站内链规范纳入 scope；§6 AI 文档规格（`.ai/internal-links.md` + AGENTS + README） |
| 2026-05-31 | 批量改链默认改为全站 `--scope all`（~35 篇 / ~224 链）；取消 Phase B/C 分阶段 |
| 2026-05-31 | CLI 增加 `--file` 单篇试点；修订流程：先试点部署验证再全站 |
| 2026-05-31 | 链接迁移 **不改 `lastmod`**（§5.6、T5） |
