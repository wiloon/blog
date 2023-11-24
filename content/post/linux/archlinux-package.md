---
title: archlinux package
author: "-"
date: "2021-12-30 10:10:08"
url: ""
categories:
  - Linux
tags:
  - inbox
---
## archlinux package

## linux-firmware

在Linux Kernel中，Driver和Firmware是有明确含义的，其中Driver是控制被操作系统管理的外部设备(Device)的代码段。很多时候Driver会被实现为LKM，但这不是必要条件。driver通过driver_register()注册到总线(bus_type)上，代表系统具备了驱动某种设备(device)的能力。当某个device被注册到同样的总线的时候(通常是总线枚举的时候发现了这个设备)，总线驱动会对driver和device会通过一定的策略进行binding(即进行匹配)，如果Binding成功，总线驱动会调用driver的probe()函数，把设备的信息(例如端口，中断号等)传递给驱动，驱动就可以对真实的物理部件进行初始化，并把对该设备的控制接口注册到Linux的其他子系统上(例如字符设备，v4l2子系统等)。这样操作系统的其他部分就可以通过这些通用的接口来访问设备了。

而Firmware，是表示运行在非“控制处理器”(指不直接运行操作系统的处理器，例如外设中的处理器，或者被用于bare metal的主处理器的其中一些核)中的程序。这些程序很多时候使用和操作系统所运行的处理器完全不同的指令集。这些程序以二进制形式存在于Linux内核的源代码树中，生成目标系统的时候，通常拷贝在/lib/firmware目录下。当driver对device进行初始化的时候，通过request_firmware()等接口，在一个用户态helper程序的帮助下，可以把指定的firmware加载到内存中，由驱动传输到指定的设备上。

所以，总的来说，其实driver和firmware没有什么直接的关系，但firmware通常由驱动去加载。我们讨论的那个OS，一般不需要理解firmware是什么，只是把它当做数据。firmware是什么，只有使用这些数据的那个设备才知道。好比你用一个电话，电话中有一个软件，这个软件你完全不关心如何工作的，你换这个软件的时候，就可以叫这个软件是“固件”，但如果你用了一个智能手机，你要细细关系什么是上面的应用程序，Android平台，插件之类的细节内容，你可能就不叫这个东西叫“固件”了。

这种情况在计算机领域非常常见，所以大部分Spec都自己重新定义概念。比如说，我们平时写软件，说Component，很多就是只软件的其中一个部分，但在UEFI中，Component的定义是：

An executable image. Components defined in this specification support on elf the defined module types.

这是一个“独立的映像”，和我们一般理解的概念就完全不同，但如果你学计算机，请了解，这是我们的惯例。
————————————————
版权声明：本文为CSDN博主「AllFiredUp」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/weixin_36272622/article/details/112024476](https://blog.csdn.net/weixin_36272622/article/details/112024476)

### akonadi

Akonadi 框架为应用程序提供中心数据库来统一保存、索引和获取用户的个人信息。这包括邮件、联系人、日历、事件、日志、闹钟和笔记等。在 SC 4.4 中， KAddressBook 成为首个使用 Akonadi 框架的程序。在 SC 4.7 中， KMail, KOrganizer, KJots等也开始更新使用 Akonadi 。此外，一些 等离子 部件也使用 Akonadi 保存和获取日历事件、笔记等。

### iana-etc

安装的文件：
/etc/protocols 和 /etc/services
简要介绍
/etc/protocols

描述 TCP/IP 子系统中可用的多种 DARPA 网络协议, 该文件是网络协议定义文件，里面记录了TCP/IP协议族的所有协议类型。

/etc/services

提供友好文本名称和背后分配的端口号以及协议类型之间的映射

互联网号码分配局 (英語：Internet Assigned Numbers Authority，缩写IANA）

## cmake

一个跨平台的编译(Build)工具

## btrfs-progs

Userspace utilities to manage btrfs filesystems

## gst-plugins-base

This is GStreamer, a framework for streaming media.

## c-ares

c-ares是一个C语言实现的异步请求DNS的实现。很多知名 软件(curl、seastar、gevent、Nodejs等等)都使用了该软件。
