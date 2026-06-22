---
title: "XeLaTeX: Unicode 友好的 LaTeX 引擎"
author: "-"
date: 2026-06-22T14:01:54+08:00
lastmod: 2026-06-22T14:01:54+08:00
url: xelatex
categories:
  - development
tags:
  - xelatex
  - latex
  - texlive
  - typography
  - remix
  - AI-assisted
---

XeLaTeX 是 TeX Live 发行版中的一种 **LaTeX 编译引擎**，与 pdfLaTeX、LuaLaTeX 并列。处理**中文、英文混排**或需要调用系统 OpenType 字体时，XeLaTeX 是最常用的选择之一。若还不熟悉 [LaTeX](./latex.md) 本身，建议先读该文建立概念，再回来看引擎差异。

## LaTeX 与引擎是什么关系

可以先这样理解：

| 概念 | 角色 |
| --- | --- |
| **[LaTeX](./latex.md)** | 排版语言与宏集；你写 `.tex` 源文件 |
| **引擎**（pdfLaTeX、XeLaTeX、LuaLaTeX） | 读取 `.tex`，输出 PDF |
| **TeX Live** | 引擎 + 海量宏包 + 字体的发行版 |

```text
document.tex  →  xelatex  →  document.pdf
```

[Pandoc](./pandoc.md) 生成 PDF 时，也是先写出 `.tex`，再调用你指定的 `--pdf-engine`（如 `xelatex`）完成最后一步。

## 为什么需要 XeLaTeX

### pdfLaTeX 的局限

传统的 **pdfLaTeX** 历史悠久，但：

- 字体接入方式偏旧（多为 T1 编码、内置字体）
- 中文等非拉丁文字支持麻烦，常要额外宏包和配置
- 直接调用系统里的 Noto、Inter 等 OpenType 字体不直观

### XeLaTeX 的优势

XeLaTeX 原生支持 **Unicode**，并通过 **`fontspec`** 宏包直接加载系统字体：

```latex
\usepackage{fontspec}
\setmainfont{Inter}
\setCJKmainfont{Noto Sans CJK SC}  % via xeCJK
```

因此适合：

- 中文 / 日文 / 韩文文档
- 中英文混排简历、论文、说明材料
- 指定 Inter、思源黑体等品牌字体

### 与 LuaLaTeX 的简要对比

| 引擎 | 特点 |
| --- | --- |
| **pdfLaTeX** | 默认、生态最大；西文为主 |
| **XeLaTeX** | Unicode + `fontspec`；中文场景成熟 |
| **LuaLaTeX** | 同样现代；部分复杂排版用 Lua 扩展更方便 |

简历、一般技术文档用 XeLaTeX 足够；三者很多宏包通用，但字体配置方式不同，**不要混用同一套字体配置**。

## 基本使用

### 最小示例

`hello.tex`：

```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Inter}
\begin{document}
Hello, XeLaTeX.
\end{document}
```

编译：

```bash
xelatex hello.tex
```

生成 `hello.pdf`。部分文档需要编译两次以稳定交叉引用，Pandoc 流水线里通常会 `xelatex` 跑两遍。

### 中文示例

```latex
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK SC}
\begin{document}
中文与 English 混排。
\end{document}
```

Pandoc 转中文 PDF 时，常用 `-V CJKmainfont="Noto Sans CJK SC"`，底层即由 `xeCJK` 等宏包处理。

## Arch Linux 安装

XeLaTeX 来自 TeX Live，不是单独一个小包。最小可用集合：

```bash
sudo pacman -S --needed \
  texlive-basic \
  texlive-latexrecommended \
  texlive-xetex
```

中文 PDF 通常还需要：

```bash
sudo pacman -S --needed \
  texlive-fontsrecommended \
  texlive-langcjk \
  texlive-langchinese \
  noto-fonts-cjk
```

自定义章节标题样式（如 `titlesec`）在 `texlive-latexextra` 里：

```bash
sudo pacman -S texlive-latexextra
```

完整体积约 **1 GB 量级**，按需安装即可。

## 常见报错与对应包

| 报错 / 缺失文件 | 常见解决 |
| --- | --- |
| `lmodern.sty` not found | `texlive-fontsrecommended` |
| `xeCJK.sty` not found | `texlive-langcjk` |
| `ctexhook.sty` not found | `texlive-langchinese` |
| `titlesec.sty` not found | `texlive-latexextra` |
| 字体找不到 | 安装 `noto-fonts-cjk`、`inter-font` 等，确认 `fc-list` 可见 |

## 与 Pandoc 配合

典型命令：

```bash
pandoc input.md -o output.pdf \
  --standalone \
  --pdf-engine=xelatex \
  -V mainfont="Inter" \
  -V CJKmainfont="Noto Sans CJK SC"
```

Pandoc 负责：Markdown → 结构化 LaTeX + 默认模板。  
XeLaTeX 负责：字体渲染、分页、生成 PDF。

更完整的简历导出流水线（含自定义 `resume-header.tex`、表格后处理）见 [Markdown to PDF: Pandoc + XeLaTeX 简历导出实践](./markdown-to-pdf-pandoc-xelatex.md)。

## 小结

- **pdfLaTeX**：西文传统路线，简单文档够用
- **XeLaTeX**：Unicode 与系统字体友好，**中文 PDF 首选**
- 与 [Pandoc](./pandoc.md) 组合时，记住：Pandoc 写 `.tex`，XeLaTeX 出 `.pdf`

## 延伸阅读

- [LaTeX: 标记语言与排版系统简介](./latex.md)
- TeX Live：<https://www.tug.org/texlive/>
- `fontspec` 文档：随 `texlive-xetex` 安装
- Pandoc 手册 PDF 章节：<https://pandoc.org/MANUAL.html#creating-a-pdf>
