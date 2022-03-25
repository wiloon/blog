---
title: raspberry pi nfs server
author: "-"
date: 2019-01-19T11:06:36+00:00
url: /?p=13430
categories:
  - Uncategorized

tags:
  - reprint
---
## raspberry pi nfs server
```bash
#安装 NFS 服务器
sudo apt install nfs-kernel-server

vim /etc/exports
# 添加如下内容以允许所有可以访问 NAS 云盘的设备挂载存储: 
/nas/data *(rw,sync,no_subtree_check)

# restart nfs server
systemctl restart  nfs-kernel-server

# 在另一台linux 上挂载
sudo mkdir /nas/data
sudo mount -t nfs <raspberry-pi-hostname-or-ip>:/nas/data /nas/data
```

### autofs

```bash
pacman -S autofs
pacman -S nfs-utils
sudo systemctl start rpcbind
sudo systemctl enable rpcbind

sudo vim /etc/autofs/auto.master
/nas   /etc/autofs/auto.pi3bp --timeout 61

sudo vim /etc/autofs/auto.pi3bp
data  -rw,soft,intr,rsize=8192,wsize=8192 pi3bp:/nas/data

sudo systemctl start autofs
sudo systemctl enable autofs

# 共享目录权限问题, 在服务端安装 acl
sudo apt-get install acl
setfacl -R -m u:1000:rwx /nas/data

```

共享目录权限问题
  
默认情况下,root用户被映射成nfsnobody用户,对于客户端机器上和NFS服务器上UID相同的用户会对应映射,其它非root用户被映射成nobody用户。当root用户访问共享目录时是以nfsnobody用户访问共享目录的,这时客户端用户无法正常读写文件,如果要让客户端用户具有读写权限,需要做如下操作: 

在nfs服务端,对共享目录添加facl文件权限给与客户端要执行读写操作的用户一样的UID文件权限；如下: 
  
客户端用户 yufu 要对 服务端的 /dai 共享目录具有读写权限,那么: 查看yufu 的uid 执行 :  id yufu  (查看uid为1000) 

到nfs服务端,给 /dai 目录添加facl文件权限给这个用户ID执行如下操作: 
   
setfacl -R -m u:1000:rwx /dai

https://github.com/dnschneid/crouton/wiki/How-to-mount-network-shares-on-Chromebook-(sshfs,-cifs,-nfs-etc)

https://wiki.archlinux.org/index.php/NFS#Mount_using_autofs
  
https://wiki.archlinux.org/index.php/Autofs#Configuration


  
    NFS文件共享权限问题与autofs的自动挂载等
  



  
https://mp.weixin.qq.com/s?__biz=MjM5NjQ4MjYwMQ==&mid=2664612263&idx=1&sn=d4a4ca2b1bf2692debb3db5cd65f1d17&chksm=bdcefae18ab973f75335ed34dd8ecd8ad411dc004db0ef7d8053e503e8b71326c30a4f696d44&scene=0&subscene=131&ascene=7&devicetype=android-26&version=26070333&nettype=WIFI&abtest_cookie=AwABAAoACwATAAMAJZceAFmZHgBgmR4AAAA%3D&lang=zh_CN&pass_ticket=ImdQ85AP2YJJffE%2BSgUyrxOrtw39rlqAByjKnj6v4bE%3D&wx_header=1