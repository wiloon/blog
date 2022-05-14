---
title: 'linux  网桥'
author: "-"
date: 2011-12-04T07:17:59+00:00
url: /?p=1778
categories:
  - inbox
tags:
  - reprint
---
## 'linux  网桥'
安装过vmware的朋友应该都知道 vmware宿主和虚拟机上网的3中方式

1. 桥接

2. NAT

3. host-only

这3种方式的操作手法网上都有描述，我们工作中主要使用到了 第一种 桥接的方式 ，这种方式 最大的好处 就是能建立一个和宿主机 对等的网络， 实现vm 和整个局域网的通信 ，就像 宿主机和VM在一个交换机上 链接一样！

**网桥的功能: **

网桥的功能在延长网络跨度上类似于中继器，然而它能提供智能化连接服务， 即根据帧的终点地址处于哪一网段来进行转发和滤除。网桥对站点所处网段的了 解是靠"自学习"实现的。

当使用网桥连接两段LAN 时，网桥对来自网段1 的MAC 帧，首先要检查其终 点地址。如果该帧是发往网段1 上某一站的，网桥则不将帧转发到网段2 ，而将 其滤除;如果该帧是发往网段2 上某一站的，网桥则将它转发到网段2.这表明， 如果LAN1和LAN2上各有一对用户在本网段上同时进行通信，显然是可以实现的。 因为网桥起到了隔离作用。可以看出，网桥在一定条件下具有增加网络带宽 的作用。

**网桥工作流程如下: **

1. 检查收到的信号，解释0和1的含义，并找出帧中的目的MAC地址。

2. 如果具有该目的的MAC地址的帧能够通过网桥上不同的接口到达目的地(不是帧到达网桥的那个接口)，则通过重新生成信号来传输这帧。(这个过程叫做转发。)

3. 如果该帧到达的接口就是目的地址可达到的端口，则丢弃该帧。(这个过程叫做过滤。)

**为什么要使用网桥: **

许多单位都有多个局域网，并且希望能够将它们连接起来。之所以一个单位有多个局域网，有以下6个原因: 

首先，许多大学的系或公司的部门都有各自的局域网，主要用于连接他们自己的个人计算机、工作站以及服务器。由于各系(或部门)的工作性质不同，因此选用了不同的局域网，这些系(或部门)之间早晚需相互交往，因而需要网桥。

其次，一个单位在地理位置上较分散，并且相距较远，与其安装一个遍布所有地点的同轴电缆网，不如在各个地点建立一个局域网，并用网桥和红外链路连接起来，这样费用可能会低一些。

第3，可能有必要将一个逻辑上单一的LAN分成多个局域网，以调节载荷。例如采用由网桥连接的多个局域网，每个局域网有一组工作站，并且有自己的文件服务器，因此大部分通信限于单个局域网内，减轻了主干网的负担。

第4，在有些情况下，从载荷上看单个局域网是毫无问题的，但是相距最远的机器之间的物理距离太远(比如超过802.3所规定的2.5km)。即 使电缆铺设不成问题，但由于来回时延过长，网络仍将不能正常工作。唯一的办法是将局域网分段，在各段之间放置网桥。通过使用网桥，可以增加工作的总物理距 离。

第5，可靠性问题。在一个单独的局域网中，一个有缺陷的节点不断地输出无用的信息流会严重地破坏局域网的运行。网桥可以设置在局域网中的关键部位，就像建筑物内的放火门一样，防止因单个节点失常而破坏整个系统。

第6，网桥有助于安全保密。大多数LAN接口都有一种混杂工作方式(promiscuousmode)，在这种方式下，计算机接收所有的帧，包括那些并不是编址发送给它的帧。如果网中多处设置网桥并谨慎地拦截无须转发的重要信息，那么就可以把网络分隔以防止信息被窃。

**linux 下 设置网桥的方式 (主要步骤) : **

1. 创建网桥设备 br0:   brctl addbr br0

2. 向br0中添加网卡 eth0  eth1

brctl addif eth0

brctl addif eth1

3. 从网桥中删除网卡 eth0 eth1

brctl delif eth0

brctl delif eth1

4. 删除网桥 br0 :    brctl  delbr  br0

**开机后自动搭建网络桥接脚本  (根据需要修改) : **


  
    
      Python代码
  
  
  
    
      #!/bin/bash
    
    
      modprobe tun
    
    
      tunctl -t tap0 -u $USERNAME
    
    
      tunctl -t tap1 -u $USERNAME
    
    
      brctl addbr br0
    
    
      ifconfig eth0 0.0.0.0 promisc
    
    
      brctl addif br0 eth0
    
    
      ifconfig br0 up
    
    
      dhclient br0
    
    
      brctl addif br0 tap0
    
    
      brctl addif br0 tap1
    
    
      ifconfig tap0 up
    
    
      ifconfig tap1 up
    
    
      chmod a+rw /dev/net/tun
    
  

把该脚本添加到rc.local开机脚本去，实现开机自动构建桥接网络

> su -c 'echo "$HOME/vmbridge.sh" >> /etc/rc.local'
  
> 或者
  
> su -c 'cat $HOME/vmbridge.sh >> /etc/rc.local'

**注意事项**

  1. 桥接后，br0的IP就是宿主机的IP，而虚拟机的IP需要在虚拟机内设定。至于是动态IP还是静态IP，需要根据使用者的需要来设定。因为虚拟 机桥接接入局域网以后，虚拟机就相当于是局域网内的一台实体计算机，与宿主机平行，所以IP的设定要谨慎一些。如果宿主机是静态IP，而虚拟机是动态 IP，那么请确保局域网内有一台DHCP服务器来分配IP。
  2. 设定虚拟机IP的时候，请不要跟br0的IP相同，否则会造成IP冲突，导致宿主机或虚拟机不能连接网络。
  3. 如果出现虚拟机、宿主机和网关能够互相ping通，但虚拟机不能浏览网络等情况，请检查虚拟机的DNS设置。如果出现宿主机或虚拟机断开网络，请检查桥接网络中网桥是否连接好，网关是否设置好。
  4. 本方法适用于XEN、KVM、QEMU和版本较旧的VirtualBox。

**centos中 kvm 网桥的设置:**


  
    
      新建一个ifcfg－br0文件: 
    
    
    
      DEVICE=br0
 TYPE=Bridge
 BOOTPROTO=static
 BROADCAST=10.1.255.255
 IPADDR=10.1.29.3
 NETMASK=255.255.0.0
 NETWORK=10.1.0.0
 ONBOOT=yes
    
    
    
      然后修改相应网卡的配置文件，我的是eth1: 
    
    
    
      # Realtek Semiconductor Co., Ltd. RTL-8169 Gigabit Ethernet
 DEVICE=eth1
 #BOOTPROTO=none
 #BROADCAST=10.1.255.255
 HWADDR=D8:5D:4C:74:EE:E8
 #IPADDR=10.1.29.3
 #NETMASK=255.255.0.0
 #NETWORK=10.1.0.0
 ONBOOT=yes
 #TYPE=Ethernet
 #USERCTL=no
 #IPV6INIT=no
 #PEERDNS=yes
 BRIDGE=br0
    
    
    
      可以看出，原来网卡的配置只保留device名称，硬件地址，onboot选项，以及新添加的BRIDGE=br0。
    
    
    
      然后重启网络: 
    
    
    
      /etc/init.d/network restart 或service network restart
    
    
    
      实验中在br0中加入gateway后，/etc/sysconfig/network中的gateway就消失了。成功后，利用route -n查看路由，发现所有的包都从br0走了。
  

**可用的开机建立网桥的脚本: **


  
    
      Html代码
  
  
  
    
      #!/bin/sh
    
    
      brctl addbr br0
    
    
      brctl addif br0 eth0
    
    
      ifconfig eth0 down
    
    
      ifconfig eth0 0.0.0.0 up
    
    
      ifconfig br0 192.168.198.71 up
    
    
      service network restart
    
  

在此脚本中eth0为桥接的网卡，br0为创建的虚拟网络。将br0桥接到真实的网卡eth0是，以实现虚拟机的桥接功能。如果要添加新的桥接网络，将eth0和br0替换成需要的借口即可。
  
注意: 以上命令建议使用脚本运行，如果使用命令逐条执行会造成网络中断。
  
执行次脚本即可实现添加桥接网卡的功能。
  
桥接功能在重启之后就会失效，可以将此脚本添加到/etc/rc.d/rc.local下以实现开机自动执行。