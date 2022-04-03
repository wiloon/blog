---
title: Linux命令pidof
author: "-"
date: 2012-04-06T14:55:41+00:00
url: /?p=2813
categories:
  - Linux

tags:
  - reprint
---
## Linux命令pidof
Linux命令pidof - 找出正在运行程序的进程PID

本文链接: <http://codingstandards.iteye.com/blog/841123>    (转载请注明出处) 

## 用途说明

pidof用于找出正在运行的程序的进程PID (find the process ID of a running program.) ，程序可以是一个二进制执行程序，也可以是一个shell脚本。如果是找出java程序的进程PID，pidof就无能为力了，可以使用ps -ef|grep java或jps -l来查看java进程的信息。通常找出进程PID的目的是确认程序是否在运行、或者为了把它杀掉、或者发送一个信号给它。

## 常用参数

格式: pidof program

找出program程序的进程PID，如果有多个就会全部列出，program不能是shell脚本名称。

格式: pidof -s program

找出program程序的进程PID，只列出一个。 (Single shot - this instructs the program to only return one pid.) 

格式: pidof -x script

找出shell脚本script的进程PID。

参数: -o omitpid

参数: -o omitpid1 -o omitpid2

在列出的进程PID中忽略omitpid。可以有多个。

参数: -s

只列出一个。

## 使用示例

### 示例一

[root@smsgw root]# pidof pidof
  
24386
  
[root@smsgw root]# pidof console

[root@smsgw root]# pidof bash
  
[root@smsgw root]# pidof man

[root@smsgw root]# pidof java
  
8882 27498 27482 30945 940 24465 23811 23068 2171 7022 24641 32656 32526
  
[root@smsgw root]# jps -l
  
25442 sun.tools.jps.Jps

注: 在这台机器上jps似乎不能很好的看java进程信息。
  
[root@smsgw root]#

### 示例二 查看shell脚本的 PID

下面演示了怎么查看脚本的PID的，可以发现通过不含路径的脚本文件名称、或者执行时的路径来查看，其他方式不行。

[root@web ~]# ls /opt/imx/imx_web3q/update.sh
  
/opt/imx/imx_web3q/update.sh
  
[root@web ~]# ps -ef|grep update.sh
  
root     17989 17963  0 Dec09 pts/7    00:00:05 /bin/sh ./update.sh
  
root     29329 28002  0 20:10 pts/2    00:00:00 grep update.sh
  
[root@web ~]# pidof update.sh

[root@web ~]# pidof -x update.sh
  
17989
  
[root@web ~]# pidof -x /opt/imx/imx_web3q/update.sh

[root@web ~]# pidof ./update.sh

[root@web ~]# pidof -x ./update.sh
  
17989
  
[root@web ~]#