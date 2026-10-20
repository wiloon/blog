---
title: "Resend: 事务邮件发送服务"
author: "-"
date: 2026-10-17T12:00:00+08:00
lastmod: 2026-10-17T12:00:00+08:00
url: resend
categories:
  - cloud
tags:
  - email
  - resend
  - dns
  - remix
  - AI-assisted
---

## Resend 是什么

Resend 是一个面向开发者的邮件发送服务（ESP，Email Service Provider）。程序调一个 HTTP API，Resend 负责把邮件真正投递到收件人的邮箱。2023 年上线，主打 API 简单、文档清楚，同一团队还维护了用 React 写邮件模板的 React Email。

它主要用来发事务邮件（transactional email）：注册验证、密码重置、账单通知、给管理员的告警。这类邮件是某个事件触发的、一对一的，和营销群发不是一回事（Resend 也有群发功能，叫 Broadcasts，这里不涉及）。

免费档每月 3,000 封、每天 100 封，对个人项目的通知邮件足够。具体额度以官网定价页为准。

## 为什么不自己发

服务器自己跑 SMTP 往外发信，基本进不了收件箱：

- 新 IP 没有发信信誉，Gmail、Outlook 会直接扔进垃圾箱或拒收。
- 云主机通常封了 25 端口出站（AWS EC2 默认就封）。
- 要自己处理退信、投诉、限速、重试。

ESP 的价值就在这里：它有养好信誉的发信 IP，处理退信和投诉，你只要证明「这个域名是我的，允许你代我发信」。

## 收信和发信是两件事

以 catglish.com 为例，两个方向用的是两套服务：

| 方向 | 服务 | 地址 | 作用 |
| ---- | ---- | ---- | ---- |
| 收信 | Cloudflare Email Routing | `support@`、`privacy@` | 别人写给这些地址的信，转发到我的 Gmail |
| 发信 | Resend | `no-reply@` | enx-api 往外发通知邮件 |

Cloudflare Email Routing 只能收、不能发；Resend 只管发。两者的 DNS 记录互不冲突：收信的 MX 在根域 `catglish.com` 上，Resend 的记录在 `send.catglish.com` 子域和 `resend._domainkey` 上。

## 域名验证：三类 DNS 记录

在 Resend 后台 Domains 里添加域名时，要选一个发信区域（离服务器近的即可，比如东京 `ap-northeast-1`），然后它会给出几条 DNS 记录。全部生效后点 Verify，状态变成 Verified 才能用这个域名发信。

### DKIM：证明邮件确实是你发的

一条 TXT 记录，名字是 `resend._domainkey`，值是一把公钥（`p=MIGf...`）。

Resend 发信时用对应的私钥给邮件签名，收件方的邮件服务器去 DNS 查这把公钥验签。验签通过，说明邮件确实出自被授权的发信方，而且传输途中没被改过。

### SPF 和 Return-Path：退信往哪儿回

邮件有两个「发件人」：

- 信头里的 `From:`，用户看到的那个，这里是 `no-reply@catglish.com`。
- 信封上的 MAIL FROM（也叫 Return-Path），退信寄回的地址。

Resend 把 MAIL FROM 放在子域 `send.catglish.com` 上，所以要给这个子域加：

- 一条 MX 记录：退信和投诉反馈回到 Resend，由它处理。
- 一条 SPF 的 TXT 记录（`v=spf1 ...`）：列出允许用这个域名发信的服务器 IP。

我的账号里，Resend 给的是一条 CNAME：`send.catglish.com` 指向 `send.forge.rmta.net`，MX 和 SPF 都由那边提供。效果一样，好处是 Resend 换发信 IP 时我不用改 DNS。

用子域而不是根域，是为了不碰根域已有的 SPF。catglish.com 根域的 SPF 是 Cloudflare Email Routing 的，一个域名只能有一条 SPF，直接改很容易把收信弄坏。

### DMARC：验证失败时怎么处理

一条 TXT 记录，名字是 `_dmarc`，告诉收件方：DKIM 或 SPF 对不上时该怎么处理（`p=none` 只观察、`quarantine` 进垃圾箱、`reject` 拒收），以及把汇总报告发到哪里。

DMARC 不是 Resend 验证的必需项，但 Gmail、Yahoo 现在都看重它，建议加一条最宽松的起步：

```text
_dmarc.catglish.com  TXT  "v=DMARC1; p=none;"
```

### 记录要设成灰云

在 Cloudflare 上，这些记录必须是 DNS only（灰云），不能开代理（橙云）。代理只对 HTTP 流量有意义，CNAME 开了代理以后，外面查到的是 Cloudflare 的 IP，不再是 Resend 的目标，验证就会失败。

## API Key

后台 API Keys 里创建，两种权限：

- Full access：能管理域名、key 等一切，只给自己在本地用。
- Sending access：只能发信，还可以限定某个域名。部署到服务器上的用这个。

key 以 `re_` 开头，只在创建时显示一次，属于密钥，不进代码仓库。

## 在 enx-api 里怎么用

enx-api 不用 SDK，直接调 HTTP API：

```bash
# What enx-api's email.Sender does, as curl
curl -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Catglish <no-reply@catglish.com>",
    "to": ["support@catglish.com"],
    "subject": "Test",
    "html": "<p>hello</p>"
  }'
```

用到三个环境变量：

| 变量 | 值 | 是否密钥 |
| ---- | -- | -------- |
| `RESEND_FROM` | `Catglish <no-reply@catglish.com>` | 否 |
| `RESEND_ADMIN_TO` | `support@catglish.com` | 否 |
| `RESEND_API_KEY` | `re_...` | 是 |

目前发两种管理员通知：

- 用户在扩展里上报页面问题（ENX ADR-010）。
- Stripe 退款找不到对应的积分发放、没能自动扣回（ENX ADR-049），提醒我手动处理。

`RESEND_ADMIN_TO` 或 key 为空时，通知直接跳过，不报错。所以「没收到邮件」不等于「没事发生」，配完之后要实际触发一封验证。

整条链路：enx-api 调 Resend 从 `no-reply@catglish.com` 发出 → 收件人 `support@catglish.com` → Cloudflare Email Routing 转发 → Gmail。

## 怎么确认能发出去

- Resend 后台的 Emails 页列出每一封信的状态：Sent、Delivered、Bounced、Complained。发不出去先看这里。
- 收到信后，在 Gmail 里「显示原始邮件」，看 `SPF`、`DKIM`、`DMARC` 三项是不是 `PASS`。
- 命令行查 DNS 记录是否生效：

```bash
# DKIM public key
dig +short TXT resend._domainkey.catglish.com
# Return-Path subdomain
dig +short CNAME send.catglish.com
# DMARC policy
dig +short TXT _dmarc.catglish.com
```
