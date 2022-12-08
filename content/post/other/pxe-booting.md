---
title: PXE booting
author: "-"
date: 2015-04-18T10:03:43+00:00
url: /?p=7468
categories:
  - Inbox
tags:
  - reprint
---
## PXE booting

**预启动执行环境** (**Preboot eXecution Environment**，**PXE**，也被称为预执行环境)提供了一种使用网络接口 (Network Interface) 启动计算机的机制。这种机制让计算机的启动可以不依赖本地数据存储设备 (如硬盘) 或本地已安装的操作系统。

PXE当初是作为Intel的有线管理体系的一部分，Intel 和 Systemsoft于1999年9月20日公布其规格[版本2.1](1)。通过使用像网际协议(IP)、用户数据报协议(UDP)、动态主机设定协定(DHCP)、小型文件传输协议(TFTP)等几种网络协议和全局唯一标识符(GUID)、通用网络驱动接口(UNDI)、通用唯一识别码(UUID)的概念并通过对客户机(通过PXE自检的电脑)固件扩展预设的API来实现目的。

_PXE 客户机(client)_这个术语是指机器在PXE启动过程中的角色。一个_PXE 客户机(client)_可以是一台服务器、桌面级电脑、笔记本电脑或者其他装有PXE启动代码的机器。
