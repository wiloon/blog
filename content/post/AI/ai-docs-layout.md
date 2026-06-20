---
title: 项目里的 AI 文档怎么放
author: "-"
date: 2026-06-20T17:27:28+08:00
lastmod: 2026-06-20T17:27:28+08:00
url: ai-docs-layout
categories:
  - AI
tags:
  - AI
  - cursor
  - copilot
  - remix
  - AI-assisted
---

## 背景

给 AI 编程助手写「项目级说明」，目前尚无统一行业标准——没有 RFC，也没有各家都认的固定文件名。2024 到 2026 年间的常见做法是：在仓库里放 markdown，让 agent 改代码前先读约束。

真正稳定的实践，往往不在某个目录名上，而在三件事：

1. 入口清晰 — agent 知道先读哪个文件
2. 约束可执行 — 语言、目录、测试命令等，少写空泛原则
3. 规模匹配 — 小 demo 不必拆十几份 doc

## 常见组织方式

| 方式 | 典型路径 | 优点 | 缺点 |
| ---- | -------- | ---- | ---- |
| 根目录入口 | `AGENTS.md`、`CLAUDE.md` | 易发现，多工具能扫到 | 规则一多文件会很长 |
| `.ai/` 目录 | `.ai/instructions.md` | 可拆分，根目录干净 | 部分工具不会自动索引子目录 |
| Cursor 专用 | `.cursor/rules/*.mdc` | 与 Cursor IDE 深度集成 | 绑定 Cursor，换工具需迁移 |
| Copilot 专用 | `.github/copilot-instructions.md` | VS Code / Copilot 原生支持 | 绑定 GitHub Copilot 生态 |
| 与人类文档合并 | `CONTRIBUTING.md` 内 AI 段 | 贡献指南一处维护 | AI 规则与人工流程易混杂 |

没有「唯一正确」的目录名。`.ai/` 是合理选项之一，不是法定标准。

## Cursor 与 Copilot 并用时的折中

我同时用 Cursor 和 Copilot。若只采用 Cursor 专用规范（如 `.cursor/rules/`），Copilot 侧未必读到；反之亦然。

因此我倾向于 vendor-neutral（与工具无关）的结构：

```text
repo-root/
├── AGENTS.md              # 入口：简短，指向细则
├── README.md              # 给人看
└── .ai/
    ├── README.md          # （可选）本目录索引
    └── instructions.md    # 详细约束：语言、结构、命令
```

- Cursor 可读 `AGENTS.md` 与 workspace rules
- Copilot 侧，repo 内 markdown 可进入 agent 上下文
- 换编辑器或换工具时，规则留在 git，跟着项目走

`.ai/` 目录在这里是一种可用的折中：不绑定单一 IDE，又比把所有规则塞进一个 `AGENTS.md` 更易维护。

### Copilot 桥接（可选）

若 Copilot 未稳定加载 `.ai/`，可在 `.github/copilot-instructions.md` 写一行指向细则，避免维护两套重复内容：

```markdown
Follow project AI instructions in `.ai/instructions.md`. Entry point: `AGENTS.md`.
```

## 按项目规模取舍

| 项目规模 | 建议 |
| -------- | ---- |
| 小 demo | `AGENTS.md` + `.ai/instructions.md` 足够 |
| 中等应用 | 加 `.ai/contributions.md`、workflow 文档 |
| 内容型 repo（如 blog） | `.ai/` 承载领域工作流，`AGENTS.md` 承载通用编辑规则 |

规则变多时再拆文件；始终只有几条约束时，合并成单个 `AGENTS.md` 也完全可以。

## 我各仓库里的实例

| 仓库 | 入口 | `.ai/` 用途 |
| ---- | ---- | ----------- |
| blog | `AGENTS.md` | SDD 写作、Spec（`specs/`）、内容约束 |
| enx | `AGENTS.md` | 通用 instructions、贡献记录 |
| java-playground | `AGENTS.md` | 英文-only、Gradle 约定、demo 结构 |
| w10n-config | `AGENTS.md` | 基础设施与 homelab 上下文 |

blog 与其它代码项目的区别：本仓库 `.ai/` 以 [Spec 驱动写作](./spec-driven-development.md) 为主，不是通用的 `instructions.md` 模板。跨项目复用的是「AGENTS 入口 + `.ai/` 细则」这一层，各 repo 细则内容按领域自定。

## 新建代码仓库时的模板

**1. `AGENTS.md`（约 10–20 行）**

- 一句话说明项目用途
- 列出必读：`.ai/instructions.md`
- 如何运行 / 测试（一行命令）

**2. `.ai/instructions.md`**

- 语言与注释约定
- 目录结构
- 编码风格（与现有代码一致）
- 禁止事项（如：不要擅自改 CI、不要提交密钥）

**3. `.ai/README.md`（可选）**

- 索引 `.ai/` 下各文件

## 小结

AI docs 的最佳实践仍在形成中。对我这种 Cursor + Copilot 并用的场景，`AGENTS.md` 做入口、`.ai/` 放细则，是一种务实且与工具无关的折中；小项目保持精简，大项目再按领域拆分即可。
