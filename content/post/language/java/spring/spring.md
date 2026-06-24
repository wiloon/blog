---
title: Spring
author: "-"
date: 2026-06-24T07:10:34+08:00
lastmod: 2026-06-24T09:37:13+08:00
url: spring
categories:
  - java
tags:
  - java
  - spring
  - remix
  - AI-assisted
---

Spring 通常指 **Spring Framework**——一个以 IoC 容器为核心的 Java 企业应用基础框架。它**不是**专门为 Web 而生的；Web 处理只是其众多模块之一。要理解 Spring MVC、Spring Boot 在生态里的位置，需要先弄清 Spring Framework 本身解决什么问题、各模块如何分工，以及它在 J2EE 时代是如何演进来的。

## Spring Framework 是什么

Spring Framework 提供：

- **IoC 容器**：创建对象、装配依赖、管理生命周期（详见 [Spring IoC，依赖注入](./spring-ioc.md)）
- **AOP**：横切关注点（日志、事务、安全等）与业务代码分离（详见 [aop](../aop.md)）
- **数据访问与事务**：JDBC 抽象、`@Transactional`、与 Hibernate / JPA / MyBatis 集成
- **Web 层**：Spring MVC（详见 [Spring MVC](./spring-mvc.md)）
- **集成能力**：消息、邮件、调度任务等

典型分层关系：

```text
Spring Framework（基础框架）
  ├── Core（IoC、AOP、事件、资源抽象）
  ├── Data Access（JDBC、ORM 集成、事务）
  ├── Spring MVC（Web 层：DispatcherServlet、Controller）
  ├── Integration（JMS、邮件等）
  └── 以及 Security、Batch 等扩展项目

Spring Boot（2014，构建在 Spring Framework 之上）
  └── 自动配置 + Starter，简化上述模块的装配与部署（详见 [Spring Boot](./spring-boot.md)）
```

## Spring 与 Spring MVC 的关系

**Spring MVC 是 Spring Framework 里的 Web 模块，不是与 Spring 平级的独立框架。**

| 层次 | 职责 |
| ---- | ---- |
| Spring Core | 容器、依赖注入、AOP、事务、数据访问 |
| Spring MVC | HTTP 请求路由、`DispatcherServlet`、Controller、视图 / JSON 响应 |
| Servlet 容器（Tomcat 等） | 监听端口、Servlet 规范、把请求交给 `DispatcherServlet` |

一条典型 Web 请求的路径：

```text
HTTP 请求
  → Tomcat
  → DispatcherServlet（Spring MVC）
  → @Controller 方法
  → @Service / @Repository（由 Spring 容器管理的 Bean）
  → 数据库 / 消息队列 / 外部服务
```

因此：**Spring MVC 管「怎么接 HTTP、怎么映射到处理方法」；Spring Core 管「业务对象怎么创建、依赖怎么注入、事务怎么做」。** 两者常一起出现，但职责不同。

## 没有 Spring MVC 时，Spring 能做什么

Spring 本质是 **IoC 容器 + 企业应用基础设施**，不依赖 Web。**开发命令行工具完全可以只用 Spring（或 Spring Boot），不需要 Spring MVC。**

| 能力 | 典型场景 |
| ---- | ---- |
| IoC / DI | 管理 Service、Repository、工具类；便于测试与替换实现 |
| AOP | 日志、权限、监控、统一异常处理 |
| 声明式事务 | `@Transactional` + JDBC / JPA / MyBatis |
| JDBC 抽象 | `JdbcTemplate`，减少样板代码 |
| 命令行 / 批处理 | `main()` 启动容器，执行完退出；无 HTTP、无 Tomcat |
| 定时任务 | `@Scheduled`（也可嵌在长期运行的 CLI 守护进程里） |
| 消息 / 集成 | JMS、邮件等 |

Spring Boot 中若只引入 `spring-boot-starter`（或 `spring-boot-starter-data-jpa` 等）而**不**引入 `spring-boot-starter-web`，就没有 Spring MVC，但容器、事务、数据访问仍可正常工作。

命令行工具的典型写法：`main()` 里启动非 Web 的 `ApplicationContext`，从容器取出 Bean 执行业务逻辑，然后进程退出。

```java
@SpringBootApplication
public class ExportCliApplication implements CommandLineRunner {

    private final OrderExportService exportService;

    public ExportCliApplication(OrderExportService exportService) {
        this.exportService = exportService;
    }

    public static void main(String[] args) {
        SpringApplication.run(ExportCliApplication.class, args);
    }

    @Override
    public void run(String... args) {
        exportService.exportToCsv(args[0]);
    }
}
```

上例依赖 `spring-boot-starter`（不含 web），`OrderExportService` 仍可由 Spring 注入，数据库访问、`@Transactional` 等与 Web 项目里用法相同——只是没有 `DispatcherServlet`，也不监听 HTTP 端口。

传统 Spring（无 Boot）也一样：用 `AnnotationConfigApplicationContext` 加载配置类，取 Bean、调用方法、最后 `context.close()` 即可。

## 起源：不是为了 Web

### Rod Johnson 与 EJB 的替代方案

2002 年 Rod Johnson 出版 *Expert One-on-One J2EE Design and Development*，核心论点是：企业 Java 不必绑在重量级 **EJB** 上，用 **POJO + 轻量容器** 同样能完成业务，且更易开发、测试和部署。

当时 J2EE 的痛点包括：

1. **EJB 过重**：需要应用服务器、Home/Remote 接口、JNDI 查找，开发与部署成本高
2. **紧耦合**：业务类自己 `new` 依赖或从 JNDI 取资源，难以单元测试
3. **事务散落**：大量编程式 `begin` / `commit` / `rollback`
4. **JDBC 样板代码**：连接、Statement、异常与资源关闭重复编写

Spring 项目 2003 年启动，**2004 年 3 月发布 1.0**。首发能力以 **IoC 容器、AOP、JDBC 抽象、声明式事务、ORM 集成** 为主——解决的是 **整个企业应用的基础设施**，不是「缺一个 Web 框架」。

### Spring 1.x：几乎全是 XML

Spring 1.0 发布时 **[JDK 5](./jdk-5.md) 尚未正式发布**（正式版在 2004 年 9 月），框架基线为 **JDK 1.3 / 1.4**。这一时期的典型写法：

- Bean 定义与依赖注入：`applicationContext.xml` 里的 `<bean>`、`<property>`
- AOP、声明式事务：XML 或编程式 API
- Spring MVC：`MultiActionController`、继承 `AbstractController`，或 XML 映射 URL——**没有** `@RequestMapping`

所以：**Spring 早期并不是「用注解做配置」起家的**；IoC 与 AOP 先通过 XML 和工厂模式落地，与当时 Struts、Hibernate 等框架以 XML / 映射文件为主的风格一致。

### 与 JDK 5 注解的关系

[JDK 5 注解](./jdk-5.md)（JSR 175）在语言层提供 **注解类型**（`@interface`）、**保留策略**（`@Retention`）、**反射读取**（`AnnotatedElement`）等能力。Spring 后来广泛使用的 `@Autowired`、`@Controller` 等，**不是 JDK 内置注解**，而是 **Spring 用 `@interface` 自定义的元数据**；容器在启动时扫描、解析它们。前提是运行在 **JDK 5+** 上——没有语言级元数据与反射 API，框架只能继续依赖 XML。

| Spring 版本 | 大约时间 | 注解相关变化 |
| ---- | ---- | ---- |
| 1.x | 2004 起 | 以 XML 为主；不要求 JDK 5 |
| 2.0 | 2006-10 | 要求 Java 5；`@Transactional`、`@Required` 等 |
| 2.5 | 2007-11 | `@Autowired`、`@Component` / `@Service` / `@Repository`、`@Controller`、`@RequestMapping`；支持 JSR 250 的 `@Resource`、`@PostConstruct`、`@PreDestroy` |
| 3.0 | 2009 | `@Configuration` + `@Bean`（Java Config），进一步减少 XML |
| Boot 1.0 | 2014 | `@SpringBootApplication` 等组合注解，默认注解驱动 |

时间上有先后：**JDK 5 先提供注解基础设施（2004 GA）**，Spring 在 **2.0 / 2.5（2006–2007）** 才把注解做成主流配置方式；1.x 时代仍以 XML 为主。详见 [Java Annotation（注解）](../annotation.md)。

### Spring 与 Spring MVC 是否同时出现

**同属 Spring Framework 1.0，但角色不同：**

- Spring **从第一天起**就包含 Web/MVC 模块（基于 Servlet 的 `DispatcherServlet` 等）
- 同期 Web 层主流仍是 **Struts、JSF** 等；很多项目采用 **Struts（Web）+ Spring（Service 层与事务）** 的组合
- Spring 成名的首先是 **IoC + 轻量企业开发**，Spring MVC 是同一哲学在 Web 层的实现，并非 Spring 存在的唯一理由

## Web 层演变（MVC 框架侧）

以下梳理 Java Web **表示层** 的常见演进脉络，帮助理解 Spring MVC 在 Controller 设计上的取舍。内容部分提炼自早年 iteye 专栏（downpour，《SpringMVC 深度探险》）中对 MVC 形态的归纳，已按现代表述重写；外链图床不再保留。

### 两种表示层思路

B/S 应用本质是「请求—响应」。实现上长期存在两种侧重：

| 思路 | 代表 | 特点 |
| ---- | ---- | ---- |
| **MVC 模型** | Struts、Spring MVC | 以服务器端 Controller 为核心；页面多用原生 HTML Form；映射关系通过 URL + 配置（XML 或注解） |
| **组件 / 事件模型** | Tapestry、JSF | 扩展 HTML 标签与属性，页面组件与服务器端事件绑定；交互不总是「一个明文 URL 契约」 |

企业项目里 **MVC 模型** 长期占主导；Spring MVC 属于这一路线上的改良派。

### Controller 形态的演进

MVC 框架的发展，很大程度上是 **围绕 Controller 如何接收请求、返回响应** 不断重构的过程。可粗分为几代：

**1. Servlet（Param-Param）**

`service(ServletRequest req, ServletResponse resp)`：`void` 返回值，请求与响应都通过参数操作，是最底层的骨架。

**2. Struts 1.x（Param-Return，约 2000 年起）**

```java
public ActionForward execute(
    ActionMapping mapping, ActionForm form,
    HttpServletRequest request, HttpServletResponse response);
```

引入 `ActionForward` 作为返回值，框架参与响应跳转；仍保留 Servlet 请求/响应参数，并增加 `ActionForm` 承载表单数据。

**3. WebWork 2 / Struts 2（POJO 模式，2004–2005 合并为 Struts 2）**

Controller 不再直接依赖 `HttpServletRequest`；请求数据放到 Action **属性**上，配合 ThreadLocal 与拦截器，Action 更接近 POJO，便于单测。这是 Struts 2 一度流行的重要原因之一。

**4. Spring MVC（Param-Return 的改良）**

在 **不脱离 Servlet 编程模型** 的前提下持续改良，例如：

- 方法**参数**对应请求参数（或 `Model` 等），**返回值**表示视图或数据（`ModelAndView`、`String` 视图名、`@ResponseBody` 等）
- Spring 2.5+ 用 **注解**（`@RequestMapping` 等）替代大量 XML 映射
- Controller 本身是 Spring Bean，可直接 `@Autowired` Service

与 Struts 2 的「Action 属性 + 返回值字符串」相比，Spring MVC 更强调 **方法签名即契约**，并泛化参数与返回值类型，由框架统一转换。

### 与 Struts 2 的交替

2000 年代中后期，Struts 2 凭借 POJO Action 模型占据大量市场；2010 年代起 Spring MVC（及后来的 Spring Boot）份额上升。原因涉及架构、生态与社区，技术面上常见归纳包括：Spring MVC 更紧跟 **注解、REST、JSON** 等趋势；与 **Spring 容器一体化**（同一套 Bean、事务、AOP）；Struts 2 在配置统一、技术迭代节奏上相对滞后。框架各有适用场景，此处只作脉络说明，不作「谁取代谁」的绝对结论。

### MVC 演变小结

```text
Servlet（void + Request/Response 参数）
  → Struts 1（+ ActionForward 返回值）
  → Struts 2 / WebWork（POJO Action，属性承载请求）
  → Spring MVC（方法参数 + 返回值，注解映射，与 IoC 一体）
```

## Spring 生态时间线（简表）

| 时间 | 事件 |
| ---- | ---- |
| 2002 | Rod Johnson 出版 *Expert One-on-One J2EE*，提出轻量容器 + POJO |
| 2003 | Spring Framework 项目启动 |
| 2004.03 | Spring **1.0** 发布（Core、AOP、JDBC、ORM 集成、Spring MVC 等）；**以 XML 配置为主** |
| 2004.09 | **JDK 5** 正式发布（JSR 175 注解等）→ [JDK 5](../jdk-5.md) |
| 2004 | WebWork 2.1.7 等重要版本；Web 层 Struts 1 / 2、Spring MVC 并存 |
| 2006 | Spring **2.0**：要求 Java 5；`@Transactional` 等注解化配置 |
| 2007 | Spring **2.5**：`@Autowired`、`@RequestMapping`、`@Controller` 等 |
| 2009 | Spring 3.0 强化注解驱动与 REST 支持 |
| 2014 | **Spring Boot 1.0**；可执行 JAR、自动配置，降低 Spring 全家桶上手成本 |
| 2022 | Spring Boot 3.0 / Spring Framework 6，基线 **Java 17**、Jakarta EE 命名空间 |

## 常见误解对照

| 误解 | 实际情况 |
| ---- | -------- |
| Spring = Spring MVC | MVC 只是 Framework 中的一个模块 |
| Spring 专为 Web 而生 | 初衷是简化 J2EE/EJB 企业开发；Web 是能力之一 |
| Spring 1.x 就用注解配置 | 1.x 以 XML 为主；注解从 2.0 / 2.5 才成主流，且依赖 [JDK 5](../jdk-5.md) |
| `@Autowired` 等是 JDK 内置注解 | 是 Spring **自定义**注解，借助 JDK 5 的注解机制与反射读取 |
| 用了 Spring Boot 就不用 Spring MVC | Boot 的 Web Starter 底层仍是 Spring MVC（见 [Spring MVC](./spring-mvc.md)） |
| Spring 必须配 Tomcat | 非 Web 应用可无 Servlet 容器；Web 场景才需要 |
| 命令行工具不能用 Spring | 可以；不引入 `spring-boot-starter-web` 即可，见上文 §没有 Spring MVC 时 |

## 延伸阅读

| 主题 | 文章 |
| ---- | ---- |
| IoC / 依赖注入 | [Spring IoC，依赖注入](./spring-ioc.md) |
| HTTP 与 REST 实践 | [Spring MVC](./spring-mvc.md) |
| 自动配置与部署 | [Spring Boot](./spring-boot.md) |
| JDK 5 与注解语言特性 | [JDK 5](../jdk-5.md)、[Java Annotation（注解）](../annotation.md) |
| AOP 与版本演进 | [aop](../aop.md) |
| 原生镜像 / AOT | [Spring AOT](./spring-aot.md) |

## 小结

| 问题 | 要点 |
| ---- | ---- |
| Spring 与 Spring MVC | MVC 是 Framework 的 Web 模块；Core 管容器、事务、数据访问 |
| 去掉 MVC 还能做什么 | CLI、批处理、定时任务、消息集成等；IoC 与 Web 无关 |
| Spring 为何诞生 | 简化 EJB 时代的企业 Java（IoC、AOP、声明式事务、JDBC 集成），不是缺 Web 框架 |
| 与 MVC 是否同时出现 | 1.0 即含 MVC 模块，但成名靠 IoC；常见组合是 Struts + Spring |
| 早期是否用注解 | 1.x 几乎全 XML；2.0 / 2.5 才注解化，且依赖 JDK 5 |
| JDK 5 与 Spring 注解 | JDK 5 提供语言机制；Spring 注解是框架自定义，靠反射扫描 |
