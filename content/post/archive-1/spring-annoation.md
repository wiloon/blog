---
title: Spring annoation
author: "-"
date: 2012-12-18T04:27:33+00:00
url: /?p=4925
categories:
  - Java
  - Web
tags:$
  - reprint
---
## Spring annoation
@PostConstruct 和 @PreDestroy

Spring 容器中的 Bean 是有生命周期的,Spring 允许在 Bean 在初始化完成后以及 Bean 销毁前执行特定的操作,您既可以通过实现 InitializingBean/DisposableBean 接口来定制初始化之后 / 销毁之前的操作方法,也可以通过 <bean> 元素的 init-method/destroy-method 属性指定初始化之后 / 销毁之前调用的操作方法。关于 Spring 的生命周期,笔者在《精通 Spring 2.x—企业应用开发精解》第 3 章进行了详细的描述,有兴趣的读者可以查阅。

JSR-250 为初始化之后/销毁之前方法的指定定义了两个注释类,分别是 @PostConstruct 和 @PreDestroy,这两个注释只能应用于方法上。标注了 @PostConstruct 注释的方法将在类实例化后调用,而标注了 @PreDestroy 的方法将在类销毁之前调用。