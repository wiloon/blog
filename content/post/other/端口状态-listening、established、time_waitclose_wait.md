---
title: tcp 状态 LISTENING、ESTABLISHED、TIME_WAIT,CLOSE_WAIT
author: "-"
date: 2015-04-11T02:31:51+00:00
url: /?p=7455
categories:
  - network
tags:
  - Network
  - todo

---
## tcp状态 LISTENING, ESTABLISHED, TIME_WAIT, CLOSE_WAIT

TCP协议规定, 对于已经建立的连接, 网络双方要进行四次握手才能成功断开连接, 如果缺少了其中某个步骤, 将会使连接处于假死状态, 连接本身占用的资源不会被释放。网络服务器程序要同时管理大量连接, 所以很有必要保证无用连接完全断开, 否则大量僵死的连接会浪费许多服务器资源。在众多TCP状态中, 最值得注意的状态有两个: CLOSE_WAIT 和 TIME_WAIT。

- LISTENING 状态
  
TCP 服务启动后首先处于侦听 (LISTENING) 状态。 

- ESTABLISHED 状态
  
ESTABLISHED的意思是建立连接。表示两台机器正在通信。

- CLOSE_WAIT
  
对方主动关闭连接或者网络异常导致连接中断, 这时我方的状态会变成 CLOSE_WAIT 此时我方要调用 close() 来使得连接正确关闭

## TIME_WAIT
  
我方主动调用 close() 断开连接, 收到对方确认后状态变为 TIME_WAIT。 TCP 协议规定 TIME_WAIT 状态会一直持续 2MSL (即两倍的分段最大生存期), 以此来确保旧的连接状态不会对新连接产生影响。处于 TIME_WAIT 状态的连接占用的资源不会被内核释放, 所以作为服务器, 在可能的情况下, 尽量不要主动断开连接, 以减少 TIME_WAIT 状态造成的资源浪费。

目前有一种避免 TIME_WAIT 资源浪费的方法, 就是关闭 socket 的 LINGER 选项。但这种做法是 TCP 协议不推荐使用的, 在某些情况下这个操作可能会带来错误。

>http://www.cppblog.com/prayer/archive/2009/04/01/78592.html 
>http://www4.cs.fau.de/Projects/JX/Projects/TCP/tcpstate.html


## TIME_WAIT CLOSE_WAIT
http://blog.csdn.net/kobejayandy/article/details/17655739

在服务器的日常维护过程中,会经常用到下面的命令: 

netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
  
它会显示例如下面的信息: 

TIME_WAIT 814
  
CLOSE_WAIT 1
  
FIN_WAIT1 1
  
ESTABLISHED 634
  
SYN_RECV 2
  
LAST_ACK 1

常用的三个状态是: ESTABLISHED 表示正在通信, TIME_WAIT 表示主动关闭, CLOSE_WAIT 表示被动关闭。

TCP协议规定,对于已经建立的连接,网络双方要进行四次握手才能成功断开连接,如果缺少了其中某个步骤,将会使连接处于假死状态,连接本身占用的资源不会被释放。网络服务器程序要同时管理大量连接,所以很有必要保证无用连接完全断开,否则大量僵死的连接会浪费许多服务器资源。在众多TCP状态中,最值得注意的状态有两个: CLOSE_WAIT 和 TIME_WAIT。

## TIME_WAIT
  
TIME_WAIT 是主动关闭链接时形成的,等待 2MSL 时间, 约4分钟。 主要是防止最后一个ACK丢失。  由于TIME_WAIT 的时间会非常长,因此 server 端应尽量减少主动关闭连接

## CLOSE_WAIT
  
CLOSE_WAIT是被动关闭连接是形成的。根据TCP状态机,服务器端收到客户端发送的FIN,则按照TCP实现发送ACK,因此进入CLOSE_WAIT状态。但如果服务器端不执行close(),就不能由CLOSE_WAIT迁移到LAST_ACK,则系统中会存在很多CLOSE_WAIT状态的连接。此时,可能是系统忙于处理读、写操作,而未将已收到FIN的连接,进行close。此时,recv/read已收到FIN的连接socket,会返回0。

为什么需要 TIME_WAIT 状态？
  
假设最终的ACK丢失,server将重发FIN,client必须维护TCP状态信息以便可以重发最终的ACK,否则会发送RST,结果server认为发生错误。TCP实现必须可靠地终止连接的两个方向(全双工关闭),client必须进入 TIME_WAIT 状态,因为client可能面 临重发最终ACK的情形。
  
为什么 TIME_WAIT 状态需要保持 2MSL 这么长的时间？
  
如果 TIME_WAIT 状态保持时间不足够长(比如小于2MSL),第一个连接就正常终止了。第二个拥有相同相关五元组的连接出现,而第一个连接的重复报文到达,干扰了第二个连接。TCP实现必须防止某个连接的重复报文在连接终止后出现,所以让TIME_WAIT状态保持时间足够长(2MSL),连接相应方向上的TCP报文要么完全响应完毕,要么被 丢弃。建立第二个连接的时候,不会混淆。

### TIME_WAIT 和 CLOSE_WAIT 状态 socket 过多
  
如果服务器出了异常, 百分之八九十都是下面两种情况: 

1. 服务器保持了大量 TIME_WAIT 状态
2. 服务器保持了大量 CLOSE_WAIT 状态, 简单来说 CLOSE_WAIT 数目过大是由于被动关闭连接处理不当导致的。

因为 linux 分配给一个用户的文件句柄是有限的, 而 TIME_WAIT 和 CLOSE_WAIT 两种状态如果一直被保持, 那么意味着对应数目的通道就一直被占着, 而且是 "占着茅坑不使劲", 一旦达到句柄数上限, 新的请求就无法被处理了, 接着就是大量 `Too Many Open Files` 异常
