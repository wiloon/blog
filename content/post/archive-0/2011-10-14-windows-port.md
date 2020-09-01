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
    rmdir C:\Windows\SoftwareDistribution.old
    net stop wuauserv
    ren C:\Windows\SoftwareDistribution C:\Windows\SoftwareDistribution.old
    net start wuauserv
    

