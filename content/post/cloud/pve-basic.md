---
title: "pve"
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
## "pve"

### 创建安装盘 U盘

>wiloon.com/ventoy

```bash
dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ
```

### 安装vim

```bash
apt update && apt install vim
```

### 去除 Proxmox 企业源

```bash
vi /etc/apt/sources.list.d/pve-enterprise.list

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

<https://192.168.50.xxx:8006>

## create vm

### 上传iso

把 ISO 上传到 Proxmox 宿主机的存储里
Datacenter> nuc8> local(nuc8) >ISO Images >-->Upload

### 创建虚拟机

```bash
create vm > 
    general > name: foo
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

在Proxmox VE中，qemu代理主要用于两件事:

1. 正确关闭虚拟机，而不是依赖ACPI命令或Windows策略

2. 在进行备份时冻结来宾文件系统 (在Windows上，使用卷tem影复制服务VSS) 。

### 改ip

```bash
     vi /etc/network/interfaces
```

### 显卡直通

<https://www.10bests.com/win10-htpc-on-pve/>

#### virtio-win.iso

<https://www.10bests.com/win10-htpc-on-pve/>

<https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/>

### 创建网桥

system>network>linux bridge
bridge ports: 支持同时添加多个网口，用空格分隔

### vm export/import

利用pve的备份恢复功能进行虚拟机的导入导出

使用备份功能备份为vma文件
使用WinSCP等软件复制vma备份文件至计算机
使用WinSCP等软件上传vma备份文件至另一台pve
使用恢复功能恢复虚拟机

## 备份恢复虚拟机

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

恢复虚拟机
登录pve02节点
切换至相应的上传存储 (local)
点击子菜单中的内容菜单
选择刚上传的vma备份文件
点击恢复按钮

设置恢复到的存储和VM ID
点击恢复按钮开始恢复

等待恢复完毕

六、测试启动导入的虚拟机

————————————————
版权声明: 本文为CSDN博主「Halyace」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/lyace2010/article/details/108918070>

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

<https://pve.proxmox.com/wiki/Main_Page>

<https://wangxingcs.com/2020/0307/1424/>

<https://www.10bests.com/install-openwrt-lede-on-pve/>

## 关闭屏幕, 熄屏

setterm -blank 1 // 5分钟后关闭屏幕，5 可以改成别的整数
GRUB_CMDLINE_LINUX="consoleblank=300" //每次开机后无操作都是5分钟关闭屏幕300的单位是秒

<https://www.xltyu.com/3276.html>
