---
title: samba
author: "-"
date: 2012-02-13T11:45:25+00:00
url: samba
categories:
  - Linux
tags:
  - reprint
  - storage
---
## samba

```bash
# archlinux 安装 samba
sudo pacman -S samba

# centos install samba
sudo yum install samba samba-client

```

```bash
#创建共享目录
sudo mkdir /home/user0/share

# 创建 samba 用户，使用已有用户的话，可以跳过,pdbedit是samba的用户管理命令
sudo useradd -m -s /bin/bash user0
sudo pdbedit -a user0
# set password for user，设置密码，使用系统现有的用户时，也要设置密码，samba可以跟linux系统共享用户名，但是密码是独立的。
smbpasswd -a user0
# list user
sudo pdbedit -L -v
sudo systemctl start smb
sudo systemctl enable smb
sudo systemctl status smb
```

### 创建Samba配置文件

```bash
vim /etc/samba/smb.conf

[global]
workgroup = WORKGROUP
security = user

# share0: the share folder display name
[share0]
path = /home/user0/share
valid users = user0
public = no
writable = yes
printable = no
create mask = 0644
```

### 客户端

file share url: \\hostname0\share0

```bash
mount -t cifs //SERVER/sharename /mnt/mountpoint -o username=username,password=password,iocharset=utf8,vers=3.1.1
```

<https://linuxize.com/post/how-to-install-and-configure-samba-on-centos-7/>

[[nfs]]
