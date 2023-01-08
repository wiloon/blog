---
title: scp
author: "-"
date: 2023-01-08 12:33:41
url: scp
categories:
  - Linux
tags:
  - Shell
  - reprint
  - remix
---
## scp

scp 可以在两个 linux 主机间复制文件；

```bash
# 复制目录 -r
scp -r local_folder remote_username@remote_ip:remote_folder
```

## ash: /usr/libexec/sftp-server: not found

This is a consequence of your client machine using a very recent OpenSSH release (9.0 - check <https://www.openssh.com/txt/release-9.0> 62 for more info), which changes the scp program to use the SFTP protocol under the hood, which vanilla OpenWrt/dropbear installations do not support. To work around the problem on the client side, use the new -O (that is an uppercase letter "o") switch when invoking scp, which will cause it to fall back to the legacy behavior.

<https://forum.openwrt.org/t/ash-usr-libexec-sftp-server-not-found-when-using-scp/125772/2>

```bash
scp -O /path/to/foo root@192.168.50.4:~

```

## 在 a 主机上执行命令,把文件 从 b 主机复制到 c 主机

```bash
scp root@10.1.0.2:/testdir/ssh/test root@10.1.0.3:/testdir/ssh/
```

```bash
# 命令格式: 
scp [可选参数] file_source file_target
scp -i identity_file
scp -i mykey.pem somefile.txt root@ec2-184-73-72-150.compute-1.amazonaws.com:/home/user/xxx
# -i 指定证书
```

### 参数

```r
-P 指定端口, 注意是大写的 P, 小写的 -p 已经被 rcp 使用
-v 和大多数 linux 命令中的 -v 意思一样 , 用来显示进度 . 可以用来查看连接 , 认证 , 或是配置错误
-C 使能压缩选项
-4 强行使用 IPV4 地址 .
-6 强行使用 IPV6 地址 .
-r  Recursively copy entire directories.
```

## 从 本地 复制到 远程

```bash
scp local_file remote_username@remote_ip:remote_folder

# 或者
scp local_file remote_username@remote_ip:remote_file
# 或者
scp local_file remote_ip:remote_folder
# 或者
scp local_file remote_ip:remote_file
```

第1,2个指定了用户名，命令执行后需要再输入密码，第1个仅指定了远程的目录，文件名字不变，第2个指定了文件名；

第3,4个没有指定用户名，命令执行后需要输入用户名和密码，第3个仅指定了远程的目录，文件名字不变，第4个指定了文件名；

* 例子:

scp /home/space/music/1.mp3 root@www.cumt.edu.cn:/home/root/others/music

scp /home/space/music/1.mp3 root@www.cumt.edu.cn:/home/root/others/music/001.mp3

scp /home/space/music/1.mp3 www.cumt.edu.cn:/home/root/others/music

scp /home/space/music/1.mp3 www.cumt.edu.cn:/home/root/others/music/001.mp3
