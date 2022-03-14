---
title: libvirt、virsh、virt-manager
author: "-"
date: 2018-03-29T09:00:41+00:00
url: /?p=12089
categories:
  - Uncategorized

tags:
  - reprint
---
## libvirt、virsh、virt-manager
https://blog.csdn.net/wanglei_storage/article/details/51107648

libvirt、virsh、virt-manager 介绍
  
kvm 虚拟化中 libvirt 是目前使用最为广泛的对 kvm 虚拟机进行管理的工具和应用程序接口,而且一些常用的虚拟机管理工具 (virsh、virt-install、virt-manager等) 和云计算框架平台都在底层使用libvirt的应用程序接口。

virsh 是用于管理 虚拟化环境中的客户机和 Hypervisor 的命令行工具,与 virt-manager 等工具类似,它也是通过 libvirt API 来实现虚拟化的管理。virsh 是完全在命令行文本模式下运行的用户态工具,它是系统管理员通过脚本程序实现虚拟化自动部署和管理的理想工具之一。

virt-manager 是虚拟机管理器 (Virtual Machine Manager)  这个应用程序的缩写,也是管理工具的软件包名称。virt-manager 是用于管理虚拟机的图形化的桌面用户接口。