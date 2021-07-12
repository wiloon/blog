---
title: "Reactor模式"
author: "-"
date: "2021-07-11 09:44:24"
url: "Reactor模式"
categories:
  - inbox
tags:
  - inbox
---

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

