---
title: Spring Boot 3.x Migration: 关键特性与约束
author: wiloon
date: 2026-06-26T21:44:56+08:00
lastmod: 2026-06-26T21:44:56+08:00
url: spring-boot-3-migration
categories:
  - java
tags:
  - AI-assisted
  - java
  - remix
  - spring
  - spring boot
---

Spring Boot 3.0（2022 年底发布）底层依赖 Spring Framework 6.x。本文汇总从 2.x 升级到 3.x 时最常见的破坏性变更与约束。框架总览见 [Spring Boot](./spring-boot.md)。

## Spring Boot 与 Spring Framework 版本对应

| Spring Boot | Spring Framework |
| --- | --- |
| 3.0.x | 6.0.x |
| 3.2.x | 6.1.x |
| 3.3.x / 3.4.x | 6.1.x / 6.2.x |
| **3.5.x** | **6.2.x** |

## 1. Java 版本要求

Spring Boot 3.x **最低要求 Java 17**。

## 2. javax → jakarta 命名空间迁移（最大变更）

Java EE 已捐赠给 Eclipse 基金会，品牌更名为 Jakarta EE，所有包名从 `javax.*` 改为 `jakarta.*`。这是**代码层面影响最广**的变更，几乎所有用到 Servlet、JPA、Bean Validation 的代码都要修改：

| 旧包名（javax） | 新包名（jakarta） |
| --- | --- |
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.transaction.*` | `jakarta.transaction.*` |
| `javax.annotation.*` | `jakarta.annotation.*` |

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.persistence.Entity;
```

## 3. Spring Security 6.x：`WebSecurityConfigurerAdapter` 彻底移除

`WebSecurityConfigurerAdapter` 已彻底移除，必须改为注册 `SecurityFilterChain` Bean，详见 [Spring Security](../spring-security)。

### Lambda DSL 是什么

Spring Security 的配置支持两种 API 风格：旧的链式写法和新的 Lambda DSL 写法。

**旧写法（链式 API，Spring Security 5.x 之前）：**

```java
http
    .authorizeRequests()
        .antMatchers("/public").permitAll()
        .anyRequest().authenticated()
        .and()
    .formLogin()
        .loginPage("/login")
        .and()
    .csrf().disable();
```

**Lambda DSL 写法（Spring Security 5.2+ 引入，6.x 强制）：**

```java
http
    .authorizeHttpRequests(auth -> auth
        .requestMatchers("/public").permitAll()
        .anyRequest().authenticated()
    )
    .formLogin(form -> form
        .loginPage("/login")
    )
    .csrf(csrf -> csrf.disable());
```

| 特性 | 旧链式写法 | Lambda DSL |
| --- | --- | --- |
| 结构 | 扁平链式，靠 `.and()` 拼接 | 嵌套 Lambda，结构清晰 |
| 可读性 | 需要靠缩进约定 | 作用域边界明确 |
| IDE 支持 | 容易混淆配置层级 | 类型推断更准确 |
| Spring Security 6.x | 已废弃 | **唯一支持的写法** |

Spring Security 6.x 移除了旧的链式 API（如 `authorizeRequests()`、`.and()`），只保留 Lambda DSL，因为它更清晰地表达了每个配置块的边界，减少配置错误。

## 4. Hibernate 6.x

ORM 层升级到 Hibernate 6，部分 HQL/JPQL 语法更严格，一些隐式类型转换不再支持，自定义类型映射 API 有变化。

## 5. AOT 与 GraalVM Native Image

Spring Boot 3.x 正式支持 GraalVM Native Image 编译，可以将应用编译为原生可执行文件，启动时间从秒级降到毫秒级，但对反射、动态代理等有额外约束。构建链依赖 **Spring AOT** 在打包前处理 IoC 容器；详见 [Spring AOT 简介](./spring-aot.md) 与 [GraalVM Native Image 简介](../graalvm-native-image.md)。

## 参考

- [Spring Boot](./spring-boot.md)
- [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)
- [Spring AOT](./spring-aot.md)
