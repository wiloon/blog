---
title: Spring Security Remember Me 实现机制
author: "-"
date: 2011-12-26T06:43:20+00:00
lastmod: 2026-07-01T20:42:27+08:00
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
- 每次带着 remember-me cookie 的请求认证成功后，**token 值会轮换**，但 `series` 不变；如果 `series` 匹配但 `token` 不匹配，说明这份 cookie 被盗用后重放过，`PersistentTokenBasedRememberMeServices` 会判定为 cookie 窃取（cookie theft），删除该 `series` 的记录并强制重新登录——这是内置的重放检测机制。
- 因为每个设备对应独立的 `series` 行，服务端可以**按行删除**来单独踢掉一个设备，不影响其他设备的登录状态。这就是"跨设备失效控制"：本质是把认证状态从"无状态签名"换成了"以设备为粒度的数据库记录"。

## 跨设备失效控制的三个能力

1. **可枚举**：按 `username` 查询 `persistent_logins` 表，能看到该用户当前所有"记住我"的设备。
2. **可单点撤销**：删除某一行 `series`，对应设备下次请求 token 校验失败，强制走正常登录。
3. **可全量撤销**：改密码时清空该用户所有 `series` 记录，实现"改密码后所有设备强制下线"。

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
