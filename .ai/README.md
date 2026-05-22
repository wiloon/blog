# 博客 AI 文档

本目录 **不会** 被 Hugo 发布（位于 `content/` 之外，不参与站点构建）。

## 文档索引

| 文件 | 用途 |
| ---- | ---- |
| [article-sdd.md](article-sdd.md) | **文章 SDD**：Spec 驱动写作流程、AI 约束、Spec 是否上线 |
| [specs/](specs/) | 各篇文章 Spec（**作者维护**；AI 按 Spec 润色/输出交付物） |

## 文章 Spec 一览

| Spec | 交付物 |
| ---- | ------ |
| [specs/exploration.md](specs/exploration.md) | [content/post/development/exploration.md](../content/post/development/exploration.md) |

## 工作流（SDD）

1. **你** 在 `.ai/specs/{slug}.md` 写需求与验收。
2. **AI** 阅读 Spec + [AGENTS.md](../AGENTS.md)，更新 `content/post/.../{slug}.md`。
3. 用 Spec 里的验收清单自查；Spec **不** 出现在最终 blog 页面。

详见 [article-sdd.md](article-sdd.md)。新建 Spec 可复制 [specs/_template.md](specs/_template.md)。

**SDD 交付物标签：** `original` + `AI-assisted`（不用 `remix`）。
