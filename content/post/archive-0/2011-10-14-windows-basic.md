---
title: windows basic
author: wiloon
type: post
date: 2011-10-14T05:20:22+00:00
url: /?p=1040
---
### 查看开放端口
netstat -an|find "61616"

### windows 服务
    # 不带参数的 net start 显示正在运行服务的列表
    net start
    # 启动服务
    net start wuauserv
    # 停止服务
    net stop wuauserv

### 删除目录
    rmdir  
    rmdir /s/q foo
    # /s 是代表删除所有子目录跟其中的档案。 
    # /q 是不要它在删除档案或目录时，不再问我 Yes or No 的动作。 

### 清理c盘空间
#### 升级包
    rmdir C:\Windows\SoftwareDistribution.old
    net stop wuauserv
    ren C:\Windows\SoftwareDistribution C:\Windows\SoftwareDistribution.old
    net start wuauserv
#### 旧版本的系统
    搜索>磁盘清理》清理系统文件
### netstat
```bash
netstat -ano|findstr 8080
```

-a 显示所有连接和监听端口。

-b 显示包含于创建每个连接或监听端口的可执行组件。在某些情况下已知可执行组件拥有多个独立组件，并且在这些情况下包含于创建连接或监听端口的组件序列被显示。这种情况下，可执行组件名在底部的 [] 中，顶部是其调用的组件，等等，直到 TCP/IP 部分。注意此选项可能需要很长时间，如果没有足够权限可能失败。

-n 以数字形式显示地址和端口号。

-o 显示与每个连接相关的所属进程 ID。


### windows  剪贴板进程
    rdpclip.exe

### hosts
    C:\windows\System32\Drivers\Etc\hosts

### LTSC
Windows Server vNext Long-Term Servicing Channel (LTSC)

### 启动项
    C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp