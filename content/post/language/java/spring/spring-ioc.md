---
title: Spring IoC，依赖注入
author: "-"
date: 2026-05-12T14:10:03+08:00
lastmod: 2026-06-24T06:37:34+08:00
url: spring-ioc
categories:
  - Java
tags:
  - AI-assisted
  - java
  - remix
  - spring
---

IoC（Inversion of Control，控制反转）是 Spring 的核心机制。它把"创建和管理对象"的控制权从应用代码交给 Spring 容器，应用代码只需声明依赖，容器负责提供。Spring Framework 整体定位见 [Spring](./spring.md)。

IoC 的具体实现方式叫 **DI（Dependency Injection，依赖注入）**，容器通过构造器、字段或 Setter 方法将依赖对象注入进来。

## IoC 解决了什么问题

传统写法中，对象自己负责创建依赖：

```java
// 传统写法：自己创建依赖，紧耦合
public class OrderService {
    private UserDao userDao = new UserDaoImpl();  // 自己 new，换实现要改代码
    private EmailService email = new EmailService("smtp.example.com", 465);
}
```

这带来三个问题：

1. **紧耦合**：`OrderService` 直接依赖具体实现类，换实现必须修改源码
2. **难以测试**：无法替换成 Mock 对象，单元测试困难
3. **对象生命周期散乱**：每次 `new` 都产生新对象，无法复用单例

IoC 写法：

```java
// IoC 写法：声明需要什么，容器负责提供（推荐构造器注入）
@Service
public class OrderService {
    private final UserDao userDao;
    private final EmailService emailService;

    public OrderService(UserDao userDao, EmailService emailService) {
        this.userDao = userDao;
        this.emailService = emailService;
    }
}
```

切换实现时只需修改容器配置（或替换实现类上的 `@Primary` / `@Qualifier`），`OrderService` 代码本身不用动。

## Spring IoC 容器

Spring 提供两个核心容器接口：

| 接口                 | 说明                                                             |
| -------------------- | ---------------------------------------------------------------- |
| `BeanFactory`        | IoC 容器最基础的接口，懒加载 Bean                                |
| `ApplicationContext` | `BeanFactory` 的扩展，支持事件、国际化、AOP 等，是实际使用的容器 |

Spring Boot 通过 `SpringApplication.run()` 创建并启动 `ApplicationContext`：Web 应用常见为 `AnnotationConfigServletWebServerApplicationContext`，非 Web 为 `AnnotationConfigApplicationContext`。这就是 IoC 容器在运行时的实体。

主类上的 `@SpringBootApplication` 是组合注解，**不会创建容器**，而是为即将启动的 `ApplicationContext` 提供启动所需的配置元数据（可理解为「启动说明书」）。`SpringApplication.run(主类.class, args)` 会把该主类作为 **primary source** 传给容器；容器在 `refresh()` 里按这些元数据扫描、注册 Bean，再完成实例化与依赖注入。

| 组成部分 | 为容器提供什么 |
| --- | --- |
| `@ComponentScan` | 组件扫描范围（默认主类所在包及子包） |
| `@EnableAutoConfiguration` | 要加载的 Spring Boot 自动配置类 |
| `@SpringBootConfiguration`（本质是 `@Configuration`） | 主类本身作为配置源，可配合 `@Bean` 注册 Bean |

三者分工：`@SpringBootApplication` 声明容器该怎么启动 → `SpringApplication.run()` 创建 `ApplicationContext` → 容器执行 IoC（注册、实例化、注入）。

### 组件扫描

`@ComponentScan`（`@SpringBootApplication` 自带）在指定包路径下查找带 `@Component`、`@Service`、`@Repository`、`@Controller` 等注解的类，把它们登记为 Bean 定义。它回答的是「**哪些类本身是组件**」，不负责读出 `@Configuration` 类里的 `@Bean` 工厂方法——后者属于下面的配置解析。

### 启动时 refresh() 概览

容器在 `ApplicationContext.refresh()` 中的启动过程：

```
@ComponentScan 扫描 @Component/@Service/@Repository 等注解
  → 解析 @Configuration 类（@Bean / @Import 等）→ 登记 Bean 定义
  → @EnableAutoConfiguration 加载自动配置类（同样走配置解析）
  → 评估 @Conditional，决定哪些 Bean 定义真正注册
  → 实例化单例 Bean
  → 注入依赖（@Autowired）
  → 执行 @PostConstruct 初始化方法
  → 容器就绪，应用可以处理请求
```

## @Configuration 解析

**组件扫描**回答「哪些类是 Spring 组件」；**配置解析**回答「`@Configuration` 类里要产出哪些 Bean、怎么产出」。这里的「配置」指 Java Config（`@Configuration`、`@Bean`），不是 `application.yml`。

容器在 `refresh()` 早期由 `ConfigurationClassPostProcessor` 等组件完成解析，典型工作包括：

| 解析什么 | 例子 | 目的 |
| -------- | ---- | ---- |
| `@Bean` 方法 | `@Bean DataSource dataSource()` | 登记 Bean 定义：工厂方法、返回类型、方法参数即依赖 |
| `@Import` | `@Import(RedisConfig.class)` | 把其他配置类或 `ImportSelector` 拉进容器 |
| 嵌套 `@ComponentScan` | 配置类上再扫别的包 | 扩大组件发现范围 |
| `@PropertySource` 等 | 指定属性文件 | 与配置类绑定的外部配置 |

`@Configuration` 与带 `@Component` 的普通类有一个关键区别：配置类里的 `@Bean` 方法**互相调用**时，必须拿到容器里的**同一个单例**，不能像普通 Java 方法那样每次 `new`：

```java
@Configuration
public class AppConfig {

    @Bean
    public DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost/mydb");
        return ds;
    }

    @Bean
    public UserDao userDao() {
        // dataSource() 被调用两次也必须返回同一实例，而非两个连接池
        return new UserDao(dataSource());
    }
}
```

为此 Spring 会对 `@Configuration` 类做增强（常见为 CGLIB 子类代理），让 `@Bean` 方法之间的调用走容器，而不是直接执行原方法。

传统启动时，上述解析靠反射在运行时完成。读 [Spring AOT](./spring-aot.md) 时会看到：AOT 把解析结果固化成生成代码，运行时跳过反射解析，但**仍会按 Bean 定义实例化对象并做依赖注入**——固化的是元数据，不是运行时的 Bean 实例。

**条件装配**（`@Conditional`）决定某个 Bean 定义要不要注册；Spring Boot 的 `@ConditionalOnClass`、`@ConditionalOnProperty` 等是它的常用封装，见 [Spring Boot §@ConditionalOn*](./spring-boot.md#conditionalon-条件注解)。

## Bean 的注册方式

### 方式 1：注解扫描（最常用）

```java
@Service           // 等价于 @Component，语义上表示业务服务层
public class UserService { ... }

@Repository        // 表示数据访问层，附加异常转换功能
public class UserDao { ... }

@Component         // 通用组件，不属于特定层
public class IdGenerator { ... }
```

Spring Boot 默认扫描主类所在包及其子包下的所有 `@Component`（及派生注解）。

### 方式 2：@Bean 方法

适合注册第三方库的类（无法在源码上加注解）：

```java
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:mysql://localhost/mydb");
        return ds;
    }
}
```

### 方式 3：XML 配置（旧项目）

Spring **1.x 时代几乎全靠 XML** 定义 Bean；`@ComponentScan` 与 `@Autowired` 等注解扫描是 **2.5（2007）** 之后才成主流。见 [Spring](./spring.md) §Spring 1.x。

```xml
<bean id="userService" class="com.example.UserService">
    <property name="userDao" ref="userDao"/>
</bean>
```

现代项目几乎不再使用，了解即可。

## 依赖注入的三种方式

### 字段注入（不推荐）

```java
@Service
public class OrderService {
    @Autowired
    private UserDao userDao;  // 简洁，但无法声明 final，单元测试也不方便
}
```

**说明：** `@Autowired` 字段注入在 Spring 6 / Boot 3 中 **并未标记为 `@Deprecated`**，编译和运行都正常。业界说的「要淘汰」指的是 **工程实践上不推荐**，属于 Spring 生态（Framework + Boot + IDE 检查）的共识，而不是 Boot 单独废除了该 API。新 Bean 应优先构造器注入；详见 [Spring Boot 依赖注入方式](./spring-boot.md#依赖注入方式)。

### 构造器注入（推荐）

```java
@Service
public class OrderService {
    private final UserDao userDao;

    // Spring 4.3+ 单构造器时 @Autowired 可省略
    public OrderService(UserDao userDao) {
        this.userDao = userDao;
    }
}
```

优点：

- **依赖不可变**：协作对象可声明为 `private final`，构造完成后引用不能替换（不可变设计在 DI 层的体现）
- **对象创建即完整**：必需依赖在构造器参数中一次性声明，缺失依赖启动即失败
- **便于单元测试**：不启 Spring 容器即可 `new OrderService(mockDao, mockEmail)` 做纯单元测试

**推荐使用构造器注入**；Lombok 的 `@RequiredArgsConstructor` 可为所有 `final` 字段生成构造器，减少样板代码。

### Setter 注入（可选依赖场景）

```java
@Service
public class NotificationService {
    private EmailService emailService;

    @Autowired(required = false)   // 可选依赖，没有时不报错
    public void setEmailService(EmailService emailService) {
        this.emailService = emailService;
    }
}
```

## @Autowired 与 @Qualifier

当容器中同一类型有多个 Bean 时，`@Autowired` 按类型匹配会失败，需要用 `@Qualifier` 指定 Bean 名称：

```java
@Configuration
public class DataSourceConfig {
    @Bean("primaryDs")
    public DataSource primaryDataSource() { ... }

    @Bean("replicaDs")
    public DataSource replicaDataSource() { ... }
}

@Service
public class UserService {
    private final DataSource dataSource;

    public UserService(@Qualifier("primaryDs") DataSource dataSource) {
        this.dataSource = dataSource;
    }
}
```

## @Value：注入配置值

```java
@Service
public class PayService {
    @Value("${pay.timeout:30}")          // 读取配置，默认值 30
    private int timeout;

    @Value("${pay.api-key}")             // 没有默认值，缺少时启动报错
    private String apiKey;
}
```

对应 `application.yml`：

```yaml
pay:
  timeout: 60
  api-key: sk-xxxxxxxx
```

## Bean 的作用域

| 作用域              | 说明                                   |
| ------------------- | -------------------------------------- |
| `singleton`（默认） | 整个容器只有一个实例，所有注入点共享   |
| `prototype`         | 每次注入/获取都创建新实例              |
| `request`           | 每个 HTTP 请求一个实例（Web 应用）     |
| `session`           | 每个 HTTP Session 一个实例（Web 应用） |

```java
@Component
@Scope("prototype")
public class ReportGenerator { ... }
```

绝大多数 Bean 用默认的 `singleton` 即可，`prototype` 适合有状态的、不可复用的对象。

## Bean 的生命周期

```java
@Component
public class CacheManager {

    @PostConstruct           // 依赖注入完成后执行，用于初始化
    public void init() {
        System.out.println("缓存初始化...");
    }

    @PreDestroy              // 容器关闭前执行，用于释放资源
    public void destroy() {
        System.out.println("缓存清理...");
    }
}
```

## 与 AOP 的关系

IoC 容器负责**管理对象**，AOP 负责**增强对象行为**，两者配合：

- 容器创建 Bean 后，如果该 Bean 匹配 AOP 切面，容器会将其替换为**代理对象**再注入
- 所以 `@Autowired` 注入的实际上可能是代理对象，而非原始类的实例
- 这也是为什么 `@Transactional`、`@Cacheable` 等 AOP 注解必须加在 Spring 管理的 Bean 上才生效

## 参考

- [Spring Boot §@ConditionalOn*](./spring-boot.md#conditionalon-条件注解)（条件装配与自动配置）
- [Spring Boot 依赖注入方式](./spring-boot.md#依赖注入方式)（构造器注入、字段注入为何不推荐、不可变 `final` 依赖）
- [Spring AOT](./spring-aot.md)（构建期固化扫描、配置解析与条件装配结果）
- [Spring Framework 官方文档 - IoC Container](https://docs.spring.io/spring-framework/reference/core/beans.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-24 | 修正 IoC 容器创建主体为 `SpringApplication.run()`；补充 `@SpringBootApplication` 与 `refresh()` 分工 | 原文易误解为注解直接创建并注入 Bean |
| 2026-06-24 | 补充 `@SpringBootApplication` 为 `ApplicationContext` 提供启动元数据的分工说明 | 明确注解与 IoC 容器的职责边界 |
| 2026-06-24 | 移至 `language/java/spring/spring-ioc.md` | 与 Spring 专题文章同目录归类 |
| 2026-06-24 | XML 配置节补充 1.x 时代说明；链到 spring.md | 与 Spring 总览文对齐 |
| 2026-06-24 | 新增 `@Configuration` 解析节；`refresh()` 流程补充条件装配；拆分组件扫描小节 | 澄清配置解析含义，便于理解 Spring AOT |
