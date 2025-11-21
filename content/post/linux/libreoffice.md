---
title: LibreOffice 命令行使用
author: "-"
date: 2025-11-21T08:30:00+08:00
url: libreoffice
categories:
  - Linux
tags:
  - LibreOffice
  - AI-assisted
---

## 文档格式转换

### 转换为文本格式

```bash
libreoffice --headless --convert-to txt document.docx
```

参数说明：
- `--headless`: 无界面模式运行
- `--convert-to`: 指定转换的目标格式
- `txt`: 输出为纯文本格式

### 其他常用转换格式

```bash
# 转换为 PDF
libreoffice --headless --convert-to pdf document.docx

# 转换为 HTML
libreoffice --headless --convert-to html document.docx

# 指定输出目录
libreoffice --headless --convert-to txt --outdir /path/to/output document.docx
```
