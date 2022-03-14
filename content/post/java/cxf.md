---
title: CXF
author: "-"
date: 2012-01-02T09:18:45+00:00
url: /?p=1413
categories:
  - Java
  - Network
  - Uncategorized

tags:
  - reprint
---
## CXF
关于 Apache CXF

Apache CXF = Celtix + XFire，Apache CXF 的前身叫 Apache CeltiXfire，现在已经正式更名为 Apache CXF 了，以下简称为 CXF。CXF 继承了 Celtix 和 XFire 两大开源项目的精华，提供了对 JAX-WS 全面的支持，并且提供了多种 Binding 、DataBinding、Transport 以及各种 Format 的支持，并且可以根据实际项目的需要，采用代码优先 (Code First) 或者 WSDL 优先 (WSDL First) 来轻松地实现 Web Services 的发布和使用。目前它仍只是 Apache 的一个孵化项目。

Apache CXF 是一个开源的 Services 框架，CXF 帮助您利用 Frontend 编程 API 来构建和开发 Services ，像 JAX-WS 。这些 Services 可以支持多种协议，比如: SOAP、XML/HTTP、RESTful HTTP 或者 CORBA ，并且可以在多种传输协议上运行，比如: HTTP、JMS 或者 JBI，CXF 大大简化了 Services 的创建，同时它继承了 XFire 传统，一样可以天然地和 Spring 进行无缝集成。

功能特性

CXF 包含了大量的功能特性，但是主要集中在以下几个方面: 

  1. 支持 Web Services 标准: CXF 支持多种 Web Services 标准，包含 SOAP、Basic Profile、WS-Addressing、WS-Policy、WS-ReliableMessaging 和 WS-Security。
  2. Frontends: CXF 支持多种"Frontend"编程模型，CXF 实现了 JAX-WS API  (遵循 JAX-WS 2.0 TCK 版本) ，它也包含一个"simple frontend"允许客户端和 EndPoint 的创建，而不需要 Annotation 注解。CXF 既支持 WSDL 优先开发，也支持从 Java 的代码优先开发模式。
  3. 容易使用:  CXF 设计得更加直观与容易使用。有大量简单的 API 用来快速地构建代码优先的 Services，各种 Maven 的插件也使集成更加容易，支持 JAX-WS API ，支持 Spring 2.0 更加简化的 XML 配置方式，等等。
  4. 支持二进制和遗留协议: CXF 的设计是一种可插拨的架构，既可以支持 XML ，也可以支持非 XML 的类型绑定，比如: JSON 和 CORBA。
  
    CXF 框架支撑环境
  
  
    CXF 框架是一种基于 Servlet 技术的 SOA 应用开发框架，要正常运行基于 CXF 应用框架开发的企业应用，除了 CXF 框架本身之外，还需要 JDK 和 Servlet 容器的支持。
  
