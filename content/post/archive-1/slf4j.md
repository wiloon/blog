---
title: slf4j
author: "-"
date: 2012-12-25T02:43:26+00:00
url: slf4j
categories:
  - Java
tags:
  - reprint
---
## slf4j

```xml
<properties>
    <slf4j.version>1.7.36</slf4j.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>${slf4j.version}</version>
    </dependency>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-simple</artifactId>
        <version>${slf4j.version}</version>
    </dependency>
</dependencies>
...

  http://baike.baidu.com/view/1895694.htm


  http://ugibb510.iteye.com/blog/458482


  SLF4J， (Simple Logging Facade for Java) ，不是具体的日志解决方案，它只服务于各种各样的日志系统。按照官方的说法，SLF4J是一个用于日志系统的简单Facade，允许最终用户在部署其应用时使用其所希望的日志系统。


  实际上，SLF4J所提供的核心API是一些接口以及一个LoggerFactory的工厂类。从某种程度上，SLF4J有点类似JDBC，不过比JDBC更简单，在JDBC中，你需要指定驱动程序，而在使用SLF4J的时候，不需要在代码中或配置文件中指定你打算使用那个具体的日志系统。如同使用JDBC基本不用考虑具体数据库一样，SLF4J提供了统一的记录日志的接口，只要按照其提供的方法记录即可，最终日志的格式、记录级别、输出方式等通过具体日志系统的配置来实现，因此可以在应用中灵活切换日志系统。


  1、什么情况可以使用


  如果你开发的是类库或者嵌入式组件，那么就应该考虑采用SLF4J，因为不可能影响最终用户选择哪种日志系统。在另一方面，如果是一个简单或者独立的应用，确定只有一种日志系统，那么就没有使用SLF4J的必要。假设你打算将你使用log4j的产品卖给要求使用JDK 1.4 Logging的用户时，面对成千上万的log4j调用的修改，相信这绝对不是一件轻松的事情。但是如果开始便使用SLF4J，那么这种转换将是非常轻松的事情。


  2、举例


   (1) 代码


  ```java
 import org.slf4j.Logger; 
  
    import org.slf4j.LoggerFactory;
  
  
    public class Wombat {
  
  
    final Logger logger = LoggerFactory.getLogger(Wombat.class);
  
  
    Integer t;
  
  
    Integer oldT;
  
  
    public void setTemperature(Integer temperature) {
  
  
    oldT = t;
  
  
    t = temperature;
  
  
    Object[] objs = {new java.util.Date(), oldT, t};
  
  
    logger.info("Today is {}, Temperature set to {}. Old temperature was {}.", objs);
  
  
    if (temperature.intValue() > 50) {
  
  
    logger.warn("Temperature({}) has risen above 50 degrees.", t);
  
  
    }
  
  
    }
  
  
    public static void main(String[] args) {
  
  
    Wombat wombat = new Wombat();
  
  
    wombat.setTemperature(10);
  
  
    wombat.setTemperature(60);
  
  
    }
  
  
    }
 ```
  
   (2) 使用SLF4J提供的simple log

  将以下jar包加入到项目中，然后执行

  slf4j-api-1.5.2.jar

  slf4j-simple-1.5.2.jar

  最终输出:

  32 [main] INFO Wombat - Today is Wed Sep 10 14:50:57 CST 2008, Temperature set to null. Old temperature was 10.

  32 [main] INFO Wombat - Today is Wed Sep 10 14:50:57 CST 2008, Temperature set to 10. Old temperature was 60.

  32 [main] WARN Wombat - Temperature(60) has risen above 50 degrees.

   (3) 使用SLF4J提供的simple log

  将以下jar包加入到项目中，然后执行

  slf4j-api-1.5.2.jar

  slf4j-jdk14-1.5.2.jar

  最终输出:

  2008-9-10 15:01:20 Wombat setTemperature

  信息: Today is Wed Sep 10 15:01:20 CST 2008, Temperature set to null. Old temperature was 10.

  2008-9-10 15:01:20 Wombat setTemperature

  信息: Today is Wed Sep 10 15:01:20 CST 2008, Temperature set to 10. Old temperature was 60.

  2008-9-10 15:01:20 Wombat setTemperature

  警告: Temperature(60) has risen above 50 degrees.

   (4) 配置很简单吧

  从以上事例可以看出，配置SLF4J使用那种日志系统是非常简单的一件事，只要将与你打算使用的日志系统对应的jar包加入到项目中，SLF4J就会自动选择使用你加入的那种日志系统。这种方法被称之为动态绑定。当然，该日志系统的相关类库是不能少，例如，如果你打算使用log4j，那么还需要log4j的类库，可能还有配置配置log4j.properties。

  3、格式化日志

  SLF4J还提供了格式化日志的功能，如事例中的语句:

  logger.info("Today is {}, Temperature set to {}. Old temperature was {}.", objs);

## 日志系统绑定原理

在应用中，通过LoggerFactory类的静态getLogger()获取logger。通过查看该类的代码可以看出，最终是通过StaticLoggerBinder.SINGLETON.getLoggerFactory()方法获取LoggerFactory然后，在通过该具体的LoggerFactory来获取logger的。类org.slf4j.impl.StaticLoggerBinder并不在slf4j-api-1.5.2.jar包中，仔细查看每个与具体日志系统对应的jar包，就会发现，相应的jar包都有一个org.slf4j.impl.StaticLoggerBinder的实现，不同的实现返回与该日志系统对应的LoggerFactory，因此就实现了所谓的动态绑定，达到只要选取不同jar包就能简单灵活配置的目的。

SLF4J官方网站: <http://www.slf4j.org>

文章出处: <http://www.diybl.com/course/3_program/java/javaxl/2008910/141669.html>

SLF4J 的几种实际应用模式-之一: SLF4J+Log4J
  
2010-04-07 — Unmi
  
SLF4J(Simple Logging Facade for Java) 是一个通用的日志框架，不能何以谓之 Facade(门面)，所扮眼的角色相当于 Jakarta Commons Logging。就像 JCL 需要底层的日志实现，如 Log4J、java.util.logging、Simple Logger 等来完成具体的信息输出，事实上基本总是 JCL+Log4J 那么一个绝配。SLF4J 的原旨也是能支持多种下层日志框架实现，但最好的日志实现仍然是 Log4J，所以本篇讲述 SLF4J 的第一种用法 SLF4J+Log4J。

需要的配置文件和组件包，下面三个 jar 文件和一个 properties 文件都是要放在项目的 ClassPath 上。

- slf4j-api-1.5.11.jar
- slf4j-log4j12-1.5.11.jar
- log4j-1.2.15.jar
- log4j.properties(也可以是 log4j.xml，本例中用 log4j.propertes)

```java
package com.unmi;
                
                
                
                
                
                
                  import org.slf4j.Logger;
                
                
                
                  import org.slf4j.LoggerFactory;
                
                
                
                
                
                
                  public class TestSlf4j {
                
                
                
                      private static final Logger logger = LoggerFactory.getLogger(TestSlf4j.class);
                
                
                
                
                
                
                      public static void main(String[] args) {
                
                
                
                          logger.info("Hello {}","SLF4J");
                
                
                
                      }
                
                
                
                  }
```

执行它，控制台输出:

2010-04-07 17:14:51,390 [com.unmi.TestSlf4j]-[INFO] Hello SLF4J

把这种 SLF4J+Log4J 的使用模式与曾为霸主地位的 JCL+Log4J 的用法进行一下对比(请忽略掉包文件中的版本号):

SLF4J+Log4j 组合

对比

JCL+Log4J 组合

slf4j-api-1.5.11.jar

相当，定义高层 API

commons-logging-1.1.jar

slf4j-log4j12-1.5.11.jar

相当，左边是用绑定包，右边

 是用配置文件来指定日志实现

从上面的对比来看，SLF4j+Log4j 与 JCL+Log4J 的使用方式差不多，主要差异就在 SLF4J 用 jar 来告知用哪种日志实现，而 JCL 是通过配置文件来获得该选择哪个日志实现。

为什么会兴起 SLF4J，看看我们原来哪一个框架中，大的如 SSH 三雄(Spring、Struts、Hibernate)，还有 WAS 应用服务器，小的就不计其数以前用的通用日志框架都清一色的 Jakarta Commons Logging(JCL)，日志实现会选用 Log4j，为何现在 Hibernate、Tapesty、DbUnit、Jetty V6 等纷纷变节，都采用了 SLF4J 了呢？SLF4J 与 JCL 相比，定然是有其可表之处。而其中 SLF4J 受类加载器的影响较小，不易产生内存溢出的问题，性能得到了改善，更主要是顺应了潮流的发展-可方便部署到 OSGI 环境中。

关于当前有哪些项目改用了 SLF4J，请参看页面 <http://www.slf4j.org/>。

```java

private static Logger logger = LoggerFactory.getLogger(FooController.class);

```

gradle dependencies:

compile("org.apache.logging.log4j:log4j-api:$log4j_version",
  
"org.apache.logging.log4j:log4j-core:$log4j_version",
  
"org.apache.logging.log4j:log4j-slf4j-impl:$log4j_version",
  
"org.slf4j:slf4j-api:$slf4j_version"
  
)

每一个Java程序员都知道日志对于任何一个Java应用程序，尤其是服务端程序是至关重要的，而很多程序员也已经熟悉各种不同的日志库如java.util.logging、Apache log4j、logback。但如果你还不知道SLF4J (Simple logging facade for Java) 的话，那么是时候去在你项目中学习使用SLF4J了。

在这篇文章中，我们将学习为什么使用SLF4J比log4j或者java.util.logging要优秀。自从上次我写Java程序员的10个日志技巧已经有一段时间了，我已经不记得我写的关于日志的一切了。

不管怎样，让我们回到这个话题，SLF4J不同于其他日志类库，与其它有很大的不同。SLF4J(Simple logging Facade for Java)不是一个真正的日志实现，而是一个抽象层 ( abstraction layer) ，它允许你在后台使用任意一个日志类库。如果是在编写供内外部都可以使用的API或者通用类库，那么你真不会希望使用你类库的客户端必须使用你选择的日志类库。

如果一个项目已经使用了log4j，而你加载了一个类库，比方说 Apache Active MQ——它依赖于于另外一个日志类库logback，那么你就需要把它也加载进去。但如果Apache Active MQ使用了SLF4J，你可以继续使用你的日志类库而无语忍受加载和维护一个新的日志框架的痛苦。

总的来说，SLF4J使你的代码独立于任意一个特定的日志API，这是一个对于开发API的开发者很好的思想。虽然抽象日志类库的思想已经不是新鲜的事物而且Apache commons logging也已经在使用这种思想了，但现在SLF4J正迅速成为Java世界的日志标准。让我们再看看几个使用SLF4J而不是log4j、logback或者java.util.logging的理由。

SLF4J对比Log4J，logback和java.util.Logging的优势

正如我之前说的，在你的代码中使用SLF4J写日志语句的主要出发点是使得你的程序独立于任意特定的日志类库，依赖于特定类可能需要不同与你已有的配置，并且导致更多维护的麻烦。但除此之外，还要一个SLF4J API的特性使得我坚持使用SLF4J而抛弃我长期间钟爱的Lof4j的理由，是被称为占位符(place holder)，在代码中表示为"{}"的特性。占位符是一个非常类似于在String的format()方法中的%s，因为它会在运行时被某个提供的实际字符串所替换。这不仅降低了你代码中字符串连接次数，而且还节省了新建的String对象。即使你可能没需要那些对象，但这个依旧成立，取决于你的生产环境的日志级别，例如在DEBUG或者INFO级别的字符串连接。因为String对象是不可修改的并且它们建立在一个String池中，它们消耗堆内存( heap memory)而且大多数时间他们是不被需要的，例如当你的应用程序在生产环境以ERROR级别运行时候，一个String使用在DEBUG语句就是不被需要的。通过使用SLF4J,你可以在运行时延迟字符串的建立，这意味着只有需要的String对象才被建立。而如果你已经使用log4j，那么你已经对于在if条件中使用debug语句这种变通方案十分熟悉了，但SLF4J的占位符就比这个好用得多。

这是你在Log4j中使用的方案，但肯定这一点都不有趣并且降低了代码可读性因为增加了不必要的繁琐重复代码(boiler-plate code):

```java

if (logger.isDebugEnabled()) {
  
logger.debug("Processing trade with id: " + id + " symbol: " + symbol);
  
}

```

另一方面，如果你使用SLF4J的话，你可以得到在极简洁的格式的结果，就像以下展示的一样:

```java
  
logger.debug("Processing trade with id: {} and symbol : {} ", id, symbol);

```

在SLF4J，我们不需要字符串连接而且不会导致暂时不需要的字符串消耗。取而代之的，我们在一个以占位符和以参数传递实际值的模板格式下写日志信息。你可能会在想万一我有很个参数怎么办？嗯，那么你可以选择使用变量参数版本的日志方法或者用以Object数组传递。这是一个相当的方便和高效方法的打日志方法。记住，在生产最终日志信息的字符串之前，这个方法会检查一个特定的日志级别是不是打开了，这不仅降低了内存消耗而且预先降低了CPU去处理字符串连接命令的时间。这里是使用SLF4J日志方法的代码，来自于slf4j-log4j12-1.6.1.jar中的Log4j的适配器类Log4jLoggerAdapter。

```java
  
public void debug(String format, Object arg1, Object arg2) {
  
if (logger.isDebugEnabled()) {
  
FormattingTuple ft = MessageFormatter.format(format, arg1, arg2);
  
logger.log(FQCN, Level.DEBUG, ft.getMessage(), ft.getThrowable());
  
}
  
}

```

同时，我们也很值得知道打日志是对应用程序的性能有着很大影响的，在生产环节上只进行必要的日志记录是我们所建议的。

怎么用SLF4J做Log4J的日志记录

除了以上好处，我想还有一个告诫，就是为了使用SLF4J，你不仅需要包含SLF4J的API jar包，例如 slf4j-api-1.6.1.jar，还需要相关Jar包，这取决于你在后台使用的日志类库。如果你想要使用和Log4J 一起使用SLF4J ，Simple Logging Facade for Java,，你需要包含以下的Jar包在你的classpath中，取决于哪个SLF4J和你在使用的Log4J的版本。例如:

slf4j-api-1.6.1.jar – JAR for SLF4J API
  
log4j-1.2.16.jar – JAR for Log4J API
  
slf4j-log4j12-1.6.1.jar – Log4J Adapter for SLF4J
  
如果你在使用Maven去管理你的项目依赖，你只需要包含SLF4J JAR包，maven会包含它的依赖的相关包。为了和SLF4J一起中使用Log4J，你可以包含以下的依赖在你项目中的pom.xml。
  
```xml
<dependency>
  
<groupId>org.slf4j</groupId>
  
slf4j-log4j12</artifactId>
  
<version>1.6.1</version>
  
</dependency>

<dependency>
  
<groupId>org.slf4j</groupId>
  
slf4j-log4j12</artifactId>
  
<version>1.6.1</version>
  
</dependency>
```
  
还有，如果你对于使用变量参数版本 (variable argument version ) 的日志方法感兴趣的话，那么就导入SLF4J 1.7的版本吧。

总结

总结这次说的，我建议使用SLF4J的而不是直接使用 Log4j, commons logging, logback 或者 java.util.logging 已经足够充分了。

在你的开源或内部类库中使用SLF4J会使得它独立于任何一个特定的日志实现，这意味着不需要管理多个日志配置或者多个日志类库，你的客户端会很感激这点。
  
SLF4J提供了基于占位符的日志方法，这通过去除检查isDebugEnabled(), isInfoEnabled()等等，提高了代码可读性。
  
通过使用SLF4J的日志方法，你可以延迟构建日志信息 (Srting) 的开销，直到你真正需要，这对于内存和CPU都是高效的。
  
作为附注，更少的暂时的字符串意味着垃圾回收器 (Garbage Collector) 需要做更好的工作，这意味着你的应用程序有为更好的吞吐量和性能。
  
这些好处只是冰山一角，你将在开始使用SL4J和阅读其中代码的时候知道更多的好处。我强烈建议，任何一个新的Java程序员，都应该使用SLF4J做日志而不是使用包括Log4J在内的其他日志API。
  
更多阅读:

<http://javarevisited.blogspot.com/2013/08/why-use-sl4j-over-log4j-for-logging-in.html#ixzz2konULdTB>

原文链接:  javarevisited 翻译:  ImportNew.com - Jaskey
  
译文链接:  <http://www.importnew.com/7450.html>
  
[ 转载请保留原文出处、译者和译文链接。]
