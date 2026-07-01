---
title: Spring Boot
author: wiloon
date: 2026-05-11T14:24:31+08:00
lastmod: 2026-06-30T22:58:55+08:00
url: spring-boot
aliases:
  - /spring/boot/
categories:
  - java
tags:
  - AI-assisted
  - gradle
  - java
  - maven
  - remix
  - restful
  - spring
  - spring boot
---

## Spring Boot 是什么

Spring Boot 是 Pivotal （现为 VMware/Broadcom）在 2014 年推出的框架，建立在 Spring Framework 之上，目标是简化整个 Spring 生态的开发、配置和部署。它不只是简化 Spring MVC，同样简化了 Spring Data（数据库访问）、Spring Security（认证授权）、Spring Messaging（消息队列）等全家桶的配置。

核心理念是 **"约定优于配置"（Convention over Configuration）**：框架提前定好"默认约定"，只要遵循这些约定，就不需要写任何配置；只有想偏离默认行为时，才需要显式配置。

例如，classpath 里有 `spring-boot-starter-web`，Spring Boot 就约定你要启动一个 Web 服务，自动完成：注册 `DispatcherServlet`、内嵌 Tomcat 监听 8080 端口、注册 Jackson 用于 JSON 序列化。你什么都不写，`java -jar app.jar` 就能跑起来。需要覆盖默认行为时，只在 `src/main/resources/application.yml` 中写偏离默认值的部分：

```yaml
server:
  port: 9090  # 只需声明偏离默认值的配置
```

也可通过命令行参数临时覆盖：`java -jar app.jar --server.port=9090`，优先级高于 `application.yml`。

### 出现背景

Spring Boot（2014）与微服务架构的兴起同期出现。2014 年 Martin Fowler 发表了微服务架构的奠基性文章，微服务要求每个服务独立部署、快速启动、进程隔离。传统的 WAR 包 + 外部 Tomcat 的部署方式与这一需求存在明显矛盾，Spring Boot 正是为了解决这一问题而生。

前后端分离（React 2013、Vue 2014）也在同期兴起，但它不是 Spring Boot 出现的直接驱动力——Spring MVC 本身早已能支持 RESTful API，Spring Boot 只是让这件事更方便做。

### Spring Boot 解决了三个问题

#### 1. XML 配置的复杂性

传统 Spring 项目需要用大量 XML 配置 Spring MVC、数据库连接池、事务管理、安全等模块。即便 Spring 2.5 起业务类已多用注解，数据源、`component-scan`、事务开关、`web.xml` 等骨架配置仍长期留在 XML 里；Spring 3.0 的 Java Config（`@Configuration` + `@Bean`）技术上可替代 XML，但每个基础设施都要手写配置类。Spring Boot 通过自动配置和 Starter 依赖，把上述样板降到近乎为零——多数场景只需 `application.yml` 与业务注解。配置演进脉络见 [Spring](./spring.md) §从 Java Config 到 Spring Boot。

#### 2. WAR 包 + 外部 Tomcat 的部署复杂性

传统方式需要先在服务器上安装、配置 Tomcat，再把 WAR 包部署进去。Spring Boot 把 Tomcat 内嵌进 JAR，`java -jar app.jar` 一条命令启动一个独立进程，符合微服务"每个服务独立运行"的要求。

值得注意的是，Tomcat + WAR 包同样可以跑 RESTful API——WAR 包里的 `DispatcherServlet` 既能处理返回 JSP 的请求，也能处理返回 JSON 的请求，Tomcat 不关心你返回什么内容。Spring Boot 的内嵌方式只是把部署流程简化了，底层机制没有改变。

`java -jar app.jar` 启动时，`main()` 方法里 Spring Boot 以编程方式启动内嵌 Tomcat（等价于 `new Tomcat().start()`），把 `DispatcherServlet` 注册进去，Tomcat 开始监听端口，Web 服务就绪。本质上 Tomcat 还是那个 Tomcat，只是从"独立进程 + 外部部署"变成了"作为一个库被你的进程调用"。

|             | 传统 WAR + 外部 Tomcat   | Spring Boot JAR     |
| ----------- | ------------------------ | ------------------- |
| Tomcat 进程 | 独立进程，先于应用存在   | 内嵌在应用进程里    |
| 部署        | 把 WAR 拷贝到 `webapps/` | `java -jar app.jar` |
| 生命周期    | Tomcat 管理应用          | 应用管理 Tomcat     |
| 多应用共享  | 一个 Tomcat 可跑多个 WAR | 每个应用独立进程    |

#### 3. Tomcat 配置的独立管理问题

传统部署中 Tomcat 有自己独立的一套配置文件（`server.xml`、`context.xml` 等），与应用代码分开管理，容易出现环境差异问题。Spring Boot 将 Tomcat 的配置（端口、线程池等）统一纳入 `application.yml`，配置即代码，跟着项目走。

### 主要特性

- **自动配置（Auto-configuration）**：根据 classpath 中的依赖自动配置 Spring Bean，无需手写 XML 或 `@Configuration` 类。
- **起步依赖（Starter）**：一组预定义的 Maven/Gradle 依赖集合，例如 `spring-boot-starter-web` 会自动引入 Spring MVC、Tomcat、Jackson 等全套依赖。
- **内嵌服务器**：内置 Tomcat / Jetty / Undertow，打包为可执行 JAR，直接 `java -jar app.jar` 运行，无需单独部署到 Tomcat。切换只需在 `pom.xml` 排除默认 Tomcat、引入目标服务器的 Starter。
- **Actuator**：内置生产级监控端点（health check、metrics 等）。
- **DevTools**（开发可选）：快速 Restart、LiveReload；见 [Spring Boot DevTools](./spring-boot-devtools.md)。
- **Spring Initializr**：通过 [start.spring.io](https://start.spring.io) 快速生成项目骨架。

## Maven：`spring-boot-starter-parent`

在 Maven 工程里把 `spring-boot-starter-parent` 设为 `<parent>` 后，子 POM 会继承一整套默认约定，减少样板配置。常见效果包括：

- 统一的 Java 发行版、源码编码（如 UTF-8）与常用插件的默认行为  
- **依赖管理（BOM）**：常用依赖的兼容版本由 `spring-boot-dependencies` 对齐，声明 `spring-boot-starter-*` 时通常不必再写 `<version>`  
- 打包、`resources` 过滤等默认集成  

BOM 与「版本对齐」：BOM（Bill of Materials，物料清单）是一个只声明版本、不引入实际依赖的特殊 POM——`spring-boot-dependencies` 用 `<dependencyManagement>` 给数百个常用库钉死了一组互相兼容的版本号。继承 `spring-boot-starter-parent`（或 `import` 该 BOM）后，你写依赖时不必再写 `<version>`，版本由 BOM 统一决定，从而避免「Jackson 与 Spring 版本不匹配」这类冲突，这就是「版本对齐」。区分两个概念：Starter 解决「要引哪些 JAR」（依赖清单），BOM 解决「这些 JAR 用哪个版本」（版本清单）。

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
@SpringBootConfiguration   // 元标注了 @Configuration，本质上也是配置类
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

#### `@SpringBootConfiguration`

要理解它，得先理解 `@Configuration`。`@Configuration` 是 Spring Framework（不是 Spring Boot）的注解，作用是把一个类标记为配置类：这个类负责告诉容器「要创建哪些对象、怎么创建」。

这里容易混用三个词，先分清：

| 词               | 是什么                                                          |
| ---------------- | --------------------------------------------------------------- |
| Bean             | 容器管理的对象实例（如 `DataSource`、`UserService`），不是方法  |
| `@Bean`          | 标在方法上的注解；方法返回的对象会被注册进容器，成为一个 Bean   |
| `@Configuration` | 标在类上的注解；表示这个类是配置源，里面可以有多个 `@Bean` 方法 |

所以「配合 `@Bean` 方法」是指：用带 `@Bean` 注解的方法来注册 Bean，不是说 Bean 本身是方法。三者的分工是：`@Configuration` 声明「这个类在配置东西」；`@Bean` 声明「怎么造出某个对象并放进容器」；配置里的值（URL、密码等）写在 `application.yml`，通过 `@Value` 或 `@ConfigurationProperties` 读进来，再在 `@Bean` 方法里用来组装对象。

它配置的是「Bean 怎么创建、怎么组装」，而不是数据库连接串、端口号这类「值」。那类参数写在 `application.yml`/`application.properties` 里，通过 `@Value` 或 `@ConfigurationProperties` 注入。两者常配合使用——在 `@Configuration` 类的 `@Bean` 方法里读取这些参数去创建 `DataSource` 等对象：

```java
@Configuration
public class DataSourceConfig {

    // 从 application.yml 读取连接信息（值），用来组装 DataSource Bean（装配）
    @Bean
    public DataSource dataSource(
            @Value("${app.db.url}") String url,
            @Value("${app.db.username}") String username,
            @Value("${app.db.password}") String password) {
        return DataSourceBuilder.create()
                .url(url).username(username).password(password).build();
    }
}
```

`@SpringBootConfiguration` 则是 Spring Boot 对 `@Configuration` 的特化：它的源码里直接用 `@Configuration` 标注，所以容器把它当成普通配置类处理，Bean 装配能力完全相同，只是额外多了 Boot 自己的语义和约定。

| 维度         | `@Configuration`               | `@SpringBootConfiguration`                             |
| ------------ | ------------------------------ | ------------------------------------------------------ |
| 来源         | Spring Framework               | Spring Boot                                            |
| 容器行为     | 配置类，可用 `@Bean` 定义 Bean | 同左（源码就标了 `@Configuration`）                    |
| 用途         | 任意配置类                     | 标记 Boot 应用的主配置类                               |
| 数量约定     | 可有多个                       | 全应用只应有一个（即主类）                             |
| 测试自动发现 | 需 `@ComponentScan` 或显式指定 | `@SpringBootTest` 会沿包路径向上自动找到它来加载上下文 |

> 元注解（meta-annotation）是「标在注解定义上的注解」。Java 自带的元注解有 `@Target`（能标在哪）、`@Retention`（保留到什么时候）、`@Documented` 等。`@SpringBootConfiguration` 的定义上又标了 `@Configuration`，`@SpringBootApplication` 上又标了 `@SpringBootConfiguration`——这叫组合注解（composed annotation）。Java 没有注解的 `extends` 语法，社区里一般不说「注解多继承」，而说组合注解；口语里的「带着 `@Configuration` 的语义」只是形象说法，不是语言层面的继承。Spring 启动时会做元注解查找：看到 `@SpringBootApplication` 就知道它「带着」 `@Configuration` 的语义，尽管类上只写了最外层那一个注解。

日常开发几乎不直接写 `@SpringBootConfiguration`，它通过 `@SpringBootApplication` 间接带上。

为什么要单独标记主类？不标 `@SpringBootConfiguration`、主类上只有普通 `@Configuration` 时，容器照样能启动，但会丢失 Boot 的若干约定：`@SpringBootTest` 默认沿包路径向上查找带 `@SpringBootConfiguration` 的类来加载完整上下文（不只为了测试——集成测试需要与生产相同的 Bean 装配）；Actuator、DevTools 等也会把它当作「应用主配置类」的锚点。全应用只应有一个，语义是「这是 Boot 应用的根配置入口」，而不只是「又一个 `@Configuration`」。

#### `@EnableAutoConfiguration`

开启 [Auto-configuration](#auto-configuration自动配置) 机制——这是 Spring Boot 相对 Spring Framework 最核心的增量能力。`SpringApplication.run()` 刷新 `ApplicationContext` 时，在处理 `@Configuration` 的阶段会通过 `ImportSelector` 用类加载器读取 classpath 上各 JAR 的 `AutoConfiguration.imports`，加载其中列出的自动配置类，再经条件注解决定是否注册 Bean。一般应用都会开启（`@SpringBootApplication` 已包含）；单独写出是为了语义明确，也可通过 `exclude` 关掉部分自动配置。

#### `@ComponentScan`

来自 Spring Framework（Boot 2.5 之前就有），不是 Boot 专有。默认扫描主类所在包及其所有子包，将带有 `@Component`、`@Service`、`@Repository`、`@Controller` 等注解的类注册为 Spring Bean。详见 [Spring IoC §@ComponentScan 与组件注解](./spring-ioc.md#componentscan-与组件注解)（含 [`@Indexed` 与组件索引](./spring-ioc.md#indexed-与组件索引)）。

这也是为什么通常把主类放在项目的根包下（如 `com.example.myapp.MyApp`），确保所有业务代码都能被扫描到。如果某个类放在主类包之外，就不会被自动发现（可在其他 `@Configuration` 上再声明 `@ComponentScan` 扩大范围）。

#### `@ConfigurationPropertiesScan`

`@ConfigurationProperties` 把 `application.yml` / `application.properties` 里的一组键绑定到 POJO 字段上，但光写注解不会自动进容器——还得把它注册成 Bean，绑定才会生效、别处才能 `@Autowired` 注入。

常见注册方式有三种：

| 方式     | 写法                                                                             | 适用场景                                                                                |
| -------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 标成组件 | 类上同时 `@ConfigurationProperties` + `@Component`（或 `@Configuration`）        | 单个、固定的配置类                                                                      |
| 显式启用 | 在任意 `@Configuration` 上 `@EnableConfigurationProperties(XxxProperties.class)` | 自动配置类、或只注册少数几个类（Boot 自动配置常用此写法）                               |
| 包扫描   | 主类上 `@ConfigurationPropertiesScan`                                            | 项目里有多处 `@ConfigurationProperties` 类，不想逐个 `@Enable`、也不想都加 `@Component` |

`@ConfigurationPropertiesScan`（Spring Boot 2.2+）的作用类似 `@ComponentScan`，但扫描目标是带 `@ConfigurationProperties` 的类：在指定包路径下找到它们并注册为 Bean。默认扫描范围与 `@ComponentScan` 一致（主类所在包及子包），也可用 `basePackages` / `basePackageClasses` 自定义。

```java
@SpringBootApplication
@ConfigurationPropertiesScan  // 扫描 com.example.myapp 及子包下的 @ConfigurationProperties
public class MyApp { ... }
```

```java
@ConfigurationProperties(prefix = "app.mail")
public class MailProperties {
    private String host;
    private int port;
    // getters / setters
}
```

上例中 `MailProperties` 不需要 `@Component`；加了 `@ConfigurationPropertiesScan` 后会被自动注册，YAML 里 `app.mail.host` 等键会绑定到字段。

注意：`@SpringBootApplication` 不包含 `@ConfigurationPropertiesScan`。不用扫描时，仍可用 `@EnableConfigurationProperties` 或 `@Component` 单独注册；自动配置模块里的 `DataSourceProperties` 等也是靠 `@EnableConfigurationProperties` 启用的（见下文 Auto-configuration 示例）。

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

## Auto-configuration（自动配置）

Auto-configuration 是 Spring Boot 的核心机制，负责根据 classpath 中存在的依赖，自动向 Spring 容器注册所需的 Bean，无需手写任何 `@Configuration` 类或 XML。

### 为什么需要 Auto-configuration

Component Scan 是 Spring Framework 的能力，Boot 只是在 `@SpringBootApplication` 里默认带上它，用来发现你自己写的业务 Bean。Boot 的特有价值在于 Auto-configuration：按 classpath 和配置，有选择地把第三方集成所需的 Bean 注册进容器。

Spring Boot 启动时，`@SpringBootApplication` 默认只会对应用自己的包（及其子包）做 Component Scan，扫描其中带有 `@Component`、`@Service` 等注解的类并注册为 Bean。

第三方库（如 Redis）又需要把 `RedisTemplate`、`LettuceConnectionFactory` 等 Bean 放进容器，你的业务代码才能 `@Autowired` 使用。Component Scan 解决不了这件事，原因有两层：

1. 扫描范围：默认只扫主类包及子包，不会去扫 `org.springframework.data.redis.*` 等第三方包（设计上也不该把 classpath 上所有 JAR 都做注解扫描，又慢又无意义）。
2. 即使扩大扫描范围也没用：`RedisTemplate` 等是普通类，库作者不会在上面标 `@Component`——它们需要按你的 `application.yml` 用 `@Bean` 方法构造，不能无脑实例化。Component Scan 只认组件注解，扫到了也不会注册。

Auto-configuration 走另一条路：读 JAR 里的显式清单（`.imports`），加载其中的自动配置类；这些类用 `@Configuration` + `@Bean` 主动构造第三方所需对象，再放进容器。

Boot 出现之前，纯 Spring 项目集成第三方库通常要手写 `@Configuration` / XML，或 `@Import` 厂商提供的配置类，并自己处理版本对齐。Auto-configuration 把「发现该装什么 + 默认怎么装 + 用户自定义退让」这套样板收进了 starter + 条件注解。

两条机制是完全独立的两条路，各自负责不同来源的 Bean：

| 机制               | 来源             | 扫描范围                         | 触发方式                                                               |
| ------------------ | ---------------- | -------------------------------- | ---------------------------------------------------------------------- |
| Component Scan     | Spring Framework | 应用自己的包（主类所在包及子包） | 在包路径下找类，类上带有组件注解（`@Component` 及其派生）就注册为 Bean |
| Auto-configuration | Spring Boot      | classpath 上带 `.imports` 的 JAR | 读声明文件，加载自动配置类，经 `@ConditionalOn*` 过滤后注册 `@Bean`    |

两条路最终都往同一个 IoC 容器（运行时通常是 `ApplicationContext` 实现，如 `AnnotationConfigServletWebServerApplicationContext`）里放 Bean：容器内部用 Bean 定义注册表（`BeanDefinition`）登记「要创建什么、怎么创建」，实例化后放入单例缓存（默认 scope 为 singleton 的 Bean 各一份，按名称和类型索引，供 `@Autowired` 查找）。只是发现 Bean 定义的方式不同。

### 工作原理

常见误解：`.imports` 文件不在每个 starter JAR 里，更不在 Redis、Lettuce 这类普通客户端 JAR 里。Spring 官方集成的自动配置类与那份总清单集中在 `spring-boot-autoconfigure.jar` 一个 JAR 中；`spring-boot-starter-*` 通常只是 POM 依赖清单，把 `spring-boot-autoconfigure`、具体技术栈 JAR 和驱动捷在一起。非 Spring 项目（如 MyBatis）会自己发布 `xxx-spring-boot-autoconfigure` JAR，`.imports` 在那个 autoconfigure 模块里。

```
# spring-boot-autoconfigure.jar 内的 AutoConfiguration.imports（简化示意）
org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration
org.springframework.boot.autoconfigure.data.jpa.JpaRepositoriesAutoConfiguration
org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration
org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration
...
```

Spring Boot 启动时会用类加载器遍历 classpath 上每一个 JAR，若存在 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 就读取；大多数普通 JAR 没有这个文件，会被跳过。读到的类名列表会作为候选自动配置类加载。自动配置类标注 `@AutoConfiguration`（Boot 对 `@Configuration` 的特化，见下文），加载后同样要走 [@Configuration 解析](./spring-ioc.md#configuration-解析)（读出 `@Bean` 定义等），再经条件注解决定是否真正注册。

### classpath 是什么、Boot 何时用到

classpath（类路径）是 JVM 查找 `.class` 和 JAR 的搜索路径集合，由 `java -cp`、Maven/Gradle 依赖解析、`MANIFEST.MF` 的 `Class-Path` 等共同决定。概念与命令行见 [java -cp](../java-cp.md)；类加载器如何加载 classpath 上的类见 [Java ClassLoader](../classloader.md)。

Boot 与 classpath 的关联不只在启动读 `.imports` 那一次：条件注解 `@ConditionalOnClass` 在评估时也会问「这个类能不能被类加载器加载到」（等价于「对应 JAR 在不在 classpath 上」）。但「应用跑起来之后所有操作都读 classpath」不准确——只有加载类 / 读 JAR 内资源才走类加载器与 classpath；已创建的 Bean 在堆里运行，普通业务逻辑不再反复扫 classpath。

### `META-INF` 里的声明文件是什么

普通 JAR 的 `META-INF/` 里常见的是 `MANIFEST.MF`（清单）、`services/`（JDK `ServiceLoader` 用）等，并没有 Java 规范要求的 `AutoConfiguration.imports` 这类文件。

`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 是 Spring Boot 定义的约定，不是 Spring Framework 的规范，也不是 JDK / JAR 标准的一部分。启动时 Boot（不是裸 Spring 容器）会主动读 classpath 上每个 JAR 里的这个文件，把里面列出的全限定类名当作自动配置类去加载。Boot 2.7 之前同类信息写在 `META-INF/spring.factories` 里（同样是 Boot 约定），后来拆成专用文件。

第三方库配合 Boot 自动配置，常见两种形态：

1. Spring 官方全家桶（如 Redis、JPA、Security）：自动配置类与 `.imports` 在 `spring-boot-autoconfigure`；starter 只是依赖清单。classpath 上出现某技术的 JAR（如 `spring-data-redis`）且条件注解命中时，对应配置才生效——没引用的技术其配置类仍在清单里，但会被 `@ConditionalOnClass` 等跳过。这是「全家桶 JAR + 按需激活」，不是「每个 starter 各带一份 `.imports`」。
2. 非 Spring 项目（如 MyBatis、Dubbo）：由该库自己的团队发布 `xxx-spring-boot-autoconfigure`（或合并进 starter），自己的 JAR 里放 `AutoConfiguration.imports`。

以 Redis 为例，各层谁维护：

| 层次          | 产物                                      | 维护方                                                                                          |
| ------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Redis 服务器  | `redis-server`                            | Redis 社区 / Redis Ltd（与 Spring 无关）                                                        |
| Java 客户端   | Lettuce、Jedis                            | 各自的开源项目                                                                                  |
| Spring 访问层 | `spring-data-redis`（`RedisTemplate` 等） | Spring Data Redis 团队（`spring-projects/spring-data-redis`）                                   |
| 自动配置      | `RedisAutoConfiguration` 等               | Spring Boot 团队（在 `spring-boot-autoconfigure` 模块里；`AutoConfiguration.imports` 也在这里） |
| 起步依赖      | `spring-boot-starter-data-redis`          | Spring Boot 团队（基本是依赖清单 POM，把上面几样 + Lettuce 捷在一起）                           |

所以：`spring-boot-starter-data-redis` 不是 Redis 官方出的包，而是 Spring 生态为方便 Boot 集成 Redis 自己维护的 starter。你加这一个依赖，Boot 团队帮你对齐了版本，Boot 自动配置帮你注册 `RedisTemplate`，Spring Data 提供 API，底层默认用 Lettuce 连 Redis 服务器。

Boot 在 Java 企业开发里已是事实上的默认入口，大量库会额外提供 `spring-boot-starter-*`；不用 Boot 的纯 Spring Framework 项目不会读 `.imports`，需要自己 `@Import` 或 XML 配置。

注解分层（常被混为一谈）：

| 注解 / 机制                                                                             | 归属                          | 谁写                                                                                         |
| --------------------------------------------------------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------- |
| `@Component`、`@Autowired`、`@Configuration`、`@Bean`、`@ComponentScan`、`@Conditional` | Spring Framework              | 业务代码 + 框架内部                                                                          |
| `@ConfigurationProperties`、`@EnableConfigurationProperties`                            | Spring Boot（绑定外部化配置） | 业务 Properties 类；自动配置类里 `@Enable`                                                   |
| `@AutoConfiguration`、`@ConditionalOn*`、`AutoConfiguration.imports`                    | Spring Boot                   | 自动配置模块（`spring-boot-autoconfigure` 等），业务代码一般不写 `@ConditionalOnMissingBean` |

`@Autowired` 是 Spring Framework 的依赖注入注解：在容器里按类型（必要时按名称）查找已注册的 Bean 并注入字段/构造器/方法参数。Boot 没有另起一套注入机制，只是 Auto-configuration 帮你把更多 Bean 预先放进了同一个容器。

### `@AutoConfiguration` 与 `@Configuration`

`@AutoConfiguration` 标注在 `.imports` 清单里的那些类上，容器仍把它们当配置类处理（内部元标注了 `@Configuration`）。相对普通 `@Configuration`，它额外约定：

- **加载顺序**：`before` / `after`（或 `@AutoConfigureBefore` / `@AutoConfigureAfter`）控制多个自动配置类之间的先后——例如先配好 `DataSource`，再配依赖它的 `JdbcTemplate`，避免 `@Bean` 方法因依赖未就绪而失败。
- **默认** `proxyBeanMethods = false`，减轻启动开销（自动配置类通常不需要 `@Bean` 方法间互相调用）。

`@SpringBootConfiguration` 则标记应用主类，语义上「全应用唯一的根配置」，与自动配置类是不同角色。

### @ConditionalOn* 条件注解

条件装配由 Spring Framework 的 `@Conditional` 提供：标注在类或 `@Bean` 方法上，绑定一个 `Condition` 实现；容器在注册前评估，条件不成立则跳过该 Bean 定义。Boot 在其上封装了 `@ConditionalOnClass`、`@ConditionalOnProperty` 等，可视为 `@Conditional` 的语法糖，专用于自动配置场景。

自动配置类里大量使用这些条件注解做过滤，决定哪些第三方集成真正装配进容器：

| 注解                                              | 含义                                                                     |
| ------------------------------------------------- | ------------------------------------------------------------------------ |
| `@ConditionalOnClass(Xxx.class)`                  | 类加载器能加载到该类时生效（classpath 上有对应 JAR）；没有则整段配置跳过 |
| `@ConditionalOnMissingBean(Xxx.class)`            | 容器中没有该类型 Bean 时生效（用户已 `@Bean` 自定义则自动配置退让）      |
| `@ConditionalOnProperty("spring.datasource.url")` | 配置项存在且满足 `havingValue` / `matchIfMissing` 等规则时生效           |
| `@ConditionalOnWebApplication`                    | 当前是 Web 应用时生效                                                    |

`@ConditionalOnMissingBean` 主要写在 Boot 自动配置源码里，业务代码通常不需要。若业务与自动配置各注册一个同名 Bean，Boot 默认 `allow-bean-definition-overriding=false`，会启动失败而非后者覆盖前者；同类型不同名则可能导致 `@Autowired` 时 `NoUniqueBeanDefinitionException`。

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

这里的 `@Bean` 标在方法上，含义是：这个方法返回的对象会被注册进 Spring 容器，成为一个 Bean。容器在启动时调用 `dataSource(...)` 方法，把返回值（`DataSource` 实例）放进容器；方法名 `dataSource` 默认也会成为 Bean 的名称。`@Bean` 本身来自 Spring Framework，在普通 Spring 项目（不经过 Boot）里同样适用；上面示例里的 `@AutoConfiguration`、`@ConditionalOnClass` 才是 Boot 专有的。

这就是为什么：加了 `spring-boot-starter-data-jpa` + 配置了 `spring.datasource.url`，连接池就自动出现了；如果自己 `@Bean` 定义了 `DataSource`，自动配置就自动退让。

若需手写条件 Bean，可直接用 Framework 的 `@Conditional`，或 Boot 的 `@ConditionalOn*`：

```java
@Configuration
public class FeatureConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.x.enabled", havingValue = "true")
    public FeatureX featureX() {
        return new FeatureX();
    }
}
```

走 [Spring AOT](./spring-aot.md) 构建时，上述条件在构建期评估并固化；依赖运行时环境变量、真实网络等才能成立的条件，构建期可能判不到，是 Native 构建常见踩坑点。

### 覆盖自动配置

#### 方式一：自定义同类型 Bean

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

#### 方式二：通过 application.yml 调整属性

自动配置类通常都绑定了一组 `@ConfigurationProperties`，覆盖属性即可调整行为，无需替换整个 Bean：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost/mydb
    hikari:
      maximum-pool-size: 20
```

#### 方式三：排除某个自动配置类

```java
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class MyApp { ... }
```

### 查看哪些自动配置生效

Actuator 的 `/actuator/conditions` 端点（或启动时加 `--debug`）会输出 Conditions Evaluation Report，列出每个自动配置类是否生效及原因，是排查配置问题的利器。

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

## 外部化配置（Externalized Configuration）

外部化配置指把配置从代码里抽出来放到外部来源，同一个打包好的 JAR 不改动就能在不同环境运行——开发连本地库、生产连生产库，只换外部配置。Boot 支持的来源很多（`application.yml`/`.properties`、profile 专属文件、环境变量、命令行参数、配置中心等），并按固定优先级合并：高优先级覆盖低优先级，没配的就用代码里的默认值。

常见来源优先级（高 → 低，简化）：

| 优先级 | 来源                              | 例子                                |
| ------ | --------------------------------- | ----------------------------------- |
| 高     | 命令行参数                        | `--server.port=9090`                |
| ↑      | 环境变量                          | `SERVER_PORT=9090`                  |
| ↑      | `application-{profile}.yml`       | `application-prod.yml`              |
| ↓      | `application.yml` / `.properties` | 项目默认配置                        |
| 低     | 代码中的默认值                    | `@Value("${x:默认}")`、自动配置默认 |

```bash
# application.yml 写了 8080，命令行临时覆盖为 9090，不必重新打包
java -jar app.jar --server.port=9090

# 激活 prod profile：application-prod.yml 覆盖 application.yml 同名键
java -jar app.jar --spring.profiles.active=prod
```

值（URL、端口、密码等）通过 `@Value` 或 `@ConfigurationProperties` 注入到 Bean；`@ConfigurationProperties` 的绑定与注册见上文 [§@ConfigurationPropertiesScan](#configurationpropertiesscan)。这套机制正是「约定优于配置」里「只写偏离默认值的部分」能成立的基础。

---

## 启动应用

Spring Boot 应用打包后是一个可执行 JAR，通过 `java -jar` 启动。`MANIFEST.MF` 的 `Main-Class` 指向 `JarLauncher`，由 `spring-boot-loader` 加载 `BOOT-INF/classes` 与 `BOOT-INF/lib` 后再转调你的主类；布局与构建见 [Spring Boot Executable JAR](./spring-boot-executable-jar.md)。

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

命令行参数的优先级高于 `application.yml`，常用于在生产环境覆盖配置，而不用修改打包好的 JAR。

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

启动完成后若需执行初始化逻辑（Runner、`@PostConstruct` 等），见 [Spring Boot Startup Callbacks](./spring-boot-startup-callbacks.md)。

---

## Actuator（监控端点）

`spring-boot-starter-actuator` 提供一组生产级监控/管理端点，加这一个依赖即开箱即用，用于把应用的健康、指标、配置等状态以 HTTP（或 JMX）暴露出来，便于运维、监控系统和容器编排对接。

常用端点：

| 端点                                 | 用途                                        |
| ------------------------------------ | ------------------------------------------- |
| `/actuator/health`                   | 健康检查，K8s liveness/readiness 探针常用   |
| `/actuator/metrics`                  | 运行指标（内存、线程、HTTP 等）             |
| `/actuator/prometheus`               | Micrometer 暴露的 Prometheus 抓取格式       |
| `/actuator/conditions`               | 自动配置生效/未生效报告（排查利器，见上文） |
| `/actuator/env`、`/actuator/loggers` | 查看环境属性、动态调整日志级别              |

端点默认大多不暴露，需用 `management.endpoints.web.exposure.include` 显式开启；生产环境注意鉴权，避免泄露敏感信息。

---

## Bean Validation 常用约束（简述）

在控制器方法入参上配合 `@Valid` 或类上 `@Validated` 触发校验时，常见注解分工如下（语义以 Jakarta Bean Validation 为准）：

| 注解        | 典型用法                                  |
| ----------- | ----------------------------------------- |
| `@NotNull`  | 引用不能为 `null`（集合元素个数仍可为 0） |
| `@NotEmpty` | 集合、数组、字符串等「规模」非空          |
| `@NotBlank` | 字符串非 null，且不能只包含空白字符       |

---

## 延伸阅读

以下主题已从本文拆出为独立文章，便于按需阅读：

| 主题                                         | 文章                                                                    |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| 启动后回调（Runner、`@PostConstruct` 等）    | [Spring Boot Startup Callbacks](./spring-boot-startup-callbacks.md)     |
| Spring 注解体系、依赖注入三种方式            | [Spring IoC](./spring-ioc.md)                                           |
| 响应式 Web（WebFlux）                        | [Spring WebFlux](./spring-webflux.md)                                   |
| Java 21 虚拟线程与高并发                     | [Java Virtual Threads](../virtual-threads.md)                           |
| Boot 3.x 迁移（jakarta、Security 6、AOT 等） | [Spring Boot 3.x Migration](./spring-boot-3-migration.md)               |
| 可执行 JAR 布局与 `JarLauncher`              | [Spring Boot Executable JAR](./spring-boot-executable-jar.md)           |
| 容器镜像与 Buildpack 打包                    | [Spring Boot Container Packaging](./spring-boot-container-packaging.md) |
| 开发期热重启                                 | [Spring Boot DevTools](./spring-boot-devtools.md)                       |

---

## 参考

- [Spring IoC](./spring-ioc.md)（组件扫描、@Configuration 解析、依赖注入）
- [Spring Boot Startup Callbacks](./spring-boot-startup-callbacks.md)
- [Spring WebFlux](./spring-webflux.md)
- [Java Virtual Threads](../virtual-threads.md)
- [Spring Boot 3.x Migration](./spring-boot-3-migration.md)
- [Spring Boot 官方文档](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Boot Gradle 插件参考](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/htmlsingle/)
- [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)
- [Building a RESTful Web Service](https://spring.io/guides/gs/rest-service/)（官方入门）
- [Spring MVC 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html)

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                                               | 原因                                |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| 2026-06-21 | Boot 3 Native 小节链到新建 [spring-aot.md](./spring-aot.md)                                                                                                                                                                            | Spring AOT 专文拆分                 |
| 2026-06-24 | 「XML 配置的复杂性」补充 2.5 混合期、Java Config 与 Boot 分工；链到 spring.md                                                                                                                                                          | 厘清谁简化了 XML                    |
| 2026-06-24 | §启动应用 链到新建 [spring-boot-executable-jar.md](./spring-boot-executable-jar.md)                                                                                                                                                    | Fat JAR / JarLauncher 专文拆分      |
| 2026-06-24 | 展开 `@Conditional` 来源与手写示例；链到 spring-ioc 配置解析、spring-aot                                                                                                                                                               | 澄清条件装配与 AOT 构建期评估       |
| 2026-06-24 | `@ComponentScan` 小节链到 spring-ioc 专节                                                                                                                                                                                              | 避免与 IoC 文重复，集中写扫描机制   |
| 2026-06-27 | `@ComponentScan` 小节补充 `@Indexed` 链到 spring-ioc                                                                                                                                                                                   | 回应 `@Indexed` 用途疑问            |
| 2026-06-26 | 改写组合注解注释；扩写 `@SpringBootConfiguration` 小节，补 `@Configuration` 作用、两者区别表格与注解组合说明                                                                                                                           | 厘清「等价于 @Configuration」的含义 |
| 2026-06-26 | 拆出 startup-callbacks、webflux、virtual-threads、boot-3-migration；DI 与注解体系迁入 spring-ioc.md；母文转 hub                                                                                                                        | 文档过长（>800 行），按单一主题拆分 |
| 2026-06-26 | 澄清 Bean / `@Bean` / `@Configuration` 三者；扩写元注解；Component Scan 与 Auto-configuration 对比表；补 `META-INF` 声明文件说明                                                                                                       | 读者 Q&A 沉淀                       |
| 2026-06-27 | 补 `@Bean` 方法语义；组合注解 vs 继承用语；区分 Boot 约定与 Framework API                                                                                                                                                              | 读者 Q&A 沉淀                       |
| 2026-06-27 | `META-INF` 小节补 Redis starter 各层维护方表格                                                                                                                                                                                         | 读者 Q&A 沉淀                       |
| 2026-06-27 | `@SpringBootApplication` 下补 `@ConfigurationPropertiesScan` 小节                                                                                                                                                                      | 读者 Q&A 沉淀                       |
| 2026-06-28 | 澄清 `.imports` 在 `spring-boot-autoconfigure` 而非 starter；补 Component Scan 两层原因、classpath、IoC 容器、注解分层与 `@AutoConfiguration` 顺序                                                                                     | 读者 Q&A 沉淀                       |
| 2026-06-28 | 新增「外部化配置」「Actuator」小节；扩写 BOM 与「版本对齐」含义                                                                                                                                                                        | 读者 Q&A 沉淀                       |
| 2026-06-30 | 大幅精简加粗使用，将 `@SpringBootConfiguration`/`@EnableAutoConfiguration`/`@ComponentScan`/`@ConfigurationPropertiesScan`、三个「XML/WAR/Tomcat」分点、三种覆盖自动配置方式由加粗伪标题改为真实 `####` 标题；移除大量段落内无意义加粗 | 加粗过多，影响阅读                  |
