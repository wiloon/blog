---
title: cc-switch：Claude Code 多账号切换
author: "-"
date: 2026-11-21T12:00:00+08:00
lastmod: 2026-11-21T12:00:00+08:00
url: cc-switch
categories:
  - AI
tags:
  - claude-code
  - remix
  - AI-assisted
---
> 我现在已经不用 cc-switch 了，这篇只作为历史记录保留。Claude Code 本身的用法见 [Claude Code 使用笔记](./claude-code.md)。

## 安装

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

停用 cc-switch 后，也要把 `ANTHROPIC_AUTH_TOKEN` 从 `~/.zshrc` 等 shell 配置里删掉，否则 Claude Code 仍会优先使用这个 token，或者继续报上面的冲突。
