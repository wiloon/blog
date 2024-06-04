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

## apt-select

```Bash
# https://pypi.org/project/apt-select/
pip install apt-select
apt-select -C JP
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup && sudo mv sources.list /etc/apt/
```

## mirrors

http://mirrors.ubuntu.com/

## deb, deb-src

不是要看代码或者自己编译的话 deb-src 可以不要

## backports proposed security updates

简单的解释：
基础：由于ubuntu是每6个月发行一个新版，当发行后，所有软件包的版本在这六个月内将保持不变，即使是有新版都不更新。除开重要的安全补丁外，所有新功能和非安全性补丁将不会提供给用户更新。

security：仅修复漏洞，并且尽可能少的改变软件包的行为。低风险。
backports：backports 的团队则认为最好的更新策略是 security 策略加上新版本的软件（包括候选版本的）。但不会由Ubuntu security team审查和更新。
update：修复严重但不影响系统安全运行的漏洞，这类补丁在经过QA人员记录和验证后才提供，和security那类一样低风险。
proposed：update类的测试部分，仅建议提供测试和反馈的人进行安装。

个人认为：
1.重要的服务器：用发行版默认的、security
2.当有要较新软件包才行能运作的服务器：用发行版默认的、 security、（backports 还是不适合）
3.一般个人桌面：用发行版默认的、 security、backports、update
4.追求最新、能提供建议和反馈大虾：发行版默认的、 security、backports、update、proposed 全部用上！

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
deb http://mirrors.163.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ jammy-backports main restricted universe multiverse
```

```bash
vim /etc/apt/sources.list
%s/archive.ubuntu.com/mirrors.163.com/g
```

#### tsinghua

```bash
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse

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
## 中文语言环境, 设置后 vim 进入编辑状态屏幕下方会显示中文"插入"的那种
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

[https://blog.csdn.net/weixin_39792252/article/details/80415550](https://blog.csdn.net/weixin_39792252/article/details/80415550)

### 查看软件安装位置

```bash
dpkg -L openjdk-8-source
whereis openjdk-8-source
```

### apt 查看软件包版本

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

## 区域语言

ls -l 文件日期显示中文的问题

Region & Language> Manage Installed Languages> Regional Formats> Display numbers, dates and currency amounts in the usual format for: English(United States)

apply system-wide

## add a shell script to launcher as shortcut

Create *.desktop file, location depends on if it is for personal use or all users. If these directories do not exist, create them.
For personal use , ~/.local/share/applications
.desktop 文件不能用软链接

gedit ~/.local/share/applications/name.desktop
For all users, /usr/local/share/applications/ (or /usr/share/applications/ depending upon your system).

sudo -i gedit /usr/share/applications/name.desktop
Paste below text

[Desktop Entry]
Type=Application
Terminal=true
Name=unmount-mount
Icon=/path/to/icon/icon.svg
Exec=/path/to/file/mount-unmount.sh
edit Icon= and Exec= and Name=

Also Terminal=True/false determines whether the terminal opens a window and displays output or runs in the background

put this in unity panel by dragging it from files manager

logic is very simple that unity panel allows *.desktop files as launcher though I haven't tried it because I use Natty.
Exec= 指定的Shell脚本不能有 nohup, 实际上也不需要 nohup, 设置 Terminal=false terminal 不会弹出来

https://askubuntu.com/questions/141229/how-to-add-a-shell-script-to-launcher-as-shortcut

I was facing this problem and I will share my notes in case it helps someone.

If the .desktop file is for all users to use then it should be placed under /usr/local/share/applications.
If the .desktop file is only for the current user then it should be placed under ~/.local/share/applications.
The .desktop file placed as above does not need execute permissions. It can be 0644.
If the .desktop file has a key Hidden then it should be Hidden=false.
If the .desktop file has a key NoDisplay then it should be NoDisplay=false.
The Exec key should have a valid command. Bash commands may not work as detailed in this answer.
With these settings in place the desktop entry should be searchable using the Super key, and from there using the Right Click -> Add to Favorites option, it can be setup as a favorite on the dash.

Note: In the above bullet points, "Has a key" means if the key is present in the config file. Alternatively, it can be absent, in which case the default value for that key takes effect.

https://askubuntu.com/questions/1387328/add-to-favorites-not-available-for-manually-created-desktop-item

https://askubuntu.com/questions/526308/i-created-a-desktop-file-in-usr-share-applications-but-it-doesnt-show-up-in-d/527154#527154

## super key

windows key

## dev env

- citrix
  - 能打开远程桌面
  - 不能传文件，看不到 C 盘, 也许通过配置能解决
- Jetbrains OK
- webex
  - fcitx 偶尔能输入中文, 有时候没有响应,只能用英文
  - 会议模式 ok, 音质销差但是不影响
  - 不能共享屏幕
- 中文输入法
  - 某些 APP 有可能用不了中文输入法，有可能需要在外面输中文再拷进去
- outlook 用网页版

## indicator-sysmonitor

https://ubuntuhandbook.org/index.php/2023/01/indicator-show-cpu-gpu-memory-ubuntu-panel/

https://github.com/fossfreedom/indicator-sysmonitor

```Bash
cpu: {cpu} {cputemp} mem: {mem} network: {upordown} {net}
```