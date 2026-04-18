---
title: claude
author: "-"
date: 2026-04-18T17:17:06+08:00
url: claude
categories:
  - Linux
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
