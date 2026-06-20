---
title: Servlet 生命周期
author: "-"
date: 2011-10-30T08:25:36+00:00
lastmod: 2026-06-21T00:01:57+08:00
url: servlet-lifecycle
categories:
  - language
tags:
  - Servlet
  - java
  - spring-boot
  - remix
  - AI-assisted
aliases:
  - /servlet生命周期/
---

Servlet 运行在 Servlet 容器中，生命周期由容器管理。规范通过 `Servlet` 接口的 `init()`、`service()`、`destroy()` 描述这一过程；Java EE 8 及以前包名为 `javax.servlet.*`，Spring Boot 3 起对应 Jakarta Servlet（`jakarta.servlet.*`），语义不变。

## 四个阶段

### 加载和实例化

Servlet 容器负责加载和实例化 Servlet。容器启动时，或在首次需要该 Servlet 处理请求时，创建实例。容器通过类加载器找到 Servlet 类，再用反射调用**无参构造方法**实例化，因此业务 Servlet 一般不应定义带参构造方法。

### 初始化

实例化后，容器调用 `init()` 做一次性初始化（如读取配置、建立连接）。每个 Servlet 实例的 `init()` 只执行一次。初始化期间可通过 `ServletConfig` 读取配置（传统项目多在 `web.xml`，Spring Boot 中常由框架代劳）。失败时可抛出 `ServletException` 或 `UnavailableException` 通知容器。

### 请求处理

请求到达后，容器调用 `service()`；`HttpServlet` 会按 HTTP 方法分派到 `doGet()`、`doPost()` 等。`service()` 执行前 `init()` 必须已成功完成。处理中通过 `ServletRequest` / `ServletResponse`（或 `HttpServletRequest` / `HttpServletResponse`）读写请求与响应。若抛出表示永久不可用的 `UnavailableException`，容器会调用 `destroy()` 并返回 404；暂时不可用则返回 503。

### 服务终止

容器卸载 Servlet 或关闭时调用 `destroy()`，释放资源。之后实例被回收；若再次需要，容器会创建新实例。

## 生命周期概览

创建实例、`init()`、`destroy()` 各执行一次；初始化完成后实例常驻内存，每次请求由 `service()` 处理。若需在容器启动时即加载 Servlet，可在 `web.xml` 中配置 `<load-on-startup>`（Spring Boot 中可通过 `ServletRegistrationBean` 等方式注册）。

## 与 CGI 的对比

Servlet 与 Web 容器运行在**同一 JVM 进程**内，对每个请求通常启动**一个线程**处理，实例可复用、一般不在每次请求后销毁。传统 **CGI** 往往为每个请求 **fork 新进程**，处理完即退出，进程创建与销毁开销大，高并发下效率通常低于 Servlet。更完整的对比见 [Servlet](../../development/servlet.md)。

## Spring Boot 中的 Servlet

前后端分离只改变表现层职责（后端返回 JSON、不再用 JSP 拼页面），**并没有取代 Servlet**。绝大多数 Spring Boot REST 项目仍跑在 Servlet 容器上，只是日常开发很少手写 `extends HttpServlet`。

引入 `spring-boot-starter-web` 时，内嵌 Tomcat（也可换 Jetty、Undertow），本质是 Servlet 容器。请求链路大致如下：

```text
HTTP 请求
  → 嵌入式 Servlet 容器（Tomcat / Jetty / Undertow）
    → Filter 链（Spring Security、CORS 等，见 [Servlet Filter](./servlet-filter.md)）
      → DispatcherServlet（本身就是一个 Servlet）
        → HandlerMapping / HandlerAdapter
          → @RestController 方法
            → JSON 序列化（Jackson）
              → HTTP 响应
```

要点：

- **`DispatcherServlet` 是 Servlet**：Spring MVC 在 Servlet 栈上的入口，负责把请求分发给 `@Controller` / `@RestController`。
- **`@RestController` 不绕过 Servlet**：只是把返回值转成 JSON；请求仍经 `DispatcherServlet` 进入。
- **生命周期仍然适用**：`DispatcherServlet` 的 `init()` 在容器启动或首次请求时执行，`destroy()` 在容器关闭时执行；业务 Bean 由 Spring 管理，与「每个 Servlet 类一个实例」的模型并存。
- **可选的非 Servlet 栈**：`spring-boot-starter-webflux` 默认走 Reactor Netty，属于响应式模型，与上述 Servlet 链路不同；REST API 主流仍是 `starter-web`。

因此，理解 Servlet 生命周期对读 Spring Boot 日志、排查 Filter 顺序、自定义 `ServletRegistrationBean` 仍有帮助。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 补充 CGI 对比 | 承接自 java-basic 移出的 Servlet 段落 |
| 2026-06-21 | 重命名为 `servlet-lifecycle.md`；整理四个阶段结构；补充 Spring Boot 中的 Servlet；移除失效外链 | 文件名英文化；与现代前后端分离架构对齐 |
