---
title: RPC,RMI,Web Services,JMS
author: w1100n
type: post
date: 2012-10-15T09:13:47+00:00
url: /?p=4471
categories:
  - Linux

---
1. RPC：RPC本身没有规范,但基本的工作机制是一样的，即：serialization/deserialization+stub+skeleton

<div id="article_content">
  
    宽泛的讲，只要能实现远程调用，都是RPC，如:rmi .net-remoting ws/soap/rest hessian xmlrpc thrift potocolbuffer
  
  
    2. RMI是一种PRC.java的RMI就是java平台上的RPC技术方案。
  
  
    3. JMS是java平台上的消息规范。一般jms消息不是一个xml，而是一个java对象，很明显，jms没考虑异构系统，说白 了，JMS就没考虑非java的东西。但是好在现在大多数的jms provider（就是JMS的各种实现产品）都解决了异构问题。
  
  
    4. soap专注于远程服务调用，jms专注于信息交换。
  
  
    5. 大多数情况下soap是两系统间的直接交互（Consumer <-> Producer），而大多数情况下jms是三方系统交互（Consumer <- Broker -> Producer）。当然，JMS也可以实现request-response模式的通信，只要Consumer或Producer其中一方兼任broker即可。
  
  
    6. 多数情况下，ws是同步的，jms是异步。虽然，ws也可以是异步的，而jms也可以是同步的。
  
