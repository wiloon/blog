---
title: Spring Security Remember Me 实现机制
author: "-"
date: 2011-12-26T06:43:20+00:00
lastmod: 2026-07-02T17:34:42+08:00
url: remember-me
categories:
  - java
tags:
  - java
  - spring security
  - authentication
  - remix
  - AI-assisted
---

登录之外，很多系统还需要"关闭浏览器后仍保持登录"，这就是 remember-me（记住我）。Spring Security 提供两种实现，机制和安全性差别很大。`SecurityFilterChain` 整体认证流程见 [Spring Security](../../language/java/spring-security.md)。

## 常见误解：不是"让 session 活得更久"

容易望文生义地以为 remember-me 就是把普通 session 的过期时间设得很长，下次访问时顺便刷新一下 session id。实际上标准做法是**两套凭证分层**：

1. 登录后先发一个短期 session（比如 30 分钟）。
2. 勾选了 remember-me，再额外发一个长期凭证（cookie 里的 `series:token`）。
3. 下次访问时如果短期 session 已失效，服务端用长期凭证验证通过后，**重新建立一个新的 session**，而不是延长旧 session 的寿命。

这样做的原因：短期 session 追求高频、低延迟访问（常放内存/Redis），长期凭证追求低频、可撤销、可审计（放数据库即可）。如果把两者合并成"一个超长有效期的 session"，会导致服务端要长期保留大量会话状态，且缺乏按设备单独撤销的能力（下文详述）。

## 简单哈希令牌（`TokenBasedRememberMeServices`，默认方式）

Cookie 内容：

```text
username:expirationTime:md5(username + ":" + expirationTime + ":" + password + ":" + key)
```

- **优点**：无状态，不查数据库。
- **缺陷**：服务端无法单独让某一台设备的 cookie 失效——除非改密码或改全局 `key`，那样会让所有设备同时下线；且签名依赖密码本身，密码不变、cookie 一旦泄露就能一直重放。

## 持久化令牌（`PersistentTokenRepository`）

数据库维护一张 `persistent_logins` 表，每一行代表**一次登录（一个设备/浏览器）**：

| series | username | token | last_used |
| ------ | -------- | ----- | --------- |

- Cookie 里存的是 `series:token`（两个随机值），不含密码信息。
- 每次带着 remember-me cookie 的请求认证成功后，**token 值会轮换**，但 `series` 不变。判定逻辑发生在**服务端**：先用 `series` 查到数据库里当前记录的 token 值，再和客户端发来的 token 比对——相等则正常轮换；`series` 能查到但 token 不相等，说明这个值是已经被换掉的旧值又出现了一次，`PersistentTokenBasedRememberMeServices` 会判定为 cookie 窃取（cookie theft），删除该 `series` 的记录并强制重新登录。
- 因为每个设备对应独立的 `series` 行，服务端可以**按行删除**来单独踢掉一个设备，不影响其他设备的登录状态。这就是"跨设备失效控制"：本质是把认证状态从"无状态签名"换成了"以设备为粒度的数据库记录"。
- 需要澄清一点：`series` 并不是浏览器指纹或设备硬件 id，它只是"这一次 remember-me 登录时生成、存在这台设备 cookie 里的随机值"。它不校验设备身份，如果 cookie 原样被复制到另一台机器，`series` 照样验证通过——真正防重放靠的是上面的轮换 + 比对机制，不是设备识别。另外这个 cookie 和普通 cookie 一样，只要没限制 `path`，每次请求都会被发送，传输频率跟 session cookie 无异；真正低频的是服务端"校验/轮换"这个动作的触发频率（只在 session 失效时才用得上）。

## 跨设备失效控制的三个能力

1. **可枚举**：按 `username` 查询 `persistent_logins` 表，能看到该用户当前所有"记住我"的设备。
2. **可单点撤销**：删除某一行 `series`，对应设备下次请求 token 校验失败，强制走正常登录。
3. **可全量撤销**：改密码时清空该用户所有 `series` 记录，实现"改密码后所有设备强制下线"。

## 与 JWT refresh token 的对照

OAuth2 / JWT 体系里常见的 refresh token，跟这里的长期凭证是同一类角色：都是"低频使用、用来重建短期凭证"的东西。但安全性取决于实现方式：

- 纯无状态 refresh token（只验签名和过期时间，服务端不记录状态）→ 没有重放检测，也没法单独撤销某一次登录，安全性弱于持久化 remember-me。
- 加了 **rotation（轮换）+ reuse detection（重放检测）** 的 refresh token（服务端维护 `family_id` + 当前 token 值，逻辑与这里的 `series`/`token` 完全对应）→ 安全模型与持久化 remember-me 等价。

详细机制对照见 [Refresh Token Rotation: 刷新令牌轮换与重放检测](../web/refresh-token-rotation.md)。

## comments-tree 怎么用

[comments-tree](https://github.com/wiloon/comments-tree) 项目选用的是持久化令牌方案：

```java
@Bean
public PersistentTokenRepository persistentTokenRepository() {
    JdbcTokenRepositoryImpl jdbcTokenRepository = new JdbcTokenRepositoryImpl();
    jdbcTokenRepository.setDataSource(dataSource);
    jdbcTokenRepository.setCreateTableOnStartup(false);
    return jdbcTokenRepository;
}
```

```java
.rememberMe(rm -> rm
        .rememberMeParameter("rememberMe")
        .tokenRepository(persistentTokenRepository())
        .tokenValiditySeconds(30 * 24 * 60 * 60)
        .userDetailsService(userService)
)
```

选择 `PersistentTokenRepository`（JDBC 版）而不是默认的哈希令牌，核心原因是需要设备粒度的失效能力，同时避免密码参与签名带来的重放风险。

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                                      | 原因                                                                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-07-01 | 文件从 2011 年转载链接合集重写为原创技术说明；标题从 "remember me" 改为 "Spring Security Remember Me 实现机制"；categories 从 Web 改为 java；标签删除 reprint，新增 java、spring security、authentication、remix、AI-assisted | 原内容仅为外部链接列表且已过时（部分链接已失效），改写为结合 comments-tree 真实配置的技术说明，并与 spring-security.md 互相链接避免重复维护 |
| 2026-07-01 | 调整结构：先通用介绍两种 remember-me 实现和跨设备失效控制能力，再单独用「comments-tree 怎么用」一节说明实际配置                                                                                                               | 通用原理和最佳实践说明不应受具体项目选型影响，拆分后结构更清晰                                                                              |
| 2026-07-02 | 新增「常见误解：不是让 session 活更久」一节；澄清 series 不是设备指纹、cookie 传输频率与 session 一致；新增「与 JWT refresh token 的对照」一节并链接新文章 refresh-token-rotation.md | 与用户讨论后补充关键结论，避免读者把 remember-me 误解为单纯延长 session，并厘清与 JWT refresh token 的安全模型对应关系 |
