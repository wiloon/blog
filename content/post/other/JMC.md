---
title: 'JMC & Flight Recorder'
author: "-"
date: 2015-05-19T06:42:22+00:00
url: jmc
categories:
  - Java
tags:
  - reprint
---
## 'JMC & Flight Recorder'

从Java 7 Update 40之后，任务控制和Flight Recorder就将和JDK一起提供，正如InfoQ 在介绍它发布的新闻中所描述的那样。任务控制的出发点是监控、管理和排错，而Flight Recorder则是收集和评估性能数据的设施。这两个工具在JRockit中都已经存在，现在最终被移植到了HotSpot上，

任务控制
  
任务控制提供的功能几乎和JVisual VM完全相同。这两个工具都能够连接到本地或者远程Java进程收集JMX数据。任务控制能够通过Java发现协议 (Java Discovery Protocol) 自动地发现远程运行的JVM。为了使用该功能JVM需要通过下面的参数启动: -Dcom.sun.management.jmxremote.autodiscovery=true -Dcom.sun.management.jdp.name=JVM_Name。

和JVisual VM相似的是，任务控制也有一个插件机制，能够进行定制化。但是与VisualVM不同的是，任务控制还能够在收集的数据上创建新的视图。现在能够使用的两个实验性的插件是JOverflow堆分析器 (查找低效的集合使用) 和DTrace记录器 (关联DTrace配置文件) 。任务控制拥有一个JMX浏览器作为它核心功能的一部分，同时提供了稍微更加强大的功能。例如，线程监控能够提供每一个线程的分配信息以及与堆栈跟踪相关的信息。因为任务控制是基于Eclipse平台的，所以它不仅能够作为JDK中的独立工具使用，还能够作为Eclipse插件从 Oracle任务控制更新网站上获取。

Flight Recorder
  
Java Flight Recorder - JFR 默认被设置为关闭状态。JDK7 通过在启动应用程序的命令中加入-XX:+UnlockCommercialFeatures –XX:+FlightRecorder 参数来开启 JFR，以及相关的一些功能。但是值得注意的是这个命令只是开启了 JFR 功能，但并没有开启记录进程各种事件。
  
JDK 8 可能直接 通过jcmd控制JFR。

想要在JVM之外收集调试数据、特别是性能数据的工具需要实现JVMPI/JVMTI接口。虽然大部分分析工具发展的非常良好，但是让它们能够在产品中低消耗地运行依然是非常困难的。

Flight Recorder直接在JVM中实现了它自己的基于事件的监控接口，所以能够以最小的开销提供CPU时间或者对象分配分析这样的功能。例如，这个新接口允许采取线程的样本但不需要它们在还原点上，降低了开销和测量的偏差。只有少量使用字节码检测的事件对运行的代码有影响。大部分捕获技术是新的，第三方无法使用。Flight Recorder在JVM本地记录数据，但是是记录在堆外 (off-heap) ，因此它并不会影响内存特性和垃圾收集。当它被配置成持久化数据的时候，它会周期性地倾倒 (dump) 到一个文件中。

收集的数据主要包含4种类型的事件: "瞬间 (instant) "，在事件发生时进行记录；"可请求的 (requestable) "，它们会被轮循；"持续 (duration) "，表示一个时间间隔的度量；"定时的 (timed) "，它们和"持续"一样，但是对过滤数据应用了阀值。有两个预定义的配置: "连续性 (continuous) "，它的目的是始终运行；"剖析 (profiling) "，它会收集更多的数据以便进行短期分析。但是无论如何开销始终都非常低，除非明确地声明一个事件。

除了JVM生成的事件之外，还鼓励框架和应用程序服务器提供自己的事件。目前并不支持接口，但是Weblogic和Glassfish已经提供了事件，它们基本上成为了事实上的接口。Marcus Hirt在他的博客文章"使用 (非常不支持的) Java Flight Recorder API"中介绍了如何使用API。基本的步骤是扩展合适的Event类，通过添加注解表明值，然后从事件产生的代码中调用它。自定义的事件和其他事件并没有什么不同，也能够使用、创建仪表盘并随着其他的事件一起绘制。该版本包含的其他重要功能的细节信息可以从 Marcus Hirt的另一篇博客中找到。

许可
  
为了使用Flight Recorder，服务器VM需要使用下面的参数启动: -XX:+UnlockCommercialFeatures -XX:+FlightRecorder 。这已经表明这些新功能需要一个许可。但是并没有进行技术性的检查，所以许可文件并不是必须的。实际上许可是一个契约性的协议，它需要Java SE Advanced或者Java SE Suite，根据Oracle的价格表在产品系统中它的售价是每个处理器5k/15k美元。测试或者开发系统并不需要许可，但是依然需要UnlockCommercialFeatures标记。任务控制本身是否需要一个许可并不明确。文档中暗示了它也能在OpenJDK VM上免费使用，只要任务控制不要在需要每个处理器许可的产品系统上运行即可。希望Oracle能够澄清这个状况。

JMC (jmc命令) 打包在了Java开发工具集中 (JDK) ，位于bin目录下。额外的日志可以通过使用 –consoleLog –debug选项来启用。各种体验式的插件 (比如针对DTrace、JMX控制台的插件) 也可以进行在JMC中进行下载。

<http://download.oracle.com/technology/products/missioncontrol/updatesites/base/5.5.1/eclipse/update-site-instructions/index.html>
  
<https://stackoverflow.com/questions/23580934/what-are-the-differences-between-jvisualvm-and-java-mission-control>

<http://www.infoq.com/cn/news/2016/10/Java-Flight-Recorder-Mission>

<http://www.infoq.com/cn/news/2013/10/misson-control-flight-recorder>
  
<https://www.infoq.com/news/2013/09/java7u40>
  
<http://www.oracle.com/technetwork/java/javaseproducts/mission-control/java-mission-control-1998576.html>
