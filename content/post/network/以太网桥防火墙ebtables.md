---
title: linux ebtables
author: "-"
date: 2011-12-11T06:18:46+00:00
url: /?p=1850
categories:
  - Linux
  - Network

tags:
  - reprint
---
## linux ebtables
linux 以太网桥防火墙 ebtables. 2.4以后的内核才能支持ebtables

Ebtables即是以太网桥防火墙，以太网桥工作在数据链路层，Ebtables来过滤数据链路层数据包。

ebtables的功能和语法和iptables的类似，只是iptables是在ip层对数据包进行过滤和NAT的，而ebtables则是在mac层实现类似功能。最近在做虚拟机数据包流量监控的工作，需要用到ebtables。

ebtables主要用于switch，而iptables主要用于router (当然，他们都可以在host上使用，不过都不是重点) 
  
从功能上来讲，没有明显的界限，一些基本的功能两者都能实现但侧重点不同，ebtables侧重于layer2，iptables侧重于layer3 (可增加layer7扩展) 

2.6内核内置了Ebtables，要使用它必须先安装Ebtables的用户空间工具 (ebtables-v2.0.6) ，安装完成后就可以使用ebtables来过滤网桥的数据包。 参照用户实际要求，设置ebtables规则如下: 

1:对所有的数据包默认通过
  
2:分清楚源地址和目的地址和源端口和目的端口
  
3:对TCP,UDPP数据包分别过滤

Ebtables使用规则如下: 

ebtables [-t table] -[ADI] chain rule-specification [match-extensions] [watcher-extensions]

-t table :一般为FORWARD链。

－ADI: A添加到现有链的末尾；D删除规则链 (必须指明规则链号) ；I插入新的规则链 (必须指明规则链号) 。

--delete -D chain rulenum     : delete rule at position rulenum from chain
sudo ebtables -t nat -D POSTROUTING 1

-P:规则表的默认规则的设置。可以DROP,ACCEPT,RETURN。

-F:对所有的规则表的规则链清空。

-L:指明规则表。可加参数，-Lc,-Ln

-p:指明使用的协议类型，ipv4,arp等可选 (使用时必选) 详情见/etc/ethertypes

-ip-proto:IP包的类型，1为ICMP包，6为TCP包，17为UDP包，在/etc/protocols下有详细说明

-ip-src:IP包的源地址

-ip-dst:IP包的目的地址

-ip-sport:IP包的源端口

-ip-dport:IP包的目的端口

-i:指明从那片网卡进入

-o:指明从那片网卡出去

/***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\*****/

简单配置规则如下: 

#!/bin/bash

echo "The ebtables start !"

ebtables -P FORWARD ACCEPT

ebtables -P INPUT ACCEPT

ebtables -P OUTPUT ACCEPT

ebtables -F

ebtables -A FORWARD -p ipv4 -i eth0/eth1 -ip-proto (6/17) -ip-dst(目的IP)  -ip-dport(目的端口) -j DROP

ebtables -A FPRWARD -p ipv4 -i eth0/eth1 -ip-proto (7/17) -ip-src(源IP) -ip-sport(源端口) -j

DROP


<http://ebtables.sourceforge.net/misc/ebtables-man.html>


