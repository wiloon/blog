---
title: Spring IoC 与依赖注入
author: "-"
date: 2026-05-12T14:10:03+08:00
lastmod: 2026-05-12T14:10:03+08:00
url: spring-ioc
categories:
  - Java
tags:
  - java
  - spring
  - remix
  - AI-assisted
---

IoC（Inversion of Control，控制反转）是 Spring 的核心机制。它把"创建和管理对象"的控制权从应用代码交给 Spring 容器，应用代码只需声明依赖，容器负责提供。

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
// IoC 写法：声明需要什么，容器负责提供
@Service
public class OrderService {
    @Autowired
    private UserDao userDao;          // 容器注入，不关心具体实现

    @Autowired
    private EmailService emailService;
}
```

切换实现时只需修改容器配置，`OrderService` 代码本身不用动。

## Spring IoC 容器

Spring 提供两个核心容器接口：

| 接口                 | 说明                                                             |
| -------------------- | ---------------------------------------------------------------- |
| `BeanFactory`        | IoC 容器最基础的接口，懒加载 Bean                                |
| `ApplicationContext` | `BeanFactory` 的扩展，支持事件、国际化、AOP 等，是实际使用的容器 |

Spring Boot 启动时，`@SpringBootApplication` 会自动创建并启动一个 `AnnotationConfigServletWebServerApplicationContext`（Web 应用）或 `AnnotationConfigApplicationContext`（非 Web），这就是 IoC 容器的实体。

容器启动过程：

```
扫描 @Component/@Service/@Repository 等注解
  → 读取 @Configuration 类中的 @Bean 定义
  → 实例化所有单例 Bean
  → 注入依赖（@Autowired）
  → 执行 @PostConstruct 初始化方法
  → 容器就绪，应用可以处理请求
```

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
    private UserDao userDao;  // 简洁，但无法写单元测试，也无法声明 final
}
```

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

优点：依赖不可变（`final`），对象创建后状态完整，便于单元测试（直接 `new` 传入 Mock）。**推荐使用构造器注入**，Lombok 的 `@RequiredArgsConstructor` 可以消除样板代码。

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
    @Autowired
    @Qualifier("primaryDs")    // 指定注入哪个 Bean
    private DataSource dataSource;
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

- [Spring Framework 官方文档 - IoC Container](https://docs.spring.io/spring-framework/reference/core/beans.html)
