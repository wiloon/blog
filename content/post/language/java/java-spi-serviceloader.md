---
title: "Java SPI 与 ServiceLoader"
author: "-"
date: 2017-11-07T09:24:25+00:00
lastmod: 2026-06-27T04:52:28+08:00
url: java-spi-serviceloader
categories:
  - language
tags:
  - java
  - spi
  - serviceloader
  - remix
  - AI-assisted
aliases:
  - /p11372/
---

## 是什么

SPI（Service Provider Interface，服务提供者接口）是 Java 内置的**插件机制**：允许第三方在不修改调用方代码的前提下，提供接口的实现。

核心思路一句话：

```text
调用方只依赖接口 → 实现由 ServiceLoader 在运行时发现
```

调用方编译期只认接口，不写死任何实现类；具体用哪个实现，由 classpath 上的实现库通过约定文件「自报家门」，由 `java.util.ServiceLoader` 在运行时加载并实例化。这与 IoC 的思想类似——把装配的控制权移到程序之外，在模块化设计里尤其重要。

## 三个组成部分

| 组成 | 说明 |
| ---- | ---- |
| **接口（Service）** | 由框架或标准库定义，如 `java.sql.Driver` |
| **实现（Provider）** | 由第三方库提供，如 `com.mysql.cj.jdbc.Driver` |
| **注册文件** | `META-INF/services/<接口全限定名>`，内容是实现类的全限定名 |

注册文件规则：

- 文件名是服务接口的完全限定二进制名称
- 每行一个实现类的全限定名；空行、行首 `#` 注释会被忽略
- 文件必须使用 **UTF-8** 编码
- 提供者类必须有**无参构造方法**，以便被反射实例化

## 工作流程

```text
① 调用方：ServiceLoader.load(Driver.class)
      ↓
② JVM 扫描 classpath 上所有 jar 里的
   META-INF/services/java.sql.Driver
      ↓
③ 读出文件中的实现类名，反射实例化
      ↓
④ 返回一个可迭代所有实现的迭代器
```

`ServiceLoader` 以**延迟方式**查找并实例化：维护已加载实现的缓存，`iterator()` 先返回缓存中的元素，再按需查找剩余实现并依次加入缓存，可用 `reload()` 清缓存。

## 一个完整例子

接口与两个实现：

```java
package com.example.api;

public interface Greeting {
    void sayHi();
}

public class GreetingBeijing implements Greeting {
    public void sayHi() { System.out.println("hi from beijing"); }
}

public class GreetingZhengzhou implements Greeting {
    public void sayHi() { System.out.println("hi from zhengzhou"); }
}
```

注册文件 `src/main/resources/META-INF/services/com.example.api.Greeting`：

```text
com.example.api.GreetingZhengzhou
com.example.api.GreetingBeijing
```

加载并调用：

```java
public class Demo {
    public static void main(String[] args) {
        ServiceLoader<Greeting> loader = ServiceLoader.load(Greeting.class);
        for (Greeting g : loader) {
            System.out.println(g.getClass().getName());
            g.sayHi();
        }
    }
}
```

## 常见用途

| 接口 | 实现（第三方 jar） |
| ---- | ------------------ |
| `java.sql.Driver` | MySQL、PostgreSQL 驱动 |
| `org.slf4j.spi.SLF4JServiceProvider` | Logback、Log4j2 |
| `java.nio.file.spi.FileSystemProvider` | zip、嵌套 jar 文件系统 |
| `javax.crypto.JceSecurity` | BouncyCastle 等加密提供者 |

自 Java 6 起，JDBC 驱动通过 SPI 自注册，不再需要 `Class.forName("com.mysql.Driver")`。

## ServiceLoader 与 ClassLoader

两者都能加载类，但定位不同：

- **ClassLoader** 是「万能加载器」，按双亲委托加载任意类（见 [classloader](./classloader.md)）。
- **ServiceLoader** 装载的是「实现了某个共同接口的一组实现类」，依赖 `META-INF/services/` 约定文件，且实现了 `Iterable` 接口。

## 与 Spring 自动配置的区别

Spring Boot 的自动配置读取的是 `META-INF/spring/...AutoConfiguration.imports`，那是 **Spring Boot 自己的约定**，不是 JDK SPI；而 `META-INF/services/` 才是 JDK 标准的 `ServiceLoader` 机制。两者都用 `META-INF/` 下的声明文件，但分属不同体系，详见 [Spring Boot §Auto-configuration](./spring/spring-boot.md#auto-configuration自动配置)。

Spring Boot 可执行 JAR 里也用到 SPI——`NestedFileSystemProvider` 就是通过 `META-INF/services/java.nio.file.spi.FileSystemProvider` 注册的，用于读取嵌套 jar，见 [Spring Boot Executable JAR](./spring/spring-boot-executable-jar.md)。

## 参考

- [classloader](./classloader.md)
- [Spring Boot §Auto-configuration](./spring/spring-boot.md#auto-configuration自动配置)
- [Spring Boot Executable JAR](./spring/spring-boot-executable-jar.md)
- [ServiceLoader (Java SE API)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ServiceLoader.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-27 | 重写为结构化中文文档：补充 SPI 三要素、工作流程、与 Spring 自动配置区别；删除 reprint 标签 | 原文为低质量转载；合并 comments-tree 启动打包文档的 SPI 章节 |
