---
title: loom
author: "-"
date: 2011-09-04T02:32:49+00:00
url: loom
categories:
  - java

tags:
  - reprint
---
## loom

Oracle 已经停止了异步的JDBC (ADBA) 标准的相关工作。这传达了一个相当明确而又重要的信息： (在Java平台上）fiber 是未来的方向，而异步不是。Oracle 认为异步程序太难写难调，因此全力转向同步的方案 ( 注意这个帖子混用了 fiber 和 lightweight thread 这两个术语，后面的Ron用的术语是 lightweight virtual thread ）

On Wednesday, September 18, at Oracle CodeOne Oracle announced that Oracle will stop work on ADBA (Asynchronous Database Access)

The Java team's position is that synchronous code is easier to write, test, debug, maintain, and understand than async code. The only reason to write async code is that threads are so expensive. Project Loom will add fibers, very lightweight threads, to Java. Fibers are so light weight that it is completely practical to spin up as many as you need. So just write first semester CS synchronous code and and execute it on a dedicated fiber. This is much easier than writing async code to do the same task. Synchronous code will use the same JDBC we all know and love. No need to learn a new API. Existing code can be made to work with few if any changes.

异步代码太难搞，还是同步代码好。正确的方向应该是"Code like sync, works like async"。即从平台的层面支持海量fiber到少数几个内核线程的映射。啥时候发布不好说 (We honestly don't know）。现在的实现是基于 Continuation 的，它的本质是一个用户态的 scheduler，当某个线程调用阻塞方法 (LockSupport.park/Socket.accept）时，如果这是一个轻量级线程，直接把相关的栈帧从当前的栈顶挪走，换另外一个Continuation到栈上，避免context switch的开销：

作者：blindpirate
链接：https://www.zhihu.com/question/67579790/answer/1128786671
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

>https://openjdk.java.net/projects/loom/
>https://github.com/openjdk/loom
>https://mail.openjdk.java.net/pipermail/jdbc-spec-discuss/2019-September/000529.html
>https://www.jianshu.com/p/5db701a764cb
>https://www.zhihu.com/question/67579790
>https://www.zhihu.com/question/23084473
>https://www.jdon.com/54488
>http://cr.openjdk.java.net/~rpressler/loom/Loom-Proposal.html