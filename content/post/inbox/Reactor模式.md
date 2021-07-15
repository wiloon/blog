---
title: "Reactor, Dispatcher 模式"
author: "-"
date: "2021-07-11 09:44:24"
url: "Reactor模式"
categories:
  - inbox
tags:
  - inbox
---
# Reactor / Dispatcher 模式
了解 Reactor 模式，就要先从事件驱动的开发方式说起。

我们知道，服务器开发，CPU 的处理速度远高于 IO 速度，为了避免 CPU 因为 IO 为阻塞，好一点的方法是多进程或线程处理，但这会带来一些进程切换的开销。

这时先驱者找到了事件驱动，或者叫回调的方法。这种方式就是，应用向一个中间人注册一个回调（Event handler），当 IO 就绪后，这个中间人产生一个事件，并通知此 handler 进行处理。这种回调的方式，也实现了"好莱坞原则" - "Don't call us, we'll call you."

那在 IO 就绪这个事件后，谁来充当这个中间人？Reactor 模式的答案是：有一个不断等待和循环的单独进程（线程）来做这件事，它接受所有 handler 的注册，并负责向操作系统查询 IO 是否就绪，在就绪后用指定的 handler 进行处理，这个角色的名称就叫做 Reactor。

http://www.linkedkeeper.com/12.html

---


Reactor 翻译过来的意思是「反应堆」，可能大家会联想到物理学里的核反应堆，实际上并不是的这个意思。这里的反应指的是「对事件反应」，也就是来了一个事件，Reactor 就有相对应的反应/响应。事实上，Reactor 模式也叫 Dispatcher 模式，我觉得这个名字更贴合该模式的含义，即 I/O 多路复用监听事件，收到事件后，根据事件类型分配（Dispatch）给某个进程 / 线程。Reactor 模式主要由 Reactor 和处理资源池这两个核心部分组成，它俩负责的事情如下：Reactor 负责监听和分发事件，事件类型包含连接事件、读写事件；处理资源池负责处理事件，如 read -> 业务逻辑 -> send；Reactor 模式是灵活多变的，可以应对不同的业务场景，灵活在于：Reactor 的数量可以只有一个，也可以有多个；处理资源池可以是单个进程 / 线程，也可以是多个进程 /线程；

作者：小林coding
链接：https://www.zhihu.com/question/26943938/answer/1856426252
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


Reactor模式也叫反应器模式，大多数IO相关组件如Netty、Redis在使用的IO模式
最最原始的网络编程思路就是服务器用一个while循环，不断监听端口是否有新的套接字连接，如果有，那么就调用一个处理函数处理，类似：

while(true){

socket = accept();

handle(socket)

}
这种方法的最大问题是无法并发，效率太低，如果当前的请求没有处理完，那么后面的请求只能被阻塞，服务器的吞吐量太低。

之后，想到了使用多线程，也就是很经典的connection per thread，每一个连接用一个线程处理，类似：

### 多线程IO




https://www.cnblogs.com/crazymakercircle/p/9833847.html

http://gee.cs.oswego.edu/dl/cpjslides/nio.pdf

