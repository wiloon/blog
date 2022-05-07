---
title: adb command
author: "-"
date: 2014-08-07T02:40:16+00:00
url: /?p=6899
categories:
  - Inbox
tags:
  - reprint
---
## adb command
在手机上打开USB调试

```bash
adb help
adb kill-server
sudo adb start-server
adb devices

#这个命令将登录设备的shell
adb shell

# adb push <本地路径> <远程路径>
adb push <本地路径> <远程路径>
```

查看设备 –查看当前连接的设备, 连接到计算机的android设备或者模拟器将会列出显示

adb reboot bootloader

adb pull Copies a specified file from an emulator/device instance to your development computer.

从电脑上发送文件到设备 –用push命令可以把本机电脑上的文件或者文件夹复制到设备(手机)
  
adb push Copies a specified file from your development computer to an emulator/device instance.
  
sudo adb push SuperSU-v2.82-201705271822.zip /storage/emulated/0

ADB是android sdk里的一个工具, 它的主要功能有:

运行设备的shell(命令行)
  
管理模拟器或设备的端口映射
  
计算机和设备之间上传/下载文件
  
将本地apk软件安装至模拟器或android设备
  
ADB是一个 客户端-服务器端 程序, 其中客户端是你用来操作的电脑, 服务器端是android设备.

先说安装方法, 电脑上需要安装客户端. 客户端包含在sdk里. 设备上不需要安装, 只需要在手机上打开选项settings-applications-development-USB debugging.

对于Mac和Linux用户, 下载好的sdk解压后, 可以放~或者任意目录. 然后修改~/.bash_profile文件, 设置运行环境指向sdk的tools目录.
  
具体是打开~/.bash_profile文件(如果没有此文件也可以自行添加), 在里面加入一行:

export PATH=${PATH}:<你的sdk目录>/tools

然后就可以使用adb命令了.

对于windows xp用户, 需要先安装usb驱动, 然后如果你只打算使用adb而不想下载整个sdk的话, 可以下载这个单独的adb工具包 下载后解压, 把里面 adb.exe 和 AdbWinApi.dll 几个文件放到系统盘的 windows/system32 文件夹里就可以了.

现在说下ADB常用的几个命令


  
    安装软件 –将指定的apk文件安装到设备上
  


adb install 
  
3. 卸载软件

adb uninstall <软件名>
  
adb uninstall -k <软件名> 如果加 -k 参数,为卸载软件但是保留配置和缓存文件.
  
4. 登录设备shell

adb shell <command命令> 后面加<command命令>将是直接运行设备命令, 相当于执行远程命令

adb remount ## remount '/system'分区 as read-write
  
6. 从设备上下载文件到电脑 –用pull命令可以把设备(手机)上的文件或者文件夹复制到本机电脑

adb pull <远程路径> <本地路径>
  
7. 显示帮助信息(包括各种命令用法与含义) —