+++
author = "w1100n"
date = "" 
title = ""

+++

### create vm
把ISO上传到Proxmox宿主机的存储里
pve-->local(pve)-->Content-->Upload

create vm > general > name: foo
create vm > system > qemu agent: select

### qemu agent
Proxmox VE (PVE) Qemu代理 选项是什么意思，有什么作用，需要开启吗？

PVE在安装虚拟机时会见到这个选项，是开启还是关闭呢？

Qemu 代理即 qemu-guest-agent，是一个运行在虚拟机里面的程序 qemu-guest-agent是一个帮助程序，守护程序，它安装在虚拟机中。 它用于在主机和虚拟机之间交换信息，以及在虚拟机中执行命令。

在Proxmox VE中，qemu代理主要用于两件事：

1、正确关闭虚拟机，而不是依赖ACPI命令或Windows策略

2、在进行备份时冻结来宾文件系统（在Windows上，使用卷影复制服务VSS）。