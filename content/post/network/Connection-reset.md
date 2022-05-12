---
title: Connection reset
author: "-"
date: 2011-09-14T06:22:13+00:00
url: /?p=791
categories:
  - Web
tags:$
  - reprint
---
## Connection reset
在使用HttpClient调用后台resetful服务时，“Connection reset”是一个比较常见的问题，有同学跟我私信说被这个问题困扰很久了，今天就来分析下，希望能帮到大家。例如我们线上的网关日志就会抛该错误：



 

从日志中可以看到是Socket socket 在read数据时抛出了该错误。

 

导致“Connection reset”的原因是服务器端因为某种原因关闭了Connection，而客户端依然在读写数据，此时服务器会返回复位标志“RST”，然后此时客户端就会提示“java.net.SocketException: Connection reset”。

可能有同学对复位标志“RST”还不太了解，这里简单解释一下：

TCP建立连接时需要三次握手，在释放连接需要四次挥手；例如三次握手的过程如下：

第一次握手：客户端发送syn包 (syn=j）到服务器，并进入SYN_SENT状态，等待服务器确认；

第二次握手：服务器收到syn包，并会确认客户的SYN (ack=j+1），同时自己也发送一个SYN包 (syn=k），即SYN+ACK包，此时服务器进入SYN_RECV状态；

第三次握手：客户端收到服务器的SYN+ACK包，向服务器发送确认包ACK(ack=k+1），此包发送完毕，客户端和服务器进入ESTABLISHED (TCP连接成功）状态，完成三次握手。

可以看到握手时会在客户端和服务器之间传递一些TCP头信息，比如ACK标志、SYN标志以及挥手时的FIN标志等。

除了以上这些常见的标志头信息，还有另外一些标志头信息，比如推标志PSH、复位标志RST等。其中复位标志RST的作用就是“复位相应的TCP连接”。

 

TCP连接和释放时还有许多细节，比如半连接状态、半关闭状态等。详情请参考这方面的巨著《TCP/IP详解》和《UNIX网络编程》。

 

前面说到出现“Connection reset”的原因是服务器关闭了Connection[调用了Socket.close()方法]。大家可能有疑问了：服务器关闭了Connection为什么会返回“RST”而不是返回“FIN”标志。原因在于Socket.close()方法的语义和TCP的“FIN”标志语义不一样：发送TCP的“FIN”标志表示我不再发送数据了，而Socket.close()表示我不在发送也不接受数据了。问题就出在“我不接受数据” 上，如果此时客户端还往服务器发送数据，服务器内核接收到数据，但是发现此时Socket已经close了，则会返回“RST”标志给客户端。当然，此时客户端就会提示：“Connection reset”。详细说明可以参考oracle的有关文档：http://docs.oracle.com/javase/1.5.0/docs/guide/net/articles/connection_release.html。

 

另一个可能导致的“Connection reset”的原因是服务器设置了Socket.setLinger (true, 0)。但我检查过线上的tomcat配置，是没有使用该设置的，而且线上的服务器都使用了nginx进行反向代理，所以并不是该原因导致的。关于该原因上面的oracle文档也谈到了并给出了解释。

 

此外啰嗦一下，另外还有一种比较常见的错误“Connection reset by peer”，该错误和“Connection reset”是有区别的：

服务器返回了“RST”时，如果此时客户端正在从Socket socket 的输出流中读数据则会提示Connection reset”；

服务器返回了“RST”时，如果此时客户端正在往Socket socket 的输入流中写数据则会提示“Connection reset by peer”。

“Connection reset by peer”如下图所示：



 

 

前面谈到了导致“Connection reset”的原因，而具体的解决方案有如下几种：

 

出错了重试；

客户端和服务器统一使用TCP长连接；

客户端和服务器统一使用TCP短连接。

首先是出错了重试：这种方案可以简单防止“Connection reset”错误，然后如果服务不是“幂等”的则不能使用该方法；比如提交订单操作就不是幂等的，如果使用重试则可能造成重复提单。

 

然后是客户端和服务器统一使用TCP长连接：客户端使用TCP长连接很容易配置 (直接设置HttpClient就好），而服务器配置长连接就比较麻烦了，就拿tomcat来说，需要设置tomcat的maxKeepAliveRequests、connectionTimeout等参数。另外如果使用了nginx进行反向代理或负载均衡，此时也需要配置nginx以支持长连接 (nginx默认是对客户端使用长连接，对服务器使用短连接）。

使用长连接可以避免每次建立TCP连接的三次握手而节约一定的时间，但是我这边由于是内网，客户端和服务器的3次握手很快，大约只需1ms。ping一下大约0.93ms (一次往返）；三次握手也是一次往返 (第三次握手不用返回）。根据80/20原理，1ms可以忽略不计；又考虑到长连接的扩展性不如短连接好、修改nginx和tomcat的配置代价很大 (所有后台服务都需要修改）；所以这里并没有使用长连接。ping服务器的时间如下图：



 

最后的解决方案是客户端和服务器统一使用TCP短连接：我这边正是这么干的，而使用短连接既不用改nginx配置，也不用改tomcat配置，只需在使用HttpClient时使用http1.0协议并增加http请求的header信息 (Connection: Close），源码如下：

 

最后再补充几句，虽然对于每次请求TCP长连接只能节约大约1ms的时间，但是具体是使用长连接还是短连接还是要衡量下，比如你的服务每天的pv是1亿，那么使用长连接节约的总时间为：

神奇的是，亿万级pv的服务使用长连接一天内节约的总时间为27.78小时 (竟然大于一天）。

所以使用长连接还是短连接大家需要根据自己的服务访问量、扩展性等因素衡量下。但是一定要注意：服务器和客户端的连接一定要保持一致，要么都是长连接，要么都是短连接。


>https://blog.csdn.net/liyantianmin/article/details/82505734