---
title: Tomcat basic
author: "-"
date: 2012-05-13T10:33:18+00:00
url: tomcat
categories:
  - Web
tags:
  - Tomcat

---
## Tomcat basic

## archlinux install tomcat

```bash
sudo pacman -S tomcat8

```

<http://baike.baidu.com/view/10166.htm>

### tomcat 7

<https://archive.apache.org/dist/tomcat/tomcat-7>

Tomcat是Apache 软件基金会 (Apache Software Foundation) 的Jakarta 项目中的一个核心项目，由Apache、Sun 和其他一些公司及个人共同开发而成。由于有了Sun 的参与和支持，最新的Servlet 和JSP 规范总是能在Tomcat 中得到体现，Tomcat 5 支持最新的Servlet 2.4 和JSP 2.0 规范。因为Tomcat 技术先进、性能稳定，而且免费，因而深受Java 爱好者的喜爱并得到了部分软件开发商的认可，成为目前比较流行的Web 应用服务器。

Tomcat 很受广大程序员的喜欢，因为它运行时占用的系统资源小，扩展性好，支持负载平衡与邮件服务等开发应用系统常用的功能；而且它还在不断的改进和完善中，任何一个感兴趣的程序员都可以更改它或在其中加入新的功能。
  
Tomcat 是一个轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。对于一个初学者来说，可以这样认为，当在一台机器上配置好Apache 服务器，可利用它响应对HTML 页面的访问请求。实际上Tomcat 部分是Apache 服务器的扩展，但它是独立运行的，所以当你
 运行tomcat 时，它实际上作为一个与Apache 独立的进程单独运行的。
  
 这里的诀窍是，当配置正确时，Apache 为HTML页面服务，而Tomcat 实际上运行JSP 页面和Servlet。另外，Tomcat和IIS、Apache等Web服务器一样，具有处理HTML页面的功能，另外它还是一个Servlet和JSP容器，独立的Servlet容器是Tomcat的默认模式。不过，Tomcat处理静态HTML的能力不如Apache服务器。目前Tomcat最新版本为7.0.27 Released。
  
名称的由来
Tomcat最初是由Sun的软件构架师詹姆斯·邓肯·戴维森开发的。后来他帮助将其变为开源项目，并由Sun贡献给Apache软件基金会。由于大部分开源项目O'Reilly都会出一本相关的书，并且将其封面设计成某个动物的素描，因此他希望将此项目以一个动物的名字命名。因为他希望这种动物能够自己照顾自己，最终，他将其命名为Tomcat (英语公猫或其他雄性猫科动物) 。而O'Reilly出版的介绍Tomcat的书籍 (ISBN 0-596-00318-8) [1]的封面也被设计成了一个公猫的形象。而Tomcat的Logo兼吉祥物也被设计成了一只公猫。
  
版本差异 (主要版本)
  
Apache Tomcat 7.x

是目前的开发焦点。它在汲取了Tomcat 6.0.x优点的基础上，实现了对于Servlet 3.0、JSP 2.2和EL 2.2等特性的支持。除此以外的改进列表如下:

· Web应用内存溢出侦测和预防

· 增强了管理程序和服务器管理程序的安全性

· 一般 CSRF保护

· 支持web应用中的外部内容的直接引用

· 重构 (connectors, lifecycle)及很多核心代码的全面梳理

Apache Tomcat 6.x

在汲取 Tomcat 5.5.x优点的基础上，实现了Servlet 2.5和JSP 2.1等特性的支持。除此以外的改进列表如下:

· 内存使用优化

· 更大的IO容量

· 重构聚类

## 'Tomcat & Catalina'

catalina   是   tomcat   4.x   的   servlet   container，起源是加州的一个岛名，本身和猫没有什么关系，所以   tomcat:catalina   的类比一定不能选   apple:macintosh (macintosh   是美国的一种苹果，个头甚大) 。但另外一方面，PBY   catalina   是一种远程轰炸机，而   apache   是   Jane 's   鼎鼎大名的直升机，所以   catalina:apache   和   apple:macintosh   勉强有一对。

Catalina是太平洋中靠近洛杉矶的一个小岛。因为其风景秀丽而著名。最近曾被评为全美最漂亮的小岛。

Tomcat is actually composed of a number of components, including a [Tomcat JSP][1] engine and a variety of different connectors, but its core component is called Catalina.  Catalina provides Tomcat's actual implementation of the servlet specification; when you [start up your Tomcat server][2], you're actually starting Catalina.

In this article, we'll get to know Tomcat's core component, from the [origins of the name "Catalina"][3], to an overview of [how Catalina is configured][4].  We'll also look at some Catalina-related tips and tricks, such as how to get the most out of [Catalina's built-in logging][5] functionality, and how to [manage the Catalina class as an MBean][6] using JMX.

  Tired of wading through hundreds of lines of XML just to make a simple change to your Tomcat configuration?  Tcat makes Tomcat configuration simple.  Create optimized configuration profiles, save them, and apply them to groups of servers with a single click.

## How Did Catalina Get Its Name?

There's nothing like an Apache product name to raise an eyebrow - the Apache volunteers have a knack for turning out oddly named technologies that's only rivaled by Ubuntu's "adjective-animal" naming format.

The name "Catalina," according to Craig McClanahan, who designed the original architecture of the servlet container, can be attributed to three things: his love for Catalina Island (despite never having visited it), his cat's habit of hanging around the computer while he was writing the code, and the consideration, at an early stage of development, of building Tomcat on a server framework called Avalon, which is the name of a town on Catalina island.

The Avalon framework was eventually abandoned, but the name stuck, and the rest is history.

<http://www.mulesoft.com/tomcat-catalina>

[1]: http://www.mulesoft.com/tomcat-jsp
[2]: http://www.mulesoft.com/tomcat-start
[3]: http://www.mulesoft.com/tomcat-catalina#name
[4]: http://www.mulesoft.com/tomcat-catalina#config
[5]: http://www.mulesoft.com/tomcat-catalina#logging
[6]: http://www.mulesoft.com/tomcat-catalina#mbean
