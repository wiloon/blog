---
title: Spring MVC
author: "-"
date: 2012-11-30T08:01:33+00:00
lastmod: 2026-06-27T04:52:28+08:00
url: springmvc
categories:
  - java
tags:
  - java
  - spring
  - remix
  - AI-assisted
aliases:
  - /p2629/
  - /p4043/
  - /p4812/
  - /p6695/
  - /spring-mvc
---

Spring MVC 是 Spring Framework 中负责处理 HTTP 请求的 Web 框架，实现了 MVC 设计模式。它是一个**功能模块**，而非独立框架。

**本文专注 HTTP 处理与现用实践**（注解映射、REST、校验等）。Spring Framework 整体定位、非 Web 场景（如 CLI）、早期 XML 配置、与 JDK 5 注解的关系、Web 层历史演变，见 [Spring](./spring.md)。

## Spring MVC 与 Spring Boot 的关系

这两者经常被混淆，理清层次是关键。

### 层次关系

```text
Spring Framework（基础框架）
  └── Spring MVC（Web 层模块，属于 Spring Framework 的一部分）

Spring Boot（构建在 Spring Framework 之上的脚手架/工具）
  └── spring-boot-starter-web（包含 Spring MVC + 内嵌 Tomcat + Jackson）
```

- **Spring MVC** 是 Spring Framework 中负责处理 HTTP 请求的 Web 框架，实现了 MVC 设计模式。它是一个**功能模块**。
- **Spring Boot** 是一个**构建工具/脚手架**，它并不替代 Spring MVC，而是让配置 Spring MVC（以及其他模块）变得更简单。

### 对比：传统 Spring MVC vs Spring Boot

| 方面 | 传统 Spring MVC | Spring Boot |
| ---- | --------------- | ----------- |
| 配置方式 | XML（`web.xml`、`applicationContext.xml`）或 Java Config | 自动配置，几乎零 XML |
| 部署方式 | 打包为 WAR，部署到外部 Tomcat | 打包为可执行 JAR，内嵌 Tomcat |
| 依赖管理 | 手动指定每个依赖及版本，容易版本冲突 | Starter 统一管理，版本经过验证 |
| 启动入口 | 通过 Servlet 容器启动 | `@SpringBootApplication` 主类 + `main()` 方法 |
| 学习曲线 | 较陡，需理解大量 XML 配置 | 较平，约定优于配置 |

### 底层请求处理链路

无论是传统 Spring MVC + WAR，还是 Spring Boot + JAR，处理 HTTP 请求的调用链从未改变：

```text
HTTP 请求
  → Tomcat 监听端口、接收连接
  → 调用 DispatcherServlet（Servlet 规范）
  → Spring MVC 路由到对应的 Controller 方法
  → 你的业务代码
  → Jackson 序列化返回值为 JSON（REST 场景）
  → Tomcat 写回 HTTP 响应
```

Spring Boot 做的只是**把"搭起这条链路"的工作自动化**了，底层的 Servlet、Tomcat、Spring MVC 一个都没少。

### 一句话总结

> **Spring MVC 是 Spring Boot 所使用的 Web 框架**。使用 Spring Boot 开发 Web 应用时，底层仍然是 Spring MVC 在处理请求，Spring Boot 只是消除了手动配置 Spring MVC 的繁琐工作。

---

## 迁移视角：从 Spring MVC 到 Spring Boot

如果之前用过 Spring MVC + XML 配置 + 外部 Tomcat 的开发模式，迁移到 Spring Boot 主要是以下变化：

1. `web.xml` → 删除，Spring Boot 自动注册 `DispatcherServlet`
2. `applicationContext.xml` → 删除，改用 `application.properties` / `application.yml`
3. `@Controller`、`@RequestMapping`、`@Service` 等注解**完全不变**，Spring MVC 的使用方式不需要学习新东西
4. 部署方式从 WAR + Tomcat → 可执行 JAR
5. Tomcat 独立配置文件 → 统一纳入 `application.yml`

---

## Spring MVC 与 JSP：不是强绑定

一个常见的误解是 Spring MVC = JSP 模板引擎。实际上两者没有强绑定关系。

Spring MVC 支持多种视图层方案：

- **JSP / JSTL**：传统服务端渲染，返回 HTML 页面（早期常见方式，Spring Boot 中不推荐）
- **Thymeleaf / Freemarker**：现代服务端模板引擎，同样返回 HTML，Spring Boot 中的推荐方案
- **`@ResponseBody` / `@RestController`**：直接返回 JSON/XML，实现前后端分离

### Spring Boot 与 JSP

Spring Boot 对 JSP 的支持是二等公民，官方不推荐，原因有两点：

1. 内嵌 Tomcat/Jetty 对 JSP 的支持不完整，需要额外添加依赖
2. **打成可执行 JAR 后，JSP 无法工作**——JAR 内的 JSP 文件无法被 Servlet 容器解析，必须改为打 WAR 包才行，基本上就退回了传统部署模式

如果需要服务端渲染 HTML，Spring Boot 生态的标准答案是 **Thymeleaf**：添加 `spring-boot-starter-thymeleaf` 依赖，模板放在 `src/main/resources/templates/`，开箱即用，打 JAR 也没问题。

---

## @RequestMapping 及简化注解

`@RequestMapping` 是 Spring MVC 的核心注解，用于将 HTTP 请求映射到对应的处理方法上，可标注在类或方法上。

```java
@Controller
@RequestMapping("/api/users")   // class-level prefix shared by all methods
public class UserController {

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public User getUser(@PathVariable Long id) { ... }

    @RequestMapping(value = "/", method = RequestMethod.POST)
    public User createUser(@RequestBody User user) { ... }
}
```

因为每次都要写 `method = RequestMethod.GET` 比较繁琐，Spring 4.3 为常用 HTTP 方法提供了简化注解：

| 简化注解 | 等价于 |
| -------- | ------ |
| `@GetMapping` | `@RequestMapping(method = RequestMethod.GET)` |
| `@PostMapping` | `@RequestMapping(method = RequestMethod.POST)` |
| `@PutMapping` | `@RequestMapping(method = RequestMethod.PUT)` |
| `@DeleteMapping` | `@RequestMapping(method = RequestMethod.DELETE)` |
| `@PatchMapping` | `@RequestMapping(method = RequestMethod.PATCH)` |

用简化注解改写后更简洁：

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) { ... }

    @PostMapping("/")
    public User createUser(@RequestBody User user) { ... }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) { ... }
}
```

`@RestController` 是 Spring 3.x 引入的注解（等价于 `@Controller` + `@ResponseBody`），用它即可让 Spring MVC 变成纯 REST API 服务器，与前端框架（Vue、React 等）完全解耦。

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);  // serialized to JSON automatically
    }
}
```

这段代码**不需要 Spring Boot**，在传统 Spring MVC 项目里同样可以运行。

---

## @Validated 与 @Valid：请求参数校验

Spring MVC 支持通过 Bean Validation（JSR-303/380）对请求参数进行校验，涉及两个注解：

- **`@Validated`**：Spring 自己的注解，标注在 **Controller 类**上，告诉 Spring 为该类启用方法级别的参数校验（由 `MethodValidationPostProcessor` 处理）。
- **`@Valid`**：Jakarta Bean Validation 标准注解，标注在具体的**方法参数**上，触发对该参数对象内部字段的级联校验。

两者分工不同，缺一不可：

```java
@RestController
@RequestMapping("/api/users")
@Validated   // ① enable method-level validation for this controller
public class UserController {

    @PostMapping("/")
    public User createUser(@Valid @RequestBody CreateUserRequest req) {
        // ② @Valid triggers field constraints on req
        return userService.create(req);
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable @Min(1) Long id) {
        // @Validated on class makes @Min(1) on parameters work
        return userService.findById(id);
    }
}
```

```java
public class CreateUserRequest {
    @NotBlank
    private String name;

    @Email
    private String email;

    @Min(0)
    private int age;
}
```

| | `@Validated`（类上） | `@Valid`（参数上） |
| --- | --- | --- |
| 来源 | Spring（`org.springframework.validation.annotation`） | Jakarta Bean Validation（`jakarta.validation`） |
| 作用 | 为整个 Controller 启用方法级校验 | 触发该参数对象的级联字段校验 |
| 缺少时 | 方法参数上的直接约束注解（`@Min` 等）不生效 | 对象内部的字段约束不会被检查 |
| 校验失败异常 | `ConstraintViolationException` | `MethodArgumentNotValidException` |

**依赖**：Spring Boot 项目添加 `spring-boot-starter-validation` 即可引入 Hibernate Validator 实现。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

---

## 为什么 Java Web 需要 Tomcat/Jetty

### 没有 Tomcat，Java 能直接提供 HTTP 吗

能。JDK 自带一个基础 HTTP server：

```java
// 裸 TCP socket，自己解析 HTTP
ServerSocket ss = new ServerSocket(8080);

// JDK 内置（JDK 6 起），非生产级
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/", exchange -> { /* ... */ });
server.start();
```

JDK 内置的 `HttpServer` 面向工具与测试，缺少连接池、HTTP/2、完善的 TLS 与可调线程模型，生产环境基本不用。

### Servlet 规范 vs 实现

Java EE（1990 年代末）追求可移植：**同一个 WAR 应当能部署到任意服务器**（Tomcat、JBoss、WebLogic、WebSphere）。

```text
应用层（WAR）
  ↕  Servlet API（jakarta.servlet.*）   ← 标准接口，由 Sun/Oracle 定义
Servlet 容器（Tomcat / Jetty / JBoss）
  ↕  TCP / HTTP
OS
```

Servlet API 是**规范**，Tomcat/Jetty 是**实现**。应用只依赖规范，理论上与容器无关。这与 Go 的哲学相反——Go 的 `net/http` 本身就是生产级标准库，没有「部署目标」的概念。

### Tomcat/Jetty 实际解决了什么

它们不只是「适配器」，而是承载了 20 多年生产打磨的实现：HTTP/1.1、HTTP/2、HTTP/3、WebSocket、TLS、连接池与 keep-alive、线程模型调优、慢连接攻击防护等。即便没有 Tomcat，也得有别的组件来解决这些问题——复杂度不会消失，只是被一个久经测试的库吸收了。

Spring Boot 把 Tomcat/Jetty 内嵌进 fat jar，开发体验已接近 Go（`mvn package && java -jar app.jar`），但底层仍是这套 Servlet 实现。WebFlux 则用 Netty 替换 Servlet 容器，IO 模型与网络层选型见 [Spring WebFlux](./spring-webflux.md)。

---

## 小结

- Spring Framework 总览与演变（含 Struts 时代 Web 层脉络）见 [Spring](./spring.md)
- Spring MVC 可以实现前后端分离，Java 只负责 RESTful API，与 JSP 无关
- Spring Boot 不是实现 RESTful API 的必要条件，它只是**消除了配置负担**，让同样的事情做起来更快
- 用 Spring Boot 写 REST API 和用传统 Spring MVC 写，**业务代码几乎一模一样**，差异只在项目搭建和配置阶段

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-24 | 合并 `language/java/spring-mvc.md` 现代实践章节；添加 `/spring-mvc` alias；删除重复文档 | 避免 Spring MVC 内容重复 |
| 2026-06-24 | 将 iteye 导入的代码块改为标准 fenced code block；补全 Struts2 XML 片段 | 修复代码高亮与可读性 |
| 2026-06-24 | 删除 2012 iteye 转载章节（Struts/Webwork/Tapestry 等框架史） | 过时内容与现用 Spring MVC 实践无关 |
| 2026-06-24 | 移至 `language/java/spring/spring-mvc.md`；`categories` 改为 `java` | 与 Spring 专题文章同目录归类 |
| 2026-06-24 | 同批迁入 `spring-ioc`、`spring-boot-devtools` 及 `other/`/`development/` 下 Spring MVC 老文 | 统一 Spring 专题目录 |
| 2026-06-24 | 明确本文范围（MVC 实践）；小结链到 spring.md | 历史与整体定位由 spring.md 承载 |
| 2026-06-27 | 新增「为什么 Java Web 需要 Tomcat/Jetty」（JDK HttpServer、Servlet 规范 vs 实现、与 Go 对比） | 合并 comments-tree 启动打包文档相关章节 |