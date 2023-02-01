---
author: "-"
date: "2020-10-09 14:34:24" 
title: ubuntu basic
categories:
  - inbox
tags:
  - reprint
---
## ubuntu basic

## Ubuntu 22.04 LTS (Jammy Jellyfish)

### ubuntu mirror

#### aliyun

```bash
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
```

#### 163

```bash
deb http://mirrors.163.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ jammy main restricted universe multiverse

deb http://mirrors.163.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ jammy-security main restricted universe multiverse

deb http://mirrors.163.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ jammy-updates main restricted universe multiverse

deb http://mirrors.163.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ jammy-proposed main restricted universe multiverse

deb http://mirrors.163.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ jammy-backports main restricted universe multiverse
```

```bash
    vim /etc/apt/sources.list
    %s/archive.ubuntu.com/mirrors.163.com/g
```

#### tsinghua

```bash
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse

```

### WSL

```bash
export DISPLAY=172.18.80.1:0 # windows 里ipconfig看到的连接wsl的ip
apt install git-svn
apt install openjdk-8-jdk
apt install maven
# config ~/.m2/settings.xml
apt install nautilus
sudo apt-get install ttf-wqy-microhei  #文泉驿-微米黑
sudo apt-get install ttf-wqy-zenhei  #文泉驿-正黑
sudo apt-get install xfonts-wqy #文泉驿-点阵宋体
sudo apt install keepassxc
```

### 中文乱码问题

```bash
# 安装中文支持包language-pack-zh-hans
sudo apt-get install language-pack-zh-hans
# 设置语言
vim /etc/environment
## 中文语言环境, 设置后 vim 进程编辑状态屏幕下方会显示中文"插入"的那种
LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh:en_US:en"
## 英文环境 
LANG="en_US.UTF-8"
LANGUAGE="en_US:en" 

vim /var/lib/locales/supported.d/local
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8
zh_CN.GBK GBK
zh_CN GB2312

sudo locale-gen
# 中文乱码是空格的情况，安装中文字体解决
sudo apt-get install fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming
```

<https://blog.csdn.net/weixin_39792252/article/details/80415550>

### 查看软件安装位置

```bash
dpkg -L openjdk-8-source
whereis openjdk-8-source
```

### 查询版本

```bash
apt show openjdk-8-source
dpkg -l openjdk-8-source
```

### PPA

为什么要用 PPA
如你所见，Ubuntu 对系统中的软件进行管理，更重要的是控制你在系统上获得哪个版本的软件。但想象一下开发人员发布了软件的新版本的情况。

Ubuntu 不会立即提供该新版本的软件。需要一个步骤来检查此新版本的软件是否与系统兼容，从而可以确保系统的稳定性。

但这也意味着它需要经过几周才能在 Ubuntu 上可用，在某些情况下，这可能需要几个月的时间。不是每个人都想等待那么长时间才能获得他们最喜欢的软件的新版本。

类似地，假设有人开发了一款软件，并希望 Ubuntu 将该软件包含在官方软件仓库中。在 Ubuntu 做出决定并将其包含在官方存软件仓库之前，还需要几个月的时间。

另一种情况是在 beta 测试阶段。即使官方软件仓库中提供了稳定版本的软件，软件开发人员也可能希望某些终端用户测试他们即将发布的版本。他们是如何使终端用户对即将发布的版本进行 beta 测试的呢？

通过 PPA！

## 网络

## netplan

```bash
# manually install netplan.io
sudo apt-get update
sudo apt-get -y install netplan.io

```

### 动态IP

```bash
sudo vim /etc/netplan/00-installer-config.yaml

network:
  ethernets:
    ens18:
      dhcp4: true
  version: 2
```

## 静态 IP, /etc/netplan/00-installer-config.yaml

```bash
network:
  ethernets:
    ens18:
      addresses: [192.168.50.140/24]
      dhcp4: false
      optional: true
      gateway4: 192.168.50.4
      nameservers:
        addresses: [192.168.50.1]
  version: 2
```

```bash
# 使配置生效
sudo netplan apply

```
