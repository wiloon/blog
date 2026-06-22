---
title: "Pandoc: 通用文档格式转换工具"
author: "-"
date: 2026-06-22T14:01:54+08:00
lastmod: 2026-06-22T14:01:54+08:00
url: pandoc
categories:
  - development
tags:
  - pandoc
  - markdown
  - document-conversion
  - remix
  - AI-assisted
---

[Pandoc](https://pandoc.org/) 是一个命令行文档转换器，号称能把一种标记格式转成几十种另一种格式。写 Markdown 的人最常拿它做两件事：导出 Word / HTML，以及配合 LaTeX 引擎生成 PDF。

## 它解决什么问题

很多内容用 Markdown（或 reStructuredText、Org-mode 等）写更舒服，但投递、打印、协作方往往要 PDF 或 DOCX。Pandoc 在**不改动写作习惯**的前提下，充当「格式编译器」：

```text
Markdown / HTML / docx / ...
        │
        ▼
     Pandoc
        │
        ▼
PDF / HTML / docx / LaTeX / ...
```

同一份源文件，可以按需输出多种交付物。

## 支持哪些格式

Pandoc 3.x 支持大量输入、输出格式。日常最常用的一组：

| 方向 | 格式 |
| --- | --- |
| 读入 | Markdown、HTML、docx、LaTeX、EPUB、JSON 等 |
| 写出 | HTML、PDF、docx、LaTeX、EPUB、纯文本等 |

查看本机完整列表：

```bash
pandoc --list-input-formats
pandoc --list-output-formats
```

## 基本用法

最简单的转换——Markdown 转 HTML：

```bash
pandoc input.md -o output.html
```

Markdown 转 PDF（需要 LaTeX 引擎，见 [XeLaTeX 介绍](./xelatex.md)）：

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

常用参数：

| 参数 | 含义 |
| --- | --- |
| `-f` / `-t` | 指定输入 / 输出格式（通常可省略，由扩展名推断） |
| `-o` | 输出文件 |
| `--standalone` | 生成完整文档（如带 `<html>` 骨架的 HTML，或完整 LaTeX 前言） |
| `--pdf-engine` | PDF 输出时指定引擎（`xelatex`、`pdflatex`、`lualatex` 等） |
| `-V key=val` | 向 LaTeX 模板传入变量（页边距、字体、字号等） |
| `--include-in-header` | 注入自定义 LaTeX / HTML 片段 |
| `-M` | 设置元数据（title、author 等） |

带变量的 PDF 示例：

```bash
pandoc resume.md -o resume.pdf \
  --standalone \
  --pdf-engine=xelatex \
  -V papersize=a4 \
  -V geometry:margin=2cm \
  -V mainfont="Noto Sans CJK SC" \
  -V CJKmainfont="Noto Sans CJK SC"
```

## Pandoc 如何生成 PDF

Pandoc **本身不排版 PDF**。流程是：

1. 把 Markdown 转成 [LaTeX](./latex.md)（`.tex`）
2. 调用外部引擎（如 XeLaTeX）编译为 PDF

因此 PDF 质量取决于：**Pandoc 的 LaTeX 模板** + **你注入的 `.tex` 头文件** + **所选引擎与字体**。这也是简历等精细排版场景会维护 `resume-header.tex` 一类文件的原因。

若只想看中间产物：

```bash
pandoc input.md -o output.tex --standalone
```

## Arch Linux 安装

Arch 官方仓库包名是 **`pandoc-cli`**（提供 `pandoc` 命令）：

```bash
sudo pacman -S pandoc-cli
```

macOS 可用 Homebrew：

```bash
brew install pandoc
```

仅装 Pandoc 不足以出 PDF，还需 TeX 发行版（如 `texlive-*`），详见 [LaTeX](./latex.md) 与 [XeLaTeX](./xelatex.md)。

## 与其他方案对比

| 方案 | 特点 |
| --- | --- |
| **Pandoc + LaTeX** | 排版质量高，适合 PDF；依赖重 |
| cmark / 浏览器打印 | 轻量，CSS 控制样式 |
| npx md-to-pdf | Node 生态，一行命令 |
| 编辑器插件 | 手工导出，难脚本化 |

## 实践案例

我用 Pandoc + XeLaTeX 把 Markdown 简历导出为 PDF，包括自定义 LaTeX 模板、中英文字体、表格行间线等，过程记录在 [Markdown to PDF: Pandoc + XeLaTeX 简历导出实践](./markdown-to-pdf-pandoc-xelatex.md)。

## 延伸阅读

- 官网：<https://pandoc.org/>
- 用户手册：<https://pandoc.org/MANUAL.html>
- [LaTeX: 标记语言与排版系统简介](./latex.md)
- LaTeX 引擎选择：[XeLaTeX: Unicode 友好的 LaTeX 引擎](./xelatex.md)
