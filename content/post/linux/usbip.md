---
author: "-"
date: "2021-04-29 15:35:36" 
title: "usbip"
categories:
  - inbox
tags:
  - reprint
---
## "usbip"

### 下载usbip-win
<https://github.com/cezanne/usbip-win/releases>

### 解压到一个目录

    D:\workspace\apps\usbip-win-0.3.4

### 安装证书

右键usbip_test.pfx -> 安装PFX，选择"本地计算机"，而不是"当前用户"，证书密码 usbip，存储位置选择 "受信任的证书颁发机构"  

开启驱动测试签名
bcdedit.exe /set TESTSIGNING ON

重启系统

找到要使用的USB设备
.\usbip.exe list -l

### 安装USB驱动

.\usbip.exe install

### 启动服务端

     .\usbipd.exe -d -4

### WSL2客户端, 编译内核

# 安装工具包

   sudo apt install build-essential flex bison libssl-dev libelf-dev

### 下载内核

    https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/

---

<https://yadom.in/archives/usb-passthrough-hyper-v-and-wsl2.html>  
<https://snowstar.org/2020/06/14/wsl2-usb-via-usbip/>  
<https://github.com/microsoft/WSL2-Linux-Kernel>  
