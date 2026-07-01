---
title: "Spring CGLIB 动态代理"
author: "-"
date: 2012-12-15T14:05:37+00:00
lastmod: 2026-06-30T21:37:11+08:00
url: cglib
categories:
  - Java
tags:
  - java
  - spring
  - AI-assisted
  - remix
aliases:
  - /p4901/
---

CGLIB（Code Generation Library）是一个运行期生成字节码的代码生成库，能在不实现接口的情况下，为一个类动态创建**子类代理**。Spring 内部大量依赖它做方法拦截（method interception）——无论是 AOP 代理还是 `@Configuration` 类的单例保证，背后用的都是 Spring 自己维护的一份 CGLIB fork（`org.springframework.cglib`），而不是外部独立发布的 `cglib.jar`。本文以 **Spring 里的 CGLIB** 为主线；原始独立 CGLIB 项目的来历、维护现状作为背景信息放在文末。

## 为什么需要 CGLIB：JDK 动态代理的限制

JDK 自 1.3 起自带动态代理（`java.lang.reflect.Proxy`），使用简单，但有一个硬性限制：**被代理的类必须实现一个或多个接口**，代理对象本质上是这些接口的另一份实现。如果要代理一个没有实现任何接口的普通类，JDK 动态代理就无能为力了——这正是 CGLIB 存在的原因。

CGLIB 的做法是：在运行期通过字节码处理框架 **[ASM](./asm.md)**，动态生成目标类的一个**子类**，重写其中的非 `final` 方法，在方法体里插入拦截逻辑，再调用原方法。因为是继承实现，所以不要求目标类实现接口，但也带来限制：**类和方法不能是 `final`**（无法被继承和重写），构造函数会被调用（生成的子类需要调用父类构造器）。

**CGLIB 和 ASM 的分工**：CGLIB 只关心「给目标类生成一个什么样的子类代理」这个业务语义层面的问题——该重写哪些方法、方法体里怎么织入拦截逻辑、生成的类怎么加载成 `Class` 对象并实例化；至于「怎么把这份子类描述翻译成合法的 `.class` 字节码」，全部委托给 ASM 完成。可以理解成：**CGLIB 决定生成一个什么样的子类，ASM 负责把这个子类真正写成字节码**——CGLIB 是构建在 ASM 之上、面向「动态生成子类代理」这个具体场景的应用层库，ASM 才是真正操作字节码指令的底层工具。

|            | JDK 动态代理                   | CGLIB                                                      |
| ---------- | ------------------------------ | ---------------------------------------------------------- |
| 实现方式   | 实现目标接口                   | 生成目标类的子类                                           |
| 前提条件   | 目标类必须实现接口             | 目标类和方法不能是 `final`                                 |
| 底层机制   | 反射（`InvocationHandler`）    | ASM 生成字节码                                             |
| 典型使用方 | Spring AOP（默认，接口存在时） | Spring AOP（无接口时）、Hibernate 延迟加载、EasyMock/jMock |

## Spring 如何使用 CGLIB：两个典型场景

### 1. Spring AOP 方法拦截

Spring AOP 优先用 JDK 动态代理；只有当目标类没有实现任何接口时，才回退（或显式配置 `proxyTargetClass=true`）使用 CGLIB 生成子类代理，在方法调用前后插入切面逻辑（比如 `@Transactional` 开启/提交事务）。

**具体怎么插入逻辑：** CGLIB 生成的子类会重写目标方法，方法体不再是原始逻辑，而是委托给一个 `MethodInterceptor.intercept(...)`；拦截器方法拿到一个 `MethodProxy`（能调用父类的原始实现），自己决定**什么时候调用原始逻辑**——可以在调用前执行代码、调用后再执行代码，甚至完全不调用原始逻辑直接返回别的结果。这套「方法调用前/后插入逻辑」的能力，正好对应 AOP 的几种通知（advice）：

| Advice 类型                                 | 拦截器行为                                                                                                      |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 前置通知（`@Before`）                       | 先执行自己的代码，再调用 `methodProxy.invokeSuper(...)`                                                         |
| 后置/返回通知（`@After`/`@AfterReturning`） | 先调用原方法，再执行自己的代码                                                                                  |
| 环绕通知（`@Around`）                       | 完全控制原方法调不调用、什么时候调用——`@Transactional` 就是典型的环绕逻辑：开事务 → 调用原方法 → 提交或回滚事务 |

需要强调：**CGLIB 本身不知道「AOP」这个概念**，它只提供通用的方法拦截能力（`MethodInterceptor`）；是 Spring AOP 在 CGLIB 生成的代理之上，把「拦截到的调用」和「切面逻辑」关联起来，才组成完整的 AOP 功能。CGLIB（连同 JDK 动态代理）只是这套机制里「生成代理 + 拦截调用」的底层实现选项。

### 2. `@Configuration` 类的 Full 模式代理

这是容易被面试问到、也最能体现"为什么需要 CGLIB"的例子。`@Configuration` 类默认 `proxyBeanMethods = true`，Spring 会用 CGLIB 生成这个配置类的子类代理：

```java
@Configuration
public class AppConfig {

    @Bean
    public ServiceA serviceA() {
        return new ServiceA(serviceB()); // 经 CGLIB 代理拦截，拿到容器里的单例 ServiceB
    }

    @Bean
    public ServiceB serviceB() {
        return new ServiceB();
    }
}
```

如果没有 CGLIB 代理，`serviceA()` 内部调用 `serviceB()` 就是一次普通 Java 方法调用，每次都会 `new` 出新对象，破坏单例语义。CGLIB 生成的子类拦截了这次方法调用，转而去容器里取已注册的单例——这就是 Spring 官方文档里说的 **Full 模式**。相对地，把 `@Bean` 方法写在普通 `@Component` 类里则是 **Lite 模式**，没有这层代理，方法互调不保证走容器。

## Spring 内嵌的 CGLIB：`org.springframework.cglib`

Spring Framework 没有直接依赖外部发布的 `cglib` jar，而是把 CGLIB 源码 fork 后重新打包进了 `spring-core` 模块，包名改成了 `org.springframework.cglib`（源码目录见 [spring-core/src/main/java/org/springframework/cglib](https://github.com/spring-projects/spring-framework/tree/main/spring-core/src/main/java/org/springframework/cglib)）。这样做首先是为了避免类路径版本冲突：应用自己引入的任何版本的 `cglib`，都不会影响 Spring 内部使用的这一份。

更关键的是维护责任的转移。Spring 团队对这份 fork 有**持续的实际维护**（该目录近期仍有提交，例如针对 `ClassNameReader` 的 ASM API 优化），会跟进修复兼容性问题、适配新版 JDK 字节码格式。所以即使原始 CGLIB 项目已经停止维护（见下文「背景：原始 CGLIB 项目」），Spring 的 AOP 代理、`@Configuration` Full 模式代理依旧能在 JDK 17、21 等新版本上正常工作——靠的是 Spring 自己维护的这份 fork，而不是上游发布的 `cglib` jar。

## 背景：原始 CGLIB 项目（历史信息）

Spring 内嵌的这份 CGLIB fork 源自一个独立的开源项目：代码托管在 [github.com/cglib/cglib](https://github.com/cglib/cglib)，采用 Apache-2.0 协议，Maven 坐标是 `groupId: cglib`、`artifactId: cglib`（或不依赖外部 ASM 的 `cglib-nodep`）。它不属于某个公司或基金会，而是由多名贡献者零散维护。

这个上游项目目前**基本处于无人维护状态**：官方仓库 README 明确写明在 JDK 17+ 上可能无法正常工作甚至完全不可用，并建议需要支持新版 JDK 的项目改用 [ByteBuddy](https://bytebuddy.net/)。这也是 Spring 当初把它 fork 进自己代码库、自行维护的原因之一——避免长期依赖一个已经停止更新的第三方库。

## 延伸阅读

- Hibernate 用 CGLIB 为持久化对象（Persistent Object）生成字节码代理，实现懒加载（对集合的延迟抓取则依赖其他机制）。
- EasyMock、jMock 用 CGLIB 为没有接口的类生成 mock 对象，支撑单元测试里的桩替换。
- 除 CGLIB 外，Groovy、BeanShell 等脚本语言也基于 ASM 生成 Java 字节码；不建议直接手写 ASM，因为它要求对 JVM 内部结构（class 文件格式、字节码指令集）有较深了解，详见 [Java ASM 与运行时字节码织入](./asm.md)。

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                            | 原因                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 2026-06-30 | 补充 JDK 动态代理 vs CGLIB 对比、Spring AOP 与 `@Configuration` Full 模式代理的具体机制与示例；标题从 `cglib` 改为 `CGLIB 动态代理`；标签由 `reprint` 改为 `remix` + `AI-assisted`                                  | 原文内容过于简单（只有背景介绍），补充实际使用场景和面试常问的原理细节      |
| 2026-06-30 | 补充项目维护现状（JDK 17+ 不建议使用、官方建议迁移 ByteBuddy）、Spring 内嵌 fork 的处理方式、项目原始仓库地址                                                                                                       | 说明 CGLIB 的归属、维护方与当前可用性，便于读者判断是否该在新项目中继续使用 |
| 2026-06-30 | 修正 Spring 内嵌 CGLIB 一节：说明上游 `cglib/cglib` 的"无人维护、JDK 17+ 可能不可用"结论不能直接套用到 Spring，Spring 自行维护 `org.springframework.cglib` fork 并持续修复兼容性                                    | 原表述容易让读者误以为 Spring 里的 CGLIB 也不支持新版 JDK，与实际情况不一致 |
| 2026-06-30 | 调整全文结构与标题（`CGLIB 动态代理` → `Spring CGLIB 动态代理`），以 Spring 内嵌的 `org.springframework.cglib` 为主线，原始 CGLIB 项目信息与 JDK 17+ 维护现状收入独立的"背景：原始 CGLIB 项目"章节作为历史/关联信息 | 明确文章定位为 Spring CGLIB 主文档，区分主线内容与背景资料                  |
| 2026-06-30 | 将正文中的 "ASM" 关联到站内文章 [Java ASM 与运行时字节码织入](./asm.md)                                                                                                                                        | 站内已有专门讲 ASM 的文章，补充内链方便读者深入了解底层机制                 |
| 2026-06-30 | 补充 CGLIB 与 ASM 的分工说明（CGLIB 决定生成什么样的子类，ASM 负责写成字节码）；展开 AOP 方法拦截一节，说明 `MethodInterceptor`/`MethodProxy` 机制与前置/后置/环绕通知的对应关系                                    | 读者 Q&A 沉淀，澄清 CGLIB 和 ASM 的层次关系、CGLIB 如何支撑 AOP 语义        |

原始来源：<http://baike.baidu.com/view/1254036.htm?fr=aladdin>
项目仓库：<https://github.com/cglib/cglib>
