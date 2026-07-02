---
title: CSRF/XSRF
author: "-"
date: 2012-07-15T09:16:25+00:00
lastmod: 2026-07-02T18:20:33+08:00
url: csrfxsrf
categories:
  - Web
tags:
  - csrf
  - xsrf
  - security
  - remix
  - AI-assisted
aliases:
  - /p3857/
---
## CSRF/XSRF

CSRF (Cross-site request forgery) 跨站请求伪造，也被称成为"one click attack"或者session riding，通常缩写为CSRF或者XSRF，是一种对网站的恶意利用。尽管听起来像跨站脚本 (XSS) ，但它与XSS非常不同，并且攻击方式几乎相左。XSS利用站点内的信任用户，而CSRF则通过伪装来自受信任用户的请求来利用受信任的网站。与XSS攻击相比，CSRF攻击往往不大流行 (因此对其进行防范的资源也相当稀少) 和难以防范，所以被认为比XSS更具危险性。攻击通过在授权用户访问的页面中包含链接或者脚本的方式工作。例如: 一个网站用户 Bob 可能正在浏览论坛，而同时另一个用户 Alice 也在此论坛中，并且后者刚刚发布了一个具有 Bob 银行链接的图片消息。设想一下，Alice 编写了一个在 Bob 的银行站点上进行取款的 form 提交的链接，并将此链接作为图片 tag。如果 Bob 的银行在 cookie 中保存他的授权信息，并且此 cookie 没有过期，那么当 Bob 的浏览器尝试装载图片时将提交这个取款 form 和他的 cookie，这样在没经 Bob 同意的情况下便授权了这次事务。

CSRF 是一种依赖 web 浏览器的、被混淆过的代理人攻击 (deputy attack) 。在上面银行示例中的代理人是 Bob 的 web 浏览器，它被混淆后误将 Bob 的授权直接交给了 Alice 使用。

下面是CSRF的常见特性:

依靠用户标识危害网站

利用网站对用户标识的信任

欺骗用户的浏览器发送HTTP请求给目标站点

另外可以通过IMG标签会触发一个GET请求，可以利用它来实现CSRF攻击。风险在于那些通过基于受信任的输入form和对特定行为无需授权的已认证的用户来执行某些行为的web应用。已经通过被保存在用户浏览器中的cookie进行认证的用户将在完全无知的情况下发送HTTP请求到那个信任他的站点，进而进行用户不愿做的行为。

使用图片的CSRF攻击常常出现在网络论坛中，因为那里允许用户发布图片而不能使用JavaScript。贴图只是GET的方式，很多时候我们需要伪造POST的请求。一个办法是利用跨站，当然目标站点可能不存在跨站，这个时候我们可以从第三方网站发动攻击。

比如我要攻击一个存在问题的blog，那就先去目标blog留言，留下一个网址，诱其主人点击过来 (这个就要看你的忽悠本事咯:p) ，然后构造个HTML表单提交些数据过去。

多窗口浏览器就帮了一点忙。

多窗口浏览器 (firefox、遨游、MyIE……) 便捷的同时也带来了一些问题，因为多窗口浏览器新开的窗口是具有当前所有会话的。即我用IE登陆了我的Blog，然后我想看新闻了，又运行一个IE进程，这个时候两个IE窗口的会话是彼此独立的，从看新闻的IE发送请求到Blog不会有我登录的cookie；但是多窗口浏览器永远都只有一个进程，各窗口的会话是通用的，即看新闻的窗口发请求到Blog是会带上我在blog登录的cookie。

想一想，当我们用鼠标在Blog/BBS/WebMail点击别人留下的链接的时候，说不定一场精心准备的CSRF攻击正等着我们。

## 前后端分离架构下还有 CSRF 风险吗

前后端分离本身不是防 CSRF 的银弹，关键要看前端如何保存和发送身份凭证。

**风险显著降低的情况**：登录后把 token（如 JWT）存在 `localStorage`/`sessionStorage`，前端手动在请求头 `Authorization: Bearer <token>` 里带上。浏览器不会像 cookie 那样自动附加这个 token，跨站页面伪造的请求拿不到它，天然免疫经典 CSRF。

**风险依然存在的情况**：

1. 仍用 cookie 保存凭证：不少方案把 refresh token 或 session id 存成 `HttpOnly` cookie（防 XSS 窃取），但 cookie 会被浏览器自动带上，这种情况下 CSRF 依然成立，需配合 `SameSite=Strict/Lax`、CSRF token（如双重提交 cookie）等防护。
2. CORS 配置不当：接口把 `Access-Control-Allow-Origin` 错误地回显为请求来源而不做白名单校验，同时又开启 `Access-Control-categories 由 CS 改为 Web（与目录一致）；新增「相关阅读」及「前后端分离架构下还有 CSRF 风险吗」两个章节 | 修正分类不一致；补充与站内 XSS/JWT 文章的互链；原文只讲传统 cookie 会话场景，补充现代 token 认证下的 CSRF 风险辨析
3. 无鉴权的状态变更接口：内部管理后台或微服务间调用为图省事只信任来源 IP 或 Referer，同样可能被伪造。
4. CSRF 变种：如 Login CSRF，把攻击者的身份"种"进受害者会话，即使不直接读写数据也是同类风险。

结论：用 header 携带 token 基本免疫 CSRF；只要还用 cookie 做认证，就仍需 `SameSite` + CSRF token + 严格校验 `Origin`/`Referer` 三重防护。

## 相关阅读

- [XSS, Cross Site Scripting, CSRF, Cross-site request forgery, CORS](../cs/xss-cross-site-scripting.md)：CSRF 与 XSS 的关系辨析
- [JWT vs Session：认证方式对比](./jwt-session.md)：使用 Cookie/Session 时如何通过 `HttpOnly`/`SameSite`/`Secure` 等属性缓解 CSRF

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-02 | 补充 lastmod；标签由 reprint 改为具体技术标签（csrf/xsrf/security）+ remix + AI-assisted；新增「相关阅读」站内链接；categories 由 CS 改为 Web（该文件位于 content/post/web/ 目录，与该目录下其他文章分类保持一致） | 便于与站内其他 CSRF/XSS/JWT 相关文章互相跳转；修正分类不一致 |
