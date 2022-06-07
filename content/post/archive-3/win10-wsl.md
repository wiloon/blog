---
title: windows wsl
author: "w1100n"
date: 2019-03-28T09:40:51.000+00:00
url: "wsl"
categories:
  - Linux
tags:
  - reprint
---
## windows wsl

WSL: windows subsystem for Linux

### command

```bash
    wsl --shutdown
    wsl --list --verbose
    wsl -l -v
    # 查看wsl状态
    wsl --status

    # reboot, 先 shutdown 再打开就行了...
```

### 微软的官方安装文档

<https://docs.microsoft.com/zh-cn/windows/wsl/install>

### 开启 windows 功能

搜索 windows 功能， 勾选 `适用于 linux 的 windows 子系统` 和 `虚拟机平台`， 点击确认后会提示重启。

```bash

wsl --list --online
wsl --install -d Ubuntu-20.04

```

### 0x800701bc

download the linux kernel update package

<https://aka.ms/wsl2kernel>

### wslg

<https://github.com/microsoft/wslg>

升级wsl到最新版本

    wsl --update

#### 安装 intel 显示驱动

    https://downloadcenter.intel.com/download/30579/Intel-Graphics-Windows-DCH-Drivers

### ssh-agent, keepassxc

<https://code.mendhak.com/wsl2-keepassxc-ssh/>

### 启用 openssh authentication agent

计算机管理>服务>openssh authentication agent > 启动>启动类型>自动

## 下载 npiperelay

<https://github.com/jstarks/npiperelay/releases/download/v0.1.0/npiperelay_windows_amd64.zip>

### 安装 socat

```bash
sudo apt install socat
```

### vim .zshrc

```bash
export SSH_AUTH_SOCK=$HOME/.ssh/agent.sock

ss -a | grep -q $SSH_AUTH_SOCK
if [ $? -ne 0 ]; then
    rm -f $SSH_AUTH_SOCK
    (setsid socat UNIX-LISTEN:$SSH_AUTH_SOCK,fork EXEC:"/mnt/c/workspace/apps/npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork &) >/dev/null 2>&1
fi

ssh-add -L 
```

### wsl 卸载

    wsl --unregister Ubuntu

---

### 步骤 1 - 启用适用于 Linux 的 Windows 子系统

    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

### 检查windows的版本

    winver

### 步骤 3 - 启用虚拟机功能

    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

### 从windows应用商店安装ubuntu20.4

### 步骤 4 - 下载 Linux 内核更新包, 并安装

### 步骤 5 - 将 WSL 2 设置为默认版本

    wsl --set-default-version 2

### 把前面安装的wsl转换成wsl2

    wsl --set-version Ubuntu-20.04 2

### 步骤 6 - 安装所选的 Linux 分发

## 进入wsl2 的 ubuntu

### 配置ubuntu 镜像源, aliyun mirror

<https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b111bQgY0>

    vim /etc/apt/source.list

## 用以下内容覆盖/etc/apt/source.list

```bash
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```

### 更新系统

    sudo apt update
    sudo apt upgrade

### 安装各种依赖包

<https://www.jianshu.com/p/572c86b55a68>

    sudo apt install golang git python make maven openjdk-8-jdk ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy

### 安装nodejs

<https://github.com/nodesource/distributions/blob/master/README.md>
    curl -sL <https://deb.nodesource.com/setup_14.x> | sudo -E bash -
    sudo apt-get install -y nodejs

### config npm mirror

    npm install -g mirror-config-china --registry=http://registry.npm.taobao.org

### maven 配置

    mkdir ~/.m2
    vim ~/.m2/settingxxxx

### golang proxy

    vim .bashrc
    export GO111MODULE=on
    export GOPROXY=https://goproxy.cn

### 检查包的版本

    node -v && npm -v && go version

### maven sprint boot run

      mvn spring-boot:run

### 固定ip

#### wsl 自动设置display ip

vim .bashrc
vim .zshrc

    export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0

### windows firewall

    advanced rule add rule: tcp port 0

#### windows脚本设置网卡Ip

<https://blog.csdn.net/manbu_cy/article/details/108476859>

    @echo off
    setlocal enabledelayedexpansion

        :: set wsl2 ip
        wsl -u root ip addr | findstr "192.168.96.2" > nul
        if !errorlevel! equ 0 (
            echo wsl ip has set
        ) else (
            wsl -u root ip addr add 192.168.96.2/28 broadcast 192.168.96.15 dev eth0 label eth0:1
            echo set wsl ip success: 192.168.96.2
        )


        :: set windows ip
        ipconfig | findstr "192.168.96.1" > nul
        if !errorlevel! equ 0 (
            echo windows ip has set
        ) else (
            netsh interface ip add address "vEthernet (WSL)" 192.168.96.1 255.255.255.240
            echo set windows ip success: 192.168.96.1
        )
        
    pause

### 设置默认的用户

    powershell
    cd C:\Users\用户名\AppData\Local\Microsoft\WindowsApps
    dir
    # 有一个是以ubuntu开头的exe文件
    ubuntu2004.exe config --default-user user0

### wsl字体,乱码

><https://zhuanlan.zhihu.com/p/68336685>

    git clone https://github.com/powerline/fonts.git --depth=1 # windows 下需先安装 git
    用 powershell 执行 install.ps1

#### 修改 wsl 字体

    左上角图标-->属性-->字体-->Noto Mono for powerline

### VcXsrv 安装

从SourceForge上面下载最新版本的 VcXsrv  

    https://sourceforge.net/projects/vcxsrv/files/vcxsrv/

#### 启动开始菜单中的XLaunch

##### VcXsrv 配置

- Display settings
  - One large window
  - Display number: -1
- Client startup
  - Start no client
- Extra settings
  - Clipboard
    - Primary Selection
  - Native opengl
  - Disable access control

### wsl2 内安装 xfce4

    sudo apt install -y xfce4
    # nameserver后面的地址就是Windows系统虚拟网卡的地址,记一下,同时需要取消下面两行内容的注释,禁用自动重新生成配置文件,否则重启后这个地址会变
    [network]
    generateResolvConf = false

    vim ~/.bashrc
    # 在文件最后追加下面内容,地址使用上面查看到的
    export DISPLAY=192.168.112.1:0
    # in WSL 2
    # windows里wsl网卡的ip,每次启动都 会变, 子系统 .bashrc里加这一句动态设置display 
    export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
    # 启动xfce4
    startxfce4

### resolv.conf

    sudo vim /etc/resolv.conf

#### windows 防火墙配置

选择 公用网络, 否则 执行startxfce4 后报错 无法连接

### 快捷键

        Alt + Enter 全屏
        Alt + F2 新建窗口
        Alt + F3 搜索文本
        Ctrl + [Shift] + Tab 切换窗口
        Ctrl + = + - 0 缩放
        Ctrl + Click 打开光标处的文件、目录名或者网址

### wsl2 Install the Linux kernel update package

<https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel>

### command

```bash
# 列出当前已经安装且随时可用的发行版
wslconfig /list
# 列出所有发行版，包括正在安装、卸载和已损坏的发行版
wslconfig /list /all
# 卸载已经安装的发行版
wslconfig /unregister <这里填你要卸载的名称，只能填写使用wslconfig /list或者wslconfig /list /all中所包含的，不是随便填的>
```

## 把wsl的磁盘移到 d 盘

```bash
Run powershell.exe as Administrator

    PS C:\WINDOWS\system32> wsl -l
    Windows Subsystem for Linux Distributions:
    Ubuntu (Default)

    # mkdir D:\workspace\wsl

    PS C:\WINDOWS\system32> wsl --export Ubuntu S:\ISOs\ubuntu-wsl.tar

    # mkdir D:\workspace\vm\ubuntu-wsl

    PS C:\WINDOWS\system32> cd D:\workspace\vm\ubuntu-wsl
    PS W:\VMs> mkdir ubuntu-wsl
    PS W:\VMs> wsl --unregister Ubuntu
    Unregistering...
    PS W:\VMs> wsl --import Ubuntu W:\VMs\ubuntu-wsl S:\ISOs\ubuntu-wsl.tar
    PS W:\VMs> wsl -l
    Windows Subsystem for Linux Distributions:
    Ubuntu (Default)
```

### wsl2 graphical

<https://zhuanlan.zhihu.com/p/150555651>

### wsl2的ip每次都 会变的问题, 在windows里可以直接访问 localhost:xxxx, wsl2会把所有端口映射到windows 的 localhost

<https://github.com/microsoft/WSL/issues/4210>  
With the latest update, you can access remote ports(WSL2) as local on Windows Host

### .wslconfig

```r
    %UserProfile%\.wslconfig
    C:\Users\user0\.wslconfig


    [wsl2]
    kernel=<path>              # An absolute Windows path to a custom Linux kernel.
    memory=<size>              # How much memory to assign to the WSL2 VM.
    processors=<number>        # How many processors to assign to the WSL2 VM.
    swap=<size>                # How much swap space to add to the WSL2 VM. 0 for no swap file.
    swapFile=<path>            # An absolute Windows path to the swap vhd.
    localhostForwarding=<bool> # Boolean specifying if ports bound to wildcard or localhost in the WSL2 VM should be connectable from the host via localhost:port (default true).

    # <path> entries must be absolute Windows paths with escaped backslashes, for example C:\\Users\\Ben\\kernel
    # <size> entries must be size followed by unit, for example 8GB or 512MB
```

### auto start service

<https://github.com/shayne/wsl2-hacks/blob/master/README.md>

### Windows Terminal 中 WSL2 默认打开路径(startingDirectory)

打开Windows Terminal。鼠标点击进入设置，或者同时按ctrl和逗号。  

找到如下内容:

```json
{
    "guid": "{07b52e3e-de2c-5db4-bd2d-ba144ed6c273}",
    "hidden": false,
    "name": "Ubuntu-20.04",
    "source": "Windows.Terminal.Wsl",
    "startingDirectory": "\\wsl$\Ubuntu-20.04\home\wiloon",
},
```

添加/修改如下行:

"startingDirectory": "\\wsl$\Ubuntu-20.04\home\wiloon",

### 修改 Windows Terminal 默认打开的 Shell

修改 defaultProfile 的值为对应的 guid 即可。

例如:

"defaultProfile": "{c6eaf9f4-32a7-5fdc-b5cf-066e8a4b1e40}",
guid 需要替换为自己配置文件中的相应值。

### keepassxc win10 wsl2

```r
    title: keepassxc
```

### windows 访问wsl2文件

```bat
    \\wsl$\Ubuntu-20.04\usr\bin\git
```

---

[https://discourse.ubuntu.com/t/getting-graphical-applications-to-work-on-wsl2/11868](https://discourse.ubuntu.com/t/getting-graphical-applications-to-work-on-wsl2/11868 "https://discourse.ubuntu.com/t/getting-graphical-applications-to-work-on-wsl2/11868")

[https://wiki.ubuntu.com/WSL?_ga=2.253396937.1563783499.1590728512-1733404080.1590728512#Running_Graphical_Applications](https://wiki.ubuntu.com/WSL?_ga=2.253396937.1563783499.1590728512-1733404080.1590728512#Running_Graphical_Applications "https://wiki.ubuntu.com/WSL?_ga=2.253396937.1563783499.1590728512-1733404080.1590728512#Running_Graphical_Applications")

<https://c1oudust.me/blog/Windows10%E4%B8%8B%E4%BD%BF%E7%94%A8Linux%E7%9A%84%E5%8F%A6%E4%B8%80%E7%A7%8D%E6%96%B9%E5%BC%8F%20%E2%80%94%E2%80%94%20WSL%E4%B8%8E%E5%85%B6%E6%A1%8C%E9%9D%A2%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%8520180509/>

<http://www.yuan-ji.me/%E5%A6%82%E4%BD%95%E5%9C%A8Windows-Subsystem-for-Linux-(WSL)-%E4%B8%8A%E8%BF%90%E8%A1%8CLinux-GUI-%E8%BD%AF%E4%BB%B6/>

<https://www.reddit.com/r/bashonubuntuonwindows/comments/9lpc0o/ubuntu_1804_dbus_fix_instructions_with/>

<https://github.com/QMonkey/wsl-tutorial>

<https://github.com/yuk7/ArchWSL>

<https://zhuanlan.zhihu.com/p/34884285>

><https://docs.microsoft.com/zh-cn/windows/wsl/basic-commands>
