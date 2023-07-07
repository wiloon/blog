---
title: windows basic, win basic
author: "-"
date: 2011-10-14T05:20:22+00:00
url: windows
categories:
  - inbox
tags:
  - reprint
---
## windows basic, win basic

## cmd

```bash
## 删除 目录
remove-item dir0  -recurse -force
copy C:\Users\desktop\foo.txt D:\backup\ /y
# force overwrite
copy /b/v/y C:\Users\desktop\foo.txt D:\backup\

# cmd-连续执行多条命令
copy C:\Users\desktop\foo.txt D:\backup\ && D:\backup\foo.exe
```

## ISO

<https://isofiles.bd581e55.workers.dev/>

## win10 应用开机启动, 启动项

打开运行 `win + r`, 输入 `shell:startup`, 将该应用的快捷方式从文件位置复制并粘贴到 “启动” 文件夹中。

### msdn i tell u

<https://www.itellu.com/2021/06/22/win11-v2021-v1/>

### windows iso

打开页面: <https://www.microsoft.com/zh-cn/software-download/windows10>
点击 立即下载工具
运行 MediaCreationTool21H1.exe
选择 "为另一台电脑创建安装介质"

### uupdump

<https://uupdump.net/>

### 查看 windows 的版本

```bash
winver
```

### bat 脚本控制网卡启用禁用

```bash
netsh interface set interface "eth0" disabled
netsh interface set interface "eth0" enabled
```

### Windows 命令行 (批处理文件) 延迟 (sleep) 方法, 使用ping 的定时功能，精度1秒

```bash
ping -n 3 127.0.0.1>nul
```

说明: 3为ping包发送次数，可作为延迟秒数进行使用，需要延迟几秒就设置几。  
nul避免屏幕输出，将输出输入到空设备，因为不需要结果，仅用到其定时功能。  

### 查看开放端口

netstat -an|find "61616"

### windows 服务

```bash
    # 不带参数的 net start 显示正在运行服务的列表
    net start
    # 启动服务
    net start wuauserv
    # 停止服务
    net stop wuauserv
```

### 删除目录

```bash
    rmdir  
    rmdir /s/q foo
    # /s 是代表删除所有子目录跟其中的档案。 
    # /q 是不要它在删除档案或目录时，不再问我 Yes or No 的动作。 
```

### netstat， windows 查端口

```bash
netstat -ano|findstr 8080
```

-a 显示所有连接和监听端口。

-b 显示包含于创建每个连接或监听端口的可执行组件。在某些情况下已知可执行组件拥有多个独立组件，并且在这些情况下包含于创建连接或监听端口的组件序列被显示。这种情况下，可执行组件名在底部的 [] 中，顶部是其调用的组件，等等，直到 TCP/IP 部分。注意此选项可能需要很长时间，如果没有足够权限可能失败。

-n 以数字形式显示地址和端口号。
-o 显示与每个连接相关的所属进程 ID。

<https://blog.csdn.net/hsd2012/article/details/50759017>

### windows  剪贴板进程

```bash
    rdpclip.exe
```

### hosts

```bash
C:\windows\System32\Drivers\Etc\hosts
```

### LTSC

Windows Server vNext Long-Term Servicing Channel (LTSC)

<https://technichero.com/download-windows-10-ltsc/>

<https://www.cybermania.ws/software/windows-10-enterprise-ltsc-2021-19044-1288/comment-page-1/>

<https://sysin.org/blog/windows-10-ltsc-2021/>

### 启动项

把bat脚本复制到以下目录

#### 系统级

```bash
    C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

#### 用户级

```bash
    Win+R
    输入: shell:startup
    系统自动打开以下目录
    C:\Users\user0\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

### windows凭据

```bash
    控制面板\用户帐户\凭据管理器 > windows凭据
```

### 域用户

windows设置>控制面板>更改账户类型>添加>
用户名: <域用户名>
域: <域>

### ipconfig

在Windows系统下IPconfig命令，后面带/release和 /renew参数可以实现从DHCP服务器重新获取IP地址:

#### ipconfig /release

释放当前网卡获取的IP地址，使用该命令后，网卡 (IPv4地址) 此时IP地址为空。

#### ipconfig /renew

为网卡重新从DHCP服务器上面获取新的IP地址。

### 解除防ping

<https://blog.csdn.net/wudinaniya/article/details/80956158>

### netstat

```bash
    netstat -ano -p UDP | find "0.0.0.0:53"
```

### tasklist

```bash
    tasklist | findstr <pid>
```

<https://blog.csdn.net/hongweigg/article/details/41517025>

### 清理c盘空间, windows清理硬盘空间, windows清理磁盘空间

#### 升级包

```bash
    # win11 没有这个目录
    rmdir C:\Windows\SoftwareDistribution.old
    # 停止正在运行的自动更新服务；, win11 没有...
    net stop wuauserv
    ren C:\Windows\SoftwareDistribution C:\Windows\SoftwareDistribution.bak
    net start wuauserv
```

#### 旧版本的系统

搜索> 磁盘清理(disk cleanup)> 清理系统文件

#### pagefile.sys

- win 10 虚拟内存
搜索高级系统设置> 高级> 性能> 设置> 性能选项> 高级>
- win 11 虚拟内存
搜索 性能选项> 高级> 虚拟内存> 更改> 重启

##### win 10

点击 此电脑，然后右键打开属性，然后高级系统设置。点击“高级”，然后点击 设置。再次点击“高级”，然后点击 更改。将默认勾选的“自动管理所有驱动器的分页文件大小”选项取消；

#### hiberfil.sys

```r
powercfg.exe /hibernate off
powercfg.exe /hibernate on
```

## win10 安全模式

开始-电源按钮，按住Shift同时点击“重启”，然后Win10会自动进入高级启动菜单，再点击疑难解答-高级选项-启动设置-重启。

## windows 命令行设置 IP

<https://www.ithome.com/0/143/741.htm>

## Windows Terminal

<https://github.com/microsoft/terminal>

Windows Terminal> Settings> Actions 可以设置快捷键,解决 vim  ctrl-v 的问题

## 查看本机域名以及登录账户使用的命令

```bash
whoami
```

## rmdir

```bash
# 删除非空目录
rmdir /s /q folder0
```

## winget

windows 的包管理工具

```bash
winget -v
winget search python
winget install Python.Python.3.11
```

## 性能

control panel> advanced system settings> advanced> settings> custom

### power mode

system> power & battery> power mode> best performance
