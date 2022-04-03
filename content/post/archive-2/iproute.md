---
title: iproute2 basic
author: "-"
date: 2018-03-25T01:20:23+00:00
url: /?p=12054

categories:
  - inbox
tags:
  - reprint
---
## iproute2 basic

### install
   apt install iproute2


### 查看IP地址
```bash
# 显示所有网络地址
ip address show
# 简写
ip addr
# 再简写
ip a
```

```bash
# Delete all IPv4 addresses on interface wlp3s0
sudo ip -f inet addr del dev wlp3s0
  
#为网络接口分配IPv4地址
#使用这些命令配置网络接口的IPv4地址。
sudo ip addr add 10.0.0.1/24 dev eth1

# 查端口
ss -ntlp | grep ",1234,"

sudo ip link set down eth1
  
sudo ip link set up eth1

#查所有网卡的ip
ip addr show

#查看所有网卡
ip link show

#查看某一个网卡的ip
  
ip addr show dev eth1

```

### 设置网卡为混杂模式
ip link set enp1s0 promisc on

##### 系统启动后把网卡设置为混杂模式
vim /usr/lib/systemd/system/promiscuous_mode@.service

    [Unit]
    Description=Control promiscuous mode for interface %i
    After=network-online.target
    Wants=network-online.target

    [Service]
    Type=oneshot
    ExecStart=/sbin/ip link set promisc on dev %i
    ExecStop=/sbin/ip link set promisc off dev %i
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target

##### systemctl enable
    systemctl enable promiscuous_mode@enp1s0.service

```bash
ip addr add 192.168.53.0/24 dev wg0
ip addr del 192.168.53.0/24 dev wg0
# delete dev
ip link delete dev wg0
```

### 显示链路信息
```bash
ip link list # 显示ip链路状态信息

ip neigh show #显示邻居表
ip link
ip link show dev eth0
```



### 路由
title: iproute2 > 路由表, routing table

---

对所有来源端口是8080的数据输出包进行标记处理,设置标记2

$: iptables -t mangle -A OUTPUT -p tcp -sport 8080 -j MARK -set-mark 2
  
4.1.2 对标记的数据包进行自定义路由
  
既然数据包已经有了标记,既可以具体按标记设置路由规则了。同上的例子,我们首先增加一条路由规则。

# 标记2的数据包按照2号路由规则表路由

$: ip rule add priority 10000 fwmark 2 table 2

https://segmentfault.com/a/1190000000638244

iproute基本介绍
  
iproute是用于linux下网络配置工具,该工具包包含以下组件

# rpm -ql iproute | grep bin

/sbin/cbq #流量控制
  
/sbin/ifcfg #网络地址配置管理
  
/sbin/ip #网络配置命令
  
/sbin/rtmon #rtmon listens on netlink socket and monitors routing table changes.
  
/sbin/tc #进行流量控制的命令
  
/usr/sbin/arpd #收集arp信息保存到本地cache daemon
  
/usr/sbin/lnstat #网络统计信息
  
/usr/sbin/nstat #显示网络统计信息
  
/usr/sbin/rtacct #查看数据包流量状态
  
【nstat and rtacct are simple tools to monitor kernel snmp counters and network interface statistics.】
  
/usr/sbin/ss #类似netstat命令,显示活动连接
  
iproute的中心是ip这个命令,类似arp、ifconfig、route命令虽然这些工具能够工作,但是在Linux2.2和更高版本的内核上就有点out了。

ip基本使用方法

# ip -help

Usage: ip [ OPTIONS ] OBJECT { COMMAND | help }
         
ip [ -force ] -batch filename
  
where OBJECT := { link | addr | addrlabel | route | rule | neigh | ntable |
                     
tunnel | maddr | mroute | mrule | monitor | xfrm }
         
OPTIONS := { -V[ersion] | -s[tatistics] | -d[etails] | -r[esolve] |
                      
-f[amily] { inet | inet6 | ipx | dnet | link } |
                      
-o[neline] | -t[imestamp] | -b[atch] [filename] |
                      
-rc[vbuf] [size]}
  
OBJECT
  
link 指网络设备,通过此对象命令,我们可以查看及更改网络设备的属性。
  
addr 地址管理
  
neigh arp表管理
  
route 路由管理
  
rule 路由策略
  
maddr 多址广播地址
  
mroute 多播路由缓存管理
  
tunnel 通道管理

# ip -V #打印iproute信息

ip utility, iproute2-ss091226
  
显示链路信息

# ip link

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
      
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
  
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
      
link/ether 00:0c:29:3b:9c:6f brd ff:ff:ff:ff:ff:ff

# ip link show dev eth0

2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
      
link/ether 00:0c:29:3b:9c:6f brd ff:ff:ff:ff:ff:ff
  
显示IP地址

# ip addr

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
      
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      
inet 127.0.0.1/8 scope host lo
      
inet6 ::1/128 scope host
         
valid_lft forever preferred_lft forever
  
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
      
link/ether 00:0c:29:3b:9c:6f brd ff:ff:ff:ff:ff:ff
      
inet 192.168.0.10/24 brd 192.168.0.255 scope global eth0


```bash
# Change link MTU
ip link set dev ${interface name} mtu ${MTU value}
# Examples:
ip link set dev tun0 mtu 1480
# check arp cache
ip neigh

# Bring a link up or down
ip link set dev ${interface name} up
ip link set eth0 up

ip link set dev ${interface name} down

ip route show
ip tuntap list
```


---


https://baturin.org/docs/iproute2/
  
https://segmentfault.com/a/1190000000638244
  
https://access.redhat.com/sites/default/files/attachments/rh_ip_command_cheatsheet_1214_jcs_print.pdf
https://www.cnblogs.com/LiuYanYGZ/p/12368421.html
http://linux-ip.net/html/routing-tables.html
>http://linux-ip.net/gl/ip-cref/ip-cref.html
