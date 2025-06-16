---
title: DNS
author: "-"
date: 2017-12-17T06:27:24+00:00
url: dns
categories:
  - Network
tags:
  - reprint
  - remix
---
## DNS

DNS的本质是什么？
  
Domain Name System = DNS (域名系统) 其实是一个数据库,是用于 TCP/IP 程序的分布式数据库,同时也是一种重要的网络协议。DNS储存了网络中的 IP 地址与对应主机的信息,邮件路由信息和其他网络应用方面的信息,用户通过询问解决库 (解决库发送询问并对DNS回应进行说明) 在 DNS 上查询信息。

DNS的作用是什么?
  
DNS是网络分层里的应用层协议,事实上他是为其他应用层协议工作的,简单说就是把域名,或者说主机名转化为IP地址 (同时也提供反向域名查询的功能) ,类似字典,比如访问 `www.baidu.com`, 实际访问的是它的IP地址,因为机器识别的是拥有固定格式和含义的IP地址,而域名可以千奇百怪,甚至是中文,不利于识别。还有比如公司内部的域验证,通过分配给员工的域账号登录内网就必须通过DNS来找到域名权限服务器,来认证身份,故有些书上说: DNS是因特网世界里不可缺少的东西。

比如,使用host命令进行DNS查询

host命令用来做DNS查询。如果命令参数是域名,命令会输出关联的IP；如果命令参数是IP,命令则输出关联的域名。

[http://www.cnblogs.com/kubixuesheng/p/6260195.html](http://www.cnblogs.com/kubixuesheng/p/6260195.html)

dnsmasq
  
[http://blog.wiloon.com/?p=8698&embed=true#?secret=4F3Jvk9nTk](http://blog.wiloon.com/?p=8698&embed=true#?secret=4F3Jvk9nTk)

## dns ttl

[https://jaminzhang.github.io/dns/DNS-TTL-Understanding-and-Config/](https://jaminzhang.github.io/dns/DNS-TTL-Understanding-and-Config/)

我们有配置域名时,不同情况下,不同业务下,需要增大或减小 DNS TTL 值。这是为什么呢？ 这需要我们重新理解下 DNS TTL 值的含义。

什么是域名的 TTL 值
  
TTL(Time-To-Live), 就是一条域名解析记录在 DNS 服务器中的存留时间。
  
当各地的 DNS 服务器接受到解析请求时, 就会向域名指定的 NS 服务器发出解析请求从而获得解析记录；
  
在获得这个记录之后, 记录会在 DNS 服务器中保存一段时间,这段时间内如果再接到这个域名的解析请求,
  
DNS 服务器将不再向 NS 服务器发出请求, 而是直接返回刚才获得的记录；
  
而这个记录在 DNS 服务器上保留的时间,就是 TTL 值。

DNS记录中的 ttl 决定了信息的更新频率，如果 ttl 设置为0，每个请求都会发起DNS查询，显然这会造成性能问题，但是DNS的更新、改变延迟会相对非常低

## mDNS

archlinux mDNS, systemd-resolved 支持 mDNS
```bash
# systemd-resolve 默认禁用 mDNS
# 启用 mDNS, 删除 MulticastDNS 的注释
[Resolve]
MulticastDNS=yes
```

```bash
# 重启 systemd-resolved
sudo systemctl restart systemd-resolved
```

mDNS multicast DNS , 使用5353端口。

在局域网内，你要通过一台主机和其他主机进行通信，你需要知道对方的ip地址，但是有些时候，你并不知道对方的ip地址，因为一般使用DHCP动态分配ip地址的局域网内，各个主机的IP地址是由DHCP服务器来帮你分配IP地址的。所以在很多情况下，你要知道对方的IP地址是比较麻烦的。

mDNS就是来解决这个问题的。通过一个约定俗成的端口号，5353。（这个端口号应该是由IETF组织约定的。）每个进入局域网的主机，如果开启了mDNS服务的话，都会向局域网内的所有主机组播一个消息，我是谁，和我的IP地址是多少。然后其他也有该服务的主机就会响应，也会告诉你，它是谁，它的IP地址是多少。当然，具体实现要比这个复杂点。

比如，A主机进入局域网，开启了mDNS服务，并向mDNS服务注册一下信息：我提供FTP服务，我的IP是192.168.1.101，端口是21。当B主机进入局域网，并向B主机的mDNS服务请求，我要找局域网内FTP服务器，B主机的mDNS就会去局域网内向其他的mDNS询问，并且最终告诉你，有一个IP地址为192.168.1.101，端口号是21的主机，也就是A主机提供FTP服务，所以B主机就知道了A主机的IP地址和端口号了。

大概的原理就是这样子，mDNS提供的服务要远远多于这个，当然服务多但并不复杂。

在Apple 的设备上（电脑，笔记本，iphone，ipad等设备）都提供了这个服务。很多Linux设备也提供这个服务。Windows的设备可能没有提供，但是如果安装了iTunes之类的软件的话，也提供了这个服务。

这样就可以利用这个服务开发一些局域网内的自动发现，然后提供一些局域网内交互的应用了。

https://www.cnblogs.com/leonxyzh/p/7289025.html


DNS（Domain Name System，域名系统）因特网上作为域名和IP地址相互映射的一个分布式数据库，能够使用户更方便的访问互联网，
而不用去记住能够被机器直接读取的IP数串。通过主机名，最终得到该主机名对应的IP地址的过程叫做域名解析（或主机名解析）。
DNS协议运行在UDP协议之上，使用端口号53。
在RFC文档中RFC 2181对DNS有规范说明，RFC 2136对DNS的动态更新进行说明，RFC 2308对DNS查询的反向缓存进行说明。

一、mDNS
mdns 即多播dns（Multicast DNS），mDNS主要实现了在没有传统DNS服务器的情况下使局域网内的主机实现相互发现和通信，
使用的端口为5353，遵从dns协议，使用现有的DNS信息结构、名语法和资源记录类型。并且没有指定新的操作代码或响应代码。
在局域网中，设备和设备之前相互通信需要知道对方的ip地址的，
大多数情况，设备的ip不是静态ip地址，而是通过dhcp协议动态分配的ip 地址，如何设备发现呢，就是要mdns大显身手，
例如：现在物联网设备和app之间的通信，要么app通过广播，要么通过组播，发一些特定信息，感兴趣设备应答，
实现局域网设备的发现，当然mdns 比这强大的多
1.mDNS 基于UDP 协议
组播地址: 组播地址使用的是D类地址，地址范围为：224.0.0.0—239.255.255.255
2.mdns工作原理简单描述：
mdns 使用组播地址为： 224.0.0.251 （ipv6： FF02::FB） 端口为5353，mdns是用于局域网内部的，并且主机的域名为.local 结尾,每个进入局域网的主机，如果开启了mDNS服务的话，都会向局域网内的所有主机组播一个消息，我是谁（域名），和我的IP地址是多少。然后其他有mdns服务的主机就会响应，也会告诉你，它是谁（域名），它的IP地址是多少。
当然设备需要服务时，就是使用mdns 查询域名对对应的ip地址，
对应的设备收到该报文后同样通过组播方式应答，
此时其他主机设备也是可以收到该应答报文，其他主机也会记录域名和ip 以及ttl 等，更新缓存
比如，A主机进入局域网，开启了mDNS 服务，并向mDNS服务注册以下信息：我提供 FTP 服务，我的IP是 192.168.1.101，端口是 21。当B主机进入局域网，并向 B 主机的 mDNS 服务请求，我要找局域网内 FTP 服务器，B主机的 mDNS 就会去局域网内向其他的 mDNS 询问，并且最终告诉你，有一个IP地址为 192.168.1.101，端口号是 21 的主机，也就是 A 主机提供 FTP 服务，所以 B 主机就知道了 A 主机的 IP 地址和端口号了。
大概的原理就是这样子，mDNS提供的服务要远远多于这个，当然服务多但并不复杂。
3.mDNSResponder与Bonjour的关系:
The mDNSResponder project is a component of Bonjour,
Apple's ease-of-use IP networking initiative:
Bonjour是法语中的Hello之意。它是Apple公司为基于组播域名服务(multicast DNS)的开放性零配置网络标准所起的名字。
使用Bonjour的设备在网络中自动组播它们自己的服务信息并监听其它设备的服务信息。
设备之间就像在打招呼，这也是该技术命名为Bonjour的原因。
Bonjour使得局域网中的系统和服务即使在没有网络管理员的情况下也很容易被找到。

举一个简单的例子：在局域网中，如果要进行打印服务，必须先知道打印服务器的IP地址。此IP地址一般由IT部门的人负责分配，然后他还得全员发邮件以公示此地址。有了Bonjour以后，打印服务器自己会依据零配置网络标准在局域网内部找到一个可用的IP并注册一个打印服务，名为“print service”之类的。当客户端需要打印服务时，会先搜索网络内部的打印服务器。
由于不知道打印服务器的IP地址，客户端只能根据诸如"print service"的名字去查找打印机。

在Bonjour的帮助下，客户端最终能找到这台注册了“print service”名字的打印机，并获得它的IP地址以及端口号。

https://www.cnblogs.com/Alanf/p/8653223.html
