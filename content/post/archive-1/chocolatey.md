---
title: Chocolatey, choco, Windows 软件包管理系统
author: "-"
date: 2015-09-24T00:07:48+00:00
url: /?p=8340
categories:
  - Uncategorized

tags:
  - reprint
---
## Chocolatey, choco, Windows 软件包管理系统

Chocolatey 是 windows 下一款命令行包管理软件 ，简单说这就是 Windows 的 apt-get。习惯 Linux 操作方式并非常想用它操纵 Windows 的敬请折腾。Chocolatey 这套包管理系统目前已经包含了近 500 多款常用软件。

### 安装Chocolatey

https://chocolatey.org/install
  
以管理员权限打开powershell执行以下命令

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

设置环境变量参数 ChocolateyInstall  (当然是要对应一个路径/文件夹) 
手动创建刚才设置的ChocolateyInstall变量所对应的文件夹

    ChocolateyInstall=D:\ChocolateyInstall

### 用choco安装其它软件
查询程序是否在数据库中: clist < 程序名>
安装程序: cinst < 程序名>
  
choco install keepassxc

```bash
# 以管理员身份启动power shell,windows terminal
choco install keepassxc
choco upgrade keepassxc
choco upgrade all
choco search
choco uninstall
choco list -l
choco list -local-only
```

### 设置安装目录，环境变量

ChocolateyInstall
http://www.oschina.net/p/chocolatey
  
https://chocolatey.org/packages