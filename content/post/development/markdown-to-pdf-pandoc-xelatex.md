---
title: "Markdown to PDF: Pandoc + XeLaTeX 简历导出实践"
author: "-"
date: 2026-06-22T13:55:16+08:00
lastmod: 2026-06-22T13:55:16+08:00
url: markdown-to-pdf-pandoc-xelatex
categories:
  - development
tags:
  - pandoc
  - xelatex
  - latex
  - markdown
  - typst
  - quarto
  - arch-linux
  - remix
  - AI-assisted
---

投递职位需要 PDF 版简历，但内容仍希望用 Markdown 维护。这次在 Arch Linux 上搭了一套 **Pandoc + XeLaTeX** 流程，把中英文简历稳定导出为 PDF，并沉淀了脚本和 LaTeX 模板。本文记录选型、依赖安装、流水线，以及排版上踩过的坑。

## 背景

源文件是 Markdown：多级标题、表格、列表、加粗混排。需要：

- 中英文各一份 PDF，字体分别可调
- 改 Markdown 后能一条命令重新导出
- 排版达到简历水准（页眉、列表间距、技能表行间线等）

早期试过 **cmark + Chromium headless**（Markdown → HTML → 打印 PDF），能跑通，但 CSS 调版费时；最终选用 **Pandoc 生成 LaTeX，再用 XeLaTeX 编译 PDF**——排版可控，适合反复迭代。

## 工具链概览

| 组件 | 作用 |
| --- | --- |
| **LaTeX** | 中间排版语言（`.tex`）；详见 [LaTeX 简介](./latex.md) |
| **Pandoc** | Markdown → LaTeX（`--standalone`）；详见 [Pandoc 介绍](./pandoc.md) |
| **XeLaTeX** | 编译 `.tex` 为 PDF；详见 [XeLaTeX 介绍](./xelatex.md) |
| **resume-header.tex** | 自定义页边距、标题层级、列表间距、页眉样式 |
| **inject-table-row-rules.py** | 在 Pandoc 生成的 `longtable` 数据行之间插入 `\midrule` |
| **pandoc-pdf.sh** | 串联上述步骤的一键脚本 |

整体流水线：

```text
Resume.md
  → pandoc（+ resume-header.tex + 字体变量）
  → input.tex
  → inject-table-row-rules.py
  → xelatex × 2
  → Resume.pdf
```

XeLaTeX 跑两遍，是为了稳定生成目录、交叉引用和部分书签（即使简历里用得不多，习惯上保留）。

## Arch Linux 依赖安装

Arch 上 Pandoc 包名是 **`pandoc-cli`**（提供 `pandoc` 命令）。中文 PDF 还需要 CJK 相关 TeX 包和字体；英文简历另装 **Inter**。

```bash
sudo pacman -S --needed \
  pandoc-cli \
  texlive-basic texlive-latexrecommended texlive-xetex \
  texlive-fontsrecommended texlive-langcjk texlive-langchinese texlive-latexextra \
  noto-fonts-cjk inter-font
```

| 包 | 用途 |
| --- | --- |
| `texlive-xetex` | XeLaTeX 引擎 |
| `texlive-fontsrecommended` | 提供 `lmodern.sty` 等（首次英文编译常缺） |
| `texlive-langcjk` / `texlive-langchinese` | 中文 `xeCJK`、`ctex` 宏包 |
| `texlive-latexextra` | `titlesec`（章节标题样式） |
| `noto-fonts-cjk` | 中文简历字体 |
| `inter-font` | 英文简历字体 |

`texlive-*` 合计约 1 GB，只在需要高质量排版的机器上装即可。

## 一键导出

脚本放在个人配置仓库的 `resume/scripts/pandoc-pdf.sh`：

```bash
resume/scripts/pandoc-pdf.sh path/to/Resume_wangyue_cn_J68476.md
resume/scripts/pandoc-pdf.sh path/to/Resume_wangyue_en_J68476.md
```

输出与源文件同目录、同名 `.pdf`。脚本核心逻辑：

1. 按文件名判断中/英，设置不同 `mainfont`
2. `pandoc` 生成 `input.tex`（A4、自定义页边距、`--include-in-header` 引入模板）
3. Python 脚本给技能表等 `longtable` 行间加 `\midrule`
4. `xelatex` 编译两次

Pandoc 侧关键参数示例：

```bash
pandoc resume.md \
  --standalone \
  --pdf-engine=xelatex \
  --include-in-header=resume-header.tex \
  -V papersize=a4 \
  -V geometry:top=1.5cm \
  -V geometry:bottom=1.5cm \
  -V geometry:left=1.8cm \
  -V geometry:right=1.8cm \
  -V linestretch=1.35 \
  -V mainfont="Noto Sans CJK SC" \
  -V CJKmainfont="Noto Sans CJK SC"
```

英文简历把 `mainfont` 换成 `Inter` 即可，不必设 `CJKmainfont`。

## 字体策略

| 版本 | 字体 | 说明 |
| --- | --- | --- |
| 中文 | Noto Sans CJK SC | `mainfont` + `CJKmainfont` 均指向同一字体，避免中英文混排风格不一致 |
| 英文 | Inter | 无衬线，偏现代简历风格 |

正文里**避免** Markdown 反引号行内代码（如 `` `kubectl` ``）。Pandoc 会输出 `\texttt{}`，切换到等宽字体，与正文 sans-serif 不协调。技术名词用普通文字或加粗即可。

## LaTeX 模板做了什么

`resume-header.tex` 用 `titlesec` 控制标题层级，用 `enumitem` 拉开列表间距。要点：

- 姓名（`#` → `\section`）：左对齐 24pt
- 联系信息：通过 `\resumecontactline{...}` 渲染为 10pt 灰色单行
- `##` 章节：仅加粗，**不加**下划线（避免和表格顶线叠成双线）
- 正文 10.5pt（`scrextend`），行距 1.35

页眉示例（Markdown 内嵌 LaTeX，配合 `raw_tex`）：

```latex
\resumecontactline{大连 · +86 ... · \href{mailto:you@example.com}{you@example.com} · \href{https://example.com}{example.com}}
```

`\href` 需要 `hyperref`（Pandoc 转 PDF 时会自动加载），链接在 PDF 里可点击。

## Markdown 排版约定

与 Pandoc 默认行为打交道时，总结了几条约定：

| 问题 | 处理 |
| --- | --- |
| `---` 分隔线 | **不要用**。Pandoc 会生成居中半宽横线，简历里很突兀 |
| 「个人信息」章节 | 欧美简历风格：姓名 + 一行联系信息即可，不设 `## 个人信息` |
| 分组小标题 | 工作经历内用 `#####`，比加粗段落层次更清晰 |
| 过长 bullet | 拆成主条 + 子列表，避免「文字墙」 |
| 技能表行间线 | Pandoc `booktabs` 默认只有顶/底线；用 Python 后处理插入行间 `\midrule` |

中文简历联系行写「大连」；英文写 `Dalian, China`。

## Typst 与 Quarto

选型时除了 HTML 打印路线，也看过 **Typst** 和 **Quarto**。二者定位不同：Quarto 是 Pandoc 之上的「出版框架」；Typst 是另一套排版引擎，可减轻 TeX Live 负担。当前主流程仍是 **Pandoc + XeLaTeX**，下表是与本文场景的对比。

### 三者关系（先分清层次）

```text
                    Markdown / 类 Markdown 源稿
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   Pandoc + XeLaTeX        Quarto              Typst
   （本文主流程）      （底层仍常走 Pandoc      （独立引擎；
                        + LaTeX 出 PDF）         也可经 Pandoc 接入）
          │                   │                   │
          ▼                   ▼                   ▼
        LaTeX              LaTeX / HTML         .typ → PDF
          │              等多格式                 （通常不经 LaTeX）
          ▼
        PDF
```

### 对比表

| 维度 | Pandoc + XeLaTeX（当前） | Quarto | Typst |
| --- | --- | --- | --- |
| **是什么** | 通用转换器 + LaTeX 引擎 | 基于 Pandoc 的「可重复出版」工具 | 新一代标记排版语言 + 编译器 |
| **源文件** | `.md` | `.qmd`（Markdown + YAML 元数据） | `.typ`，或 Pandoc 从 `.md` 转 `.typ` |
| **出 PDF 的路径** | md → tex → xelatex | 多数情况仍是 md → tex → xelatex | md → typ → typst compile，或直接写 `.typ` |
| **依赖体积** | 大（`texlive-*` 约 1 GB） | 在 Pandoc/TeX 之上再加 Quarto CLI | 小（`typst` 单包，Arch 上远小于 TeX Live） |
| **编译速度** | 慢（xelatex × 2） | 与底层引擎相同 | 快 |
| **排版控制力** | 很强（`resume-header.tex` 等） | 与 Pandoc+LaTeX 同级（共用引擎） | 强，语法比 LaTeX 简洁 |
| **中文 / 系统字体** | 成熟（XeLaTeX + `fontspec` / `xeCJK`） | 同左 | 支持良好，需按 Typst 方式配置字体 |
| **简历场景匹配度** | 已验证（脚本 + 模板已落地） | 功能偏多，简历只用 PDF 时收益有限 | 有潜力，需重写版式模板 |
| **迁移成本** | — | 低：把现有 md 包进 `.qmd`，PDF 参数基本可复用 | 中高：`resume-header.tex` 要改写成 Typst 模板或 `#set` 规则 |
| **多格式同源** | 需另配 Pandoc 参数 | 强项（PDF / HTML / 幻灯片等一条命令） | 以 PDF 为主，其它格式非重点 |

### Quarto：换壳不换芯

[Quarto](https://quarto.org/) 底层依赖 [Pandoc](./pandoc.md)。出 PDF 时通常仍指定 `--pdf-engine=xelatex`，仍要装 TeX Live，仍会遇到本文里的 LaTeX 模板、表格后处理等问题——**不是绕开 LaTeX，而是把配置收进 YAML 和项目结构**。

适合 Quarto 的情况：

- 同一份稿要稳定产出 **PDF + 网站 + 幻灯片**（技术博客、论文、讲义）
- 需要 **交叉引用、代码块执行、文献管理** 等「出版级」能力
- 团队已统一 Quarto 工作流

对**只做投递简历 PDF** 而言，Quarto 多一层 CLI 和 `.qmd` 约定，**不会比现有 `pandoc-pdf.sh` 更简单**，也**不会更轻**。若未来简历仓库还要附带「在线版 HTML 简历」或演讲稿，再评估 Quarto 更合适。

示意（本质与 Pandoc 命令等价）：

```bash
quarto render resume.qmd --to pdf
# 内部：解析 .qmd → 调用 pandoc → xelatex
```

### Typst：换引擎，可能更轻

[Typst](https://typst.app/) 是独立的排版系统，编译器直接出 PDF，**不依赖 TeX Live**。Arch 安装：

```bash
sudo pacman -S typst
```

与 Markdown 简历的衔接方式：

1. **Pandoc 中转**：`pandoc resume.md -o resume.typ -t typst`，再 `typst compile resume.typ`
2. **直接写 `.typ`**：版式用 Typst 原生语法（`#set page(...)`、`#text(size: 24pt)[姓名]` 等）

相对当前方案的优势：

- 安装与编译都更轻、更快
- 表格、标题、间距用 Typst 语法表达，往往比 LaTeX 宏包组合更直观
- 不必维护 `inject-table-row-rules.py` 这类 LaTeX 补丁（若版式在 Typst 模板里一次定义好）

代价与风险：

- 现有 `resume-header.tex` **不能复用**，要迁移为 Typst 模板或 Pandoc 的 typst 模板
- Pandoc 的 Typst 后端与 LaTeX 后端成熟度、默认模板质量仍在演进，复杂简历需更多自测
- 生态（简历范例、企业模板）不如 LaTeX 丰富

若主要痛点是 **TeX Live 体积和编译慢**，Typst 值得做一个小型 PoC；若当前 PDF 已满意，**没有迫切理由立刻迁移**。

### 怎么选（简历场景）

| 你的目标 | 建议 |
| --- | --- |
| PDF 版式已达标，继续迭代内容 | **维持 Pandoc + XeLaTeX** |
| 想少装依赖、加快编译 | 试 **Typst** PoC，对比同一份简历的版式与维护成本 |
| 同时要 PDF、HTML 简历页、幻灯片 | 评估 **Quarto** |
| 偶尔导一次、不想装 TeX | 保留 HTML 打印或编辑器插件作兜底（见下节） |

## 本次讨论结论与后续计划

围绕「简历场景下是否考虑 Typst」补充几个结论，避免后续重复调研：

### 结论速记

| 问题 | 结论（简历场景） |
| --- | --- |
| Typst 是否开源免费 | **是**。Typst 编译器（CLI）是 Apache-2.0 开源软件，可免费商用；Web 编辑器有免费档和付费档，但本地编译不依赖它 |
| Typst 是否有替代 XeLaTeX 潜力 | **有**。在简历、报告、程序化 PDF 生成场景潜力明显；但在学术投稿模板与超大 LaTeX 生态方面，短期难全面替代 |
| Typst 是否流行、社区是否活跃 | **增长快且活跃**。开源后持续迭代，社区包和编辑器生态在增长；相对 LaTeX 仍是新生态，成熟度与覆盖面仍在追赶 |

### 为什么暂不切换主流程

- 当前 `Pandoc + XeLaTeX` 已满足投递质量，且中英文版式已稳定
- 现有 `resume-header.tex`、表格后处理脚本可复用，迁移成本已摊薄
- 若立即切换 Typst，需要重写模板并重新做一轮版式回归

### 下次可执行的 Typst PoC（记录）

目标：在不影响当前投递流程的前提下，评估 Typst 是否值得作为后续候选方案。

1. 环境：安装 `typst`，保留现有 TeX 流程不动
2. 输入：使用同一份中文简历 `Resume_wangyue_cn_J68476.md`
3. 路线 A：`pandoc -t typst` 生成 `.typ`，再 `typst compile`
4. 路线 B：手写最小 Typst 模板（姓名、联系行、技能表）验证版式控制
5. 对比项：编译耗时、依赖体积、字体效果、表格可控性、模板维护复杂度
6. 验收：若版式达到当前 PDF 水平且维护成本更低，再评估是否引入并行脚本（如 `typst-pdf.sh`）

## 其它备选方案（未纳入主流程）

| 方案 | 特点 |
| --- | --- |
| cmark + Chromium | 无 TeX，轻量；CSS 调版成本高 |
| npx md-to-pdf | 一行命令；依赖下载慢，离线不便 |
| VS Code 插件 Markdown PDF | 适合偶尔手工导出，难脚本化 |

## 小结

对**结构复杂、需要精细排版**的 Markdown（简历、说明文档），**Pandoc + XeLaTeX + 自定义 `.tex` 头文件** 比 HTML 打印路线更可控。成本是 TeX 依赖体积和一点 LaTeX 学习曲线；收益是字体、间距、表格、分页都能稳定复现。

**Quarto** 并未替代 LaTeX，适合多格式出版，对「只出简历 PDF」偏重。**Typst** 是更轻的潜在替代引擎，值得在 TeX 体积成为瓶颈时再试，但需重写版式层。

更完整的 Spec、脚本与模板见个人配置仓库中的 `resume/TASK-SPEC-markdown-to-pdf.md`（与本文同步维护）。
