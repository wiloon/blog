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
