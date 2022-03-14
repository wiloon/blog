---
title: tunctl
author: "-"
date: 2012-03-25T05:55:58+00:00
url: /?p=2620
categories:
  - Linux
  - Network

tags:
  - reprint
---
## tunctl
tunctl is used to set up and maintain persistent TUN/TAP network interfaces, enabling user applications to simulate network traffic. Such interfaces is useful for VPN software, virtualization, emulation, simulation, and a number of other applications.

**-t** _interface _Specifies the desired interface name.


**-b **Brief output, prints just the interface name

**-d** _interfacename _Delete the specified interfacename (set it to non-persistent)

**-t** _interface _Specifies the desired interface name.

**-u** _user _Specifies the owner of the interface. This user is allowed to attach to the "network/wire" side.

tun/tap 驱动程序实现了虚拟网卡的功能，tun表示虚拟的是点对点设备，tap表示虚拟的是以太网设备，这两种设备针对网络包实施不同的封装。
  
利用tun/tap 驱动，可以将tcp/ip协议栈处理好的网络分包传给任何一个使用tun/tap驱动的进程，由进程重新处理后再发到物理链路中。
  
开源项目openvpn  ( [http://openvpn.sourceforge.net][1]) 和Vtun( [http://vtun.sourceforge.net][2])都是利用tun/tap驱动实现的隧道封装。

安装uml-utilities和bridge-utils和,这两个工具分别含有_tunctl_和brctl命令

 [1]: http://openvpn.sourceforge.net/
 [2]: http://vtun.sourceforge.net/