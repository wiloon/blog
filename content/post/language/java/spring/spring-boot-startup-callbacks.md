---
title: "Spring Boot Startup Callbacks: 应用启动后执行逻辑"
author: wiloon
date: 2026-06-26T21:44:56+08:00
lastmod: 2026-06-26T21:44:56+08:00
url: spring-boot-startup-callbacks
categories:
  - java
tags:
  - AI-assisted
  - java
  - remix
  - spring
  - spring boot
---

若要在 **Spring 应用上下文已就绪** 之后执行一段初始化代码，常见做法如下。多个 Bean 可同时实现同一类接口，使用 `@Order` 或 `Ordered` 控制顺序。框架总览见 [Spring Boot](./spring-boot.md)。

## `ApplicationRunner` 与 `CommandLineRunner`

二者都会在 `SpringApplication` 启动流程末尾被调用。需要结构化解析命令行参数（如 `key=value` 形式）时，优先使用 `ApplicationRunner`（入参为 `ApplicationArguments`）；只关心原始字符串数组时用 `CommandLineRunner` 即可。

```java
@Component
@Order(1)
public class SeedDataRunner implements ApplicationRunner {
    @Override
    public void run(ApplicationArguments args) {
        // post-startup logic
    }
}

@Component
@Order(2)
public class BannerRunner implements CommandLineRunner {
    @Override
    public void run(String... args) {
        // post-startup logic
    }
}
```

## `@PostConstruct`

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

## `ServletContextAware` 与 `ServletContextListener`

仅在 **基于 Servlet 的 Web 应用** 中有意义：前者在 Bean 属性填充后注入 `ServletContext`；后者监听 Web 应用启动与销毁。在 Spring Boot 中注册 `ServletContextListener` 往往需要 `@ServletComponentScan`、`ServletListenerRegistrationBean` 或容器相关配置配合，具体写法随场景选择。

## 静态代码块

`static { ... }` 在类加载阶段执行，时机早于 Spring 依赖注入，**不适合**编写依赖容器中其他 Bean 的逻辑。

## 参考

- [Spring Boot](./spring-boot.md)
- [Spring IoC §Bean 的生命周期](./spring-ioc.md#bean-的生命周期)
