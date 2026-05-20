---
title: Jetty
author: "-"
date: 2012-12-16T03:32:06+00:00
lastmod: 2026-05-20T10:15:58+08:00
url: jetty
categories:
  - Java
  - Web
tags:
  - java
  - jetty
  - tomcat
  - servlet
  - remix
  - AI-assisted
aliases:
  - /p4907/
  - /p7308/
  - /p4909/
  - jetty-tomcat
---
## Jetty

Jetty 是一个开源的 servlet 容器，它为基于 Java 的 web 内容（例如 JSP 和 servlet）提供运行环境。Jetty 使用 Java 编写，API 以一组 JAR 包的形式发布。开发人员可以将 Jetty 容器实例化成一个对象，为一些独立运行（stand-alone）的 Java 应用提供网络和 web 连接。

### 易用性

易用性是 Jetty 设计的基本原则，主要体现在：

- 通过 XML 或 API 配置 Jetty
- 默认配置可满足大部分需求
- 将 Jetty 嵌入应用程序只需很少的代码

### 可扩展性

在使用了 Ajax 的 Web 2.0 应用中，每个连接需要保持更长时间，线程和内存消耗会明显增加。Jetty 在这方面有优势：

- 即使在大量服务请求下，系统性能仍可保持可接受水平
- 利用 Continuation 机制处理大量用户请求及长连接
- 接口设计良好，当某种实现无法满足需求时，可方便地修改 Jetty 的特定实现

### 易嵌入性

Jetty 设计之初就是作为优秀组件来设计的，可非常容易地嵌入应用程序，无需为使用 Jetty 而大幅修改程序。某种程度上，也可以把 Jetty 理解为一个嵌入式 Web 服务器。

Jetty 可作为嵌入式服务器使用，运行速度较快且轻量，可在 Java 测试用例中控制其运行，使自动化测试不再依赖外部环境。

## Jetty vs Tomcat

参考：[Jetty 与 Tomcat 的比较（IBM developerWorks）](http://www.ibm.com/developerworks/cn/java/j-lo-jetty/)

Tomcat 和 Jetty 都是应用广泛的 Servlet 引擎。Tomcat 经过长期发展，已被市场广泛接受，尤其在企业级应用中仍是首选；Jetty 市场份额也在不断提高，主要得益于其在技术上的优势。

### 架构比较

从架构上看，Jetty 比 Tomcat 更简单。Jetty 的所有组件都基于 Handler 实现，也支持 JMX，主要功能扩展都可通过 Handler 完成。可以说 Jetty 是面向 Handler 的架构；而 Tomcat 以多级容器构建，架构设计上有各自的「核心」组件。

从设计模式看，Handler 的设计是责任链模式，`HandlerCollection` 可帮助构建链，`ScopeHandler` 可控制链的访问顺序。Jetty 还用观察者模式控制生命周期，继承 `LifeCycle` 接口的对象可由 Jetty 统一管理，因此扩展 Jetty 相对简单。

相比之下，Tomcat 整体更复杂，核心在于容器设计（从 Server 到 Service 再到 engine 等）。这种分层有利于扩展，但也把应用服务器内部结构暴露给使用者，扩展前需要先理解整体设计，学习成本更高。Tomcat 也有类似责任链的设计（如 Pipeline 的 Valve），实现 Valve 与实现 Handler 的难度相当。表面上看 Tomcat 功能更全（很多工作已内置），而 Jetty 更强调「能做什么、如何做」，由开发者按需实现。

打个比方：Tomcat 直接给出 1+1=2、1+2=3 等结果，你要算其它数需按它给的公式来；Jetty 则告诉你加减乘除的规则，你可以自己运算。掌握 Jetty 后，其灵活性会非常明显。

### 性能比较

单纯比较两者性能意义不大，它们面向的场景不同。从架构上看，Tomcat 在处理少量非常繁忙、连接生命周期较短的场景时更有优势；Jetty 则擅长同时处理大量连接并长时间保持，例如 web 聊天应用（淘宝 web 旺旺曾使用 Jetty 作为 Servlet 引擎）。

Jetty 架构简单，可按需加载组件，减少内存开销和请求过程中的临时对象，有利于性能。Jetty 默认使用 NIO 处理 I/O；Tomcat 默认使用 BIO。处理静态资源时，Tomcat 的性能通常不如 Jetty。

### 特性比较

作为标准 Servlet 引擎，两者都支持 Servlet 规范及 Java EE 相关规范。Tomcat 使用更广，对这些规范的支持往往更全面，很多特性已直接集成。Jetty 的应变更快，一方面因为社区更活跃，另一方面因为修改更简单——替换相应组件即可；Tomcat 整体结构复杂，功能修改相对缓慢，对新 Servlet 规范的支持有时会晚于预期。
