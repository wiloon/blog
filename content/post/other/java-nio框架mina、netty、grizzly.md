---
title: Java NIO 框架 Netty, Mina, Grizzly
author: "-"
date: 2015-08-31T06:46:08+00:00
url: java/nio
categories:
  - Java

tags:
  - reprint
---
## Java NIO 框架 Netty, Mina, Grizzly

### Netty

Netty是一款异步的事件驱动的网络应用框架和工具,用于快速开发可维护的高性能、高扩展性协议服务器和客户端。也就是说,Netty是一个NIO客户端/服务器框架,支持快速、简单地开发网络应用,如协议服务器和客户端。它极大简化了网络编程,如TCP和UDP socket 服务器。
  
### Mina

Mina(Multipurpose Infrastructure for Network Applications) 是 Apache 组织一个较新的项目,它为开发高性能和高可用性的网络应用程序提供了非常便利的框架。当前发行的 Mina 版本2.04支持基于 Java NIO 技术的 TCP/UDP 应用程序开发、串口通讯程序,Mina 所支持的功能也在进一步的扩展中。目前,正在使用 Mina的应用包括: Apache Directory Project、AsyncWeb、AMQP (Advanced Message Queuing Protocol) 、RED5 Server (Macromedia Flash Media RTMP) 、ObjectRADIUS、 Openfire等等。
  
Grizzly:

Grizzly是一种应用程序框架,专门解决编写成千上万用户访问服务器时候产生的各种问题。使用JAVA NIO作为基础,并隐藏其编程的复杂性。容易使用的高性能的API。带来非阻塞socketd到协议处理层。利用高性能的缓冲和缓冲管理使用高性能的线程池。
  
OK,我们现在可以看看三者的简单对比了。
  
首先,从设计的理念上来看,Mina的设计理念是最为优雅的。当然,由于Netty的主导作者与Mina的主导作者是同一人,出自同一人之手的Netty在设计理念上与Mina基本上是一致的。而Grizzly在设计理念上就较差了点,几乎是Java NIO的简单封装。

其次,从项目的出身来看,Mina出身于开源界的大牛Apache组织,Netty出身于商业开源大亨Jboss,而Grizzly则出身于土鳖Sun公司。从其出身可以看到其应用的广泛程序,到目前为止,我见到业界还是使用Mina多一些,而Netty也在慢慢的应用起来,而Grizzly则似乎只有Sun自已的项目使用了,如果还有其他的公司或开源项目在使用,那就算我孤陋寡闻。
  
最后,从入门的文档来说,由于Mina见世时间相对较长,官方以及民间的文档与入门示例都相当的多。Netty的官方文档也做得很好,而民间文档就要相对于Mina少一些了。至于Grizzly,不管是官方还是民间,都很少见到其文档。

<http://www.blogjava.net/javagrass/archive/2011/07/05/353680.html>
