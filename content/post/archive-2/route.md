---
title: iproute2 > 路由表, routing table, ip route
author: "-"
date: 2022-02-11 10:55:05
url: iproute2/route
categories:
  - Network
tags:
  - reprint
  - remix

---

## iproute2 > 路由表, routing table, ip route

## commands

```bash
ip route
# 简写, Abbreviations
# route: ro, r.
# show: list, sh, ls, l.

ip route ls tab all
```

### ip route

```bash
Usage: ip route { list | flush } SELECTOR
```

- := 表示声明并定义
- { xxx | xxx } 表示多选 - 必选
- [] 表示可选
- SPEC 应该是 specification 的缩写
- NH 应该是 next hop 的缩写
- PREFIX 就是地址加掩码的格式,比如 0.0.0.0/0
- PREFIX 有个 default 的特殊表示,等同于 0.0.0.0/0,也就是默认路由

### 路由

linux 系统路由表可以自定义从1－252个路由表,
操作系统维护了4个路由表:

- 0#表   系统保留表
- 253#表 defulte table 没特别指定的默认路由都放在该表
- 254#表 main table 没指明路由表的所有路由放在该表
- 255#表 locale table 保存本地接口地址,广播地址、NAT地址 由系统维护,用户不得更改

#### 数字与名字的关联

```bash
/etc/iproute2/rt_tables
```

此文件保存的是路由表序号和表名的对应关系, 可手动编辑

```bash
echo 200 John >> /etc/iproute2/rt_tables
```

### 查看路由

```bash

ip route show #显示主路由表信息
ip route | column -t

ip route list table table_number
ip route list table table_name

# 不带参数时显示main表
ip route list

# local表中存储的是内核自动生成本机路由和广播路由。
ip route list table local

# main 路由表
ip route list table main

# get 指定目的 IP/网段 的路由信息
ip route get 172.18.0.10
```

## 删除路由

```bash
ip r del default
ip r del 10.61.90.0/24
ip route del 192.168.0.0/24 via 172.16.15.253 dev eth0
```

## 添加路由, ip route add

路由表添加完毕即时生效

```bash
ip route add DESTINATION       [via NEXT_HOP]      [src SOURCE_ADDRESS]    [dev DEVICE]

ip route add default           via 192.168.50.4    src 192.168.50.169      dev ens18
ip route add 192.168.54.0/24   via 192.168.50.11   src 192.168.50.8        dev enp0s31f6
ip route add 192.168.0.0/24     via 172.16.15.253                           dev eth0
```

- DESTINATION
目标主机, 目标网络/掩码

- via NEXT_HOP
网关, 下一跳的 IP,  下一跳的路由器或主机的 IP

- src SOURCE_ADDRESS
当一个主机有多个网卡或者配置了多个 IP 的时候, 对于它产生的网络包, 可以在路由选择时设置源 IP 地址。  
ip route add 78.22.45.0/24 via 10.45.22.1 src 10.45.22.12  (发到 78.22.45.0/24 网段的网络包,下一跳的路由器 IP 是 10.45.22.1, 包的源IP地址设为 10.45.22.12) 。
要注意的是, src 选项只会影响该 host 上产生的网络包。如果是一个被路由的外来包,明显地它已经带有了一个源 IP 地址,这时候,src 参数的配置对它没有任何影响, 除非你使用 NAT 来改变它。

- dev DEVICE
网卡

路由表添加完毕即时生效,下面为实例
注: 各路由表中应当指明默认路由,尽量不回查路由表. 路由添加完毕,即可在路由规则中应用

```bash
ip route add default via 192.168.1.1 table 1        在一号表中添加默认路由为192.168.1.1
ip route add 192.168.0.0/24 via 192.168.1.2 table 1 在一号表中添加一条到192.168.0.0网段的路由为192.168.1.2
```

### 路由表示例

```r
Destination        Netmask            Gateway           Interface         Metric
0.0.0.0            0.0.0.0            192.168.123.254   192.168.123.88    1       #缺省路由,目的地址不在本路由表中的数据包,经过本机的 192.168.123.88 接口发到下一个路由器 192.168.123.254
127.0.0.0          255.0.0.0          127.0.0.1         127.0.0.1         1       #发给本机的网络包
192.168.123.0      255.255.255.0      192.168.123.68    192.168.123.68    1       #直连路由。目的地址为 192.168.123.0/24 的包发到本机 192.168.123.68 接口
192.168.123.88     255.255.255.255    127.0.0.1         127.0.0.1         1       #目的地址为 192.168.123.88的包是发给本机的包
192.168.123.255    255.255.255.255    192.168.123.88    192.168.123.88    1       #广播包的网段是 192.168.123.0/24,经过 192.168.123.88 接口发出去
224.0.0.0          224.0.0.0          192.168.123.88    192.168.123.88    1       #多播包,经过 192.168.123.88 接口发出去
255.255.255.255    255.255.255.255    192.168.123.68    192.168.123.68    1       #全网广播包

Default Gateway: 192.168.123.254
```

### 路由表 ip route|column -t

```r
default          via  192.168.50.1  dev    wlp2s0  proto  dhcp  src  192.168.50.116  metric  1024
192.168.50.0/24  dev  wlp2s0        proto  kernel  scope  link  src  192.168.50.116          
192.168.50.1     dev  wlp2s0        proto  dhcp    scope  link  src  192.168.50.116  metric  1024
```

### default

default route (for all addresses), 默认路由, 相当于目标地址 0.0.0.0

### via  192.168.50.1 dev wlp2s0

via the local gateway 192.168.1.1 that can be reached on device wlp2s0,
via the address of nexthop router,
dev the output device name

### proto字段

routing protocol identifier of this route.
proto字段的定义在内核中并没有实质的意义,只是一个显示字段

UNSPEC表示未指定
REDIRECT已经不再使用
KERNEL 内核自身添加的路由
BOOT为在启动过程中安装的路由

### src

src ADDRESS the source address to prefer when sending to the destinations covered by the route prefix.

### scope

scope of the destinations covered by the route prefix.

### metric

设置路由跳数。路由距离,到达指定网络所需的中转数。

metric Metric
为路由指定所需跃点数的整数值 (范围是 1 ~ 9999) ,它用来在路由表里的多个路由中选择与转发包中的目标地址最为匹配的路由。所选的路由具有最少的跃点数。跃点数能够反映跃点的数量、路径的速度、路径可靠性、路径吞吐量以及管理属性。
路由的metric

路由表中含有由交换软件用以选择最佳路径的信息。但是路由表是怎样建立的呢？它们包含信息的本质是什么？路由算法怎样根据这些信息决定哪条路径更好呢？

路由算法使用了许多不同的metric以确定最佳路径。复杂的路由算法可以基于多个metric选择路由,并把它们结合成一个复合的metric。常用的metric如下:

路径长度
可靠性
延迟
带宽
负载
通信代价

路径长度是最常用的路由metric。一些路由协议允许网管给每个网络链接人工赋以代价值,这种情况下,路由长度是所经过各个链接的代价总和。其它路由协议定义了跳数,即分组在从源到目的的路途中必须经过的网络产品,如路由器的个数。

可靠性,在路由算法中指网络链接的可依赖性 (通常以位误率描述) ,有些网络链接可能比其它的失效更多,网路失效后,一些网络链接可能比其它的更易或更快修复。任何可靠性因素都可以在给可靠率赋值时计算在内,通常是由网管给网络链接赋以metric值。

路由延迟指分组从源通过网络到达目的所花时间。很多因素影响到延迟,包括中间的网络链接的带宽、经过的每个路由器的端口队列、所有中间网络链接的拥塞程度以及物理距离。因为延迟是多个重要变量的混合体,它是个比较常用且有效的metric。

带宽指链接可用的流通容量。在其它所有条件都相等时,10Mbps的以太网链接比64kbps的专线更可取。虽然带宽是链接可获得的最大吞吐量,但是通过具有较大带宽的链接做路由不一定比经过较慢链接路由更好。例如,如果一条快速链路很忙,分组到达目的所花时间可能要更长。

负载指网络资源,如路由器的繁忙程度。负载可以用很多方面计算,包括CPU使用情况和每秒处理分组数。持续地监视这些参数本身也是很耗费资源的。

通信代价是另一种重要的metric,尤其是有一些公司可能关系运作费用甚于性能。即使线路延迟可能较长,他们也宁愿通过自己的线路发送数据而不采用昂贵的公用线路。

### 路由条目的意义

路由的设计远比一般的理解要复杂的多。典型的路由条目包括了源IP,目的IP,网关IP,scope,dev和type六个要素。

网关IP就是在配置路由的时候指定的via后面的地址,在路由表中叫Gateway,这是说明这条路由的下一跳是这个IP地址。这个IP地址之所以出现,是因为目的地址不是当前自己出口可以直接可达的,需要经过网关路由到下个网络才能投递。

也就是因此,如果这个via域配置为0.0.0.0,或者是用*表示,总之是代表一定的通配,那么就意味着这个路由的目的地和自己在一个二层的网络,到达那个目的地并不需要网关转发,只需要配置MAC地址从端口上发出去即可。这个发送出去的过程显然是去查ARP表,通过IP地址查询目标的MAC地址。很容易理解网关在路有条目中的意义,如果到达一个目标地址是需要通过网关转发出去的,via就要指定网关。大部分的个人局域网中,都会指定一个默认网关,目的IP填写了0.0.0.0,也就是所有的目的地址 (通常使用命令的时候,这个词语叫做default) ,via后面填写网关地址。这样在其他的更精确的路由条目都不命中的情况下,就一定会命中这个默认路由条目。因为这个条目的目的IP设置是通配。使用ip命令设置这样的默认路由是例如dpip route add default via 10.0.0.1。

假设一个路由条目指定了gateway,那么决策还需要知道这个gateway到底是从哪个网口发出去可达的,这就是dev的作用。熙然到一个gateway必然要从一个设备出去,而其他的地方并不能指定这个gateway和设备的对应关系,于是就在路由表这里就指定了。通过dev可以到达该gateway。

如果gateway不指定,也就是该路由在同一个二层,那么仍然需要指定dev,因为即使是发送出去,也需要查从哪里发送出去。因为在收到一个数据包的时候,进入系统的时候目的IP不是自己就需要根据目的IP来查找路由,这个路由会决定这个目的IP是要转发给哪个端口 (通常通过目的IP和网关IP和dev来决定) 。

Dev相对于对gateway的一个更小的约束。同样起到约束作用的还有scope。Scope是一个更小程度的约束,指明了该路由在什么场景下才有效。也是用于约束目的地址的。例如不指定网关的二层路由,通常对应的scope类型是scope link。scope link的意义就是说明在同一个二层。这个意义与网关不指定的效果是呼应的。

有四种scope,global是在任何的场景下都有效,link是在链路上才有效,这个链路是指同一个端口,也就是说接收和发送都是走的同一个端口的时候,这条路由才会生效 (也就是说在同一个二层) 。Global则可以转发,例如从一个端口收到的包,可以查询global的路由条目,如果目的地址在另外一个网卡,那么该路由条目可以匹配转发的要求,进行路由转发。Link的scope路由条目是不会转发任何匹配的数据包到其他的硬件网口的。还有就是host,host表示这是一条本地路由,典型的是回环端口,loopback设备使用这种路由条目,该路由条目比link类型的还要严格,约定了都是本机内部的转发,不可能转发到外部。Site则是ipv6专用的路由scope。

源IP是一个路由条目的重要组成部分,这个源IP的意义在于一个补充作用。匹配还是根据目的IP进行匹配,但是由于在查找路由条目的时候很可能源地址还没有指定。典型的就是没有进行bind的发送情况,通常是随机选择端口和按照一定的规则源地址。这个一定的规则就是在这里的路由条目的src域可以影响。也就是如果进程没有bind一个源地址,将会使用这里src域里面的源地址作为数据包的源地址进行发送。但是如果进程提前bind了,命中了这个条目,就仍然会使用进程bind的源地址作为数据包的源地址。所以说这里的src只是一个建议的作用。

### type: 路由类型

unicast ,local, broadcast ,multicast , throw,unreachable ,prohibit , blackhole, nat
    类型        说明
    unicast        该类型路由描述到目的地址的真实路径
    local        目的地址被分配给本机,数据包通过回环被投递到本地
    broadcast    目的地址是广播地址,数据包作为链路广播发送。
    multicast    使用多播路由。在普通的路由表中,这种路由并不存在。
    throw        如果选择了这种路由,就会认为没有发现路由,在这个表中的查询就会被终止,并产生ICMP信息net unreachable。本地发送者会返回ENETUNREACH错误。
    unreachable    目的地址是不可达的。如果发过去的数据包都被丢弃并且收到ICMP信息host unreachable,目的地址就会被标记为不可达。在这种情况下,本地发送者将返回EHOSTUNREACH错误。
    prohibit    路由是不可达的。发过去的数据包都被丢弃,而且产生ICMP信息communication administratively prohibited 。本地发送者会返回EACCESS错误。
    blackhole    目的地址不可达,而且发过去的数据包都被丢弃。在这种情况下,本地发送者将返回EINVAL错误。
    nat            特定的NAT路由。目标地址属于哑地址 (或者称为外部地址) ,在转发前需要进行地址转换。

## # ip route

```r
default via 115.238.122.129 dev eth1 
115.238.122.128/25 dev eth1  proto kernel  scope link  src 115.238.122.163 
192.168.0.160/24 dev dpdk0.kni  proto kernel  scope link  src 192.168.0.163 
192.168.1.160/24 dev dpdk1.kni  proto kernel  scope link  src 192.168.1.163
```

举一个例子,从本机发出的目的地址是192.168.0.160/24网段的数据包将匹配第三条路由,如果在查询路由表之前没有设置bind,这个查询路由表的操作就会把数据包的源地址设置为192.168.0.163 。如果设置了bind,就保留bind的结果 (所以你可以很容易的在Linux的主机上伪造原地址发送数据) 。

src域在处理转发的数据包的时候,由于数据包是从外部收到的,外部进来的数据包也会查找路由表,也能命中同一个路由条目。但是由于外部进来的数据包已经有了明确的源地址,这里的src源地址建议就不会起作用了。所以关键就是理解src只是一个源地址的一个建议的作用即可。

对于路由表,是一个匹配的过程。一个数据包去查找匹配自己最能够匹配哪条路由表,然后就使用该路由条目指定的路由方法进行路由转发。匹配的方法就是鼎鼎大名的LPM,简单的说,就是匹配最匹配的那一个。

所以整个过程可以看到,核心的是对目的地址的限制,其他的域都是用于辅助这个限制,甚至可以辅助决策。

我们看一个虚拟机里的默认路由表:

root@ubuntu:~/# ip route show

default via 192.168.142.2 dev ens33 proto static metric 100

169.254.0.0/16 dev ens33 scope link metric 1000

192.168.142.0/24 dev ens33 proto kernel scope link src 192.168.142.135 metric 100

跳过default,后面两条的第一个域都是目的地址,确切的说,这里指定的是目的网段,然后约束了设备,也就是enc33,这个路由条目是link scope的,也就是说当主机收到目标地址是169.254.0.0/16 这个网段的时候,通过ens33这个设备将包转发出去。

虽然理论上是如此,但是实际上,例如在linux中,这个dev ens33是没有在路由中起到任何作用的,也就是说你收到改了enc33的名字,而不改路由表,那这个路由表项一样命中,从改名后的网口发送出去。所以dev的这个限制相当于不存在,也就是只是一个命名的作用。但是并不确定在其他的实现中是否有限制的意义。

Default路由本质上就是目标地址填了0.0.0.0的路由。Default路由有两种添加方式,一种是约束网关地址,另外一种是约束源IP。因为要添加到网关地址的默认路由,是需要在添加的时候发一个arp请求到网络上,看这个网关的地址是否存在于二层的,但是这个arp请求也是需要首先经过路由的。也就是一个鸡生蛋,蛋生鸡的问题。所以一个空的路由表是不能直接配置默认路由是一个网关的。但是明明网关确实是和当前的主机在同一个网段的。

如果要配置默认网关,首先需要先让这个网络通。这个通的方法一个是配一个link scope的路由,也就是目的地址是该网段的发包,都可以匹配这个路由。因为是link scope的,所有的请求都会走二层的路由表,这就解决了arp不能到达网关的问题。Link scope的特点是所有的数据请求走二层arp,而不是走三层路由。所以在配置了这条路由之后,再配置网关就可以了。

但是还有一个思路是使用源地址约束,我们要的只是这个查询能命中一个可以出去的路由,当我们使用源地址约束,不指定目标地址,也就是源地址是自己设备的IP的地址的包全部走link scope,同样也可以匹配,由于是link scope,也就可以触发arp请求了。

所以我们看到,整个过程的关键在于区分同二层和三层转发。Link scope的作用是用在二层转发,命中该路由条目的可以触发arp查找,但是如果是网关式的,就是一个三层转发,虽然也会触发arp查找,但是目标MAC地址永远是网关的地址,这样下一跳就锁死了。

但是这里有一个问题是如果先添加了link scope的路由条目,然后又添加了gateway的路由,这个时候再把link scope的路由条目删除,那么gateway的路由条目仍然存在并且生效,这个时候,所有的转发都会匹配这个gateway的路由条目,包括本来应该走二层转发的数据包。也就是说,原本应该在同一个二层传输走arp的数据包,在这种情况下,也会直接走网关,网关回复一个icmp redirect,但是网关仍然会把这个数据包转发到同一个二层的目标地址。

理论上,收到icmp redirect的主机应当更新自己的arp表,但是并不会更新路由表,而arp表是要先经过路由表查询的,所以这个icmp redirect相当于没有意义。Arp表里面即使是有了IP到MAC的映射关系,但是由于路由没有命中link scope,所以永远不会查询ARP表。

另外linux下的路由条目还会有一个proto的域,一般有proto kernel和proto dhcp两种。Proto表明的是这个路由条目是由谁添加,例如给一个linux设备添加一个IP的时候会自动添加一条有这个源IP约束的Link scope的路由。前面说了,也正是有了这条路由才能够使得配置网关的路由条目可以进行。这个内核自动添加的路由就是proto kernel了。

需要理解的是,路由表和网络设备是两个实体,路由表在决策的时候,由路由表看到的网络设备是独立于路由表存在的。他们是并行的关系,先要查询了路由表,找到满足路由表的路由条目,才有可能按照条目约定的路由路径去找到对应的设备。路由过程并不是发生在设备逻辑的内部,而是外部。所以实际上给设备添加了一个IP地址的时候,同时生成的路由条目实际上是两个操作被在上层进行了组合。技术上,完全可以分别的添加IP地址和路由条目,上面也说了这个添加的路由条目可以被删除,然后再次添加回去。

## 策略路由  (Policy Routing)

### 查看策略数据库

要查看策略数据库的内容,可以使用ip rule show命令,或者可以使用ip rule ls。如下是命令执行后所得到的输出结果,在这些数据中,可以看到系统的三条默认规则,而这三条规则默认分别对应于local、mail及default三个路由表。

```bash
    ip rule show
```

```r
0: from all lookup local  
32766: from all lookup main  
32767: from all lookup default 
```

### IPTABLES MARK机制

MARK是IPTABLES的一种规则目标,它用于给匹配了相应规则的数据包设置标签。它只能用于mangle表中。然而,标签并不是设置于数据包内容中,而是设置在内核中数据包的载体上。如果需要在数据包内容中设置标签,可以使用TOS规则目标,它可以修改IP数据包头的TOS值。

MARK是一个32位整数值, MARK目标可以使用3种方法来设置mark值:

--set-mark value: 直接设置mark值为value
--and-mark value: 将mark值与value做位与运算后设置为新mark值
--or-mark value: 将mark值与value做位或运算后设置为新mark值
比如,将从网络接口tun0进入的、目标端口为5222的TCP数据包设置mark值为1:

```bash
    iptables -t mangle -A PREROUTING -j MARK --set-mark 1 -i tun0 -p tcp --dport 5222
```

设置的mark值可用来设定策略路由。

比如,我们想把mark值为1的数据包交由网关192.168.0.1转发。

首先,确定一张空路由表,这里选定300:

ip route show table 300
在表中添加路由条目:

ip route add default via 192.168.0.1 table 300
查看,当前路由规则:

ip rule list
0:         from all lookup local
32766:     from all lookup main
32767:     from all lookup default

### 策略路由, 为mark值为1的数据包指定路由表策略

```bash
    ip rule add fwmark 0x1 table 300
```

再查看当前策略,确定已经生效:

```r
ip rule list

0:         from all lookup local
32765:     from all fwmark 0x1 lookup 300
32766:     from all lookup main
32767:     from all lookup default
```

通过这种方法,可以使用IPTABLES根据匹配规则设置mark, 再由路由模块根据mark值进行路由决策,从而实现复杂的策略路由。

### Tos

IP包头的TOS: type of service
ip报文头的type of sevice字段长度为1个字节,其中高3 bit用来标记优先级,所以有0-7共8个ip preference级别。type of service字段的中间4bit为tos子字段,最低1bit未用但必须置0。4bit的tos分别代表: 最小时延、最大吞吐量、最小费用和最高可靠性。4bit中只能将其中1bit置1。如果所有4bit均为0,那么就表示是普通服务。

### 添加规则

fwmark

将fwmark(forward mark,转发标记)作为匹配条件时,必须搭配Netfilter一起使用, 这看起来很麻烦, 却是最灵活的匹配条件。例如,某公司对外有三条ADSL,我们希望所有HTTP 协议经由第一条ADSL ,SMTP及POP3经由第二条ADSL,其余流量则经由第三条ADSL。可以使用如下的命令组合来达到这样的目的:
首先使用Netfilter的managle机制针对特定的数据包设置MARK值,在此将HTTP数据包的MARK值设置为1,SMTP及POP3数据包的MARK值设置为2,其余数据包则设置MARK值为3。接着,再根据fwmark条件来判断数据包的MARK值,如果MARK值为1,则参考路由表1将数据包送出；MAKR值为2时,则参考路由表2将数据包送出；最后,MARK值为3的数据包则参考路由表3送出。

以上示例只是一个概念而已,如果真要完整体现出这个示例的所有功能,还需要注意许多细节,稍后将使用详细的示例讲解这部分内容,在此只要首先了解fwmark与Netfilter结合使用的概念即可。

```r
iptables -t mangle -A FORWARD -i eth3 -p tcp --dport 80 -j MARK --set-mark 1  
iptables -t mangle -A FORWARD -i eth3 -p tcp --dport 25 -j MARK --set-mark 2  
iptables -t mangle -A FORWARD -i eth3 -p tcp --dport 110 -j MARK --set-mark 2  
iptables -t mangle -A FORWARD -i eth3 -j MARK --set-mark 3  
ip rule add fwmark 1 table 1  
ip rule add fwmark 2 table 2  
ip rule add fwmark 3 table 3
```

### ip rule

```bash
# 使用iptables给相应的数据打上标记
iptables -A PREROUTING -t mangle -i eth0 -s 192.168.0.1 -192.168.0.100 -j MARK --set-mark 3
# fwmark 3是标记,table 3 是路由表3 上边。 意思就是凡事标记了 3 的数据使用table3 路由表
ip rule add fwmark 3  table 3
```

### 默认规则

```bash
ip rule [list]
```

```bash
# ip rule
0:    from all lookup local 
32766:    from all lookup main
32767:    from all lookup default
```

上面列出了规则的优先顺序。ip route命令默认显示的就是main表

高级路由重点之一路由规则 ip rule
进行路由时,根据路由规则来进行匹配,按优先级 (pref) 从低到高匹配,直到找到合适的规则.所以在应用中配置默认路由是必要的..

ip rule show 显示路由规则

路由规则的添加
ip rule add from 192.168.1.10/32 table 1 pref 100

0: from all lookup local
  
32766: from all lookup main
  
32767: from all lookup default
  
上面列出了规则的优先顺序。ip route命令默认显示的就是main表。ip route show table all显示所有规则中的表

```bash
ip r
ip route show
ip route list
ip route show table all
ip route show table table0

ip route add DESTINATION [via NEXT_HOP] [src SOURCE_ADDRESS] [dev DEVICE]
ip route add 192.168.1.0/24 via 172.16.1.106
如果网卡配置有多个ip时可以指定数据包从哪个网卡出去

# ip route add 192.168.1.0/24 src 172.16.1.106 dev eth1

 ip route del 192.168.0.1/24
```

ip rule 命令:
  
Usage: ip rule [ list | add | del ] SELECTOR ACTION  (add 添加；del 删除； llist 列表)
  
SELECTOR := [ from PREFIX 数据包源地址] [ to PREFIX 数据包目的地址] [ tos TOS 服务类型][ dev STRING 物理接口] [ pref NUMBER ] [fwmark MARK iptables 标签]
  
ACTION := [ table TABLE_ID 指定所使用的路由表] [ nat ADDRESS 网络地址转换][ prohibit 丢弃该表| reject 拒绝该包| unreachable 丢弃该包]
  
[ flowid CLASSID ]
  
TABLE_ID := [ local | main | default | new | NUMBER ]
  
例子:

ip rule add from 192.203.80/24 table inr.ruhep prio 220 通过路由表 inr.ruhep 路由来自源地址为192.203.80/24的数据包
  
ip rule add from 193.233.7.83 nat 192.203.80.144 table 1 prio 320 把源地址为193.233.7.83的数据报的源地址转换为192.203.80.144,并通过表1进行路由
  
————————————————
  
版权声明: 本文为CSDN博主「zqixiao_09」的原创文章,遵循 CC 4.0 BY-SA 版权协议,转载请附上原文出处链接及本声明。
  
原文链接: <https://blog.csdn.net/zqixiao_09/article/details/53327074>

路由表是指路由器或者其他互联网网络设备上存储的一张路由信息表,该表中存有到达特定网络终端的路径,在某些情况下,还有一些与这些路径相关的度量。

路由表中只存储网络信息而不是主机信息,这样可以大大简化路由表。
  
路由表中包含一系列被称为路由的规则,可用于判断网络流量的导向目的地。

Let's interpret the output above by starting with the second line. This line says that packets sent to any IP address within the subnetwork 192.168.1.0/24 must be sent through the network interface wlan0 (a wireless network ínterface) with 192.168.1.100 as the source IP address, which in this case is the IP address assigned to wlan0 via DHCP. The other parts are not so interesting: proto kernel means this entry in the routing table was created by the kernel during autoconfiguration, while scope link means the destination IP addresses within 192.168.1.0/24 are valid only on the device wlan0.

The first line says that the default route for any packet (i.e., the route which is taken by a packet when no other route applies) is through the network device wlan0 via the default gateway (the router) which has the IP address 192.168.1.1. Figure 1 shows this network scheme.

The first column is the `<Destination>` subnet with the "default" being a wildcard for everything else. The "via" fragment points to the `<Gateway>` however when it is missing it indicates that that network is connected directly and instead it describes a source address.

The `<Metric>` column translates to the number of hops required to reach the destination and is used to determine which route shall be preferred when there are more than one route available for a specific destination. Since it reassembles the concept of distance the lower it's value is the better.

The `<Metric>` value can be set manually however when NetworkManager creates a connection the following defaults are applied:

Ethernet is preferred over WiFi
  
WiFi is preferred over WWAN

<https://diego.assencio.com/?index=d71346b8737ee449bb09496784c9b344>

### deprecated net-tools command

查看 Linux 内核路由表
  
使用下面的 route 命令可以查看 Linux 内核路由表。
  
route
  
route -n
  
-c 显示更多信息
  
-n 不解析名字
  
-v 显示详细的处理信息
  
-F 显示发送信息
  
-C 显示路由缓存
  
-f 清除所有网关入口的路由表。
  
-p 与 add 命令一起使用时使路由具有永久性。

Destination Gateway Genmask Flags Metric Ref Use Iface
  
192.168.0.0 * 255.255.255.0 U 0 0 0 eth0
  
169.254.0.0 * 255.255.0.0 U 0 0 0 eth0
  
default 192.168.0.1 0.0.0.0 UG 0 0 0 eth0
  
route 命令的输出项说明

输出项说明
  
Destination 目标网段或者主机
  
Gateway 网关地址,"*" 表示目标是本主机所属的网络,不需要路由
  
Genmask 网络掩码
  
Flags 标记。一些可能的标记如下:

U — 路由是活动的
  
H — 目标是一个主机
  
G — 路由指向网关
  
R — 恢复动态路由产生的表项
  
D — 由路由的后台程序动态地安装
  
M — 由路由的后台程序修改
  
! — 拒绝路由

Metric 路由距离,到达指定网络所需的中转数 (linux 内核中没有使用)
  
Ref 路由项引用次数 (linux 内核中没有使用)
  
Use 此路由项被路由软件查找的次数
  
Iface 该路由表项对应的输出接口

## 3 种路由类型

### 主机路由

主机路由是路由选择表中指向单个IP地址或主机名的路由记录。主机路由的Flags字段为H。例如,在下面的示例中,本地主机通过IP地址192.168.1.1的路由器到达IP地址为10.0.0.10的主机。

Destination Gateway Genmask Flags Metric Ref Use Iface
  
---- --- --- -- -- - - --
  
10.0.0.10 192.168.1.1 255.255.255.255 UH 0 0 0 eth0

网络路由
  
网络路由是代表主机可以到达的网络。网络路由的Flags字段为N。例如,在下面的示例中,本地主机将发送到网络192.19.12的数据包转发到IP地址为192.168.1.1的路由器。

Destination Gateway Genmask Flags Metric Ref Use Iface
  
---- --- --- -- -- - - --
  
192.19.12 192.168.1.1 255.255.255.0 UN 0 0 0 eth0
  
默认路由
  
当主机不能在路由表中查找到目标主机的IP地址或网络路由时,数据包就被发送到默认路由 (默认网关) 上。默认路由的Flags字段为G。例如,在下面的示例中,默认路由是IP地址为192.168.1.1的路由器。

Destination Gateway Genmask Flags Metric Ref Use Iface
  
---- --- --- -- -- - - --
  
default 192.168.1.1 0.0.0.0 UG 0 0 0 eth0

设置包转发
  
在 CentOS 中默认的内核配置已经包含了路由功能,但默认并没有在系统启动时启用此功能。开启 Linux的路由功能可以通过调整内核的网络参数来实现。要配置和调整内核参数可以使用 sysctl 命令。例如: 要开启 Linux内核的数据包转发功能可以使用如下的命令。

```bash
sysctl -w net.ipv4.ip_forward=1
```

这样设置之后,当前系统就能实现包转发,但下次启动计算机时将失效。为了使在下次启动计算机时仍然有效,需要将下面的行写入配置文件/etc/sysctl.conf。

vi /etc/sysctl.conf

net.ipv4.ip_forward = 1
  
用户还可以使用如下的命令查看当前系统是否支持包转发。

sysctl net.ipv4.ip_forward

ip rule add from 10.1.1.0/24 table TR1
  
ip rule add iff eth0 table RT2

如上,第一条命令创建了基于源地址路由的一条策略,这个策略使用了RT1这个路由表,第二条命令创建了基于数据包入口的一个策略,这个策略使用了RT2这个路由表。当被指定的路由表不存在时,相应的路由表将被创建。

第二步就是遍历这个路由表的fn_zone,遍历是从最长前缀 (子网掩码最长) 的fn_zone开始的,直到找到或出错为止。因为最长前缀才是最匹配的。假设有如下一个路由表:

dst nexthop dev

10.1.0.0/16 10.1.1.1 eth0

10.1.0.0/24 10.1.0.1 eth1

它会先找到第二条路由,然后选择10.1.0.1作为下一跳地址。但是,如果由第二步定位到的子网(fib_node)有多个路由,如下:

dst nexthop dev

10.1.0.0/24 10.1.0.1 eth1

10.1.0.0/24 10.1.0.2 eth1

到达同一个子网有两个可选的路由,仅凭目的子网无法确定,这时,它就需要更多的信息来确定路由的选择了,这就是用于查找路由的键值 (structflowi) 还包括其它信息 (如TOS) 的原因。这样,它才能定位到对应一个路由的一个fib_alias实例。而它指向的fib_info就是路由所需的信息了。
  
最后一步,如果内核被编译成支持多路径(multipath)路由,则fib_info中有多个fin_nh,这样,它还要从这个fib_nh数组中选出最合适的一个fib_nh,作为下一跳路由。

三、路由的插入与删除

路由表的插入与删除可以看看是路由查找的一个应用,插入与删除的过程本身也包含一个查找的过程,这两个操作都需要检查被插入或被删除的路由表项是否存在,插入一个已经存在的路由表项要做特殊的处理,而删除一个不存在的路由表项当然会出错。

下面看一个路由表插入的例子:

ip route add 10.0.1.0/24 nexthop via 10.0.1.1 weight 1

nexthop via 10.0.1.2 weight 2

table RT3

这个命令在内核中建立一条新的路由。它首先查找路由表RT3中的子网掩码长为24的fn_zone,如果找不到,则创建一个fn_zone。接着,继续查找子网为10.0.1的fib_node,同样,如果不存在,创建一个fib_node。然后它会在新建一个fib_info结构,这个结构包含2个fib_nh结构的数组 (因为有两个nexthop) ,并根据用户空间传递过来的信息初始化这个结构,最后内核再创建一个fib_alias结构 (如果先前已经存在,则出错) ,并用fib_nh来创始化相应的域,最后将自己链入fib_node的链中,这样就完成了路由的插入操作。

路由的删除操作是插入操作的逆过程,它包含一系列的查找与内存的释放操作,过程比较简单,这里就不再赘述了。

四、策略路由的一个简单应用

Linux系统在策略路由开启的时候将使用多个路由表,它不同于其它某些系统,在所有情况下都只使用单个路由表。虽然使用单个路由表也可以实现策略路由,但是如本文之前所提到的,使用多个路由表可以得到更好的性能,特别在一个大型的路由系统中。下面只通过简单的情况说明Linux下策略路由的应用。
  
如图2,有如下一个应用需求,其中网关服务器上有三个网络接口。接口1的IP为172.16.100.1,子网掩码为255.255.255.0,网关gw1为a.b.c.d,172.16.100.0/24这个网段的主机可以通过这个网关上网；接口2的IP是172.16.10.1,子网掩码同接口一,网关gw2为e.f.g.h,172.16.10.0/24这个网段的主机可以通过这个网关上网；接口0的IP为192.168.1.1,这个网段的主机由于网络带宽的需求需要通过e.f.g.h这个更快的网关路由出去。

图 2

步骤一: 设置各个网络接口的IP, 和默认网关:

ip addr add 172.16.100.1/24 dev eth1
  
ip route add default via a.b.c.d dev eth1

其它接口IP的设置和第一个接口一样,这时,如果没有其它设置,则所有的数据通过这个默认网关路由出去。

步骤二: 使子网172.16.10.0/24可以通过gw2路由出去

```bash
       ip route add 172.16.10.0/24 via e.f.g.h dev eth2
```

步骤三: 添加一个路由表

```bash
       echo   "250 HS_RT" >> /etc/iproute2/rt_tables
```

步骤四: 使用策略路由使192.168.1.0/24网段的主机可以通过e.f.g.h这个网关上网

```bash
       ip rule add from 192.168.1.0/24 dev eth0 table HS_RT pref 32765
       ip route add default via e.f.g.h dev eth2
       iptables –t nat –A POSTROUTING –s 192.168.1.0/24 –j MASQUERADE
```

步骤五: 刷新路由cache,使新的路由表生效

ip route flush cache
  
这样就可以实现了以上要求的策略路由了,并且可以通过traceroute工具来检测上面的设置是否能正常工作。

===============================================================================

linux双网卡怎么设置我就不说了,我这里说的是linux双网卡的流量问题...
  
可能这个问题很偏们..你们也许用不上..我还是要说..

问题描述,一个linux主机,上面两个网卡..:)

route -n的输出是这样的.

Destination Gateway Genmask Flags Metric Ref Use Iface

61.132.43.128 0.0.0.0 255.255.255.192 U 0 0 0 eth1

127.0.0.0 0.0.0.0 255.0.0.0 U 0 0 0 lo

0.0.0.0 61.132.43.134 0.0.0.0 UG 0 0 0 eth0

这里解释一下...第一行是说,你要访问61.132.43.128这个网段,掩码是255.255.255.192的话..从e
  
th1这个网卡出去..
  
第二行是关于本机的,访问自己从lo这个虚拟的本地网卡走..
  
第三行是说你要去任何地方的话..从网关61.132.43.134出去.并且网卡是eth0

到这里我们看到了..我们除了去61.132.43.128这个网络是从eth1走以外..去其他地方都是从eth0�
  
�...

这样是不是很浪费了双网卡??没错..是很浪费..因为不论你用那种监测工具查看流量..都是eth0有
  
..而其他网卡没有...天哪...为此我是煞费苦心..甚至怀疑网卡是不是坏了..因为在win2k上这种�
  
虑槭遣豢赡芊⑸�..:)

那我们怎么解决这个问题呢?有人也许会说给个不同网关让另一块网卡用其他网关不就可以..是这�
  
鍪强梢�..但是问题是我的ip都是在同一个网段..那来的不同网关.?网关就一个61.132.43.134...

还好linux系统给我们提供了一个很好的路由套件-iproute2

我们来熟悉一下..iproute2由几个常见的命令..
  
ip ro ls ip就是ip命令啦,ro就是route的所写,ls是list的缩写...
  
整个命令就是列出系统的路由表..这个可和route
  
-n的效果差不多..但是更为清楚系统的route是如何的..

我们来看看吧:

[root@localhost root]# ip ro ls

61.132.43.128/26 dev eth1 proto kernel scope link src 61.132.43.136

127.0.0.0/8 dev lo scope link

default via 61.132.43.134 dev eth0

是不是一样呢?由几个地方不同..第一条多了一个src,增加了对源数据包的选择,而且子网掩码也变
  
成/26的形式..(参考ip地址的书籍)
  
最后一个仍然是网关...

现在我们只要稍稍动手把从61.132.43.136出来的流量让他不要从eth0出去..然他走eth1
  
我们加一条自定义的路由表

ip ro add default via 61.132.43.134 table 200

这里只是加了一条默认路由到一个自定义的路由表200中,最大数值是255,但是你不要用255,因为那
  
是系统默认用了..你用200以下就可以.
  
具体的路由表在/etc/iproute2/rt_tables中

查看刚才建立的路由表可以用ip ro ls table 200

[root@localhost root]# ip ro ls table 200

default via 61.132.43.134 dev eth1

看到了吗?虽然我没有指定dev是什么.但是系统自动分配了一个eth1给这个路由表,因为eth0已经用
  
在主路由表中了..
  
这也说明了,的确不能在同一个路由表中由相同的网关..虽然可以设置,但是具体没什么作用.

然后我们要用一个规则把,匹配的数据包引导到刚刚建立的路由表中..:)

ip ru add from 61.132.43.136 table 200

这里ru是rule的缩写.from是一个匹配的动作.就是所源地址是61.132.43.136的包..请走自定义路�
  
杀�的设置..:)

查看一下

[root@localhost root]# ip ru ls

0: from all lookup local

32765: from 61.132.43.136 lookup 200

32766: from all lookup main

32767: from all lookup 253

ip ro flush cache

linux 下 双网卡 同网段,可以把IP_FORWARD 打开,这样一个网卡down掉数据会从另外一个网卡出去

linux路由表
  
2010年08月18日 星期三 17:44
  
宏CONFIG_IP_MULTIPLE_TABLES表示路由策略,当定义了该宏,也即意味着内核配置了"路由策略"。产生的最大的不同就是内核可以使用多达256张FIB。其实,这256张FIB在内核中的表示是一个全局数组:

struct fib_table *myfib_tables[RT_TABLE_MAX+1];
  
而宏RT_TABLE_MAX定义如下:

enum rt_class_t

{

RT_TABLE_UNSPEC=0,

RT_TABLE_DEFAULT=253,

RT_TABLE_MAIN=254,

RT_TABLE_LOCAL=255,

__RT_TABLE_MAX

};

define RT_TABLE_MAX (__RT_TABLE_MAX - 1)

我们可以看到,虽然这张表多达256项,但枚举类型rt_class_t给出的表示最常用的也就三项,在系统初始化时,由内核配置生成的路由表只有RT_TABLE_MAIN,RT_TABLE_LOCAL两张。

main表中存放的是路由类型为RTN_UNICAST的所有路由项,即网关或直接连接的路由。在myfib_add_ifaddr函数中是这样添加main表项的: 对于某个网络设备接口的一个IP地址,如果目的地址的网络号不是零网络 (网络号与子网号全为零) ,并且它是primary地址,同时,它不是D类地址 (网络号与子网号占32位) 。最后一个条件是: 它不是一个环回地址(device上有flagIFF_LOOPBACK) 。那么,就添加为main表项,如果是环回地址,则添加为local表的一个表项。

在我们的系统中,有两个已开启的网络设备接口eth0和lo,eth0上配置的primaryIP地址是172.16.48.2,所以,相应的,main表中就只有一项。为main表添加路由项的时候,该路由项的目的地址是子网内的所有主机 (把主机号部分字节清零) ,而对应于lo,在local表中也有一项,其类型为RTN_LOCAL(注: 前一篇文章中的local表的hash8中的路由项表述有误,类型应该是RTN_LOCAL,而不是RTN_BORADCAST)。

而其它的路由项全部归入local表,主要是广播路由项和本地路由项。在我们的系统环境下,local表共有7项,每个网络设备接口占三项。分别是本地地址 (源跟目的地址一致) ,子网广播地址 (主机号全为1),子网广播地址 (主机号为零)。再加上一个lo的RTN_LOCAL项。

现在我们再来看myfib_add_ifaddr函数的路由添加策略。对于一个传入的ip地址 (结构structin_ifaddr表示) ,如果它是secondary地址,首先要确保同一个网络设备接口上存在一个跟其同类型的primary地址(网络号与子网号完全一致) ,因为,路由项的信息中的源地址全是primary的,secondary地址其实没有实际使用,它不会在路由表中产生路由项。然后,向local表添加一项目的地址是它本身的,类型为RTN_LOCAL的路由项；如果该ip地址结构中存在广播地址,并且不是受限广播地址(255.255.255.255),那么向local表添加一个广播路由项；然后,对符合加入main表的条件进行判断,如果符合,除了加入main表,最后,如果不是D类地址,还要加入两个广播地址 (其实,已经跟前面有重叠,很多情况下不会实际触发加入的动作,只要记住,一个ip地址项对应最多有两个广播地址就可以了) 。

多路由表 (multiple Routing Tables)

传统的路由算法是仅使用一张路由表的。但是在有些情形底下,我们是需要使用多路由表的。例如一个子网通过一个路由器与外界相连,路由器与外界有两条线路相连,其中一条的速度比较快,一条的速度比较慢。对于子网内的大多数用户来说对速度并没有特殊的要求,所以可以让他们用比较慢的路由；但是子网内有一些特殊的用户却是对速度的要求比较苛刻,所以他们需要使用速度比较快的路由。如果使用一张路由表上述要求是无法实现的,而如果根据源地址或其它参数,对不同的用户使用不同的路由表,这样就可以大大提高路由器的性能。

规则 (rule)

规则是策略性的关键性的新的概念。我们可以用自然语言这样描述规则,例如我门可以指定这样的规则:

规则一: "所有来自192.16.152.24的IP包,使用路由表10, 本规则的优先级别是1500"

规则二: "所有的包,使用路由表253,本规则的优先级别是32767"

我们可以看到,规则包含3个要素:

什么样的包,将应用本规则 (所谓的SELECTOR,可能是filter更能反映其作用) ；

符合本规则的包将对其采取什么动作 (ACTION) ,例如用那个表；

本规则的优先级别。优先级别越高的规则越先匹配 (数值越小优先级别越高) 。

策略性路由的配置方法

传统的linux下配置路由的工具是route,而实现策略性路由配置的工具是iproute2工具包。这个软件包是由Alexey Kuznetsov开发的,软件包所在的主要网址为<ftp://ftp.inr.ac.ru/ip-routing/>。
  
这里简单介绍策略性路由的配置方法,以便能更好理解第二部分的内容。详细的使用方法请参考Alexey Kuznetsov写的 ip-cfref文档。策略性路由的配置主要包括接口地址的配置、路由的配置、规则的配置。

接口地址的配置IP Addr

对于接口的配置可以用下面的命令进行:

Usage: ip addr [ add | del ] IFADDR dev STRING

例如:

router># ip addr add 192.168.0.1/24 broadcast 192.168.0.255 label eth0 dev eth0

上面表示,给接口eth0赋予地址192.168.0.1 掩码是255.255.255.0(24代表掩码中1的个数),广播地址是192.168.0.255

路由的配置IP Route

Linux最多可以支持255张路由表,其中有3张表是内置的:

表255 本地路由表 (Local table)  本地接口地址,广播地址,已及NAT地址都放在这个表。该路由表由系统自动维护,管理员不能直接修改。

表254 主路由表 (Main table)  如果没有指明路由所属的表,所有的路由都默认都放在这个表里,一般来说,旧的路由工具 (如route) 所添加的路由都会加到这个表。一般是普通的路由。

表253 默认路由表  (Default table)  一般来说默认的路由都放在这张表,但是如果特别指明放的也可以是所有的网关路由。

表 0 保留

路由配置命令的格式如下:

Usage: ip route list SELECTOR
  
ip route { change | del | add | append | replace | monitor } ROUTE

如果想查看路由表的内容,可以通过命令:

ip route list table table_number

对于路由的操作包括change、del、add 、append 、replace 、 monitor这些。例如添加路由可以用:

router># ip route add 0/0 via 192.168.0.4 table main
  
router># ip route add 192.168.3.0/24 via 192.168.0.3 table 1

第一条命令是向主路由表 (main table) 即表254添加一条路由,路由的内容是设置192.168.0.4成为网关。

第二条命令代表向路由表1添加一条路由,子网192.168.3.0 (子网掩码是255.255.255.0) 的网关是192.168.0.3。

在多路由表的路由体系里,所有的路由的操作,例如网路由表添加路由,或者在路由表里寻找特定的路由,需要指明要操作的路由表,所有没有指明路由表,默认是对主路由表 (表254) 进行操作。而在单表体系里,路由的操作是不用指明路由表的。

显示路由ip route [类似route -n]

```bash
ip route | column -t
```

192.168.0.0/24 dev eth1 scope link
  
10.2.0.0/16 dev eth2 proto kernel scope link src 10.2.0.111
  
default via 10.2.255.254 dev eth2

```bash
ip route del 192.168.0.0/24 dev eth1
ip route add 192.168.0.0/24 dev eth1
ip route del via 10.2.255.254 //删除默认路由
ip route add via 10.2.255.254 //增加默认路由
ip route add 192.168.1.0/24 via 192.168.0.1 //增加静态路由,192.168.0.1为下一跳地址
ip route del 192.168.1.0/24 via 192.168.0.1 //删除静态路由
```

显示arp信息ip neigh [可以取代arp -n],删除则是ip neigh del IP地址 dev 设备名

路由策略数据库
  
如果你有一个大规模的路由器,需要同时满足不同用户对于路由的不通需求,路由策略数据库可以帮你通过多路由表技术来实现。当内核需要做出路由选择时,它会找出应该参考哪一张路由表。除了ip外,route也可以修改main和local表。

默认规则

```bash
ip route list table local
```

broadcast 192.168.0.255 dev eth0 proto kernel scope link src 192.168.0.10
  
broadcast 10.2.0.0 dev eth1 proto kernel scope link src 10.2.0.217
  
broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
  
... ...
  
default表为空

例 简单策略路由添加 [引用自Linux高级路由中文HOWTO]
  
让我们再来一个真实的例子。我有两个Cable Modem,连接到了一个 Linux的NAT ("伪装") 路由器上。这里的室友们向我付费使用Internet。假如我其中的一个室友因为只想访问 hotmail 而希望少付一些钱。对我来说这没有问题,他们肯定只能使用那个比较次的Cable Modem。

那个比较快的cable modem 的IP地址是 212.64.94.251,PPP 链路,对端IP是212.64.94.1。而那个比较慢的cable modem的IP地址是212.64.78.148,对端是195.96.98.253。

local 表:

[ahu@home ahu]$ ip route list table local
  
broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
  
local 10.0.0.1 dev eth0 proto kernel scope host src 10.0.0.1
  
broadcast 10.0.0.0 dev eth0 proto kernel scope link src 10.0.0.1
  
local 212.64.94.251 dev ppp0 proto kernel scope host src 212.64.94.251
  
broadcast 10.255.255.255 dev eth0 proto kernel scope link src 10.0.0.1
  
broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
  
local 212.64.78.148 dev ppp2 proto kernel scope host src 212.64.78.148
  
local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
  
local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
  
让我们看看"main"路由表:

[ahu@home ahu]$ ip route list table main
  
195.96.98.253 dev ppp2 proto kernel scope link src 212.64.78.148
  
212.64.94.1 dev ppp0 proto kernel scope link src 212.64.94.251
  
10.0.0.0/8 dev eth0 proto kernel scope link src 10.0.0.1
  
127.0.0.0/8 dev lo scope link
  
default via 212.64.94.1 dev ppp0
  
我们现在为我们的朋友创建了一个叫做"John"的规则。其实我们完全可以使用纯数字表示规则,但是不方便。我们可以向/etc/iproute2/rt_tables文件中添加数字与名字的关联:

```bash
# ip rule add from 10.0.0.10 table John

# ip rule
```

0: from all lookup local
  
32765: from 10.0.0.10 lookup John
  
32766: from all lookup main
  
32767: from all lookup default
  
现在,剩下的事情就是为 John 的路由表创建路由项了。别忘了刷新路由缓存:

```bash
# ip route add default via 195.96.98.253 dev ppp2 table John

# ip route flush cache
```

总结主要是以下几步:

echo 200 John >> /etc/iproute2/rt_tables #方便表示,把规则名字和数字对应加入到/etc/iproute2/rt_tables文件
  
ip rule add from 10.0.0.10 table John #新增规则
  
ip route add default via 195.96.98.253 dev ppp2 table John #规则中添加路由表
  
ip route flush cache #刷新路由表

<http://www.policyrouting.org/iproute2.doc.html#ss9.5>
  
<http://www.cnblogs.com/gunl/archive/2010/09/14/1826234.html>
  
<http://www.cnblogs.com/peida/archive/2013/03/05/2943698.html>
  
<https://blog.csdn.net/younger_china/article/details/72081779>
<https://www.cnblogs.com/wanstack/p/7728785.html>
<http://just4coding.com/2016/12/23/iptables-mark-and-polices-based-route/>
<https://man7.org/linux/man-pages/man8/ip-route.8.html>
<https://blog.csdn.net/destruction666/article/details/7974199>
<https://zhuanlan.zhihu.com/p/43279912>
<https://www.jianshu.com/p/efed363da831>
<https://www.jianshu.com/p/76d7ed2d77b9>
