---
title: "Refresh Token Rotation: 刷新令牌轮换与重放检测"
author: "-"
date: 2026-07-02T17:17:44+08:00
lastmod: 2026-07-02T17:17:44+08:00
url: refresh-token-rotation
categories:
  - Web
tags:
  - oauth2
  - jwt
  - authentication
  - remix
  - AI-assisted
---

OAuth2 / JWT 体系里的 refresh token，如果只靠"签名 + 过期时间"校验，是**无状态**的：服务端不记录任何已发放、已使用的记录，因此没法检测重放、也没法单独撤销某一次登录。要补齐这块安全能力，业界通用做法叫 **refresh token rotation（轮换）+ reuse detection（重放检测）**，思路和 Spring Security 的持久化 remember-me（见 [Spring Security Remember Me 实现机制](../other/remember-me.md)）几乎一致，只是术语不同。

## 无状态 refresh token 的问题

最简单的实现：refresh token 就是一个长期有效的签名字符串，服务端只验证签名和过期时间，不查库。

- 优点：无状态，扩展性好。
- 缺陷：refresh token 一旦泄露，在过期之前可以被无限次使用，服务端**发现不了**，也**撤销不了**单独一次登录（除非撤销全部密钥或拉黑名单）。

这跟 Spring Security 默认的 `TokenBasedRememberMeServices`（哈希令牌）是同一类问题：都是"无状态签名"，天然缺少重放检测和单点撤销能力。

## Rotation + Reuse Detection 的做法

给每一条 refresh token 的"血统"维护一个 `family_id`（有的实现里叫 `session_id`、`lineage_id`，作用等价于 remember-me 里的 `series`）：

| family_id | current_token | issued_at | used |
| --------- | -------------- | --------- | ---- |

1. 用户登录时，颁发 `family_id` + 第一个 `refresh_token`，同时记录到数据库。
2. 客户端用 `refresh_token` 换新的 `access_token` 时，服务端**同时颁发一个新的 `refresh_token`**，旧值作废，数据库里 `current_token` 更新为新值。
3. 如果收到的 `refresh_token` 匹配 `family_id` 但**不等于**数据库里记录的 `current_token`——说明这个 token 已经被换过一次了，现在又被用了一次，只有两种可能：客户端重复提交，或者 token 被别人窃取后重放。
4. 一旦判定为重放，直接**撤销整条 `family_id`**，强制该登录下线重新认证。

这跟持久化 remember-me 的判定逻辑完全对应：

| 概念 | Remember-me（持久化令牌） | Refresh token rotation |
| --- | --- | --- |
| 登录血统标识 | `series` | `family_id` |
| 一次性凭证值 | `token` | `refresh_token` |
| 轮换时机 | 每次带 cookie 认证成功后 | 每次用 refresh token 换 access token 后 |
| 重放判定 | series 匹配、token 不匹配 | family_id 匹配、refresh_token 不匹配 |
| 处理方式 | 删除该 series，强制重新登录 | 撤销该 family_id，强制重新认证 |

## 安全性取决于有没有服务端状态

`refresh token rotation` 不是 JWT 天生自带的能力，而是**额外加的一层服务端状态**。所以对比时不能简单说"JWT 比 session 安全"或反过来，要看具体实现：

- 纯无状态 refresh token（只验签名和过期）→ 没有重放检测、没法单点撤销，安全性弱于持久化 remember-me。
- 加了 rotation + family 追踪的 refresh token（本质上又变成"有状态"）→ 和持久化 remember-me 的安全模型等价。

一句话总结：能不能防重放、能不能单独踢掉一次登录，取决于**服务端是否维护了轮换记录**，跟用的是 session 还是 JWT 无关。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-02 | 新建文章，说明 refresh token rotation 与 reuse detection 机制，并与 remember-me.md 对照 | 博客里此前没有相关文档，用户希望系统了解并留档 |
