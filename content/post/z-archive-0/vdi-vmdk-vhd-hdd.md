---
title: VirtualBox磁盘镜像文件(VDI, VMDK, VHD, HDD)
author: "-"
date: 2011-10-17T15:27:21+00:00
url: /?p=1184
categories:
  - Uncategorized
tags:
  - VirtualBox

---
## VirtualBox磁盘镜像文件(VDI, VMDK, VHD, HDD)
(1)由VirtualBox的虚拟磁盘映像 (VDI) 的文件作为其自己的容器格式为主机硬盘。这是当用户创建一个新的虚拟机与一个新的磁盘将用于的格式。
  
(2)VirtualBox也支持VMware的VMDK容器格式。这种格式是颇为流行，和其他虚拟化软件使用。

(3)微软的VHD格式也完全由VirtualBox的支持；Microsoft Virtual PC的默认格式。

HDD: Parallels的第2版 (硬盘格式) 的镜像文件也被VirtualBox支持.由于缺乏新的格式 (3和4) 的文档,所以VirtualBox不支持。但是，可以使用由Parallels提供的工具版本2格式转换镜像文件。

Windows7的引导程序能够引导vhd格式的虚拟硬盘，而VirtualBox创建的虚拟硬盘文件是vdi格式的，

VirtualBox提供了VBoxManager.exe用来转换格式。


