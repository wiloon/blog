---
title: CXF Axis2
author: "-"
date: 2011-10-31T04:24:20+00:00
url: /?p=1409
categories:
  - Java
  - Web
tags:
  - reprint
---
## CXF Axis2
[http://apache-cxf.group.iteye.com/group/wiki/1252](http://apache-cxf.group.iteye.com/group/wiki/1252)

新一代的 Web Services 框架如 Axis2、CXF 都是由现有的项目中逐渐演化而来的，Axis2 是由大家熟悉的 Axis 1.x 系列演化过来，而 Apache CXF 则是由 Celtix 和 XFire 项目整合而生，并且刚刚发布了 2.0.2 的最新版本，不过仍是 Apache 的一个孵化项目。

Axis2 是对 Axis 进行了彻底的重写的一个新项目了，它使用了新的模块化架构，更方便于功能性的扩展等等。
  
Apache CXF 则是由 XFire 和 Celtix 两个现有的项目进行了重组。

问题: 如果现有的应用程序是基于 Axis 1.x、XFire 或者 Celtix 的话，那应该怎么办？都迁移到这些新的框架上去吗？但是即使是要迁移，那应该迁移到哪个框架上去呢？
  
如果是编写一个新的 Web Services 应用程序的话，就不存在迁移的问题了，但是哪个框架是你应当选择进行使用的呢？哪个比哪个更好呢？

对于现在的应用程序的迁移，如果你的应用程序是稳定而成熟的，并且在可预知的未来的情况下，只要很少的一些需求变更要做的话，那么保存你的体力，不要去做"劳民伤财"的迁移工作了。
  
如果你的现有应用程序BUG缠身，性能，功能等等都一片糟糕的话，那就要考虑迁移了，那选哪个框架呢？先比较一下它们的不同之处: 

1. Apache CXF 支持 WS-Addressing、WS-Policy、WS-RM、WS-Security和WS-I BasicProfile
  
2. Axis2 支持 WS-Addressing、WS-RM、WS-Security和WS-I BasicProfile，WS-Policy将在新版本里得到支持
  
3. Apache CXF 是根据Spring哲学来进行编写的，即可以无缝地与Spring进行整合
  
4. Axis2 不是
  
5. Axis2 支持更多的 data bindings，包括 XMLBeans、JiBX、JaxMe 和 JaxBRI，以及它原生的 data binding (ADB) 。
  
6. Apache CXF 目前仅支持 JAXB 和 Aegis，并且默认是 JAXB 2.0，与 XFire 默认是支持 Aegis 不同，XMLBeans、JiBX 和 Castor 将在 CXF 2.1 版本中得到支持，目前版本是 2.0.2
  
7. Axis2 支持多种语言，它有 C/C++ 版本。
  
8. Apache CXF 提供方便的Spring整合方法，可以通过注解、Spring标签式配置来暴露Web Services和消费Web Services

如何抉择: 
  
1. 如果应用程序需要多语言的支持，Axis2 应当是首选了；
  
2. 如果应用程序是遵循 Spring 哲学路线的话，Apache CXF 是一种更好的选择，特别对嵌入式的 Web Services 来说；
  
3. 如果应用程序没有新的特性需要的话，就仍是用原来项目所用的框架，比如 Axis1，XFire，Celtrix 或 BEA 等等厂家自己的 Web Services 实现，就别劳民伤财了。