---
title: Spring Boot DevTools
author: "-"
date: 2026-05-31T07:25:07+08:00
lastmod: 2026-05-31T07:25:07+08:00
url: spring-boot-devtools
categories:
  - language
tags:
  - java
  - spring
  - spring-boot
  - devtools
  - remix
  - AI-assisted
---

## 背景

开发 Spring Boot 时，`spring-boot-devtools` 提供 **快速重启** 与 **静态资源热刷新**，常被误认为「和 IDE HotSwap 一样改 Java 就能生效」。本文说明它实际做什么，并与 [开发期热替换](/dcevm-hotswapagent)、[JPDA](/java-debug-jpda) 区分。

Spring Boot 总览见 [Spring Boot](/spring-boot)。

## 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

仅在开发 classpath 使用；生产打包应排除（`optional` + 不打进 fat jar 的常见做法）。

## 两个 ClassLoader（Restart）

DevTools 默认启用 **Restart**：

| ClassLoader | 加载内容 | 变更时 |
| ----------- | -------- | ------ |
| **base** | 第三方依赖（`spring-boot-starter-*` 等） | 一般不 reload |
| **restart** | 你的 `target/classes` 业务代码 | 监控到变更后 **快速重启** 应用上下文 |

「快速重启」不是 HotSpot 的 **类热替换**：而是 **停掉当前 Spring 上下文再拉起**，但 **base ClassLoader 保留**，比冷启动整个 JVM 快。

因此：

- 改 **业务 Java 类** → 触发 **restart**（仍是一次上下文重建，不是 JPDA 改方法体）
- 改 **静态资源**（`src/main/resources` 下 html/css 等）→ **LiveReload** 通知浏览器刷新，无需重启 JVM

## 与 HotSwap / BTrace 的对比

| 机制 | 层级 | 典型场景 |
| ---- | ---- | -------- |
| **DevTools Restart** | Spring 上下文 + 双 ClassLoader | 本地改代码后几秒内重新跑 Bean |
| **IDE HotSwap** | JVM + [JPDA](/java-debug-jpda) / 有限 redefine | Debug 下改 **方法体** |
| **DCEVM + HotSwapAgent** | 增强 HotSpot + javaagent | 开发机放宽 redefine、重载 Spring 配置 |
| **BTrace attach** | [Attach](/attach-api) + [ASM](/java-asm) | **已运行** 进程观测，非开发热更 |

DevTools **不** 使用 Attach API 给业务类插探针；也 **不** 替代 `mvn spring-boot:run` 外的生产部署。

## 常用配置

```properties
# 关闭 Restart（只要 LiveReload 时）
spring.devtools.restart.enabled=false

# 额外监控路径
spring.devtools.restart.additional-paths=src/main/java

# 排除某些资源不触发 restart
spring.devtools.restart.exclude=static/**,public/**
```

IDEA 需开启 **Build project automatically** 并与 DevTools 配合，改代码后才会编译并触发 restart（具体以 IDE 版本为准）。

## 参考

- [Spring Boot Reference — DevTools](https://docs.spring.io/spring-boot/reference/using/devtools.html)
- [Spring Boot](/spring-boot)
- [开发期热替换（HotSwap / DCEVM）](/dcevm-hotswapagent)
