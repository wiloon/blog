---
title: JAX-WS
author: "-"
date: 2011-10-31T03:16:56+00:00
url: /?p=1404
categories:
  - Java
  - Web
tags:$
  - reprint
---
## JAX-WS
JAX-WS规范是一组XML web services的JAVA API。JAX-WS允许开发者可以选择RPC-oriented或者message-oriented 来实现自己的web services。

在 JAX-WS中，一个远程调用可以转换为一个基于XML的协议例如SOAP。在使用JAX-WS过程中，开发者不需要编写任何生成和处理SOAP消息的代码。JAX-WS的运行时实现会将这些API的调用转换成为对应的SOAP消息。

在服务器端，用户只需要通过Java语言定义远程调用所需要实现的接口SEI  (service endpoint interface) ，并提供相关的实现，通过调用JAX-WS的服务发布接口就可以将其发布为WebService接口。

在客户端，用户可以通过JAX-WS的API创建一个代理 (用本地对象来替代远程的服务) 来实现对于远程服务器端的调用。

当然 JAX-WS 也提供了一组针对底层消息进行操作的API调用，你可以通过Dispatch 直接使用SOAP消息或XML消息发送请求或者使用Provider处理SOAP或XML消息。

通过web service所提供的互操作环境，我们可以用JAX-WS轻松实现JAVA平台与其他编程环境 (.net等) 的互操作。

JAX-WS与JAX-RPC之间的关系

Sun最开始的web services的实现是JAX-RPC 1.1 (JSR 101)。这个实现是基于Java的RPC,并不完全支持schema规范，同时没有对Binding和Parsing定义标准的实现。

JAX-WS2.0 (JSR 224)是Sun新的web services协议栈，是一个完全基于标准的实现。在binding层，使用的是the Java Architecture for XML Binding (JAXB, JSR 222)，在parsing层，使用的是the Streaming API for XML (StAX, JSR 173)，同时它还完全支持schema规范。