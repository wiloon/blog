---
title: "IO多路复用, IO Multiplexing"
author: "-"
date: "2021-07-02 16:49:41"
url: "iomultiplex"
categories:
  - OS
tags:
  - IO
---

## 什么是IO多路复用
I/O 多路复用技术会用一个系统调用函数来监听我们所有关心的连接，也就说可以在一个监控线程里面监控很多的连接。


一个用机场管理来解释的例子，以及对select、poll、epoll的讲解
IO 多路复用是什么意思？ - 罗志宇的回答 - 知乎

有趣的比喻

这些名词比较绕口，理解涵义就好。一个epoll场景：一个酒吧服务员（一个线程），前面趴了一群醉汉，突然一个吼一声“倒酒”（事件），你小跑过去给他倒一杯，然后随他去吧，突然又一个要倒酒，你又过去倒上，就这样一个服务员服务好多人，有时没人喝酒，服务员处于空闲状态，可以干点别的玩玩手机。至于epoll与select，poll的区别在于后两者的场景中醉汉不说话，你要挨个问要不要酒，没时间玩手机了。io多路复用大概就是指这几个醉汉共用一个服务员。

作者：匿名用户
链接：https://www.zhihu.com/question/32163005/answer/55687802

为什么要有IO多路复用
一个从本质上讲的清晰描述

要弄清问题 先要知道问题的出现原因

原因:

由于进程的执行过程是线性的(也就是顺序执行),当我们调用低速系统I/O(read,write,accept等等),进程可能阻塞,此时进程就阻塞 在这个调用上,不能执行其他操作.阻塞很正常.

接下来考虑这么一个问题：一个服务器进程和一个客户端进程通信,服务器端read(sockfd1,bud,bufsize),此时客户端进程没有发送数据,那么read(阻塞调用)将 阻塞直到客户端调用write(sockfd,but,size)发来数据.

在一个客户和服务器通信时这没什么问题,当多个客户与服务器通信时,若服 务器阻塞于其中一个客户sockfd1,当另一个客户的数据到达套接字sockfd2时,服务器不 能处理,仍然阻塞在read(sockfd1,…)上;此时问题就出现了,不能及时处理另一个客户的服务,咋么办?I/O多路复用来解决!

I/O多路复用:继续上面的问题,有多个客户连接,sockfd1,sockfd2,sockfd3..sockfdn 同时监听这n个客户,当其中有一个发来消息时就从select的阻塞中返回,然后就调用read 读取收到消息的sockfd,然后又循环回select阻塞;这样就不会因为阻塞在其中一个上而不能处 理另一个客户的消息

Q: 那这样子，在读取socket1的数据时，如果其它socket有数据来，那么也要等到socket1读取完了才能继续读取其它socket的数据吧。那不是也阻塞住了吗？而且读取到的数据也要开启线程处理吧，那这和多线程IO有什么区别呢？

A:
1. CPU本来就是线性的，不论什么都需要顺序处理，并行只能是多核CPU
2. io多路复用本来就是用来解决对多个I/O监听时,一个I/O阻塞影响其他I/O的问题,跟多线程没关系.
3. 跟多线程相比较,线程切换需要切换到内核进行线程切换,需要消耗时间和资源. 而I/O多路复用不需要切换线/进程,效率相对较高,特别是对高并发的应用nginx就是用I/O多路复用,故而性能极佳.但多线程编程逻辑和处理上比I/O多路复用简单.而I/O多路复用处理起来较为复杂.

作者总结
用自己的话解释清楚新的知识，这就是内化的过程。

【IO多路复用】和【多线程】是两种解决单个服务器应对多客户端同时IO请求阻塞问题的方案，问题出现的根源在于原始情况下，服务器收到客户端的进程的连接请求后都会调用阻塞的read()方法尝试从客户端读取数据，若读取不到则一直保持阻塞，但是这种处理方式显然会造成问题，譬如如果正在等待读取的这个客户端不传数据了，而其它有正在等待处理的客户端数据传输请求，那么显然就会造成服务器资源的浪费（不能及时处理真正紧急的客户端请求，而浪费时间在暂时没有处理需求的客户端请求上）。

解决这个问题有个简单的思路：

【多线程】：即针对每一个客户端进程都新建一个新的服务器端线程，即一对一地应付客户端的通信需求。

不过这个解决方案有个问题就是：如果通信的客户端很多，那么服务器就需要开很多线程来处理IO，服务器这边的压力就会比较大，除开开启线程与维持线程本身需要的资源以外，服务器CPU在线程之间切换也要耗时，导致效率低下。

因此，【IO多路复用】搞定了多线程解决方案的痛点，只用一个线程来解决阻塞问题，具体做法就是：依然调用一个阻塞方法，这个阻塞方法会监听跟踪每一个IO流的状态，当有一个新的数据传输请求到来，就会通知服务器，然后服务器找到对应有需求的客户端，并读取它要传输的数据。这样，就不用开一大堆线程去一对一的监听IO状态变化了。

而select、poll、epoll三个东西都是上述思路的不同实现方式，并且是按照它们被列出的顺序被先后发明出来的，每个更新发明出来的方法都是在之前方法上做了一些改进。

poll在select的基础上，去掉了select给定的只能最多处理1024个客户端连接的限制，并不会再修改传入该方法的参数数组。epoll是在poll的基础上，使其变成了线程安全的（不会因为通信过程中其它线程关掉了已经加入到select或者poll中的IO流而产生未知的后果），同时会告知服务端具体是哪个IO流来了数据，不需要靠服务器自己去找。
————————————————
版权声明：本文为CSDN博主「蓝色枫魂」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_32690999/article/details/80157034

https://www.zhihu.com/question/26943938

https://mp.weixin.qq.com/s/Qpa0qXxuIM8jrBqDaXmVNA
