---
title: javaEE
author: "-"
date: 2011-09-23T01:55:55+00:00
url: /?p=871
categories:
  - Java
tags:
  - Java

---
## javaEE
今天的程序员越来越认识到我们需要高性能、安全和可靠的服务器端技术来开发分布式的、事务性的和可移植的应用程序。在信息化的世界里，企业级应用通常需要更高的性能，更少的费用和更少的资源。

在 Java 平台中，使用 Java EE 来开发 Java 企业程序相当容易和高效。Java EE 平台为程序员提供了强大的 API，目的是为了缩短开发周期，降低应用程序复杂度，提高应用程序性能。

Java EE 通过 JCP (Java 执行委员会) 进行开发，JCP 是一个开放的国际组织，其中的成员包括 Oracle、IBM、Apache 等，JCP 负责所有的 Java 技术。其中的专家组会提交 Java EE 相关的 JSR (Java 标准请求) 。JCP 需要确保 Java 标准的稳定和跨平台兼容性。

Java EE 6 平台最主要的目标是为大量的 Java EE 组件提供共同的基础。程序员可以更多地使用 annotation (元数据注释) 来代替 XML 配置文件，更多地使用 POJO 来进行来发，并且应用程序的打包部署过程也更加简单。

Java EE 6 包括了以下新的特性: 

Profiles

我们知道 Java EE 规范本身相当庞大，如果我们需要开发的应用使用不到这么多的 Java EE 技术，那么完全没有必要引入这么多的 Java EE 技术到我们的应用程序中去。例如，如果要构建一个类似于 SOA 的应用程序，会用到消息，事务，持久化以及 Web Services ，但犯不着需要使用像 JSP 或 JSF 这类的展示层技术。

因此，从 Java EE 6 开始引入了 Profiles 的概念，在 Java EE 中定义了包含所有 Java EE 技术的 Profile 叫做 Full Profile，其它所有的 Profile 都是 Full Profile 的子集。

例如在 Java EE 6 规范中引入了轻量级的 Web Profile，它就仅仅只包含了一些最有可能在大绝大多数 Java web 应用程序中使用的 API。我们通过下表可以对比 Web Profile 和 Full Profile 的区别。

API Web Profile Full Profile
  
Servlet 3.0
  
JSP 2.2
  
JSTL 1.2
  
EL 1.2
  
JSF 2.0 支持
  
WebBeans 1.0 (?) 支持 支持
  
EJB 3.1 (Lite) 支持 支持
  
EJB 3.1 (Full) 支持
  
JPA 2.0 支持 支持
  
JTA 1.1 支持 支持
  
JMS 1.1 支持
  
JavaMail 1.4 支持
  
JAX-WS 2.2 支持
  
JAX-RS 1.1 支持
  
JAXB 2.2 支持
  
JACC 1.0 支持
  
JCA 1.6 支持
  
新的技术

开发 RESTful Web Services 的 Java API (JAX-RS) 
  
托管 Beans
  
上下文依赖注入 (JSR 299) ，通常也叫做 CDI
  
Java 依赖注入 (JSR 330) 
  
Bean 验证 (JSR 303) 
  
Java Authentication Service Provider Interface for Containers (JASPIC)


J2EE是一系列技术标准所组成的平台，包括: 

  * [Applet][1]{.mw-redirect} - Java Applet
  * [EJB][2] - 企业级[JavaBean][3]{.mw-redirect} (Enterprise Java Beans) 
  * [JAAS][4] - Java Authentication and Authorization Service
  * [JACC][5]{.new} - J2EE Authorization Contract for Containers
  * [JAF][6]{.new} - Java Beans Activation Framework
  * [JAX-RPC][7] - Java API for XML-Based Remote Procedure Calls
  * [JAX-WS][8] - Java API for XML Web Services
  * [JAXM][9] - Java API for XML Messaging
  * [JAXP][10] - Java XML解析API (Java API for XML Processing) 
  * [JAXR][11] - Java API for XML Registries
  * [JCA][12]{.mw-redirect} - J2EE连接器架构 (J2EE Connector Architecture) 
  * [JDBC][13]{.mw-redirect} - Java数据库联接 (Java Database Connectivity) 
  * [JMS][14]{.mw-redirect} - Java消息服务 (Java Message Service) 
  * [JMX][15] - Java Management
  * [JNDI][16]{.new} - Java名稱与目录接口 (Java Naming and Directory Interface) 
  * [JSF][17]{.mw-disambig} - Java Server Faces
  * [JSP][18] - Java服务器页面 (Java Server Pages) 
  * [JSTL][19] - Java服务器页面标准标签库 (Java Server Pages Standard Tag Library) 
  * [JTA][20]{.mw-disambig} - Java事务API (Java Transaction API) 
  * [JavaMail][21]{.new}
  * [Servlet][22]{.mw-redirect} - Java Servlet [API][23]{.mw-redirect}
  * [StAX][24] - Streaming APIs for XML Parsers
  * [WS][25]{.mw-disambig} - Web Services
  *

 [1]: https://zh.wikipedia.org/wiki/Applet "Applet"
 [2]: https://zh.wikipedia.org/wiki/EJB "EJB"
 [3]: https://zh.wikipedia.org/wiki/JavaBean "JavaBean"
 [4]: https://zh.wikipedia.org/wiki/JAAS "JAAS"
 [5]: https://zh.wikipedia.org/w/index.php?title=JACC&action=edit&redlink=1 "JACC (页面不存在) "
 [6]: https://zh.wikipedia.org/w/index.php?title=JAF&action=edit&redlink=1 "JAF (页面不存在) "
 [7]: https://zh.wikipedia.org/wiki/JAX-RPC "JAX-RPC"
 [8]: https://zh.wikipedia.org/wiki/JAX-WS "JAX-WS"
 [9]: https://zh.wikipedia.org/wiki/JAXM "JAXM"
 [10]: https://zh.wikipedia.org/wiki/JAXP "JAXP"
 [11]: https://zh.wikipedia.org/wiki/JAXR "JAXR"
 [12]: https://zh.wikipedia.org/wiki/JCA "JCA"
 [13]: https://zh.wikipedia.org/wiki/JDBC "JDBC"
 [14]: https://zh.wikipedia.org/wiki/JMS "JMS"
 [15]: https://zh.wikipedia.org/wiki/JMX "JMX"
 [16]: https://zh.wikipedia.org/w/index.php?title=JNDI&action=edit&redlink=1 "JNDI (页面不存在) "
 [17]: https://zh.wikipedia.org/wiki/JSF "JSF"
 [18]: https://zh.wikipedia.org/wiki/JSP "JSP"
 [19]: https://zh.wikipedia.org/wiki/JSTL "JSTL"
 [20]: https://zh.wikipedia.org/wiki/JTA "JTA"
 [21]: https://zh.wikipedia.org/w/index.php?title=JavaMail&action=edit&redlink=1 "JavaMail (页面不存在) "
 [22]: https://zh.wikipedia.org/wiki/Servlet "Servlet"
 [23]: https://zh.wikipedia.org/wiki/API "API"
 [24]: https://zh.wikipedia.org/wiki/StAX "StAX"
 [25]: https://zh.wikipedia.org/wiki/WS "WS"