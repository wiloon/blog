---
title: "Spring WebFlux: 响应式 Web 框架"
author: wiloon
date: 2026-06-26T21:44:56+08:00
lastmod: 2026-06-27T04:52:28+08:00
url: spring-webflux
categories:
  - java
tags:
  - AI-assisted
  - java
  - remix
  - spring
  - webflux
---

Spring WebFlux 是 Spring 5（2017）引入的响应式 Web 框架，与基于 Servlet 的 Spring MVC 并列。Boot 总览见 [Spring Boot](./spring-boot.md)；若只需提升并发能力而不改编程模型，可先看 [Java Virtual Threads](../virtual-threads.md)。

## 解决的问题

传统 Spring MVC 基于 Servlet 模型，每个请求占用一个线程，调用数据库或外部 API 时线程阻塞等待：

```
请求进来 → 分配线程 → 调用数据库（等待 100ms，线程阻塞）→ 调用外部 API（等待 200ms，线程阻塞）→ 返回
```

Tomcat 默认线程池约 200 个线程，高并发下线程池耗尽，后续请求排队。

Spring WebFlux 引入响应式编程模型，底层使用 **Netty**（非 Servlet 容器），少量线程处理大量并发：

```
请求进来 → 少量线程（CPU 核数）→ 发起数据库查询（注册回调，线程立刻去处理其他请求）→ 数据返回时触发回调继续处理
```

## 编程模型

WebFlux 使用 **Reactor** 库的 `Mono<T>`（0 或 1 个异步结果）和 `Flux<T>`（0 到 N 个异步结果）：

```java
// Spring MVC（同步阻塞）
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userService.findById(id);  // blocks on DB
}

// Spring WebFlux（异步非阻塞）
@GetMapping("/users/{id}")
public Mono<User> getUser(@PathVariable Long id) {
    return userService.findById(id);  // returns a deferred result
}
```

## WebFlux 的局限

- 编程模型与传统命令式完全不同，调试困难，学习成本高
- 需要支持响应式的驱动（R2DBC 替代 JDBC），不是所有库都有响应式版本
- **Java 21 虚拟线程的出现大幅削弱了 WebFlux 在普通业务系统里的核心优势**（见 [Java Virtual Threads](../virtual-threads.md)）

## 何时仍选 WebFlux

- SSE 实时推送
- 需要背压控制（消费者告知生产者降速）的流式处理
- 已有 WebFlux 项目：继续用即可，不必为并发改回 MVC

## Java 网络层全景

主流 Java Web 栈最终归为两大谱系：

```text
Servlet 容器系：  Tomcat / Jetty / Undertow
Netty 系：        Netty（或包装 Netty 的 Vert.x）
```

### Undertow

Red Hat / JBoss 出品，Spring Boot 把它作为与 Tomcat、Jetty 并列的一等选项：排除默认 `spring-boot-starter-tomcat`、引入 `spring-boot-starter-undertow` 即可。支持 HTTP/1.1、HTTP/2、WebSocket、TLS，非阻塞 IO，比 Tomcat 更轻；Quarkus 默认用它。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

### 其它框架的网络层

| 框架 | 网络层 | 备注 |
| ---- | ------ | ---- |
| Quarkus | Vert.x → Netty | Red Hat，云原生 |
| Micronaut | Netty | 编译期 DI，快速启动 |
| Helidon SE | Netty | Oracle |
| Vert.x | Netty | 多语言、事件驱动 |
| gRPC-Java | Netty | gRPC 协议 |

### Tomcat vs Netty：只是 IO 模型不同

二者解决的协议级问题相同（HTTP/1.1、HTTP/2、WebSocket、TLS 都支持），差别只在 IO 模型：

|  | Tomcat/Jetty/Undertow | Netty |
| ---- | --------------------- | ----- |
| IO 模型 | 阻塞（+ 虚拟线程） | 非阻塞异步 |
| 编程模型 | 同步，简单 | 异步，复杂 |
| 调试 | 堆栈清晰 | 响应式链路复杂 |

WebFlux 用 Netty 替换 Tomcat，协议复杂度并未消失，只是从 Tomcat 转移到 Netty。

### Netty 相对虚拟线程仍占优的场景

Java 21 虚拟线程让阻塞 IO 几乎零成本（见 [Java Virtual Threads](../virtual-threads.md)），多数业务用 Spring MVC + 虚拟线程即可。Netty / WebFlux 仍胜出的场景：

| 场景 | 原因 |
| ---- | ---- |
| 背压控制 | 响应式流让消费者告知生产者降速；虚拟线程无对应机制 |
| 单连接内存 | EventLoop 模型开销低于虚拟线程（每个虚拟线程有可增长的栈，初始约 1KB） |
| 流式响应 | `Flux<T>` 原生逐块发送；Servlet 仍是请求-响应 |

## 参考

- [Spring Boot](./spring-boot.md)
- [Java Virtual Threads](../virtual-threads.md)
- [Spring WebFlux 官方文档](https://docs.spring.io/spring-framework/reference/web/webflux.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-27 | 新增「Java 网络层全景」（Undertow、各框架网络层、Tomcat vs Netty IO 模型、Netty 占优场景） | 合并 comments-tree 启动打包文档相关章节 |
