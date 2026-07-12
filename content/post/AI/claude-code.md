---
title: claude
author: "-"
date: 2026-04-20T12:54:03+08:00
url: claude
categories:
  - AI
tags:
  - remix
  - AI-assisted
---
## 安装 Claude Code

```bash
# macOS 用 brew 安装（推荐）
brew install --cask claude-code

# 或安装最新版
brew install --cask claude-code@latest

# 用 npm 安装
npm install -g @anthropic-ai/claude-code
```

## 安装 cc-switch（多账号切换工具）

```bash
brew install --cask cc-switch
```

安装后从 Launchpad 或用以下命令启动：

```bash
open -a cc-switch
```

## 认证冲突处理

cc-switch 会设置 `ANTHROPIC_AUTH_TOKEN` 环境变量，若同时存在 `claude /login` 的 key，启动时会出现：

```text
⚠ Auth conflict: Both a token (ANTHROPIC_AUTH_TOKEN) and an API key (/login managed key) are set.
```

**想用 cc-switch 管理的账号：**

```bash
claude /logout
```

**想用 `/login` 的 key：**

```bash
unset ANTHROPIC_AUTH_TOKEN
# 或从 ~/.zshrc 中删除该变量
```

## claude command

```bash
claude whoami
claude chat --prompt "你当前是哪个模型？请给出模型名称。"

export ANTHROPIC_BASE_URL=http://127.0.0.1:4141 && \
export ANTHROPIC_AUTH_TOKEN=sk-ant-api03-bridging-locally-format-check-passed-xxxxxxxxxxxx && \
claude
```

## CLAUDE.md 与 AGENTS.md

不同 AI 编程工具各自识别不同的项目指令文件：

| 工具 | 识别的指令文件 |
|---|---|
| VS Code Copilot | `AGENTS.md`、`.github/copilot-instructions.md` |
| Claude Code CLI | `CLAUDE.md`（项目根目录或父目录） |
| OpenAI Codex CLI | `AGENTS.md` |

两者**不会**自动识别对方的约定文件：

- 项目只有 `AGENTS.md`：Claude Code 不会加载它
- 项目只有 `CLAUDE.md`：VS Code Copilot 不会加载它

### 同时使用两个工具的方案

**推荐：软链接**（以 `AGENTS.md` 为主文件）

```bash
ln -s AGENTS.md CLAUDE.md
```

优点：单一事实来源，改一处两个工具都生效，不依赖任何工具特定语法。

**不推荐：`@include`**

Claude Code 支持 `@path/to/file` 语法，但 VS Code Copilot 的 `AGENTS.md` 不支持 `@include`，只能单向引用，不是真正的双向共享。

## 常见错误

### model_max_prompt_tokens_exceeded

```text
API Error: 400 {"error":{"code":"model_max_prompt_tokens_exceeded","message":"prompt token count of 133252 exceeds the limit of 128000"}}
```

**原因：** 当前对话的上下文（prompt）超过了模型的最大 token 限制。

Claude 原生 API 的上下文窗口为 **200k tokens**（claude-3-5-sonnet 等主流模型）。如果报错显示 128k 限制，通常是因为使用了**中转代理**（通过 `ANTHROPIC_BASE_URL` 设置的第三方或本地 API），代理服务自身限制了 prompt 大小为 128k。

Claude Code 有**自动压缩**机制：当上下文接近限制时会自动触发 `/compact`，把对话历史总结压缩。但以下情况仍会绕过自动压缩直接报错：

- **单次操作本身就超限**：比如一次性读取多个大文件，单个请求的 prompt 已经超过 128k，还没来得及压缩
- **CLAUDE.md 本身过大**：每次请求都会带上指令文件，如果文件很长会持续占用大量 token
- **自动压缩触发太晚**：压缩是在接近上限时触发，但如果下一步操作读取的内容很大，仍可能超出

**解决方法：**

- 手动执行 `/compact` 压缩当前对话历史
- 开启新对话（`/clear`），彻底清空上下文
- 减少一次性加载的文件数量，分批处理
- 精简 CLAUDE.md / AGENTS.md 的内容，删除冗余说明
