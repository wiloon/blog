---
title: PVE
author: "-"
date: "2022-09-10 15:39:49"
url: "pve"
categories:
  - Linux
tags:
  - Linux
  - VM
  - remix
---
## PVE

## macos

```bash
hdiutil convert proxmox-ve_8.3-1.iso -format UDRW -o proxmox-ve_8.3-1.dmg
diskutil list
# insert the USB flash drive
diskutil list
diskutil unmountDisk /dev/diskX

# rdiskX, instead of diskX, in the last command is intended. It will increase the write speed.
sudo dd if=proxmox-ve_8.3-1.dmg bs=1M of=/dev/rdisk5
```

### 创建安装盘 U盘

>wiloon.com/ventoy

```bash
dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ
```

### 去除 Proxmox 企业源

```bash
apt update && apt install vim
vim /etc/apt/sources.list.d/pve-enterprise.list

#deb https://enterprise.proxmox.com/debian/pve buster pve-enterprise
```

## 更新源

### pve 6.x

vi /etc/apt/sources.list

```bash
#deb http://ftp.debian.org/debian buster main contrib
#deb http://ftp.debian.org/debian buster-updates main contrib
# security updates
#deb http://security.debian.org buster/updates main contrib

# debian aliyun source
deb https://mirrors.aliyun.com/debian buster main contrib non-free
deb https://mirrors.aliyun.com/debian buster-updates main contrib non-free
deb https://mirrors.aliyun.com/debian-security buster/updates main contrib non-free

# proxmox source
# deb http://download.proxmox.com/debian/pve buster pve-no-subscription
deb https://mirrors.ustc.edu.cn/proxmox/debian/pve buster pve-no-subscription
```

### pve 7.2

```bash
deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib

deb http://ftp.debian.org/debian bullseye main contrib

deb http://ftp.debian.org/debian bullseye-updates main contrib

# security updates
deb http://security.debian.org bullseye-security main contrib
deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription
```

## 管理页面

https://192.168.50.xxx:8006

## create vm

### 上传iso

把 ISO 上传到 Proxmox 宿主机的存储里
Datacenter> nuc8> local(nuc8) >ISO Images >-->Upload

### 创建虚拟机

```bash
create vm >
    general > name: nam_0
    general > advanced
        advanced > start at boot

    next

    OS> use cd/dvd disc image file > iso image

    next

    Hard Disk> Disk size
    Hard Disk> Backup

create vm > system > qemu agent: select
```

### create vm from template

- right click and select "clone"
- Name: input the name of new vm
- mode: full clone
- target storage: local-lvm
- 调整内存大小
- 启动

### qemu agent

Proxmox VE (PVE) Qemu代理 选项是什么意思，有什么作用，需要开启吗？

PVE在安装虚拟机时会见到这个选项，是开启还是关闭呢？

Qemu 代理即 qemu-guest-agent，是一个运行在虚拟机里面的程序 qemu-guest-agent是一个帮助程序，守护程序，它安装在虚拟机中。 它用于在主机和虚拟机之间交换信息，以及在虚拟机中执行命令。

在 Proxmox VE中，qemu代理主要用于两件事:

1. 正确关闭虚拟机，而不是依赖ACPI命令或Windows策略
2. 在进行备份时冻结来宾文件系统 (在Windows上，使用卷tem影复制服务VSS) 。

### 改ip

```bash
vi /etc/network/interfaces
```

### 显卡直通

[https://www.10bests.com/win10-htpc-on-pve/](https://www.10bests.com/win10-htpc-on-pve/)

#### virtio-win.iso

[https://www.10bests.com/win10-htpc-on-pve/](https://www.10bests.com/win10-htpc-on-pve/)

[https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/)

### 创建网桥

system>network>linux bridge
ipv4/cidr: 192.168.50.6/24
gateway: 192.168.50.1
bridge ports: 支持同时添加多个网口，用空格分隔

网桥创建好之后, 默认是 active: no, 要点击 apply configuration 来激活

### vm export/import

利用 pve 的备份恢复功能进行虚拟机的导入导出

使用备份功能备份为vma文件
使用WinSCP等软件复制vma备份文件至计算机
使用WinSCP等软件上传vma备份文件至另一台pve
使用恢复功能恢复虚拟机

## 备份恢复虚拟机, pve vm backup

### 备份虚拟机

登录 pve 选择要备份的虚拟机
磁盘需要勾选备份选项: tick the box, Hardware> Hard Disk> Edit> Advanced> Backup
从 Hardware 菜单切换到 Backup 点击子菜单中的备份按钮
点击立即备份按钮(Backup now)
设置备份到的存储 (local的备份路径为: /var/lib/vz/dump)
设置模式(Mode): 停止(Stop)
设置压缩: 无
等待备份完毕

```bash
# 页面打印的日志里能找到 文件路径 INFO: creating vzdump archive '/var/lib/vz/dump/vzdump-qemu-105-2022_09_10-15_19_12.vma.zst'
scp root@192.168.50.5:/var/lib/vz/dump/vzdump-qemu-105-2022_09_10-15_19_12.vma.zst .
```

### 恢复

```bash
scp vzdump-qemu-105-2022_09_10-15_19_12.vma.zst root@192.168.50.7:/var/lib/vz/dump/
```

等待上传完毕

#### 恢复虚拟机

登录pve02节点
切换至相应的上传存储 (local)
点击子菜单中的内容菜单
选择刚上传的vma备份文件
点击恢复按钮 (Restore)

设置恢复到的存储和 VM ID
点击恢复按钮开始恢复

等待恢复完毕

测试启动导入的虚拟机

### pve cli

#### 查看一下虚拟机的运行状态

```bash
    pvesh get /cluster/resources
```

#### 取得虚拟机当前状态

```bash
    pvesh get /nodes/PVE节点名称/qemu/虚拟机的id/status/current
```

#### 启动虚拟机的命令

```bash
    pvesh create /nodes/PVE节点名称/qemu/虚拟机的id/status/start
```

[https://pve.proxmox.com/wiki/Main_Page](https://pve.proxmox.com/wiki/Main_Page)

[https://wangxingcs.com/2020/0307/1424/](https://wangxingcs.com/2020/0307/1424/)

[https://www.10bests.com/install-openwrt-lede-on-pve/](https://www.10bests.com/install-openwrt-lede-on-pve/)

## 关闭屏幕, 熄屏

```bash
setterm --blank 1 # 1分钟后关闭屏幕，1 可以改成别的整数
# setterm 不能通过 ssh  执行, ssh 执行 setterm 会报错 setterm: terminal xterm-256color does not support --blank
# 只能连物理键盘执行
GRUB_CMDLINE_LINUX="consoleblank=300" # 每次开机后无操作都是5分钟关闭屏幕300的单位是秒
```

[https://www.xltyu.com/3276.html](https://www.xltyu.com/3276.html)

————————————————
版权声明: 本文为CSDN博主「Halyace」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: [https://blog.csdn.net/lyace2010/article/details/108918070](https://blog.csdn.net/lyace2010/article/details/108918070)



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
