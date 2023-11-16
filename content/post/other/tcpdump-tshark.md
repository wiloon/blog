---
title: Linux网络协议分析工具tcpdump和tshark用法
author: "-"
date: 2012-06-25T14:46:16+00:00
url: /?p=3671
categories:
  - Linux
  - Network
tags:
  - reprint
---
## Linux网络协议分析工具tcpdump和tshark用法

Tcpdump是网络协议分析的基本工具。tshark是大名鼎鼎的开源网络协议分析工具wireshark  (原名叫ethereal) 的命令行版本，wireshark可对多达千余种网络协议进行解码分析。Wireshark 和 tcpdump 均使用libpcap 库 (参见 libpcap 编程教程) 进行网络截包。
  
    TCPDUMP
  
  
    详细manpage参见tcpdump网站。
  
  
    基本用法 
  
  
    Tcpdump的参数基本分为两块:选项 (options) 和过滤器表达式 (filter_expression) 。
  
  
    # tcpdump [options] [filter_expression]
  
  
    例如
  
  
    # tcpdump -c 100 -i eth0 -w log tcp dst port 50000
  
  
    其中 options部分参数: 
  
  
    -c 100 指定截取的包的数量
 -i eth0 指定监听哪个网络端口
 -w log 输出到名为log的文件中 (libpcap格式)
  
    filter_expression参数为 tcp dst port 50000，即只监听目标端口为50000的tcp包。
  
  
    更多的例子: 
  
  
    /* 监视目标地址为除内网地址(192.168.3.1-192.168.3.254)之外的流量 */

# tcpdump dst net not 192.168.3.0/24
  
    /*
 监视除HTTP浏览 (端口80/8080) 、SSH(22)、 POP3 (110)之外的流量，注意在括号(之前添加转义符, -n和-nn的解释见随后
 */

# tcpdump -n -nn port not (www or 22 or 110)

 或

# tcpdump -n -nn port ! (www or 22 or 110)
  
    /* 监视源主机MAC地址为00:50:04:BA: 9B的包 */

# tcpdump ether src 00:50:04:BA: 9B
  
    /* 监视源主机为192.168.0.1并且目的端口不是telnet的包 */

# tcpdump src host 192.168.0.1 and dst port not telnet
  
ip icmp arp rarp 和 tcp、udp、icmp这些选项等都要放到第一个参数的位置，用来过滤数据报的类型。例如

# tcpdump ip src…… //只过滤数据-链路层上的IP报头

# tcpdump udp and src host 192.168.0.1 //只过滤源主机192.168.0.1的所有udp报头
  
    TcpDump提供了很多options参数来让我们选择如何处理得到的数据，如下所示: 
  
  
    -l 将数据重定向。 如tcpdump -l > tcpcap.txt将得到的数据存入tcpcap.txt文件中。
 -n 不进行IP地址到主机名的转换。如果不使用这一项，当系统中存在某一主机的主机名时，TcpDump会把IP地址转换为主机名显示，就像这样: eth0 ＜ ntc9.1165＞ router.domain.net.telnet，使用-n后变成了: eth0 ＜ 192.168.0.9.1165 ＞ 192.168.0.1.telnet。
 -nn 不进行端口名称的转换。 上面这条信息使用-nn后就变成了: eth0 ＜ ntc9.1165 ＞ router.domain.net.23。
 -N 不打印出默认的域名。 还是这条信息-N 后就是: eth0 ＜ ntc9.1165 ＞ router.telnet。
 -O 不进行匹配代码的优化。
 -t 不打印UNIX时间戳，也就是不显示时间。
 -tt 打印原始的、未格式化过的时间。
 -v 详细的输出，也就比普通的多了个TTL和服务类型。
  
    参数详解
  
  
    tcpdump采用命令行方式，它的命令格式为: 
 tcpdump [ -adeflnNOpqStvx ] [ -c 数量 ] [ -F 文件名 ]
 [ -i 网络接口 ] [ -r 文件名] [ -s snaplen ]
 [ -T 类型 ] [ -w 文件名 ] [表达式 ]
  
    -a 将网络地址和广播地址转变成名字；
 -d 将匹配信息包的代码以人们能够理解的汇编格式给出；
 -dd  将匹配信息包的代码以c语言程序段的格式给出；
 -ddd 将匹配信息包的代码以十进制的形式给出；
 -e 在输出行打印出数据链路层的头部信息；
 -f 将外部的Internet地址以数字的形式打印出来；
 -l 使标准输出变为缓冲行形式；
 -n 不把网络地址转换成名字；
 -t 在输出的每一行不打印时间戳；
 -v 输出一个稍微详细的信息，例如在ip包中可以包括ttl和服务类型的信息；
 -vv 输出详细的报文信息；
 -c 在收到指定的包的数目后，tcpdump就会停止；
 -F 从指定的文件中读取表达式,忽略其它的表达式；
 -i 指定监听的网络接口；
 -r 从指定的文件中读取包(这些包一般通过-w选项产生)；
 -w 直接将包写入文件中，并不分析和打印出来；
 -T 将监听到的包直接解释为指定的类型的报文，常见的类型有rpc  (远程过程
 调用) 和snmp (简单网络管理协议；)
  
    tcpdump的表达式介绍
 表达式是一个正则表达式，tcpdump利用它作为过滤报文的条件，如果一个报文满足表
 达式的条件，则这个报文将会被捕获。如果没有给出任何条件，则网络上所有的信息包将会
 被截获。
 在表达式中一般如下几种类型的关键字，一种是关于类型的关键字，主要包括host，
 net，port, 例如 host 210.27.48.2，指明 210.27.48.2是一台主机，net 202.0.0.0 指明
 202.0.0.0是一个网络地址，port 23 指明端口号是23。如果没有指定类型，缺省的类型是
 host.
 第二种是确定传输方向的关键字，主要包括src , dst ,dst or src, dst and src ,
 这些关键字指明了传输的方向。举例说明，src 210.27.48.2 ,指明ip包中源地址是210.27.
 48.2 , dst net 202.0.0.0 指明目的网络地址是202.0.0.0 。如果没有指明方向关键字，则
 缺省是src or dst关键字。
 第三种是协议的关键字，主要包括fddi,ip ,arp,rarp,tcp,udp等类型。Fddi指明是在
 FDDI(分布式光纤数据接口网络)上的特定的网络协议，实际上它是"ether"的别名，fddi和e
 ther具有类似的源地址和目的地址，所以可以将fddi协议包当作ether的包进行处理和分析。
 其他的几个关键字就是指明了监听的包的协议内容。如果没有指定任何协议，则tcpdump将会
 监听所有协议的信息包。
 除了这三种类型的关键字之外，其他重要的关键字如下: gateway, broadcast,less,
 greater,还有三种逻辑运算，取非运算是 'not ' '! ', 与运算是'and','&&';或运算 是'o
 r' ,'||'；
 这些关键字可以组合起来构成强大的组合条件来满足人们的需要，下面举几个例子来
 说明。
 (1)想要截获所有210.27.48.1 的主机收到的和发出的所有的数据包:
 #tcpdump host 210.27.48.1
 (2) 想要截获主机210.27.48.1 和主机210.27.48.2 或210.27.48.3的通信，使用命令
 :  (在命令行中适用括号时，一定要
 #tcpdump host 210.27.48.1 and (210.27.48.2 or 210.27.48.3 )
 (3) 如果想要获取主机210.27.48.1除了和主机210.27.48.2之外所有主机通信的ip包
 ，使用命令:
 #tcpdump ip host 210.27.48.1 and ! 210.27.48.2
 (4)如果想要获取主机210.27.48.1接收或发出的telnet包，使用如下命令:
 #tcpdump tcp port 23 host 210.27.48.1
  
    tcpdump 的输出结果介绍
 下面我们介绍几种典型的tcpdump命令的输出信息
 (1) 数据链路层头信息
 使用命令#tcpdump -e host ice
 ice 是一台装有linux的主机，她的MAC地址是0: 90: 27: 58: AF: 1A
 H219是一台装有SOLARIC的SUN工作站，它的MAC地址是8: 0: 20: 79: 5B: 46；上一条
 命令的输出结果如下所示:
 21:50:12.847509 eth0 < 8:0:20:79:5b:46 0:90:27:58:af:1a ip 60: h219.33357 > ice.
 telne
 t 0:0(0) ack 22535 win 8760 (DF)
 分析: 21: 50: 12是显示的时间， 847509是ID号，eth0 <表示从网络接口eth0 接受该
 数据包，eth0 >表示从网络接口设备发送数据包, 8:0:20:79:5b:46是主机H219的MAC地址,它
 表明是从源地址H219发来的数据包. 0:90:27:58:af:1a是主机ICE的MAC地址,表示该数据包的
 目的地址是ICE . ip 是表明该数据包是IP数据包,60 是数据包的长度, h219.33357 > ice.
 telnet 表明该数据包是从主机H219的33357端口发往主机ICE的TELNET(23)端口. ack 22535
 表明对序列号是222535的包进行响应. win 8760表明发送窗口的大小是8760.
  
### ARP包的 TCPDUMP 输出信息

 使用命令#tcpdump arp
 得到的输出结果是:
 22:32:42.802509 eth0 > arp who-has route tell ice (0:90:27:58:af:1a)
 22:32:42.802902 eth0 < arp reply route is-at 0:90:27:12:10:66 (0:90:27:58:af
 :1a)
 分析: 22:32:42是时间戳, 802509是ID号, eth0 >表明从主机发出该数据包, arp表明是
 ARP请求包, who-has route tell ice表明是主机ICE请求主机ROUTE的MAC地址。 0:90:27:5
 8:af:1a是主机ICE的MAC地址。
  
### TCP 包的输出信息

用TCPDUMP捕获的TCP包的一般输出信息是:
src > dst: flags data-seqno ack window urgent options
src > dst:表明从源地址到目的地址, flags是TCP包中的标志信息,S 是SYN标志, F (FIN), P (PUSH) , R (RST) "." (没有标记); data-seqno是数据包中的数据的顺序号, ack是
下次期望的顺序号, window是接收缓存的窗口大小, urgent表明数据包中是否有紧急指针.
Options是选项.
  
### UDP 包的输出信息

用TCPDUMP捕获的UDP包的一般输出信息是:
route.port1 > ice.port2: udp lenth
UDP十分简单，上面的输出行表明从主机ROUTE的port1端口发出的一个UDP数据包到主机ICE的port2端口，类型是UDP， 包的长度是lenth

    Tshark

```bash
sudo pacman -S wireshark-cli
#安装后可以使用 tshark 命令
```
  
    详细参数参见tshark的manpage。
  
  
    // 列出可监听流量的网络接口列表。tshark使用1,2,...等数字来标识eth0,eth1...

# tshark -D
  
    // 监听接口eth0上的UDP端口为1234的流量

# tshark -f "udp port 1234" -i 1
  
    tshark的强悍之处在于对协议进行完全解码，甚至对分片的TCP包进行重组再行解码，例如
  
  
    // 监听接口eth0上目标端口为80的http流量，并将http请求头的host和location打印

# tshark -f "dst port 80" -T fields -e http.host -e http.location -i 1

 其中 -f 参数指定过滤表达式 (即等同tcpdump的 filter_expression)
 -T fields 指定屏幕输出信息类型为指定的协议字段 (用-e添加指定字段) ，仅在wireshark的0.99.6以后的版本支持。
 -i 1为指定监听的网络接口为1号
  
    // 监听http流量，仅过滤GET请求, 监听10秒钟，打印出HTTP HOST和URL
 c:Program FilesWiresharktshark.exe -i 4 -n -f "tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420" -T fields -e http.host -e http.request.uri -a duration:10
  
    关于各种协议的具体字段参数参见 http://www.wireshark.org/docs/dfref/
