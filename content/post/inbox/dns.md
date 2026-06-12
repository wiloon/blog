---
title: DNS
author: "-"
date: 2017-12-17T06:27:24+00:00
lastmod: 2026-06-13T00:33:28+08:00
url: dns
categories:
  - Network
tags:
  - remix
  - AI-assisted
aliases:
  - /p11620/
---
## DNS

DNS 的本质是什么？
  
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

mDNS（Multicast DNS，多播 DNS）主要实现了在没有传统 DNS 服务器的情况下，使局域网内的主机实现相互发现和通信。遵从 DNS 协议，使用现有的 DNS 信息结构、名语法和资源记录类型，端口 `5353`。

在局域网内，设备之间通信需要知道对方的 IP 地址，而大多数情况下 IP 由 DHCP 动态分配，mDNS 就是来解决这个设备发现问题的。每个进入局域网的主机如果开启了 mDNS 服务，都会向局域网内的所有主机组播一条消息：我是谁（域名），和我的 IP 地址是多少。其他有 mDNS 服务的主机就会响应，也会告诉你它是谁和它的 IP 地址。

平台支持：Apple 设备（macOS、iOS）原生支持；Linux 设备通过 systemd-resolved 或 avahi 支持；Windows 安装 iTunes 等软件后也提供此服务。

### 工作原理

- 基于 UDP 协议
- 组播地址：`224.0.0.251`（IPv6：`FF02::FB`），端口 `5353`
- 组播地址使用 D 类地址，范围：`224.0.0.0—239.255.255.255`
- 主机域名以 `.local` 结尾
- 查询时设备通过组播发起请求；对应设备通过组播应答，其他主机也会收到并更新缓存

### Bonjour

Bonjour 是 Apple 公司为基于 mDNS 的开放性零配置网络标准所起的名字（法语中 Hello 的意思）。`mDNSResponder` 是 Bonjour 的核心组件。

使用 Bonjour 的设备在网络中自动组播它们的服务信息并监听其它设备的服务信息，使得局域网中的系统和服务即使在没有网络管理员的情况下也很容易被找到。

### Arch Linux：启用 mDNS（systemd-resolved）

systemd-resolved 默认禁用 mDNS，通过以下配置启用：

```bash
# /etc/systemd/resolved.conf
[Resolve]
MulticastDNS=yes
```

```bash
sudo systemctl restart systemd-resolved
```

## 域名解析, DNS

### 域名解析

域名解析就是国际域名或者国内域名以及中文域名等域名申请后做的到IP地址的转换过程。IP地址是网路上标识您站点的数字地址,为了简单好记,采用域名来代替ip地址标识站点地址。域名的解析工作由DNS服务器完成。

### A (Address) 记录

A (Address) 记录是用来指定主机名 (或域名) 对应的 IP 地址记录。用户可以将该域名下的网站服务器指向到自己的 web server 上。
同时也可以设置您域名的二级域名。

1. 如果想创建不带 www 的记录, 即 ezloo.com, 在主机记录中填写 @ 或者留空, 不同的注册商可能不一样。
2. 创建多个域名到同一个 IP, 比如给博客建了二级域名, 可以使用 *.blog.ezloo.com 来指向一个 IP, 这样的话, 不管是访问 a.blog.ezloo.com 还是 b.blog.ezloo.com 都能到同一个 IP。
3. 如果你给同一个二级域名设置了多个 A 记录, 比如你建了两个 blog 的 A 记录, 其中一个指向了 111.111.111.111, 另一个指向了 111.111.111.112, 那么在查询的时候, 每次返回的数据包含了两个 IP 地址, 但是在返回的过程中数据排列的顺序每次都不相同。由于大部分的客户端只选择第一条记录所以通过这种方式可以实现一定程度的负载均衡。

在命令行下可以通过 `nslookup -qt=a www.ezloo.com` 来查看 A 记录。

### CNAME 记录
  
别名记录。这种记录允许您将多个名字映射到同一台计算机。 通常用于同时提供 WWW 和 MAIL 服务的计算机。
例如, 有一台计算机名为 "host.mydomain.com" (A记录) 。 它同时提供 WWW 和 MAIL 服务, 为了便于用户访问服务。
可以为该计算机设置两个别名 (CNAME) : WWW 和 MAIL。 这两个别名的全称就 `www.mydomain.com` 和 mail.mydomain.com。
实际上他们都指向 host.mydomain.com

### TTL
  
TTL 值全称是"生存时间 (Time To Live)",简单的说它表示DNS记录在DNS服务器上缓存时间。要理解TTL值,请先看下面的一个例子:
  
假设,有这样一个域名myhost.abc.com (其实,这就是一条DNS记录,通常表示在abc.com域中有一台名为myhost的主机) 对应IP地址为1.1.1.1,它的TTL为10分钟。这个域名或称这条记录存储在一台名为dns.abc.com的DNS服务器上。
TTL=time to live,表示解析记录在DNS服务器中的缓存时间。比如当我们请求解析www.ezloo.com的时候,DNS服务器发现没有该记录,就会下个NS服务器发出请求,获得记录之后,该记录在DNS服务器上保存TTL的时间长度。当我们再次发出请求解析www.ezloo.com 的时候,DNS服务器直接返回刚才的记录,不去请求NS服务器。TTL的时间长度单位是秒,一般为3600秒。

## NS 记录  NS (Name Server) 记录

NS 记录是域名服务器记录,用来指定域名由哪台服务器来进行解析。可以使用nslookup -qt=ns ezloo.com来查看。  
域名服务器记录,用来指定该域名由哪个DNS服务器来进行解析。  您注册域名时,总有默认的DNS服务器,每个注册的域名都是由一个DNS域名服务器来进行解析的,DNS服务器NS记录地址一般以以下的形式出现:  ns1.domain.com、ns2.domain.com等。  简单的说,NS记录是指定由哪个DNS服务器解析你的域名。  

CNAME记录

CNAME记录也成别名记录,它允许你将多个记录映射到同一台计算机上。比如你建了如下几条记录:

a1 CNAME a.ezloo.com
  
a2 CNAME a.ezloo.com
  
a3 CNAME a.ezloo.com
  
a A 111.222.111.222

我们访问a1 (a2,a3) .ezloo.com的时候,域名解析服务器会返回一个CNAME记录,并且指向a.ezloo.com,然后我们的本地电脑会再发送一个请求,请求a.ezloo.com的解析,返回IP地址。

当我们要指向很多的域名到一台电脑上的时候,用CNAME比较方便,就如上面的例子,我们如果服务器更换IP了,我们只要更换a.ezloo.com的A记录即可。

在命令行下可以使用nslookup -qt=cname a.ezloo.com来查看CNAME记录。

### TXT 记录

TXT记录一般是为某条记录设置说明,比如你新建了一条a.ezloo.com的TXT记录,TXT记录内容"this is a test TXT record.",然后你用 nslookup -qt=txt a.ezloo.com ,你就能看到"this is a test TXT record"的字样。

除外,TXT还可以用来验证域名的所有,比如你的域名使用了Google的某项服务,Google会要求你建一个TXT记录,然后Google验证你对此域名是否具备管理权限。

在命令行下可以使用nslookup -qt=txt a.ezloo.com来查看TXT记录。

### AAAA 记录

AAAA记录是一个指向IPv6地址的记录。

可以使用nslookup -qt=aaaa a.ezloo.com来查看AAAA记录。

### SOA 记录

NS 记录说明了有多台服务器在进行解析,但哪一个才是主服务器呢, NS 并没有说明, 这个就要看 SOA 记录了, SOA 名叫起始授权机构记录, 
SOA 记录说明了在众多 NS 记录里那一台才是主要的服务器！

SOA 记录表明了 DNS 服务器之间的关系。SOA 记录表明了谁是这个区域的所有者。比如 51CTO.COM 这个区域。
一个 DNS 服务器安装后, 需要创建一个区域, 以后这个区域的查询解析, 都是通过 DNS 服务器来完成的。
现在来说一下所有者, 我这里所说的所有者, 就是谁对这个区域有修改权利。常见的 DNS 服务器只能创建一个标准区域, 然后可以创建很多个辅助区域。
标准区域是可以读写修改的。而辅助区域只能通过标准区域复制来完成, 不能在辅助区域中进行修改。 
而创建标准区域的 DNS 就会有 SOA 记录, 或者准确说 SOA 记录中的主机地址一定是这个标准区域的服务器IP地址。

[https://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html](https://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html)

## DNS

### [http://www.alidns.com/](http://www.alidns.com/)

   223.5.5.5
   223.6.6.6

### Google DNS

    8.8.8.8

### IBM DNS

    9.9.9.9

## MX 记录

邮件路由记录,用户可以将该域名下的邮件服务器指向到自己的mail server上,然后即可自行操控所有的邮箱设置。您只需在线填写您服务器的IP地址,即可将您域名下的邮件全部转到您自己设定相应的邮件服务器上。

MX记录是Mail Exchanger的缩写,意思是邮件交换记录,它指向一个邮件服务器,用于电子邮件系统发邮件时根据收信人的地址后缀来定位邮件服务器。例如,当Internet上的某用户要发一封信给`user@mydomain.com`时,该用户的邮件系统通过DNS查找mydomain.com这个域名的MX记录,如果MX记录存在, 用户计算机就将邮件发送到MX记录所指定的邮件服务器上。

检查MX记录是否存在的方法

进行 DNS 查询的一个非常有用的工具是 nslookup,可以使用它来查询DNS中的各种数据。可以在 Windows 的命令行下直接运行 nslookup 进入一个交互模式, 在这里能查询各种类型的 DNS 数据。在运行中输入 cmd 回车,打开命令提示符, 输入 nslookup -q=mx mydomain.com 便可检查 MX 记录是否生效。

在命令行下可以通过 nslookup -qt=mx ezloo.com 来查看MX记录。

mx 记录的权重对 Mail 服务是很重要的,当发送邮件时,Mail 服务器先对域名进行解析,查找 mx 记录。先找权重数最小的服务器 (比如说是 10) ,如果能连通,那么就将服务器发送过去；如果无法连通 mx 记录为 10 的服务器,那么才将邮件发送到权重为 20 的 mail 服务器上。

这里有一个重要的概念,权重 20 的服务器在配置上只是暂时缓存 mail ,当权重 20 的服务器能连通权重为 10 的服务器时,仍会将邮件发送的权重为 10 的 Mail 服务器上。当然,这个机制需要在 Mail 服务器上配置。 ([http://blog.ixpub.net/viewthread-1308142](http://blog.ixpub.net/viewthread-1308142))
