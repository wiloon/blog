---
title: "pve basic"
author: "-"
date: ""
url: ""
categories:
  - Linux
tags:
  - Linux
  - VM
  - remix
---
## "pve basic"

### 创建安装盘 U盘

>wiloon.com/ventoy

```bash
dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ
```

### 安装vim

    apt update && apt install vim

### 去除Proxmox企业源

```bash
vi /etc/apt/sources.list.d/pve-enterprise.list

#deb https://enterprise.proxmox.com/debian/pve buster pve-enterprise
```

### 更新源

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
            advanced > start at boot

        next

        OS>use cd/dvd disc image file > iso image

        next

        Hard Disk>Disk size
        Hard Disk>Backup




    create vm > system > qemu agent: select

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

     vi /etc/network/interfaces

### 显卡直通

<https://www.10bests.com/win10-htpc-on-pve/>

#### virtio-win.iso

<https://www.10bests.com/win10-htpc-on-pve/>

#### virtio-win.iso
<https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/>

### 创建网桥

system>network>linux bridge
bridge ports: 支持同时添加多个网口，用空格分隔

### vm  export/import

利用pve的备份恢复功能进行虚拟机的导入导出

使用备份功能备份为vma文件
使用WinSCP等软件复制vma备份文件至计算机
使用WinSCP等软件上传vma备份文件至另一台pve
使用恢复功能恢复虚拟机

#### 备份虚拟机

登录pve01选择要备份的虚拟机
点击子菜单中的备份按钮
点击立即备份按钮
设置备份到的存储 (local的备份路径为: /var/lib/vz/dump)
设置模式: 停止(Stop)
设置压缩: 无
等待备份完毕

三、使用WinSCP下载备份
WinSCP可以使用SFTP连接pve节点
WinSCP下载地址: WinSCP官网

登录pve01节点

切换远程目录至备份目录 (local存储的备份目录为: /var/lib/vz/dump) 找到虚拟机备份文件右键点击下载

使用二进制方式下载vma备份文件至本机目录

等待下载完成

四、上传备份
使用WinSCP登录pve02节点
本地目录切换至刚下载备份的目录
右键点击vma备份文件选择上传

输入上传路径/var/lib/vz/dump/. (local存储的备份目录为: /var/lib/vz/dump) 并使用二进制方式上传

等待上传完毕

五、恢复虚拟机
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

    pvesh get /cluster/resources

#### 取得虚拟机当前状态

    pvesh get /nodes/PVE节点名称/qemu/虚拟机的id/status/current

#### 启动虚拟机的命令

    pvesh create /nodes/PVE节点名称/qemu/虚拟机的id/status/start
---

<https://pve.proxmox.com/wiki/Main_Page>
<https://wangxingcs.com/2020/0307/1424/>
<https://www.10bests.com/install-openwrt-lede-on-pve/>
