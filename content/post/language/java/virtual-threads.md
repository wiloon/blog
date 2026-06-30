---
title: "Java Virtual Threads: 虚拟线程与高并发"
author: wiloon
date: 2026-06-26T21:44:56+08:00
lastmod: 2026-06-26T21:44:56+08:00
url: virtual-threads
categories:
  - java
tags:
  - AI-assisted
  - java
  - java 21
  - remix
  - virtual threads
---

Java 21（2023）正式引入虚拟线程（Project Loom）。对多数业务系统，**Spring MVC + 虚拟线程**是比 [Spring WebFlux](./spring/spring-webflux.md) 更低成本的并发方案。Boot 里一行配置即可开启，见下文。

## 什么是虚拟线程

虚拟线程由 JVM 管理，数量可达百万级。阻塞时 JVM 自动挂起虚拟线程、释放底层 OS 线程去处理其他任务，数据返回后再恢复执行——**对应用代码完全透明**。

这与 Go 语言的协程（goroutine）是同一思想：用户态轻量级并发，阻塞时不占用 OS 线程。Go 从 2009 年就原生支持，Java 晚了约 14 年。

| | Java 虚拟线程 | Go 协程（goroutine） |
| --- | --- | --- |
| 出现时间 | 2023（Java 21） | 2009（Go 1.0） |
| 调度器 | JVM 内置 | Go runtime |
| 初始栈内存 | 约 1KB | 约 2KB |
| 与现有代码兼容 | ✅ 完全兼容，API 不变 | — |

## 对应用层完全透明

虚拟线程的复杂性封装在 JVM 内部，应用层代码写法与传统线程一模一样：

```java
// platform thread pool
ExecutorService executor = Executors.newFixedThreadPool(200);

// virtual threads: same API, one-line change
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

executor.submit(() -> {
    User user = db.findById(id);  // looks blocking; JVM parks the virtual thread
    return user;
});
```

Spring Boot 3.2 开启虚拟线程只需一行配置，业务代码不用改：

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

## 虚拟线程 vs WebFlux

对于绝大多数业务系统，**Spring MVC + Java 21 虚拟线程**是更好的选择：

| | Spring MVC + 虚拟线程 | Spring WebFlux |
| --- | --- | --- |
| 代码改动 | 零改动，一行配置 | 需要重写为响应式风格 |
| 调试体验 | 清晰可读的堆栈 | 复杂的响应式链路 |
| 库兼容性 | 所有现有库直接可用 | 需要响应式版本的驱动 |
| 适合场景 | 普通业务系统 | 流式推送、背压控制 |

WebFlux 仍有价值的场景：SSE 实时推送、需要背压控制的流式处理。详见 [Spring WebFlux](./spring/spring-webflux.md)。

## 实际建议

- 新项目：Spring MVC + Java 21 虚拟线程，首选
- 已有 MVC 项目：升级 Java 21，开启虚拟线程，低成本高收益
- 已有 WebFlux 项目：继续用，没有必要改回 MVC
- 需要流式推送/背压：WebFlux 仍有价值

## 参考

- [Spring Boot](./spring/spring-boot.md)
- [Spring WebFlux](./spring/spring-webflux.md)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
