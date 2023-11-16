---
title: socket, 套接字, 套接口 
author: "-"
date: 2013-11-17T08:40:04+00:00
url: socket
categories:
  - network
tags:
  - reprint

---
## socket, 套接字, 套接口

应用层通过传输层进行数据通信时，TCP 和 UDP 会遇到同时为多个应用程序进程提供并发服务的问题。多个 TCP 连接或多个应用程序进程可能需要通过同一个 TCP 协议端口传输数据。为了区别不同的应用程序进程和连接，许多计算机操作系统为应用程序与 TCP/IP 协议交互提供了称为 socket  (Socket) 的接口，区分不同应用程序进程间的网络通信和连接。
  
生成 socket ，主要有3个参数: 通信的`目的 IP 地址`、使用的传输层协议(TCP或UDP)和使用的`端口号`。Socket原意是"插座"。通过将这3个参数结合起来，与一个"插座"Socket绑定，应用层就可以和传输 层通过 socket 接口，区分来自不同应用程序进程或网络连接的通信，实现数据传输的并发服务。
  
Socket可以看成在两个程序进行通讯连接中的一个端点，一个程序将一段信息写入Socket中，该Socket将这段信息发送给另外一个Socket中，使这段信息能传送到其他程序中。
  
Host A上的程序A将一段信息写入Socket中，Socket的内容被Host A的网络管理软件访问，并将这段信息通过Host A的网络接口卡发送到Host B，Host B的网络接口卡接收到这段信息后，传送给Host B的网络管理软件，网络管理软件将这段信息保存在Host B的Socket中，然后程序B才能在Socket中阅读这段信息。
  
要通过互联网进行通信，至少需要一对 socket ，一个运行于客户机端，称之为ClientSocket，另一个运行于服务器端，称之为serverSocket。
  
根据连接启动的方式以及本地 socket 要连接的目标， socket 之间的连接过程可以分为三个步骤: 服务器监听，客户端请求，连接确认。
  
服务器监听: 是服务器端 socket 并不定位具体的客户端 socket ，而是处于等待连接的状态，实时监控网络状态。
  
客户端请求: 是指由客户端的 socket 提出连接请求，要连接的目标是服务器端的 socket 。为此，客户端的 socket 必须首先描述它要连接的服务器的 socket ，指出服务器端 socket 的地址和端口号，然后就向服务器端 socket 提出连接请求。
  
连 接确认: 是指当服务器端 socket 监听到或者说接收到客户端 socket 的连接请求，它就响应客户端 socket 的请求，建立一个新的线程，把服务器端 socket 的描述发给客 户端，一旦客户端确认了此描述，连接就建立好了。而服务器端 socket 继续处于监听状态，继续接收其他客户端 socket 的连接请求。
  
socket的英文原义是"孔"或"插座"。作为4BDS UNIX的进程通信机制，取后一种意思。通常也称作" socket "，用于描述IP地址和端口，是一个通信链的句柄。在Internet上的主机一般运行了多个服务软件，同时提供几种服务。每种服务都打开一个Socket，并绑定到一个端口上，不同的端口对应于不同的服务。Socket正如其英文原意那样，象一个多孔插座。一台主机犹如布满各种插座的房间，每个插座有一个编号，有的插座提供220伏交流电， 有的提供110伏交流电，有的则提供有线电视节目。 客户软件将插头插到不同编号的插座，就可以得到不同的服务。

 socket

现象解释

socket非常类似于电话插座。以一个国家级电话网为例，电话的通话双方相当于相互通信的2个进程，区号是它的网络地址；区内一个单位的交换机相当于一台主机，主机分配给每个用户的局内号码相当于socket号。任何用户在通话之前，首先要占有一部电话机，相当于申请一个socket；同时要知道对方的号码，相当于对方有一个固定的socket。然后向对方拨号呼叫，相当于发出连接请求 (假如对方不在同一区内，还要拨对方区号，相当于给出网络地址) 。假如对方在场并空闲 (相当于通信的另一主机开机且可以接受连接请求) ，拿起电话话筒，双方就可以正式通话，相当于连接成功。双方通话的过程，是一方向电话机发出信号和对方从电话机接收信号的过程，相当于向socket发送数据和从socket接收数据。通话结束后，一方挂起电话机相当于关闭socket，撤消连接。
  
电话系统

在电话系统中，一般用户只能感受到本地电话机和对方电话号码的存在，建立通话的过程，话音传输的过程以及整个电话系统的技术细节对他都是透明的，这也与socket机制非常相似。socket利用网间网通信设施实现进程通信，但它对通信设施的细节毫不关心，只要通信设施能提供足够的通信能力，它就满足了。
  
至此，我们对socket进行了直观的描述。抽象出来，socket实质上提供了进程通信的端点。进程通信之前，双方首先必须各自创建一个端点，否则是没有办法建立联系并相互通信的。正如打电话之前，双方必须各自拥有一台电话机一样。在网间网内部，每一个socket用一个半相关描述:
  
 (协议，本地地址，本地端口)
  
一个完整的socket有一个本地唯一的socket号，由操作系统分配。
  
最重要的是，socket 是面向客户/服务器模型而设计的，针对客户和服务器程序提供不同的socket系统调用。客户随机申请一个socket  (相当于一个想打电话的人可以在任何一台入网电话上拨号呼叫) ，系统为之分配一个socket号；服务器拥有全局公认的 socket ，任何客户都可以向它发出连接请求和信息请求 (相当于一个被呼叫的电话拥有一个呼叫方知道的电话号码) 。
  
socket利用客户/服务器模式巧妙地解决了进程之间建立通信连接的问题。服务器socket 半相关为全局所公认非常重要。读者不妨考虑一下，两个完全随机的用户进程之间如何建立通信？假如通信双方没有任何一方的socket 固定，就好比打电话的双方彼此不知道对方的电话号码，要通话是不可能的。
  
什么是socket

所谓socket通常也称作" socket "，应用程序通常通过" socket "向网络发出请求或者应答网络请求。以J2SDK-1.3为例，Socket和ServerSocket类库位于java .net包中。ServerSocket用于服务器端，Socket是建立网络连接时使用的。在连接成功时，应用程序两端都会产生一个Socket实例，操作这个实例，完成所需的会话。对于一个网络连接来说， socket 是平等的，并没有差别，不因为在服务器端或在客户端而产生不同级别。不管是Socket还是ServerSocket它们的工作都是通过SocketImpl类及其子类完成的。
  
重要的Socket API

重要的SocketAPI: java .net.Socket继承于java.lang.Object，有八个构造器，其方法并不多，下面介绍使用最频繁的三个方法，其它方法大家可以见JDK-1.3文档。
  
Accept方法用于产生"阻塞"，直到接受到一个连接，并且返回一个客户端的Socket对象实例。"阻塞"是一个术语，它使程序运行暂时"停留"在这个地方，直到一个会话产生，然后程序继续；通常"阻塞"是由循环产生的。
  
getInputStream方法获得网络连接输入，同时返回一个InputStream对象实例。
  
getOutputStream方法连接的另一端将得到输入，同时返回一个OutputStream对象实例。注意: 其中getInputStream和getOutputStream方法均可能会产生一个IOException，它必须被捕获，因为它们返回的流对象，通常都会被另一个流对象使用。
  
### SOCKET连接过程

根据连接启动的方式以及本地 socket 要连接的目标， socket 之间的连接过程可以分为三个步骤: 服务器监听，客户端请求，连接确认。
  
服务器监听: 是服务器端 socket 并不定位具体的客户端 socket ，而是处于等待连接的状态，实时监控网络状态。
  
客户端请求: 是指由客户端的 socket 提出连接请求，要连接的目标是服务器端的 socket 。为此，客户端的 socket 必须首先描述它要连接的服务器的 socket ，指出服务器端 socket 的地址和端口号，然后就向服务器端 socket 提出连接请求。
  
连接确认: 是指当服务器端 socket 监听到或者说接收到客户端 socket 的连接请求，它就响应客户端 socket 的请求，建立一个新的线程，把服务器端 socket 的描述发给客户端，一旦客户端确认了此描述，连接就建立好了。而服务器端 socket 继续处于监听状态，继续接收其他客户端 socket 的连接请求。

当客户端调用connect时，触发了连接请求，向服务器发送了SYN J包，这时connect进入阻塞状态；服务器监听到连接请求，即收到SYN J包，调用accept函数接收请求向客户端发送SYN K ，ACK J+1，这时accept进入阻塞状态；客户端收到服务器的SYN K ，ACK J+1之后，这时connect返回，并对SYN K进行确认；服务器收到ACK K+1时，accept返回，至此三次握手完毕，连接建立。
  
[http://www.cnblogs.com/skynet/archive/2010/12/12/1903949.html](http://www.cnblogs.com/skynet/archive/2010/12/12/1903949.html)

### 四元组

       源IP地址、目的IP地址、源端口、目的端口

## 五元组是

      源IP地址、目的IP地址、协议号、源端口、目的端口

## 七元组是

       源IP地址、目的IP地址、协议号、源端口、目的端口，服务类型, 接口索引

协议号:IP是网络层协议，IP头中的协议号用来说明IP报文中承载的是哪种协议,协议号标识上层是什么协议 (一般是传输层协议，比如6 TCP，17 UDP；但也可能是网络层协议，比如1 ICMP；也可能是应用层协议，比如89 OSPF）。
TCP/UDP是传输层协议，TCP/UDP的端口号用来说明是哪种上层应用，比如TCP 80代表WWW，TCP 23代表Telnet，UDP 69代表TFTP。
目的主机收到IP包后，根据IP协议号确定送给哪个模块 (TCP/UDP/ICMP...）处理，送给TCP/UDP模块的报文根据端口号确定送给哪个应用程序处理。
>[https://www.coonote.com/tcpip-note/tcp-quadruple-quintuple.html](https://www.coonote.com/tcpip-note/tcp-quadruple-quintuple.html)

### SO_REUSEADDR 地址复用

1、一般来说，一个端口释放后会等待两分钟之后才能再被使用，SO_REUSEADDR 是让端口释放后立即就可以被再次使用。

SO_REUSEADDR用于对TCP套接字处于TIME_WAIT状态下的socket，才可以重复绑定使用。server程序总是应该在调用bind()之前设置SO_REUSEADDR套接字选项。TCP，先调用 close() 的一方会进入TIME_WAIT状态

2、SO_REUSEADDR和SO_REUSEPORT

SO_REUSEADDR提供如下四个功能：

    SO_REUSEADDR允许启动一个监听服务器并捆绑其众所周知端口，即使以前建立的将此端口用做他们的本地端口的连接仍存在。这通常是重启监听服务器时出现，若不设置此选项，则bind时将出错。

    SO_REUSEADDR允许在同一端口上启动同一服务器的多个实例，只要每个实例捆绑一个不同的本地IP地址即可。对于TCP，我们根本不可能启动捆绑相同IP地址和相同端口号的多个服务器。

    SO_REUSEADDR允许单个进程捆绑同一端口到多个套接口上，只要每个捆绑指定不同的本地IP地址即可。这一般不用于TCP服务器。

    SO_REUSEADDR允许完全重复的捆绑：当一个IP地址和端口绑定到某个套接口上时，还允许此IP地址和端口捆绑到另一个套接口上。一般来说，这个特性仅在支持多播的系统上才有，而且只对UDP套接口而言 (TCP不支持多播）。

SO_REUSEPORT选项有如下语义：

    此选项允许完全重复捆绑，但仅在想捆绑相同IP地址和端口的套接口都指定了此套接口选项才行。

    如果被捆绑的IP地址是一个多播地址，则SO_REUSEADDR和SO_REUSEPORT等效。

使用这两个套接口选项的建议：

    在所有TCP服务器中，在调用bind之前设置SO_REUSEADDR套接口选项；

当编写一个同一时刻在同一主机上可运行多次的多播应用程序时，设置SO_REUSEADDR选项，并将本组的多播地址作为本地IP地址捆绑。

    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR,

   (const void *)&nOptval , sizeof(int)) < 0) ...

附

    Q:编写 TCP/SOCK_STREAM 服务程序时，SO_REUSEADDR到底什么意思？

    A:这个套接字选项通知内核，如果端口忙，但TCP状态位于 TIME_WAIT ，可以重用端口。如果端口忙，而TCP状态位于其他状态，重用端口时依旧得到一个错误信息，指明"地址已经使用中"。如果你的服务程序停止后想立即重启，而新套接字依旧使用同一端口，此时SO_REUSEADDR 选项非常有用。必须意识到，此时任何非期望数据到达，都可能导致服务程序反应混乱，不过这只是一种可能，事实上很不可能。

    一个套接字由相关五元组构成，协议、本地地址、本地端口、远程地址、远程端口。SO_REUSEADDR 仅仅表示可以重用本地本地地址、本地端口，整个相关五元组还是唯一确定的。所以，重启后的服务程序有可能收到非期望数据。必须慎重使用 SO_REUSEADDR 选项。【2】

【1】 [http://topic.csdn.net/u/20090103/16/a0414edb-b289-4c72-84da-39e155e8f4be.html](http://topic.csdn.net/u/20090103/16/a0414edb-b289-4c72-84da-39e155e8f4be.html)

【2】

以下博客对这个问题进行了对答式的解答：

[http://blog.sina.com.cn/s/blog_53a2ecbf010095db.html](http://blog.sina.com.cn/s/blog_53a2ecbf010095db.html)

【3】 [http://www.sudu.cn/info/html/edu/20050101/296180.html](http://www.sudu.cn/info/html/edu/20050101/296180.html)

同一个机器上一个端口PORT1，TCP socket1 绑定PORT1，然后UDP socket2绑定PORT1会成功；
同一个ip, 同一个端口可以跑不同的协议 tcp, udp

>[https://www.cnblogs.com/mydomain/archive/2011/08/23/2150567.html](https://www.cnblogs.com/mydomain/archive/2011/08/23/2150567.html)
>[https://www.jianshu.com/p/711be2f1ec6a](https://www.jianshu.com/p/711be2f1ec6a)
