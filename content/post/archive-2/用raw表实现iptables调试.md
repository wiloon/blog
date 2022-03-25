---
title: iptables 调试, raw表, LOG
author: "-"
date: 2018-04-09T16:04:45+00:00
url: iptables/log
categories:
  - network

tags:
  - reprint
  - remix
---
## iptables调试, raw表, LOG

### 启用iptables的日志

```bash
iptables -t nat -A POSTROUTING -p icmp  -s 192.168.50.215 -j LOG --log-prefix 'iptable-log: '
iptables -t nat -I PREROUTING -p tcp -s 192.168.50.115 --dport 80 -j LOG --log-prefix 'iptable-log: '

# 配置日志级别
iptables -t raw -I OUTPUT -d 10.254.51.153 -j LOG --log-level 7 --log-prefix "raw out: "
```

raw 表使用 PREROUTING 和 OUTPUT 两个链, 因此 raw 可以覆盖所有包。在raw表中支持一个特殊的目标:TRACE,使内核记录下每条匹配该包的对应iptables规则信息。使用raw表内的TRACE target即可实现对iptables规则的跟踪调试。

配置
  
假设需要对ipv4的ICMP包进行跟踪调试,抓取所有流经本机的ICMP包

```bash
iptables -t raw -A OUTPUT -p icmp -j TRACE
iptables -t raw -A PREROUTING -p icmp -j TRACE
```

加载对应内核模块

```bash
modprobe ipt_LOG
modprobe xt_LOG
```

日志输出在journalctl 里查看, 用journalctl -f 查看调试日志。

#### TRACE
TRACE This target marks packes so that the kernel will log every rule which match the packets as those traverse the tables, chains, rules. (The ipt_LOG or ip6t_LOG module is required for the logging.) The packets are logged with the string prefix:

"TRACE: tablename:chainname:type:rulenum " where type can be "rule" for plain rule, "return" for implicit rule at the end of a user defined chain and "policy" for the policy of the built in chains. It can only be used in the raw table.

policy 是指iptables内置的规则如: accept
  
policy 会跟用户定义的rule放在一起排序,如果用户定义了6条规则,那么链默认的accept 规则的number会是7, 日志里会打印成policy:7

for openwrt > iptables

```bash
# install raw table for iptables
opkg install kmod-ipt-raw

#build kmod-ipt-debug as module which provides the iptables TRACE target

iptables -t raw -j TRACE -p tcp -d 216.58.193.196 -I PREROUTING 1
iptables -t raw -I PREROUTING 1 -p tcp -d 216.58.193.196 -j TRACE
```

调试
  
在vm内对外部作ping操作,vm的ip为10.0.0.4

[root@10-0-0-4 ~]# ping -c 1 192.168.0.19
  
PING 192.168.0.19 (192.168.0.19)56(84) bytes of data.
  
- 192.168.0.19 ping statistics -1 packets transmitted, 0 received, 100% packet loss, time 0ms
  
在/var/log/kern.log中的对应调试信息如下

Apr 1811:50:23 openstack-network kernel: [1038991.870882] TRACE: raw:PREROUTING:policy:2IN=tap5c42978b-ac OUT= MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=64ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870902] TRACE: nat:PREROUTING:rule:1IN=tap5c42978b-ac OUT= MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=64ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870909] TRACE: nat:quantum-l3-agent-PREROUTING:return:4IN=tap5c42978b-ac OUT= MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=64ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870915] TRACE: nat:PREROUTING:policy:2IN=tap5c42978b-ac OUT= MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=64ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870938] TRACE: filter:FORWARD:rule:1IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870944] TRACE: filter:quantum-filter-top:rule:1IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870950] TRACE: filter:quantum-l3-agent-local:return:1IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870957] TRACE: filter:quantum-filter-top:return:2IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870962] TRACE: filter:FORWARD:rule:2IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870969] TRACE: filter:quantum-l3-agent-FORWARD:return:1IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870974] TRACE: filter:FORWARD:policy:3IN=tap5c42978b-ac OUT=br-ex MAC=fa:16:3e:a7:0c:f3:fa:16:3e:a4:49:14:08:00 SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870979] TRACE: nat:POSTROUTING:rule:1IN= OUT=br-ex SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
Apr 1811:50:23 openstack-network kernel: [1038991.870985] TRACE: nat:quantum-l3-agent-POSTROUTING:rule:1IN= OUT=br-ex SRC=10.0.0.4 DST=192.168.0.19 LEN=84TOS=0x00 PREC=0x00 TTL=63ID=0 DF PROTO=ICMP TYPE=8CODE=0ID=28976SEQ=1
  
可见数据包流在nat表的quantum-l3-agent-POSTROUTING的第一条规则处被截断了,查看iptables中的nat表的规则如下

*nat
  
:PREROUTING ACCEPT [99:21975]
  
:INPUT ACCEPT [74:20608]
  
:OUTPUT ACCEPT [181:30548]
  
:POSTROUTING ACCEPT [26:13022]
  
:quantum-l3-agent-OUTPUT - [0:0]
  
:quantum-l3-agent-POSTROUTING - [0:0]
  
:quantum-l3-agent-PREROUTING - [0:0]
  
:quantum-l3-agent-float-snat - [0:0]
  
:quantum-l3-agent-snat - [0:0]
  
:quantum-postrouting-bottom - [0:0]-A PREROUTING -j quantum-l3-agent-PREROUTING
  
-A OUTPUT -j quantum-l3-agent-OUTPUT
  
-A POSTROUTING -j quantum-l3-agent-POSTROUTING
  
-A POSTROUTING -j quantum-postrouting-bottom
  
-A quantum-l3-agent-OUTPUT -d 192.168.0.16/32-j DNAT -to-destination 10.0.0.4
  
-A quantum-l3-agent-OUTPUT -d 192.168.0.17/32-j DNAT -to-destination 10.0.0.3
  
-A quantum-l3-agent-POSTROUTING !-i qg-91757ded-c4 !-o qg-91757ded-c4 -m conntrack !-ctstate DNAT -j ACCEPT
  
-A quantum-l3-agent-POSTROUTING -s 10.0.0.0/24-d 192.168.1.1/32-j ACCEPT
  
-A quantum-l3-agent-PREROUTING -d 169.254.169.254/32-p tcp -m tcp -dport80-j DNAT -to-destination 192.168.1.1:8775-A quantum-l3-agent-PREROUTING -d 192.168.0.16/32-j DNAT -to-destination 10.0.0.4
  
-A quantum-l3-agent-PREROUTING -d 192.168.0.17/32-j DNAT -to-destination 10.0.0.3
  
-A quantum-l3-agent-float-snat -s 10.0.0.4/32-j SNAT -to-source 192.168.0.16
  
-A quantum-l3-agent-snat -j quantum-l3-agent-float-snat
  
-A quantum-l3-agent-snat -s 10.0.0.0/24-j SNAT -to-source 192.168.0.15
  
-A quantum-postrouting-bottom -j quantum-l3-agent-snat
  
COMMIT
  
确定有问题的规则为

-A quantum-l3-agent-POSTROUTING !-i qg-91757ded-c4 !-o qg-91757ded-c4 -m conntrack !-ctstate DNAT -j ACCEPT
  
把这条规则删掉后重启iptables,vm能顺利连接外网,问题解决。

https://www.howtoing.com/enable-logging-in-iptables-on-linux


  
    iptables debugging
  


https://backreference.org/2010/06/11/iptables-debugging/embed/#?secret=GkDsoEKKiO
  
http://blog.51cto.com/flymanhi/1276331
  
http://blog.youlingman.info/debugging-iptables-with-raw-table/