---
title: Spring Boot
author: wiloon
date: 2026-05-11T14:24:31+08:00
lastmod: 2026-05-12T16:06:52+08:00
tags: ["java", "spring", "spring boot", "remix", "AI-assisted"]
categories: ["java"]
---

## Spring Boot 是什么

Spring Boot 是 Pivotal （现为 VMware/Broadcom）在 2014 年推出的框架，建立在 Spring Framework 之上，目标是**简化整个 Spring 生态的开发、配置和部署**。它不只是简化 Spring MVC，同样简化了 Spring Data（数据库访问）、Spring Security（认证授权）、Spring Messaging（消息队列）等全家桶的配置。

核心理念是 **"约定优于配置"（Convention over Configuration）**：框架提前定好"默认约定"，只要遵循这些约定，就不需要写任何配置；只有想偏离默认行为时，才需要显式配置。

例如，classpath 里有 `spring-boot-starter-web`，Spring Boot 就**约定**你要启动一个 Web 服务，自动完成：注册 `DispatcherServlet`、内嵌 Tomcat 监听 **8080 端口**、注册 Jackson 用于 JSON 序列化。你什么都不写，`java -jar app.jar` 就能跑起来。需要覆盖默认行为时，只在 `src/main/resources/application.yml` 中写偏离默认值的部分：

```yaml
server:
  port: 9090  # 只需声明偏离默认值的配置
```

也可通过命令行参数临时覆盖：`java -jar app.jar --server.port=9090`，优先级高于 `application.yml`。

### 出现背景

Spring Boot（2014）与微服务架构的兴起同期出现。2014 年 Martin Fowler 发表了微服务架构的奠基性文章，微服务要求每个服务**独立部署、快速启动、进程隔离**。传统的 WAR 包 + 外部 Tomcat 的部署方式与这一需求存在明显矛盾，Spring Boot 正是为了解决这一问题而生。

前后端分离（React 2013、Vue 2014）也在同期兴起，但它不是 Spring Boot 出现的直接驱动力——Spring MVC 本身早已能支持 RESTful API，Spring Boot 只是让这件事更方便做。

### Spring Boot 解决了三个问题

**1. XML 配置的复杂性**

传统 Spring 项目需要用大量 XML 配置 Spring MVC、数据库连接池、事务管理、安全等模块。Spring Boot 通过自动配置和 Starter 依赖，将这些配置降到近乎为零。

**2. WAR 包 + 外部 Tomcat 的部署复杂性**

传统方式需要先在服务器上安装、配置 Tomcat，再把 WAR 包部署进去。Spring Boot 把 Tomcat 内嵌进 JAR，`java -jar app.jar` 一条命令启动一个独立进程，符合微服务"每个服务独立运行"的要求。

值得注意的是，Tomcat + WAR 包同样可以跑 RESTful API——WAR 包里的 `DispatcherServlet` 既能处理返回 JSP 的请求，也能处理返回 JSON 的请求，Tomcat 不关心你返回什么内容。Spring Boot 的内嵌方式只是把部署流程简化了，底层机制没有改变。

`java -jar app.jar` 启动时，`main()` 方法里 Spring Boot 以编程方式启动内嵌 Tomcat（等价于 `new Tomcat().start()`），把 `DispatcherServlet` 注册进去，Tomcat 开始监听端口，Web 服务就绪。本质上 Tomcat 还是那个 Tomcat，只是从"独立进程 + 外部部署"变成了"作为一个库被你的进程调用"。

|             | 传统 WAR + 外部 Tomcat   | Spring Boot JAR     |
| ----------- | ------------------------ | ------------------- |
| Tomcat 进程 | 独立进程，先于应用存在   | 内嵌在应用进程里    |
| 部署        | 把 WAR 拷贝到 `webapps/` | `java -jar app.jar` |
| 生命周期    | Tomcat 管理应用          | 应用管理 Tomcat     |
| 多应用共享  | 一个 Tomcat 可跑多个 WAR | 每个应用独立进程    |

**3. Tomcat 配置的独立管理问题**

传统部署中 Tomcat 有自己独立的一套配置文件（`server.xml`、`context.xml` 等），与应用代码分开管理，容易出现环境差异问题。Spring Boot 将 Tomcat 的配置（端口、线程池等）统一纳入 `application.yml`，配置即代码，跟着项目走。

### 主要特性

- **自动配置（Auto-configuration）**：根据 classpath 中的依赖自动配置 Spring Bean，无需手写 XML 或 `@Configuration` 类。
- **起步依赖（Starter）**：一组预定义的 Maven/Gradle 依赖集合，例如 `spring-boot-starter-web` 会自动引入 Spring MVC、Tomcat、Jackson 等全套依赖。
- **内嵌服务器**：内置 Tomcat / Jetty / Undertow，打包为可执行 JAR，直接 `java -jar app.jar` 运行，无需单独部署到 Tomcat。切换只需在 `pom.xml` 排除默认 Tomcat、引入目标服务器的 Starter。
- **Actuator**：内置生产级监控端点（health check、metrics 等）。
- **Spring Initializr**：通过 [start.spring.io](https://start.spring.io) 快速生成项目骨架。

---

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

## Auto-configuration（自动配置）

Auto-configuration 是 Spring Boot 的核心机制，负责**根据 classpath 中存在的依赖，自动向 Spring 容器注册所需的 Bean**，无需手写任何 `@Configuration` 类或 XML。

### 为什么需要 Auto-configuration

Spring Boot 启动时，`@SpringBootApplication` 默认只会对**应用自己的包**（及其子包）做 Component Scan，扫描其中带有 `@Component`、`@Service` 等注解的类并注册为 Bean。

第三方库（如 `spring-boot-starter-data-redis`）的包名是 `org.springframework.data.redis.*`，不在应用的扫描路径里，Component Scan 根本扫不到。但这些库又需要把 `RedisTemplate`、`LettuceConnectionFactory` 等 Bean 注入到你的容器中才能正常工作。

Auto-configuration 就是为解决这个问题而设计的：第三方库在自己的 JAR 包里放一个声明文件，Spring Boot 启动时主动读取这些声明文件，绕过 Component Scan，把对应的 Bean 注册进容器。

两条机制是完全独立的路径：

| 机制               | 扫描范围                                              | 触发方式                                                     |
| ------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| Component Scan     | 应用自己的包（`@SpringBootApplication` 所在包及子包） | 扫描类上的 `@Component` 等注解                               |
| Auto-configuration | 所有 JAR 包                                           | 读取 `META-INF/spring/...AutoConfiguration.imports` 声明文件 |

### 工作原理

每个 Spring Boot Starter（或任何带有自动配置的库）都会在 JAR 包的 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 文件中声明自己的自动配置类：

```
# spring-boot-autoconfigure JAR 中的声明（简化示意）
org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration
org.springframework.boot.autoconfigure.data.jpa.JpaRepositoriesAutoConfiguration
org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
...
```

Spring Boot 启动时会扫描所有 JAR 包中的这份列表，加载每一个自动配置类。

### @ConditionalOn* 条件注解

自动配置类里大量使用**条件注解**，只有条件满足时才真正注册 Bean，避免乱注入：

| 注解                                              | 含义                                                       |
| ------------------------------------------------- | ---------------------------------------------------------- |
| `@ConditionalOnClass(Xxx.class)`                  | classpath 中存在该类时生效（即引入了对应依赖）             |
| `@ConditionalOnMissingBean(Xxx.class)`            | 容器中**没有**该类型 Bean 时生效（用户没有自定义则用默认） |
| `@ConditionalOnProperty("spring.datasource.url")` | 配置文件中存在该属性时生效                                 |
| `@ConditionalOnWebApplication`                    | 当前是 Web 应用时生效                                      |

以 `DataSourceAutoConfiguration` 为例，它的逻辑大致是：

```java
@AutoConfiguration
@ConditionalOnClass(DataSource.class)           // 有 JDBC 驱动才生效
@ConditionalOnMissingBean(DataSource.class)     // 用户没有自定义 DataSource 才生效
@EnableConfigurationProperties(DataSourceProperties.class)  // 绑定 application.yml 中的配置
public class DataSourceAutoConfiguration {
    @Bean
    public DataSource dataSource(DataSourceProperties props) {
        return props.initializeDataSourceBuilder().build();
    }
}
```

这就是为什么：加了 `spring-boot-starter-data-jpa` + 配置了 `spring.datasource.url`，连接池就自动出现了；如果自己 `@Bean` 定义了 `DataSource`，自动配置就自动退让。

### 覆盖自动配置

**方式一：自定义同类型 Bean**

自动配置类上的 `@ConditionalOnMissingBean` 保证：只要你自己定义了同类型的 Bean，自动配置就不会再注册一个。

```java
@Configuration
public class MyConfig {
    @Bean
    public DataSource dataSource() {
        // 自定义连接池，自动配置的 DataSource 不会再注册
        return new HikariDataSource(...);
    }
}
```

**方式二：通过 application.yml 调整属性**

自动配置类通常都绑定了一组 `@ConfigurationProperties`，覆盖属性即可调整行为，无需替换整个 Bean：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost/mydb
    hikari:
      maximum-pool-size: 20
```

**方式三：排除某个自动配置类**

```java
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class MyApp { ... }
```

### 查看哪些自动配置生效

Actuator 的 `/actuator/conditions` 端点（或启动时加 `--debug`）会输出 **Conditions Evaluation Report**，列出每个自动配置类是否生效及原因，是排查配置问题的利器。

```
=========================
AUTO-CONFIGURATION REPORT
=========================

Positive matches:
  DataSourceAutoConfiguration - @ConditionalOnClass found: DataSource

Negative matches:
  MongoAutoConfiguration - @ConditionalOnClass did not find: MongoClient
```

---

## 启动应用

Spring Boot 应用打包后是一个可执行 JAR，通过 `java -jar` 启动：

```bash
# 基本启动
java -jar app.jar

# 指定端口（覆盖 application.yml 中的配置）
java -jar app.jar --server.port=9090

# 指定激活的 profile（环境）
java -jar app.jar --spring.profiles.active=prod

# 同时指定多个参数
java -jar app.jar --spring.profiles.active=prod --server.port=9090

# 传 JVM 参数（放在 -jar 前面）
java -Xmx512m -Xms256m -jar app.jar
```

命令行参数的优先级**高于** `application.yml`，常用于在生产环境覆盖配置，而不用修改打包好的 JAR。

### Tomcat 配置示例

以前需要修改 Tomcat 的 `server.xml`，现在统一在 `application.yml` 中管理：

```yaml
server:
  port: 8080
  tomcat:
    threads:
      max: 200
    connection-timeout: 5000ms
```

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

### @RequestMapping 及简化注解

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

### @Validated 与 @Valid：请求参数校验

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

### 结论

- Spring MVC 可以实现前后端分离，Java 只负责 RESTful API，与 JSP 无关
- Spring Boot 不是实现 RESTful API 的必要条件，它只是**消除了配置负担**，让同样的事情做起来更快
- 用 Spring Boot 写 REST API 和用传统 Spring MVC 写，**业务代码几乎一模一样**，差异只在项目搭建和配置阶段

---

## Spring 注解体系

Spring 注解按职责可分为以下几类：

| 类型                       | 说明                         | 典型例子                                                                       |
| -------------------------- | ---------------------------- | ------------------------------------------------------------------------------ |
| **标记注解**（Stereotype） | 声明类的角色，让容器扫描注册 | `@Component` `@Service` `@Repository` `@Controller`                            |
| **配置注解**               | 定义 Bean、导入配置          | `@Configuration` `@Bean` `@Import` `@ComponentScan`                            |
| **依赖注入注解**           | 声明依赖关系，让容器自动装配 | `@Autowired` `@Qualifier` `@Value` `@Resource`                                 |
| **Web 注解**               | 定义 HTTP 路由和参数绑定     | `@RequestMapping` `@GetMapping` `@RequestParam` `@PathVariable` `@RequestBody` |
| **AOP 注解**               | 在方法执行时插入额外逻辑     | `@Aspect` `@Before` `@Around` `@Transactional` `@Cacheable` `@PreAuthorize`    |
| **校验注解**               | 声明参数约束规则             | `@NotNull` `@Size` `@Email` `@Valid` `@Validated`                              |
| **条件注解**               | 按条件决定是否加载 Bean      | `@ConditionalOnClass` `@ConditionalOnProperty` `@Profile`                      |
| **生命周期注解**           | 控制 Bean 的初始化和销毁     | `@PostConstruct` `@PreDestroy` `@Scope`                                        |
| **调度注解**               | 定时任务                     | `@Scheduled` `@EnableScheduling`                                               |
| **测试注解**               | 测试环境专用                 | `@SpringBootTest` `@MockBean`                                                  |

AOP 注解与其他类型的本质区别：AOP 注解会在**运行时**动态拦截方法，其余大多数注解只在**启动时**被容器读取一次用于注册或配置。判断一个注解是否属于 AOP：**它是否会在方法执行时悄悄做点额外的事？**

- `@Transactional` → 会，方法执行前开事务、执行后提交 → **AOP**
- `@RestController` → 不会，只是让 Spring 认识这个类 → **标记注解，不是 AOP**

---

## Spring WebFlux：响应式 Web 框架

### 解决的问题

传统 Spring MVC 基于 Servlet 模型，每个请求占用一个线程，调用数据库或外部 API 时线程阻塞等待：

```
请求进来 → 分配线程 → 调用数据库（等待 100ms，线程阻塞）→ 调用外部 API（等待 200ms，线程阻塞）→ 返回
```

Tomcat 默认线程池约 200 个线程，高并发下线程池耗尽，后续请求排队。

Spring WebFlux（Spring 5，2017）引入响应式编程模型，底层使用 **Netty**（非 Servlet 容器），少量线程处理大量并发：

```
请求进来 → 少量线程（CPU 核数）→ 发起数据库查询（注册回调，线程立刻去处理其他请求）→ 数据返回时触发回调继续处理
```

### 编程模型

WebFlux 使用 **Reactor** 库的 `Mono<T>`（0或1个异步结果）和 `Flux<T>`（0到N个异步结果）：

```java
// Spring MVC（同步阻塞）
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userService.findById(id);  // 阻塞等待数据库
}

// Spring WebFlux（异步非阻塞）
@GetMapping("/users/{id}")
public Mono<User> getUser(@PathVariable Long id) {
    return userService.findById(id);  // 返回"将来会有值"的容器
}
```

### WebFlux 的局限

- 编程模型与传统命令式完全不同，调试困难，学习成本高
- 需要支持响应式的驱动（R2DBC 替代 JDBC），不是所有库都有响应式版本
- **Java 21 虚拟线程的出现大幅削弱了 WebFlux 的核心优势**

---

## Java 21 虚拟线程：更简单的高并发方案

### 什么是虚拟线程

Java 21（2023）正式引入虚拟线程（Project Loom），由 JVM 管理，数量可达百万级。阻塞时 JVM 自动挂起虚拟线程、释放底层 OS 线程去处理其他任务，数据返回后再恢复执行——**对应用代码完全透明**。

这与 Go 语言的协程（goroutine）是同一思想：用户态轻量级并发，阻塞时不占用 OS 线程。Go 从 2009 年就原生支持，Java 晚了约 14 年。

|                | Java 虚拟线程        | Go 协程（goroutine） |
| -------------- | -------------------- | -------------------- |
| 出现时间       | 2023（Java 21）      | 2009（Go 1.0）       |
| 调度器         | JVM 内置             | Go runtime           |
| 初始栈内存     | 约 1KB               | 约 2KB               |
| 与现有代码兼容 | ✅ 完全兼容，API 不变 | —                    |

### 对应用层完全透明

虚拟线程的复杂性封装在 JVM 内部，应用层代码写法与传统线程一模一样：

```java
// 普通线程池
ExecutorService executor = Executors.newFixedThreadPool(200);

// 换成虚拟线程，代码完全不变，只改这一行
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

executor.submit(() -> {
    User user = db.findById(id);  // 看起来阻塞，JVM 内部自动挂起虚拟线程
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

### 虚拟线程 vs WebFlux

对于绝大多数业务系统，**Spring MVC + Java 21 虚拟线程**是更好的选择：

|          | Spring MVC + 虚拟线程 | Spring WebFlux       |
| -------- | --------------------- | -------------------- |
| 代码改动 | 零改动，一行配置      | 需要重写为响应式风格 |
| 调试体验 | 清晰可读的堆栈        | 复杂的响应式链路     |
| 库兼容性 | 所有现有库直接可用    | 需要响应式版本的驱动 |
| 适合场景 | 普通业务系统          | 流式推送、背压控制   |

WebFlux 仍有价值的场景：SSE 实时推送、需要背压控制（消费者告知生产者降速）的流式处理。

**实际建议：**

- 新项目：Spring MVC + Java 21 虚拟线程，首选
- 已有 MVC 项目：升级 Java 21，开启虚拟线程，低成本高收益
- 已有 WebFlux 项目：继续用，没有必要改回 MVC
- 需要流式推送/背压：WebFlux 仍有价值

---

## Spring Boot 3.x 关键特性与约束

Spring Boot 3.0（2022 年底发布）底层依赖 Spring Framework 6.x。

Spring Boot 与 Spring Framework 版本的对应关系：

| Spring Boot   | Spring Framework |
| ------------- | ---------------- |
| 3.0.x         | 6.0.x            |
| 3.2.x         | 6.1.x            |
| 3.3.x / 3.4.x | 6.1.x / 6.2.x    |
| **3.5.x**     | **6.2.x**        |

### 1. Java 版本要求

Spring Boot 3.x **最低要求 Java 17**。

### 2. javax → jakarta 命名空间迁移（最大变更）

Java EE 已捐赠给 Eclipse 基金会，品牌更名为 Jakarta EE，所有包名从 `javax.*` 改为 `jakarta.*`。这是**代码层面影响最广**的变更，几乎所有用到 Servlet、JPA、Bean Validation 的代码都要修改：

| 旧包名（javax）       | 新包名（jakarta）       |
| --------------------- | ----------------------- |
| `javax.servlet.*`     | `jakarta.servlet.*`     |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*`  | `jakarta.validation.*`  |
| `javax.transaction.*` | `jakarta.transaction.*` |
| `javax.annotation.*`  | `jakarta.annotation.*`  |

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.persistence.Entity;
```

### 3. Spring Security 6.x：WebSecurityConfigurerAdapter 彻底移除

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

| 特性                | 旧链式写法                 | Lambda DSL            |
| ------------------- | -------------------------- | --------------------- |
| 结构                | 扁平链式，靠 `.and()` 拼接 | 嵌套 Lambda，结构清晰 |
| 可读性              | 需要靠缩进约定             | 作用域边界明确        |
| IDE 支持            | 容易混淆配置层级           | 类型推断更准确        |
| Spring Security 6.x | 已废弃                     | **唯一支持的写法**    |

Spring Security 6.x 移除了旧的链式 API（如 `authorizeRequests()`、`.and()`），只保留 Lambda DSL，因为它更清晰地表达了每个配置块的边界，减少配置错误。

### 4. Hibernate 6.x

ORM 层升级到 Hibernate 6，部分 HQL/JPQL 语法更严格，一些隐式类型转换不再支持，自定义类型映射 API 有变化。

### 5. AOT 与 GraalVM Native Image

Spring Boot 3.x 正式支持 GraalVM Native Image 编译，可以将应用编译为原生可执行文件，启动时间从秒级降到毫秒级，但对反射、动态代理等有额外约束。

---

## 参考

- [Spring Boot 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)
- [Spring MVC 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html)
