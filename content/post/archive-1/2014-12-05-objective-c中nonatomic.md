---
title: ExecutorService
author: "-"
type: post
date: 2014-12-05T01:14:19+00:00
url: /?p=7101
categories:
  - Uncategorized

---
在 Java 1.5 引入 ExecutorService 之后，基本上已经不推荐直接创建 Thread 对象，而是统一使用 ExecutorService。毕竟从接口的易用程度上来说 ExecutorService 就远胜于原始的 Thread，更不用提 java.util.concurrent 提供的数种线程池，Future 类，Lock 类等各种便利工具。

http://blog.dyngr.com/blog/2016/09/15/java-forkjoinpool-internals/