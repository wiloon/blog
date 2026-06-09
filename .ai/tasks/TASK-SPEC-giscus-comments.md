# Task Spec: 集成 Giscus 评论系统

| 字段 | 值 |
| --- | --- |
| **状态** | Draft |
| **目标** | 在 Hugo + PaperMod 博客上启用 Giscus 评论功能，数据存储在 GitHub Discussions |
| **非目标** | 不引入第三方评论平台（Disqus、Waline 等）；不修改 PaperMod 主题文件本身 |
| **触发原因** | 博客目前无评论功能，希望让读者能直接在文章下反馈 |

---

## 1. 现状

- Hugo 博客地址：`https://wiloon.com`
- GitHub 仓库：`wiloon/blog`
- 主题：PaperMod（已内置 comments 机制）
- `config.toml` 中 `comments = false`（已存在，只需改 true）
- `themes/PaperMod/layouts/single.html` 已有判断：

  ```html
  {{- if (.Param "comments") }}
  {{- partial "comments.html" . }}
  {{- end }}
  ```

- `themes/PaperMod/layouts/_partials/comments.html` 为空占位文件
- `layouts/_partials/` 目录已存在（用于 override 主题）
- `infra/github/opentofu/blog/` workspace 已创建（`w10n-config` 仓库），管理 `wiloon/blog` 仓库设置，含 `has_discussions = true`；`tofu output node_id` 可直接输出 `data-repo-id`

---

## 2. Giscus 工作原理

Giscus 把每篇文章的评论映射到 GitHub Discussions 中的一个 Discussion，匹配规则可选：

| 映射方式 | 说明 |
| --- | --- |
| `pathname`（推荐） | 按页面 URL 路径匹配，最通用 |
| `title` | 按文章标题匹配 |
| `og:title` | 按 Open Graph 标题匹配 |

评论数据完全在 GitHub，无需额外数据库。

---

## 3. 前置条件

### 3.1 OpenTofu（自动化）

在 `w10n-config` 仓库的 `infra/github/opentofu/blog/` 目录下执行：

```bash
cp terraform.tfvars.example terraform.tfvars
# 填入 github_token

tofu init
tofu import github_repository.blog blog   # blog 仓库已存在，先 import
tofu apply
tofu output node_id                        # 输出 data-repo-id（形如 R_kgDO...）
```

`tofu apply` 会确保 `has_discussions = true` 生效（即 §3.2 步骤被自动化）。

### 3.2 手动步骤（浏览器）

| 步骤 | 操作 |
| --- | --- |
| 3.2.1 | 访问 [github.com/apps/giscus](https://github.com/apps/giscus) → Install → 选择 `wiloon/blog`（GitHub App，无法用 OpenTofu 安装） |
| 3.2.2 | 访问 [giscus.app](https://giscus.app)，填写：<br>- Repository: `wiloon/blog`<br>- Page ↔ Discussion 映射：`pathname`<br>- Discussion 分类：`Announcements`（只有维护者能在 GitHub 网页直接新建 Discussion；Giscus App 会在首次评论时自动建；普通用户只能在 Giscus 框里留言，无法绕过博客直接发帖）<br>- 主题：`preferred_color_scheme`（跟随系统深色/浅色）<br>从页面底部生成的 `<script>` 标签中找到 `data-category-id`（形如 `DIC_kwDO...`），`data-repo-id` 已由 `tofu output node_id` 获得，无需从此处复制 |

---

## 4. 实现步骤（AI 执行）

### 4.1 创建 comments.html override

创建 `layouts/_partials/comments.html`，内容为 Giscus `<script>` 标签：

```html
<div class="comments">
  <script src="https://giscus.app/client.js"
    data-repo="wiloon/blog"
    data-repo-id="REPO_ID_PLACEHOLDER"
    data-category="Announcements"
    data-category-id="CATEGORY_ID_PLACEHOLDER"
    data-mapping="pathname"
    data-strict="1"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="bottom"
    data-theme="preferred_color_scheme"
    data-lang="zh-CN"
    crossorigin="anonymous"
    async>
  </script>
</div>
```

**配置说明：**

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `data-strict` | `1` | 严格匹配 pathname，URL 不变则评论不丢失 |
| `data-input-position` | `bottom` | 输入框在评论列表下方 |
| `data-lang` | `zh-CN` | 界面语言中文 |

**注意：**
- `data-repo-id`：从 `tofu output node_id` 获取（§3.1）
- `data-category-id`：从 giscus.app 生成的 script 中获取（§3.2.2）

### 4.2 修改 config.toml

将 `comments = false` 改为 `comments = true`（全局开启，所有文章默认显示评论区；如需对个别文章关闭，可在该文章 front matter 添加 `comments: false`）。

### 4.3 验证

```bash
hugo server -D
```

访问任意文章页，确认评论区出现在正文下方。

---

## 5. 文件变更清单

**`blog` 仓库：**

| 文件 | 操作 |
| --- | --- |
| `layouts/_partials/comments.html` | 新建 |
| `config.toml` | 修改 `comments = false` → `true` |

**`w10n-config` 仓库：**

| 文件 | 操作 |
| --- | --- |
| `infra/github/opentofu/blog/providers.tf` | 新建（已完成） |
| `infra/github/opentofu/blog/main.tf` | 新建（已完成） |
| `infra/github/opentofu/blog/variables.tf` | 新建（已完成） |
| `infra/github/opentofu/blog/outputs.tf` | 新建（已完成） |
| `infra/github/opentofu/blog/terraform.tfvars.example` | 新建（已完成） |
| `infra/github/opentofu/blog/README.md` | 新建（已完成） |

---

## 6. 回退方案

如需全局关闭评论，只需将 `config.toml` 中 `comments = true` 改回 `false`，无需删除 `layouts/_partials/comments.html`。评论数据仍保留在 GitHub Discussions，不会丢失。

---

## 7. 验收清单

- [ ] `tofu import` + `tofu apply` 完成，`has_discussions = true` 已生效
- [ ] `tofu output node_id` 输出的 `data-repo-id` 已填入 `comments.html`
- [ ] Giscus App 已安装到 `wiloon/blog`
- [ ] `data-category-id`（`DIC_kwDO...` 格式）已从 giscus.app 获取并填入 `comments.html`
- [ ] 本地 `hugo server` 能看到评论区
- [ ] 深色/浅色主题切换时评论区随之变化
- [ ] 发布后线上文章评论区正常加载

---

## 变更记录

| 日期 | 变更 |
| --- | --- |
| 2026-06-09 | 初版 |
