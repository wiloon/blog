---
title: Proxmox VE, pve
author: "-"
date: 2020-04-25T16:35:56+00:00
url: /?p=16081
categories:
  - inbox
tags:
  - reprint
---
## Proxmox VE, pve

[https://www.proxmox.com/en/](https://www.proxmox.com/en/)

一、Proxmox VE 简介
  
Proxmox Virtual Environment，或 Proxmox VE，是来自德国的开源虚拟化方案。软件和社区支持都是免费的，企业用户则可以通过订阅制获得付费商业支持。

前几年我曾了解过 Proxmox VE，当时 PVE 的重心还在容器化 (OpenVZ 和 LXC) 上，因此没多做考虑。后来 PVE 的重心渐渐转移到虚拟机上，现在已经是相当成熟的 VM 虚拟化方案了。PVE 的虚拟化核心是 QEMU/KVM，因此可以说是「站在巨人的肩膀上」。QEMU 虽然成熟而强大，但是使用与管理却不够用户友好，PVE 则是补上了这缺失的一环，通过直观的网页管理界面和高效的命令行工具，让各种用户都能愉快地管理虚拟机。

贯彻「不重复造轮子」的原则，当前版本的 PVE 基于成熟稳定的 Debian 9 "Stretch" 构建。在熟悉和使用 PVE 的过程中，我越发喜欢它「不重复造轮子」的特性。相较之前用过的其他虚拟化方案，PVE 的内部构造和工作原理对我来说不再是一个黑盒，我可以清晰地观测到它在干什么——比如要迁移一台虚拟机到另一个节点，我就可以通过 ps 观察到它启动了一个 dd 进程，对接 ssh 管道，将磁盘数据通过网络复制到目标机器——这种仿佛透明手表一样能看到内部工作原理的感觉真是太棒了！

二、Proxmox VE 安装
  
用户可以直接在现有的 Debian 上安装 PVE 相关的软件包，将之改造成 PVE 节点，但更推荐的方法是直接用官方提供的 ISO 文件，完成全系统的安装。安装过程中除了问装到哪儿之类的常规问题，没有别的复杂情况。安装完之后会重启，重启完成后即可使用 SSH 登录，或是用 `https://<ipaddress>:8006/` 访问网页管理页面 (注意是 https://) ，这一地址也会打印在屏幕上 (如果你忘了的话) 。

网页或是命令行管理真是方便啊，再也不用在 Windows 虚拟机里运行 Citrix XenCenter 或是 VMware vSphere Client 了。

网络
PVE网络配置官方文档: [https://pve.proxmox.com/wiki/Network_Configuration](https://pve.proxmox.com/wiki/Network_Configuration)

可以通过GUI或通过手动编辑文件/etc/network/interfaces来完成网络配置，该文件包含整个网络配置。以下介绍两种常用模式。

## 网桥模式(默认网络模式)

网桥模式(默认网络模式)
网桥就像用软件实现的物理网络交换机。所有虚拟机都可以共享一个网桥，或者您可以创建多个网桥来分离网络域。每个主机最多可以有4094个网桥。
安装程序将创建一个名为vmbr0的网桥，该网桥连接到第一个以太网卡。/etc/network/interfaces中的相应配置可能如下所示 (不同网口配置，需要使用空行分隔) :

[https://wzyboy.im/post/1293.html](https://wzyboy.im/post/1293.html)
