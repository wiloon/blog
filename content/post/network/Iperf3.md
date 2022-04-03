---
author: "-"
date: "" 
title: "iperf3"

categories:
  - inbox
tags:
  - reprint
---
## "iperf3"
### install
#### centos
    yum install iperf3
#### openwrt
    opkg install iperf3
#### ubuntu
    apt-get install iperf3

### command
#### server
    iperf3 -s
#### client
    iperf3 -c 192.168.50.101 -t 104

Iperf3 是一个网络性能测试工具。Iperf可以测试最大TCP和UDP带宽性能,具有多种参数和UDP特性,可以根据需要调整,可以报告带宽、延迟抖动和数据包丢失.对于每个测试,它都会报告带宽,丢包和其他参数,可在Windows、Mac OS X、Linux、FreeBSD等各种平台使用,是一个简单又实用的小工具。

软件下载地址:  https://iperf.fr/iperf-download.php

安装iperf3

在CentOS 7上使用下列命令即可安装: 
 
在ubuntu 上使用下列命令安装:
# apt-get install iperf3
 
windows端安装: 
下载解压安装包,进入dos切换到iperf3解压目录,执行iperf3即可运行.
网络带宽测试

Iperf3也是C/S(客户端/服务器端)架构模式,在使用iperf3测试时,要同时在server端与client端都各执行一个程序,让它们互相传送报文进行测试。

我这边在ubuntu主机安装iperf3作为服务端,ip地址为192.168.1.43 ,本地windows pc机作为客户端,来做测试实验.

1. 首先在192.168.1.43 机器启动server端的程序: 

saneri@saneri-VirtualBox:~$ iperf3 -s


2. 接着在本地windows PC服务器上执行client 端的程序: 

C:\Users\iperf3>iperf3.exe -c 192.168.1.43
 

从打印的内容看,缺省参数下,Client将连接Server端的5201端口,持续向Server端发送数据,并统计出每秒传输的字节数、带宽、出现报文重传的次数、拥塞窗口 (Congestion Window) 大小,整个测试将持续10秒钟；最后将汇总10秒的平均数据,并给出发送和接收端的统计。
---------------------
接下来分析一下Server的测试输出结果: 



Server端日志显示接收了来自192.168.1.71,源端口56569的测试请求。Client端连续进行了10秒的测试,并显示了每秒传输的字节数,带宽信息；测试结束后会汇总发送和接收的统计信息。在Client连接关闭之后会继续侦听5201端口。
---------------------
iperf3 所提供的选项非常多,以下介绍一些常用的参数。

服务器端命令行

其中: 

-s    表示服务器端；
-p    定义端口号；
-i    设置每次报告之间的时间间隔,单位为秒,如果设置为非零值,就会按照此时间间隔输出测试报告,默认值为零
客户端命令行
其中,

复制代码
-c    表示服务器的IP地址；
-p    表示服务器的端口号；
-t    参数可以指定传输测试的持续时间,Iperf在指定的时间内,重复的发送指定长度的数据包,默认是10秒钟.

-i    设置每次报告之间的时间间隔,单位为秒,如果设置为非零值,就会按照此时间间隔输出测试报告,默认值为零；

-w    设置 socket 缓冲区为指定大小,对于TCP方式,此设置为TCP窗口大小,对于UDP方式,此设置为接受UDP数据包的缓冲区大小,限制可以接受数据包的最大值.

--logfile    参数可以将输出的测试结果储存至文件中.

-J  来输出JSON格式测试结果.
-R  反向传输,缺省iperf3使用上传模式: Client负责发送数据,Server负责接收；如果需要测试下载速度,则在Client侧使用-R参数即可.
复制代码
常用启动命令: 

服务端: 
saneri@saneri-VirtualBox:~$ iperf3 -s -p 12345 -i 1
客户端: 
C:\Users\iperf3>iperf3.exe -c 192.168.1.43 -p 12345 -i 1 -t 20 -w 100k
 

windows图形界面版本的为jperf:

---

https://wenku.baidu.com/view/521c7017ed630b1c58eeb537.html
参考文档: https://blog.csdn.net/jinguangliu/article/details/82468482
https://man.linuxde.net/iperf