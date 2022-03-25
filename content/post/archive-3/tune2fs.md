---
title: tune2fs
author: "-"
date: 2020-01-12T06:51:40+00:00
url: /?p=15348
categories:
  - Uncategorized

tags:
  - reprint
---
## tune2fs
tune2fs命令

一.简介: 

tune2fs用来调整和查看ext2/ext3 (现在有ext4了) 文件系统的文件系统参数，Windows平台如果出现意外断电死机情况，下次开机一般都会出现系统自检。Linux系统当然也有文件系统自检，而且是可以通过tune2fs命令，自行定义自检周期及方式。

二.用法: 

自己去man吧，man man，更健康。。。

常用选项说明: 
  
-l 查看文件系统信息
  
-c max-mount-counts 设置强制自检的挂载次数，如果开启，每挂载一次mount conut就会加1，超过次数就会强制自检
  
-i interval-between-checks[d|m|w] 设置强制自检的时间间隔[d天m月w周]
  
-m reserved-blocks-percentage 保留块的百分比
  
-j 将ext2文件系统转换为ext3类型的文件系统
  
-L volume-label 类似e2label的功能，可以修改文件系统的标签
  
-r reserved-blocks-count 调整系统保留空间
  
-o [^]mount-option[,...] Set or clear the indicated default mount options in the filesystem. 设置或清除默认挂载的文件系统选项 (这一条是我需要的。) 

三.例如: 

tune2fs -c 30 /dev/hda1 设置强制检查前文件系统可以挂载的次数
  
tune2fs -c -l /dev/hda1 关闭强制检查挂载次数限制。 #有些分区本身默认就是-1，也就是不检测
  
tune2fs -i 10 /dev/hda1 10天后检查
  
tune2fs -i 1d /dev/hda1 1天后检查
  
tune2fs -i 3w /dev/hda1 3周后检查
  
tune2fs -i 6m /dev/hda1 半年后检查
  
tune2fs -i 0 /dev/hda1 禁用时间检查

tune2fs -j /dev/hda1 添加日志功能，将ext2转换成ext3文件系统

tune2fs -r 40000 /dev/hda1 调整/dev/hda1分区的保留空间为40000个磁盘块

tune2fs -o acl,user_xattr /dev/hda1 设置/dev/hda1挂载选项，启用Posix Access Control Lists和用户指定的扩展属性
  
https://www.cnblogs.com/yaobai609/archive/2012/11/21/2781292.html