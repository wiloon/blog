---
title: linux kvm nat nftables
author: "-"
date: 2016-01-19T15:41:05+00:00
url: /?p=8681
categories:
  - Inbox
tags:
  - reprint
---
## linux kvm nat nftables

### nft command

[https://blog.wiloon.com/nft](https://blog.wiloon.com/nft)

#### ip forward

[https://blog.wiloon.com/?p=13701](https://blog.wiloon.com/?p=13701)

### 配置 TAP

[http://blog.wiloon.com/?p=13281](http://blog.wiloon.com/?p=13281)

```bash
# nftables nat
sudo nft add table ip nat
sudo nft add chain ip nat post \{ type nat hook postrouting priority 0 \; \}
sudo nft add chain ip nat pre \{ type nat hook prerouting priority 0 \; \}
# 注意修改网段, 网卡
sudo nft add rule nat post ip saddr 192.168.60.0/24 oif wlp3s0 masquerade
# 注意修改网段, 网卡
sudo nft add rule nat pre iif wlp3s0 tcp dport \{ 3389,9999 \} dnat 192.168.60.2

#sudo nft add rule nat post ip saddr 192.168.3.0/24 oif wlp3s0 snat 192.168.x.xxx
```

### save your ruleset to /etc/nftables.conf which is loaded by nftables.service

```bash
sudo -s
nft list ruleset > /etc/nftables.conf

```

[http://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT](http://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT))

```bash
sudo brctl addbr br0
sudo brctl show
sudo ip tuntap add dev tap1 mode tap
sudo brctl addif br0 tap1
sudo ip link set tap1 up
sudo ip tuntap
sudo ip addr add 192.168.3.1/24 dev br0
```

```bash
# iptables
sudo ip tuntap add dev tap0 mode tap
sudo ip addr add 192.168.3.1/24 dev tap0
sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
```

linux下 `brctl` 配置网桥
  
[http://zhumeng8337797.blog.163.com/blog/static/1007689142011643834429/](http://zhumeng8337797.blog.163.com/blog/static/1007689142011643834429/)

先装好网卡,连上网线,这是废话,不用说了。
  
然后开始！

设置linux让网桥运行    配置网桥
  
我们需要让linux知道网桥,首先告诉它,我们想要一个虚拟的以太网桥接口:  (这将在主机bridge上执行,不清楚的看看测试场景)
  
root@bridge:~> brctl addbr br0
  
其次,我们不需要STP(生成树协议)等。因为我们只有一个路由器,是绝对不可能形成一个环的。我们可以关闭这个功能。 (这样也可以减少网络环境的数据包污染) :
  
root@bridge:~> brctl stp br0 off
  
经过这些准备工作后,我们终于可以做一些立竿见影的事了。我们添加两个 (或更多) 以太网物理接口,意思是: 我们将他们附加到刚生成的逻辑 (虚拟) 网桥接口br0上。
  
root@bridge:~> brctl addif br0 eth0
  
root@bridge:~> brctl addif br0 eth1
  
现在,原来我们的两个以太网物理接口变成了网桥上的两个逻辑端口。那两个物理接口过去存在,未来也不会消失。要不信的话,去看看好了。 .现在他们成了逻辑网桥设备的一部分了,所以不再需要IP地址。下面我们将这些IP地址释放掉
  
root@bridge:~> ifconfig eth0 down
  
root@bridge:~> ifconfig eth1 down
  
root@bridge:~> ifconfig eth0 0.0.0.0 up
  
root@bridge:~> ifconfig eth1 0.0.0.0 up

好了！我们现在有了一个任何IP地址都没有的box w/o了。 好了,这下如果你想通过TP配置你的防火墙或路由器的话,你就只能通过本地的控制端口了。你不会告诉我你的机器上连串行端口都没有吧？
  
注: 上面红色部分其实是可选的,在试验中,我发现,就算不把原有的网卡地址释放掉,网桥也能工作！但是,为了更规范,或者说为了避免有什幺莫名其妙的问题,最好还是按要求做,执行这四步吧！

最后,启用网桥 root@bridge:~> ifconfig br0 up

可选:     我们给这个新的桥接口分配一个IP地址
  
root@bridge:~> ifconfig br0 10.0.3.129

或者把最后这两步合成一步:
  
root@bridge:~> ifconfig br0 10.0.3.129 up
  
就是多一个up!

这下我们做完了 。

关闭网桥命令
  
brctl delif ena eth1;
  
brctl delif ena eth0;
  
ifconfig ena down;
  
brctl delbr ena;

ALinux网桥的实现分析与使用
  
[http://www.ibm.com/developerworks/cn/linux/kernel/l-netbr/index.html](http://www.ibm.com/developerworks/cn/linux/kernel/l-netbr/index.html)
  
一、什么是桥接

桥接工作在OSI网络参考模型的第二层数据链路层,是一种以MAC地址来作为判断依据来将网络划分成两个不同物理段的技术,其被广泛应用于早期的计算机网络当中。
  
我们都知道,以太网是一种共享网络传输介质的技术,在这种技术下,如果一台计算机发送数据的时候,在同一物理网络介质上的计算机都需要接收,在接收后分析目的MAC地址,如果是属于目的MAC地址和自己的MAC地址相同便进行封装提供给网络层,如果目的MAC地址不是自己的MAC地址,那么就丢弃数据包。
  
桥接的工作机制是将物理网络段 (也就是常说的冲突域) 进行分隔,根据MAC地址来判断连接两个物理网段的计算机的数据包发送。
  
下面,我们举个例子来为各位网友讲解: 在下图中的网络结构中,有两台集线器分别连接多台计算机,我们分别将A集线器和B集线器定为A冲突域和B冲突域。在这样的网络环境中,如果计算机A向计算机C发送数据包时,集线器A会将数据包在整个网络中的全部计算机 (包括集线器B) 发送一遍,而不管这些数据包是不是需要发送到另一台区域B。

图1

我们再将集线器A和集线器B分别连接到网桥的两个端口上,如果计算机A再向计算机C发送数据包时会遇到什么样的情况呢？这时集线器A也是同样会将数据包在全网发送,当到达网桥后,网桥会进行数据包目的MAC地址的分析,然后对比自己学习到的MAC地址表,如果这个表中没有此MAC地址,网桥便会在两个网段上的发送数据包,同时会将计算机A的MAC地址记录在自己的表当中。
  
经过多次这样的记录,网桥会将所有的MAC地址记录,并划分为两个段。这时计算机A再次发送数据包给B的时候,因为这两台计算机同处在一个物理段位上,数据包到达网桥时,网桥会将目的MAC地址和自己的表进行对比,并且判断计算机A和计算机B在同一个段位上,便不会转发到区域B当中,而如果不在同一个物理段当中,网桥便会允许数据包通过网桥。
  
通过以上的例子我们了解到,网桥实际上是一种控制冲突域流量的设备。网桥现在基本上已经很少用到了,除了隔离冲突域以外,网桥还可以实现不同O类型网络的连接 (令牌环网和以太网之间的连接) 和网络的扩展 (IEEE的5.4.3连接规则) 等等功能。
  
二、什么是交换
  
交换同样工作在OSI网络参考模型的第二层数据链路层,也是一种以MAC地址来作为判断依据来将网络划分成两个不同段的技术,不同的是交换将物理网段划分到每一个端口当中,简单的理解就是一种多端口的网桥,它实际上是一种桥接技术的延伸。
  
在前面的了解当中,我们已经知道桥接是连接两个不同的物理网段 (冲突域) 的技术,交换是连接多个物理网段技术,典型的交换机通常都有多个端口,每个端口实际上就是一个网桥,当连接到交换机端口的计算机要发送数据包时,所有的端口都会判断这个数据包是否是发给自己的,如果不是就将其丢弃,这样就将冲突域的概念扩展到每个交换机端口上。
  
我们还是举例为大家说明,在下面的图中,我们可以看到计算机A、B分别连接到交换机的不同端口当中,当计算机A向B发送数据包时,假设这时A端口并没有学习到B端口的MAC地址,这时,A端口便会使用广播将数据包发送到除A端口以外的所有端口 (广播域) ,当其他计算机接收到数据包后会与自己的MAC地址进行对比,然后简单的丢弃数据包；当B接收到数据包后,通过对比后接收数据包,并且记录源地址。通过反复这样的学习,交换机会构建一个基于所有端口的转发数据库,存储在交换机的内容可寻址存储器当中 (CAM) 。

图1

在交换机学习到所有端口的信息后,计算机A再次发送数据包给B时,就不再广播地址,而是直接发送到转发数据库中所对应的B端口。通过这样的学习,在交换机上实现了微分段,每个连接到交换机端口的计算机都可以独享带宽。
  
三、什么是路由
  
路由工作在OSI参考模型的第三层网络层当中,它是基于第三层的IP地址信息来作为判断依据来将网络划分成不同段 (IP子网) 的技术,与桥接和交换不同,路由划分的是独立的逻辑网段,每个所连接的网段都具有独立的网络IP地址信息,而不是以MAC地址作为判断路径的依据,这样路由便有隔离广播的能力；而交换和桥接是划分物理网段,它们仅仅是将物理传输介质进行分段处理。同时路由具备路径选择的功能,会根据不同的目的IP地址来分析到达目的地最合适的路径。
  
在下图中,我们看到路由器所连接了三台交换机,这三台交换机分别被划分为三个不同的子网地址段: 192.168.0.0、192.168.1.0、192.168.3.0。当计算机A向B发送数据包时,在不知道到达B的路径时,交换机A会将数据包在自己所在的段上全网广播,当到达路由器中,路由器便不会再广播这个数据包,它根据路由协议的规则来判断到达B应该选择将其转发到那个段上,这时便会将数据包转发到对应的IP地址段当中,而不广播到不需要这个数据包的C网段当中。如果路由器中没有规则定义到达目的IP地址的路径时,它会直接丢弃这个数据包。

图3

路由器主要有路径选择和数据转发两个基本功能,但在很多场景下,路由器一般都承担着网关的角色。在国内,我们通常都是采用 PPPOE 拨号或者静态路由两种方式实现局域网共享上网。这时,路由器主要的功能是实现局域网和广域网之间的协议转换,这同样也是网关的主要用途。
  
四、三者之间的区别
  
1. 位于参考模型的层数不同
在开放系统互联参考模型当中,网桥和交换机都是位于参考模型的第二层-数据链路层,而路由器则位于更高一层-网络层。
  
2. 基于的路径判断条件不同
由于位于OSI参考模型的层数不同,所以使交换机、网关这两种设备判断路径的条件也不相同,网桥和交换机是根据端口的MAC地址来判断数据包转发,而路由器则使用IP地址来进行判断。
  
3. 控制广播的能力不同
网桥和交换机 (三层交换机或支持VLAN功能的除外) 这两种设备是无法控制网络的广播,如果有广播数据包,就会向所有的端口转发,所以在大的网络环境当中,必须得要有路由器来控制网络广播。
  
4. 智能化程度不同
在判断数据的时候,网桥只能判断是否在同一个物理网段,交换机则可以判断数据包是属于那个端口,但是这两种设备都没有选择最优路径的能力,而路由器基于IP地址判断路径,所以会根据IP地址信息来判断到达目的地的最优路径。

五、三者的不同应用场景及未来发展
  
在现实的应用环境当中,网桥已经基本上不会被使用了,在中小型的局域网当中,最常用到的组网设备便是交换机,是否选择路由器会根据网络的规模和功能来决定,在大型网络中,路由器是必须的,用来控制广播,但是由于技术的不断延伸,交换机也被集成了基于IP地址判断路径及控制广播的功能,所以,路由器现在逐步在被可路由式交换机所取代。
  
前面提到,路由器在很多场景下都是被用过网关,所以,随着宽带技术的迅速发展,在最末一公里,一种新兴的设备-宽带路由器将会逐步取代传统路由器来实现网络的接入功能。
  
相信通过上面的介绍,大家对于网桥、交换、路由及网关的功能有了更清晰的了解！
  
三、   brctl 的使用方法
  
有五台主机。其中一台主机装有linux ,安装了网桥模块,而且有四块物理网卡,分别连接同一网段的其他主机。我们希望其成为一个网桥,为其他四台主机(IP 分别为192.168.1.2,192.168.1.3 ,192.168.1.4 ,192.168.1.5) 之间转发数据包。同时,为了方便管理,希望网桥能够有一个IP  (192.168.1.1 ) ,那样管理员就可以在192.168.1.0/24 网段内的主机 上telnet 到网桥,对其进行配置,实现远程管理。

前一节中提到,网桥在同一个逻辑网段转发数据包。针对上面的拓扑,这个逻辑网段就是192.168.1.0/24 网段。我们为这个逻辑网段一个名称,br0 。首先需要配置这样一个逻辑网段。

```bash
brctl addbr br0 ( 建立一个逻辑网段,名称为br0)
brctl delbr br0
```

实际上,我们可以把逻辑网段192.168.1.0/24 看作使一个VLAN ,而br0 则是这个VLAN 的名称。

建立一个逻辑网段之后,我们还需要为这个网段分配特定的端口。在Linux 中,一个端口实际上就是一个物理网卡。而每个物理网卡的名称则分别为eth0 ,eth1 ,eth2 ,eth3 。我们需要把每个网卡一一和br0 这个网段联系起来,作为br0 中的一个端口。

````bash
brctl addif br0 eth0       (让eth0 成为br0 的一个端口)
brctl addif br0 eth1                ( 让eth1 成为br0 的一个端口)
brctl addif br0 eth0                ( 让eth2 成为br0 的一个端口)
brctl addif br0 eth3                ( 让eth3 成为br0 的一个端口)
brctl delif br0 eth0
```

网桥的每个物理网卡作为一个端口,运行于混杂模式,而且是在链路层工作,所以就不需要IP了。

# ifconfig eth0 0.0.0.0

# ifconfig eth1 0.0.0.0

# ifconfig eth2 0.0.0.0

# ifconfig eth3 0.0.0.0

# ip addr add 127.0.0.1/8 dev lo brd +

 (ip 是iproute2 软件包里面的一个强大的网络配置工具,它能够替代一些传统的网络管理工具。例如: ifconfig 、route 等。这个手册将分章节介绍ip 命令及其选项。)
  
然后给br0 的虚拟网卡配置IP : 192.168.1.1 。那样就能远程管理网桥。

# ifconfig br0 192.168.1.1

给br0 配置了IP 之后,网桥就能够工作了。192.168.1.0/24 网段内的主机都可以telnet 到网桥上对其进行配置。

以上配置的是一个逻辑网段,实际上Linux 网桥也能配置成多个逻辑网段( 相当于交换机中划分多个VLAN) 。

四、   brctl 命令详细分析
  
增加桥接过程
  
 ( 1 )  # brctl addbr br0
  
 ( 2 )  # brctl addif br0 eth0
  
 ( 3 )  #   ip addr add 172.16.12.43/8 dev br0 brd +
  
 ( 4 )  #   ifconfig br0 up

删除桥接过程

 ( 1 )  # ip addr del 172.16.12.43/8 dev br0 brd +

 ( 2 )  # ifconfig br0 down

 ( 3 )  # brctl delif br0 eth0

 ( 4 )  # brctl delbr br0

[http://blog.csdn.net/x_nazgul/article/details/20233237](http://blog.csdn.net/x_nazgul/article/details/20233237)

[https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/%25e6%2589%258b%25e5%258a%25a8%25e5%2588%259b%25e5%25bb%25banat%25e7%25bd%2591%25e7%25bb%259c?lang=en](https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/%25e6%2589%258b%25e5%258a%25a8%25e5%2588%259b%25e5%25bb%25banat%25e7%25bd%2591%25e7%25bb%259c?lang=en)
