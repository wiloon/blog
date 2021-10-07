---
title: loom
author: "-"
date: 2011-09-04T02:32:49+00:00
url: loom
categories:
  - java

---

Oracle已经停止了异步的JDBC标准的相关工作。这传达了一个相当明确而又重要的信息：（在Java平台上）fiber是未来的方向，而异步不是。Oracle认为异步程序太难写难调，因此全力转向同步的方案

异步代码太难搞，还是同步代码好。正确的方向应该是"Code like sync, works like async"。即从平台的层面支持海量fiber到少数几个内核线程的映射。啥时候发布不好说（We honestly don't know）。现在的实现是基于Continuation的，它的本质是一个用户态的scheduler，当某个线程调用阻塞方法（LockSupport.park/Socket.accept）时，如果这是一个轻量级线程，直接把相关的栈帧从当前的栈顶挪走，换另外一个Continuation到栈上，避免context switch的开销：

作者：blindpirate
链接：https://www.zhihu.com/question/67579790/answer/1128786671
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

>https://github.com/openjdk/loom
>https://mail.openjdk.java.net/pipermail/jdbc-spec-discuss/2019-September/000529.html
>https://www.jianshu.com/p/5db701a764cb
>https://www.zhihu.com/question/67579790
>https://www.zhihu.com/question/23084473
>https://www.jdon.com/54488
