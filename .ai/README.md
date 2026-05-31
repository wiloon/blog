# 博客 AI 文档

本目录 **不会** 被 Hugo 发布（位于 `content/` 之外，不参与站点构建）。

## 文档索引

| 文件 | 用途 |
| ---- | ---- |
| [article-sdd.md](article-sdd.md) | **文章 SDD**：Spec 驱动写作流程、AI 约束、Spec 是否上线 |
| [delivery-style.md](delivery-style.md) | **仅 SDD 交付物**：共通 prose 文风（加粗、人称适度用「我」、语气）；无 Spec 的文章不适用 |
| [content-constraints.md](content-constraints.md) | **全站内容约束**：VPN 相关表述（WireGuard/OpenVPN 除外不写软件名）等 |
| [internal-links.md](internal-links.md) | **全站内链**：相对 `.md` + Hugo embedded hook |
| [specs/](specs/) | 各篇文章 Spec（**作者维护**；AI 按 Spec 润色/输出交付物） |

## 文章 Spec 一览

| Spec | 交付物 |
| ---- | ------ |
| [specs/exploration.md](specs/exploration.md) | [content/post/development/exploration.md](../content/post/development/exploration.md) |
| [specs/booster-recovery.md](specs/booster-recovery.md) | [content/post/starship/booster-recovery.md](../content/post/starship/booster-recovery.md) |
| [specs/java-knowledge-map.md](specs/java-knowledge-map.md) | [java-knowledge-map.md](../content/post/language/java/java-knowledge-map.md) + **全站**内链迁移（`scripts/migrate-internal-links.py --scope all`） |

## 工作流（SDD）

1. **你** 在 `.ai/specs/{slug}.md` 写需求与验收。
2. **AI** 阅读 Spec + [AGENTS.md](../AGENTS.md)，更新 `content/post/.../{slug}.md`。
3. 用 Spec 里的验收清单自查；Spec **不** 出现在最终 blog 页面。

详见 [article-sdd.md](article-sdd.md)。新建 Spec 可复制 [specs/_template.md](specs/_template.md)。

**SDD 交付物标签：** `original` + `AI-assisted`（不用 `remix`）。
