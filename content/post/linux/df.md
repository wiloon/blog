---
title: df
author: "-"
date: 2011-10-16T10:39:32+00:00
url: df
categories:
  - Linux
tags:
  - reprint
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


## df command

disk free 的缩写;用于显示目前Linux系统上的文件系统的磁盘使用情况统计, df 是用 superblock 的信息统计磁盘占用的.

```bash
df -h
df -t ext4 -h
# 查看文件系统类型
df -T -h

# inode 使用统计
df -i

```

df命令可以获取硬盘被占用了多少空间, 目前还剩下多少空间等信息, 它也可以显示所有文件系统对i节点和磁盘块的使用情况。

## df选项

    -T: 显示文件系统类型。
    -a: 显示所有文件系统的磁盘使用情况,包括0块 (block) 的文件系统,如/proc文件系统。
    -k: 以k字节为单位显示。
    -i: 查看 inode 信息, 而不是磁盘块。
    -t: 显示各指定类型的文件系统的磁盘空间使用情况。
    -x: 列出不是某一指定类型文件系统的磁盘空间使用情况 (与t选项相反) 。
    -i, --inodes 列出 inode 资讯，不列出已使用 block
    

  
我们先看看使用df命令的例子: 

//列出各文件系统的磁盘空间使用情况
  
#df
  
Filesystem 1k-blocks Used Available Use% Mounted on
  
/dev/hda5 381139 332921 28540 93% /
  
/dev/hda1 46636 6871 37357 16% /boot
  
/dev/hda3 10041144 6632528 2898556 70% /home
  
none 127372 0 127372 0% /dev/shm
  
/dev/hda2 27474876 24130460 1948772 93% /usr
  
/dev/hda6 256667 232729 10686 96% /var
  
第1列是代表文件系统对应的设备文件的路径名 (一般是硬盘上的分区) ；第2列给出分区包含的数据块 (1024字节) 的数目；第3,4列分别表示已用的和可用的数据块数目。

◆用户也许会感到奇怪,第3,4列块数之和不等于第2列中的块数。这是因为默认的每个分区都留了少量空间供系统管理员使用的缘故。即使遇到普通用户空间已满的情况,管理员仍能登录和留有解决问题所需的工作空间。清单中Use%列表示普通用户空间使用的百分比,若这一数字达到100%,分区仍然留有系统管理员使用的空间。

最后,Mounted on列表示文件系统的安装点。

//列出各文件系统的i节点使用情况。
  
#df -ia
  
Filesystem Inodes IUsed IFree IUse% Mounted on
  
/dev/hda5 98392 23919 74473 25% /
  
none 0 0 0 - /proc
  
/dev/hda1 12048 38 12010 1% /boot
  
none 0 0 0 - /dev/pts
  
/dev/hda3 1275456 355008 920448 28% /home
  
none 31843 1 31842 1% /dev/shm
  
/dev/hda2 3489792 133637 3356155 4% /usr
  
/dev/hda6 66264 9876 56388 15% /var

//列出文件系统的类型。
  
#df -T
  
Filesystem Type 1k-blocks Used Available Use% Mounted on
  
/dev/hda5 ext3 381139 332921 28540 93% /
  
/dev/hda1 ext3 46636 6871 37357 16% /boot
  
/dev/hda3 ext3 10041144 6632528 2898556 70% /home
  
none tmpfs 127372 0 127372 0% /dev/shm
  
/dev/hda2 ext3 27474876 24130460 1948772 93% /usr
  
/dev/hda6 ext3 256667 232729 10686 96% /var2

http://os.51cto.com/art/201012/240726_all.htm

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
