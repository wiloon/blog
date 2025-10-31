# AI Agent 工作指南

## 编辑博客文章注意事项

### 更新文章日期
当更新文章内容时，**必须**同步更新文章顶部 front matter 中的 `date` 字段为当前日期时间。

示例：
```yaml
---
title: 文章标题
author: "-"
date: 2025-10-30T08:30:00+00:00  # 更新为当前时间
url: article-url
categories:
  - 分类
tags:
  - 标签1
  - 标签2
---
```

---

### 添加 AI 辅助标签
当使用 AI 编辑某篇文章后，**必须**检查文章顶部 front matter 中的 `tags` 字段，确保包含以下标签：
- `AI-assisted` - AI 辅助编辑的标识
- `remix` - 表示内容经过重新编辑和改进

示例：
```yaml
---
title: 文章标题
author: "-"
date: 2025-10-31T08:30:00+00:00
url: article-url
categories:
  - 分类
tags:
  - 原有标签
  - remix          # 内容经过编辑改进
  - AI-assisted    # AI 辅助编辑的标识
---
```

### 其他注意事项
- 保持文章格式的一致性
- 使用适当的 Markdown 语法
- 代码块要指定语言类型
- 保持中英文之间的适当空格
