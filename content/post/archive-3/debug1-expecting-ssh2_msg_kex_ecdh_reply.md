---
title: 'debug1,expecting SSH2_MSG_KEX_ECDH_REPLY'
author: "-"
date: 2019-06-22T05:23:23+00:00
url: /?p=14558
categories:
  - Uncategorized

tags:
  - reprint
---
## 'debug1,expecting SSH2_MSG_KEX_ECDH_REPLY'
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY

设置网卡接口的MTU值，改成: 1200

```bash
sudo ip link set dev eth0 mtu 1200
```

/etc/systemd/network/en0s25.network

[Match]
  
Name=enp0s25

[Link]
  
MTUBytes=9000

[Network]
  
Address=192.168.1.101/24
  
Gateway=192.168.1.1/24
  
DNS=192.168.1.1

以太网的MTU是1500，而隧道的MTU值1400左右，比以太网的小，因此，以太网发出去的包就被拒绝了，最终导致无法建立SSH连接。

原理
  
MTU (Maximum Transmission Unit) : 最大传输单元，是指一种通信协议的某一层上面所能通过的最大数据包大小 (以字节为单位) 。最大传输单元这个参数通常与通信接口有关 (网络接口卡、串口等) .(摘自维基百科)

从维基百科种看到: 

这里的MTU所指的是无需分段的情况下，可以传输的最大IP报文 (包含IP头部，但不包含协议栈更下层的头部) 。

下面是普通媒体的MTU表: 

网络 MTU(Byte)
  
超通道 65535
  
16Mb/s令牌环 17914
  
4Mb/s令牌环 4464
  
FDDI 4352
  
以太网 1500
  
IEEE 802.3/802.2 1492
  
X.25 576
  
点对点 (低时延)  296
  
对于使用AUTOSSH建立隧道: 

传输模式，MTU值最大是: 1440
  
隧道模式，MTU值最大是: 1420
  
所以，出现这个现象的原因也就清楚了:  本身以太网的MTU是1500，而隧道的MTU值1400左右，比以太网的小，因此，以太网发出去的包就被拒绝了，最终导致无法建立SSH连接。

ssh 密钥交换阶段一次发送的数据一般大于 1500 字节，因此至少填满了一个 MTU；
  
通过tun0发出密钥交换信息，因为大于目标网络的MTU，而被丢弃；
  
将tun0设备的MTU设置为1200后，不会超过目标网络设定的MTU，因此可以正常交换密钥。

https://github.com/johnnian/Blog/issues/44
  
http://blog.sina.com.cn/s/blog_4da051a60102vdpb.html
  
https://bbs.archlinux.org/viewtopic.php?id=237885