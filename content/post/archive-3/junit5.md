---
title: junit
author: "-"
date: 2020-01-09T02:27:43+00:00
url: /?p=15303
categories:
  - Inbox
tags:
  - reprint
---
## junit

### junit5

JUnit5的第一个可用性版本是在2017年9月10日发布的。

JUnit5架构
  
相比JUnit4，JUnit5由三个不同的子项目及不同的模块组成。

JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage

1. JUnit Platform
  
    启动Junit测试、IDE、构建工具或插件都需要包含和扩展Platform API，它定义了TestEngine在平台运行的新测试框架的API。
  
    它还提供了一个控制台启动器，可以从命令行启动Platform，为Gradle和Maven插件提供支持。

2. JUnit Jupiter
  
    它用于编写测试代码的新的编程和扩展模型。它具有所有新的Junit注释和TestEngine实现来运行这些注释编写的测试。

3. JUnit Vintage
  
    它主要的目的是支持在JUnit5的测试代码中运行JUnit3和4方式写的测试，它能够向前兼容之前的测试代码。
  
    [https://tonydeng.github.io/2017/10/09/junit-5-tutorial-introduction/](https://tonydeng.github.io/2017/10/09/junit-5-tutorial-introduction/)

### 安装

你可以在Maven或Gradle项目中使用JUnit5，包含最小的两个依赖关系，即junit-jupiter-engince和junit-platform-runner。

```xml

<properties>
    <junit.jupiter.version>5.5.2</junit.jupiter.version>
    <junit.platform.version>1.5.2</junit.platform.version>
</properties>

<dependency>
    <groupId>org.junit.jupiter</groupId>
    junit-jupiter-engine</artifactId>
    <version>${junit.jupiter.version}</version>
</dependency>
<dependency>
    <groupId>org.junit.platform</groupId>
    junit-platform-runner</artifactId>
    <version>${junit.platform.version}</version>
    <scope>test</scope>
</dependency>
```

```java
import org.junit.jupiter.api.Test;

public class AppTest {
    @Test
    public void Test() {
        System.out.println("foo");
    }
}

```

Annotations 描述
  
@BeforeEach 在方法上注解，在每个测试方法运行之前执行。
  
@AfterEach 在方法上注解，在每个测试方法运行之后执行
  
@BeforeAll 该注解方法会在所有测试方法之前运行，该方法必须是静态的。
  
@AfterAll 该注解方法会在所有测试方法之后运行，该方法必须是静态的。
  
@Test 用于将方法标记为测试方法
  
@DisplayName 用于为测试类或测试方法提供任何自定义显示名称
  
@Disable 用于禁用或忽略测试类或方法
  
@Nested 用于创建嵌套测试类
  
@Tag 用于测试发现或过滤的标签来标记测试方法或类
  
@TestFactory 标记一种方法是动态测试的测试工场

[https://sjyuan.club/junit5/user-guide-cn/#11-junit-5-%E6%98%AF%E4%BB%80%E4%B9%88](https://sjyuan.club/junit5/user-guide-cn/#11-junit-5-%E6%98%AF%E4%BB%80%E4%B9%88)
