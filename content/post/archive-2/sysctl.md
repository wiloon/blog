---
title: sysctl
author: "-"
date: 2018-08-24T09:42:15+00:00
url: sysctl

---
## sysctl
### archlinux
systemd-sysctl 服务在启动时会加载/etc/sysctl.d/*.conf, 配置内核参数

/etc/sysctl.conf 不起作用

sysctl命令被用于在内核运行时动态地修改内核的运行参数,可用的内核参数在目录/proc/sys中。它包含一些TCP/ip堆栈和虚拟内存系统的高级选项,用sysctl可以读取设置超过五百个系统变量。
  
CentOS 5 supported the placement of sysctl directives in files under /etc/sysctl.d/ . The code is within /etc/init.d/functions

    sysctl [options] [variable[=value] …]
    -a: 打印所有内核参数变量
    -n: 打印时只打印值,不打印参数名称；
    -e: 忽略未知关键字错误；
    -N: 打印时只打印参数名称,不打印值；
    -w: 设置参数的值（不过好像不加这个选项也可以直接设置)
    -p: 从配置文件"/etc/sysctl.conf"加载内核参数设置
    -A: 以表格方式打印所有内核参数变量。

### 查看变量
```bash
# 查看变量
sysctl -a |grep tcp_syn_retrie
```
### 设置内核参数
在 /etc/sysctl.d/ 下创建 foo.conf, 填写参数值
```bash
net.core.rmem_max=2097152
```
### 加载文件使其生效
```bash
# load one file
sysctl -p /etc/sysctl.d/foo.conf
sysctl --load=/etc/sysctl.d/foo.conf
```

```bash
# To load all configuration files manually
sysctl --system

sysctl tcp_syn_retrie
sysctl -w net.ipv4.tcp_synack_retries=5
# 从配置文件加载内核参数设置
sysctl -p /etc/sysctl.conf
sysctl --system
```

sysctl -w xxx_tcp_syn_retrie =0 时 不会生效。保持原值

### fs.file-max
    所有用户打开文件描述符的总和  
    系统级文件描述符数限制。直接修改这个参数和<<linux 最大文件描述符>>中修改方法有相同的效果（不过这些都是临时修改) 。一般修改/proc/sys/fs/file-max 后,应用程序需要把/proc/sys/fs/inode-max 设置为/proc/sys/fs/fs/file-max 值的3-4倍,否则可能导致inode数不够用。 
### kernel.core_uses_pid**

即使core_pattern中没有设置%p,最后生成的core dump文件名仍会加上进程ID。

#### /proc/sys/fs/inode-max
This  file  contains  the  maximum  number of in-memory inodes.  On some (2.4) systems, it may not be
              present. This value should be 3-4 times larger than the value in file-max, since  stdin,  stdout  and
              network  sockets also need an inode to handle them. When you regularly run out of inodes, you need to
              increase this value.

  * kernel.msgmax
  
    从一个进程发送到另一个进程的消息的最大长度（bytes) 。进程间的消息传递是在内核的内存中进行的,不会交换到磁盘上,所以如果增加该值,则将增加操作系统所使用的内存数量。

  * kernel.msgmnb
  
    消息队列的最大长度（bytes) 

  * kernel.shmall
  
    系统上可以使用的共享内存的总量（bytes) 。

  * kernel.shmmax
  
    内核所允许的最大共享内存段的大小（bytes) 。

  * kernel.sysrq
  
    启用SsyRq

  * net.ipv4.conf.all.promote_secondaries

  * net.ipv4.conf.default.promote_secondaries
  
    命​名​地​址​迁​移​。​它​允​许​第​二​个​IPv4地​址​迁​移​为​主​地​址​。​通​常​,主​地​址​被删除时,第二地址也被删除。启用了新的sysctl键net.ipv4.conf.all.promote_secondaries(或接口特定的变量之一)后,这样做将使第二地址成为新的主地址。
  
    0: 当接口的主IP地址被移除时,删除所有次IP地址
  
    1: 当接口的主IP地址被移除时,将次IP地址提升为主IP地址

  * net.ipv4.conf.all.rp_filt

  * net.ipv4.conf.default.rp_filte
  
    1: 通过反向路径回溯进行源地址验证(在RFC1812中定义)。对于单穴主机和stub网络路由器推荐使用该选项。
  
    0: 不通过反向路径回溯进行源地址验证。

  * net.ipv4.conf.all.send_redirects
  
    允许发送重定向消息。(路由使用)
  
    0: 禁止
  
    1: 允许

  * net.ipv4.conf.default.accept_source_route
  
    接收带有SRR选项的数据报。主机设为0,路由设为1

  * net.ipv4.conf.all.accept_redirects = 0

  * net.ipv4.conf.default.accept_redirects = 0
  
    These commands disable acceptance of all ICMP redirected packets on all interfaces:

  * net.ipv4.conf.all.secure_redirects = 0

  * net.ipv4.conf.default.secure_redirects = 0
  
    This command disables acceptance of secure ICMP redirected packets on all interfaces:

关闭重定向。如果主机所在的网络有多个路由器,你将其中一个设为缺省网关,但该网关在收到你的ip包时,发现该ip包必须经过另外一个路由器,于是该网关就給你的主机发一个"重定向"的icmp包,告诉主机把包转发到另外一个路由器。1表示主机接受这样的重定向包,0表示忽略；linux默认是1,可以设位0以消除隐患。
  
是否接受ICMP转发

#忽略所有接收到的icmp echo请求的广播
  
#0: 不忽略
  
#1: 忽略
  
net.ipv4.icmp_echo_ignore_broadcasts

  * net.ipv4.ip_forward
  * net.ipv4.conf.all.forwarding
  
    ipv4的IP转发。0: 禁止, 1: 打开

本地发起连接时使用的端口范围,tcp初始化时会修改此值

net.ipv4.ip_local_port_range

#本端断开的socket连接,TCP保持在FIN-WAIT-2状态的时间。对方可能会断开连接或一直不结束连接或不可预料的进程死亡。默认值为 60 秒。过去在2.2版本的内核中是 180 秒。您可以设置该值,但需要注意,如果您的机器为负载很重的web服务器,您可能要冒内存被大量无效数据报填满的风险,FIN-WAIT-2 sockets 的危险性低于 FIN-WAIT-1,因为它们最多只吃 1.5K 的内存,但是它们存在时间更长。
  
net.ipv4.tcp_fin_timeout

#表示从最后一个包结束后多少秒内没有活动,才发送keepalive包保持连接,默认7200s,理想可设为1800s,即如果非正常断开,1800s后可通过keepalive知道。
  
net.ipv4.tcp_keepalive_time

### net.ipv4.tcp_max_syn_backlog
  
对于那些依然还未获得客户端确认的连接请求,需要保存在队列中最大数目。默认值是1024,可提高到2048。
  
    指定listen监听队列里,能够转移至ESTABLISHED或者SYN_RCVD状态的socket的最大数目。

#系统在同时所处理的最大timewait sockets 数目。如果超过此数的话,time-wait socket 会被立即砍除并且显示警告信息。
  
#Bug-to-bug compatibility with some broken printers.
      
On retransmit try to send bigger packets to work around bugs in
      
certain TCP stacks.
  
net.ipv4.tcp_max_tw_buckets

#表示本机向外发起TCP SYN连接超时重传的次数,不应该高于255；该值仅仅针对外出的连接,对于进来的连接由tcp_retries1控制。
  
net.ipv4.tcp_syn_retries

#对于远端的连接请求SYN,内核会发送SYN + ACK数据报,以确认收到上一个 SYN连接请求包。
  
这是所谓的三次握手.这里决定内核在放弃连接之前所送出的 SYN+ACK 数目.
  
net.ipv4.tcp_synack_retries

  * net.ipv4.tcp_syncookies
  
    net.ipv4.tcp_syncookies = 1 表示开启SYN Cookies。当出现SYN等待队列溢出时,启用cookies来处理,可防范少量SYN攻击,默认为0,表示关闭；
  
    表示是否打开TCP同步标签(syncookie),内核必须打开了 CONFIG_SYN_COOKIES项进行编译。同步标签(syncookie)可以防止一个套接字在有过多试图连接到达时引起过载。
  
    指定是否打开TCP同步标签。同步标签通过启动cookie 来防止一个监听socket因不停的重复接收来自同一个地址的连接请求（同步报文段) ,而导致listen监听队列溢出（所谓的SYN 风暴) 。
  
    0: 关闭
  
    1: 打开 
### fs.inotify.max_user_watches
同一用户同时可以添加的watch数目（watch一般是针对目录,决定了同时同一用户可以监控的目录数量) 

表示是否启用以一种比超时重发更精确的方法（请参阅 RFC 1323) 来启用对 RTT 的计算；为了实现更好的性能应该启用这个选项。
  
0: 不启用
  
1: 启用

```bash
# Increasing the amount of inotify watchers
#archlinux
echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl -system
```

### net.ipv4.tcp_timestamps

  * net.ipv4.tcp_tw_recycle
  
    打开快速 TIME-WAIT sockets 回收。能够更快地回收TIME-WAIT套接字。除非得到技术专家的建议或要求,请不要随意修改这个值。
  * /proc/sys/net/ipv4/tcp_tw_reuse
  
    表示是否允许将处于TIME-WAIT状态的socket（TIME-WAIT的端口) 用于新的TCP连接 。
  
    表示是否允许重新应用处于TIME-WAIT状态的socket用于新的TCP连接。
  
    0: 关闭
  
    1: 打开

arp通知链操作
  
0: 不做任何操作
  
1: 当设备或硬件地址改变时自动产生一个arp请求
  
net.ipv4.conf.all.arp_notify
  
net.ipv4.conf.default.arp_notify

是否禁用ipv6
  
0: 不禁用
  
1: 禁用
  
net.ipv6.conf.all.disable_ipv6

  * debug.panic_on_rcu_stall
  
    The kernel.panic_on_rcu_stall sysctl is disabled by default. 
### fs.aio-nr
aio-nr shows the current system-wide number of asynchronous io requests.

### aio-max-nr
异步 I/O 请求数的最大范围  
aio-max-nr  
allows you to change the maximum value/proc/sys/fs/aio-nr can grow to.

### fs.epoll.max_user_watches
允许并发请求的最大数量,一般是65536（即64KB,对大部分程序来说已经足够了) 。

  * fs.epoll.max_user_watches
  
    用户能够往epoll 内核事件表注册的事件总量。 它是指该用户打开的所有epoll实例总共能监听的事件数目,而不是单个epoll实例能监听的事件数目。往epoll内核事件表中注册一个事件,在32位系统上大概消耗90字节的内核空间,在64位系统上则消耗160字节的内核空间。所以,这个内核参数限制了epoll使用的内核内存总量。

  * net.ipv4.tcp_rmem
    它包含了3个值,分别指定一个socket的TCP读缓存区的最小值、默认值和最大值。

### net.core.somaxconn
定义了系统中每一个端口最大的监听队列的长度,这是个全局的参数。  
对于一个TCP连接,Server与Client需要通过三次握手来建立网络连接.当三次握手成功后,
我们可以看到端口的状态由LISTEN转变为ESTABLISHED,接着这条链路上就可以开始传送数据了.
每一个处于监听(Listen)状态的端口,都有自己的监听队列.监听队列的长度,与如下两方面有关:
- somaxconn参数.
- 使用该端口的程序中listen()函数.

　　1. 关于somaxconn参数:

　　定义了系统中每一个端口最大的监听队列的长度,这是个全局的参数,默认值为128,具体信息为:

　　Purpose:

　　Specifies the maximum listen backlog.

　　Values:

　　Default: 128 connections

　　Range: 0 to MAXSHORT

　　Type: Connect

　　Diagnosis:

　　N/A

　　Tuning

　　Increase this parameter on busy Web servers to handle peak connection rates.

　　看下FREEBSD的解析: 

　　限制了接收新 TCP 连接侦听队列的大小。对于一个经常处理新连接的高负载 web服务环境来说,默认的 128 太小了。大多数环境这个值建议增加到 1024 或者更多。 服务进程会自己限制侦听队列的大小(例如 sendmail(8) 或者 Apache),常常在它们的配置文件中有设置队列大小的选项。大的侦听队列对防止拒绝服务 DoS 攻击也会有所帮助。


Let's consider a TCP-handshake.. tcp_max_syn_backlog represents the maximal number of connections in SYN_RECV queue. I.e. when your server received SYN, sent SYN-ACK and haven't received ACK yet. This is a separate queue of so-called "request sockets" - reqsk in code (i.e. not fully-fledged sockets, "request sockets" occupy less memory. In this state we can save some memory and not yet allocate a full socket because the full connection may not be at all in the future if ACK will not arrive). The value of this queue is affected (see this post) by listen()'s backlog argument and limited by tcp_max_syn_backlog in kernel.

somaxconn represents the maximal size of ESTABLISHED queue. This is another queue.
Recall the previously mentioned SYN_RECV queue - your server is waiting for ACK from client. When the ACK arrives the kernel roughly speaking makes the big full-fledged socket from "request socket" and moves it to ESTABLISHED queue. Then you can do accept() on this socket. This queue is also affected by listen()'s backlog argument and limited by somaxconn in kernel.


### fs.mount-max
  
    number of mounts allowed per mount namespace

  * fs.nfs.idmap_cache_timeout
  
    设置idmapper缓存项的最大寿命,单位是秒
  
    <http://blog.wiloon.com/?p=12603>

  * fs.nfs.nfs_callback_tcpport

  * fs.nr_open
  
    单个进程可分配的最大文件数
  * fs.file_max
  
    内核可分配的最大文件数

  * /proc/sys/net/nf_conntrack_max
  
    当nf_conntrack模块被装置且服务器上连接超过这个设定的值时,系统会主动丢掉新连接包,直到连接小于此设置值才会恢复。

  * /proc/sys/net/ipv4/tcp_mem
  
    确定TCP栈应该如何反映内存使用,每个值的单位都是内存页（通常是4KB) 。第一个值是内存使用的下限；第二个值是内存压力模式开始对缓冲区使用应用压力的上限；第三个值是内存使用的上限。在这个层次上可以将报文丢弃,从而减少对内存的使用。对于较大的BDP可以增大这些值（注意,其单位是内存页而不是字节) 。
  * /proc/sys/net/ipv4/tcp_rmem
  
    为自动调优定义socket使用的内存。第一个值是为socket接收缓冲区分配的最少字节数；第二个值是默认值（该值会被rmem_default覆盖) ,缓冲区在系统负载不重的情况下可以增长到这个值；第三个值是接收缓冲区空间的最大字节数（该值会被rmem_max覆盖) 。
  * /proc/sys/net/ipv4/tcp_wmem
  
    为自动调优定义socket使用的内存。第一个值是为socket发送缓冲区分配的最少字节数；第二个值是默认值（该值会被wmem_default覆盖) ,缓冲区在系统负载不重的情况下可以增长到这个值；第三个值是发送缓冲区空间的最大字节数（该值会被wmem_max覆盖) 。

### net.core.rmem_max, /proc/sys/net/core/rmem_max

最大的TCP数据接收窗口（字节) 。  
默认的和最大的接收数据包内存大小  
大多数的 Linux 中 rmem_max 和 wmem_max 被分配的值为 128 k，在一个低延迟的网络环境中，或者是 apps 比如 DNS、Web Server，这或许是足够的。尽管如此，如果延迟太大，默认的值可能就太小了

需要设置 minimum size, initial size, and maximum size in bytes:

```bash
echo 'net.ipv4.tcp_rmem= 10240 87380 12582912' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem= 10240 87380 12582912' >> /etc/sysctl.conf
```
quic-go 建议设置的值是 net.ipv4.tcp_rmem=2048kiB
>https://github.com/lucas-clemente/quic-go/wiki/UDP-Receive-Buffer-Size
>https://zhuanlan.zhihu.com/p/89620832

UDP中SO_RCVBUF与内核中/proc/sys/net/core/rmem_default对应，SO_SNDBUF与/proc/sys/net/core/wmem_default对应。  
而TCP中SO_RCVBUF与内核中/proc/sys/net/ipv4/tcp_rmem 的第二项default对应，SO_SNDBUF与/proc/sys/net/ipv4/tcp_wmem的第二项default对应。  (可能是操作系统实现的差异?)
SO_RCVBUF来设置接收缓冲区，该参数在设置的时候不会与rmem_max进行对比校验，但是如果设置的大小超过rmem_max的话，则超过rmem_max的部分不会生效；  
rmem_max参数是整个系统的大小，不是单个socket的大小。  
>https://www.cnblogs.com/scaugsh/p/10254483.html

如果指定了tcp_wmem，则net.core.wmem_default被tcp_wmem的覆盖。send Buffer在tcp_wmem的最小值和最大值之间自动调整。如果调用setsockopt()设置了socket选项SO_SNDBUF，将关闭发送端缓冲的自动调节机制，tcp_wmem将被忽略，SO_SNDBUF的最大值由net.core.wmem_max限制。
>https://zhuanlan.zhihu.com/p/89620832


### net.core.rmem_default
### wmem
默认情况下Linux系统会自动调整这个buffer（net.ipv4.tcp_wmem）, 也就是不推荐程序中主动去设置SO_SNDBUF，除非明确知道设置的值是最优的。
### /proc/sys/net/core/wmem_max, /proc/sys/net/core/wmem_default
  
    最大的TCP数据发送窗口（字节) 。
    默认的和最大的发送数据包内存的大小

  * /proc/sys/net/core/netdev_max_backlog
  
    在每个网络接口接收数据包的速率比内核处理这些包的速率快时,允许送到队列的数据包的最大数目。

https://www.kernel.org/doc/Documentation/sysctl/fs.txt
  
https://blog.csdn.net/u012707739/article/details/78254241
  
https://www.cnblogs.com/tolimit/p/5065761.html
  
https://www.centos.org/forums/viewtopic.php?t=5657
  
https://blog.51cto.com/qujunorz/1703295
  
https://www.cnblogs.com/fczjuever/archive/2013/04/17/3026694.html  
https://www.cnblogs.com/leonardchen/p/9635407.html  