---
title: Wireshark 过滤
author: "-"
date: 2016-01-05T07:47:07+00:00
url: wireshark/filter
categories:
  - network
tags:
  - reprint
---
## Wireshark 过滤

### port

#### 按端口过滤

    tcp.port == 25

#### 按目标端口过滤

    tcp.dstport == 25

#### 显示来自10.230网段的封包

    ip.src == 10.230.0.0/16

wireshark http ssdp 过滤方法

http&&!(udp.dstport == 1900)

ip.addr == 10.1.1.1
  
ip.src != 10.1.2.3 or ip.dst != 10.4.5.6
  
[http://blog.csdn.net/cumirror/article/details/7054496](http://blog.csdn.net/cumirror/article/details/7054496)

[http://blog.csdn.net/wishfly/article/details/43226455](http://blog.csdn.net/wishfly/article/details/43226455)
