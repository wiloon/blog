---
title: linux version, Linux 查看版本, 发行版, 内核版本, uname
author: "-"
date: 2012-02-01T05:28:07+00:00
url: uname
categories:
  - Linux
tags:
  - reprint
---
## linux version, Linux 查看版本, 发行版, 内核版本, uname


```bash
# 查看内核版本
uname -r

# 打印所有信息，包括内核版本和系统名称
uname -a

# archlinux, debian, ubuntu
cat /etc/issue

# RedHat,CentOS
cat /etc/redhat-release

# debian, ubuntu
cat /etc/os-release

#查看目录"/proc"下version的信息，也可以得到当前系统的内核版本号及系统名称
cat /proc/version
file /bin/ls
```

/proc文件系统，它不是普通的文件系统，而是系统内核的映像，也就是说，该目录中的文件是存放在系统内存之中的，它以文件系统的方式为访问系统内核数据的操作提供接口。而我们使用命令"uname -a"的信息就是从该文件获取的，当然用方法二的命令直接查看它的内容也可以达到同等效果.另外，加上参数"a"是获得详细信息，如果不加参数为查看系统名称。

## 查看发行版本信息

### ubuntu

```bash
    lsb_release -a
```

<https://my.oschina.net/vshcxl/blog/698656>

## 查 LINUX是32位还是64位, 64bit

```bash
uname -m

sudo file /sbin/init
/sbin/init: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked ...



uname -a


getconf LONG_BIT
# 32/64

uname -m
```

### uname -a

```bash
uname -a
```

回显, x86_64表示64位机器, i686 只是i386的一个子集,支持的cpu从Pentium 2 (686)开始,之前的型号不支持.

>Linux host0 5.16.4-arch1-1 #1 SMP PREEMPT Sat, 29 Jan 2022 19:08:13 +0000 x86_64 GNU/Linux

回显, i686表示32位机器

>Linux pmx0**.**.**    2.6.9-5.ELsmp #1 SMP Wed Jan 5 19:30:39 EST 2005 i686 i686 i386 GNU/Linux

备注:
  
1. i386 适用于intel和AMD所有32位的cpu.以及via采用X86架构的32的cpu.  
intel平台包括8086,80286,80386,80486,奔腾系列(1.2.3.4)、赛扬系列,Pentium D系列  
以及centrino P-M,core duo 等.
  
2. X86_64 适用于intel的Core 2 Duo, Centrino Core 2 Duo, and Xeon 和AMD Athlon64/x2, Sempron64/x2, Duron64等采用X86架构的64位cpu.
3. PPC   适用于Apple Macintosh G3, G4, G5, PowerBook, and other non-Intel models

安装DVD包括的软件要比安装光盘多一些,安装DVD也包括了两种图形界面(KDE和gnome).
  
4. Jigdo
也可以通过 Jigdo 下载 Fedora 发行版。Jigdo 可以加速下载安装盘的 ISO 镜像。同 BT 下载等待任务完全完成所不同，Jidgo 自动定位最快的镜像服务器(通过 Fedora 镜像管理器)，并且从中下载所需要的文件。为了减少所需的网络流量，可以让 Jigdo 扫描现存的 DVD 或 CD 介质。这个功能对于以下用户特别有用。

http://blog.csdn.net/carolzhang8406/article/details/6080400  


