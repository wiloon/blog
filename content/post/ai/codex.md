---
title: "Codex 使用笔记：Approve for me 与配置作用范围"
author: "-"
date: 2026-11-05T11:53:39+08:00
lastmod: 2026-11-05T11:53:39+08:00
url: codex
categories:
  - AI
tags:
  - codex
  - ai-coding
  - remix
  - AI-assisted
---

## Approve for me 是什么

这篇文档记录 Codex 的使用与配置，先从自动审批功能开始。以下内容按 2026-11-05 的 OpenAI 官方文档整理。

Codex 的自动审批功能叫 Auto-review，桌面端的选项名称是 Approve for me。遇到需要审批的操作时，由独立的 reviewer agent 判断是否允许执行，并给出理由。原有沙箱、网络和文件访问限制仍然保留。来源：[Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)。

## 桌面端怎么启用

在桌面端打开聊天，点击输入框下方的权限控件，选择 Approve for me，并确认当前聊天已经选中它。选项是否可用受账号和组织策略影响。

这里确认的是当前聊天的权限选择；要设置本地 Codex 的持久默认值，再使用下面的配置文件。桌面端入口见官方文档的 [Select automatic review](https://learn.chatgpt.com/docs/sandboxing/auto-review#select-automatic-review)。

## 用户级还是项目级

两种都支持，取决于配置文件的位置：

| 范围 | 位置或方式 | 用途 |
| --- | --- | --- |
| 用户级 | `~/.codex/config.toml` | 设置当前用户的默认行为 |
| 项目级 | `<repo>/.codex/config.toml` | 为某个仓库覆盖默认值 |
| 单次 CLI 启动 | 命令行参数 | 临时试用，不写入默认配置 |

CLI 和 IDE 扩展共用这些配置层。项目配置只有在项目被信任后才会加载。来源：[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)。

### 用户级配置

如果希望平时默认使用自动审批，在 `~/.codex/config.toml` 的顶层添加或修改：

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
sandbox_mode = "workspace-write"
```

三项分别表示：遇到需要升级权限的操作时申请审批；交给 Auto-review 审批；使用允许工作区写入的沙箱。前两项负责审批流程，第三项负责沙箱范围。配置组合见 [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)。

这些键应放在第一个 `[section]` 之前，避免误写进其他 TOML 表。已有同名键时修改原值，不要重复追加。

### 项目级配置

如果只希望某个仓库启用，在该仓库的 `.codex/config.toml` 中写入上面的三项配置即可。

反过来，用户级已经启用自动审批，但某个项目希望保留人工审批，可以在项目配置中覆盖：

```toml
approval_policy = "on-request"
approvals_reviewer = "user"
```

项目配置还可以放在仓库的子目录中。同名配置按从项目根目录到当前工作目录的顺序加载，越靠近当前目录的配置优先。用户目录默认是 `~/.codex`；如果设置了 `CODEX_HOME`，用户配置位于该目录下的 `config.toml`。来源：[Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced)。

### 单次启动时启用

想先试用一次，可以在项目目录运行：

```bash
codex --sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review
```

该命令为这次 CLI 启动指定配置，写法来自 [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)。

## 配置冲突时谁优先

与本文相关的配置优先级，从高到低是：

1. CLI 参数和 `-c` / `--config` 覆盖。
1. 已信任项目的 `.codex/config.toml`，越靠近当前目录越优先。
1. 通过 `--profile` 选中的 profile 文件。
1. 用户级 `~/.codex/config.toml`。
1. 云端下发的配置默认值、系统配置、内置默认值。

组织强制要求另行约束可选值，本地配置不能突破这些要求。来源：[Configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence)。

## 自动审批与其他权限设置的区别

| 设置 | 控制什么 |
| --- | --- |
| `sandbox_mode` | 命令运行时的文件与网络访问边界 |
| `approval_policy` | 什么时候提出审批请求 |
| `approvals_reviewer` | 请求交给用户还是 Auto-review 审批 |

只设置 `approval_policy = "on-request"`，不会自动选中 Auto-review。设置 `approval_policy = "never"` 后，没有交互式审批请求可供 Auto-review 处理。`--dangerously-bypass-approvals-and-sandbox` 则跳过审批和沙箱，也不是这个功能的启用方式。来源：[Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)、[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)。

## 启用后仍需留意什么

沙箱内已经允许的操作直接执行，不会每次都额外审查。需要越过边界的操作才进入审批流程；被拒绝后，主 agent 应寻找更安全的方案，或停下来向用户说明。Computer Use 的应用级审批仍直接交给用户。来源：[Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)。

自动审批会增加模型调用，因此也可能增加 Codex 用量。桌面端可查看 Reviewing、Approved、Denied 等审查状态。来源：[Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)。

如果配置后没有按预期工作，先检查当前聊天选项、项目是否已信任、更高优先级的配置，以及组织策略。排查配置加载可参考 [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)。
