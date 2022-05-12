---
title: sk_buff
author: "-"
date: 2012-10-31T07:13:50+00:00
url: skbuff
categories:
  - Java
  - Web
tags:$
  - reprint
---
## sk_buff

sk_buff (internal networking structure used by linux kernel)
sk_buff的意思是socket buffer，这是Linux网络子系统中的核心数据结构

><https://liu-jianhao.github.io/2019/05/linux%E5%86%85%E6%A0%B8%E7%BD%91%E7%BB%9C%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%901sk_buff%E7%BB%93%E6%9E%84/>

## tcp连接的资源占用

size of sk_buff (internal networking structure used by linux kernel)

the read and write buffer for a connection

the size of buffers can be tweaked as required

root@x:~# sysctl -A | grep net | grep mem
check for these variables

these specify the maximum default memory buffer usage for all network connections in kernel

net.core.wmem_max = 131071

net.core.rmem_max = 131071

net.core.wmem_default = 126976

net.core.rmem_default = 126976
these specify buffer memory usage specific to tcp connections

net.ipv4.tcp_mem = 378528   504704  757056

net.ipv4.tcp_wmem = 4096    16384   4194304

net.ipv4.tcp_rmem = 4096    87380   4194304
the three values specified are " min default max" buffer sizes. So to start with linux will use the default values of read and write buffer for each connection. As the number of connection increases , these buffers will be reduced [at most till the specified min value] Same is the case for max buffer value.

These values can be set using this sysctl -w  KEY=KEY VALUE

eg. The below command ensures the read and write buffers for each connection are 4096 each.

sysctl -w net.ipv4.tcp_rmem='4096 4096 4096'

sysctl -w net.ipv4.tcp_wmem='4096 4096 4096'

><https://stackoverflow.com/questions/8646190/how-much-memory-is-consumed-by-the-linux-kernel-per-tcp-ip-network-connection>
