---
title: BeanFactory, ApplicationContext
author: "-"
date: 2015-01-26T01:04:59+00:00
url: /?p=7286
categories:
  - Uncategorized
tags:
  - Spring

---
## BeanFactory, ApplicationContext
http://blog.csdn.net/liaomin416100569/article/details/4924183


org.springframework.beans.factory.BeanFactory 是Spring IoC容器的实际代表者,


IoC容器负责容纳此前所描述的bean,并对bean进行管理。


在Spring中,BeanFactory是IoC容器的核心接口。 它的职责包括: 实例化、定位、配置


应用程序中的对象及建立这些对象间的依赖。


Spring为我们提供了许多易用的BeanFactory实现, XmlBeanFactory就是最常用的一个。


该实现将以XML方式描述组成应用的对象 以


及对象间的依赖关系。XmlBeanFactory类将获取此XML配 置元数据,并用它来构建一个完


全可配置的系统或应用。


BeanFactory 提供的高级配置机制,使得管理各种对象成为可能。 ApplicationContext


是BeanFactory的扩展,功能得到了进一步增强,比如更易 与Spring AOP集成、资源处理


(国际化处理)、事件传递及各种不同应用层的context实现 (如针对web应用的WebApplicationContext)。


简而言之,BeanFactory提供了配制框架及基本功能,而 ApplicationContext 则增加了


更多支持企业核心内容的功能。 ApplicationContext完全由BeanFactory扩展而来,


因而BeanFactory所具备的能力和行为也适用于ApplicationContext。


使用getBean(String) 方法就可以取得bean的实例；BeanFactory 提供的方法极其简单。 BeanFactory接口提供 了非常多的方法,但是对于我们的应用来说,最好永远不要调用它们,当然也包括 使用getBean(String)方法,这样可以避免我们对 Spring API的依赖。

BeanFactory 同时也不具备 编译spring配置文件的功能  在容器初始化时 如果applicationContext出现错误时


BeanFactory并不能及时察觉,必须等待第一次获取bean的实例时才能抛出异常


比如实例化 BeanFactory


Resource res = new FileSystemResource("applicationContext.xml");
  
BeanFactory factory = new XmlBeanFactory(res);

Resource  resClasspath = new ClassPathResource("applicationContext.xml.xml");
  
BeanFactory factory2 = new XmlBeanFactory(resClasspath);
  
获得BeanFactory实例时 不能检查错误


User u=(User)u.getBean("user");

当获得对象实例时 方可抛出异常


而实例化ApplicationContext


ApplicationContext  context=new ClassPathXmlApplicationContext("applicationContext.xml");

就能直接抛出异常