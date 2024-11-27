---
title: rfkill
author: "-"
date: 2016-11-08T01:28:51+00:00
url: /?p=9370
categories:
  - Inbox
tags:
  - reprint
---
## rfkill
https://linux.cn/article-5957-1.html


很多计算机系统包含无线电传输,其中包括Wi-Fi、蓝牙和3G设备。这些设备消耗电源,在不使用这些设备时是一种能源浪费。

RFKill 是Linux内核中的一个子系统,它可提供一个接口,在此接口中可查询、激活并取消激活计算机系统中的无线电传输。当取消激活传输时,可使其处于可被软件重新激活的状态 ( 软锁定 ) 或软件无法重新激活的位置 ( 硬锁定 ) 。

RFKill 为内核子系统提供应用程序编程界面 (API) 。内核驱动程序被设计为支持RFKill使用这个API注册内核,并包含启用和禁用这个设备的方法。另外,RFKill提供用户程序可解读的通知以及用户程序查询传输状态的方法。

RFKill接口位于 /dev/rfkill,其中包含系统中所有无线电传输的当前状态。每个设备都在 sysfs 中注册当前RFKill状态。另外,在启用了RFKill的设备中每当状态更改时,RFKill会发出 uevents。

rfkill 是一个命令行工具,您可使用它查询和更改系统中启用了RFKill的设备。要获得这个工具,请安装 rfkill 软件包。

如果开机时在可以搜索到无线网络且输入密码正确但仍然无法接入的情况下,就可能是rfkill这个程序阻拦了接入,它是个用来控制无线网络及蓝牙的使用的软开关。

使用命令 rfkill list 获得设备列表,每个都包含与之关联的索引号 ,从 0 开始。

rfkill list

您可以使用这个索引号让 rfkill 停使或者使用某个设备,例如: 

rfkill block 0
  
停用系统中第一个启用RFKill的设备。

您还可以使用 rfkill 阻断某一类设备,或者所有启用了RFKill的设备。例如: 

rfkill block wifi
  
停用系统中的所有Wi-Fi设备。要停用所有启用了RFKill的设备,请运行: 

rfkill block all
  
要重新使用设备,请运行 rfkill unblock。要获得 rfkill 可停用的完整设备类别列表,请运行 rfkill help。