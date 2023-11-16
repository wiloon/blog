---
author: "-"
date: "2021-02-15 13:26:32" 
title: tcp
categories:
  - network
tags:
  - reprint
  - tcp

---
### tcp

TCP将数据分解成网络数据包，并在每个数据包中添加少量数据。这些附加数据包括一个序列号，用于检测丢失或到达顺序不正确的数据包，以及一个校验和，可以检测数据包数据内的错误。当其中任何一个问题发生时，TCP使用自动重传请求 (ARQ）告诉发送方重新发送丢失或损坏的数据包。

[https://luoguochun.cn/post/2016-09-23-tcp-fuck/](https://luoguochun.cn/post/2016-09-23-tcp-fuck/)

TCP 的连接标识是通过 “源IP + 源Port + 目标IP + 目标Port + 协议号“ 组成的唯一五元组，一旦其中一个参数发生变化，则需要重新创建新的 TCP 连接。

tcp协议是一个比较复杂的协议,对tcp协议深入理解的,真的非常少非常少；对tcp协议误理解或理解片面的,真的非常多非常多。当然这也包括自己在内,当然也可能包括这篇小结在内。 P.S.: 《TCP/IP详解卷1:协议》是介绍TCP/IP协议栈最经典的著作(神级已故人物W.Richard Stevens经典书籍之一),然而个人觉得这个"详解"对于tcp的介绍有点简略或者理解起来印象非深,读了一次,一次又一次,还是概念模糊。当然这也与中文译本烂得一塌糊涂有关。同时这本经典书籍也有了它的更新版,不同的是作者已经不是原来的神级人物,相同的是译文继续烂。

### tcp协议头

tcp协议头 tcp基本协议头占用20个字节,协议中Header Length(4bits)中标明协议头的长度,含义是多少个32bit数据,该字段占用4位,所有整个tcp头最多可以占用60字节。当tcp建立时,主机会生成一个初始的序列号(ISN, Initial Sequence Number),在tcpdump程序抓取的报文中可以看到该初始Sequence,Sequence的生成方式有一定的算法,一般tcp分析很少关注。如果tcpdump查看报文,可以发现,第一个SYN包收到ACK后,后续的SEQ都变成了ISN的偏移量。如果是用大鲨鱼wireshark查看报文,则可以发现,seq总是从0开始,并提示这个值是相对值,大鲨鱼已经处理好这些细节。如:  tcpdump seq wireshark seq

tcp报文SYN ACK的计算如下:

     A -> B SYN J ACK K LEN L
     B -> A SYN K ACK J+L LEN M
     A -> B SYN J+L ACK K+M
需要注意到的是,注意,对于DATA LEN为0的,发送的SYN包和FIN包,需要消耗一个序号。为了提高传送的效率,ACK是支持累计的,也就是说没必要对每个SYN进行ACK。如: 发送端连续发送3个报文,那么接收端收到3个报文后,可以直接应答一个ACK。

tcp标志位
CWR(Congestion Window Reduced) & ECN (ECN-Echo, Explicit Congestion Notification)  CWR 阻塞窗口已减少,意思是告诉对端我已经按照你的要求,进行阻塞窗口减少了,并启动阻塞算法来控制我的发包速度； ECN 显式阻塞窗口通知,意思通知发送方,我接收的报文出现了阻塞,请控制发包速度。也就是说,CWR 和 ECN 必须配合使用,CWR 是收到 ECN 的应答。此外,在tcp三次握手时,这两个标志表明tcp端是否支持ECN。如果建立连接一方支持,则在发送的SYN包,将 ECN 标志置为1,如果服务端也支持,则在ACK包只设置ECN。缘由: tcp建立连接后,报文经过经过路由或网关等网络设备后,在路由器或网关等网络设备出现阻塞时,路由器或网关等设备设置IP层的某个标志表明出现阻塞,这样接收可以明确知道报文出现了阻塞。然而,需要知道阻塞进行阻塞控制的是报文发送方而非接收方。所以接收方会在ACK报文中设置ECN标志,同时发送方在ACK中设置CWR标志,表明已经收到ECN,并进行了减少阻塞窗口操作和启用阻塞算法。

URG(Urgent) 这就是传说中的带外数据。因为tcp是没有消息边界的,假如有一种情况,你已经发送了一些数据,但是此时,你要发送一些数据优先处理,就可以设置这些标志。同时如果设置了这个标志,紧急指针(报文头中, Urgent Pointer(16Bit)部分)也会设置为相应的偏移。当接受方收到URG数据时,不缓存在接收窗口,直接往上传给上层。具体的使用带外数据大体的方法,就是,调用send和recv是要加上MSG_OOB参数。同时接收方要处理SIGURG信号。使用MSG_OOB是需要注意:  1) 紧急指针只能标示一个字节数据,所以如果发送带外数据多于一个字节,其他数据将当成是正常的数据。 2) 接收端需要调用fcntl(sockfd,F_SETOWN, getpid());,对socket描述符号进行宿主设置,否则无法捕获SIGURG信号。 3) 如果设置选项SO_OOBINLINE,那么将不能使用MSG_OOB参数接收的报文(调用报错),紧急指针的字符将被正常读出来,如果需要判断是否紧急数据,则需要提前判断: ioctl (fd,SIOCATMARK,&flag);if (flag) {read(sockfd,&ch,1);。 不过,据说这个带外数据在实际上,用得很少。

PSH (Push)  tcp报文的流动,先是发送方塞进发送方的缓存再发送；同样接收方是先塞到接收方的缓存再投递到应用。PSH标志的意思是,无论接收或发送方,都不用缓存报文,直接接收投递给上层应用或直接发送。PSH标志可以提供报文发送的实时性。如果设置了SO_NODELAY选项(也就是关闭Nagle算法),可以强制设置这个标志。

SYN(Synchronize), ACK(Acknowledgement), FIN (Finish) 和 RST(Reset) 这几个标记比较容易理解。SYN, Synchronize sequence numbers。ACK, Acknowledgement Number有效,应答标记。FIN,发送端结束发送。RST连接不可达。

tcp 选项(不完全)
tcp 除了20字节基本数据外,后面还包括了最多40个字节的tcp的选项。tcp选项一般存储为kind/type(1byte) length(1byte) value的格式式,不同的选项具体格式有所不同。这里简单罗列一些常见的tcp选项并做简单介绍。

MSS(Maximum Segment Size) tcp报文最大传输长读,tcp在三次握手建立阶段,在SYN报文交互该值,注意的是,这个数值并非协商出来的,而是由网络设备属性得出。MSS一个常见的值是1460(MTU1500 - IP头部 - TCP头部)。

SACK(Selective Acknowledgements) 选择ACK,用于处理segment不连续的情况,这样可以减少报文重传。比如:  A 向B发送4个segment,B收到了1,2,4个segment,网络丢失了3这个segment。B收到1,2segment后,回应ACK 3,表示1,2这两个ACK已经收到,同时在选项字段里面,包括4这个段,表示4这个segment也收到了。于是A就重传3这个segment,不必重传4这个segment。B收到3这个segment后,直接ACK 5,表明3,4都收到了。

## WS (Window Scale)

在tcp头部,Window Size(16Bit)表面接收窗口大小,但是对于现代网络而言,这个值太小了。所以tcp通过选项来增加这个窗口的值。WS值的范围0～14,表示 Window Size(16Bit)数值先向左移动的位数。这样实际上窗口的大小可达31位。在程序网络设计时,有个SO_RECVBUF,表示设置接收缓冲的大小,然而需要注意的是,这个值和接收窗口的大小不完全相等,但是这个数值和接收窗口存在一定的关系,在内核配置的范围内,大小比较接近。

## TS(Timestamps)

Timestamps在tcp选项中包括两个32位的 timestamp: TSval(Timestamp value) 和 TSecr(Timestamp Echo Reply)。 如果设置了TS这个选项, 发送方发送时, 将当前时间填入TSval, 接收方回应时, 将发送方的TSval 填入 TSecr 即可(注意发送或接收都有设置TSval和TSecr )。TS 选项的存在有两个重要作用: 一是可以更加精确计算 RTT(Round-Trip-Time), 只需要在回应报文里面用当前时间减去 TSecr 即可；二是P AWS(Protection Against Wrapped Sequence number, 防止sequence回绕), 什么意思呢？比如说,发送大量的数据: 0-10G,假设segment比较大为1G而且sequence比较小为5G,接收端接收1,3,4,5数据段正常接收,收到的发送时间分别1,3,4,5,第2 segment丢失了,由于SACK,导致2被重传,在接收6时,sequence由于回绕变成了1,这时收到的发送时间为6,然后又收到迷途的2,seq为2,发送时间为2,这个时间比6小,是不合法的,tcp直接丢弃这个迷途的报文。

UTO(User Timeout) UTO指的是发送SYN,收到ACK的超时时间,如果在UTO内没有收到,则认为对端已挂。 在网络程序设计的时候,为了探测对端是否存活,经常涉及心跳报文,通过tcp的keepalive和UTO机制也可以实现,两者的区别是,前者可以通过心跳报文实时知道对端是否存活,二后者只有等待下次调用发送或接收函数才可以断定:  1) SO_KEEPALIVE相关选项 设置SO_KEEPALIVE 选项,打开keepalive机制。 设置TCP_KEEPIDLE 选项,空闲时间间隔启动keepalive机制,默认为2小时。 设置TCP_KEEPINTVL选项,keepalive机制启动后,每隔多长时间发送一个keepalive报文。默认为75秒。 设置TCP_KEEPCNT选项,设置发送多少个keepalive数据包都没有正常响应,则断定对端已经崩溃。默认为9。 由于tcp有超时重传机制,如果对于ACK丢失的情况,keepalive机制将有可能失效。

2) TCP_USER_TIMEOUT相关选项 TCP_USER_TIMEOUT选项的函义是多久没有收到ACK则认为对端已经挂了。

配合SO_KEEPALIVE和TCP_USER_TIMEOUT选项,可以利用tcp机制实现探测对端存活。

### tcp 建立和终止

对于建链接的3次握手,主要是要初始化Sequence Number 的初始值。通信的双方要互相通知对方自己的初始化的Sequence Number (缩写为ISN: Inital Sequence Number) ——所以叫SYN,全称Synchronize Sequence Numbers。也就上图中的 x 和 y。这个号要作为以后的数据通信的序号,以保证应用层接收到的数据不会因为网络上的传输的问题而乱序 (TCP会用这个序号来拼接数据) 。

[https://imgchr.com/i/Bo6VQx](https://imgchr.com/i/Bo6VQx)

正常情况下,tcp的建立需要进行3次握手,tcp断开需要进行4次挥手。抓包看下建立连接和断开过程,通过抓取22端口报文,用telnent远程连接22端口测试,测试命令如下:

    heidong@HEIDONGVM:~$ sudo tcpdump -i eth0 port 22 -s 0 -w tcpdump-est-fin.cap

    heidong@HEIDONGVM:~$ telnet 192.168.1.101 22
    Trying 192.168.1.101...
    Connected to 192.168.1.101.
    Escape character is '^]'.
    SSH-2.0-OpenSSH_6.1
   ^]

    telnet> quit
    Connection closed.
    heidong@HEIDONGVM:~$
wireshark tcp 报文 1. TCP3次握手的过程是帧1到3 - 第1帧,发送SYN J:

     36600→22 [SYN] Seq=0 Win=29200 Len=0 MSS=1460 SACK_PERM=1 TSval=1488865 TSecr=0 WS=128

从主机10.0.2.15:36600 -> 192.168.1.101:22报文,`MSS=1460`, `Win=29200`,由于后面有`WS=128`选项,所以`Window=29200*128`。`SACK_PERM=1`表明10.0.2.15这台主机支持 **SACK**。`TSval`和`TSecr`为 **TS**的两个数值。
第2帧,发送SYN K, ACK J+1:

22→36600 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1460
从主机192.168.1.101:22 -> 10.0.2.15:36600报文,SYN报文将消耗一个字节,所以这里ACK为1。192.168.1.101这太主机的MSS=1460, win=65535没有WS。

第3帧,发送ACK K+1:

36600→22 [ACK] Seq=1 Ack=1 Win=29200 Len=0
这是建立TCP连接的第3次握手,是主机10.0.2.15对第二帧的应答,这时win=29200,意思是,接收窗口的大小。

当这3次交互完成后,连接真正建立,就可以接收和发送数据了。

TCP终止连接的4次挥手过程是帧6到9
第6帧,发送FIN J, ACK K:

36600→22 [FIN, ACK] Seq=1 Ack=22 Win=29200 Len=0
主机10.0.2.15: 36600主动关闭连接,发送FIN,和上个报文的ACK,这是第一次交换。 - 第7帧,发送ACK J+1:

     22→36600 [ACK] Seq=22 Ack=2 Win=65535 Len=0
主机192.168.1.101:22,回应第6帧FIN。 - 第8帧,FIN K, ACK J+1:

     22→36600 [FIN, ACK] Seq=22 Ack=2 Win=65535 Len=0
主机192.168.1.101:22关闭socket,发送FIN。 - 第9帧,ACK K+1:

     36600→22 [ACK] Seq=2 Ack=23 Win=29200 Len=0
主机10.0.2.15:36600,回应第5帧FIN。

至此,tcp进行了正常的关闭,10.0.2.15: 36600进入了TIME_WAIT状态。此次交互是非常理想的4次挥手过程,现实中,4次挥手的每一次交互的过程中都有可能携带额外的数据。 另外,tcp在结束连接时,例如它断开发送能力时,却依然希望能够接收数据。这属于tcp的半关闭功能。在程序实现时,不是调用close函数,而是调用shutdown函数,shutdown函数有个参数指明怎么关闭连接。

异常情况
建立连接异常 1.1 建立连接端口不存在 如果对端的端口不存在,那么在报文中回应RST标志,表示连接不可达。事实上发送端在需要重复一次SYN报文,对端才会响应RST。如:

heidong@HEIDONGVM:~$ telnet 192.168.1.101 9900
Trying 192.168.1.101...
telnet: Unable to connect to remote host: Connection refused
heidong@HEIDONGVM:~$

heidong@HEIDONGVM:~$ sudo tcpdump -i eth0 host 192.168.1.101
[sudo] password for heidong:
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
21:19:36.424426 IP 10.0.2.15.52519 > 192.168.1.101.9900: Flags [S], seq 4012293140, win 29200, options [mss 1460,sackOK,TS val 5302548 ecr 0,nop,wscale 7], length 0
21:19:37.424498 IP 10.0.2.15.52519 > 192.168.1.101.9900: Flags [S], seq 4012293140, win 29200, options [mss 1460,sackOK,TS val 5302798 ecr 0,nop,wscale 7], length 0
21:19:37.516340 IP 192.168.1.101.9900 > 10.0.2.15.52519: Flags [R.], seq 0, ack 4012293141, win 0, length 0
^C
3 packets captured
3 packets received by filter
0 packets dropped by kernel
heidong@HEIDONGVM:~$
1.2 建立连接主机不存在 如果连接的主机不存在,那么tcp 会重发报文SYN。重发的次数在内核参数了net.ipv4.tcp_syn_retries配置,如:

    heidong@HEIDONGVM:~$ cat /proc/sys/net/ipv4/tcp_syn_retries 
    6
重连重试的是时间分别是。2^X-1秒。如:

    heidong@HEIDONGVM:~$ telnet 192.168.1.101 9900
    Trying 192.168.1.101...
    telnet: Unable to connect to remote host: Connection refused
    heidong@HEIDONGVM:~$ telnet 192.168.1.156 9900
    Trying 192.168.1.156...
    telnet: Unable to connect to remote host: Connection timed out
    heidong@HEIDONGVM:~$

    heidong@HEIDONGVM:~$ sudo tcpdump -i eth0 host 192.168.1.156
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    21:39:58.109141 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5607969 ecr 0,nop,wscale 7], length 0
    21:39:59.109694 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5608219 ecr 0,nop,wscale 7], length 0
    21:40:01.112512 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5608720 ecr 0,nop,wscale 7], length 0
    21:40:05.119962 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5609722 ecr 0,nop,wscale 7], length 0
    21:40:13.146103 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5611728 ecr 0,nop,wscale 7], length 0
    21:40:29.176601 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5615736 ecr 0,nop,wscale 7], length 0
    21:41:01.208154 IP 10.0.2.15.38610 > 192.168.1.156.9900: Flags [S], seq 1424720904, win 29200, options [mss 1460,sackOK,TS val 5623744 ecr 0,nop,wscale 7], length 0
    ^C
    7 packets captured
    7 packets received by filter
    0 packets dropped by kernel
    heidong@HEIDONGVM:~$ 
断开连接异常 对于没有正常收到FIN异常终止连接的情况,tcp回应RST。 另外,SO_LINGER选项提供异常终止的能力:  默认的情况下,使用close函数关闭一个连接,tcp默认的行为是,1) 如果发送缓冲没有数据,发送FIN并直接返回 2) 如果缓冲存在数据,tcp将尽力把数据发送出去,然后发送FIN并返回。SO_LINGER选项可以改变这默认行为,相关数据结构

struct linger {
    int l_onoff; /*0=off, nozero=on*/
    int l_linger; /*linger time, POSIX specifies units as seconds*/
}

1) l_onoff = 0,l_linger被忽略,同默认行为 2) l_onoff 非0,l_linger为0,close清空发送缓冲,并发送RST,然后返回,这中情况下,可以避免TIME_WAIT状态的产生。 3) l_onoff非0,l_linger大于0,close将使内核推延一段时间。如果缓冲有数据,进程将进入睡眠状态,直到数据发送完毕并收到对方的ACK或者滞留超时(close返回EWOULDBLOCK),缓冲去数据丢失。(如果是非阻塞,则直接返回EWOULDBLOCK) shutdown使用可以避免关闭时还有数据的处理。

## tcp 状态机

tcp在每个时刻都存在于一个特定的状态(CLOSED状态为假想状态),这里的状态和netstat显示的状态是一致的,各个状态以及状态转换如下:  TCP状态机 TIME_WAIT 也称为 2MSL(Maximum Segment Lifetime) 状态, 它可以保证对端发送最后的 FIN (重发的), 能够响应ACK, 另外一个含是, 保证端口在 2MSL 端口不被重发使用。 在服务端编程的时候, 我们通常会使用 SO_REUSEADDR 这个选项, 这样可以避免如果服务端进入 TIME_WAIT 状态后, 可以及时重启。 FIN_WAIT_2 状态是在发送 FIN, 接收到ACK时, 进入的状态, 如果对端没有发送 FIN 那么, 将无法进入 TIME_WAIT 状态, 这时对端一直是CLOSE_WAIT 状态,当服务器出现大量的 FIN_WAIT_2 或 CLOSE_WAIT 状态时, 一般都是被动关闭那端忘记了调用close函数关闭socket。

## TCP数据传输

滑动窗口 在tcp头部,窗口大小占用16位,再加上WS选项,实际上可以达31位。已经建立连接的TCP双方,都维护两个窗口,分别为接收窗口和接收窗口。

1. 发送方窗口 发送方窗口 如图示,在任意一时刻,发送方的发送窗口数据可分4大类: 1) 已经发送并收到ACK的,2) 已经发送并未收到ACK的,3) 准备发送的,4) 未发送的。第1和第2类数据之间的边界称为左边界；第3和第4类之间的数据称之为右边界。第2和第3类数据之间的窗口称之为Offered Window,是接收方通告的窗口大小。左边界向做右移动,称为窗口合拢；右边界向右移动,称为窗口张开；右边界向左移动,称为窗口的收缩(实际tcp实现不一定有)。如果左边界到达右边界,那么窗口为0,不能发送任何数据。当窗口变为0时,这里存在一个问题: 因为接收方的窗口大小是通过ACK告知的,如果窗口为0了,那么哪里来的ACK呢？解决的办法是,发送方会发送ZWP(Zero Windonw Probe)的报文给接收端,让接收端应答ACK告知窗口大小,当发送方发送3次ZWP后(一般设置3次,每次给30~60秒),如果窗口依然是0,那么有些tcp实现将关闭连接。在当发送方收到发送数据的ACK时,左边界向右合拢或窗口向右移动。注意到,只有收到ACK时,左边界才会右移。

2. 接收方窗口 接收方窗口 如图示,类似发送方窗口,接收方窗口分为3大类,1) 已经接收并发送ACK的,2) 将接收存储的,3) 不能接收的。第1和2类之间的边界称为左边界,第2和第3类数据之间的边界称之为右边界。当接收方收到报文的SEQ小与左边界,则当做是重发报文直接丢弃；当接收的报文的SEQ大于右边界,则认为是溢出也直接丢弃,只有报文在左边界和右边界 之间的报文才允许接收。如果在左边界和右边界 之间收到的非连续的报文(由于SACK,报文将缓存),那么左边界并不会向右移动,等待重传数据连续后,才移动。

由于滑动窗口的这些特性,接收方可以进行窗口的控制,通过告知对方窗口大大小,让发送方进行控制调整,从而具备流量控制功能。

糊涂窗口综合症(SWS) 如果建立连接的双方,当发送方产生的数据速度很慢,或者接收发消耗的数据很慢或者两者都有,这样会导致发送方向接收方发送极少量的数据,接收方回应很小的窗口。这样就会导致网络上存在大量的小数据包,tcp头部至少占20字节,加上IP头部的20字节,这个传输一个小包,耗费这么大的网络资源,这样是很不经济的,出现的这种情况称之为糊涂窗口综合症Silly Window Syndrome(SWS),SWS导致网络利用的低效率。SWS可由发送方或接收方造成,解决方法:  2.1 发送方Nagle算法 Nagle算法最多允许有一个为确认的未完成小分组(小于MSS),在该分组的ACK到达之前,不能发送其他小分组。也就是说,如果对端ACK回应的很快的话,Nagle算法并不会合并多少数据包(也就是说并不会启用),在"低速"网络环境里面才会出现更多的小分组合并发送。tcp协议默认是打开 Nagle算法的,发送报文条件是:  1) 如果包长度达到MSS,则允许发送； 2) 如果该包含有FIN,则允许发送； 3) 所有发出去的小数据包 (包长度小于MSS) 均被确认,则允许发送； 4) 上述条件都未满足,但发生了超时 (一般设置延迟ACK,一般为200ms) ,则立即发送。
TCP_NODELAY选项可以关闭Nagle算法。关闭后,只要有数据就立刻进行发送。

2.2 接收方Cork算法或延长ACK 如果接收方处理比较慢,ACK的窗口很小,这样接收端就引起SWS。Cork算法就是只要有数据达到,就回应,但是回应的窗口大小为0,直到空闲窗口已经可以放入MSS的报文长度,或者窗口的空间一半已经变为可用,这时才回应真实的可用窗口。TCP_CORK 选项可以启用这个算法。另外的一种机制是延迟确认,接收端收到报文时,并不立刻进行确认,等到有足够的窗口空间,才进行确认。延迟确认会引入另外一个问题,就是会导致tcp发送方进行报文重发,现在延迟确认的数据定义为500毫秒。TCP_QUICKACK选项可以关闭延迟ACK,然而这个选项并非是永久的,需要每次接收数据后,重新设置一次。

TCP阻塞控制
在复杂和经常变化的网络环境中,当网络程序阻塞时,tcp不是一味的发送数据加塞网络,而是进行自我调整。传统的阻塞控制算法有4种: 慢启动(Slow Start),阻塞避免(Congestion Avoidance),快速重传(Fast Retransmit),快速恢复(Fast Recovery)。 1. 慢启动 慢启动算法启动发生在建立tcp连接后,或者报文重传超时(Retransmit Timeout, RTO)后,也有可能是tcp空闲某段时间后。慢启动为TCP增加了一个阻塞窗口(Congestion Window, cwnd),cwnd以MSS 为单位,发送时,取 cwnd和通告的窗口大小最小值为发送上限。慢启动算法: 1) cwnd通常初始化为1个MSS(Linux 3.0或以上,设置为10MSS) 2) 在没有出现丢包的情况下,每收到一个ACK,cwnd = cwnd * 2 3) 当cwnd增长的一个阈值,(slow start threshold, ssthresh),即cwnd >= ssthresh,tcp 进入避免阻塞算法

当RTO时,ssthresh = cwnd / 2,cwnd = 1,重启慢启动算法。

由上可知,当 ACK 很快时,慢启动算法的增长速率是很快的。如果存在延迟确认,那么增长速率并不快,所以在建立连接的慢启动算法启动期间,延迟确认是关闭的。

阻塞避免 当cwnd >= ssthresh时,就会启用避免阻塞算法,算法如下:  1) 每收到一个非重复的ACK,cwnd = cwnd + 1/cwnd 避免阻塞算法,避免了慢启动那种指数级别的快速增长,而变成了缓慢的线性增长,慢慢调整到网络最佳值。

快速重传 当收到一连串3个或以上的重复ACK时,则可以认为有报文段丢失了,这个时候,不需要得等RTO,直接重传丢失的报文。这就是快速重传算法。但启用快速重传算法后,tcp并不启用慢启动算法,因为接收端已经在高速接收数据了,tcp不想突然减速,而是启动另个一个算法,快速恢复。

快速恢复 当收到3个或以上重发ACK,快速恢复算法启动,算法如下:  1) ssthresh = cwnd / 2 2) 每次收到重复的ACK, cwnd = cwnd + 1 3) 收到新数据ACK,cwnd = ssthresh

由上,网络出现阻塞时,快速恢复算法将发送速率降低了。

小结
这里小结只是tcp的很小一部分,没有涉及到tcp的方方面面,也没有涉及到内核调优,编程技巧等方方面面。另外tcp目前还是发展中的协议,随着时间推移,有很多新的功能特性添加进来,这里也没有涉及到。对于tcp的熟悉,必须通过抓包实践才能进行一步了解,停留在读书计理论,永远无法理解。期待以后有更全面的认识！

tcpdump 使用参考:  [https://luoguochun.cn/2015/07/25/tcpdump-usage/](https://luoguochun.cn/2015/07/25/tcpdump-usage/) 完。

一些参考:  TCP_DEFER_ACCEPT TFO–TCP Fast Open – 由于存在安全隐患而没有广泛使用。

### tcp包发送流程

[![IBT7gH.jpg](https://z3.ax1x.com/2021/11/12/IBT7gH.jpg)](https://imgtu.com/i/IBT7gH)

### 自动重传请求 ARQ

---

[https://coolshell.cn/articles/11564.html](https://coolshell.cn/articles/11564.html)
[https://www.cnblogs.com/liwei0526vip/p/14587300.html](https://www.cnblogs.com/liwei0526vip/p/14587300.html)

[https://xie.infoq.cn/article/760f379a3e3f2694b5e994ffd?utm_source=rss&utm_medium=article](https://xie.infoq.cn/article/760f379a3e3f2694b5e994ffd?utm_source=rss&utm_medium=article)
>[https://developer.aliyun.com/article/720202](https://developer.aliyun.com/article/720202)

RWIN (receivers advertised window size)

## MSL, Maximum Segment Lifetime

MSL是 Maximum Segment Lifetime 英文的缩写，中文可以译为“报文最大生存时间”，他是任何报文在网络上存在的最长时间，超过这个时间报文将被丢弃。因为tcp报文（segment）是ip数据报（datagram）的数据部分，具体称谓请参见《数据在网络各层中的称呼》一文，而ip头中有一个TTL域，TTL是time to live的缩写，中文可以译为“生存时间”，这个生存时间是由源主机设置初始值但不是存的具体时间，而是存储了一个ip数据报可以经过的最大路由数，每经过一个处理他的路由器此值就减1，当此值为0则数据报将被丢弃，同时发送ICMP报文通知源主机。RFC 793中规定MSL为2分钟，实际应用中常用的是30秒，1分钟和2分钟等。

2MSL 即两倍的 MSL，TCP 的 TIME_WAIT 状态也称为 2MSL 等待状态，当 TCP 的一端发起主动关闭，在发出最后一个 ACK 包后，即第3次握手完成后发送了第四次握手的 ACK 包后就进入了 TIME_WAIT 状态，必须在此状态上停留两倍的MSL时间，等待 2MSL 时间主要目的是怕最后一个 ACK 包对方没收到，那么对方在超时后将重发第三次握手的FIN包，主动关闭端接到重发的FIN包后可以再发一个ACK应答包。在TIME_WAIT 状态时两端的端口不能使用，要等到 2MSL 时间结束才可继续使用。当连接处于2MSL等待阶段时任何迟到的报文段都将被丢弃。不过在实际应用中可以通过设置 SO_REUSEADDR 选项达到不必等待 2MSL 时间结束再使用此端口。

TTL与MSL是有关系的但不是简单的相等的关系，MSL要大于等于TTL。

————————————————
版权声明：本文为CSDN博主「xiaofei0859」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/xiaofei0859/article/details/6044694](https://blog.csdn.net/xiaofei0859/article/details/6044694)
