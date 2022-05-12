---
title: debian 网络配置
author: "-"
date: 2011-12-03T14:06:17+00:00
url: /?p=1718
categories:
  - Linux
  - Network
tags:
  - reprint
---
## debian 网络配置
/etc/network/interfaces

```bash
  
#wlan
  
auto wlan0
  
iface wlan0 inet dhcp
        
wpa-ssid "xxxx"
        
wpa-psk "xxxx"
  
```
  
话说Debian系的网卡配置跟Redhat系很不一样，Redhat是放在/etc/sysconfig/network-scripts目录下 面的一大堆文件里面，要修改？你一个一个文件来过吧。Debian系的则是存在/etc/network/interfaces文件里面，无论有多少块网 卡，统统扔在这个文件里。下面就来看一下这个文件的内容。

首先，一个基本的配置大概是下面这个样子: 

1 auto lo
 2 iface lo inet loopback
 3 
 4 # The primary network interface
 5 auto eth0
 6 iface eth0 inet static
 7      address 192.168.0.42
 8      network 192.168.0.0
 9      netmask 255.255.255.0
 10      broadcast 192.168.0.255
 11      gateway 192.168.0.1

上面的配置中，

第1行跟第5行说明lo接口跟eth0接口会在系统启动时被自动配置；

第2行将lo接口设置为一个本地回环 (loopback) 地址；

第6行指出eth0接口具有一个静态的 (static) IP配置；

第7行-第11行分别设置eth0接口的ip、网络号、掩码、广播地址和网关。

再来看一个更复杂点的: 

12 auto eth0
 13 iface eth0 inet static
 14     address 192.168.1.42
 15     network 192.168.1.0
 17     netmask 255.255.255.128
 18     broadcast 192.168.1.0
 19     up route add -net 192.168.1.128 netmask 255.255.255.128 gw 192.168.1.2
 20     up route add default gw 192.168.1.200
 21     down route del default gw 192.168.1.200
 22     down route del -net 192.168.1.128 netmask 255.255.255.128 gw 192.168.1.2

这次，有了一个复杂一些的掩码，和一个比较奇怪的广播地址。还有就是增加的接口启用、禁用时的路由设置；

第19行和20行配置的左右是在接口启用的时候，添加一条静态路由和一个缺省路由；

第21行和22行会在接口禁用的时候，删掉这两条路由配置。

至于配置路由的写法，仔细看，它就是route命令嘛。

继续，下面是一个物理网卡上多个接口的配置方法: 

23 auto eth0 eth0:1
 24 iface eth0 inet static
 25     address 192.168.0.100
 26     network 192.168.0.0
 27     netmask 255.255.255.0
 28     broadcast 192.168.0.255
 29     gateway 192.168.0.1
 30 iface eth0:1 inet static
 31     address 192.168.0.200
 32     network 192.168.0.0
 33     netmask 255.255.255.0

30行到33行在eth0上配置了另外一个地址，这种配置方法在配置一块网卡多个地址的时候很常见: 有几个地址就配置几个接口。冒号后面的数字可以随便写的，只要几个配置的名字不重复就可以。

下面是pre-up和post-down命令时间。这是一组命令 (pre-up、up、post-up、pre-down、down、post-down) ，分别定义在对应的时刻需要执行的命令。

34 auto eth0
 35 iface eth0 inet dhcp
 36     pre-up [ -f /etc/network/local-network-ok ]

第36行会在激活eth0之前检查/etc/network/local-network-ok文件是否存在，如果不存在，则不会激活eth0。

再更进一步的例子: 

37 auto eth0 eth1
 38 iface eth0 inet static
 39     address 192.168.42.1
 40     netmask 255.255.255.0
 41     pre-up /path/to/check-mac-address.sh eth0 11:22:33:44:55:66
 42     pre-up /usr/local/sbin/enable-masq
 43 iface eth1 inet dhcp
 44     pre-up /path/to/check-mac-address.sh eth1 AA:BB:CC:DD:EE:FF
 45     pre-up /usr/local/sbin/firewall

第41行和第44行中，check-mac-address.sh放在/usr/share/doc/ifupdown/examples/目录 中，使用的时候需要给它加上可执行权限。这两行命令会检测两块网卡的MAC地址是否为11:22:33:44:55:66和 AA:BB:CC:DD:EE:FF，如果正确，则启用网卡。如果MAC地址错误，就不会启用这两块网卡。

第42行和第45行是假定在这两块网卡上分别执行的命令，你可以把它们替换成你想要的任何玩意 : ) 

手册上说，这种方法主要是用来检测两块网卡的MAC地址交换 (If their MAC addresses get swapped) ，其实就是两块网卡名互换了，这种情况在debian系统上再常见不过了，主要是因为内核识别网卡的顺序发生了变化。这个问题可以用下面 的这种方法来避免。

> 46 auto eth0 eth1
47 mapping eth0 eth1
48     script /path/to/get-mac-address.sh
49     map 11:22:33:44:55:66 lan
50     map AA:BB:CC:DD:EE:FF internet
51 iface lan inet static
52     address 192.168.42.1
53     netmask 255.255.255.0
54     pre-up /usr/local/sbin/enable-masq $IFACE
55 iface internet inet dhcp
56     pre-up /usr/local/sbin/firewall $IFACE

第48行中的get-mac-address.sh也在/usr/share/doc/ifupdown/examples/目录里，也同样要加可执行权限。这个脚本的作用，就是获得每块网卡的MAC地址。

这段配置首先配置了两个逻辑接口 (这个名词的定义请参见debian参考手册) lan和internet，然后根据网卡的MAC地址，将逻辑接口映射 (mapped) 到物理接口上去。

再来看下面这段配置: 

> 57 auto eth0  58 iface eth0 inet manual  59       up ifconfig $IFACE 0.0.0.0 up  60       up /usr/local/bin/myconfigscript  61       down ifconfig $IFACE down

这段配置只是启用一个网卡，但是ifupdown不对这个网卡设置任何ip，而是由外部程序来设置ip。

最后一段配置，这段配置启用了网卡的混杂模式，用来当监听接口。

> 177 auto eth0
178 iface eth0 inet manual
179     up ifconfig $IFACE 0.0.0.0 up
180       up ip link set $IFACE promisc on
181       down ip link set $IFACE promisc off
182       down ifconfig $IFACE down

### wlan

# The wireless network interface  (配置无线网络接口) 

# 开机自动激活wlan0接口

auto wlan0

# 配置wlan0接口为DHCP自动获取

iface wlan0 inet dhcp