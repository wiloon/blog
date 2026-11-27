---
title: "Coding Agent Headless Auth: Claude Code、Codex、Cursor、Antigravity 无人值守登录对比"
author: "-"
date: 2026-11-25T15:51:04+08:00
lastmod: 2026-11-25T15:51:04+08:00
url: coding-agent-headless-auth
categories:
  - AI
tags:
  - claude-code
  - codex
  - cursor
  - antigravity
  - remix
  - AI-assisted
---

我在一台无人值守的 Linux 机器（SER8）上用 [baton](../projects/baton.md) 跑四家 coding agent：Claude Code、OpenAI Codex、Cursor CLI 和 Google Antigravity CLI（`agy`）。四家都用个人订阅，不用按量计费的 API。机器上没人点浏览器，所以登录怎么保持有效是个实际问题。下面是 2026-11 按官方文档和实测整理的结果。

## 对比

| | 无人值守的官方方式 | 计费 | 登录能撑多久 |
| ---- | ---- | ---- | ---- |
| Claude Code | `claude setup-token` 生成一年有效的 OAuth token，放进 `CLAUDE_CODE_OAUTH_TOKEN` | 订阅 | token 一年；`/login` 登录有固定到期日，使用不会延长 |
| Codex | `codex login --device-auth`（设备码），或在有浏览器的机器上登录后把 `~/.codex/auth.json` 拷过去 | ChatGPT 登录走订阅；API key 按 API 计价 | 使用期间自动刷新 token；闲置多久失效文档没写 |
| Cursor CLI | `CURSOR_API_KEY`（在 cursor.com/dashboard/api 生成） | API key 是否算个人 Pro/Ultra 订阅额度，文档没写 | 浏览器登录存在系统密钥库，有效期文档没写 |
| Antigravity CLI | 只有交互登录：SSH 远程 OAuth（打开链接、粘贴授权码）；或 Gemini API key | 个人订阅只能交互登录；API key 走 Gemini API 计费 | 凭证存在 keyring，有效期文档没写 |

只有 Claude Code 给了一个按订阅计费、明确为无人值守准备的长期 token。另外三家要么靠能自动刷新的登录，要么换成按量计费的 API key。

## Claude Code

`claude auth login`（会话里的 `/login`）登录有固定的到期日，用 Claude Code 不会延长它。快到期时 `claude -p` 会提示：

```text
Warning: this sign-in can end at any time from now until 2026-11-25. Renewing it does not move that date. Run claude auth login now, or use claude setup-token for unattended jobs.
```

官方给的办法是 `claude setup-token`：浏览器授权后打印一个一年有效的 OAuth token（前缀 `sk-ant-oat`），不会存到本地，要自己放进环境变量 `CLAUDE_CODE_OAUTH_TOKEN`。细节见 [Claude Code 使用笔记](./claude-code.md) 里的「无人值守机器上的登录：claude setup-token」。

我在 SER8 上只用这个 token（清空 `CLAUDE_CONFIG_DIR`，不读已有登录）测过：

- `claude auth status` 显示 `Auth token: CLAUDE_CODE_OAUTH_TOKEN`
- `claude -p` 正常运行，用量算在订阅里
- `--output-format stream-json` 输出里仍有 `rate_limit_event`，带 `five_hour`、`seven_day` 两个窗口的利用率和重置时间
- `claude -p /usage` 只显示本次会话的花费和 token 数，不显示订阅额度；用 `/login` 登录时它会显示「Current session / Current week」的百分比

所以用 token 时，订阅额度只能从运行输出的 `rate_limit_event` 里读。

另外两点：`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 的优先级比这个 token 高，设了就会改走 API；`--bare` 模式不读这个 token。

## Codex

`codex login` 默认是 ChatGPT 账号登录，凭证在 `~/.codex/auth.json`（或系统凭证库，由 `cli_auth_credentials_store` 决定），里面有 refresh token。官方说法是使用期间会在过期前自动刷新，所以经常跑任务的机器一般不用重新登录。文档没写闲置多久会失效。

没有浏览器的机器有两种办法：

```bash
# Device code login (must be enabled in ChatGPT security settings first)
codex login --device-auth

# Or log in on a machine with a browser, then copy the credential file
scp ~/.codex/auth.json ser8:~/.codex/auth.json
```

`codex login --with-access-token` 读的 access token 要在 ChatGPT Enterprise 工作区里由管理员授权才能创建，个人 Plus/Pro 用不了。官方自动化场景首推 API key（`codex login --with-api-key`），但那是按 API 计价，不用订阅额度。

## Cursor CLI

`cursor-agent login` 打开浏览器登录，设 `NO_OPEN_BROWSER=1` 可以只打印登录链接。新版本（2026.11.19 起）把凭证存进系统密钥库，`~/.config/cursor/auth.json` 里只剩 `{"storedIn": "os-secret-store"}`。

这带来一个坑：通过 SSH 跑 `cursor-agent status` 显示「Not logged in」，在 systemd 用户服务里跑才显示已登录，因为 SSH 会话里访问不到密钥库。排查时要在和实际运行相同的环境里检查。

自动化方式是 `CURSOR_API_KEY` 或 `--api-key`，在 cursor.com/dashboard/api 生成。文档没说个人 Pro/Ultra 订阅的 API key 用的是不是订阅额度；CLI 的帮助文本里提到「Enterprise plan + service account API key」，看起来服务账号是企业版功能。

## Antigravity CLI（agy）

个人 Google AI 订阅（Free、Pro、Ultra）只能交互登录。本机登录会打开浏览器；远程机器用「Remote SSH OAuth flow」：CLI 打印授权链接，在别的电脑浏览器里打开，再把页面上的授权码粘回 SSH 终端。headless 模式（`agy -p`）用缓存的凭证，没登录时直接报 `authentication required` 退出，不会卡住。

登录存储方式取决于会话类型。实测 1.5.x 在 SSH 会话里会写文件 `~/.gemini/antigravity-cli/antigravity-oauth-token`（日志：`Using file-based token storage because SSH session detected`），这个文件过一段时间会消失；在 systemd 用户服务里则从 keyring 读（日志：`ChainedAuth: authenticated via keyring`）。所以检查文件在不在来判断是否登录是不对的，我在 baton 里就因此误判过 agy 掉线。

其他两种方式都不用个人订阅：

- Gemini API key：`settings.json` 里设 `"modelProvider": "gemini"`，再设 `GEMINI_API_KEY`，按 Gemini API 计费
- ADC：`gcloud auth application-default login` 加 `AGY_ADC_AUTH=true`，面向 Gemini Enterprise / Vertex

额度可以不花 token 查到：

```bash
agy -p "/quota"
```

输出每行一条记录（额度池、窗口、剩余百分比、重置时间），Gemini 和 Claude/GPT 模型分开计。

## 我的做法

- Claude Code 换成 `setup-token`，token 存在密码管理器里，部署时写到机器上一个 0600 的文件，只注入给 `claude` 进程，其他 agent 看不到
- Codex、Cursor、agy 保持订阅登录，靠自动刷新维持；登录失效时让流水线把这家标为认证失败、暂停调用，然后人工重新登录
- 检查登录状态一律在 agent 实际运行的环境（systemd 用户服务）里做，不在 SSH 会话里做

## 参考

- [Claude Code Authentication](https://code.claude.com/docs/en/authentication)
- [Codex Authentication](https://developers.openai.com/codex/auth)
- [Cursor CLI Authentication](https://cursor.com/docs/cli/reference/authentication)
- [Antigravity CLI Authenticate](https://antigravity.google/docs/install?tab=cli)、[Headless mode](https://antigravity.google/docs/cli/headless)
