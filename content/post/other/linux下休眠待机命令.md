---
title: linux下休眠/待机命令
author: "-"
date: 2014-03-02T05:05:01+00:00
url: /?p=6302
categories:
  - Uncategorized
tags:
  - Linux

---
## linux下休眠/待机命令

命令行工具hibernate

安装 hibernate

```bash

sudo aptitude install hibernate

# sleep ,系统内存映象将写入 swap 区后关机

sudo hibernate-disk

# suspend ,就是挂起。

sudo hibernate-ram

#配置hiberante

sudo dpkg-reconfigure hibernate

```

主要是休眠唤醒密码。

if you

# cat /sys/power/state

mem disk

you can

echo "mem" > /sys/power/state 这相当于待机

echo "disk" > /sys/power/state 这相当于休眠

from <http://linux.chinaunix.net/bbs/viewthread.php?tid=1057578>

命令行中执行如下:

[root@fsc feng]# file /sys/power/state

/sys/power/state: ASCII text

[root@fsc feng]# cat /sys/power/state

standby mem disk

[root@fsc feng]# echo "mem">/sys/power/state

/sys/power/state是个文本文档,一个"mem"的导向就能使系统挂起到内存 (待机) 或硬盘 (休眠) ,实在太神奇了,一定要深入学习了解一下其中原因！

—————————————–

关于Linux操作系统睡眠和休眠

from <http://www.xxlinux.com/linux/article/accidence/technique/20080303/14073.html>

在作之前,先检查一下你的内核能支持哪些方式:

# cat /sys/power/state

standby disk

1. 睡眠 (sleep)

睡眠可能有两种方式: mem和standby,这两种方式都是suspend to RAM,简称STR,只是standby耗电更多一些,返回到正常工作方式时间更短一些而已。

只需要

# echo standby > /sys/power/state

就可以了。

2. 休眠 (hibernation)

休眠也有两种方式: shutdown和platform。shutdown是通常的方式,比较可靠一些。如果你的系统上ACPI支持非常好,那就有机会支持platform方式。激活的方式稍有不同:

# echo platform > /sys/power/disk; echo disk > /sys/power/state

or

# echo shutdown > /sys/power/disk; echo disk > /sys/power/state

注意休眠有一个前提,就是在系统启动时需要指定resume设备,也就是休眠的镜像需要保存的分区。一般都用swap分区来做。

指定方式是:

kernel /boot/vmlinuz root=/dev/sda1 resume=/dev/sda2 vga=0×314 …

这样在系统启动时,内核会检查resume中的内容,如果存在上次休眠的镜像,那内核便会将镜像读入内存,恢复正常工作状态。

—————————————-

Linux休眠和挂起 (2008新版)

from <http://blog.chinaunix.net/u/20515/showart_637851.html>

Linux2.6内核已经有了非常多的变化,配置也要相应的改变

The only thing that not changes is Change: )

系统要求:

配置编译内核:  kernel2.6.22,2.6.24适用,最新内核未作测试

所需上层软件:  hibernate,hal,gnome-power-manager

测试环境:

系统:  Debian lenny/sid

桌面: gnome2.22

机器: Thinkpad r40

操作细节:

1. 必需的内核选项:

Power Management support :

Suspend to Ram and Standby

Hibernate

()Default resume partition

 (如果有多个 swap 交换区,需要设定默认使用的swap。用 fdisk -l 确定)

ACPI Support

Future power /sys interface

AC adapter

Battery

Button

Fan

Processor

Thermal zone

Device driver

Block devices

Ram Disk support

编译时一定要注意: 使用initrd引导内核

3.图形界面下的工具

环境: gnome2.22

所需上层软件: hal,gnome-power-manager

sudo aptitude install gnome-power-manager

将电源管理加到系统任务栏Panel。

到这里root用户已经可以使用鼠标实现挂起和休眠了

普通用户使用休眠的关键: 增加权限

最简单安全的方法就是加入管理休眠的组group,他们是haldaemon,powerdev。

注意,haldaemon可能在你的机器上是hal,主要是hal版本新旧的原因。

加入以上两个group,就可以很方便的使用电源管理了。

小结:

＊linux 下suspend和hibernate模式可以随意使用,不需要额外的配置,较为方便。 而windows xp 只能是 sleep 模式,或者 suspend 模式,二者切换需要更新设置。

＊linux里涉及具体硬件的驱动太多,非常希望有一天它们能从内核里抽象出来,放到Userspace里。
