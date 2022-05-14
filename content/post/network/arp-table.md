---
author: "-"
date: "2021-03-23 10:48:47" 
title: "arp table, arp 表"
categories:
  - inbox
tags:
  - reprint
---
## "arp table, arp 表"

ARP表(Address Resolution Table)
ARP协议
首先明确一点,在以太网环境下,同一个网段的主机之间需要知道对方的MAC地址,才能进行通信。

上一节介绍了交换机的工作原理,了解到交换机是根据MAC寻址,查表确认输出端口以完成本节点转发任务的。看到这里其实应该可以抛出从一开始就被我们忽视了的问题: 在初始构造数据包准备发送时,源主机究竟要如何获得目的主机网络设备MAC地址的呢？这时,就需要使用到ARP协议。在网络拓扑中的每个节点或说主机上,实际都维护有一张ARP表,它记录着主机的IP地址(网络地址)到MAC地址(物理地址)的映射关系。

ARP协议,即地址解析协议,它是一个网络层协议,运行在各网络节点上,负责完成主机IP地址到MAC地址的映射。


ip neighbour–neighbour/arp 表管理命令

ip neighbour–neighbour/arp 表管理命令
缩写 neighbour、neighbor、neigh、n
命令 add、change、replace、delete、fulsh、show(或者list)
ip neighbour add    －－－－－添加一个新的邻接条目
ip neighbour change －－－－－修改一个现有的条目
ip neighbour replace －－－－－替换一个已有的条目
缩写: add、a；change、chg；replace、repl

例: 在设备eth0上,为地址 10.0.0.3 添加一个 permanent ARP条目: 
# ip neigh add 10.0.0.3 lladdr 0:0:0:0:0:1 dev eth0 nud perm

例: 把状态改为 reachable
# ip neigh chg 10.0.0.3 dev eth0 nud reachable

ip neighbour delete －－－删除一个邻接条目
例: 删除设备eth0上的一个ARP条目10.0.0.3
# ip neigh del 10.0.0.3 dev eth0

ip neighbour show －－ 显示网络邻居的信息. 缩写: show、list、sh、ls
例: # ip -s n ls 193.233.7.254
193.233.7.254. dev eth0 lladdr 00:00:0c:76:3f:85 ref 5 used 12/13/20 nud reachable

ip neighbour flush －－清除邻接条目. 缩写: flush、f
例:  (-s 可以显示详细信息)
# ip -s -s n f 193.233.7.254



---

http://www.huilog.com/?p=409