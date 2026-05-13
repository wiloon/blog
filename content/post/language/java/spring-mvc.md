---
title: Spring MVC
author: "-"
date: 2026-05-12T23:17:31+08:00
lastmod: 2026-05-12T23:17:31+08:00
url: spring-mvc
categories:
  - java
tags:
  - java
  - spring
  - remix
  - AI-assisted
---

Spring MVC 是 Spring Framework 中负责处理 HTTP 请求的 Web 框架，实现了 MVC 设计模式。它是一个**功能模块**，而非独立框架。

## Spring MVC 与 Spring Boot 的关系

这两者经常被混淆，理清层次是关键。

### 层次关系

```
Spring Framework（基础框架）
  └── Spring MVC（Web 层模块，属于 Spring Framework 的一部分）

Spring Boot（构建在 Spring Framework 之上的脚手架/工具）
  └── spring-boot-starter-web（包含 Spring MVC + 内嵌 Tomcat + Jackson）
```

- **Spring MVC** 是 Spring Framework 中负责处理 HTTP 请求的 Web 框架，实现了 MVC 设计模式。它是一个**功能模块**。
- **Spring Boot** 是一个**构建工具/脚手架**，它并不替代 Spring MVC，而是让配置 Spring MVC（以及其他模块）变得更简单。

### 对比：传统 Spring MVC vs Spring Boot

| 方面     | 传统 Spring MVC                                          | Spring Boot                                   |
| -------- | -------------------------------------------------------- | --------------------------------------------- |
| 配置方式 | XML（`web.xml`、`applicationContext.xml`）或 Java Config | 自动配置，几乎零 XML                          |
| 部署方式 | 打包为 WAR，部署到外部 Tomcat                            | 打包为可执行 JAR，内嵌 Tomcat                 |
| 依赖管理 | 手动指定每个依赖及版本，容易版本冲突                     | Starter 统一管理，版本经过验证                |
| 启动入口 | 通过 Servlet 容器启动                                    | `@SpringBootApplication` 主类 + `main()` 方法 |
| 学习曲线 | 较陡，需理解大量 XML 配置                                | 较平，约定优于配置                            |

### 底层请求处理链路

无论是传统 Spring MVC + WAR，还是 Spring Boot + JAR，处理 HTTP 请求的调用链从未改变：

```
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
@RequestMapping("/api/users")   // 类级别：所有方法共享前缀
public class UserController {

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public User getUser(@PathVariable Long id) { ... }

    @RequestMapping(value = "/", method = RequestMethod.POST)
    public User createUser(@RequestBody User user) { ... }
}
```

因为每次都要写 `method = RequestMethod.GET` 比较繁琐，Spring 4.3 为常用 HTTP 方法提供了简化注解：

| 简化注解         | 等价于                                           |
| ---------------- | ------------------------------------------------ |
| `@GetMapping`    | `@RequestMapping(method = RequestMethod.GET)`    |
| `@PostMapping`   | `@RequestMapping(method = RequestMethod.POST)`   |
| `@PutMapping`    | `@RequestMapping(method = RequestMethod.PUT)`    |
| `@DeleteMapping` | `@RequestMapping(method = RequestMethod.DELETE)` |
| `@PatchMapping`  | `@RequestMapping(method = RequestMethod.PATCH)`  |

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
        return userService.findById(id);  // 直接返回对象，自动序列化为 JSON
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
@Validated   // ① 类级别：开启整个 Controller 的方法校验
public class UserController {

    @PostMapping("/")
    public User createUser(@Valid @RequestBody CreateUserRequest req) {
        // ② @Valid：触发对 req 对象内部字段的校验
        // 如果 req 中有 @NotBlank、@Min 等注解，校验失败时抛出 MethodArgumentNotValidException
        return userService.create(req);
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable @Min(1) Long id) {
        // @Validated 在类上才能让方法参数上的约束注解（@Min）生效
        // 否则 @Min(1) 不会被执行
        return userService.findById(id);
    }
}
```

```java
// 请求参数对象
public class CreateUserRequest {
    @NotBlank
    private String name;

    @Email
    private String email;

    @Min(0)
    private int age;
}
```

|              | `@Validated`（类上）                                  | `@Valid`（参数上）                              |
| ------------ | ----------------------------------------------------- | ----------------------------------------------- |
| 来源         | Spring（`org.springframework.validation.annotation`） | Jakarta Bean Validation（`jakarta.validation`） |
| 作用         | 为整个 Controller 启用方法级校验                      | 触发该参数对象的级联字段校验                    |
| 缺少时       | 方法参数上的直接约束注解（`@Min` 等）不生效           | 对象内部的字段约束不会被检查                    |
| 校验失败异常 | `ConstraintViolationException`                        | `MethodArgumentNotValidException`               |

**依赖**：Spring Boot 项目添加 `spring-boot-starter-validation` 即可引入 Hibernate Validator 实现。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

---

## 结论

- Spring MVC 可以实现前后端分离，Java 只负责 RESTful API，与 JSP 无关
- Spring Boot 不是实现 RESTful API 的必要条件，它只是**消除了配置负担**，让同样的事情做起来更快
- 用 Spring Boot 写 REST API 和用传统 Spring MVC 写，**业务代码几乎一模一样**，差异只在项目搭建和配置阶段
