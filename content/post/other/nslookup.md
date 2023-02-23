---
title: nslookup
author: "-"
date: 2013-05-12T03:22:59+00:00
url: nslookup
categories:
  - Linux
tags:
  - reprint
---
## nslookup

nslookup: name server lookup

nslookup命令用于查询DNS记录，查看域名解析是否正常

nslookup 有两种模式: 交互 & 非交互，进入交互模式在命令行界面直接输入nslookup按回车，非交互模式则是后面跟上查询的域名或者IP地址按回车。一般来说，非交互模式适用于简单的单次查询，若需要多次查询，则交互模式更加适合，从根服务器进行迭代查询。

RR (Resource Records)————资源记录（RR）是包含了下列字段的4元组：
(Name, Value, Type, TTL)

主机记录（A记录）：RFC 1035 定义，A记录是用于名称解析的重要记录，提供标准的主机名到IP的地址映射。
别名记录（CNAME记录）：RFC 1035 定义，向查询的主机提供主机名对应的规范主机名。
域名服务器记录（NS记录）：用来指定该域名由哪个DNS服务器来进行解析。您注册域名时，总有默认的DNS服务器，每个注册的域名都是由一个DNS域名服务器来进行解析的，DNS服务器NS记录地址一般以以下的形式出现：ns1.domain.com、ns2.domain.com等。简单的说，NS记录返回域中主机IP地址的权威DNS服务器的主机名。
邮件交换记录（MX记录）：返回别名为Name对应的邮件服务器的规范主机名。

<https://www.cnblogs.com/even160941/p/14292059.html>

```bash
# nslookup –option1 –option2 host-to-find dns-server
nslookup redis.wiloon.com 192.168.50.1
```

2.格式

nslookup [IP地址/域名]

3.应用实例

(1)在本地计算机上使用nslookup命令

$ nslookup

Default Server: name.cao.com.cn

Address: 192.168.1.9

在符号">"后面输入要查询的IP地址域名，并回车即可。如果要退出该命令，输入"exit"，并回车即可。

(2)使用nslookup命令测试named

输入下面命令:

nslookup

然后就进入交换式nslookup环境。如果named正常启动，则nslookup会显示当前DNS服务器的地址和域名，否则表示named没能正常启动。

下面简单介绍一些基本的DNS诊断。

◆检查正向DNS解析，在nslookup提示符下输入带域名的主机名，如hp712.my.com，nslookup应能显示该主机名对应的IP地址。如

果只输入hp712，nslookup会根据/etc/resolv.conf的定义，自动添加my.com域名，并回答对应的IP地址。

◆检查反向DNS解析，在nslookup提示符下输入某个IP地址，如192.22.33.20，nslookup应能回答该IP地址所对应的主机名。

◆检查MX邮件地址记录在nslookup提示符下输入:

set q=mx

然后输入某个域名，输入my.com和mail.my.com，nslookup应能够回答对应的邮件服务器地址，即support.my.com和support2.my.com。

动手练习

1.危险的网络命令

互联网的发展使安全成为一个不能忽视的问题，finger、ftp、rcp和telnet在本质上都是不安全的，因为它们在网络上用明文传送口令和数据，嗅探器可以非常容易地截获这些口令和数据。而且，这些服务程序的安全验证方式也是有弱点的，很容易受到"中间服务器"方式的攻击。这里笔者把一些不安全的命令根据危险等级列出，见表3所示。现在ftp、telnet可以被SSH命令代替绑定在端口22上，其连接采用协商方式，使用RSA加密。身份鉴别完成之后，后面的所有流量都使用IDEA进行加密。SSH(SecureShell)程序可以通过网络登录到远程主机，并执行命令。rcp、rlogin等远程调用命令也逐渐被VNC软件代替。

2.在一张网卡上绑定多个IP地址

在Linux下，可以使用ifconfig方便地绑定多个IP地址到一张网卡。例如，eth0接口的原有IP地址为192.168.0 .254，可以执行下面命令:

ifconfig eth0:0 192.168.0.253 netmask 255.255.255.0

ifconfig eth0:1 192.168.0.252 netmask 255.255.255.0

......

3.修改网卡MAC地址

首先必须关闭网卡设备，命令如下:

/sbin/ifconfig eth0 down

修改MAC地址，命令如下:

/sbin/ifconfig eth0 hw ether 00:AA:BB:CC:DD:EE

重新启用网卡:

/sbin/ifconfig eht0 up

这样网卡的MAC地址就更改完成了。每张网卡的MAC地址是惟一，但不是不能修改的，只要保证在网络中的MAC地址的惟一性就可以了。

4.初步部署IPv6

IPv4

技术在网络发展中起到了巨大的作用，不过随着时间的流逝它无论在网络地址的提供、服务质量、安全性等方面都越来越力不从心，IPv6呼之欲出。Linux是所有操作系统中最先支持IPv6的，一般Linux基于2.4内核的Linux发行版本都可以直接使用IPv6，不过主要发行版本没有加载IPv6模块，可以使用命令手工加载，需要超级用户的权限。

(1)加载IPv6模块

使用命令检测，其中inet6 addr: fe80::5054:abff:fe34:5b09/64，就是eth0网卡的IPv6地址。

modprobe IPv6

ifconfig

eth0 Link encap:Ethernet HWaddr 52:54:AB:34:5B:09

inet addr:192.168.1.2 Bcast:192.168.1.255 Mask:255.255.255.0

inet6 addr: fe80::5054:abff:fe34:5b09/64 Scope:Link

UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1

RX packets:0 errors:0 dropped:0 overruns:0 frame:0

TX packets:21 errors:0 dropped:0 overruns:0 carrier:0

collisions:0 txqueuelen:100

RX bytes:0 (0.0 b) TX bytes:1360 (1.3 Kb)

Interrupt:5 Base address:0xec00

(2)使用ping命令检测网卡的IPv6地址是否有效

ping6 -I eth0 -c 2 fe80::200:e8ff:fea0:2586

和IPv4不一样，使用ping6命令时必须指定一个网卡界面，否则系统不知道将数据包发送到哪个网络设备。I表示Interface、eth0是第一个网卡，-c表示回路，2表示ping6操作两次。

(3)使用ip命令在IPv6下为eth0增加一个IP地址

ip -6 addr add 3ffe:ffff:0:f101::1/64 dev eth0

使用ifconfig命令，查看网卡是否出现第二个IPv6地址。

Linux网络的主要优点是能够实现资源和信息的共享，并且用户可以远程访问信息。Linux提供了一组强有力的网络命令来为用户服务，这些工具能够帮助用户进行网络设定、检查网络状况、登录到远程计算机上、传输文件和执行远程命令等。上面介绍了Linux中比较重要的网络命令，其实Linux还有许多命令需要学习。Linux网络操作命令的一个特点就是命令参数选项很多，并不要求全部记住，关键在于理解命令的主要用途和学会使用帮助信息
