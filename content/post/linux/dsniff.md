---
title: Dsniff
author: "-"
date: 2012-01-08T05:31:08+00:00
url: dsniff
categories:
  - Linux
  - Network
tags:
  - reprint
---
## Dsniff

Dsniff是一个著名的网络嗅探工具包。其开发者Dug Song早在1999年12月，以密歇根大学CITI研究室 (Center for Information Technology Integration) 的研究成果为基础，开发了这个后来具有很大影响力的网络安全工具包。Dug Song开发Dsniff的本意是揭示网络通信的不安全性，借助这个工具包，网络管理员可以对自己的网络进行审计，也包括渗透测试。但万事总有其两面 性，Dsniff所带来的负面作用也是"巨大"的，首先它是可以自由获取的，任何拥有这个工具包的人都可能做"非正当"的事，其次，Dsniff里面的某 些工具，充分揭示了一些安全协议的"不安全性"，例如针对SSH1和SSL的MITM (Man-In-The-Middle) 攻击工具—SSHmitm和 Webmitm。SSH1和SSL都是建立网络通信加密通道的机制，向来被认为是很安全的，但人们在具体使用时，往往因为方便性上的考虑而忽视了某些环 节，造成实事上的不安全。所以说，最大的不安全性，往往并不在于对安全的一无所知，而在于过于相信自己的安全。

Dub Song在2000年12月发布了Dsniff的v2.3版本，该版本支持OpenBSD、Linux、Solaris系统平台。目前，最新版本是 2001年3月发布的v2.4b1的Beta版
  
除了针对Unix系统的版本，从网上也可以得到Windows平台上运行的Dsniff早期版

作为一个工具集，dsniff包括的工具分为四类:

* 纯粹被动地进行网络活动监视的工具，包括: dsniff、filesnarf、mailsnarf 、msgsnarf、urlsnarf、webspy
* 针对SSH和SSL的MITM (Man-In-The-Middle) "攻击"工具，包括sshmitm和webmitm
* 发起主动欺骗的工具，包括: arpspoof、dnsspoof、macof
* 其它工具，包括tcpkill、tcpnice

### dsniff的安装

    sudo pacman -S dsniff

安装完成后，默认dsniff的安装目录是/usr/local/sbin，在这里可以看到dsniff所有的工具

![][1]

### dsniff工具介绍

* 纯粹被动地进行网络活动监视的工具，包括: dsniff、filesnarf、mailsnarf 、msgsnarf、urlsnarf、webspy
* 针对SSH和SSL的MITM (Man-In-The-Middle) "攻击"工具，包括sshmitm和webmitm
* 发起主动欺骗的工具，包括: arpspoof、dnsspoof、macof
* 其它工具，包括tcpkill、tcpnice

#### dsniff

dsniff 是一个密码侦测工具，他能够自动分析端口上收到的某些协议的数据包，并获取相应的密码。 dnisff 支持的协议有 FTP, Telnet, SMTP, HTTP, POP, poppass, NNTP, IMAP, SNMP, LDAP, Rlogin, RIP, OSPF, PPTP MS-CHAP, NFS, VRRP, YP/NIS, SOCKS, X11, CVS, IRC, AIM, ICQ, Napster, PostgreSQL, Meeting Maker, Citrix ICA, Symantec pcAnywhere, NAI Sniffer, Microsoft SMB, Oracle SQL*Net, Sybase and Microsoft SQL。

> **dsniff** [**-c**] [**-d**] [**-m**] [**-n**] [**-i **_interface_] [**-s **_snaplen_] [**-f **_services_] [**-t **_trigger[,...]_]] [**-r**|**-w** _savefile_] [_expression_]     **注意**: 这里所有的expression都是代表TCPDUMP的表达式，指定对哪些数据包进行攻击

#### filesnarf

**filesnarf**可以嗅探网络文件系统 (NFS) 的流量，并选定某个文件，转储到本地当前工作目录

**filesnarf**[**-i** _interface_] [[**-v**] _pattern _[_expression_]]

#### mailsnarf

**mailsnarf**可以嗅探SMTP和POP流量，并以Berkeley邮件格式输出e-mail消息

**mailsnarf**[**-i** _interface_] [[**-v**] _pattern _[_expression_]]

嗅探发送的SMTP流量:

嗅探接收的POP流量:

#### msgsnarf

**msgsnarf**可以嗅探聊天软件的聊天内容，包括AOL,ICQ 2000, IRC, MSN Messenger, 或Yahoo Messenger

**msgsnarf**[**-i** _interface_] [[**-v**] _pattern _[_expression_]]

#### urlsnarf

**urlsnarf**可以嗅探HTTP请求报文的内容，并以CLF (Common Log Format) 通用日志格式输出

**urlsnarf**[**-n**] [**-i** _interface_] [[**-v**] _pattern _[_expression_]]

#### webspy

webspy指定一个要嗅探的主机，如果指定主机发送HTTP请求，打开网页，webspy也会通过netscape浏览器在本地打开一个相同的网 页

**webspy**[**-i** _interface_] _host_host 指定要嗅探的主机

#### sshmitm

sshmitm 是Dsniff自带的一个具有威胁的工具之一。首先通过dnsspoof伪造实际机器主机名将攻 击目标主机的SSH连接转到本地，那么sshmitm可以截获来自主机的密钥，并获得被劫持连接中的所有信息解码，然后重新转发SSH流量到SSH服务 器。

sshmitm可以对某个SSH会话发动MITM (Monkey-In-The-Middle) 攻击 (注意，这里的Monkey是Dsniff包 readme文件中的解析，而不是常见的Man，这种区别实际上是没有"区别"，也许就是因为Dsniff以猴子做为其标志的原因吧) 。通过 sshmitm，攻击者可以捕获某个SSH会话的登录口令，甚至可以"劫持"整个会话过程 (攻击者在其主机上通过OpenSSL提供的代码生成伪造的证 书，以欺骗目标主机，使之相信就是有效的通信另一方，结果是，攻击者主机成了SSH安全通道的中转站) 。目前，对于SSH1，这种MITM攻击已经构成了 严重的威胁。MITM并不是一个新的概念，它是一种对认证及密钥交换协议进行攻击的有效手段。通常，在SSH会话中，服务器首先会给客户端发送其公钥，严 格来说，这种密钥的交换和管理应该是基于X.509这种公钥基础设施 (PKI) 的，但因为PKI本身的复杂性导致真正应用了这种公钥管理机制的服务器非常 少，所以，通常情况下，服务器只是简单的自己生成密钥对，并将其中的公钥发送给客户端。客户端收到服务器的公钥后，必须独立验证其有效性。通常，使用 SSH的客户端会由sysadmin或其它账号来维护一个"密钥/主机名"的本地数据库，当首次与某个SSH服务器建立连接时，客户端可能被事先配制成自 动接受并记录服务器公钥到本地数据库中，这就导致可能发生MITM攻击。其实，建立加密的安全网络都存在一个基本的问题，无论如何，某种程度上讲，加密通 道的初始化连接总是建立在一个存在潜在危险的网络之上的，如果密钥交换机制并不健全，或者是根本就被忽略了，那之后建立起来的加密通道也形同虚设了。按道 理讲，SSH之类的协议本身是没有问题的，只要严格按照标准来建立加密及密钥交换管理机制 (例如PKI) ，攻击者是根本不会有可乘之机的，可问题就在于， 许多时候，为了使用上的方便，"复杂"的保证技术就被人们抛之脑后了。当然，一种协议如果其可用性并不很强，也许本身就是问题，现在，SSH2较SSH1 已经有了较大改进。具体来说，在某个SSH连接建立之初，如果客户端收到一个未知的服务器端公钥，OpenSSH会有下列配置处理方式:

1. 自动增加该公钥到本地数据库；
2. 发出下面列出的警告消息，并询问用户是添加该公钥还是放弃连接；
  
------------------------

- WARNING: HOST IDENTIFICATION HAS CHANGED! -

------------------------

IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!

Someone could be eavesdropping on you right now (man-in-the-middle attack)! It is also possible that the host-key has just been changed. Please contact your system administrator.

1. 拒绝接受。如果客户端对未知公钥的验证被取消了 (或者客户端配置本身已经旁路掉了这个过程) ，或者如果客户端保存已知主机CA证书的缓存 被"毒害"了，就很有可能导致攻击者发起MITM攻击。从根本上讲，要防止MITM方式的攻击，用户自身加强安全措施才是关键，例如，密钥的初始交换也许 可以换做其它方式 (比如软盘) ，严格管理本地的证书列表数据库，对于出现的告警提示，应该仔细甄别，防止第三方的欺骗行为。

> **sshmitm**[**-d**] [**-I**] [**-p** _port_] _host_[_port_]

> 注意: 这里的-P后面指定的是sshmitm本地使用的端口，也就是攻击目标主机用来连接SSH服务器的端口，而后面的port则是我转发SSH流 量到SSH服务器使用的端口，此外如果是用了参数-I，就可以在攻击目标主机连接到SSH服务器后，查看他们之间的交互内容。

> 首先通过dnsspoof进行对攻击目标进行dns欺骗:

> ![][6]

> 接着便可以进行sshmitm嗅探:  (由于使用了-I，所以，SSH连接后的交互内容也显示 了出来)

> ![][7]

#### webmitm

**webmitm**与sshmitm类似，也需要dnsspoof的"配合"，不同的是，webmitm"劫持"的 是HTTP和HTTPS会话过程，捕获SSL的加密通信。

> **webmitm**[**-d**]

#### arpspoof

**arpspoof**启用arp欺骗，将自己网卡的IP地址伪装成指定IP地址的MAC

持续不断的发送假的ARP响应包给一台或多台主机，以"毒害"其ARP缓存表。一旦成功，即可以用别的嗅探工具来"接收"发送到本地的数据包。与 Ettercap不同的是，arpspoof并不进行真正的"嗅探"，它只是简单的进行ARP欺骗，本地主
  
机必须启动内核的IP Forwarding功能 (或者使用fragrouter这样的工具) ，否则，所有"转向"发到本地的数据包就如同进了黑洞，正常的网络通信将无法进行， 而一旦启动了本地的IP Forwarding，内核将自动对本地收到的目的IP却是别处的数据包进行转发，正常的通信自然可以进行。这样，就可以进行后续的许多工作，包括分析嗅 探得到的数据包、修改数据包中的某些信息以重新转发等等。

> 在Linux中，缺省是禁止IP Forwarding的，可以使用简单的命令启动它:

> 修改#vi /etc/sysctl.conf:
  
net.ipv4.ip_forward = 1

> 修改后运行#sysctl –p命令使得内核改变立即生效；

一旦启动了本地的IP Forwarding，内核将自动对本地收到的目的IP却是别处的数据包进行转发， (同时向数据包的源地址发送ICMP重定向报文，当然，由于启用了ARP欺骗，这个重定向报文是不起作用的) 。 这里第17个数据包的源地址已经从本来的源MAC地址改变为本地MAC地址了。说明数据包是本地转发出去的。

![][8]

> **arpspoof**[**-i** _interface_] [**-t** _target_] _host_如 果不指定tagget则向网络中所有的主机发送欺骗

> ![][9]

#### dnsspoof

dnsspoof启用DNS欺骗，如果dnsspoof嗅探到局域网内有DNS请求数据包，它会分析其内容，并用伪造的DNS响应包来回复请求者。 如果是请求解析某个域名，dnsspoof会让该域名重新指向另一个IP地址 (黑客所控制的主机) ，如果是反向IP指针解析，dnsspoof也会返回一 个伪造的域名。

> **dnsspoof**[**-i** _interface_] [**-f** _hostsfile_] [_expression_]   这里-f 可以指定主机列表文件，文件格式与/usr/local/lib/dnsspoof.hosts相同，如果不指定该文件，dnsspoof会返回本地的 IP给域名解析请求者

> ![][10]

> 这里本地主机会抢先代替DNS服务器来相应查询，前提是本地主机先回答DNS查询，如果因为 网络问题，DNS服务器先发送了应答，DNS欺骗就不能生效了

> <img src="http://hiphotos.baidu.com/sdusoul/pic/item/0ef41bd5dacdb4f851da4bbb.jpg" alt="" width="655" height="85" />

#### macof

**macof**用来进行MAC flooding，可以用来使交换机的MAC表溢出，对于以后收到的数据包以广播方式发送。注意: 在进行MAC泛洪之前就存在于交换机MAC表中的条目不会被覆盖，只能等到这些条目自然老化

> **macof**[**-i** _interface_] [**-s** _src_] [**-d** _dst_] [**-e** _tha_] [**-x** _sport_] [**-y** _dport_] [**-n** _times_]

> ![][11]

#### tcpkill

tcpkill能够切断指定的TCP会话连接，主要是基于TCP的三次握手过程

> **tcpkill**[**-i** _interface_] [**-1...9**] _expression_

> ![][12]

> ![][13]

> 这里，当tcpkill检测到两边的TCP连接后，会同时想两边 (冒充对方) 发送tcp reset报文，重置连接。

#### tcpnice

tcpnice能够通过在添加活动的流量，降低指定的LAN上的TCP连接的速度

> **tcpnice**[**-I**] [**-i** _interface_] [**-n** _increment_] _expression_这里的-n后面可以跟1-20，代表降低的速度，1为原速，20为最低

> _![][14]_

 [1]: http://hiphotos.baidu.com/sdusoul/pic/item/4134970a67ed4c2395ca6bbb.jpg
 [2]: http://hiphotos.baidu.com/sdusoul/pic/item/304e251fcc69b8f4a78669bb.jpg
 [3]: http://hiphotos.baidu.com/sdusoul/pic/item/7f3e6709969e19f33bc763bb.jpg
 [4]: http://hiphotos.baidu.com/sdusoul/pic/item/3bc79f3d9b7fb83cbaa167bb.jpg
 [5]: http://hiphotos.baidu.com/sdusoul/pic/item/f8dcd100df02a42d728b65bb.jpg
 [6]: http://hiphotos.baidu.com/sdusoul/pic/item/728b4710d0b1a1c0c3ce79bb.jpg
 [7]: http://hiphotos.baidu.com/sdusoul/pic/item/b912c8fca86daac1fc037fbb.jpg
 [8]: http://hiphotos.baidu.com/sdusoul/pic/item/fc039245b92bbd03879473bb.jpg
 [9]: http://hiphotos.baidu.com/sdusoul/pic/item/d688d43ff637cdfe7d1e71bb.jpg
 [10]: http://hiphotos.baidu.com/sdusoul/pic/item/7d1ed21b7b5772e9ad6e75bb.jpg
 [11]: http://hiphotos.baidu.com/sdusoul/pic/item/51da81cb4278dfc152664fbb.jpg
 [12]: http://hiphotos.baidu.com/sdusoul/pic/item/39dbb6fd2fc5b92a09244dbb.jpg
 [13]: http://hiphotos.baidu.com/sdusoul/pic/item/5266d0167687c224972b43bb.jpg
 [14]: http://hiphotos.baidu.com/sdusoul/pic/item/972bd407b6598ff17b8947bb.jpg
