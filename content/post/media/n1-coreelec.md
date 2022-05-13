---
author: "-"
date: "2020-09-11 00:50:45" 
title: "n1 coreelec"
categories:
  - inbox
tags:
  - reprint
---
## "n1 coreelec"
从官网下载最新版本的coreelec, CoreELEC-Amlogic.arm-9.2.4.2-Generic.img.gz
    https://coreelec.org/
用7z 解压 CoreELEC-Amlogic.arm-9.2.4.2-Generic.img.gz， 得到 CoreELEC-Amlogic.arm-9.2.4.2-Generic.img

用Win32DiskImager.exe将CoreELEC-Amlogic.arm-9.2.4.2-Generic.img写入U盘
替换文件
运行N1降级工具，选择3 进入线刷模式   
在提示插入usb线时，插入u盘 ， 进入 U盘上的 coreelec系统， 
开启ssh支持
ssh 登录 coreelec, 执行以下命令将coreelec写入emmc
     /flash/installtoemmc  