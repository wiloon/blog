---
title: "ntfy: 用 HTTP 请求给手机发推送"
author: "-"
date: 2026-10-17T07:17:29+08:00
lastmod: 2026-10-17T07:17:29+08:00
url: ntfy
categories:
  - development
tags:
  - ntfy
  - notification
  - self-hosted
  - remix
  - AI-assisted
---

## ntfy 是什么

[ntfy](https://ntfy.sh)（读作 notify）是一个开源的发布/订阅推送服务。脚本用一个普通的 HTTP PUT/POST 把消息发到某个 **topic**，订阅了这个 topic 的手机 App、浏览器或其他脚本就会收到通知。

- 不需要注册账号，topic 第一次被用到时自动创建
- 服务端是一个 Go 程序，可以用官方的 ntfy.sh，也可以自己部署
- 客户端：Android（Google Play / F-Droid）、iOS（App Store）、网页（Web Push），都是开源的

典型用途是让无人值守的脚本在出结果时通知人：备份完成、CI 失败、定时任务出错、AI agent 跑完一个任务。

## 最简单的用法

手机装好 App，订阅一个 topic，比如 `wiloon-enx-agent-7f3k9q`，然后：

```bash
# Plain message
curl -d "Backup finished" ntfy.sh/wiloon-enx-agent-7f3k9q

# Title, priority, tags (emoji shortcodes) and a link opened on tap
curl \
  -H "Title: enx-agent: #51 merged" \
  -H "Priority: default" \
  -H "Tags: white_check_mark" \
  -H "Click: https://github.com/wiloon/enx/pull/203" \
  -d "PR #203 merged, issue #51 closed" \
  ntfy.sh/wiloon-enx-agent-7f3k9q
```

常用的请求头：

| 请求头 | 作用 |
| ---- | ---- |
| `Title` | 通知标题 |
| `Priority` | `min` / `low` / `default` / `high` / `urgent`（或 1–5），高优先级会响铃、可以穿透勿扰 |
| `Tags` | 标签，emoji 短码会显示成图标，比如 `warning`、`white_check_mark` |
| `Click` | 点通知时打开的 URL |
| `Actions` | 通知上的按钮（打开链接、发 HTTP 请求等） |
| `Authorization` | 受保护 topic 的访问令牌，`Bearer tk_...` |

## 安全：topic 名就是密码

在公共的 ntfy.sh 上，**知道 topic 名的人都能读和写这个 topic**。所以：

- topic 名用一段随机字符串，不要用 `alerts`、`backup` 这种能猜到的名字
- 消息里不要放密钥、token 这类敏感内容，只放「发生了什么 + 去哪里看」
- 需要更强的控制时，用付费账号预留 topic 并设访问令牌，或者自己部署

## 自己部署

服务端是一个可执行文件，也有官方容器镜像 `binwiederhier/ntfy`（`docker run -p 80:80 -it binwiederhier/ntfy serve`），源码在 [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy)。配置文件是 `/etc/ntfy/server.yml`，个人用的最小配置：

```yaml
# /etc/ntfy/server.yml
base-url: "https://ntfy.example.com"
listen-http: ":80"
cache-file: "/var/cache/ntfy/cache.db"
auth-file: "/var/lib/ntfy/user.db"
auth-default-access: "deny-all"      # read-write (default) | read-only | write-only | deny-all
# iOS can only be woken through Apple's push service, which ntfy.sh relays.
# Only a poll request (message ID + topic hash, no content) goes through ntfy.sh.
upstream-base-url: "https://ntfy.sh"
```

```bash
# Create a user and an access token, then grant it one topic
ntfy user add wiloon
ntfy access wiloon enx-agent rw
ntfy token add wiloon
```

前面加一层带 TLS 的反向代理即可。一个人用的话，资源占用很小。

自部署时要注意 **iOS 的限制**：iPhone 上的 App 只能被 Apple 推送服务（APNs）唤醒，而 APNs 证书在 ntfy.sh 手里。所以自部署服务器会经由 ntfy.sh 发一个 `poll_request`，App 被唤醒后再回你自己的服务器取消息，这就是 `upstream-base-url` 的作用。按官方文档，这个请求只带消息 ID 和 topic URL 的 SHA256，不带消息内容。去掉这项，iOS 上的通知可能延迟几个小时才到。Android 可以直接和自己的服务器保持长连接，不依赖 Google 的推送服务。

## 是不是手机推送的最佳选择

没有唯一的最佳选择，按手机和网络环境选：

| 方案 | 平台 | 自部署 | 费用 | 特点 |
| ---- | ---- | ---- | ---- | ---- |
| ntfy | Android / iOS / 网页 | 可以 | 免费，托管版有付费档 | 开源；`curl` 一行就能发；Android 不依赖 Google 推送 |
| Bark | 仅 iOS | 可以 | 免费 | 开源；走 APNs，iPhone 上到达稳定；中文用户多 |
| Pushover | Android / iOS / 桌面 | 不可以 | 每个平台一次性付费 | 闭源但成熟稳定，到达率好 |
| Gotify | Android / 网页 | 只能自部署 | 免费 | 开源；没有 iOS App |
| Telegram Bot | 全平台 | 不需要 | 免费 | 已经在用 Telegram 的话最省事；国内网络需要额外处理 |
| 企业微信 / 飞书 / 钉钉 机器人 | 全平台 | 不需要 | 免费 | webhook 调用；国内网络直接可用 |

几条选择思路：

- **iPhone + 国内网络**：Bark 最省心；ntfy 也能用，但 iOS 推送绕经 ntfy.sh
- **Android**：ntfy 或 Gotify，自部署在家里的服务器上
- **不想维护服务**：Pushover（付费）、Telegram Bot、企业微信机器人
- **需要多端（手机 + 电脑 + 浏览器）**：ntfy

ntfy 的优势是协议简单、开源、可以自部署、各端都有客户端。它是一个通用的好选择，但不是任何情况下都最好。

## 在脚本里用

失败和成功用不同的优先级，失败时点通知直接打开日志或 PR：

```bash
notify() {
  # $1 title, $2 body, $3 priority, $4 click URL
  curl -fsS -m 10 \
    -H "Authorization: Bearer $NTFY_TOKEN" \
    -H "Title: $1" -H "Priority: ${3:-default}" -H "Click: ${4:-}" \
    -d "$2" "$NTFY_URL/enx-agent" >/dev/null || true
}

notify "enx-agent: #51 needs info" "Questions left on the issue" high \
  "https://github.com/wiloon/enx/issues/51"
```

`|| true` 是为了推送失败时不影响主流程，`-m 10` 防止推送服务不可用时卡住脚本。

无人值守 agent 的完整用法见 [让 Claude Code 自主处理 GitHub Issue](../AI/afk-agent-github-issues.md)。
