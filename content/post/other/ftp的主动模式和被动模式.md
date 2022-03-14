---
title: FTP的主动模式和被动模式
author: "-"
date: 2012-05-26T02:28:17+00:00
url: /?p=3238
categories:
  - Linux
  - Network

tags:
  - reprint
---
## FTP的主动模式和被动模式
<http://space.itpub.net/14075938/viewspace-495630>

**FTP**两种工作**模式**: **主动****模式** (Active **FTP**) 和被动**模式** (Passive **FTP**) 

在主动模式下，FTP客户端随机开启一个大于1024的端口N向服务器的21号端口发起连接，然后开放N+1号端口进行监听，并向服务器发出PORT N+1命令。服务器接收到命令后，会用其本地的FTP数据端口 (通常是20) 来连接客户端指定的端口N+1，进行数据传输。
  
在被动模式下，FTP库户端随机开启一个大于1024的端口N向服务器的21号端口发起连接，同时会开启N+1号端口。然后向服务器发送PASV命令，通知服务器自己处于被动模式。服务器收到命令后，会开放一个大于1024的端口P进行监听，然后用PORT P命令通知客户端，自己的数据端口是P。客户端收到命令后，会通过N+1号端口连接服务器的端口P，然后在两个端口之间进行数据传输。
  
总的来说，主动模式的FTP是指服务器主动连接客户端的数据端口，被动模式的FTP是指服务器被动地等待客户端连接自己的数据端口。
  
被动模式的FTP通常用在处于防火墙之后的FTP客户访问外界FTp服务器的情况，因为在这种情况下，防火墙通常配置为不允许外界访问防火墙之后主机，而只允许由防火墙之后的主机发起的连接请求通过。因此，在这种情况下不能使用主动模式的FTP传输，而被动模式的FTP可以良好的工作。

win 下面设置ftp模式

一、什么是PASV和PORT方式

 (1) PORT其实是Standard模式的另一个名字，又称为Active模式。中文意思是"主动模式。

 (2) PASV也就是Passive的简写。中文就是"被动模式。

二、两者不同

不同之处是由于PORT (主动) 这个方式需要在接上TCP 21端口后，服务器通过自己的TCP 20来发出数据。并且需要建立一个新的连接来传送档案。而PORT的命令包含一些客户端没用的资料，所以有了PASv的出现。而PASV模式拥有PORT模式的优点，并去掉一些PORT的缺点。PASV运行方式就是当服务器接收到客户端连接请求时，就会自动从端口1024到5000中随机选择一个和客户端建立连接传递数据。由于被动且自动建立连接，容易受到攻击，所以安全性差。

三、常见的FTP客户端软件PORT方式与PASV方式的切换方法

大部分FTP客户端默认使用PASV方式。IE默认使用PORT方式。 在大部分FTP客户端的设置里，常见到的字眼都是"PASV"或"被动模式"，极少见到"PORT"或"主动模式"等字眼。因为FTP的登录方式只有两种: PORT和PASV，取消PASV方式，就意味着使用PORT方式。

 (1) IE: 工具 -> Internet选项 -> 高级 -> "使用被动FTP" (需要IE6.0以上才支持) 。

 (2) CuteFTP: Edit -> Setting -> Connection -> Firewall -> "PASV Mode" 或File -> Site Manager，在左边选中站点 -> Edit -> "Use PASV mode" 。

 (3) FlashGet: 工具 -> 选项 -> 代理服务器 -> 直接连接 -> 编辑 -> "PASV模式"。

 (4) FlashFXP: 选项 -> 参数选择 -> 代理/防火墙/标识 -> "使用被动模式" 或 站点管理 -> 对应站点 -> 选项 -> "使用被动模式"或快速连接 -> 切换 -> "使用被动模式"。

vsftpd被动模式配置

一、系统环境: LinuxAS4 + vsftpd

二、网络结构

xp(Client)--[eth0]linux (Firewall) [eth1] ---linux (ftpserve

ip:172.16.0.0/24 172.16.0.0/16 192.168.0.0/24 192.168.0.10/24

三、ftp配置: 

# vi /etc/vsftpd/vsftpd.conf

pasv_enable=YES

pasv_min_port=3000

pasv_max_port=4000

四、防火墙配置

#!/bin/bash
  
#ip.sh

echo "1" >/proc/sys/net/ipv4/ip_forward

modprobe ip_conntrack_ftp
  
modprobe ip_nat_ftp
  
iptables -F
  
iptables -X
  
iptables -Z
  
iptables -t nat -F
  
iptables -t nat -X
  
iptables -t nat -Z

iptables -P INPUT ACCEPT
  
iptables -P OUTPUT ACCEPT
  
iptables -P FORWARD DROP

iptables -t filter -A FORWARD -p tcp -s 172.16.0.0/16 -d 192.168.0.10 -dport 21 -j ACCEPT
  
iptables -t filter -A FORWARD -p tcp -s 192.168.0.10 -sport 21 -j ACCEPT
  
iptables -t filter -A FORWARD -p tcp -s 172.16.0.0/16 -d 192.168.0.10 -dport 3000:4000 -j ACCEPT
  
iptables -t filter -A FORWARD -p tcp -s 192.168.0.10 -sport 3000:4000 -j ACCEPT
  
iptables -t filter -A FORWARD -p tcp -m state -state RELATED,ESTABLISHED -j ACCEPT
  
iptables -t filter -A FORWARD -p icmp -icmp-type 8 -j ACCEPT
  
iptables -t filter -A FORWARD -p icmp -icmp-type 0 -j ACCEPT

五、验证: 

# 在xp下用ftp命令连接，都是采用主动模式连接，可以采用图形界面的软件，默认一般为被动模式。

# netstat -an|grep 172