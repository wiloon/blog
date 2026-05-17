---
title: AOP
author: "-"
date: 2012-01-07T07:58:58+00:00
lastmod: 2026-05-12T14:25:47+08:00
url: aop
categories:
  - Java
tags:
  - java
  - spring
  - AOP
  - remix
  - AI-assisted
aliases:
  - /p2097/
---

AOP（Aspect-Oriented Programming，面向切面编程）是对 OOP 的补充，用于将**横切关注点**（cross-cutting concerns）从业务逻辑中分离出来，集中管理。典型横切关注点包括：日志记录、事务管理、权限校验、性能监控、缓存、同步等——这些逻辑如果分散在每个方法里，既冗余又难以维护。

AOP 实际是 GoF 设计模式的延续，设计模式孜孜不倦追求的是调用者和被调用者之间的解耦，AOP 可以说也是这种目标的一种实现。

## AOP 解决了什么问题

在没有 AOP 的情况下，每个业务方法都要亲自处理横切逻辑：

```java
// 没有 AOP：每个方法都要重复写日志、事务、权限检查
public User findById(Long id) {
    log.info("开始查询 user={}", id);          // 日志
    checkPermission("user:read");              // 权限
    Transaction tx = db.beginTransaction();    // 事务
    try {
        User user = db.query(id);              // 真正的业务逻辑
        tx.commit();
        return user;
    } catch (Exception e) {
        tx.rollback();
        throw e;
    } finally {
        log.info("查询结束");                   // 日志
    }
}
```

这带来三个问题：

1. **重复代码**：日志、事务、权限逻辑散落在每个方法里，修改一处要改几十个地方
2. **职责混乱**：业务方法承担了与业务无关的基础设施职责，难以阅读
3. **无法集中管控**：想统一修改日志格式或事务策略，必须逐一修改每个方法

AOP 把这些横切逻辑**抽取到切面里统一管理**，业务方法只写业务：

```java
// 有 AOP：业务方法只写业务，其余由切面处理
@Transactional
@PreAuthorize("hasRole('USER')")
public User findById(Long id) {
    return db.query(id);   // 只剩业务逻辑
}
```

## Spring AOP

Spring AOP 基于**动态代理**实现，不修改原始类的字节码，而是在运行时生成代理对象，在方法调用前后插入额外逻辑。

### 版本历史

Spring AOP 从 **Spring 1.0（2004年）** 就已存在，是 Spring Framework 最早的核心特性之一：

| 版本            | 发布时间   | AOP 能力                                                                      |
| --------------- | ---------- | ----------------------------------------------------------------------------- |
| Spring 1.0      | 2004年3月  | Spring AOP 首次发布，只能用 XML + 接口（`MethodInterceptor`）写切面，配置繁琐 |
| Spring 1.2      | 2004年     | 支持 AspectJ 切点表达式，但仍需 XML 配置                                      |
| **Spring 2.0**  | **2006年** | **引入 `@Aspect`、`@Around`、`@Before` 等注解**，切面写法大幅简化             |
| Spring 3.0      | 2009年     | 支持 `@EnableAspectJAutoProxy`，可以完全不写 XML                              |
| Spring Boot 1.0 | 2014年     | `spring-boot-starter-aop` 自动配置，零配置启用                                |

`@Around`、`@Before` 等注解来自 **AspectJ 项目**（`org.aspectj.lang.annotation.*`），Spring 2.0 开始借用这套注解语法，底层仍用自己的动态代理执行，不依赖 AspectJ 的编译器或织入器。

### Spring MVC 时代 vs Spring Boot 时代

`@Around` 等注解本身没有变化，区别在于**谁来开启代理机制**。

**Spring MVC 时代（需手动开启）：**

必须在 `applicationContext.xml` 里显式声明，否则 `@Aspect` 注解完全不生效：

```xml
<!-- 开启 AspectJ 注解代理 -->
<aop:aspectj-autoproxy/>

<!-- 切面类也要注册成 Bean -->
<bean class="com.example.aspect.LogAspect"/>
```

或 Java Config 写法（Spring 3.0+，不写 XML，但仍需显式声明）：

```java
@Configuration
@EnableAspectJAutoProxy    // 必须加，否则 @Aspect 不生效
public class AppConfig {

    @Bean
    public LogAspect logAspect() {
        return new LogAspect();
    }
}
```

**Spring Boot 时代（自动开启）：**

加一个依赖，框架自动完成上述所有配置：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

Spring Boot 的 `AopAutoConfiguration` 检测到 `aspectjweaver` 在 classpath 上时，自动等效于加了 `@EnableAspectJAutoProxy`。切面类只需 `@Component` + `@Aspect` 即可被扫描并生效，不需要任何手动配置。

### 核心概念

| 术语                     | 说明                                                                |
| ------------------------ | ------------------------------------------------------------------- |
| **Aspect（切面）**       | 横切关注点的模块化封装，用 `@Aspect` 标注的类                       |
| **Join Point（连接点）** | 程序执行过程中可以被拦截的点，Spring AOP 中**只支持方法执行**这一种 |
| **Pointcut（切入点）**   | 定义「拦截哪些方法」的表达式，筛选出感兴趣的 Join Point             |
| **Advice（通知）**       | 在切入点处执行的逻辑，即「做什么」                                  |
| **Weaving（织入）**      | 将切面应用到目标对象的过程，Spring AOP 在运行时织入                 |

### Advice 类型

| 注解              | 执行时机                                         |
| ----------------- | ------------------------------------------------ |
| `@Before`         | 方法执行**前**                                   |
| `@AfterReturning` | 方法**正常返回后**                               |
| `@AfterThrowing`  | 方法**抛出异常后**                               |
| `@After`          | 方法执行**后**（无论正常还是异常，类似 finally） |
| `@Around`         | 方法执行**前后**，最灵活，可以控制是否执行原方法 |

### 示例：记录接口耗时

```java
@Aspect
@Component
public class TimingAspect {

    // Pointcut：拦截 com.example.controller 包下所有类的所有方法
    @Around("execution(* com.example.controller..*(..))") 
    public Object logTiming(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            return pjp.proceed();   // 执行原方法
        } finally {
            long elapsed = System.currentTimeMillis() - start;
            System.out.printf("%s 耗时 %dms%n", pjp.getSignature(), elapsed);
        }
    }
}
```

不需要修改任何 Controller，所有接口自动被计时。

### Pointcut 表达式常用语法

```
execution(修饰符? 返回类型 类路径? 方法名(参数) 异常?)
```

```java
// 拦截指定包下所有方法（含子包）
execution(* com.example.service..*(..))

// 拦截特定注解标注的方法
@annotation(org.springframework.transaction.annotation.Transactional)

// 拦截特定类的特定方法
execution(* com.example.UserService.findById(Long))
```

多个切入点可以用 `&&`、`||`、`!` 组合。

`*.*` 只匹配**当前包**，不含子包；`..`（两个点）匹配当前包及所有子包：

```java
// 只匹配 com.example.service 包（不含子包）
execution(* com.example.service.*.*(..))

// 匹配 com.example.service 包及所有子包
execution(* com.example.service..*(..))
```

实际项目中通常用两个点，否则 Service 类一旦移入子包切面就失效。

### Spring AOP vs AspectJ

Spring AOP 基于动态代理，**只能拦截 Spring Bean 的方法调用**，且同一个 Bean 内部的方法互调不会触发 AOP（因为内部调用绕过了代理）。

AspectJ 是完整的 AOP 框架，在编译期或类加载期织入字节码，可以拦截任意方法、构造器、字段访问，功能更强但配置更复杂。Spring AOP 可以集成 AspectJ 的注解语法（`@Aspect`、`@Pointcut` 等），但底层仍是代理，不是字节码织入。

**绝大多数业务场景 Spring AOP 已经够用**，只有需要拦截非 Spring 管理对象、同类内部方法调用等场景才需要引入完整 AspectJ。

### Spring AOP 与 AspectJ 混合使用

两者可以在同一应用中共存，常见的三种组合方式：

**方式 1：Spring AOP 借用 AspectJ 注解（最常见，默认方式）**

`@Aspect`、`@Around`、`@Before` 等注解来自 AspectJ，但织入由 Spring 代理完成。`spring-boot-starter-aop` 已自动引入 `aspectjweaver`，无需额外配置。

```java
@Aspect          // AspectJ 注解
@Component
public class MyAspect {
    @Around("execution(* com.example.service..*(..))") // AspectJ Pointcut 语法
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        // Spring 代理执行，不是 AspectJ 字节码织入
        return pjp.proceed();
    }
}
```

**方式 2：启用 AspectJ LTW（类加载期织入）**

AspectJ 真正接管织入，可拦截内部方法调用和非 Spring Bean。需加 JVM 参数：

```bash
java -javaagent:aspectjweaver.jar -jar app.jar
```

或在 Spring 配置中启用：

```java
@Configuration
@EnableLoadTimeWeaving
public class AppConfig { }
```

**方式 3：两种切面并存**

部分切面走 Spring AOP（代理），部分切面走 AspectJ 字节码织入，互不干扰。

| 场景                              | 选择                             |
| --------------------------------- | -------------------------------- |
| 只拦截 Spring Bean 方法           | Spring AOP（默认，无需额外配置） |
| 需要拦截内部调用 / 非 Spring 对象 | AspectJ LTW                      |
| 两种需求都有                      | 可以共存，不冲突                 |

### 内部调用问题

```java
@Service
public class OrderService {

    public void placeOrder() {
        validate();  // ❌ 内部调用，AOP 不生效，validate() 上的切面被绕过
    }

    @Transactional
    public void validate() { ... }
}
```

解决方法：通过 `ApplicationContext` 获取自身的代理对象，或拆分为两个 Bean。

## 在 Spring Web 开发中的具体应用

Spring 内置了大量基于 AOP 的功能，开发 Web 应用时几乎每个层次都在用：

### Controller 层

| 场景     | 注解 / 机制                         | 说明                                 |
| -------- | ----------------------------------- | ------------------------------------ |
| 权限校验 | `@PreAuthorize("hasRole('ADMIN')")` | Spring Security 在方法执行前校验权限 |
| 限流     | `@RateLimiter`（Resilience4j）      | 拦截方法，超过阈值直接拒绝           |
| 接口日志 | 自定义 `@Around` 切面               | 记录请求参数、响应结果、耗时         |

### Service 层

| 场景     | 注解 / 机制                       | 说明                                             |
| -------- | --------------------------------- | ------------------------------------------------ |
| 事务管理 | `@Transactional`                  | 方法前开启事务，正常返回提交，异常回滚           |
| 缓存     | `@Cacheable` / `@CacheEvict`      | 命中缓存直接返回，不执行方法体；或方法后清除缓存 |
| 熔断降级 | `@CircuitBreaker`（Resilience4j） | 故障率超阈值时自动降级                           |
| 重试     | `@Retryable`（Spring Retry）      | 方法抛出异常时自动重试                           |

### 各层通用

| 场景           | 实现方式                                |
| -------------- | --------------------------------------- |
| 慢方法监控     | `@Around` 切面，记录超过阈值的调用      |
| 异常统一处理   | `@AfterThrowing` 切面，上报异常监控     |
| 方法级参数校验 | `@Validated` + `@Valid`（底层也是 AOP） |

### 一个完整的调用链示意

```
HTTP 请求
  → Controller.findUser()
       ↕ Spring Security AOP（权限校验）
       ↕ 日志切面（记录入参）
  → Service.findUser()
       ↕ @Transactional AOP（开启事务）
       ↕ @Cacheable AOP（查缓存，命中则返回）
  → Repository.findById()   ← 真正的数据库查询
       ↕ @Transactional AOP（提交事务）
       ↕ 日志切面（记录耗时）
  → 返回响应
```

可以看到，`@Transactional`、`@PreAuthorize`、`@Cacheable` 这些日常常用的注解，**底层全都是 AOP**。Spring 把这些通用能力封装成注解，让业务代码只需要贴一个注解，背后的切面由框架统一处理。


## @Transactional

`@Transactional` 是 Spring 基于 AOP 封装的事务管理注解。Spring 在方法执行前开启数据库事务，正常返回时提交，抛出异常时回滚。

### 典型使用场景

**1. 多步写操作必须原子完成**

```java
@Transactional
public void transferMoney(Long fromId, Long toId, BigDecimal amount) {
    accountDao.deduct(fromId, amount);   // 扣款
    accountDao.add(toId, amount);        // 入账
    // 任一步失败，两步都回滚，不会出现"扣了款但没入账"
}
```

**2. 批量写入**

```java
@Transactional
public void batchInsert(List<Order> orders) {
    for (Order order : orders) {
        orderDao.insert(order);
    }
    // 全部成功才提交；任何一条失败，全部回滚
}
```

**3. 读写组合（防幻读）**

```java
@Transactional
public void deductStock(Long productId, int qty) {
    Product p = productDao.findById(productId);  // 读
    if (p.getStock() < qty) throw new RuntimeException("库存不足");
    productDao.deductStock(productId, qty);      // 写
    // 同一事务内，读到的库存和写时的库存一致
}
```

### 常用参数

| 参数              | 说明                                                           |
| ----------------- | -------------------------------------------------------------- |
| `rollbackFor`     | 指定哪些异常触发回滚，默认只回滚 `RuntimeException` 和 `Error` |
| `noRollbackFor`   | 指定哪些异常不回滚                                             |
| `propagation`     | 事务传播行为，默认 `REQUIRED`（没有事务就新建，有就加入）      |
| `readOnly = true` | 只读事务，数据库可做优化（如跳过脏检查），适合纯查询           |
| `timeout`         | 超时秒数，超时自动回滚                                         |

### 常见的坑

**坑 1：受检异常不回滚**

```java
@Transactional  // 默认只回滚 RuntimeException
public void save() throws IOException {
    fileService.write();   // IOException 是受检异常，不触发回滚！
    dao.insert(record);
}

// 修复：
@Transactional(rollbackFor = Exception.class)
```

**坑 2：内部调用失效**

```java
@Service
public class OrderService {
    public void placeOrder() {
        saveOrder();   // ❌ 内部调用，@Transactional 不生效
    }

    @Transactional
    public void saveOrder() { ... }
}
```

原因同 [AOP 内部调用问题](#内部调用问题)：内部调用绕过了代理对象。

**坑 3：`private` 方法无效**

```java
@Transactional          // ❌ 无效，代理无法重写 private 方法
private void doSave() { ... }
```

`@Transactional` 应标注在 `public` 方法上。
