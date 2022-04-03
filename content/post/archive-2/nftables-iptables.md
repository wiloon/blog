---
title: nftables iptables
author: "-"
date: 2016-01-05T08:36:54+00:00
url: /?p=8641
categories:
  - Uncategorized

tags:
  - reprint
---
## nftables iptables
跟iptables相比,nftables带来了一系列的好处

更易用易理解的语法
  
表和链是完全可配置的
  
匹配和目标之间不再有区别
  
在一个规则中可以定义多个动作
  
每个链和规则都没有内建的计数器
  
更好的动态规则集更新支持
  
简化IPv4/IPv6双栈管理
  
支持set/map等
  
支持级连 (需要内核4.1+) 

新的防火墙子系统/包过滤引擎Nftables将在Linux3.13中替代有十多年历史的iptables。iptables/netfilter在2001年加入到2.4内核中。诞生于2008年的NFTables设计替代iptables,它提供了一个更简单的kernelABI,减少重复代码,改进错误报告,更有效的支持过滤规则。
  
除了iptables,NFTables还将替代ip6tables、arptables和ebtables。Linux内核的第一代包过滤机制是ipfwadm (1.2.1内核,1995年) ,之后是ipchains (1999年) ,iptables、Nftables是第四代。

http://luxiaok.blog.51cto.com/2177896/1312846

http://segmentfault.com/a/1190000000410970

Linux 3.13 带来了很多特性。nftables也是第一次正式发布。nftables是一个致力于替换现有的{ip,ip6,arp,eb}tables框架 (也就是大家熟知的iptables) 的项目。然而,Linux3.13中的nftables版本还是不完整的,还缺少一些重要的特性。这些特性会在后续的Linux版本中发布。大多数场景下nftables已经可以使用,但是完整的支持 (即,nftables优先级高于iptables) 应该在Linux 3.15。

nftables引入了一个新的命令行工具nft。nft是iptables及其衍生指令 (ip6tables,arptables) 的超集。同时,nft拥有完全不同的语法。是的,如果你习惯于iptables,这是个不好的消息。但是有一个兼容层允许你使用iptables,而过滤是由内核中的nftables完成的。

到目前为止,只有非常少的文档资料。你可以找到我的nftables快速开始,其他的一些初步文档很快就会公开。