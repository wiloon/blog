---
title: ipset
author: "-"
date: 2016-07-23T09:22:41+00:00
url: /?p=9145
categories:
  - Inbox
tags:
  - reprint
---
## ipset

```bash
# install ipset
pacman -S ipset
apt-get install ipset

# 查看集合。
ipset list

ipset create vlist hash:net

ipset add myset 14.144.0.0/12
ipset -A vlist 172.217.24.14

ipset del yoda x.x.x.x    # 从 yoda 集合中删除内容
ipset list yoda           # 查看 yoda 集合内容
ipset list                # 查看所有集合的内容
ipset flush yoda          # 清空 yoda 集合
ipset flush               # 清空所有集合
ipset destroy yoda        # 销毁 yoda 集合
ipset destroy             # 销毁所有集合
ipset save > /etc/ipset.up.rules                # 输出所有集合内容到标准输出
ipset restore -! < /etc/ipset.up.rules             # 根据输入内容恢复集合内容

```

### 启动时创建ipset

```bash
vim /etc/systemd/system/ipset-persistent.service

[Unit]
Description=ipset persistancy service
DefaultDependencies=no
Requires=netfilter-persistent.service
Requires=ufw.service
Before=network.target
Before=netfilter-persistent.service
Before=ufw.service
ConditionFileNotEmpty=/etc/ipsets.conf
 
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/ipset restore -f -! /etc/ipsets.conf
 
# save on service stop, system shutdown etc.
ExecStop=/sbin/ipset save blacklist -f /etc/ipsets.conf
 
[Install]
WantedBy=multi-user.target
 
RequiredBy=netfilter-persistent.service
RequiredBy=ufw.service
```
[https://confluence.jaytaala.com/pages/viewpage.action?pageId=11763750#UsingipsettoblockIPaddresses-firewall-Settingipsettobepersistent(notloselistsonreboot)](https://confluence.jaytaala.com/pages/viewpage.action?pageId=11763750#UsingipsettoblockIPaddresses-firewall-Settingipsettobepersistent(notloselistsonreboot))

[https://fixatom.com/block-ip-with-ipset/](https://fixatom.com/block-ip-with-ipset/)
  
-N, 创建 集合名称 类型 类型具体选项
  
创建一个用集合名称命名并且指定类型的集合。类型具体选项必须是系统规定的。

iptables是在linux内核里配置防火墙规则的用户空间工具,它实际上是netfilter框架的一部分.可能因为iptables是netfilter框架里最常见的部分,所以这个框架通常被称为iptables,iptables是linux从2.4版本引入的防火墙解决方案.
  
ipset是 Linux 防火墙iptables的一个伴随工具。是iptables的扩展,它允许你创建匹配整个地址sets (地址集合)  的规则。而不像普通的iptables链是线性的存储和过滤,ip集合存储在带索引的数据结构中,这种结构即时集合比较大也可以进行高效的查找.

除了一些常用的情况,比如阻止一些危险主机访问本机,从而减少系统资源占用或网络拥塞,IPsets也具备一些新防火墙设计方法,并简化了配置.

在本文中,在快速的讨论ipsets的安装要求后,我会花一点时间来介绍iptables的核心机制和基本概念.然后我会介绍ipset的使用方法和语法,并且演示ipset如何与iptables结合来完成各种不同的配置。最后,我会提供一些细节和较高级的例子来演示如何解决现实中的问题。

ipset比传统的iptables拥有显著的性能提升和扩展特性,比如将单个防火墙规则通过一次配置应用到整个主机所在的组和网络。

由于ipset只是iptables的扩展,所以也会对iptables进行描述。

在许多的linux发布中ipset是一个简单的安装包,大家可以通过自己的linux发行版提供的包管理工具进行安装。

需要理解的重点时,同iptables一样,ipset是由用户空间的工具和内核空间的模块两部分组成,所以你需要将这两部分都准备好。你也需要"ipset-aware"这个iptables 模块,这个模块用来增加 rules that match against sets。 (……)

首先我们使用自己的linux发行版的包管理工具对ipset进行搜索。在ubuntu上安装需要安装ipset 和 xtables-addons-source 包,然后,运行module-assistant auto-install xtables-addons,等待大约30秒后ipset就可以使用了。

如果你的linux发行版没有被支持,那就需要根据ipset 首页中的安装步骤构建源码并对内核打补丁。

这篇文章中使用ipset v4.3 和 iptables v1.4.9。

iptables概述

简单来讲,iptables防火墙配置由规则链的集合组成,每一个链包含一个规则。一个数据包,在各个处理阶段,内核商量合适的规则来决定数据报的命运。

规则链按照顺序进行匹配,基于数据包的流向 (remote-to-local, remote-to-remote or local-to-remote)和当前所处的处理阶段(before or after "routing")。参考图1。
  
当需要匹配规则链时,数据包需要与链中的每个规则按照顺序进行比对,直道找到匹配的规则。一旦找到了匹配的规则,目标规则就会被调用。如果最后一个规则与数据包也不匹配,就会使用默认规则。
  
一个规则链就是许多规则按顺序排列组成,一个规则就是match/target 的组合。一个简单的match例子是"TCP 目标端口为80"。target的例子是"接受这个包"。target同样可以将数据包重定向到其他的用户自定义的链,用户自定义链提供了一些机制,包括组合和细分规则,将多个链级联来完成一个功能。
  
每一个用来定义规则的iptables命令,不管是用于简单的规则还是复杂的规则,都有三个基本的部分组成,包括指定table/chain (and order), match 和 target。

Figure 2. 解析iptables 命令
  
配置所有的这些选项,创建一个完整得防火墙,你需要按照特定的顺序运行一系列的iptables命令。
  
iptables非常强大并且可扩展。除了许多内部特性,iptables提供了扩展match和target的API。
  
ipset
  
ipset是iptables的match扩展。如果要使用它,需要使用ipset命令行工具创建一个集合并指定一个唯一的集和名,然后在iptables规则的match部分分别索引这些集合。
  
一个集合是一个方便有效快速查询的地址列表。
  
下面有两个常见的iptables命令,这两个命令阻止从1.1.1.1和2.2.2.2进入主机的数据包:
  
iptables -A INPUT -s 1.1.1.1 -j DROP
  
iptables -A INPUT -s 2.2.2.2 -j DROP
  
match 部分语法 -s 1.1.1.1 表示"匹配源地址是1.1.1.1的数据包"。
  
下面的ipset/iptables命令同样可以达到上面的目的:
  
ipset -N myset iphash
  
ipset -A myset 1.1.1.1
  
ipset -A myset 2.2.2.2
  
iptables -A INPUT -m set –set myset src -j DROP
  
上面的ipset命令创建了一个包含两个地址(1.1.1.1 and 2.2.2.2)的集合(myset of type iphash)。
  
然后iptables命令通过-m set –set myset src这个match选项使用这个集合,这个匹配规则的意思是"匹配源地址包含在集合myset中的数据包"
  
src 表示源地址,dst表示目标地址。如果同时使用 src 和 dst 表示既要匹配源地址又要匹配目的地址。
  
在第二个例子里,只需要一个iptables命令,不管集合里有多少ip地址需要添加。虽然这个例子里只使用了两个地址,但是你可以依据这个例子简单的定义1000个地址,并且仍然只需要一条iptables语句。而如果使用第一个例子的方法,不使用ipset,就需要1000条iptables规则。
  
Set Types
  
每一个集合都是特定类型的,它不但定义了什么类型的值可以储存在里面(IP addresses, networks, ports and so on),而且定义了如何匹配数据包 (换言之,数据包的那一部分需要被检查和如何检查) 。除了一些最通用的集合类型,比如检查ip地址,也提供了一些其他的集合类型,比如检查端口,地址和端口同时检查,mac地址和ip地址同时检查等。
  
每一种集合类型都有自己的规则,这些规则表示集合的类型,范围,它包含的值得分布。不同的集合类型使用不同的类型索引,并且在不同的情况下被优化。需要根据不同的现实情况选择集合类型。
  
最灵活的集合类型是iphash,它可以存储任意的ip地址和nethash (IP/mask) 。请参考ipset的man手册来了解所有的集合类型。
  
setlist是一个特别的集合类型,它允许组织多个集合到一个集合里面。比如你需要一个单独的集合既包含ip地址又包含网络信息。
  
Advantages of ipset
  
除了性能优势,一些情况下ipset允许更直接的配置方法。
  
如果你想定义一个防火墙环境,该环境不会处理来自1.1.1.1和2.2.2.2的包,并且处理过程包含在mychain中,注意下面的方法是无效的:
  
iptables -A INPUT -s ! 1.1.1.1 -g mychain
  
iptables -A INPUT -s ! 2.2.2.2 -g mychain
  
如果数据包来自1.1.1.1,它匹配第一条规则失败,但是匹配第二条规则时会成功。如果数据包来自2.2.2.2,匹配第一个规则就会成功。
  
虽然有有一些其它的方法可以不适用ipset就能达到指定的要求,但是ipset是最直接了当的。
  
ipset -N myset iphash
  
ipset -A myset 1.1.1.1
  
ipset -A myset 2.2.2.2
  
iptables -A INPUT -m set ! –set myset src -g mychain
  
用上面的方法,如果数据包来自1.1.1.1,它不会匹配规则(because the source address 1.1.1.1 does match the set myset)。如果数据包来自2.2.2.2,它也不会匹配规则。
  
这只是一个简单的例子,它说明在一个规则里匹配完整条件的基本优点。其他方面,每个iptables规则与其它规则是独立的,并且将规则逻辑的连接起来是比较难的,特别当它包含混合了正常和反向测试时。ipset只是在这些情况下使配置变简单。
  
ipset的另一个优势是集合可以动态的修改,即使iptables的规则正在使用这个集合。添加/修改/删除接口使用很简单并且是顺序无关的。另一方面,在iptables里每一条规则都比较复杂,并且规则的顺序也是很重要的元素,所以修改内部规则很困难并且会存在潜在问题。
  
Excluding WAN, VPN and Other Routed Networks from the NAT—the Right Way

Outbound NAT (SNAT 或 IP 伪装)允许私有局域网内的主机访问internet.iptables NAT规则匹配私网内访问internat的包,并用网关地址替换包的源地址 (使数据包看起来像是从网关发送的,从而隐藏网关后面的主机) 。

NAT自动跟踪活动的连接,所以它能将返回的包发送给正确的内网主机 (通过将数据包的目的地址修改为内部主机地址) 。

下面是一个简单的outbound NAT规则,10.0.0.0/24是内部局域网:

iptables -t nat -A POSTROUTING \
  
-s 10.0.0.0/24 -j MASQUERADE

该规则匹配所有来自内网的包,并对他们进行伪装。如果只有一个路由连接到internat这种方法是非常有效率的,通过该路有的所有流量都是公网的流量。然而,如果有连接到其它私有网络的路由存在,比如VPN或无力WAN连接,你可能就不会使用地址伪装。

克服这个限制的一个简单方法是基于物理接口建立NAT规则,而不是使用基于网络地址的方式。

iptables -t nat -A POSTROUTING \
  
-o eth0 -j MASQUERADE

该规则假设eth0是外部接口,该规则会匹配所有离开这个接口的包。与前面的规则不同的是,其他内网的数据包通过其它接口访问公网时不会匹配这条规则 (比如OpenVPN的连接) 。

虽然许多连接是通过不同的接口路由,但并不能假设所有的链接都是这样。一个例子是基于KAME的 IPsec VPN 连接(比如 Openswan)就不是使用虚拟接口。

不适用上面的接口匹配技术的另一种情况是如果向外的接口 (连接到Internet的接口) 连接 路由到其他私有网络的中间网络,而不是连接到Internet。

通过匹配物理接口来设计的防火墙规则可以使用在一些人为限制方面,并且依赖网络拓扑。

后来发现,ipset还有另一个应用。假设有一个本地LAN (10.0.0.0/24)需要连接到internet,除此之外还有三个本地网络(10.30.30.0/24, 10.40.40.0/24, 192.168.4.0/23 和 172.22.0.0/22),执行下面的命令:
  
ipset -N routed_nets nethash
  
ipset -A routed_nets 10.30.30.0/24
  
ipset -A routed_nets 10.40.40.0/24
  
ipset -A routed_nets 192.168.4.0/23
  
ipset -A routed_nets 172.22.0.0/22
  
iptables -t nat -A POSTROUTING \
  
-s 10.0.0.0/24 \
  
-m set ! –set routed_nets dst \
  
-j MASQUERADE

如我们所见,ipset 简单的实现了精确匹配。该规则伪装所有来自(10.0.0.0/24)的数据包,而不处理其他在routed_nets集合中的网络的包。由于该配置完全基于网络地址,所以你完全不用担心其他特殊的网络连接 (比如VPN) ,也不用担心物理接口和网络拓扑。

Limiting Certain PCs to Have Access Only to Certain Public Hosts

假设老板较关心员工上班时间上网问题,请你限制员工的PC只能访问指定的几个网站,但是不想所有的内部PC都受到限制。

限制3台PC (10.0.0.5, 10.0.0.6 and 10.0.0.7)只能访问worksite1.com,worksite2.com 和 worksite3.com。执行下面的命令:
  
ipset -N limited_hosts iphash
  
ipset -A limited_hosts 10.0.0.5
  
ipset -A limited_hosts 10.0.0.6
  
ipset -A limited_hosts 10.0.0.7
  
ipset -N allowed_sites iphash
  
ipset -A allowed_sites worksite1.com
  
ipset -A allowed_sites worksite2.com
  
ipset -A allowed_sites worksite3.com
  
iptables -I FORWARD \
  
-m set –set limited_hosts src \
  
-m set ! –set allowed_sites dst \
  
-j DROP

该例子在一条规则里使用了两个集合。如果源地址匹配limited_hosts 目的地址不匹配allowed_sites,数据包就被丢弃。

注意该规则被添加到了FORWARD链,它不会影响防火墙主机自己的通信。

Blocking Access to Hosts for All but Certain PCs (Inverse Scenario)

假设老板想阻止员工访问几个特定的网站,但是不阻止他自己的PC和他助理的PC。在这个例子里,我们可以匹配老板和助理的PC的MAC地址,而不是匹配IP地址。假设他们的MAC是11:11:11:11:11:11 和 22:22:22:22:22:22,需要组织员工访问的站点是badsite1.com, badsite2.com 和 badsite3.com.

这次我们不使用第二个集合匹配MAC地址,而是使用多个iptables命令,利用MARK target标记数据包,而利用后面的规则处理被标记的数据包。

ipset -N blocked_sites iphash
  
ipset -A blocked_sites badsite1.com
  
ipset -A blocked_sites badsite2.com
  
ipset -A blocked_sites badsite3.com
  
iptables -I FORWARD -m mark –mark 0x187 -j DROP
  
iptables -I FORWARD \
  
-m mark –mark 0x187 \
  
-m mac –mac-source 11:11:11:11:11:11 \
  
-j MARK –set-mark 0x0
  
iptables -I FORWARD \
  
-m mark –mark 0x187 \
  
-m mac –mac-source 22:22:22:22:22:22 \
  
-j MARK –set-mark 0x0
  
iptables -I FORWARD \
  
-m set –set blocked_sites dst \
  
-j MARK –set-mark 0x187

上面的例子,由于没有使用ipset完成所有的匹配工作,所以使用的命令比较多,而且比较复杂。由于用到了多个iptables命令,所以各个命令的顺序是非常重要的。

注意这些规则是使用—I (insert)选项而不是使用-A (append)选项。当一个规则被插入,他会被添加的链的顶端,而以前的规则自动下移。因为每一格规则都是被插入德,所以实际的有效顺序是相反的。

最后一个iptables命令实际在FORWARD链的顶端。该规则匹配所有目的地址与blocked_sites集合相匹配的数据包,然后将这些数据标记为0x187.下面的两个规则匹配来自特定MAC地址并且已经标记为0x187的数据包,然后将他们标记为0。

最后,最后的iptables规则丢弃所有的被标记为0x187的数据包。除了来源是两个特定MAC地址的数据包,他将会匹配所有的目标地址在blocked_sites集合里的数据包。

这是解决问题的一种方法。还有一些其他方法,除了使用第二个ipset集合的方法,还可以使用用户自定义链等。

使用第二个ipset集合代替标记的方法是不可能完成上面的要求的,因为ipset没有machash集合类型,只有集合类型,但是他要求同时匹配IP和MAC,而不是只匹配MAC地址。

警告: 在大多数实际环境里,这个方法可能不可行,应为大部分你需要屏蔽的网站他们的主机都有多个ip地址(比如 Facebook, MySpace 等等),而且这些ip会频繁的更换。iptables/ipset的一个限制是主机名只有被解析为单个ip地址时才能使用。

而且,主机名lookup只有在命令执行时发生,所以如果ip地址改变了,防火墙是不会意识到的,而是仍然使用以前的ip地址。基于这个原因,一个完成Web访问限制的更好的方法是使用HTTP代理,比如Squid。

Automatically Ban Hosts That Attempt to Access Invalid Services

ipset为iptables提供了目标扩展功能,它提供了一种向集合动态添加和删除目标的机制。不必手动使用ipset命令添加目标,而是在运行时通过iptables自动添加。

比如,如果远程主机尝试连接端口25,但是你并没有运行SMTP服务,我们怀疑对方不怀好意,所以我们在对方还没有干什么坏事前就组织他的其他尝试,使用下面的规则:

ipset -N banned_hosts iphash
  
iptables -A INPUT \
  
-p tcp –dport 25 \
  
-j SET –add-set banned_hosts src
  
iptables -A INPUT \
  
-m set –set banned_hosts src \
  
-j DROP

如果从端口25接收到数据包,假设来源地址是1.1.1.1,那么该地址马上就被添加到banned_hosts集合,和下面的例子等效:

ipset -A banned_hosts 1.1.1.1

所有的1.1.1.1的连接都会被阻塞。

他同样会阻止其他主机对本设备进行端口扫描,除非他不扫描25号端口。
  
Clearing the Running Config

如果你想清除ipset和iptables的配置,将防火墙reset,运行下面的命令:

iptables -P INPUT ACCEPT
  
iptables -P OUTPUT ACCEPT
  
iptables -P FORWARD ACCEPT
  
iptables -t filter -F
  
iptables -t raw -F
  
iptables -t nat -F
  
iptables -t mangle -F
  
ipset -F
  
ipset -X

如果集合正在被使用,意味着其它的iptables规则正在引用该集合,就不能对集合进行销毁 (ipset -X),所以为了在任何状态下都完成reset,iptables链必须首先清除。

Conclusion

ipset为netfilter/iptables在增加了很多有用的特性和功能,正如本篇文章描述的 ,ipset不仅提供了新的防火墙配制的可能性,而且他减少了之前只使用iptables来配置防火墙的困难。

任何时候,如果你想将防火墙规则应用到一个组,你应该使用ipset。正如前面的例子,你可以通过将ipset与iptables的其它特性相结合,来完成各种各样的网络配置和策略。

下一次你再进行防火墙配置时,考虑使用ipset。我相信你会被他的可用性和灵活性震惊。
  
Resources

Netfilter/iptables Project Home Page: [http://www.netfilter.org](http://www.netfilter.org)

ipset Home Page: [http://ipset.netfilter.org](http://ipset.netfilter.org)

原文地址: [http://www.linuxjournal.com/content/advanced-firewall-configurations-ipset?page=0](http://www.linuxjournal.com/content/advanced-firewall-configurations-ipset?page=0),0
  
[http://blog.chinaunix.net/uid-21706718-id-3561951.html](http://blog.chinaunix.net/uid-21706718-id-3561951.html)
  
[http://blog.sina.com.cn/s/blog_6bdc95ab0100m58b.html](http://blog.sina.com.cn/s/blog_6bdc95ab0100m58b.html)
  
[https://fixatom.com/block-ip-with-ipset/](https://fixatom.com/block-ip-with-ipset/)
  
[http://ipset.netfilter.org/ipset.man.html](http://ipset.netfilter.org/ipset.man.html)
