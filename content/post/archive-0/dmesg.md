---
title: dmesg
author: "-"
type: post
date: 2011-08-20T19:58:44+00:00
url: /?p=466
bot_views:
  - 5
categories:
  - Linux

---
Linux命令dmesg用来显示开机信息，kernel会将开机信息存储在 ring buffer 中。您若是开机时来不及查看信息，可利用dmesg来查看。开机信息亦保存在/var/log目录中，名称为dmesg的文件里。
  
dmesg[1] - print or control the kernel ring buffer
  
dmesg用于检测和控制内核环缓冲。程序用来帮助用户了解系统的启动信息
  
```bash
  
dmesg |grep scsi -A 3
  
```