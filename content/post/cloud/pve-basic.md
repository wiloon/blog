+++
author = "w1100n"
date = "2020-08-08 12:28:15" 
title = "pve basic"

+++
### 创建安装盘 U盘
    dd bs=1M conv=fdatasync if=./proxmox-ve_*.iso of=/dev/XYZ

### 安装vim
    apt install vim

### 更新源
vim /etc/apt/sources.list

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
vim /etc/apt/sources.list.d/pve-enterprise.list

    #deb https://enterprise.proxmox.com/debian/pve buster pve-enterprise

https://pve.proxmox.com/wiki/Main_Page
https://wangxingcs.com/2020/0307/1424/