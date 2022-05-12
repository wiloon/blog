---
title: Java Bean
author: "-"
date: 2011-10-16T08:25:59+00:00
url: /?p=1062
categories:
  - Java
tags:$
  - reprint
---
## Java Bean

  一、 javabean 是什么？


  Bean的中文含义是"豆子"，顾名思义，JavaBean是指一段特殊的Java类，


  就是有默然构造方法,只有get,set的方法的java类的对象.


  最初，JavaBean的目的是为了将可以重复使用的软件代码打包标准。特别是用与帮助厂家开发在IDE下使用的java软件部件。这些包括如Grid控件，用户可以将该部件拖放到开发环境中。从此，JavaBean就可以扩展为一个java web 应用的标准部件，并且JavaBean部件框架已经扩展为企业版的 Bean (EJB) 。


  专业点解释是: 


  JavaBean定义了一组规则


  JavaBean就是遵循此规则的平常的Java对象


  满足这三个条件:


  1.执行java.io.Serializable 接口


  2.提供无参数的构造器


  3.提供getter 和 setter方法访问它的属性.

  
    简单地说，JavaBean是用Java语言描述的软件组件模型，其实际上是一个类。这些类遵循一个接口格式，以便于使函数命名、底层行为以及继承或实现的行为，可以把类看作标准的JavaBean组件进行构造和应用。
  
  
    JavaBean一般分为可视化组件和非可视化组件两种。可视化组件可以是简单的GUI元素，如按钮或文本框，也可以是复杂的，如报表组件；非可视化组件没有GUI表现形式，用于封装业务逻辑、数据库操作等。其最大的优点在于可以实现代码的可重用性。JavaBean又同时具有以下特性。
  
  
    易于维护、使用、编写。
  
  
    可实现代码的重用性。
  
  
    可移植性强，但仅限于Java工作平台。
  
  
    便于传输，不限于本地还是网络。
  
  
    可以以其他部件的模式进行工作。
  
  
    对于有过其他语言编程经验的读者，可以将其看作类似微软的ActiveX的编程组件。但是区别在于JavaBean是跨平台的，而ActiveX组件则仅局限于Windows系统。总之，JavaBean比较适合于那些需要跨平台的、并具有可视化操作和定制特性的软件组件。
  
  
    JavaBean组件与EJB (Enterprise JavaBean，企业级JavaBean) 组件完全不同。EJB 是J2EE的核心，是一个用来创建分布式应用、服务器端以及基于Java应用的功能强大的组件模型。JavaBean组件主要用于存储状态信息，而EJB组件可以存储业务逻辑。
  
  
    2  使用JavaBean的原因
  
  
    程序中往往有重复使用的段落，JavaBean就是为了能够重复使用而设计的程序段落，而且这些段落并不只服务于某一个程序，而且每个JavaBean都具有特定功能，当需要这个功能的时候就可以调用相应的JavaBean。从这个意义上来讲，JavaBean大大简化了程序的设计过程，也方便了其他程序的重复使用。
  
  
    JavaBean传统应用于可视化领域，如AWT (窗口工具集) 下的应用。而现在，JavaBean更多地应用于非可视化领域，同时，JavaBean在服务器端的应用也表现出强大的优势。非可视化的JavaBean可以很好地实现业务逻辑、控制逻辑和显示页面的分离，现在多用于后台处理，使得系统具有更好的健壮性和灵活性。JSP + JavaBean和JSP + JavaBean + Servlet成为当前开发Web应用的主流模式。
  
  
    3  JavaBean的开发
  
  
    在程序设计的过程中，JavaBean不是独立的。为了能够更好地封装事务逻辑、数据库操作而便于实现业务逻辑和前台程序的分离，操作的过程往往是先开发需要的JavaBean，再在适当的时候进行调用。但一个完整有效的JavaBean必然会包含一个属性，伴随若干个get/set (只读/只写) 函数的变量来设计和运行的。JavaBean作为一个特殊的类，具有自己独有的特性。应该注意以下3个方面。
  
  
    JavaBean类必须有一个没有参数的构造函数。
  
  
    JavaBean类所有的属性最好定义为私有的。
  
  
    JavaBean类中定义函数setXxx() 和getXxx()来对属性进行操作。其中Xxx是首字母大写的私有变量名称。
  
  
  
  
    二、JavaBean和企业Bean的区别
  
  http://www.hudong.com/wiki/Enterprise%20JavaBean

JavaBean 和 Server Bean (通常称为  Enterprise JavaBean (EJB)) 有一些基本相同之处。它们都是用一组特性创建，以执行其特定任务的对??获得其它特性的能力。这使得 bean 的行为根据特定任务和所在环境的不同而有所不同。
  
  
Enterprise Bean 与 JavaBean 不同。JavaBean 是使用 java.beans 包开发的，它是 Java 2 标准版的一部分。JavaBean 是一台机器上同一个地址空间中运行的组件。JavaBean 是进程内组件。Enterprise Bean 是使用 javax.ejb 包开发的，它是标准JDK的扩展，是 Java 2 Enterprise Edition 的一部分。Enterprise Bean 是在多台机器上跨几个地址空间运行的组件。因此 Enterprise Bean 是进程间组件。JavaBean 通常用作 GUI 窗口小部件，而 Enterprise Bean 则用作分布式商业对象.
