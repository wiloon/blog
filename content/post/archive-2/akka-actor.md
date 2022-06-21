---
title: AKKA
author: "-"
date: 2015-12-15T11:39:45+00:00
url: /?p=8560kjn
categories:
  - inbox
tags:
  - reprint
---
## AKKA

<http://sunxiang0918.cn/2016/01/10/Akka-in-JAVA-1/>

Akka是一个由Scala编写的,能兼容Sacala和JAVA的,用于编写高可用和高伸缩性的**Actor模型**框架.它基于了事件驱动的并发处理模式,性能非常的高,并且有很高的可用性.大大的简化了我们在应用系统中开发并发处理的过程.它在各个领域都有很好的表现.
  
使用AKKA的好处
  
就如上面简介中所说的,AKKA把并发操作的各种复杂的东西都统一的做了封装.我们主要关心的是业务逻辑的实现,只需要少量的关心Actor模型的串联即可构建出高可用,高性能,高扩展的应用.
  
Akka for JAVA
  
由于AKKA是使用Scala编写的,而Scala是一种基于JVM的语言.因此JAVA对AKKA的支持也是很不错的.Akka自身又是采用微内核的方式来实现的,这就意味着能很容易的在自己的项目中应用AKKA,只需要引入几个akka的Lib包即可.而官方直接就提供了Maven库供我们在JAVA中使用AKKA.
  
这些AKKA的依赖包主要有:
  
akka-actor:最核心的依赖包,里面实现了Actor模型的大部分东西
  
akka-agent:代理/整合了Scala中的一些STM特性
  
akka-camel:整合了Apache的Camel
  
akka-cluster:akka集群依赖,封装了集群成员的管理和路由
  
akka-kernel:akka的一个极简化的应用服务器,可以脱离项目单独运行.
  
akka-osgi:对OSGI容器的支持,有akka的最基本的Bundle
  
akka-remote:akka远程调用
  
akka-slf4j:Akka的日志事件监听
  
akka-testkit:Akka的各种测试工具
  
akka-zeromq:整合ZeroMQ
  
其中最总要的就是akka-actor,最简单的AKKA使用的话,只需要引入这个包就可以了.
  
### Actor模型

什么是Actor
  
既然说AKKA是一个Actor模型框架,那么就需要搞清楚什么是Actor模型.Actor模型是由Carl Hewitt于上世纪70年代提出的,目的是为了解决分布式编程中的一系列问题而产生.
  
在Actor模型中,一切都可以抽象为Actor.
  
而Actor是封装了状态和行为的对象,他们的唯一通讯方式就是交换消息,交换的消息放在接收方的邮箱(Inbox)里.也就是说Actor之间并不直接通信,而是通过了消息来相互沟通,每一个Actor都把它要做的事情都封装在了它的内部.
  
每一个Actor是可以有状态也可以是无状态的,理论上来讲,每一个Actor都拥有属于自己的轻量级进程,保护它不会被系统中的其他部分影响.因此,我们在编写Actor时,就不用担心并发的问题.
  
通过Actor能够简化锁以及线程管理,Actor具有以下的特性:
  
提供了一种高级的抽象,能够封装状态和操作.简化并发应用的开发.
  
提供了异步的非阻塞的/高性能的事件驱动模型
  
超级轻量级的线程事件处理能力.
  
要在JAVA中实现一个Actor也非常的简单,直接继承akka.actor.UntypedActor类,然后实现public void onReceive(Object message) throws Exception方法即可.

><https://guobinhit.github.io/akka-guide/>
><https://www.zhihu.com/question/279512440/answer/407373037>
