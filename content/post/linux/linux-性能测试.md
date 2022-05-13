---
date: "2020-05-10T16:00:00Z"
title: "Linux性能测试工具"
categories:
  - inbox
tags:
  - reprint
---
## "Linux性能测试工具"
uptime

uptime命令用于查看服务器运行了多长时间以及有多少个用户登录，快速获知服务器的负荷情况。

uptime的输出包含一项内容是load average，显示了最近1，5，15分钟的负荷情况。它的值代表等待CPU处理的进程数，如果CPU没有时间处理这些进程，load average值会升高；反之则会降低。
  

load average的最佳值是1，说明每个进程都可以马上处理并且没有CPU cycles被丢失。对于单CPU的机器，1或者2是可以接受的值；对于多路CPU的机器，load average值可能在8到10之间。
  

也可以使用uptime命令来判断网络性能。例如，某个网络应用性能很低，通过运行uptime查看服务器的负荷是否很高，如果不是，那么问题应该是网络方面造成的。

dmesg

dmesg命令主要用来显示内核信息。使用dmesg可以有效诊断机器硬件故障或者添加硬件出现的问题。
  

另外，使用dmesg可以确定您的服务器安装了那些硬件。每次系统重启，系统都会检查所有硬件并将信息记录下来。执行/bin/dmesg命令可以查看该记录。

top

top命令显示处理器的活动状况。缺省情况下，显示占用CPU最多的任务，并且每隔5秒钟做一次刷新。
  

Process priority的数值决定了CPU处理进程的顺序。LIUNX内核会根据需要调整该数值的大小。nice value局限于priority。priority的值不能低于nice value (nice value值越低，优先级越高) 。您不可以直接修改Process priority的值，但是可以通过调整nice level值来间接地改变Process priority值，然而这一方法并不是所有时候都可用。如果某个进程运行异常的慢，可以通过降低nice level为该进程分配更多的CPU。

iostat

iostat由Red Hat Enterprise Linux AS发布。同时iostat也是Sysstat的一部分，可以下载到，网址是[http://perso.wanadoo.fr/sebastien.godard/](http://perso.wanadoo.fr/sebastien.godard/ "http://perso.wanadoo.fr/sebastien.godard/")
  

执行iostat命令可以从系统启动之后的CPU平均时间，类似于uptime。除此之外，iostat还对创建一个服务器磁盘子系统的活动报告。该报告包含两部分: CPU使用情况和磁盘使用情况。

vmstat

vmstat提供了processes, memory, paging, block I/O, traps和CPU的活动状况

sar

sar是Red Hat Enterprise Linux AS发行的一个工具，同时也是Sysstat工具集的命令之一，可以从以下网址下载: [http://perso.wanadoo.fr/sebastien.godard/](http://perso.wanadoo.fr/sebastien.godard/ "http://perso.wanadoo.fr/sebastien.godard/")

sar用于收集、报告或者保存系统活动信息。sar由三个应用组成: sar显示数据、sar1和sar2用于收集和保存数据。

使用sar1和sar2，系统能够配置成自动抓取信息和日志，以备分析使用。配置举例: 在/etc/crontab中添加如下几行内容

同样的，你也可以在命令行方式下使用sar运行实时报告。如图所示:

从收集的信息中，可以得到详细的CPU使用情况(%user, %nice, %system, %idle)、内存页面调度、网络I/O、进程活动、块设备活动、以及interrupts/second

KDE System Guard

KDE System Guard (KSysguard) 是KDE图形方式的任务管理和性能监视工具。监视本地及远程客户端/服务器架构体系的中的主机。

## free

/bin/free命令显示所有空闲的和使用的内存数量，包括swap。同时也包含内核使用的缓存。

Traffic-vis

Traffic-vis是一套测定哪些主机在IP网进行通信、通信的目标主机以及传输的数据量。并输出纯文本、HTML或者GIF格式的报告。

注: Traffic-vis仅仅适用于SUSE LINUX ENTERPRISE SERVER。

pmap

pmap可以报告某个或多个进程的内存使用情况。使用pmap判断主机中哪个进程因占用过多内存导致内存瓶颈。strace

strace截取和记录系统进程调用，以及进程收到的信号。是一个非常有效的检测、指导和调试工具。系统管理员可以通过该命令容易地解决程序问题。