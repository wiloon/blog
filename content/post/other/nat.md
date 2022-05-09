---
title: 网络地址转换 NAT,Network Address Translation
author: "-"
date: 2013-11-10T05:24:44+00:00
url: /?p=5924
categories:
  - Network
tags:
  - NAT

---
## 网络地址转换 NAT,Network Address Translation
NAT属接入广域网(WAN)技术,是一种将私有(保留)地址转化为公有(合法)IP地址的转换技术,它被广泛应用于各种类型Internet接入方式和各种类型的网络中。原因很简单，NAT不仅完美地解决了lP地址不足的问题，而且还能够有效地避免来自网络外部的攻击，隐藏并保护网络内部的计算机。

基本网络地址转换 (Basic NAT) 是一种将一组 IP地址映射到另一组 IP 地址的技术，这对终端用户来说是透明的。网络地址端口转换 (NAPT) 是一种将群体网络地址及其对应 TCP/UDP 端口翻译成单个网络地址及其对应TCP/UDP端口的方法。这两种操作，即传统 NAT 提供了一种机制，将只有私有地址的内部领域连接到有全球唯一注册地址的外部领域。 
  
由于保密原因或 IP 在外网不合法，网络的内部 IP 地址无法在外部网络使用，就产生了 IP 地址转换的需求。局域网络以外的网络的拓扑结构能以多种方式改变: 公司更换供应商；重组公司主干网络或者供应商合并或散伙。一旦外部拓扑结构改变，本地网络的地址分配也必须改变以反映外部变化。通过将这些变化集中在单个地址转换路由器中，局域网用户并不需知道这些改变。基本地址转换允许主机从内部网络中透明地访问外部网络，并容许从外部访问选定的本地主机。对于一个机构其网络主要用于内部服务而仅有时用于外部访问， 这种配置是很适用的。
  
使用这种转换方法是有一定限制的，即会话的请求及响应的发送必须经过相同的 NAT路由器。在边界路由器上安装 NAT 能确保这一过程，边界路由器在该域中是唯一的，而所有经过的 IP 包要么来自于此域要么到达此域。此外还可使用多重 NAT 设备确保这一过程。
  
NAT 解决方法有其不足之处，仅以增强的网络状态作为补充，而忽略了 IP 地址端对端的重要性。结果是，由于存在 NAT 设备，由 IPSec 保证的端对端 IP 网络级安全无法应用到终端主机。此方法的优势是不需要改变主机或路由器就可以直接安装 NAT 。 
    

### 转换方式
NAT的实现方式有三种，即静态转换Static Nat、动态转换Dynamic Nat和端口多路复用OverLoad。

静态转换是指将内部网络的私有IP地址转换为公有IP地址，IP地址对是一对一的，是一成不变的，某个私有IP地址只转换为某个公有IP地址。借助于静态转换，可以实现外部网络对内部网络中某些特定设备(如服务器)的访问。

动态转换是指将内部网络的私有IP地址转换为公用IP地址时，IP地址是不确定的，是随机的，所有被授权访问上Internet的私有IP地址可随机转换为任何指定的合法IP地址。也就是说，只要指定哪些内部地址可以进行转换，以及用哪些合法地址作为外部地址时，就可以进行动态转换。动态转换可以使用多个合法外部地址集。当ISP提供的合法IP地址略少于网络内部的计算机数量时。可以采用动态转换的方式。

端口多路复用(Port address Translation,PAT)是指改变外出数据包的源端口并进行端口转换，即端口地址转换(PAT，Port Address Translation).采用端口多路复用方式。内部网络的所有主机均可共享一个合法外部IP地址实现对Internet的访问，从而可以最大限度地节约IP地址资源。同时，又可隐藏网络内部的所有主机，有效避免来自internet的攻击。因此，目前网络中应用最多的就是端口多路复用方式。 
       

相关实现

在配置网络地址转换的过程之前，首先必须搞清楚内部接口和外部接口，以及在哪个外部接口上启用NAT。通常情况下，连接到用户内部网络的接口是NAT内部接口，而连接到外部网络(如Internet)的接口是NAT外部接口。
      
http://20100823.blog.51cto.com/2031838/401704


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

## 局域网保留地址

- 10.0.0.0/8
- 100.64.0.0/10
- 172.16.0.0/12
- 192.0.0.0/24

<https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml>