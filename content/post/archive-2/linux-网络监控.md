---
title: linux 网络监控, NetHogs
author: "-"
date: 2015-11-04T02:03:53+00:00
url: network/monitor
categories:
  - network
tags:
  - reprint
---
## linux 网络监控, NetHogs

- NetHogs
- iftop
- slurm


## nethogs 

```bash
sudo pacman -S nethogs

```

```bash
# 刷新频率 5秒
nethogs -d 5

```
https://linux.cn/article-2808-1.html

NetHogs 是一个开源的命令行工具 (类似于Linux的top命令), 用来按进程或程序实时统计网络带宽使用率.

来自NetHogs项目网站:

NetHogs是一个小型的'net top'工具,不像大多数工具那样拖慢每个协议或者是每个子网的速度而是按照进程进行带宽分组.NetHogs NetHogs不需要依赖载入某个特殊的内核模块. 如果发生了网络阻塞你可以启动NetHogs立即看到哪个PID造成的这种状况.这样就很容易找出哪个程序跑飞了然后突然占用你的带宽.

本文介绍了一些可以用来监控网络使用情况的Linux命令行工具。这些工具可以监控通过网络接口传输的数据,并测量目前哪些数据所传输的速度。入站流量和出站流量分开来显示。

一些命令可以显示单个进程所使用的带宽。这样一来,用户很容易发现过度使用网络带宽的某个进程。

这些工具使用不同的机制来制作流量报告。nload等一些工具可以读取"proc/net/dev"文件,以获得流量统计信息；而一些工具使用pcap库来捕获所有数据包,然后计算总数据量,从而估计流量负载。

下面是按功能划分的命令名称。

监控总体带宽使用――nload、bmon、slurm、bwm-ng、cbm、speedometer和netload
  
监控总体带宽使用 (批量式输出) ――vnstat、ifstat、dstat和collectl
  
每个 socket 连接的带宽使用――iftop、iptraf、tcptrack、pktstat、netwatch和trafshow
  
每个进程的带宽使用――nethogs
  
1. nload

nload是一个命令行工具,让用户可以分开来监控入站流量和出站流量。它还可以绘制图表以显示入站流量和出站流量,视图比例可以调整。用起来很简单,不支持许多选项。

所以,如果你只需要快速查看总带宽使用情况,无需每个进程的详细情况,那么nload用起来很方便。

$ nload
  
安装nload: Fedora和Ubuntu在默认软件库里面就有nload。CentOS用户则需要从Epel软件库获得nload。

# fedora或centos
  
$ yum install nload -y
  
# ubuntu/debian
  
$ sudo apt-get install nload
  
2. iftop

iftop可测量通过每一个 socket 连接传输的数据；它采用的工作方式有别于nload。iftop使用pcap库来捕获进出网络适配器的数据包,然后汇总数据包大小和数量,搞清楚总的带宽使用情况。

虽然iftop报告每个连接所使用的带宽,但它无法报告参与某个套按字连接的进程名称/编号 (ID) 。不过由于基于pcap库,iftop能够过滤流量,并报告由过滤器指定的所选定主机连接的带宽使用情况。

$ sudo iftop -n
  
n选项可以防止iftop将IP地址解析成主机名,解析本身就会带来额外的网络流量。


安装iftop: Ubuntu/Debian/Fedora用户可以从默认软件库获得它。CentOS用户可以从Epel获得它。

# fedora或centos
  
yum install iftop -y
  
# ubuntu或 debian
  
$ sudo apt-get install iftop
  
3. iptraf

iptraf是一款交互式、色彩鲜艳的IP局域网监控工具。它可以显示每个连接以及主机之间传输的数据量。下面是屏幕截图。

$ sudo iptraf
  
安装iptraf: 

# Centos (基本软件库) 
  
$ yum install iptraf
  
# fedora或centos (带epel) 
  
$ yum install iptraf-ng -y
  
# ubuntu或debian
  
$ sudo apt-get install iptraf iptraf-ng
  
4. nethogs

nethogs是一款小巧的"net top"工具,可以显示每个进程所使用的带宽,并对列表排序,将耗用带宽最多的进程排在最上面。万一出现带宽使用突然激增的情况,用户迅速打开 nethogs,就可以找到导致带宽使用激增的进程。nethogs可以报告程序的进程编号 (PID) 、用户和路径。

$ sudo nethogs

安装nethogs: Ubuntu、Debian和Fedora用户可以从默认软件库获得。CentOS用户则需要Epel。

# ubuntu或debian (默认软件库) 
  
$ sudo apt-get install nethogs
  
# fedora或centos (来自epel) 
  
$ sudo yum install nethogs -y
  
5. bmon

bmon (带宽监控器) 是一款类似nload的工具,它可以显示系统上所有网络接口的流量负载。输出结果还含有图表和剖面,附有数据包层面的详细信息。

安装bmon: Ubuntu、Debian和Fedora用户可以从默认软件库来安装。CentOS用户则需要安装repoforge,因为Epel里面没有bmon。

# ubuntu或debian
  
$ sudo apt-get install bmon
  
# fedora或centos (来自repoforge) 
  
$ sudo yum install bmon
  
bmon支持许多选项,能够制作HTML格式的报告。欲知更多信息,请参阅参考手册页。

  1. slurm

slurm是另一款网络负载监控器,可以显示设备的统计信息,还能显示ASCII图形。它支持三种不同类型的图形,使用c键、s键和l键即可激活每种图形。slurm功能简单,无法显示关于网络负载的任何更进一步的详细信息。

$ slurm -s -i eth0

安装slurm

# debian或ubuntu
  
$ sudo apt-get install slurm
  
# fedora或centos
  
$ sudo yum install slurm -y
  
7. tcptrack

tcptrack类似iftop,使用pcap库来捕获数据包,并计算各种统计信息,比如每个连接所使用的带宽。它还支持标准的pcap过滤器,这些过滤器可用来监控特定的连接。

安装tcptrack: Ubuntu、Debian和Fedora在默认软件库里面就有它。CentOS用户则需要从RepoForge获得它,因为Epel里面没有它。

# ubuntu, debian
  
$ sudo apt-get install tcptrack
  
# fedora, centos (来自repoforge软件库) 
  
$ sudo yum install tcptrack
  
8. vnstat

vnstat与另外大多数工具有点不一样。它实际上运行后台服务/守护进程,始终不停地记录所传输数据的大小。之外,它可以用来制作显示网络使用历史情况的报告。

$ service vnstat status
  
* vnStat daemon is running
  
运行没有任何选项的vnstat,只会显示自守护进程运行以来所传输的数据总量。

$ vnstat
  
Database updated: Mon Mar 17 15:26:59 2014
  
eth0 since 06/12/13
  
rx:  135.14 GiB      tx:  35.76 GiB      total:  170.90 GiB
  
monthly
  
rx      |     tx      |    total    |   avg. rate

--------+-----+-----+-----
  
Feb '14      8.19 GiB  |    2.08 GiB  |   10.27 GiB |   35.60 kbit/s
  
Mar '14      4.98 GiB  |    1.52 GiB  |    6.50 GiB |   37.93 kbit/s
  
--------+-----+-----+-----
  
estimated       9.28 GiB |    2.83 GiB  |   12.11 GiB |
  
daily
  
rx      |     tx      |    total    |   avg. rate
  
--------+-----+-----+-----
  
yesterday     236.11 MiB |   98.61 MiB |  334.72 MiB |   31.74 kbit/s
  
today    128.55 MiB |   41.00 MiB |  169.56 MiB |   24.97 kbit/s
  
--------+-----+-----+-----
  
estimated       199 MiB |      63 MiB |     262 MiB |
  
想实时监控带宽使用情况,请使用"-l"选项 (实时模式) 。然后,它会显示入站数据和出站数据所使用的总带宽量,但非常精确地显示,没有关于主机连接或进程的任何内部详细信息。

$ vnstat -l -i eth0
  
Monitoring eth0...    (press CTRL-C to stop)
  
rx:       12 kbit/s    10 p/s          tx:       12 kbit/s    11 p/s
  
vnstat更像是一款制作历史报告的工具,显示每天或过去一个月使用了多少带宽。它并不是严格意义上的实时监控网络的工具。

vnstat支持许多选项,支持哪些选项方面的详细信息请参阅参考手册页。

安装vnstat

# ubuntu或debian
  
$ sudo apt-get install vnstat
  
# fedora或 centos (来自epel) 
  
$ sudo yum install vnstat
  
9. bwm-ng

bwm-ng (下一代带宽监控器) 是另一款非常简单的实时网络负载监控工具,可以报告摘要信息,显示进出系统上所有可用网络接口的不同数据的传输速度。

$ bwm-ng
  
bwm-ng v0.6 (probing every 0.500s), press 'h' for help
  
input: /proc/net/dev type: rate
  
/         iface                   Rx                   Tx                T
  
ot=================================================================
  
==           eth0:           0.53 KB/s            1.31 KB/s            1.84
  
KB             lo:           0.00 KB/s            0.00 KB/s            0.00
  
KB-------------------------------------
  
total:           0.53 KB/s            1.31 KB/s            1.84
  
KB/s
  
如果控制台足够大,bwm-ng还能使用curses2输出模式,为流量绘制条形图。

$ bwm-ng -o curses2
  
安装bwm-ng: 在CentOS上,可以从Epel来安装bwm-ng。

# ubuntu或debian
  
$ sudo apt-get install bwm-ng
  
# fedora或centos (来自epel) 
  
$ sudo apt-get install bwm-ng
  
10. cbm: Color Bandwidth Meter

这是一款小巧简单的带宽监控工具,可以显示通过诸网络接口的流量大小。没有进一步的选项,仅仅实时显示和更新流量的统计信息。

$ sudo apt-get install cbm
  
11. speedometer

这是另一款小巧而简单的工具,仅仅绘制外观漂亮的图形,显示通过某个接口传输的入站流量和出站流量。

$ speedometer -r eth0 -t eth0

安装speedometer

# ubuntu或debian用户
  
$ sudo apt-get install speedometer
  
12. pktstat

pktstat可以实时显示所有活动连接,并显示哪些数据通过这些活动连接传输的速度。它还可以显示连接类型,比如TCP连接或UDP连接；如果涉及HTTP连接,还会显示关于HTTP请求的详细信息。

$ sudo pktstat -i eth0 -nt
  
$ sudo apt-get install pktstat
  
13. netwatch

netwatch是netdiag工具库的一部分,它也可以显示本地主机与其他远程主机之间的连接,并显示哪些数据在每个连接上所传输的速度。

$ sudo netwatch -e eth0 -nt
  
$ sudo apt-get install netdiag
  
14. trafshow

与netwatch和pktstat一样,trafshow也可以报告当前活动连接、它们使用的协议以及每条连接上的数据传输速度。它能使用pcap类型过滤器,对连接进行过滤。

只监控TCP连接

$ sudo trafshow -i eth0 tcp
  
$ sudo apt-get install netdiag
  
15. netload

netload命令只显示关于当前流量负载的一份简短报告,并显示自程序启动以来所传输的总字节量。没有更多的功能特性。它是netdiag的一部分。

$ netload eth0
  
$ sudo apt-get install netdiag
  
16. ifstat

ifstat能够以批处理式模式显示网络带宽。输出采用的一种格式便于用户使用其他程序或实用工具来记入日志和分析。

$ ifstat -t -i eth0 0.5
  
Time           eth0
  
HH:MM:SS   KB/s in  KB/s out
  
09:59:21      2.62      2.80
  
09:59:22      2.10      1.78
  
09:59:22      2.67      1.84
  
09:59:23      2.06      1.98
  
09:59:23      1.73      1.79
  
安装ifstat: Ubuntu、Debian和Fedora用户在默认软件库里面就有它。CentOS用户则需要从Repoforge获得它,因为Epel里面没有它。

# ubuntu, debian
  
$ sudo apt-get install ifstat
  
# fedora, centos (Repoforge) 
  
$ sudo yum install ifstat
  
## dstat

dstat是一款用途广泛的工具 (用python语言编写) ,它可以监控系统的不同统计信息,并使用批处理模式来报告,或者将相关数据记入到CSV或类似的文件。这个例子显示了如何使用dstat来报告网络带宽。

安装dstat

    dstat -nt
  
-net/total- --system--
  
recv  send|     time
  
0     0 |23-03 10:27:13
  
1738B 1810B|23-03 10:27:14
  
2937B 2610B|23-03 10:27:15
  
2319B 2232B|23-03 10:27:16
  
2738B 2508B|23-03 10:27:17
  
18. collectl

collectl以一种类似dstat的格式报告系统的统计信息；与dstat一样,它也收集关于系统不同资源 (如处理器、内存和网络等) 的统计信息。这里给出的一个简单例子显示了如何使用collectl来报告网络使用/带宽。

$ collectl -sn -oT -i0.5
  
waiting for 0.5 second sample...
  
#         <----Network---->
  
#Time       KBIn  PktIn  KBOut  PktOut
  
10:32:01      40     58     43      66
  
10:32:01      27     58      3      32
  
10:32:02       3     28      9      44
  
10:32:02       5     42     96      96
  
10:32:03       5     48      3      28
  
安装collectl

# Ubuntu/Debian用户
  
$ sudo apt-get install collectl
  
#Fedora
  
$ sudo yum install collectl
  
结束语

上述几个使用方便的命令可以迅速检查Linux服务器上的网络带宽使用情况。不过,这些命令需要用户通过SSH登录到远程服务器。另外,基于Web的监控工具也可以用来实现同样的任务。

ntop和darkstat是面向Linux系统的其中两个基本的基于Web的网络监控工具。除此之外还有企业级监控工具,比如nagios,它们提供了一批功能特性,不仅仅可以监控服务器,还能监控整个基础设施。

原文链接: http://www.binarytides.com/linux-commands-monitor-network/

【编辑推荐】

4个强大的Linux服务器监控工具
  
监控 Linux 性能的 18 个命令行工具
  
五款好玩又好用的Linux网络测试和监控工具
  
10个实用的 Linux 网络和监控命令


## linux 网络 监控 iftop

在类Unix系统中可以使用top查看系统资源、进程、内存占用等信息。查看网络状态可以使用netstat、nmap等工具。若要查看实时的网络流量，监控TCP/IP连接等，则可以使用iftop。
  
### iftop是什么？
iftop是类似于top的实时流量监控工具。
  
官方网站: http://www.ex-parrot.com/~pdw/iftop/
  
二、iftop有什么用？
  
iftop可以用来监控网卡的实时流量 (可以指定网段) 、反向解析IP、显示端口信息等

界面上面显示的是类似刻度尺的刻度范围，为显示流量图形的长条作标尺用的。
  
中间的这两个左右箭头，表示的是流量的方向，2行显示时，进和出的流量是分开计算的，一行显示时是加在一起计算的;单独显示进或出时就是单独的进或出的流量。
  
右侧的三列数值: 
  
第一列是: 在此次刷新之前2s或10s或40s的平均流量 (按B设置秒数) ;
  
第二列是: 在此次刷新之前10秒钟的总流量的一半;
  
第三列是: 在此次刷新之前40秒钟的总流量的1/5;
  
中间的列表，默认没有排序情况下，把10秒平均通信量大的排在前面。
  
界面最下面的三行显示的分别是发送、接收、总计的流量，右侧值分别是总流量 (过滤后的，没过滤就是全部的) 、在此次刷新之前40秒内的峰值流量、最近2秒的平均传输速率、最近10秒的平均传输速率、最近40秒的平均传输速率。

### 常用的参数: 

/usr/local/iftop
  
/sbin/iftop help //查看帮助命令
  
-i设定监测的网卡，如: # iftop -i eth1
  
-B 以bytes为单位显示流量(默认是bits)，如: # iftop -B
  
-n使host信息默认直接都显示IP，如: # iftop -n
  
-N使端口信息默认直接都显示端口号，如: # iftop -N
  
-F 显示特定网段的进出流量，如# iftop -F 10.10.1.0/24或# iftop -F 10.10.1.0/255.255.255.0
  
-h (display this message) 没明白啥意思呢。。。hehe
  
-p使用这个参数后，中间的列表显示的本地主机信息，出现了本机以外的IP信息;
  
-b使流量图形条默认就显示;
  
-f这个暂时还不太会用，过滤计算包用的;
  
-P使host信息及端口信息默认就都显示;
  
-m设置界面最上边的刻度的最大值，刻度分五个大段显示，例: # iftop -m 100M
  
-c指定具体的设定文件，暂时没用过;

### 进入iftop画面后的一些操作命令(注意大小写): 

按h切换是否显示帮助;
  
按n切换显示本机的IP或主机名;
  
按s切换是否显示本机的host信息;
  
按d切换是否显示远端目标主机的host信息;
  
按t切换显示格式为2行/1行/只显示发送流量/只显示接收流量;
  
按N切换显示端口号或端口服务名称;
  
按S切换是否显示本机的端口信息;
  
按D切换是否显示远端目标主机的端口信息;
  
按p切换是否显示端口信息;
  
按P切换暂停/继续显示;
  
按b切换是否显示平均流量图形条;
  
按B切换计算2秒或10秒或40秒内的平均流量;
  
按T切换是否显示每个连接的总流量;
  
按l打开屏幕过滤功能，输入要过滤的字符，比如ip,按回车后，屏幕就只显示这个IP相关的流量信息;
  
按L切换显示画面上边的刻度;刻度不同，流量图形条会有变化;
  
按j或按k可以向上或向下滚动屏幕显示的连接记录;
  
按1或2或3可以根据右侧显示的三列流量数据进行排序;
  
按 按>根据远端目标主机的主机名或IP排序;
  
按o切换是否固定只显示当前的连接;
  
按f可以编辑过滤代码，这是翻译过来的说法，我还没用过这个！
  
按!可以使用shell命令，这个没用过！没搞明白啥命令在这好用呢！
  
按q退出监控。

TX: 发送流量
  
RX: 接收流量
  
TOTAL: 总流量
  
Cumm: 运行iftop到目前时间的总流量
  
peak: 流量峰值
  
rates: 分别表示过去 2s 10s 40s 的平均流量

按1或2或3可以根据右侧显示的三列流量数据进行排序;

按<根据左边的本机名或IP排序;

按>根据远端目标主机的主机名或IP排序;
  
按T切换是否显示每个连接的总流量;
  
按t切换显示格式为2行/1行/只显示发送流量/只显示接收流量;

Linux流量监控工具 - iftop (最全面的iftop教程)
  
 

>https://www.vpser.net/manage/iftop.html/embed#?secret=MdTvcxHN5f


## slurm 实时网络流量监控

虽然GNOME的系统监视器可以查看到网络状态，但是像slurm这样的命令行工具，占用资源少，查看方便，用起来到是别有一番风味。slurm 最初是给FreeBSD的做端口状态监视器，功能概述: 

显示实时流量吐吞状态

视图显示可选择

可以监视任何网络接口

显示关于接口的详细信息

安装slurm到Ubuntu


print?

```bash

sudo aptitude install slurm

```

这样安装就完成了

Slurm 语法

[cpp][/cpp]

print?

slurm [-hHz] [-csl] [-d delay] -i interface

如果你想监视第一块网卡 (eth0) ,使用下面的命令: 

[cpp][/cpp]

print?

slurm -i eth0