---
title: DNS
author: "-"
date: 2017-12-17T06:27:24+00:00
url: /?p=11620
categories:
  - Inbox
tags:
  - reprint
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

# mDNS

mDNS 原理的简单理解
mDNS multicast DNS , 使用5353端口。

在局域网内，你要通过一台主机和其他主机进行通信，你需要知道对方的ip地址，但是有些时候，你并不知道对方的ip地址，因为一般使用DHCP动态分配ip地址的局域网内，各个主机的IP地址是由DHCP服务器来帮你分配IP地址的。所以在很多情况下，你要知道对方的IP地址是比较麻烦的。

mDNS就是来解决这个问题的。通过一个约定俗成的端口号，5353。（这个端口号应该是由IETF组织约定的。）每个进入局域网的主机，如果开启了mDNS服务的话，都会向局域网内的所有主机组播一个消息，我是谁，和我的IP地址是多少。然后其他也有该服务的主机就会响应，也会告诉你，它是谁，它的IP地址是多少。当然，具体实现要比这个复杂点。

比如，A主机进入局域网，开启了mDNS服务，并向mDNS服务注册一下信息：我提供FTP服务，我的IP是192.168.1.101，端口是21。当B主机进入局域网，并向B主机的mDNS服务请求，我要找局域网内FTP服务器，B主机的mDNS就会去局域网内向其他的mDNS询问，并且最终告诉你，有一个IP地址为192.168.1.101，端口号是21的主机，也就是A主机提供FTP服务，所以B主机就知道了A主机的IP地址和端口号了。

大概的原理就是这样子，mDNS提供的服务要远远多于这个，当然服务多但并不复杂。

在Apple 的设备上（电脑，笔记本，iphone，ipad等设备）都提供了这个服务。很多Linux设备也提供这个服务。Windows的设备可能没有提供，但是如果安装了iTunes之类的软件的话，也提供了这个服务。

这样就可以利用这个服务开发一些局域网内的自动发现，然后提供一些局域网内交互的应用了。

https://www.cnblogs.com/leonxyzh/p/7289025.html

