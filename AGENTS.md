# AI Agent 工作指南

## 文章 SDD（Spec 驱动写作）

部分文章采用 **SDD**：作者在 `.ai/specs/{slug}.md` 维护 Spec，AI 在 Spec 基础上润色并输出交付物 `content/post/**/*.md`。

- **流程与 AI 约束**：见 [.ai/article-sdd.md](.ai/article-sdd.md)
- **Spec 索引**：见 [.ai/README.md](.ai/README.md)
- **内容约束（VPN 命名等）**：见 [.ai/content-constraints.md](.ai/content-constraints.md)
- **Spec 不会渲染到最终 blog**（仅在 `content/` 下的 Markdown 会发布）

编辑 **带有 Spec 的文章** 时：必须先读对应 Spec，以 Spec 的「必须包含 / 禁止包含」为准；正文 prose 风格（默认不加粗、人称适度用「我」等）另见 [.ai/delivery-style.md](.ai/delivery-style.md)。涉及 VPN 等敏感表述时另见 [.ai/content-constraints.md](.ai/content-constraints.md)。仍遵守下文 front matter、标签与 Markdown 规则。**无 Spec 的文章** 不读 delivery-style，但 **仍须** 遵守 content-constraints；其余按常规流程与下文规则处理。

**SDD 交付物标签**（作者写 Spec、AI 润色成稿）：必须使用 **`original`** + **`AI-assisted`**，**不得**使用 `remix` 或 `reprint`（与 §添加 AI 辅助标签 中 `original` 优先级规则一致）。详见 [.ai/article-sdd.md](.ai/article-sdd.md) §标签。

---

## 🚨 编辑博客文章强制规则 🚨

### ⚠️ 每次编辑文章必做五件事（缺一不可）：

> **无论改动大小——哪怕只是删除一行、修改一个词——都必须执行以下全部步骤。**

1. ✅ **检查文件名和标题** → 文件名必须是英文，且与文章内容匹配；**如果文件名含中文，必须先用 `mv` 重命名再做任何其他修改**
2. ✅ **检查并更新 URL** → 确保 URL 与文章标题匹配
3. ✅ **检查并更新 categories** → 确保分类与文章实际内容匹配
4. ✅ **更新 lastmod 字段** → 若 `lastmod` 的日期（东八区）**不是今天**，则更新或添加为当前东八区时间；若**已是今天**则**保持不变**；`date` 字段保留原始创建日期，**不要修改**
5. ✅ **添加标签** → 先检查是否有 `original` 标签：有则只加 `AI-assisted` 并删除 `remix`/`reprint`；无则加 `remix` 和 `AI-assisted` 并删除 `reprint`
6. ✅ **编辑内容** → 完成实际的文章修改
7. ✅ **维护记录** → 仅当文章 `date` **不是今天**（即已发布文章）时，才在文章末尾添加或更新 `## 维护记录` 表格；今天新建并首次发布的文章**不需要**维护记录

**❌ 如果只是移动文件位置，不要更新日期和标签！**

---

## 编辑博客文章详细说明

### 检查并更新文件名和标题

**核心规则：每次编辑文章时必须检查文件名和标题是否与文章内容匹配**

#### 文件名规范

- 文件名**必须使用英文**，不允许中文或特殊字符
- 使用小写字母和连字符（kebab-case），如 `exception-handling.md`
- 文件名应简洁地反映文章的核心主题
- **不要用父目录名做文件名前缀**：文件已经放在对应目录下，前缀重复冗余
  - ❌ `java/java-exception-handling.md`（`java-` 前缀与目录重复）
  - ✅ `java/exception-handling.md`
- 如果发现文件名是中文或与内容不符，**用 `mv` 命令重命名**

**示例：**

```bash
# 错误示例（中文文件名）
一篇不错的讲解java异常的文章.md  # ❌

# 错误示例（目录名重复做前缀）
content/post/language/java/java-exception-handling.md  # ❌

# 正确示例（英文、语义化、无冗余前缀）
content/post/language/java/exception-handling.md  # ✅
```

#### 标题（title）规范

- `title` 字段应准确反映文章的实际内容
- 如果原标题含糊或与内容不符，更新为更准确的标题
- 标题可以是中文或英文，但要有实际语义
- **避免极端/夸张词汇**：不用「最佳实践」「终极指南」「深度解析」等，直接描述主题即可
  - ❌ `Shell 创建文件并写入内容的最佳实践`
  - ✅ `Shell 创建文件并写入内容`

**示例：**

```yaml
# 错误示例（标题含糊）
title: '一篇不错的讲解 Java 异常的文章（转载）'  # ❌ 不直接

# 正确示例（标题准确）
title: 'Java Exception Handling: Anti-Patterns and Best Practices'  # ✅
```

#### 文件名和标题检查清单

- ✅ 文件名是否为英文？如果不是，重命名为英文
- ✅ 文件名是否反映文章主题？如果不符，重命名
- ✅ `title` 是否准确描述文章内容？如果不符，更新
- ✅ 文件名、title、url 三者语义是否一致？

---

### 检查并更新文章 URL

**核心规则：每次编辑文章时必须检查和更新 URL**

#### URL 检查规则

1. **缺少 URL 字段必须添加**

   - 如果 front matter 中没有 `url` 字段，必须添加
   - 根据文章标题生成语义化 URL

1. **数字 URL 必须转换**

   - ❌ 错误格式：`url: /?p=4058`（WordPress 默认数字 ID）
   - ✅ 正确格式：`url: ai-agent-development`（语义化 URL）

1. **URL 必须与标题匹配**

   - 检查现有 URL 是否与文章标题语义相符
   - 如果不符，更新为与标题匹配的 URL

#### URL 命名规范

- 使用小写字母和连字符（kebab-case）
- 只包含英文字母、数字和连字符 `-`
- 简洁明了，反映文章主题
- 避免特殊字符、中文、下划线
- **不要用所在目录名做 URL 前缀**：文章已归类在对应目录（Hugo 会生成分类页），URL 无需重复分类信息
  - ❌ `java/exception-handling` 或 `java-exception-handling`（`java` 与目录重复）
  - ✅ `exception-handling`

**示例：**

```yaml
# 错误示例
title: AI Agent Development
url: /?p=4058  # ❌ 数字 URL

# 正确示例
title: AI Agent Development
url: ai-agent-development  # ✅ 语义化 URL
```

```yaml
# 错误示例（目录名重复做前缀）
title: Java 异常处理
url: java-exception-handling  # ❌ java 与所在目录重复

# 正确示例
title: Java 异常处理
url: exception-handling  # ✅ 不含目录前缀
```

```yaml
# 需要更新的示例
title: Docker 容器网络详解
url: docker-basic  # ❌ 不够准确

# 更新后
title: Docker 容器网络详解
url: docker-container-network  # ✅ 与标题匹配（docker 是主题词，非目录名）
```

#### URL 更新检查清单

- ✅ 检查 `url` 字段是否存在，**如果不存在则添加**
- ✅ 如果是 `/?p=数字` 格式，立即转换为语义化 URL
- ✅ 如果是非数字 URL，检查是否与标题语义匹配
- ✅ 确保 URL 遵循命名规范（小写、连字符分隔）

---

### 站内 Markdown 内链

**核心规则：站内互链写相对 `.md` 路径，不写 `/permalink`。**

1. ✅ 同目录：`[HotSpot](./hotspot.md)`；跨目录：`../../cs/dcevm-hotswapagent.md`
2. ❌ 不要新建 `[text](/hotspot)` 形式的站内链接
3. ✅ 保留 anchor：`./foo.md#section`；外链 `https://` 不变
4. ✅ 代码块内的 `` `/hotspot` `` 字面量 **不要** 改为 `.md`

细则与 Hugo 配置见 [`.ai/internal-links.md`](.ai/internal-links.md)。批量迁移用 `scripts/migrate-internal-links.py`（`--file` 单篇 / `--scope all` 全站）。

---

### 检查并更新 categories

**核心规则：每次编辑文章时必须检查 `categories` 是否与文章实际内容匹配**

#### categories 检查规则

- 查看文章的实际内容，判断分类是否准确
- 如果分类与内容不符，更新为正确的分类
- 如果缺少 `categories` 字段，必须添加

**常用分类参考：**

- `AI` — 人工智能、机器学习、LLM 相关
- `Linux` — Linux 系统、命令行工具
- `cloud` — 云计算、容器、K8s
- `development` — 通用开发话题
- `network` — 网络协议、配置
- `language` — 编程语言（Java、Go、Rust 等）

**示例：**

```yaml
# 错误示例（分类与内容不符）
title: Claude Code 使用指南
categories:
  - Linux   # ❌ 内容是 AI 工具，不是 Linux

# 正确示例
title: Claude Code 使用指南
categories:
  - AI      # ✅ 与内容匹配
```

#### categories 检查清单

- ✅ `categories` 字段是否存在？如果不存在则添加
- ✅ 分类是否与文章实际内容匹配？如果不符则更新

### 更新文章日期

`date` 和 `lastmod` 两个字段各司其职：

- `date` — 文章**原始创建日期**，一旦设定**永远不要修改**，Hugo 用它控制文章排序和归档
- `lastmod` — **最后修改日期**，编辑内容时按需更新（见下方规则）

**关键规则：**
- ✅ 新建文章 → 同时添加 `date`、`lastmod` 和 `url`，日期均设为当前时间
- ✅ 编辑已有文章，**有** `lastmod` 且其日期（东八区）**不是今天** → 更新 `lastmod` 为当前东八区时间，`date` 保持不变
- ✅ 编辑已有文章，**有** `lastmod` 且其日期（东八区）**已是今天** → **不要**再次更新 `lastmod`
- ✅ 编辑已有文章，**没有** `lastmod` 字段 → 添加 `lastmod` 设为当前时间，`date` 保持不变
- ❌ 仅移动文件到其他目录 → 不要更新任何日期
- 🕐 时区**必须**使用东八区 (UTC+8)，即 `+08:00`
- 🔧 **必须使用工具获取准确时间**：运行 `date '+%Y-%m-%dT%H:%M:%S+08:00'` 命令获取当前时间，不要猜测或估计时间
- ⚠️ **日期格式必须带时区**：必须使用 `2026-05-18T11:00:00+08:00` 格式，**不能**用 `"2026-05-18 11:00:00"`（无时区），否则 Hugo 当作 UTC 处理，导致文章被视为未来文章而不显示

示例（新建文章）：
```yaml
---
title: 文章标题
author: "-"
date: 2025-10-30T08:30:00+08:00     # 创建日期，不再修改
lastmod: 2025-10-30T08:30:00+08:00  # 最后修改日期；同日多次编辑时不重复更新
url: article-url
categories:
  - 分类
tags:
  - 标签1
  - 标签2
---
```

示例（编辑已有文章）：
```yaml
---
title: 文章标题
author: "-"
date: 2019-04-22T14:58:44+08:00     # ✅ 原始创建日期，保持不变
lastmod: 2025-10-30T08:30:00+08:00  # ✅ 若原 lastmod 不是今天，则更新为当前时间
url: article-url
---
```

**时区说明：**
- 使用 `+08:00` 表示东八区（北京时间、上海时间等）
- 不要使用 `+00:00` (UTC) 或其他时区
- 格式：`YYYY-MM-DDTHH:MM:SS+08:00`

---

### 添加 AI 辅助标签
当使用 AI 编辑或创建文章后，**必须立即**在同一次操作中添加以下标签到 `tags` 字段：

**标签使用规则：**
- **编辑已有文章**：必须添加 `remix` 和 `AI-assisted` 两个标签
  - `remix` - 表示内容经过重新编辑和改进（先写这个）
  - `AI-assisted` - AI 辅助编辑的标识（后写这个）
- **新建文章**：必须添加 `remix` 和 `AI-assisted` 两个标签
- **内容标签**：除强制标签外，必须根据文章实际内容添加具体技术标签（如 `java`、`go`、`docker`、`k8s` 等），便于检索

⚠️ **`remix` 和 `reprint` 不能同时存在**：添加 `remix` 标签时，如果文章已有 `reprint` 标签，必须将其删除。

⚠️ **`original` 标签优先级最高，与 `remix`/`reprint` 互斥**：如果文章已有 `original` 标签，**不要添加** `remix` 或 `reprint` 标签；如果文章同时存在 `original` 和 `remix`/`reprint`，必须将 `remix` 和 `reprint` 删除。

⚠️ **`content/post/career/` 目录特殊规则**：该目录下的文章全部是作者的真实工作经历，**必须带 `original` 标签，禁止添加 `remix` 或 `reprint` 标签**。无论新建还是编辑，标签规则等同于"有 `original` 标签"的情况。

⚠️ **不要忘记：**
- 编辑文章（无 `original` 标签）= 按需更新 `lastmod`（见 §更新文章日期）+ 添加 `remix` 和 `AI-assisted` 标签 + 删除 `reprint`（如有）
- 编辑文章（有 `original` 标签）= 按需更新 `lastmod`（见 §更新文章日期）+ 添加 `AI-assisted` 标签 + 删除 `remix` 和 `reprint`（如有）
- 新建文章 = 添加 `date` + `lastmod` + `url` + `remix` 和 `AI-assisted` 标签

示例：
```yaml
---
title: 文章标题
author: "-"
date: 2019-04-22T14:58:44+08:00     # 原始创建日期，保持不变
lastmod: 2025-10-31T08:30:00+08:00  # 若原 lastmod 不是今天，则更新为当前东八区时间
url: article-url
categories:
  - 分类
tags:
  - 原有标签        # 保留原有其他标签，但删除 reprint（如有）
  - java           # 内容相关的具体技术标签（必须添加）
  - remix          # 内容经过编辑改进（与 reprint 互斥，不能共存）
  - AI-assisted    # AI 辅助编辑的标识
---
```

### 编辑工作流程检查清单

每次编辑文章时，按以下顺序检查：

1. ✅ **检查文件名**：文件名必须是英文且与内容匹配，否则用 `mv` 重命名
2. ✅ **检查标题**：`title` 是否准确描述文章内容，否则更新
3. ✅ **检查 URL**：确认 URL 是否与标题匹配，转换数字 URL
4. ✅ **站内互链**：是否为相对 `.md`（见 [`.ai/internal-links.md`](.ai/internal-links.md)），而非 `/permalink`
5. ✅ **检查 categories**：分类是否与文章内容匹配，否则更新
6. ✅ **更新 lastmod**：若 `lastmod` 的日期（东八区）不是今天，则更新或添加为当前东八区时间；若已是今天则保持不变；`date` 字段**不要动**
7. ✅ **添加标签**：先检查文章是否有 `original` 标签：
   - **有 `original` 标签**：只添加 `AI-assisted`，删除 `remix` 和 `reprint`（如有）
   - **无 `original` 标签**：确保包含 `remix` 和 `AI-assisted`，并删除 `reprint`（如有）
   - 同时添加与文章内容相关的具体技术标签（如 `java`、`go`、`docker` 等）
8. ✅ **内容编辑**：完成实际的文章内容修改
9. ✅ **维护记录**：仅当文章 `date` **不是今天**（已发布文章）时，在文章末尾添加或更新 `## 维护记录` 表格（见下文规范）；今天新建并首次发布的文章**不需要**维护记录
10. ✅ **格式检查**：确保 Markdown 格式正确

**记忆口诀：编辑文章 = 改文件名 + 改标题 + 检查 URL + 站内互链 + 检查分类 + 按需更新 lastmod（不改 date；同日不重复）+ 加标签 + 改内容 + 维护记录（仅已发布文章）**

### 维护记录规范

**核心规则：仅对已发布文章（`date` 不是今天）进行 AI 辅助编辑后，才在文章末尾添加或更新 `## 维护记录` 章节。今天新建并首次发布的文章不需要维护记录。**

#### 格式

使用表格，固定三列：时间、修改内容、原因。

```markdown
## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-15 | 文件重命名为 `vsftpd.md`；url 改为 `vsftpd` | 文件名含中文不符合规范 |
| 2026-06-20 | 补充 TLS 配置说明 | 原文缺少安全配置内容 |
```

#### 规则

- 表格放在文章**最末尾**，是文章的最后一个章节
- 每次改动追加一行，**不要删除历史记录**
- 时间格式：`YYYY-MM-DD`（日期精度足够，无需时分秒）
- 修改内容：简洁列出改了什么，多项用分号分隔
- 原因：说明为什么要改
- 如果文章末尾已有 `## 维护记录`，直接在表格末尾追加新行
- **判断是否需要维护记录**：检查 front matter 的 `date` 字段，若日期是今天则跳过；若是过去日期则必须添加或追加

### 其他注意事项
- 保持文章格式的一致性
- 使用适当的 Markdown 语法
- 代码块要指定语言类型
- 保持中英文之间的适当空格

### Markdown lint 规范

#### 🚨 MD025 规则：禁止多个一级标题（Critical）

**核心规则：文章正文中不能出现一级标题 `#`**

- ❌ **错误示例**：

```markdown
---
title: 文章标题
---

# 文章标题  ← 错误！与 front matter 中的 title 重复

## 第一节
```

- ✅ **正确示例**：

```markdown
---
title: 文章标题
---

## 第一节  ← 正确！正文从二级标题开始
```

**为什么这样规定：**

1. Hugo 会自动将 front matter 中的 `title` 渲染为页面的 h1 标题
1. 如果正文再出现 `#`，会导致一个页面有多个 h1，违反 HTML 语义和 SEO 最佳实践
1. 搜索引擎和屏幕阅读器期望每个页面只有一个主标题

**检查清单：**

- ✅ front matter 中有 `title` 字段
- ✅ front matter 结束后（`---` 之后）紧接着是二级标题 `##`
- ❌ 正文中不出现一级标题 `#`

#### 其他重要 Markdown lint 规则

**标题规范：**

- 标题前后需有一个空行
- 标题层级不要跳级（不要从 `##` 直接跳到 `####`）
- 避免重复标题内容

**表格规范（MD060）：**

- 表格所有行的管道符 `|` 两侧必须有空格，风格必须统一
- 分隔行写法：`| --- | --- |`，**不要写** `|---|---|`
- 正确示例：

```markdown
| 选项 | 说明                     |
| ---- | ------------------------ |
| `-n` | 以 IP 地址代替主机名显示 |
```

- 错误示例（管道符后无空格）：

```markdown
| 选项 | 说明                     |
| ---- | ------------------------ |
| `-n` | 以 IP 地址代替主机名显示 |
```

**列表规范：**

- 列表项前后需有一个空行
- 无序列表统一使用 `-`，左侧不加多余空格
- 有序列表建议全部编号为 `1.`，Markdown 会自动渲染正确序号

```markdown
1. 第一项
1. 第二项
1. 第三项
```

**代码块规范：**

- 代码块使用三个反引号包裹，**必须指定语言类型**
- 代码块前后需要空行

```markdown
正确写法：

​```python
print("Hello")
​```

错误写法（缺少语言标识）：

​```
print("Hello")
​```
```

**Mermaid 图规范：**

- Mermaid flowchart（`graph TD` / `graph LR`）节点标签内换行**必须用 `<br/>`**，不能用 `\n`
  - ✅ 正确：`A[Adapter 转换<br/>dict → 对象]`
  - ❌ 错误：`A[Adapter 转换\ndict → 对象]`（`\n` 在节点标签里会被忽略，不会渲染为换行）
- `sequenceDiagram`、`classDiagram`、`stateDiagram-v2` 不涉及此问题，可正常使用文本

**空行规范：**

- front matter（YAML 区块）与正文之间有一个空行
- 避免多余空行（连续空行只保留一个）
- 段落之间用一个空行分隔

**其他规范：**

- 保证中英文之间有适当空格（如：`使用 Python 开发`）
- 链接和图片引用格式要正确
- 行尾不要有多余空格

> 参考 lint 工具：markdownlint、remark-lint
>
> **常见 lint 错误代码：**
>
> - MD025: 多个一级标题
> - MD029: 有序列表编号不一致
> - MD031/MD032: 代码块/列表缺少空行
> - MD040: 代码块缺少语言标识
> - MD041: 文件第一行应该是顶级标题（通常忽略，因为有 front matter）
> - MD060: 表格管道符风格不一致（分隔行应写 `| --- | --- |` 而非 `|---|---|`）

---

## 开发环境信息

### 容器工具

- 本地使用 **nerdctl** 而非 docker 或 podman
- 需要使用 **sudo** 权限执行
- 构建镜像时使用：`sudo nerdctl build`
- 运行容器时使用：`sudo nerdctl run`

### Hugo 博客信息

- 静态站点生成器：Hugo
- 当前主题：PaperMod
- Hugo 版本：Extended 版本（具体版本见 `Containerfile` 中的 `HUGO_VERSION`）
- 内容目录：`content/post/`
- 主题目录：`themes/PaperMod/`

### 升级 Hugo 版本

升级 Hugo 版本时，**必须同时修改以下两个文件**，否则本地构建与 CI 部署版本不一致：

1. `Containerfile` — `ENV HUGO_VERSION=x.x.x`（本地容器构建用）
2. `.github/workflows/deploy.yml` — `hugo-version: 'x.x.x'`（GitHub Actions 生产部署用）
