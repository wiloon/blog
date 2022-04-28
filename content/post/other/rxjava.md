---
title: RxJava
author: "-"
date: 2011-08-29T04:48:41+00:00
url: rxjava

categories:
  - Java

tags:
  - reprint
---
## RxJava
### Reactive Extension (RX)
RX在Future和Promise的基础上更进了一步，将单一的事件处理扩展到多个先后相关的事件流处理。举个例子，鼠标拖拽事件，是由一个MouseDown事件加多个MouseMove事件以及一个MouseUp事件构成，Promise处理这种情况需要处理器具有状态记住拖拽的阶段。RX将MouseDown和MouseUp这些事件的处理标准化，并且将拖拽阶段的这一共享状态从业务处理器中抽离，而固化到事件处理流程中。RX抽象了大量的事件操作，使得我们可以将重心放到事件流程建模中，而不是具体的一个接一个事件的处理。共享状态从处理器中抽离也有利于业务处理器的重用以及并发处理。

综上，响应式编程中的事件驱动，要求

对事件建模
对事件流程建模
对事件相关性建模

---

在那个RxJava刚刚火爆的年代，那是一个荒蛮的年代。我们在异步方面资源匮乏，手头仅有ThreadPool,AsyncTask和Handler这些基础封装的异步库。所以当我们看见RxJava这个新奇的小玩意，当我们看到异步还可以这么简单，轻而易举的解决Concurrency问题。我们当然如获至宝。
而我们现在选择就更多了，无论是Java 8本身提供的CompletableFuture。还是后起之秀Kotlin上的Coroutine，还有Android 上官方提供的LiveData

作者：W_BinaryTree
链接：https://juejin.cn/post/6844903838978146317
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


RxJava 在 GitHub 主页上的自我介绍是 "a library for composing asynchronous and event-based programs using observable sequences for the Java VM" (一个在 Java VM 上使用可观测的序列来组成异步的、基于事件的程序的库）


ReactiveX是Reactive Extensions的缩写，一般简写为Rx，最初是LINQ的一个扩展，由微软的架构师Erik Meijer领导的团队开发，在2012年11月开源，Rx是一个编程模型，目标是提供一致的编程接口，帮助开发者更方便的处理异步数据流，Rx库支持.NET、JavaScript和C++，Rx近几年越来越流行了，现在已经支持几乎全部的流行编程语言了，Rx的大部分语言库由ReactiveX这个组织负责维护，比较流行的有RxJava/RxJS/Rx.NET，社区网站是 reactivex.io。

Netflix参考微软的Reactive Extensions创建了Java的实现RxJava，主要是为了简化服务器端的并发。2013年二月份,Ben Christensen 和 Jafar Husain发在Netflix技术博客的一篇文章第一次向世界展示了RxJava。

RxJava也在Android开发中得到广泛的应用。

ReactiveX
An API for asynchronous programming with observable streams.
A combination of the best ideas from the Observer pattern, the Iterator pattern, and functional programming.

>https://juejin.cn/post/6844903838978146317
>http://reactivex.io/
>https://github.com/ReactiveX/RxJava
>https://gank.io/post/560e15be2dca930e00da1083#toc_31