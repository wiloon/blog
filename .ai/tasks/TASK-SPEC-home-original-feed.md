# Task Spec: 首页只展示原创（original）文章

| 字段 | 值 |
| --- | --- |
| **状态** | Accepted（方案 A，文案候选 A，菜单不变） |
| **目标** | 把博客首页 `/` 的文章列表从「全部文章」改为「只显示带 `original` 标签的文章」，让访客落地首页即看到作者原创内容（周记、career、生活随笔等） |
| **非目标** | 不改 URL 结构（首页仍是 `/`）；不删除/隐藏非原创文章（仍可经标签/分类/搜索访问）；不引入新插件；不动 PaperMod 主题源文件 |
| **触发原因** | 作者开始写周记，`original` 内容持续积累，希望首页突出原创而非转载/整理类内容 |

---

## 1. 概念澄清：`original` 是 tag，不是 category

需求里说的「原创分类」，在本博客的打标体系中实际是 **标签（tag）**，不是 `categories`：

- `categories` 用于主题分类：`AI`、`Linux`、`language`、`cloud` 等
- `tags` 中的 `original` / `remix` / `reprint` 用于标记内容来源（原创 / 整理 / 转载）

证据：

- `config.toml` 菜单「日常记录」已指向 `/tags/original/`
- career 目录下所有周记（`weekly-2026-w23/24/25/26.md` 等）front matter 均含 `tags: [..., original]`
- 全站约 29 篇文章带 `original` 标签

**结论**：本任务的「首页只显示原创」= 首页文章列表按 **tag `original`** 过滤。下文统一以 tag 表述。

---

## 2. 现状

- 主题：PaperMod。**首页没有独立的 `index.html`**，由 `list.html` 在 `.IsHome` 分支渲染。
- 项目已 override 主题：`layouts/list.html`（相对主题仅多了一行 `hiddenInHomeList` 过滤）。
- 当前首页取文章的逻辑（`layouts/list.html` 第 43–46 行）：

  ```go-html-template
  {{- if .IsHome }}
  {{- $pages = where site.RegularPages "Type" "in" site.Params.mainSections }}
  {{- $pages = where $pages "Params.hiddenInHomeList" "!=" "true"  }}
  {{- end }}
  ```

  （即：取 `mainSections`（实际为 `post`）下、未被 `hiddenInHomeList` 排除的全部文章，按 `lastmod` 倒序分页。）

- `config.toml` 未显式配置 `mainSections`，Hugo 默认取文章最多的顶层 section，即 `post`，所以首页当前显示全部文章。
- 首页顶部有一段 `homeInfoParams` 文案：

  ```text
  这里收集整理了一些技术资料(大部分是转载的，经常用到的有整理过)，希望能帮助到有需要的人。
  ```

---

## 3. 方案决策（ADR 式）

### 决策

采用 **方案 A：在 `layouts/list.html` 的首页分支增加 tag 过滤**，过滤的标签名通过 `config.toml` 参数 `homeTag` 配置（默认 `original`），避免硬编码。

### 备选方案与权衡

| 方案 | 做法 | 优点 | 缺点 | 结论 |
| --- | --- | --- | --- | --- |
| **A（推荐）** | override `list.html` 首页分支加 `where ... "Params.tags" "intersect" (slice site.Params.homeTag)` | URL 不变（仍 `/`）；保留 `homeInfoParams`、分页、封面等所有 PaperMod 首页特性；改动集中在已 override 的一个文件；标签名可配置 | 需维护一处主题 override（项目本就已 override 该文件） | ✅ 采用 |
| B | 首页 alias / 重定向到 `/tags/original/` | 改动最小，复用 taxonomy term 页 | 落地页变成 `/tags/original/`，首页与该标签页重复；丢失 `homeInfoParams` 等首页定制；菜单「首页」语义混乱 | ❌ |
| C | 启用 PaperMod `profileMode` | 首页变个人主页卡片 | 改变首页形态，不再是文章流，不符合「直接看到原创文章」诉求 | ❌ |
| D | 用 `mainSections` 限制 | Hugo 原生、零模板改动 | `mainSections` 按 **section（目录）** 过滤，不能按 tag 过滤；原创文章散落在 career/life/log 等多个目录，无法用它实现 | ❌ |

---

## 4. 实现步骤（方案 A）

### 4.1 `config.toml` 增加参数

在 `[params]` 下新增（与现有 `homeInfoParams` 同级）：

```toml
[params]
  # 首页文章流仅展示带该标签的文章；留空或删除则恢复显示全部
  homeTag = "original"
```

### 4.2 修改 `layouts/list.html` 首页分支

在首页过滤逻辑里追加一行 tag 过滤（仅当 `homeTag` 非空时生效，便于随时回退）：

```go-html-template
{{- if .IsHome }}
{{- $pages = where site.RegularPages "Type" "in" site.Params.mainSections }}
{{- $pages = where $pages "Params.hiddenInHomeList" "!=" "true"  }}
{{- with site.Params.homeTag }}
{{- $pages = where $pages "Params.tags" "intersect" (slice .) }}
{{- end }}
{{- end }}
```

说明：

- `intersect` 对「无 tags 字段」的文章天然不匹配，安全。
- `homeTag` 留空 / 删除即恢复「首页显示全部」，回退零成本。
- 排序仍沿用现有 `$pages.ByLastmod.Reverse`，不变。

### 4.3 更新首页文案 `homeInfoParams.Content`

当前文案强调「大部分是转载的」，是因为旧首页展示的就是转载内容；改造后首页主要是周记和日常记录，这句已不适用。新文案需满足两点：

1. 体现首页主体是 **原创**（周记 / 工作复盘 / 日常随笔）；
2. 仍引导读者去顶部导航「收集综合症/转载」查看作者收集整理的技术资料，避免给人「博客没技术内容」的错觉。

候选文案（**作者已选定候选 A**）：

**候选 A（已选定）：**

```toml
  [params.homeInfoParams]
    Title = "Hi, 我是 W10N"
    Content = "这里主要是我的日常记录——周记、工作复盘和一些随笔。另外我也收集整理了一些技术资料，可从顶部导航「收集综合症/转载」「整理过的」查看。"
```

**候选 B（更口语）：**

```toml
  [params.homeInfoParams]
    Title = "Hi, 我是 W10N"
    Content = "首页是我的原创内容，主要是周记和日常记录。如果想找技术资料，我收集整理的那些都放在顶部导航「收集综合症/转载」和「整理过的」里。"
```

### 4.4 菜单

改造后「首页」`/` 与「日常记录」`/tags/original/` 内容高度重叠，但 **作者已决定保持现状**，本任务 **不动菜单**。

---

## 5. 文件变更清单

| 文件 | 操作 |
| --- | --- |
| `config.toml` | 新增 `params.homeTag = "original"`；改写 `homeInfoParams.Content` |
| `layouts/list.html` | 首页分支新增 `homeTag` 的 tag 过滤（约 3 行） |

---

## 6. 验证

```bash
task preview   # 或 hugo server -D
```

- [ ] 首页 `/` 仅列出带 `original` 标签的文章
- [ ] 周记（`weekly-2026-w*`）出现在首页
- [ ] 转载/整理类（仅 `reprint` / `remix`）文章 **不** 出现在首页
- [ ] 首页分页、封面、`homeInfoParams` 文案正常
- [ ] 非原创文章仍可经 `/tags/`、`/categories/`、搜索访问
- [ ] `hugo` 构建无 error（front matter / 模板均正常）

---

## 7. 回退方案

删除或清空 `config.toml` 中的 `params.homeTag`，首页立即恢复显示全部文章；`list.html` 的 `with` 块在 `homeTag` 为空时不执行，无需回滚模板。

---

## 变更记录

| 日期 | 变更 |
| --- | --- |
| 2026-06-30 | 初版 |
