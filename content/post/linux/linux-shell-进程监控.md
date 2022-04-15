---
title: linux shell 进程监控
author: "-"
date: 2012-07-05T05:08:16+00:00
url: /?p=3740
categories:
  - shell
tags:
  - reprint
---
## linux shell 进程监控
http://www.ibm.com/developerworks/cn/linux/l-cn-shell-monitoring/index.html?ca=drs-

```bash
  
 function GetPID #User #Name
   
{
      
PsUser=$1
      
PsName=$2
      
pid=\`ps -u $PsUser|grep $PsName|grep -v grep|grep -v vi|grep -v dbxn
      
|grep -v tail|grep -v start|grep -v stop |sed -n 1p |awk '{print $1}'\`
      
echo $pid
   
}
  
```
  
```bash

function killJboss {
   
jbosspid=\`ps -ef | grep -i jboss | grep -v grep |grep -v killJboss.sh | awk '{print $2}'\`
   
if [ "$jbosspid" != "" ]; then

echo "Killing Jboss."

echo $jbosspid
   
for pid in $jbosspid
   
do
   
kill -9 $pid
   
done
   
fi
  
}

```
  
```bash
  
function GetCpu
    
{
     
CpuValue=\`ps -p $pid -o pcpu |grep -v CPU | awk '{print $1}' | awk -F. '{print $1}'\`
          
echo $CpuValue
      
}
  
```
  
```bash
  
 function GetMem
      
{
          
MEMUsage=\`ps -o vsz -p $1|grep -v VSZ\`
          
(( MEMUsage /= 1000))
          
echo $MEMUsage
      
}
  
```

检测进程句柄使用量

在对应用服务进行维护时，也经常遇到由于句柄使用 过量导致业务中断的情况。每个平台对进程的句柄使用都是有限的，例如在 Linux 平台，我们可以使用 ulimit – n 命令 (open files (-n) 1024) 或者对 /etc/security/limits.conf 的内容进行查看，得到进程句柄限制。句柄使用过高可能由于负载过高，句柄泄露等情况，通过脚本对业务进程句柄使用量进行时时监控，可以在异常时及时发送告警 (例如通过短信) ，便于维护人员及时处理。下面的函数可获得指定进程 ID 的进程句柄使用情况。它有一个参数为进程 ID，它首先使用 ls 输出进程句柄信息，然后通过 wc -l 统计输出句柄个数。

```bash
  
function GetDes
      
{
          
DES=\`ls /proc/$1/fd | wc -l\`
          
echo $DES
      
}
  
```
查看某个 TCP 或 UDP 端口是否在监听

端口检测是系统资源检测经常遇到的，特别是在网络通讯情况下，端口状态的检测往往是很重要的。有时可能进程，CPU，内存等处于正常状态，但是端口处于异常状态，业务也是没有正常运行。下面函数可判断指定端口是否在监听。它有一个参数为待检测端口，它首先使用 netstat 输出端口占用信息，然后通过 grep, awk,wc 过滤输出监听 TCP 端口的个数，第二条语句为输出 UDP 端口的监听个数，如果 TCP 与 UDP 端口监听都为 0，返回 0，否则返回 1.

```bash
  
function Listening
   
{
      
TCPListeningnum=\`netstat -an | grep ":$1 " | n
      
awk '$1 == "tcp" && $NF == "LISTEN" {print $0}' | wc -l\`
      
UDPListeningnum=\`netstat -an|grep ":$1 " n
      
|awk '$1 == "udp" && $NF == "0.0.0.0:*" {print $0}' | wc -l\`
      
(( Listeningnum = TCPListeningnum + UDPListeningnum ))
      
if [ $Listeningnum == 0 ]
      
then
      
{
          
echo "0"
      
}
      
else
      
{
         
echo "1"
      
}
      
fi
   
}
  
```

检测系统 CPU 负载

在对服务器进行维护时，有时也遇到由于系统 CPU (利用率) 负载 过量导致业务中断的情况。服务器上可能运行多个进程，查看单个进程的 CPU 都是正常的，但是整个系统的 CPU 负载可能是异常的。通过脚本对系统 CPU 负载进行时时监控，可以在异常时及时发送告警，便于维护人员及时处理，预防事故发生。下面的函数可以检测系统 CPU 使用情况 . 使用 vmstat 取 5 次系统 CPU 的 idle 值，取平均值，然后通过与 100 取差得到当前 CPU 的实际占用值。

```bash
  
 function GetSysCPU
   
{
     
CpuIdle=\`vmstat 1 5 |sed -n '3,$p' n
     
|awk '{x = x + $15} END {print x/5}' |awk -F. '{print $1}'
     
CpuNum=\`echo "100-$CpuIdle" | bc\`
     
echo $CpuNum
   
}
  
```

检测系统磁盘空间

系统磁盘空间检测是系统资源检测的重要部分，在系统维护维护中，我们经常需要查看服务器磁盘空间使用情况。因为有些业务要时时写话单，日志，或者临时文件等，如果磁盘空间用尽，也可能会导致业务中断，下面的函数可以检测当前系统磁盘空间中某个目录的磁盘空间使用情况 . 输入参数为需要检测的目录名，使用 df 输出系统磁盘空间使用信息，然后通过 grep 和 awk 过滤得到某个目录的磁盘空间使用百分比。

```bash
  
function GetDiskSpc
   
{
      
if [ $# -ne 1 ]
      
then
          
return 1
      
fi

Folder="$1$"
      
DiskSpace=\`df -k |grep $Folder |awk '{print $5}' |awk -F% '{print $1}'
      
echo $DiskSpace
   
}
  
```
  
```bash

```
  
```bash

```
  
```bash

```
  
```bash

```
  
```bash

```