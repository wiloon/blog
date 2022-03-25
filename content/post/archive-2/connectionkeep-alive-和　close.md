---
title: connection=keep alive 和close
author: "-"
date: 2015-12-02T01:16:53+00:00
url: /?p=8501
categories:
  - Uncategorized

tags:
  - reprint
---
## connection=keep alive 和close
浏览器和服务器在建立 http 连接的时候需要3次握手, 在高并发的环境下每一次建立连接都3次握手会消耗太多的服务资源, 这个本质上是由于http是无状态造成的．http1.0默认开启了 connection=close 模式意味着服务器和客户端都需要关闭TCP连接, 而客户端是通过判断连接关闭来判断响应是否都收到了。http1.1 默认开启connection=keep-alive模式 (长连接) ,主要为了解决浏览器内高并发的访问服务器资源,而且每次的访问都可以复用连接,从而提高响应速度。但是也需要注意,因为浏览器无法判断当前发送的二进制码流是否结束, 也就是所谓的粘包问题, 所以在 keep-alive 模式下, 服务器需要显示的返回Content-Length 用来根据码流的长度来判断一个完整的 response 是否结束。