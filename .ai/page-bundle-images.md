# 文章插图：Page Bundle 与 PaperMod 封面

> **适用范围**：`content/post/` 下需要本地图片的文章（SDD 与非 SDD）。  
> 与 [AGENTS.md](../AGENTS.md) 的 front matter / URL 规则并列。

## 背景

- 老文章多用外链图床（imgtu 等），链接易失效；**新文章插图应进 git**。
- Hugo **Page Bundle**：文章与图片同目录，便于维护；`url` 字段不变，线上 permalink 不受影响。
- 主题 **PaperMod** 支持 front matter `cover`，在文章页标题下方显示封面（含 responsive 多尺寸）。

参考实例：[homelab-k8s-node-rebalance](../content/post/cloud/homelab-k8s-node-rebalance/index.md)。

## 目录结构

单篇 `.md` 改为「目录 + `index.md` + 图片」：

```text
content/post/cloud/my-article/
├── index.md           # 原 my-article.md 移入
├── cover.png          # 封面（可选）
└── diagram.png        # 正文插图（可选，可多张）
```

`url: my-article` 保持不变 → 线上仍为 `https://wiloon.com/my-article/`。

## 新建带图文章

1. 直接建 Page Bundle 目录与 `index.md`（不必先写单文件 `.md` 再迁移）。
2. 图片放入同目录，文件名用小写 kebab-case + 扩展名（如 `grafana-cpu.png`）。
3. front matter 照常写 `title`、`url`、`categories`、`tags` 等（见 AGENTS.md）。

## 已有单文件 `.md` 迁移

```bash
mkdir -p content/post/cloud/my-article
mv content/post/cloud/my-article.md content/post/cloud/my-article/index.md
# 再把 png/jpg/webp 放进 my-article/
```

迁移**不算内容修订**：若仅移动文件、未改正文，**不要**改 `date` / `lastmod` / 标签。

## 正文插图

同目录下写相对路径：

```markdown
![Grafana 上 k8s-50 CPU 偏高](grafana-cpu-before.png)
```

可选 title：

```markdown
![说明](diagram.png "悬停标题")
```

## PaperMod 封面

在 `index.md` front matter 增加（封面文件也在 bundle 目录内）：

```yaml
cover:
  image: cover.png
  alt: 封面图 alt 文本
  caption: 图下方说明（可选，支持 Markdown）
```

- `cover.image`：bundle 内文件名，或外链 `https://...`。
- 封面与正文插图可以是同一张，也可以分开（如 `cover.png` + 正文里再插细节图）。
- Hugo Extended 会为 jpg/png 等生成 responsive `srcset`（生产构建 `env = production` 时生效）。

隐藏封面（保留 og:image 等 meta 时可设）：

```yaml
cover:
  image: cover.png
  hiddenInSingle: true
```

## 本地预览

```bash
task preview
# → http://localhost:1313/{url}/
```

需本机 **Hugo Extended**（与 CI / Containerfile 版本一致为佳）。改 `index.md` 或换图后自动热重载。

## YAML 注意

`title` 含英文冒号 `:` 时须加引号，否则 Hugo 解析 front matter 失败：

```yaml
# ❌
title: Homelab K8s: 从 Grafana 到 Descheduler

# ✅
title: "Homelab K8s: 从 Grafana 到 Descheduler"
```

## 不推荐

| 做法 | 原因 |
| ---- | ---- |
| 新文章用外链图床 | 链接失效、无法随 git 版本管理 |
| `static/images/...` 放单篇专属图 | 可行但图片与文章分离，删文易漏删图 |
| 正文写 `/images/...` 绝对路径 | Page Bundle 内用相对路径即可；绝对路径适合全站共用资源 |

全站共用图（logo 等）仍放 `static/`，引用 `/path/from/static`（不含 `static` 前缀）。

## AI 加图时

1. 用户贴图或指定路径 → 复制/保存到 **该文 Page Bundle 目录**。
2. 若当前是单文件 `.md`，先迁移为 bundle（见上），**`url` 不变**。
3. 封面：按用户意图设 `cover`；正文图：用相对路径 `![alt](file.png)`。
4. 加图后建议 `task preview` 或 `hugo --minify` 确认构建通过。
5. 仅加图/改图、未改正文 prose 时，按 AGENTS.md 规则决定是否更新 `lastmod`（同日多次编辑不重复更新）。
