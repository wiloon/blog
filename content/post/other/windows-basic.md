---
title: windows basic, win basic
author: "-"
date: 2011-10-14T05:20:22+00:00
url: windows
categories:
  - windows
tags:
  - reprint
  - remix
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

[https://isofiles.bd581e55.workers.dev/](https://isofiles.bd581e55.workers.dev/)

## win10 应用开机启动, 启动项

打开运行 `win + r`, 输入 `shell:startup`, 将该应用的快捷方式从文件位置复制并粘贴到 “启动” 文件夹中。

### msdn i tell u

[https://www.itellu.com/2021/06/22/win11-v2021-v1/](https://www.itellu.com/2021/06/22/win11-v2021-v1/)

### windows iso

打开页面: [https://www.microsoft.com/zh-cn/software-download/windows10](https://www.microsoft.com/zh-cn/software-download/windows10)
点击 立即下载工具
运行 MediaCreationTool21H1.exe
选择 "为另一台电脑创建安装介质"

### uupdump

[https://uupdump.net/](https://uupdump.net/)

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

[https://blog.csdn.net/hsd2012/article/details/50759017](https://blog.csdn.net/hsd2012/article/details/50759017)

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

[https://technichero.com/download-windows-10-ltsc/](https://technichero.com/download-windows-10-ltsc/)

[https://www.cybermania.ws/software/windows-10-enterprise-ltsc-2021-19044-1288/comment-page-1/](https://www.cybermania.ws/software/windows-10-enterprise-ltsc-2021-19044-1288/comment-page-1/)

[https://sysin.org/blog/windows-10-ltsc-2021/](https://sysin.org/blog/windows-10-ltsc-2021/)

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

[https://blog.csdn.net/wudinaniya/article/details/80956158](https://blog.csdn.net/wudinaniya/article/details/80956158)

### netstat

```bash
    netstat -ano -p UDP | find "0.0.0.0:53"
```

### tasklist

```bash
    tasklist | findstr <pid>
```

[https://blog.csdn.net/hongweigg/article/details/41517025](https://blog.csdn.net/hongweigg/article/details/41517025)

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

[https://www.ithome.com/0/143/741.htm](https://www.ithome.com/0/143/741.htm)

## Windows Terminal

[https://github.com/microsoft/terminal](https://github.com/microsoft/terminal)

winget 搜不到最新版本, 目前看...只能去 github 下载, 然后解压就能用, 不需要安装

默认配置文件在 `C:\Users\user0\AppData\Local\Microsoft\Windows Terminal`

Windows Terminal> Settings> Actions 可以设置快捷键, 解决 vim  ctrl-v 的问题

- setting> rendering> use the new text renderer AtlasEngine, 打开字体渲染引擎
- 可以把常用的服务器添加到 自定义 profile 里
- profile 可以自定义图标, 不支持 SVG 格式
- 调整 profile 顺序貌似只能打开 json 配置文件修改.

### add archlinux@virtualbox into Windows terminal list

```json
{
    "commandline": "ssh wiloon@localhost",
    "guid": "{14fd428f-8203-4f45-b9d8-c70e02741cc9}",
    "hidden": false,
    "name": "Arch Linux"
}
```

## 查看本机域名以及登录账户使用的命令

```bash
whoami
```

## rmdir

```bash
# 删除非空目录
rmdir /s /q folder0
```

## winget, windows 的包管理工具

### 按名字查找包, winget search

```bash
winget search golang
```

winget search 输出

```bash
Name                    Id                          Version  Match       Source
-------------------------------------------------------------------------------
Go Programming Language GoLang.Go                   1.21.4   Tag: golang winget
```

### winget install

Need to run with administrator privileges

```bash
# Id: GoLang.Go
winget install GoLang.Go
```

### commands

```bash
winget -v
winget search python
winget install Python.Python.3.11
winget install Python.Python.3.6

# uninstall
winget uninstall OpenJS.NodeJS
```

## 性能

control panel> advanced system settings> advanced> settings> custom

### power mode

system> power & battery> power mode> best performance

## 设置环境变量, system env

在任务栏的 Search, 搜索: Edit the system environment variables  
    或者点击 windows> settings> 搜索 Edit the system environment variables  
    点击窗口最下方的按钮 "Environment Variables"  

## mklink

[https://blog.csdn.net/guyue35/article/details/49761347](https://blog.csdn.net/guyue35/article/details/49761347)

```bash
MKLINK [[/D] | [/H] | [/J]] Link Target
```

```bash
# 创建软链接
# /d 创建目录符号链接。默认为文件符号链接。
# Link(符号链接): C:\Users\ywang6\workspace 
# Target(已存在的目录, 源文件或目录): C:\workspace
# mklink 跟 linux 的 ln 命令参数相反
mklink /d C:\Users\ywang6\workspace C:\workspace
```

## dir

```Bash
# the /B option says to only show the file names
dir /B
```

## scoop

```Bash
# non-admin PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
iwr -useb get.scoop.sh | iex
scoop install main/gradle-bin
```

## 输入法快捷键

Settings> Time & language> Typing> Advanced keyboard settings> Input language hot keys

## PowerToys disable win + space

1. install power toys "Per user - x64"
2. go to keyboard manager> shortcuts> Select> click "Select" button then press win + space
3. To send: keep key/shortcut
4. select "Disable" in the second drop box

## windows dev env

- winget 安装软件不知道会安装到哪
- winget 需要 admin cmd, 但是 run as admin 经常报错, 几乎用不了.
- cmd 没有 shell 好用, 也许 powershell 会更好用, 但是需要学习一下
  - 复制到 cmd里的字符串过长会折行显示,但是其实并不在同一行, 从最后一行开始删除只能删到行首, 不能删到上面一行.
- curl 在 windows 下不正常
  - powershell 里 curl --version 执行不了
  - cmd里能执行 curl --version
  - 同样的 curl 命令, linux能执行 windows里执行不了, 有可能是因为命令参数是多行的. curl用最新版本,命令 改成一行也不行.. 神奇
- 全局查找文件, 在资源管理器里搜索之后点击打开文件所在位置然后返回, 已经搜到的文件都 不见了, 得重新搜
- Command Prompt's character escaping rules are both archaic and awful.  https://superuser.com/questions/1016710/how-to-make-a-curl-post-call-in-windows 
- 让 curl 命令在 windows 下正常运行需要花太多精力...
- 用 golang 写 Api 的测试, 有时候要执行 Shell 命令, 比如 执行 `nft add rule table0 chain0 tcp sport 1025 drop` 去 禁用掉邮件服务的连接, 测试重发, 不是说不能在 win 里做, 如果在 win 里做的话就要再学习一下 windows 有没有类似 iptables, nftables 之类的工具, 假设找到了也研究出来怎么用了, 这些知识也只能适用于 windows, 如果开发环境在 linux 里, 就可以去研究 iptables, nftabls, 在解决生产环境的问题的时候, 这些知识也是可以用到的.

## 在 windows 里重启然后进入 BIOS

1. settings
2. Recovery
3. Advanced startup> Restart now
4. Restart now
5. 在显示 lenovo logo 的屏幕, 不需要按提示按 Enter
6. Choose an option> Troubleshoot
7. advanced options
8. UEFI Firmware Settings
9. Restart
