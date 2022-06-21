---
title: nfs
author: "-"
date: 2018-12-16T08:36:59+00:00
url: nfs
categories:
  - Linux
tags:
  - reprint
---
## nfs

```bash
# nfs-utils 包含客户端和服务端实现
sudo pacman -S  nfs-utils

# ubuntu, nfs client
sudo apt install nfs-common
```

### nfs 依赖时钟, 需要ntp服务

<https://blog.wiloon.com/?p=10869>

```bash
mkdir -p /data/nfs/tmp /mnt/nfs/tmp
mount --bind /mnt/nfs/tmp /data/nfs/tmp

vim /etc/fstab
/mnt/nfs/tmp /data/nfs/tmp  none   bind   0   0

vim /etc/exports
/data/nfs       192.168.100.0/24(rw,async,crossmnt,fsid=0)
/data/nfs/tmp   192.168.100.0/24(rw,sync)

# 使export 生效
exportfs -rav

# 查看 export dir
exportfs -v

sudo systemctl restart nfs-server
sudo systemctl enable nfs-server
```

## client

### linux client

```bash
showmount -e servername
mount server:/ /mountpoint/on/client
```

### windows client

```bash
# 挂载之前先改注册表
需要读写权限的需要修改注册表
通过修改注册表将windows访问NFS时的UID和GID改成0即可,步骤如下
1. 在运行中输入regedit,打开注册表编辑器；
2. 进入HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default条目；
3. Create two DWORD values namely AnonymousUid and AnonymousGid,十进制值跟nfs服务端文件 所属用户 的用户 id一致。

# 重启windows的NFS client service
C:\Windows\system32>hostname
DESKTOP-AE0D2H0
C:\Windows\System32>nfsadmin client DESKTOP-AE0D2H0 config casesensitive=yes
The settings were successfully updated.
C:\Windows\system32>nfsadmin client DESKTOP-AE0D2H0 stop
The service was stopped successfully.
C:\Windows\system32>nfsadmin client DESKTOP-AE0D2H0 start
The service was started successfully.
C:\Windows\system32>

#win10 mount nfs
打开控制面板 > 程序 > 启用或关闭 Windows 功能,找到NFS服务打开子目录勾选NFS客户端与管理工具。
showmount -e [server]    显示 NFS 服务器导出的所有共享。
showmount -a [server]    列出客户端主机名或 IP 地址,以及使用"主机:目录"格式显示的安装目录。
showmount -d [server]    显示 NFS 服务器上当前由某些 NFS 客户端安装的目录。

# 挂载nfs
mount -o anon \\192.168.50.220\data\nfs\data Z:\

#卸载
umount z:

```

<https://wiki.archlinux.org/index.php/NFS#Installation>
  
<https://blogs.msdn.microsoft.com/sfu/2009/03/27/can-i-set-up-user-name-mapping-in-windows-vista/>

NFS on CentOS 7 & Windows 10 NFS Client Configuration
  
<https://dovidenko.com/2017/505/nfs-centos-7-windows-10-network-shares.html/embed#?secret=DYEnZkJ5i8>

## 其他选项

- secure：限制客户端只能从小于1024的TCP/IP端口连接NFS服务器（默认设置）。
- insecure：允许客户端从大于1024的TCP/IP端口连接NFS服务器。
- sync：将数据同步写入内存缓冲区与磁盘中，虽然这样做效率较低，但可以保证数据的一致性。
- async：将数据先保存在内存缓冲区中，必要时才写入磁盘。
- wdelay：检查是否有相关的写操作，如果有则将这些写操作一起执行，这样可提高效率（默认设置）。
- no_wdelay：若有写操作则立即执行，应与sync配合使用。
- subtree_check：所输出目录是一个子目录，则NFS服务器将检查其父目录的权限（默认设置）。
- no_subtree_check：即使输出目录是一个子目录，NFS服务器也不检查其父目录的权限，这样做可以提高效率。

<https://www.cnblogs.com/nufangrensheng/p/3486839.html>
