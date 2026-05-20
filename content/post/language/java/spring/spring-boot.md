---
title: Spring Boot
author: wiloon
date: 2026-05-11T14:24:31+08:00
lastmod: 2026-05-20T11:18:20+08:00
url: spring-boot
aliases:
  - /spring/boot/
tags:
  - java
  - spring
  - spring boot
  - maven
  - gradle
  - restful
  - remix
  - AI-assisted
categories:
  - java
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
|-------------|--------------------------|---------------------|
| Tomcat 进程 | 独立进程，先于应用存在    | 内嵌在应用进程里    |
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

## Maven：`spring-boot-starter-parent`

在 Maven 工程里把 `spring-boot-starter-parent` 设为 `<parent>` 后，子 POM 会继承一整套默认约定，减少样板配置。常见效果包括：

- 统一的 Java 发行版、源码编码（如 UTF-8）与常用插件的默认行为  
- **依赖管理（BOM）**：常用依赖的兼容版本由 `spring-boot-dependencies` 对齐，声明 `spring-boot-starter-*` 时通常不必再写 `<version>`  
- 打包、`resources` 过滤等默认集成  

若需覆盖某个托管依赖的版本，可在当前 POM 的 `<properties>` 中声明官方文档给出的属性名，或在 `<dependencyManagement>` 里显式指定版本。

老项目从传统 Spring 迁到 Boot 时，偶尔会碰到 Maven 资源过滤使用 `@...@` 作为占位符、与 Spring 的 `${…}` 习惯不一致的情况，可通过 Maven 的 `resource.delimiter` 等属性按需调整。

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.5.0</version>
  <relativePath/>
</parent>

<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
</dependencies>
```

---

## `@SpringBootApplication`

`@SpringBootApplication` 是一个**组合注解**，通常标注在应用的主类（`main` 方法所在类）上，是启动 Spring Boot 应用的入口。它等价于同时声明了以下三个注解：

```java
@SpringBootConfiguration   // 等价于 @Configuration，声明该类是一个配置类
@EnableAutoConfiguration   // 开启自动配置机制
@ComponentScan             // 扫描当前包及子包下的 Spring 组件
public class MyApp { ... }
```

典型用法：

```java
@SpringBootApplication
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

### 三个组合注解的职责

**`@SpringBootConfiguration`**

继承自 `@Configuration`，表示该类是一个 Spring 配置类，其中可以用 `@Bean` 定义 Bean。与 `@Configuration` 的区别在于前者还做了一个约束：整个应用中只应存在一个 `@SpringBootConfiguration`（即主类唯一）。

**`@EnableAutoConfiguration`**

开启 [Auto-configuration](#auto-configuration自动配置) 机制。Spring Boot 启动时会扫描所有 JAR 包中的 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 声明文件，按需自动注册第三方库的 Bean。

**`@ComponentScan`**

默认扫描**主类所在包及其所有子包**，将带有 `@Component`、`@Service`、`@Repository`、`@Controller` 等注解的类注册为 Spring Bean。

这也是为什么通常把主类放在项目的**根包**下（如 `com.example.myapp.MyApp`），确保所有业务代码都能被扫描到。如果某个类放在主类包之外，就不会被自动发现。

### 常用属性

```java
// 排除某个自动配置类（不想让它生效时）
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class MyApp { ... }

// 自定义扫描范围（不用默认包扫描时）
@SpringBootApplication(scanBasePackages = "com.example.service")
public class MyApp { ... }
```

---

<!-- ## Auto-configuration（自动配置） -->

Auto-configuration 是 Spring Boot 的核心机制，负责**根据 classpath 中存在的依赖，自动向 Spring 容器注册所需的 Bean**，无需手写任何 `@Configuration` 类或 XML。

### 为什么需要 Auto-configuration

Spring Boot 启动时，`@SpringBootApplication` 默认只会对**应用自己的包**（及其子包）做 Component Scan，扫描其中带有 `@Component`、`@Service` 等注解的类并注册为 Bean。

第三方库（如 `spring-boot-starter-data-redis`）的包名是 `org.springframework.data.redis.*`，不在应用的扫描路径里，Component Scan 根本扫不到。但这些库又需要把 `RedisTemplate`、`LettuceConnectionFactory` 等 Bean 注入到你的容器中才能正常工作。

Auto-configuration 就是为解决这个问题而设计的：第三方库在自己的 JAR 包里放一个声明文件，Spring Boot 启动时主动读取这些声明文件，绕过 Component Scan，把对应的 Bean 注册进容器。

两条机制是完全独立的路径：

| 机制               | 扫描范围                                            | 触发方式                                                     |
|--------------------|-----------------------------------------------------|--------------------------------------------------------------|
| Component Scan     | 应用自己的包（`@SpringBootApplication` 所在包及子包） | 扫描类上的 `@Component` 等注解                               |
| Auto-configuration | 所有 JAR 包                                         | 读取 `META-INF/spring/...AutoConfiguration.imports` 声明文件 |

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

| 注解                                              | 含义                                                     |
|---------------------------------------------------|----------------------------------------------------------|
| `@ConditionalOnClass(Xxx.class)`                  | classpath 中存在该类时生效（即引入了对应依赖）             |
| `@ConditionalOnMissingBean(Xxx.class)`            | 容器中**没有**该类型 Bean 时生效（用户没有自定义则用默认） |
| `@ConditionalOnProperty("spring.datasource.url")` | 配置文件中存在该属性时生效                               |
| `@ConditionalOnWebApplication`                    | 当前是 Web 应用时生效                                    |

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

### Gradle 运行

使用 Gradle 与 Spring Boot 插件时，可在开发阶段直接启动应用：

```bash
./gradlew bootRun
```

---

## 应用启动完成后执行逻辑

若要在 **Spring 应用上下文已就绪** 之后执行一段初始化代码，常见做法如下。多个 Bean 可同时实现同一类接口，使用 `@Order` 或 `Ordered` 控制顺序。

### `ApplicationRunner` 与 `CommandLineRunner`

二者都会在 `SpringApplication` 启动流程末尾被调用。需要结构化解析命令行参数（如 `key=value` 形式）时，优先使用 `ApplicationRunner`（入参为 `ApplicationArguments`）；只关心原始字符串数组时用 `CommandLineRunner` 即可。

```java
@Component
@Order(1)
public class SeedDataRunner implements ApplicationRunner {
    @Override
    public void run(ApplicationArguments args) {
        // 启动后逻辑
    }
}

@Component
@Order(2)
public class BannerRunner implements CommandLineRunner {
    @Override
    public void run(String... args) {
        // 启动后逻辑
    }
}
```

### `@PostConstruct`

在某个 Spring Bean 完成依赖注入之后、对外使用前执行，适合该 Bean 自身的轻量初始化。**不要**在 `static` 方法上使用 `@PostConstruct`（规范要求实例方法）。

```java
@Component
public class CacheWarmer {

    @PostConstruct
    void warmUp() {
        // ...
    }
}
```

### `ServletContextAware` 与 `ServletContextListener`

仅在 **基于 Servlet 的 Web 应用** 中有意义：前者在 Bean 属性填充后注入 `ServletContext`；后者监听 Web 应用启动与销毁。在 Spring Boot 中注册 `ServletContextListener` 往往需要 `@ServletComponentScan`、`ServletListenerRegistrationBean` 或容器相关配置配合，具体写法随场景选择。

### 静态代码块

`static { ... }` 在类加载阶段执行，时机早于 Spring 依赖注入，**不适合**编写依赖容器中其他 Bean 的逻辑。

---

## Spring 注解体系

Spring 注解按职责可分为以下几类：

| 类型                     | 说明                        | 典型例子                                                                       |
|--------------------------|-----------------------------|--------------------------------------------------------------------------------|
| **标记注解**（Stereotype） | 声明类的角色，让容器扫描注册 | `@Component` `@Service` `@Repository` `@Controller`                            |
| **配置注解**             | 定义 Bean、导入配置          | `@Configuration` `@Bean` `@Import` `@ComponentScan`                            |
| **依赖注入注解**         | 声明依赖关系，让容器自动装配 | `@Autowired` `@Qualifier` `@Value` `@Resource`                                 |
| **Web 注解**             | 定义 HTTP 路由和参数绑定    | `@RequestMapping` `@GetMapping` `@RequestParam` `@PathVariable` `@RequestBody` |
| **AOP 注解**             | 在方法执行时插入额外逻辑    | `@Aspect` `@Before` `@Around` `@Transactional` `@Cacheable` `@PreAuthorize`    |
| **校验注解**             | 声明参数约束规则            | `@NotNull` `@Size` `@Email` `@Valid` `@Validated`                              |
| **条件注解**             | 按条件决定是否加载 Bean     | `@ConditionalOnClass` `@ConditionalOnProperty` `@Profile`                      |
| **生命周期注解**         | 控制 Bean 的初始化和销毁    | `@PostConstruct` `@PreDestroy` `@Scope`                                        |
| **调度注解**             | 定时任务                    | `@Scheduled` `@EnableScheduling`                                               |
| **测试注解**             | 测试环境专用                | `@SpringBootTest` `@MockBean`                                                  |

AOP 注解与其他类型的本质区别：AOP 注解会在**运行时**动态拦截方法，其余大多数注解只在**启动时**被容器读取一次用于注册或配置。判断一个注解是否属于 AOP：**它是否会在方法执行时悄悄做点额外的事？**

- `@Transactional` → 会，方法执行前开事务、执行后提交 → **AOP**
- `@RestController` → 不会，只是让 Spring 认识这个类 → **标记注解，不是 AOP**

---

## 依赖注入方式

Spring 支持三种注入方式：构造器注入、Setter 注入和字段注入。

| 注入方式    | 写法                                  | Spring 官方推荐  |
|-------------|-------------------------------------|-----------------|
| 构造器注入  | 通过构造函数参数                        | ✅ 推荐          |
| Setter 注入 | 通过 `setXxx()` 方法 + `@Autowired`   | 可选依赖时使用     |
| 字段注入    | 字段上直接 `@Autowired`                | ❌ 不推荐        |

### 构造器注入（Constructor Injection）

构造器注入是 **Spring 官方推荐的首选方式**：通过构造函数参数声明依赖，由 Spring 容器在实例化 Bean 时把依赖传入。

```java
@Service
public class OrderService {

    private final UserRepository userRepository;
    private final PaymentService paymentService;

    // Spring 自动识别并注入，不需要 @Autowired（Spring 4.3+，只有一个构造器时可省略）
    public OrderService(UserRepository userRepository, PaymentService paymentService) {
        this.userRepository = userRepository;
        this.paymentService = paymentService;
    }
}
```

**为什么推荐构造器注入**

**1. 依赖不可变（`final` 字段）与不可变设计**

构造器注入允许将依赖字段声明为 `private final`：对象在构造完成后，其协作对象（Repository、Service 等）的引用不能再被替换。这属于 **不可变设计（immutable design）** 在依赖层面的应用——不是说整个 Bean 的所有状态都不能变，而是 **「必需的协作对象在创建时就固定下来」**。

| 注入方式    | 依赖字段能否 `final` | 含义                                        |
|-------------|----------------------|---------------------------------------------|
| 构造器注入  | ✅ 可以               | 创建后依赖引用不可变，对象处于「完整可用」状态 |
| 字段注入    | ❌ 不行               | `@Autowired` 在对象构造之后才赋值           |
| Setter 注入 | ❌ 通常不行           | 依赖可被再次 `set`，适合可选依赖             |

字段注入和 Setter 注入做不到 `final` 依赖，因为赋值发生在 `new` 之后、容器装配阶段。

**2. 依赖完整性保证**

构造器参数是必须提供的，如果依赖没有注册到容器，启动时就会立刻报错，而不是等到第一次调用某个方法时才出现 `NullPointerException`。字段注入在启动时不会暴露缺失的依赖。

**3. 可测试性更好**

构造器注入的类可以在不启动 Spring 容器的情况下直接 `new` 出来做单元测试：

```java
// 单元测试：直接 new，不需要 @SpringBootTest
@Test
void should_create_order() {
    UserRepository mockRepo = mock(UserRepository.class);
    PaymentService mockPayment = mock(PaymentService.class);

    OrderService service = new OrderService(mockRepo, mockPayment);
    // ... 测试逻辑
}
```

字段注入的类只能通过反射（`ReflectionTestUtils.setField`）或启动完整容器来注入依赖，测试更繁琐。

**4. 循环依赖的早期发现**

如果两个类互相依赖（A 依赖 B，B 又依赖 A），构造器注入会在启动时抛出 `BeanCurrentlyInCreationException`，强制开发者解决设计问题。字段注入在某些情况下会"成功"（Spring 通过三级缓存处理），掩盖了架构问题。

**Lombok 简化写法**

引入 Lombok 后，`@RequiredArgsConstructor` 会自动为所有 `final` 字段生成构造函数，消除样板代码：

```java
@Service
@RequiredArgsConstructor   // Lombok 自动生成包含 final 字段的构造器
public class OrderService {

    private final UserRepository userRepository;
    private final PaymentService paymentService;

    // 不需要手写构造函数
}
```

### Setter 注入

适合**可选依赖**：该依赖不存在时 Bean 仍然可以正常工作。

```java
@Service
public class NotificationService {

    private EmailClient emailClient;

    @Autowired(required = false)   // required = false：找不到时不报错
    public void setEmailClient(EmailClient emailClient) {
        this.emailClient = emailClient;
    }
}
```

### 字段注入（不推荐）

```java
@Service
public class OrderService {

    @Autowired
    private UserRepository userRepository;  // 字段注入
}
```

看起来最简洁，但有以下缺点：

- 字段无法声明为 `final`，依赖可以在任何时刻被替换
- 依赖缺失不会在启动时暴露
- 脱离 Spring 容器无法直接实例化，单元测试需要借助反射
- IDE 通常会给出 "Field injection is not recommended" 警告

### 字段注入：不推荐，但 API 并未废弃

常说「字段 `@Autowired` 要淘汰」，需要区分两层含义：

| 层面           | 实际情况                                                                                                                     |
|----------------|------------------------------------------------------------------------------------------------------------------------------|
| **API / 语言** | `@Autowired` 字段注入在 Spring Framework 6、Spring Boot 3 中 **仍然合法**，没有 `@Deprecated`，也不会编译失败                   |
| **工程实践**   | Spring 官方文档、Spring Boot 参考指南、IntelliJ 检查等 **普遍推荐构造器注入**；团队规范与代码评审里常把字段注入视为应避免的写法 |

因此更准确的说法是：**这是 Spring 生态（Framework + Boot + 工具链）的共识，不是 Boot 单独废弃了某个注解。** Spring Boot 没有定义另一套注入规则，只是基于 Spring 容器，并在文档与示例中越来越倾向构造器注入。

仍可能见到字段注入的场景：老项目遗留、快速原型、教程示例图省事。新代码与 `@Service` / `@Repository` / `@RestController` / `@Configuration` 等 Bean 应优先构造器注入；`@Value("${...}")` 注在字段上属于 **配置绑定**，与 **注入其他 Bean** 是不同问题。

更系统的 IoC / DI 背景见 [Spring IoC 与依赖注入](/spring-ioc)。

## Bean Validation 常用约束（简述）

在控制器方法入参上配合 `@Valid` 或类上 `@Validated` 触发校验时，常见注解分工如下（语义以 Jakarta Bean Validation 为准）：

| 注解        | 典型用法                                |
|-------------|-----------------------------------------|
| `@NotNull`  | 引用不能为 `null`（集合元素个数仍可为 0） |
| `@NotEmpty` | 集合、数组、字符串等「规模」非空            |
| `@NotBlank` | 字符串非 null，且不能只包含空白字符      |

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

|                | Java 虚拟线程       | Go 协程（goroutine） |
|----------------|---------------------|--------------------|
| 出现时间       | 2023（Java 21）       | 2009（Go 1.0）       |
| 调度器         | JVM 内置            | Go runtime         |
| 初始栈内存     | 约 1KB              | 约 2KB             |
| 与现有代码兼容 | ✅ 完全兼容，API 不变 | —                  |

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
|----------|-----------------------|----------------------|
| 代码改动 | 零改动，一行配置       | 需要重写为响应式风格 |
| 调试体验 | 清晰可读的堆栈        | 复杂的响应式链路     |
| 库兼容性 | 所有现有库直接可用    | 需要响应式版本的驱动 |
| 适合场景 | 普通业务系统          | 流式推送、背压控制    |

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
|---------------|------------------|
| 3.0.x         | 6.0.x            |
| 3.2.x         | 6.1.x            |
| 3.3.x / 3.4.x | 6.1.x / 6.2.x    |
| **3.5.x**     | **6.2.x**        |

### 1. Java 版本要求

Spring Boot 3.x **最低要求 Java 17**。

### 2. javax → jakarta 命名空间迁移（最大变更）

Java EE 已捐赠给 Eclipse 基金会，品牌更名为 Jakarta EE，所有包名从 `javax.*` 改为 `jakarta.*`。这是**代码层面影响最广**的变更，几乎所有用到 Servlet、JPA、Bean Validation 的代码都要修改：

| 旧包名（javax）         | 新包名（jakarta）         |
|-----------------------|-------------------------|
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

| 特性                | 旧链式写法                | Lambda DSL           |
|---------------------|---------------------------|----------------------|
| 结构                | 扁平链式，靠 `.and()` 拼接 | 嵌套 Lambda，结构清晰 |
| 可读性              | 需要靠缩进约定            | 作用域边界明确       |
| IDE 支持            | 容易混淆配置层级          | 类型推断更准确       |
| Spring Security 6.x | 已废弃                    | **唯一支持的写法**   |

Spring Security 6.x 移除了旧的链式 API（如 `authorizeRequests()`、`.and()`），只保留 Lambda DSL，因为它更清晰地表达了每个配置块的边界，减少配置错误。

### 4. Hibernate 6.x

ORM 层升级到 Hibernate 6，部分 HQL/JPQL 语法更严格，一些隐式类型转换不再支持，自定义类型映射 API 有变化。

### 5. AOT 与 GraalVM Native Image

Spring Boot 3.x 正式支持 GraalVM Native Image 编译，可以将应用编译为原生可执行文件，启动时间从秒级降到毫秒级，但对反射、动态代理等有额外约束。

---

## 参考

- [Spring Boot 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Boot Gradle 插件参考](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/htmlsingle/)
- [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)
- [Building a RESTful Web Service](https://spring.io/guides/gs/rest-service/)（官方入门）
- [Spring MVC 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html)
