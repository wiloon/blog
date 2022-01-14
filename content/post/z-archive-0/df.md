---
title: df
author: "-"
date: 2011-10-16T10:39:32+00:00
url: df
categories:
  - Linux

---
## df

df 是来自于coreutils 软件包，系统安装时，就自带的；我们通过这个命令可以查看磁盘的使用情况以及文件系统被挂载的位置；

举例: 

[root@localhost beinan]# df -lh
Filesystem            容量  已用 可用 已用% 挂载点
/dev/hda8              11G  6.0G  4.4G  58% /
/dev/shm              236M     0  236M   0% /dev/shm
/dev/sda1              56G   22G   35G  39% /mnt/sda1

我们从中可以看到,系统安装在/dev/hda8 ；还有一个56G的磁盘分区/dev/sda1挂载在 /mnt/sda1中；

其它的参数请参考 man df