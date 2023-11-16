---
title: ss command
author: "-"
date: 2019-01-08T13:44:55+00:00
url: ss
categories:
  - network
tags:
  - reprint
---
## ss command

## ss, Socket Statistics

   ss -ntlp
   ss -ntp
   ss -nxlp
   ss -nxp

ss 是 Socket Statistics 的缩写。ss 命令可以用来获取 socket 统计信息，它显示的内容和 netstat 类似。但 ss 的优势在于它能够显示更多更详细的有关 TCP 和连接状态的信息，而且比 netstat 更快。当服务器的 socket 连接数量变得非常大时，无论是使用 netstat 命令还是直接 cat /proc/net/tcp，执行速度都会很慢。ss 命令利用到了 TCP 协议栈中 tcp_diag。tcp_diag 是一个用于分析统计的模块，可以获得 Linux 内核中第一手的信息，因此 ss 命令的性能会好很多。

常用选项
-h, --help 帮助
-V, --version  显示版本号
-t, --tcp 显示 TCP 协议的 sockets
-u, --udp 显示 UDP 协议的 sockets
-x, --unix 显示 unix domain sockets，与 -f 选项相同
-n, --numeric 不解析服务的名称，如 "22" 端口不会显示成 "ssh"
-l, --listening 只显示处于监听状态的端口
-p, --processes 显示监听端口的进程(Ubuntu 上需要 sudo)
-a, --all 对 TCP 协议来说，既包含监听的端口，也包含建立的连接
-r, --resolve 把 IP 解释为域名，把端口号解释为协议名称

[https://www.cnblogs.com/sparkdev/p/8421897.html](https://www.cnblogs.com/sparkdev/p/8421897.html)

网络状态工具

ss 是 iproute2 包附带的一个查询 socket 有关的统计信息的工具, 它的功能跟 netstat 类似, 比netstat更快速更高效.当服务器的socket连接数量变得非常大时，无论是使用 `netstat` 命令还是直接 `cat /proc/net/tcp`，执行速度都会很慢。ss快的秘诀在于，它利用到了TCP协议栈中tcp_diag。tcp_diag是一个用于分析统计的模块，可以获得Linux 内核中第一手的信息，这就确保了ss的快捷高效。当然，如果你的系统中没有tcp_diag，ss也可以正常运行，只是效率会变得稍慢。

```bash
# 语法: ss [options] [ FILTER ]
# FILTER := [ state STATE-FILTER ] [ EXPRESSION ]

ss -ntl # tcp port
ss -nul # udp port

ss -nul4 # udp port  -ipv4
ss -nul6 # udp port -ipv6

ss state established

# 统计各种状态的连接数量
ss -s
# 列出当前监听端口
ss -l
```

### option

- -n, --numeric   不解析服务名称
- -t, --tcp       仅显示 TCP sockets
- -u, --udp       仅显示 UCP sockets
- -l, --listening 显示监听状态的 sockets
- -o, --options   显示计时器信息, 连接时间
- -s, -summary show socket usage summary

### ss tcp states

- established
- syn-sent
- syn-recv
- fin-wait-1
- fin-wait-2
- time-wait
- closed
- close-wait
- last-ack
- listen
- closing

>[http://www.ttlsa.com/linux-command/ss-replace-netstat/](http://www.ttlsa.com/linux-command/ss-replace-netstat/)

## Recv-Q, Send-Q

LISTEN 状态：

Recv-Q 表示当前 listen backlog 队列中的连接数目 (等待用户调用 accept() 获取的、已完成 3 次握手的 socket 连接数量），而 Send-Q 表示了 listen socket 最大能容纳的 backlog ，即 min(backlog, somaxconn) 值。
非 LISTEN 状态：Recv-Q 表示了 receive queue 中存在的字节数目；Send-Q 表示 send queue 中存在的字节数；

    strace -s 128 ss -nat
    // Recv-Q, 等待接收的下一个 tcp 段的序号 - 尚未从内核空间 copy 到用户空间的段最前面的一个序号
    // Send-Q, 已加入发送队列中的 tcp 段的最后一个序号 - 已发送但尚未确认的最早一个序号

>[https://github.com/moooofly/MarkSomethingDown/blob/master/Linux/%E5%85%B3%E4%BA%8E%20Recv-Q%20%E5%92%8C%20Send-Q%20%E7%9A%84%E8%AF%B4%E6%98%8E.md](https://github.com/moooofly/MarkSomethingDown/blob/master/Linux/%E5%85%B3%E4%BA%8E%20Recv-Q%20%E5%92%8C%20Send-Q%20%E7%9A%84%E8%AF%B4%E6%98%8E.md)

---

ss 命令用于显示 socket 状态. 可以显示 PACKET sockets, TCP sockets, UDP sockets, DCCP sockets, RAW sockets, Unix domain sockets 等等统计. 它比其他工具展示等多tcp和state信息. 它是一个非常实用、快速、有效的跟踪IP连接和sockets的新工具.SS命令可以提供如下信息:

所有的 TCP sockets
  
所有的 UDP sockets
  
所有 ssh/ftp/ttp/https 持久连接
  
所有连接到 Xserver 的本地进程
  
使用 state (例如: connected, synchronized, SYN-RECV, SYN-SENT,TIME-WAIT) 、地址、端口过滤
  
所有的 state FIN-WAIT-1 tcpsocket 连接以及更多
  
很多流行的 Linux 发行版都支持 ss 以及很多监控工具使用 ss 命令. 熟悉这个工具有助于您更好的发现与解决系统性能问题.

netstat, ss 命令对比, 统计服务器并发连接数

netstat

    time netstat -ant | grep EST | wc -l

    3100
    real 0m12.960s
    user 0m0.334s
    sys 0m12.561s

    time ss -o state established | wc -l

    3204
    real 0m0.030s 
    user 0m0.005s
    sys 0m0.026s

    time netstat -ant | grep EST | wc -l

    3100
    real 0m12.960s
    user 0m0.334s
    sys 0m12.561s

    time ss -o state established | wc -l

    3204
    real 0m0.030s
    user 0m0.005s
    sys 0m0.026s

结果很明显ss 性能更好一些

### 常用ss命令

ss -l 显示本地打开的所有端口
  
ss -pl 显示每个进程具体打开的socket
  
ss -t -a 显示所有tcp socket
  
ss -u -a 显示所有的UDP Socekt
  
ss -o state established '( dport = :smtp or sport = :smtp )' 显示所有已建立的SMTP连接
  
ss -o state established '( dport = :http or sport = :http )' 显示所有已建立的HTTP连接
  
ss -x src /tmp/.X11-unix/* 找出所有连接X服务器的进程
  
ss -s 列出当前socket详细信息:
  
ss -l 显示本地打开的所有端口
  
ss -pl 显示每个进程具体打开的socket
  
ss -t -a 显示所有tcp socket
  
ss -u -a 显示所有的UDP Socekt
  
ss -o state established '( dport = :smtp or sport = :smtp )' 显示所有已建立的SMTP连接
  
ss -o state established '( dport = :http or sport = :http )' 显示所有已建立的HTTP连接
  
ss -x src /tmp/.X11-unix/* 找出所有连接X服务器的进程
  
ss列出每个进程名及其监听的端口

# ss -pl

# ss -pl

ss列所有的tcp sockets

# ss -t -a

# ss -t -a

ss列出所有udp sockets

# ss -u -a

# ss -u -a

ss列出所有http连接中的连接

# ss -o state established '( dport = :http or sport = :http )'

# ss -o state established '( dport = :http or sport = :http )'

·以上包含对外提供的80,以及访问外部的80
  
·用以上命令完美的替代netstat获取http并发连接数,监控中常用到

ss列出本地哪个进程连接到x server

# ss -x src /tmp/.X11-unix/*

# ss -x src /tmp/.X11-unix/*

ss列出处在FIN-WAIT-1状态的http、https连接

   ss -o state fin-wait-1 '( sport = :http or sport = :https )'

    ss -o state fin-wait-1 '( sport = :http or sport = :https )'

all : All of the above states
  
connected : All the states except for listen and closed
  
synchronized : All the connected states except for syn-sent
  
bucket : Show states, which are maintained as minisockets, i.e. time-wait and syn-recv.
  
big : Opposite to bucket state.

connected : All the states except for listen and closed
  
synchronized : All the connected states except for syn-sent
  
bucket : Show states, which are maintained as minisockets, i.e. time-wait and syn-recv.
  
big : Opposite to bucket state.
  
ss使用IP地址筛选

ss src ADDRESS_PATTERN
  
src: 表示来源
  
ADDRESS_PATTERN: 表示地址规则

如下:
  
ss src 120.33.31.1 # 列出来之20.33.31.1的连接

＃列出来至120.33.31.1,80端口的连接
  
ss src 120.33.31.1:http
  
ss src 120.33.31.1:80
  
ss src ADDRESS_PATTERN
  
src: 表示来源
  
ADDRESS_PATTERN: 表示地址规则

如下:
  
ss src 120.33.31.1 # 列出来之20.33.31.1的连接

＃列出来至120.33.31.1,80端口的连接
  
ss src 120.33.31.1:http
  
ss src 120.33.31.1:80
  
ss使用端口筛选

ss dport OP PORT
  
OP:是运算符
  
PORT: 表示端口
  
dport: 表示过滤目标端口、相反的有sport
  
ss dport OP PORT
  
OP:是运算符
  
PORT: 表示端口
  
dport: 表示过滤目标端口、相反的有sport
  
OP运算符如下:

<= or le : 小于等于 >= or ge : 大于等于
  
== or eq : 等于
  
!= or ne : 不等于端口
  
< or lt : 小于这个端口 > or gt : 大于端口
  
<= or le : 小于等于 >= or ge : 大于等于
  
== or eq : 等于
  
!= or ne : 不等于端口
  
< or lt : 小于这个端口 > or gt : 大于端口
  
OP实例

ss sport = :http 也可以是 ss sport = :80
  
ss dport = :http
  
ss dport > :1024
  
ss sport > :1024
  
ss sport \< :32000
  
ss sport eq :22
  
ss dport != :22
  
ss state connected sport = :http
  
ss ( sport = :http or sport = :https )
  
ss -o state fin-wait-1 ( sport = :http or sport = :https ) dst 192.168.1/24
  
ss sport = :http 也可以是 ss sport = :80
  
ss dport = :http
  
ss dport > :1024
  
ss sport > :1024
  
ss sport \< :32000
  
ss sport eq :22
  
ss dport != :22
  
ss state connected sport = :http
  
ss ( sport = :http or sport = :https )
  
ss -o state fin-wait-1 ( sport = :http or sport = :https ) dst 192.168.1/24
  
为什么ss比netstat快:
  
netstat是遍历/proc下面每个PID目录,ss直接读/proc/net下面的统计信息。所以ss执行的时候消耗资源以及消耗的时间都比netstat少很多

ss命令帮助

# ss -h

Usage: ss [ OPTIONS ]

ss [ OPTIONS ] [ FILTER ]

-h, -help this message

-V, -version output version information

-n, -numeric don't resolve service names

-r, -resolve resolve host names

-a, -all display all sockets

-l, -listening display listening sockets

-o, -options show timer information

-e, -extended show detailed socket information

-m, -memory show socket memory usage

-p, -processes show process using socket

-i, -info show internal TCP information

-s, -summary show socket usage summary

-4, -ipv4 display only IP version 4 sockets

-6, -ipv6 display only IP version 6 sockets

-0, -packet display PACKET sockets

-t, -tcp display only TCP sockets

-u, -udp display only UDP sockets

-d, -dccp display only DCCP sockets

-w, -raw display only RAW sockets

-x, -unix display only Unix domain sockets

-f, -family=FAMILY display sockets of type FAMILY

-A, -query=QUERY, -socket=QUERY

QUERY := {all|inet|tcp|udp|raw|unix|packet|netlink}[,QUERY]

-D, -diag=FILE Dump raw information about TCP sockets to FILE

-F, -filter=FILE read filter information from FILE

FILTER := [ state TCP-STATE ] [ EXPRESSION ]
  
32

# ss -h

Usage: ss [ OPTIONS ]

ss [ OPTIONS ] [ FILTER ]

-h, -help this message

-V, -version output version information

-r, -resolve resolve host names

-a, -all display all sockets
-e, -extended show detailed socket information

-m, -memory show socket memory usage

-p, -processes show process using socket

-i, -info show internal TCP information

-4, -ipv4 display only IP version 4 sockets

-6, -ipv6 display only IP version 6 sockets

-0, -packet display PACKET sockets

-t, -tcp display only TCP sockets

-u, -udp display only UDP sockets

-d, -dccp display only DCCP sockets

-w, -raw display only RAW sockets

-x, -unix display only Unix domain sockets

-f, -family=FAMILY display sockets of type FAMILY

-A, -query=QUERY, -socket=QUERY

QUERY := {all|inet|tcp|udp|raw|unix|packet|netlink}[,QUERY]

-D, -diag=FILE Dump raw information about TCP sockets to FILE

-F, -filter=FILE read filter information from FILE

FILTER := [ state TCP-STATE ] [ EXPRESSION ]
  
参考: [http://www.cyberciti.biz/tips/linux-investigate-sockets-network-connections.html](http://www.cyberciti.biz/tips/linux-investigate-sockets-network-connections.html)
  
转摘请注明出处: Linux网络状态工具ss命令详解 [http://www.ttlsa.com/html/2070.html](http://www.ttlsa.com/html/2070.html)

>[https://wangchujiang.com/linux-command/c/ss.html](https://wangchujiang.com/linux-command/c/ss.html)
