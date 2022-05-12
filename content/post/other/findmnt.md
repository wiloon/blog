---
title: findmnt, 查找已挂载的文件系统
author: "-"
date: 2014-08-13T08:28:06+00:00
url: findmnt
categories:
  - Linux
tags:
  - reprint
---
## findmnt, 查找已挂载的文件系统

无任何选项运行 findmnt，会以树形结构图的方式列出所有已挂载的文件系统。

Findmnt 可以用“-D”或“-df”选项创建一个 df 格式的输出报告空闲和已用磁盘空间。
使用“-s”或“-fstab”选项，findmnt 将只从/etc/fstab文件和/etc/fstab.d目录读取文件系统。

Findmnt 可以打印出只基于类型的特定的文件系统，例如 ext4，多个系统类型可以指定一个逗号分隔。
