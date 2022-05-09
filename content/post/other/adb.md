---
title: archlinux, adb
author: "-"
date: 2015-05-30T00:06:20+00:00
url: /?p=7731
categories:
  - Inbox
tags:
  - Arch Linux

---
## archlinux, adb
```bash
pacman -S android-tools
```

装了个64位的Archlinux,发现adb用不了,运行adb提示没有这个文件或目录,进入到sdk的platform-tools目录下去运行还是不行。

运行一下file命令

file adb
  
adb: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.8, stripped

可以看到adb是一个32位的linux程序。
  
那么首先就需要装32的glibc了,在archlinux的官网包搜索里面搜索glibc

4 packages found.
  
Arch
  
Repo
  
Name
  
Version
  
Description
  
Last Updated
  
Flag Date
  
x86_64
  
Core
  
glibc
  
2.16.0-4
  
GNU C Library
  
2012-08-29

x86_64
  
Extra
  
kdesdk-kmtrace
  
4.9.1-1
  
A KDE tool to assist with malloc debugging using glibc´s "mtrace" functionality
  
2012-09-05

x86_64
  
Multilib
  
lib32-glibc
  
2.16.0-4
  
GNU C Library for multilib
  
2012-08-30

x86_64
  
Extra
  
nss-mdns
  
0.10-5
  
glibc plugin providing host name resolution via mDNS
  
2012-02-21

4 packages found.
  
看到了32的glibc,但是在Multilib仓里面,这个仓默认是没有打开的

编辑/etc/pacman.conf文件,将下面几行前面的注释去掉

[multilib]
  
SigLevel = PackageRequired
  
Include = /etc/pacman.d/mirrorlist
  
然后运行pacman -Sy同步包数据库

再运行pacman -S lib32-glibc安装32位的glibc
  
再运行adb

    adb devices
  
adb: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
  
同理搜索ncurses可以看到需安装lib32-ncurses

# pacman -S lib32-ncurses

再运行adb

# adb devices

adb: error while loading shared libraries: libstdc++.so.6: cannot open shared object file: No such file or directory
  
再搜索可以看到需安装lib32-libstdc++5

# pacman -S lib32-libstdc++5

再运行adb

# adb devices

List of devices attached
  
10C61F9CD8B1 device

正常了。