---
title: TUN, TAP
author: "-"
date: 2011-12-04T13:41:39+00:00
url: tun-tap
categories:
  - network

tags:
  - reprint
---
## TUN, TAP

在计算机网络中，TUN与TAP是操作系统内核中的虚拟网络设备。不同于普通靠物理设备/硬件网卡实现的设备，这些虚拟的网络设备全部用软件实现，并向运行于操作系统上的软件提供与硬件的网络设备完全相同的功能。

操作系统通过TUN/TAP设备向绑定该设备的用户空间的程序发送数据，反之，用户空间的程序也可以像操作硬件网络设备那样，通过TUN/TAP设备发送数据。在后种情况下，TUN/TAP设备向操作系统的网络栈投递 (或"注入") 数据包，从而模拟从外部接受数据的过程。

TUN/TAP虚拟网络设备为用户空间程序提供了网络数据包的发送和接收能力。他既可以当做点对点设备 (TUN) ，也可以当做以太网设备 (TAP) 。实际上，不仅Linux支持TUN/TAP虚拟网络设备，其他UNIX也是支持的，他们之间只有少许差别。

TUN/TAP 虚拟网络设备的原理比较简单，他在Linux内核中添加了一个TUN/TAP虚拟网络设备的驱动程序和一个与之相关连的字符设备  
/dev/net/tun，字符设备tun作为用户空间和内核空间交换数据的接口。当内核将数据包发送到虚拟网络设备时，数据包被保存在设备相关的一个队列中，直到用户空间程序通过打开的字符设备tun的描述符读取时，它才会被拷贝到用户空间的缓冲区中，其效果就相当于，数据包直接发送到了用户空间。通过系统调用write发送数据包时其原理与此类似。

值得注意的是: 一次read系统调用，有且只有一个数据包被传送到用户空间，并且当用户空间的缓冲区比较小时，数据包将被截断，剩余部分将永久地消失，write系统调用与read类似，每次只发送一个数据包。所以在编写此类程序的时候，请用足够大的缓冲区，直接调用系统调用read/write，避免采用C语言的带缓存的IO函数。

tap/tun 是 Linux 内核 2.4.x 版本之后实现的虚拟网络设备  
Linux 内核 2.6.x 之后的版本中，tap/tun 对应的字符设备文件分别为:

    tap: /dev/tap0
    tun: /dev/net/tun

tun/tap驱动程序实现了虚拟网卡的功能

### TUN (namely network TUNnel)

tun 表示虚拟的是点对点设备  
TUN 模拟了网络层设备，操作(网络层)第三层(TCP/IP四层协议) 数据包比如IP数据封包。
TUN 模拟的是一个三层设备,也就是说,通过它可以处理来自网络层的数据，更通俗一点的说，通过它，我们可以处理 IP 数据包。

### TAP (namely network tap), Terminal Access Point
TAP设备
tap表示虚拟的是以太网设备 , TAP 等同于一个以太网设备，它操作第二层数据包如以太网数据帧。 
TAP 设备与 TUN 设备工作方式完全相同，区别在于: 

- TUN 设备是一个三层设备，它只模拟到了 IP 层，即网络层, 我们可以通过 /dev/tunX 文件收发 IP 层数据包，它无法与物理网卡做 bridge，但是可以通过三层交换 (如 ip_forward) 与物理网卡连通。可以使用ifconfig之类的命令给该设备设定 IP 地址。
- TAP 设备是一个二层设备，它比 TUN 更加深入，通过 /dev/tapX 文件可以收发 MAC 层数据包，即数据链路层，拥有 MAC 层功能，可以与物理网卡做 bridge，支持 MAC 层广播。同样的，我们也可以通过ifconfig之类的命令给该设备设定 IP 地址，你如果愿意，我们可以给它设定 MAC 地址。

### openvpn
在安装openvpn时，第一步就是要确认tun/tap是否开通

Tun/tap驱动是个虚拟网卡开源项目，支持非常多的类UNIX平台，OpenVPN和Vtun都是基于他实现隧道包封装。我们介绍tun/tap驱动的主要功能和作用。要装openvpn的最好了解一下: 

tun/tap 驱动程式实现了虚拟网卡的功能，tun表示虚拟的是点对点设备，tap表示虚拟的是以太网设备，这两种设备针对网络包实施不同的封装。利用tun/tap 驱动，能将tcp/ip协议栈处理好的网络分包传给所有一个使用tun/tap驱动的进程，由进程重新处理后再发到物理链路中。开源项目openvpn  ( http://openvpn.sourceforge.net) 和Vtun( http://vtun.sourceforge.net)都是利用tun/tap驱动实现的隧道封装。

做为虚拟网卡驱动，Tun/tap驱动程序的数据接收和发送并不直接和真实网卡打交道，而是通过用户态来转交。在linux下，要实现核心态和用户态数据的交互，有多种方式: 可以通用socket创建特殊 socket ，利用 socket 实现数据交互；通过proc文件系统创建文件来进行数据交互；还可以使用设备文件的方式，访问设备文件会调用设备驱动相应的例程，设备驱动本身就是核心态和用户态的一个接口，Tun/tap驱动就是利用设备文件实现用户态和核心态的数据交互。从结构上来说，Tun/tap驱动并不单纯是实现网卡驱动，同时它还实现了字符设备驱动部分。以字符设备的方式连接用户态和核心态。

Tun/tap驱动程序中包含两个部分，一部分是字符设备驱动，还有一部分是网卡驱动部分。利用网卡驱动部分接收来自TCP/IP协议栈的网络分包并发送或者反过来将接收到的网络分包传给协议栈处理，而字符驱动部分则将网络分包在内核与用户态之间传送，模拟物理链路的数据接收和发送。Tun/tap驱动很好的实现了两种驱动的结合。

作为站长，了解一下tun/tap就可以了，如果想深入学习，最好google搜索。

http://www.usa-vps.com/vps-study-guide/%E4%BB%80%E4%B9%88%E6%98%AFtuntap.htm
  
http://zh.wikipedia.org/wiki/TUN%E4%B8%8ETAP
  
https://www.ibm.com/developerworks/cn/linux/l-tuntap/index.html
  
https://en.wikipedia.org/wiki/TUN/TAP
https://www.jianshu.com/p/09f9375b7fa7
