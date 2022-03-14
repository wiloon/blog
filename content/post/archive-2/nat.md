---
title: nat, napt,snat,dnat
author: "-"
date: 2016-01-24T14:16:47+00:00
url: /?p=8704
categories:
  - Uncategorized

tags:
  - reprint
---
## nat, napt,snat,dnat
NAT英文全称是 "Network Address Translation",中文意思是"网络地址转换",它是一个IETF(Internet Engineering Task Force, Internet工程任务组)标准,允许一个整体机构以一个公用IP (Internet Protocol) 地址出现在Internet上。顾名思义,它是一种把内部私有网络地址 (IP地址) 翻译成合法网络IP地址的技术。因此我们可以认为,NAT在一定程度上,能够有效的解决公网地址不足的问题。

- 分类
  
NAT有三种类型: 静态NAT(Static NAT)、动态地址NAT(Pooled NAT)、网络地址端口转换NAPT (Port-Level NAT) 。

NAT的基本工作原理是,当私有网主机和公共网主机通信的IP包经过NAT网关时,将IP包中的源IP或目的IP在私有IP和NAT的公共IP之间进行转换。

其中,网络地址端口转换NAPT (Network Address Port Translation) 则是把内部地址映射到外部网络的一个IP地址的不同端口上。它可以将中小型的网络隐藏在一个合法的IP地址后面。NAPT与 动态地址NAT不同,它将内部连接映射到外部网络中的一个单独的IP地址上,同时在该地址上加上一个由NAT设备选定的端口号。

## NAPT技术
  
由于NAT实现是私有IP和NAT的公共IP之间的转换,那么,私有网中同时与公共网进行通信的主机数量就受到NAT的公共IP地址数量的限制。为了克服这种限制,NAT被进一步扩展到在进行IP地址转换的同时进行Port的转换,这就是网络地址端口转换NAPT (Network Address Port Translation) 技术。
  
NAPT与NAT的区别在于,NAPT不仅转换IP包中的IP地址,还对IP包中TCP和UDP的Port进行转换。这使得多台私有网主机利用1个NAT公共IP就可以同时和公共网进行通信。

NAPT是使用最普遍的一种转换方式,它又包含两种转换方式: SNAT和DNAT。

(1)SNAT (Source Network Address Translation) : 修改数据包的源地址。源NAT改变第一个数据包的来源地址,它永远会在数据包发送到网络之前完成,数据包伪装就是一具SNAT的例子。
  
(2)DNAT (Destination Network Address Translation) : 修改数据包的目的地址。Destination NAT刚好与SNAT相反,它是改变第一个数据懈的目的地地址,如平衡负载、端口转发和透明代理就是属于DNAT。

1.3 应用
  
NAT主要可以实现以下几个功能: 数据包伪装、平衡负载、端口转发和透明代理。
  
数据伪装: 可以将内网数据包中的地址信息更改成统一的对外地址信息,不让内网主机直接暴露在因特网上,保证内网主机的安全。同时,该功能也常用来实现共享上网。
  
端口转发: 当内网主机对外提供服务时,由于使用的是内部私有IP地址,外网无法直接访问。因此,需要在网关上进行端口转发,将特定服务的数据包转发给内网主机。

负载平衡: 目的地址转换NAT可以重定向一些服务器的连接到其他随机选定的服务器。 (不是很明白) 

失效终结: 目的地址转换NAT可以用来提供高可靠性的服务。如果一个系统有一台通过路由器访问的关键服务器,一旦路由器检测到该服务器当机,它可以使用目的地址转换NAT透明的把连接转移到一个备份服务器上。 (如何转移的?) 

透明代理: NAT可以把连接到因特网的HTTP连接重定向到一个指定的HTTP代理服务器以缓存数据和过滤请求。一些因特网服务提供商就使用这种技术来减少带宽的使用而不用让他们的客户配置他们的浏览器支持代理连接。 (如何重定向的?) 

2 原理

2.1 地址转换

NAT的基本工作原理是,当私有网主机和公共网主机通信的IP包经过NAT网关时,将IP包中的源IP或目的IP在私有IP和NAT的公共IP之间进行转换。

如下图所示,NAT网关有2个网络端口,其中公共网络端口的IP地址是统一分配的公共 IP,为202.20.65.5；私有网络端口的IP地址是保留地址,为192.168.1.1。私有网中的主机192.168.1.2向公共网中的主机202.20.65.4发送了1个IP包(Dst=202.20.65.4,Src=192.168.1.2)。

当IP包经过NAT网关时,NAT Gateway会将IP包的源IP转换为NAT Gateway的公共IP并转发到公共网,此时IP包 (Dst=202.20.65.4,Src=202.20.65.5) 中已经不含任何私有网IP的信息。由于IP包的源IP已经被转换成NAT Gateway的公共IP,Web Server发出的响应IP包 (Dst= 202.20.65.5,Src=202.20.65.4) 将被发送到NAT Gateway。

这时,NAT Gateway会将IP包的目的IP转换成私有网中主机的IP,然后将IP包 (Des=192.168.1.2,Src=202.20.65.4) 转发到私有网。对于通信双方而言,这种地址的转换过程是完全透明的。转换示意图如下。

如果内网主机发出的请求包未经过NAT,那么当Web Server收到请求包,回复的响应包中的目的地址就是私网IP地址,在Internet上无法正确送达,导致连接失败。

2.2 连接跟踪

在上述过程中,NAT Gateway在收到响应包后,就需要判断将数据包转发给谁。此时如果子网内仅有少量客户机,可以用静态NAT手工指定；但如果内网有多台客户机,并且各自访问不同网站,这时候就需要连接跟踪 (connection track) 。如下图所示: 

在NAT Gateway收到客户机发来的请求包后,做源地址转换,并且将该连接记录保存下来,当NAT Gateway收到服务器来的响应包后,查找Track Table,确定转发目标,做目的地址转换,转发给客户机。

2.3 端口转换

以上述客户机访问服务器为例,当仅有一台客户机访问服务器时,NAT Gateway只须更改数据包的源IP或目的IP即可正常通讯。但是如果Client A和Client B同时访问Web Server,那么当NAT Gateway收到响应包的时候,就无法判断将数据包转发给哪台客户机,如下图所示。

此时,NAT Gateway会在Connection Track中加入端口信息加以区分。如果两客户机访问同一服务器的源端口不同,那么在Track Table里加入端口信息即可区分,如果源端口正好相同,那么在时行SNAT和DNAT的同时对源端口也要做相应的转换,如下图所示。 (这里的理解灰常重要) 
  
顶
  

http://blog.sina.com.cn/s/blog_5a1d98bc0100zk0h.html
  
http://lustlost.blog.51cto.com/2600869/943110
  
http://blog.csdn.net/hzhsan/article/details/45038265