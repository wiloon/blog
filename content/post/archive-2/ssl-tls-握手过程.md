---
title: SSL/TLS 握手过程
author: "-"
date: 2019-01-06T10:06:11+00:00
url: /?p=13336
categories:
  - Inbox
tags:
  - reprint
---
## SSL/TLS 握手过程

### Client Hello

握手第一步是客户端向服务端发送 Client Hello 消息,这个消息里包含了一个客户端生成的随机数 Random1、客户端支持的加密套件 (Support Ciphers) 和 SSL Version 等信息。通过 Wireshark 抓包,我们可以看到如下信息:

Wireshark 抓包的用法可以参考这篇文章: <https://segmentfault.com/a/1190000018746027>

Server Hello
  
第二步是服务端向客户端发送 Server Hello 消息,这个消息会从 Client Hello 传过来的 Support Ciphers 里确定一份加密套件,这个套件决定了后续加密和生成摘要时具体使用哪些算法,另外还会生成一份随机数 Random2。注意,至此客户端和服务端都拥有了两个随机数 (Random1+ Random2) ,这两个随机数会在后续生成对称秘钥时用到。

Certificate
  
这一步是服务端将自己的证书下发给客户端,让客户端验证自己的身份,客户端验证通过后取出证书中的公钥。

Server Key Exchange
  
如果是DH算法,这里发送服务器使用的DH参数。RSA算法不需要这一步。

Certificate Request
  
Certificate Request 是服务端要求客户端上报证书,这一步是可选的,对于安全性要求高的场景会用到。
  
Server Hello Done
  
Server Hello Done 通知客户端 Server Hello 过程结束。

Certificate Verify
  
客户端收到服务端传来的证书后,先从 CA 验证该证书的合法性,验证通过后取出证书中的服务端公钥,再生成一个随机数 Random3,再用服务端公钥非对称加密 Random3 生成 PreMaster Key。
  
Client Key Exchange
  
上面客户端根据服务器传来的公钥生成了 PreMaster Key,Client Key Exchange 就是将这个 key 传给服务端,服务端再用自己的私钥解出这个 PreMaster Key 得到客户端生成的 Random3。至此,客户端和服务端都拥有 Random1 + Random2 + Random3,两边再根据同样的算法就可以生成一份秘钥,握手结束后的应用层数据都是使用这个秘钥进行对称加密。为什么要使用三个随机数呢？这是因为 SSL/TLS 握手过程的数据都是明文传输的,并且多个随机数种子来生成秘钥不容易被暴力破解出来。客户端将 PreMaster Key 传给服务端的过程如下图所示:

Change Cipher Spec(Client)
  
这一步是客户端通知服务端后面再发送的消息都会使用前面协商出来的秘钥加密了,是一条事件消息。

Encrypted Handshake Message(Client)
  
这一步对应的是 Client Finish 消息,客户端将前面的握手消息生成摘要再用协商好的秘钥加密,这是客户端发出的第一条加密消息。服务端接收后会用秘钥解密,能解出来说明前面协商出来的秘钥是一致的。

Change Cipher Spec(Server)
  
这一步是服务端通知客户端后面再发送的消息都会使用加密,也是一条事件消息。
  
Encrypted Handshake Message(Server)
  
这一步对应的是 Server Finish 消息,服务端也会将握手过程的消息生成摘要再用秘钥加密,这是服务端发出的第一条加密消息。客户端接收后会用秘钥解密,能解出来说明协商的秘钥是一致的。

Application Data
  
到这里,双方已安全地协商出了同一份秘钥,所有的应用层数据都会用这个秘钥加密后再通过 TCP 进行可靠传输。
  
双向验证
  
前面提到 Certificate Request 是可选的,下面这张图展示了双向验证的过程:

握手过程优化
  
如果每次重连都要重新握手还是比较耗时的,所以可以对握手过程进行优化。从下图里我们看到 Client Hello 消息里还附带了上一次的 Session ID,服务端接收到这个 Session ID 后如果能复用就不再进行后续的握手过程。

除了上述的 Session 复用,SSL/TLS 握手还有一些优化技术,例如 False Start、Session Ticket 等,这方面的介绍具体可以参考这篇文章。
  
总结
  
前面我们一起详细地了解了整个 SSL/TLS 的握手过程,这部分知识在平时的开发过程中很少用到,但能让我们更清楚地了解 HTTPS 的工作原理,而不仅仅是只知道 HTTPS 会加密数据十分安全。同时这个过程也是各种加密技术的一个经典运用,也能帮助我们加深加密相关技术的理解。最后,建议大家也用 Wireshark 实际抓包体验一下这个过程来加深印象,enjoy~
  
参考资料

### golang tls

<https://github.com/denji/golang-tls>

### RTT

Round Trip Time, 也就是一个数据包从发出去到回来的时间。  
<https://coolshell.cn/articles/11609.html#TCP%E7%9A%84RTT%E7%AE%97%E6%B3%95>

TCP的RTT算法
从前面的TCP重传机制我们知道Timeout的设置对于重传非常重要。

设长了,重发就慢,丢了老半天才重发,没有效率,性能差；
设短了,会导致可能并没有丢就重发。于是重发的就快,会增加网络拥塞,导致更多的超时,更多的超时导致更多的重发。
而且,这个超时时间在不同的网络的情况下,根本没有办法设置一个死的值。只能动态地设置。 为了动态地设置,TCP引入了RTT——Round Trip Time,也就是一个数据包从发出去到回来的时间。这样发送端就大约知道需要多少的时间,从而可以方便地设置Timeout——RTO (Retransmission TimeOut)

<https://www.zhihu.com/question/39244840>
不包括数据发射 (即将数据推送到数据链路上) 的时间。即,RTT为数据完全发送完 (完成最后一个比特推送到数据链路上) 到收到确认信号的时间。

《计算机网络自顶向下方法》中的一个插图能清晰地说明问题:
t1为发送第一个比特的时刻

t2为发完最后一个比特的时刻

t3为接收到确认信号的时刻

图中明确指出: RTT = t3 - t2

---

<http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html>
  
<https://segmentfault.com/a/1190000002554673>
  
<https://imququ.com/post/optimize-tls-handshake.html>
  
<http://blog.csdn.net/fw0124/article/details/40983787>

<https://www.jianshu.com/p/7158568e4867>
