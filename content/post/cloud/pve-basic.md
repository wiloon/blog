+++
author = "-"
date = "2020-08-08 12:28:15" 
title = "pve basic"

+++
### 创建安装盘 U盘
    dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ

### 更新源
vi /etc/apt/sources.list

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

### 去除Proxmox企业源
vi /etc/apt/sources.list.d/pve-enterprise.list

    #deb https://enterprise.proxmox.com/debian/pve buster pve-enterprise

### 安装vim
    apt update && apt install vim

### 访问管理页面
    https://192.168.50.xxx:8006

### create vm
#### 上传iso
把ISO上传到Proxmox宿主机的存储里
Datacenter>nuc8>local(nuc8)>ISO Images>-->Upload
### 创建虚拟机
    create vm > 
        general > name: foo
        general > advanced
        general > start at boot
        OS>use cd/dvd disc image file


create vm > system > qemu agent: select

### qemu agent
Proxmox VE (PVE) Qemu代理 选项是什么意思，有什么作用，需要开启吗？

PVE在安装虚拟机时会见到这个选项，是开启还是关闭呢？

Qemu 代理即 qemu-guest-agent，是一个运行在虚拟机里面的程序 qemu-guest-agent是一个帮助程序，守护程序，它安装在虚拟机中。 它用于在主机和虚拟机之间交换信息，以及在虚拟机中执行命令。

在Proxmox VE中，qemu代理主要用于两件事：

1、正确关闭虚拟机，而不是依赖ACPI命令或Windows策略

2、在进行备份时冻结来宾文件系统（在Windows上，使用卷影复制服务VSS）。

### 改ip
     vi /etc/network/interfaces

### 显卡直通
https://www.10bests.com/win10-htpc-on-pve/
#### virtio-win.iso
https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/

### 创建网桥
system>network>linux bridge
bridge ports: 支持同时添加多个网口，用空格分隔

---

https://pve.proxmox.com/wiki/Main_Page
https://wangxingcs.com/2020/0307/1424/
https://www.10bests.com/install-openwrt-lede-on-pve/