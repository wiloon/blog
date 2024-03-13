---
title: nftables
author: "-"
date: 2016-05-25T15:41:20+00:00
url: nftables
categories:
  - Network
tags:
  - reprint
---
## nftables

nftables 是一个新式的数据包过滤框架，旨在替代现用的 iptables、ip6tables、arptables 和 ebtables 的新的包过滤框架。nftables 诞生于 2008 年，2013 年底合并到 Linux 内核，从 Linux 内核 3.13 版本开始大多数场景下 nftables 已经可以使用，但是完整的支持（即：nftables 优先级高于 iptables）应该是在 Linux 内核 3.15 版本。

nftables 旨在解决现有 {ip/ip6}tables 工具存在的诸多限制。相对于旧的 iptables，nftables 最引人注目的功能包括：改进性能、支持查询表、事务型规则更新、所有规则自动应用等等。

nftables 主要由三个组件组成：内核实现、libnl netlink 通信和 nftables 用户空间。其中内核提供了一个 netlink 配置接口以及运行时规则集评估，libnl 包含了与内核通信的基本函数，用户空间可以通过新引入的命令行工具 nft 和用户进行交互。

nft 可以通过在寄存器中储存和加载来交换数据。也就是说，它的语法与 iptables 不同。但 nft 可以利用内核提供的表达式去模拟旧的 iptables 命令，维持兼容性的同时获得更大的灵活性。简单来说，nft 是 iptables 及其衍生指令（ip6tables 和 arptables ）的超集。

nftables 的特点
nftables 拥有一些高级的类似编程语言的能力，例如：定义变量和包含外部文件，即拥有使用额外脚本的能力。nftables 也可以用于多种地址簇的过滤和处理。

不同于 iptables, nftables 并不包含任何的内置表，需要哪些表并在这些表中添加什么处理规则一切由管理员决定。

表包含规则链，规则链包含规则。

nftables 相较于 iptables 的优点
更新速度更快
在 iptables 中添加一条规则，会随着规则数量增多而变得非常慢。这种状况对 nftables 而言就不存在了，因为 nftables 使用原子的快速操作来更新规则集合。

内核更新更少。
使用 iptables 时，每一个匹配或投递都需要内核模块的支持。因此，如果你忘记一些东西或者要添加新的功能时都需要重新编译内核。而在 nftables 中就不存在这种情况了， 因为在 nftables 中，大部分工作是在用户态完成的，内核只知道一些基本指令（过滤是用伪状态机实现的）。例如，icmpv6 支持是通过 nft 工具的一个简单的补丁实现的，而在 iptables 中这种类型的更改需要内核和 iptables 都升级才可以。


nftables 作为新一代的防火墙策略框架, 是从内核 3.13 版本引入的新的数据包过滤框架, 
nftables 是一个致力于替换现有的 {ip,ip6,arp,eb} tables 框架 (也就是大家熟知的iptables) 的项目,而且提供了类似tc的带宽限速能力

nftables 引入了一个新的命令行工具 nft, 取代了之前的 iptables、ip6iptables、`ebtables` 等各种工具,是用户空间的管理工具。

netfilter 是 Linux 内核的包过滤框架, 它提供了一系列的钩子 (Hook) 供其他模块控制包的流动。这些钩子包括

- NF_IP_PRE_ROUTING: 刚刚通过数据链路层解包进入网络层的数据包通过此钩子,它在路由之前处理
- NF_IP_LOCAL_IN: 经过路由查找后, 送往本机 (目的地址在本地) 的包会通过此钩子 对应 input
- NF_IP_FORWARD: 不是本地产生的并且目的地不是本地的包 (即转发的包) 会通过此钩子
- NF_IP_LOCAL_OUT: 所有本地生成的发往其他机器的包会通过该钩子; 对应 output
- NF_IP_POST_ROUTING: 在包就要离开本机之前会通过该钩子, 它在路由之后处理

nftables 的表管理
与 iptables 中的表不同，nftables 中没有内置表。表的数量和名称由用户决定。但是，每个表只有一个地址簇，并且只适用于该簇的数据包。nftables 表可以指定为以下五个簇中的一个：

- ip: 仅匹配 IPv4 数据包。如果没有指定地址系列，这是默认设置。
- ip6: 仅匹配 IPv6 数据包。
- inet: iptables 和 ip6tables
- arp: 匹配 IPv4 地址解析协议(ARP)数据包。
- bridge: 匹配通过网桥设备的数据包。 对应 ebtables

ip（即 IPv4）是默认簇，如果未指定簇，则使用该簇。如果要创建同时适用于 IPv4 和 IPv6 的规则，请使用 inet 簇 。inet 允许统一 ip 和 ip6 簇，以便更容易地定义规则。

注意: inet 不能用于 nat 类型的链，只能用于 filter 类型的链。

## nftables 的链管理

链是用来保存规则的，与 iptables 中的链不同，nftables 没有内置链。这意味着和表一样，链也需要被显示创建。链有以下两种类型：

- 常规链 : 主要用来做跳转，不需要指定钩子类型和优先级。从逻辑上对规则进行分类，支持所有的 nftables 簇。
- 基本链 : 来自网络栈数据包的入口点，需要指定钩子类型和优先级，支持 ip 和 ip6 簇。

创建链
创建一个常规链
1
2
# 将名为 tcpchain 的常规链添加到 inet 簇中名为 mytable 的表中
$ nft add chain inet mytable tcpchain
创建一个基本链
添加一个基本链，你必需指定钩子和优先级。基本链的类型可以是 filter、route 或者 nat。

添加一个筛选输入数据包的基本链
nft add chain inet mytable input { type filter hook input priority 0\; }

注意：命令中的反斜线 （\） 用来转义，这样 Shell 就不会将分号解释为命令的结尾。

编辑链
要编辑一个链，只需按名称调用并重新定义要更改的规则即可。

1
2
# 将默认表中的 input 链策略从 accept 更改为 drop
$ nft chain inet mytable input { policy drop \; }
清空链中的规则
1
2
# 清空指定链中的规则，这里为 input
$ nft flush chain inet mytable input
删除链
1
2
# 删除指定的链，这里为 input
$ nft delete chain inet mytable input
注意：要删除的链中不能包含任何规则或者跳转目标。

## nftables 的规则管理

nftables 规则由语句或表达式构成，包含在链中。以下为创建 nftables 规则的基本命令语法：

nft add rule [<family>] <table> <chain> <matches> <statements>
nft insert rule [<family>] <table> <chain> [position <position>] <matches> <statements>
nft replace rule [<family>] <table> <chain> [handle <handle>] <matches> <statements>
nft delete rule [<family>] <table> <chain> [handle <handle>]


其中 matches 是报文需要满足的条件。matches 的内容非常多，可以识别以下多种类型的报文。

ip          :  ipv4 协议字段
ip6         :  ipv6 协议字段
tcp         :  tcp 协议字段
udp         :  udp 协议字段
udplite     :  udp-lite 协议
sctp        :  sctp 协议
dccp
ah
esp
comp
icmp
icmpv6
ether       :  以太头
dst
frag        :
hbh
mh
rt            
vlan        :  vlan
arp         :  arp协议
ct          :  连接状态
meta        :  报文的基本信息
对每一种类型的报文，你又可以同时检查多个字段，例如：

ip dscp cs1
ip dscp != cs1
ip dscp 0x38
ip dscp != 0x20
ip dscp {cs0, cs1, cs2, cs3, cs4, cs5, cs6, cs7, af11, af12, af13, af21,
af22, af23, af31, af32, af33, af41, af42, af43, ef}

ip length 232
ip length != 233
ip length 333-435
ip length != 333-453
ip length { 333, 553, 673, 838}

ip6 flowlabel 22
ip6 flowlabel != 233
ip6 flowlabel { 33, 55, 67, 88 }
ip6 flowlabel { 33-55 }
而 statement 是报文匹配规则时触发的操作，大致有以下几种：

Verdict statements :   动作
Log                :   记录日志并继续处理请求
Reject             :   停止处理并拒绝请求
Counter            :   计数
Limit              :   如果达到了接收数据包的匹配限制，则根据规则处理数据包
Nat                :   NAT
Queuea             :   停止处理并发送数据包到用户空间程序
其中 Verdict Statements 是一组动作，大致有以下几种：

accept：接受数据包并停止剩余规则评估。

drop：丢弃数据包并停止剩余规则评估。

queue：将数据包排队到用户空间并停止剩余规则评估。

continue：使用下一条规则继续进行规则评估。

return：从当前链返回并继续执行最后一条链的下一条规则。

jump ：跳转到指定的规则链，当执行完成或者返回时，返回到调用的规则链。

goto ：类似于跳转，发送到指定规则链但不返回。

增加规则

```Bash
nft add rule inet mytable input tcp dport ssh accept
```

默认情况下，add 表示将规则添加到链的末尾。如果你想从链的开头增加规则，可以使用 insert 来实现。

1
$ nft insert rule inet mytable input tcp dport http accept
列出规则
列出目前链中所有的规则

$ nft list ruleset
table inet mytable {
chain input {
type filter hook input priority 0; policy accept;
tcp dport http accept
tcp dport ssh accept
}
}
列出某个表中的所有规则
1
$ nft list table inet mytable
列出某条链中的所有规则
1
$ nft list chain inet mytable input

nftables 链支持钩子的类型

nftables 和 iptables 类似，依然使用 netfiler 中的 5 个 钩子。 不同的是 nftables 在 Linux Kernel 4.2 中新增了 ingress 钩子。

nftables 链支持钩子的作用

- `prerouting`：刚到达并未被 nftables 的其他部分所路由或处理的数据包。
- input：已经被接收并且已经经过 `prerouting` 钩子的传入数据包。
- forward：如果数据报将被发送到另一个设备，它将会通过 forward 钩子。
- output：从本地传出的数据包。
- `postrouting`：仅仅在离开系统之前，可以对数据包进行进一步处理。

nftables 链支持钩子的适用范围

ip、ip6 和 inet 簇支持的钩子有： `prerouting`、 input、forward、 output、`postrouting` 。

arp 簇支持的钩子有： input、output 。

nftables 链支持的优先级

优先级采用整数值表示，数字较小的链优先处理，并且可以是负数。可以使用的值有：

NF_IP_PRI_CONNTRACK_DEFRAG (-400)

NF_IP_PRI_RAW (-300)

NF_IP_PRI_SELINUX_FIRST (-225)

NF_IP_PRI_CONNTRACK (-200)

NF_IP_PRI_MANGLE (-150)

NF_IP_PRI_NAT_DST (-100)

NF_IP_PRI_FILTER (0)

NF_IP_PRI_SECURITY (50)

NF_IP_PRI_NAT_SRC (100)

NF_IP_PRI_SELINUX_LAST (225)

NF_IP_PRI_CONNTRACK_HELPER (300)

nftables 链对报文数据支持采取的动作

accept

drop

queue

continue

return




nftables 结构上分为 table(表), chain(链), rule(规则), 
与 Iptables 不一致的地方在于, table 与 chain 允许不止一个, 名字也可以自由设置。
  
在 nftables 中, 表是链的容器。所以开始使用 nftables 时你首先需要做的是添加至少一个表。
然后, 你可以向你的表里添加链, 然后往链里添加规则。

table 只是存放 chain 的容器, 不同 table 之间没有直接关系。
  
不同的 chain 通过 priority 进行选择。相同类型的链, 
priority 数值最小、或者相同 priority 但是最先添加的 chain 作为当前有效类型的链表。
  
跟 iptables 类似, nftables 也是使用表和链来管理规则。

inet 在 Linux 内核 3.14 之后可用。这个特殊的表是 IPv4 和 IPv6 混合使用的表, 这对简化混合栈防火墙的管理有帮助。
因此, 你在 inet 表中注册的链在 IPv4 和 IPv6 中都能看到。
  
`netdev`, 这在 Linux 内核 4.2 之后可用。它有一个进入时的钩子, 你可以使用它注册一个链以便在路由之前更早的阶段进行过滤, 
它是已存在的 tc 的替代。

https://wiki.shileizcc.com/display/firewall/nftables
  
https://itxx00.github.io/blog/2017/06/13/nftables-man-page/
  
https://github.com/feiskyer/sdn-handbook/blob/master/linux/iptables.md
  
http://dog250.blog.51cto.com/2466061/1583015

https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management

https://farkasity.gitbooks.io/nftables-howto-zh/content/chapter3/operations_at_ruleset_level.html

[https://home.regit.org/netfilter-en/nftables-quick-howto/](https://home.regit.org/netfilter-en/nftables-quick-howto/)

[https://blog.csdn.net/dog250/article/details/54170683](https://blog.csdn.net/dog250/article/details/54170683)

[http://blog.jobbole.com/59624/](http://blog.jobbole.com/59624/)

[https://farkasity.gitbooks.io/nftables-howto-zh/content/](https://farkasity.gitbooks.io/nftables-howto-zh/content/)

[http://wiki.nftables.org/wiki-nftables/index.php/Main_Page](http://wiki.nftables.org/wiki-nftables/index.php/Main_Page)

nftables 链支持钩子的作用

prerouting：刚到达并未被 nftables 的其他部分所路由或处理的数据包。

input：已经被接收并且已经经过 prerouting 钩子的传入数据包。

forward：如果数据报将被发送到另一个设备，它将会通过 forward 钩子。

output：从本地传出的数据包。

postrouting：仅仅在离开系统之前，可以对数据包进行进一步处理。

nftables 链支持钩子的适用范围

ip、ip6 和 inet 簇支持的钩子有： prerouting、 input、forward、 output、postrouting 。

arp 簇支持的钩子有： input、output 。

nftables 链支持的优先级

优先级采用整数值表示，数字较小的链优先处理，并且可以是负数。可以使用的值有：

NF_IP_PRI_CONNTRACK_DEFRAG (-400)

NF_IP_PRI_RAW (-300)

NF_IP_PRI_SELINUX_FIRST (-225)

NF_IP_PRI_CONNTRACK (-200)

NF_IP_PRI_MANGLE (-150)

NF_IP_PRI_NAT_DST (-100)

NF_IP_PRI_FILTER (0)

NF_IP_PRI_SECURITY (50)

NF_IP_PRI_NAT_SRC (100)

NF_IP_PRI_SELINUX_LAST (225)

NF_IP_PRI_CONNTRACK_HELPER (300)

nftables 链对报文数据支持采取的动作

accept

drop

queue

continue

return
