---
title: RPC,RMI,Web Services,JMS
author: "-"
date: 2012-10-15T09:13:47+00:00
url: /?p=4471
categories:
  - Linux

---
## RPC (Remote Procedure Call), RMI, Web Services, JMS

1. RPC: RPC本身没有规范,但基本的工作机制是一样的，即: serialization/deserialization+stub+skeleton
宽泛的讲，只要能实现远程调用，都是RPC，如: rmi .net-remoting ws/soap/rest hessian xmlrpc thrift potocolbuffer
2. RMI 是一种PRC.java的RMI就是java平台上的RPC技术方案。
3. JMS 是java平台上的消息规范。一般jms消息不是一个xml，而是一个java对象，很明显，jms没考虑异构系统，说白 了，JMS就没考虑非java的东西。但是好在现在大多数的jms provider（就是JMS的各种实现产品) 都解决了异构问题。
4. soap 专注于远程服务调用，jms专注于信息交换。
5. 大多数情况下soap是两系统间的直接交互（Consumer <-> Producer) ，而大多数情况下jms是三方系统交互（Consumer <- Broker -> Producer) 。当然，JMS也可以实现request-response模式的通信，只要Consumer或Producer其中一方兼任broker即可。
6. 多数情况下，ws是同步的，jms是异步。虽然，ws也可以是异步的，而jms也可以是同步的。

## JAX-RPC
通过使用JAX-RPC(Java API for XML-based RPC)，已有的Java类或Java应用都能够被重新包装，并以Web Services的形式发布。JAX-RPC提供了将RPC参数(in/out)编码和解码的API，使开发人员可以方便地使用SOAP消息来完成RPC调用。同样，对于那些使用EJB(Enterprise JavaBeans)的商业应用而言，同样可以使用JAX-RPC来包装成Web服务，而这个Web Service的WSDL界面是与原先的EJB的方法是对应一致的。JAX-RPC为用户包装了Web服务的部署和实现，对Web服务的开发人员而言，SOAP/WSDL变得透明，这有利于加速Web服务的开发周期。


JAX-RPC(基于可扩展标记语言XML的远程过程调用的Java应用程序接口)是Java Web服务开发包(WSDP)的应用程序接口(API)，WSDP能使Java开发者在Web服务或其他的Web应用程序中包括远程过程调用(RPC)。JAX-RPC致力于要使应用程序或Web服务调用其他应用程序或Web服务变得更加容易。


JAX-RPC为基于SOAP(简单对象访问协议)的应用程序的开发提供了一个编程模型。JAX-RPC编程模型通过抽象SOAP协议层的运行机制与提供Java和Web服务描述语言(WSDL)间的映射服务来简化开发。

### rmi, rpc, grpc
RMI是远程方法调用（Remote Method Invocation) 的简称，其是一种计算机之间利用远程对象互相调用实现双方通讯的一种通讯机制，它能够让一个Java虚拟机上的对象调用另一个Java虚拟机上对象的方法。Java RMI在JDK1.1中实现的，其它可以被看作是RPC的Java版本。但是传统RPC并不能很好地应用于分布式对象系统。而Java RMI 则支持存储于不同地址空间的程序级对象之间彼此进行通信，实现远程对象之间的无缝远程调用。

RMI相对于其它比较复杂的RPC要简单的多（比如Thrift、Grpc、Protoff等) ，本文仅仅简单阐述了其组成、实现原理图、代码示例。如果想深入学习和了解，可以自行解读源码或参照其它解读文档。
  
局限性
  
相比于其它RPC(Thrift、Grpc等)，RMI存在许多的缺点: 

RMI只能实现JAVA系统之间的调用，而WebService可以实现跨语言实现系统之间的调用。

RMI使用了JAVA默认的序列化方式，对于性能要求比较高的系统，可能需要其他的序列化方案来解决。

RMI服务在运行时难免会存在故障，例如，如果RMI服务无法连接了，就会导致客户端无法响应的现象。

RMI服务是基于远程接口提供的服务，一旦远程接口名称或者参数发生变化，客户端程序必须作出相应改变才能保证系统的稳定。
  
————————————————
  
版权声明: 本文为CSDN博主「皮斯特劳沃」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/pistolove/article/details/64122191
