---
title: "LaTeX: 标记语言与排版系统简介"
author: "-"
date: 2026-06-22T14:04:37+08:00
lastmod: 2026-06-22T14:04:37+08:00
url: latex
categories:
  - development
tags:
  - latex
  - tex
  - texlive
  - typography
  - remix
  - AI-assisted
---

LaTeX 是一套基于 TeX 的**文档排版系统**：用纯文本写 `.tex` 源文件，交给编译器生成 PDF。学术论文、书籍、简历等需要稳定版式的场景里很常见。若你用 [Pandoc](./pandoc.md) 把 Markdown 转成 PDF，中间产物通常就是 LaTeX，再由 [XeLaTeX](./xelatex.md) 等引擎编译。

## TeX 与 LaTeX

| 名称 | 是什么 |
| --- | --- |
| **TeX** | Donald Knuth 在 1970 年代设计的底层排版程序与语言 |
| **LaTeX** | Leslie Lamport 在 1980 年代于 TeX 之上构建的宏集，提供章节、列表、表格、交叉引用等高层命令 |

日常说的「写 LaTeX」「装 TeX Live」，通常指：**用 LaTeX 语法写文档，用 TeX 发行版里的引擎编译**。

## 人物与历史

### 谁创造了什么

LaTeX 与 Linux 常被一起提起（学术写作、Arch 上装 TeX Live 等），但**作者之间没有直接关系**：

| 项目 | 主要作者 | 年代 | 做什么 |
| --- | --- | --- | --- |
| **TeX** | Donald Knuth | 1970 年代起 | 底层排版程序与语言 |
| **LaTeX** | Leslie Lamport | 1984 年起 | 建立在 TeX 上的文档宏集 |
| **Linux** | Linus Torvalds | 1991 年起 | 操作系统内核 |

LaTeX 后来的标准与维护由 [LaTeX Project](https://www.latex-project.org/) 社区延续（如 Frank Mittelbach 等），并非 Knuth 个人在管 LaTeX。生态里还有大量宏包作者（如 `beamer`、`TikZ` 的 Till Tantau）。

### TAOCP 与 TeX：一段「造工具」的故事

Knuth 最广为人知的著作是《计算机程序设计艺术》（*The Art of Computer Programming*, TAOCP）。写第二版时，他觉得当时印刷排版无法满足书中大量数学公式的质量要求，于是搁置写作、花多年造出 **TeX** 和 **METAFONT**（字体设计）。TeX 解决了**书怎么印得准、印得美**。

这段经历和 Linus Torvalds 的故事有相似的叙事结构：

| 对比 | Donald Knuth | Linus Torvalds |
| --- | --- | --- |
| **主项目** | TAOCP | Linux 内核 |
| **卡住的点** | 排版质量达不到要求 | BitKeeper 授权终止，内核协作需要新工具 |
| **造出来的工具** | TeX（及 METAFONT） | Git |
| **工具解决的问题** | 数学与技术文档的排版 | 分布式、大规模的版本管理 |

主项目推不动 → 造基础设施 ——这是计算机史上反复出现的模式。但动机不同：Knuth 为**排版**，Linus 为**协作与版本管理**。时间尺度也不同：TeX 精雕细琢多年；Git 在 2005 年约两周内搭出可用原型，再逐步演进。

若要在 Knuth 的作品里找更接近 Git 的那条线，是 **Literate Programming（文学化编程）** 与 **WEB/CWEB**：写 TeX 这类大程序时，他把源码与说明交织在一起（`tangle` / `weave`），在「怎么组织复杂程序」上更接近版本管理所要面对的问题。

### Knuth 还与什么有关

除 TeX 外，Knuth 的代表作与贡献还包括：

- **TAOCP** — 多卷本算法与程序设计经典
- **METAFONT / Computer Modern** — 与 TeX 配套的字体系统
- **Literate Programming** — 文学化编程范式
- **算法** — 如 KMP 字符串匹配（与 Pratt、Morris 合作）
- **MIX / MMIX** — TAOCP 中使用的假想机器

## 和 Word 有什么不同

LaTeX 是 **WYSIWYM**（What You See Is What You Mean）：你描述结构（章节、强调、表格），编译器决定具体排版，而不是在页面上直接拖拽。

| 对比 | Word 等 | LaTeX |
| --- | --- | --- |
| 编辑方式 | 所见即所得 | 写标记 + 编译看 PDF |
| 版式稳定性 | 手调容易乱 | 同一份源文件，输出可复现 |
| 长文档 / 公式 | 能写，但大文档易痛苦 | 强项（论文、书籍） |
| 学习曲线 | 低 | 较高 |

很多人用 Markdown 写作，只在需要高质量 PDF 时通过 Pandoc 落到 LaTeX，兼顾写作效率与排版质量。

## 一份文档长什么样

最小可编译示例：

```latex
\documentclass{article}

\begin{document}

\section{Introduction}

Hello, \LaTeX.

\end{document}
```

常用结构：

| 部分 | 作用 |
| --- | --- |
| `\documentclass{...}` | 文档类型（`article`、`report`、`book` 等） |
| 导言区（`\begin{document}` 之前） | 引入宏包、设置字体与版式 |
| `\begin{document}` … `\end{document}` | 正文 |
| `\section`、`\subsection` | 章节标题 |
| `\textbf{}`、`\emph{}` | 加粗、强调 |

编译（引擎任选其一，见下文）：

```bash
xelatex hello.tex
```

## 引擎、宏包、发行版

三个层次不要混为一谈：

```text
.tex 源文件
    │
    ▼
引擎（pdfLaTeX / XeLaTeX / LuaLaTeX）  ← 读入 LaTeX，输出 PDF
    │
    ▼
依赖宏包（graphicx、hyperref、xeCJK…）  ← 导言区 \usepackage{...}
    │
    ▼
TeX Live 等发行版                    ← 把引擎、宏包、字体打成一个安装包
```

- **引擎**：怎么把 `.tex` 变成 PDF；中文场景常用 [XeLaTeX](./xelatex.md)
- **宏包**：扩展功能（插图、超链接、中文、表格线型等）
- **TeX Live**：事实标准发行版；Arch 上通过多个 `texlive-*` 包安装

## 常见使用场景

| 场景 | 说明 |
| --- | --- |
| 学术论文 | 期刊模板、公式、参考文献（BibTeX / biblatex） |
| 书籍 / 报告 | `book`、`report` 文档类，章节结构清晰 |
| 幻灯片 | `beamer` 宏包 |
| Markdown → PDF | [Pandoc](./pandoc.md) 生成 LaTeX，再编译；见 [简历导出实践](./markdown-to-pdf-pandoc-xelatex.md) |
| 简历 | 自定义 `resume-header.tex` 控制标题、列表、表格 |

不一定每篇文档都手写 LaTeX；**理解 LaTeX 是什么**，有助于读懂 Pandoc 生成的 `.tex`、排查缺包和字体问题。

## Arch Linux 安装（入门）

不必一次装全 TeX Live。按需从下面开始：

```bash
# Minimal: compile basic English documents
sudo pacman -S --needed texlive-basic texlive-latexrecommended

# PDF with Unicode / system fonts (Chinese, Inter, etc.)
sudo pacman -S --needed texlive-xetex

# Common missing packages
sudo pacman -S --needed texlive-fontsrecommended texlive-latexextra

# Chinese
sudo pacman -S --needed texlive-langcjk texlive-langchinese noto-fonts-cjk
```

完整中文简历流水线用到的包列表，见 [XeLaTeX](./xelatex.md) 与 [简历导出实践](./markdown-to-pdf-pandoc-xelatex.md)。

## 和本系列其他文章的关系

```text
LaTeX（本文）          ← 排版语言与生态
    │
    ├── XeLaTeX        ← 常用编译引擎（Unicode、系统字体）
    │
    └── Pandoc         ← 常把 Markdown 转成 LaTeX
            │
            └── 简历 Markdown → PDF 实践
```

建议阅读顺序：先读本文建立概念 → [XeLaTeX](./xelatex.md) 了解引擎与安装 → [Pandoc](./pandoc.md) 了解如何不必手写整篇 LaTeX → 需要时看 [实践文](./markdown-to-pdf-pandoc-xelatex.md)。

## 延伸阅读

- LaTeX Project：<https://www.latex-project.org/>
- TeX Live：<https://www.tug.org/texlive/>
- 入门文档（英文）：<https://www.latex-project.org/help/documentation/>
