---
author: "-"
date: "2021-06-30 17:26:53" 
title: "dpdk"
url: "dpdk"
categories:
  - inbox
tags:
  - reprint
---
## "dpdk"

## dpdk
Intel DPDK全称Intel Data Plane Development Kit,是intel提供的数据平面开发工具集,为Intel architecture (IA) 处理器架构下用户空间高效的数据包处理提供库函数和驱动的支持,它不同于Linux系统以通用性设计为目的,而是专注于网络应用中数据包的高性能处理。DPDK应用程序是运行在用户空间上利用自身提供的数据平面库来收发数据包,绕过了Linux内核协议栈对数据包处理过程。Linux内核将DPDK应用程序看作是一个普通的用户态进程,包括它的编译、连接和加载方式和普通程序没有什么两样。DPDK程序启动后只能有一个主线程,然后创建一些子线程并绑定到指定CPU核心上运行。
 

---


https://cloud.tencent.com/developer/article/1198333

https://tonydeng.github.io/sdn-handbook/dpdk/


https://github.com/google/cpu_features

