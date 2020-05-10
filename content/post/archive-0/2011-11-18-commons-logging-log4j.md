---
title: commons-logging Log4J
author: wiloon
type: post
date: 2011-11-18T23:40:51+00:00
url: /?p=1525
bot_views:
  - 9
views:
  - 1
categories:
  - Java

---
Log4J是一个功能很强大的日志记录组件，它提供了丰富的日志记录功能，它本身和commons-logging没有什么关系，也就是说一个项目中可以单独使用Log4J来记录日志，而不需要引入commons-logging包，这样也能实现记录日志的功能，但是这样有一个不太好的地方就是如果你想使用其他的Logging组建，比如jdk1.4自带的logging框架，就不得不修改原有文件中所有使用了Log4J组建的代码。

这时，commons-logging就派上用场了，说白了commons-logging就是一个记录日志的统一接口，它定义了一套抽象的记录日志的接口，用户可以通过配置，来使用任何一个符合该接口的Logging组建。而commons-logging组建本身仅仅提供了一个很简单的记录日志的类SimpleLog，这个类的记录日志功能很有限。因此，通常情况下，会将Log4J组建与commons-logging组建一块儿使用，在程序代码中，使用commons-logging的接口方法来记录日志，而后台实际使用的是Log4J组建。

commons-logging组建使用具体的Log组建的顺序如下

1、<span style="font-family: 宋体;">如果定义了org.apache.commons.logging.Log系统参数，则使用指定的Logging实现；</span>

<span style="font-family: 宋体;">2、如果在CLASSPATH里发现了Log4J，则使用Log4J；</span>

<span style="font-family: 宋体;">3、如果使用的是JDK1.4，则使用JDK1.4内置的Logging框架；</span>

<span style="font-family: 宋体;">4、如果都没有找到，则使用Commons Logging内置的简单Log实现。</span>