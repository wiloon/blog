---
title: nftables
author: "-"
date: 2016-05-25T15:41:20+00:00
url: /?p=9022
categories:
  - Inbox
tags:
  - reprint
---
## nftables
<https://home.regit.org/netfilter-en/nftables-quick-howto/>
  
<https://blog.csdn.net/dog250/article/details/54170683>
  
<http://blog.jobbole.com/59624/>
  
<https://farkasity.gitbooks.io/nftables-howto-zh/content/>
  
<http://wiki.nftables.org/wiki-nftables/index.php/Main_Page>

nftables 作为新一代的防火墙策略框架,是从内核 3.13 版本引入的新的数据包过滤框架,nftables是一个致力于替换现有的{ip,ip6,arp,eb}tables框架 (也就是大家熟知的iptables) 的项目,而且提供了类似tc的带宽限速能力
  
nftables 引入了一个新的命令行工具nft,取代了之前的iptables、ip6iptables、ebtables等各种工具,是用户空间的管理工具。

netfilter
  
netfilter是Linux内核的包过滤框架,它提供了一系列的钩子 (Hook) 供其他模块控制包的流动。这些钩子包括
  
NF_IP_PRE_ROUTING: 刚刚通过数据链路层解包进入网络层的数据包通过此钩子,它在路由之前处理
  
NF_IP_LOCAL_IN: 经过路由查找后,送往本机 (目的地址在本地) 的包会通过此钩子
  
NF_IP_FORWARD: 不是本地产生的并且目的地不是本地的包 (即转发的包) 会通过此钩子
  
NF_IP_LOCAL_OUT: 所有本地生成的发往其他机器的包会通过该钩子
  
NF_IP_POST_ROUTING: 在包就要离开本机之前会通过该钩子,它在路由之后处理

nftables 结构上分为 table(表), chain(链), rule(规则), 与Iptables不一致的地方在于,table 与 chain 允许不止一个,名字也可以自由设置。
  
在 nftables 中,表是链的容器。所以开始使用 nftables 时你首先需要做的是添加至少一个表。然后,你可以向你的表里添加链,然后往链里添加规则。

table 只是存放chain的容器,不同table之间没有直接关系。
  
不同的chain通过priority进行选择。相同类型的链,priority数值最小、或者相同priority但是最先添加的chain作为当前有效类型的链表。
  
跟iptables类似,nftables也是使用表和链来管理规则。
  
nftables有 6 种不同类型的表,它们是: 
  
ip
  
arp
  
ip6
  
bridge
  
inet,这在 Linux 内核 3.14 之后可用。这个特殊的表是 IPv4 和 IPv6 混合使用的表,这对简化混合栈防火墙的管理有帮助。因此,你在 inet 表中注册的链在 IPv4 和 IPv6 中都能看到。
  
netdev,这在 Linux 内核 4.2 之后可用。它有一个进入时的钩子,你可以使用它注册一个链以便在路由之前更早的阶段进行过滤,它是已存在的 tc 的替代。

https://wiki.shileizcc.com/display/firewall/nftables
  
https://itxx00.github.io/blog/2017/06/13/nftables-man-page/
  
https://github.com/feiskyer/sdn-handbook/blob/master/linux/iptables.md
  
http://dog250.blog.51cto.com/2466061/1583015

https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management

https://farkasity.gitbooks.io/nftables-howto-zh/content/chapter3/operations_at_ruleset_level.html