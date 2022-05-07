---
title: 'linux  查看用户的UID和GID'
author: "-"
date: 2019-07-07T10:08:04+00:00
url: /?p=14645
categories:
  - Inbox
tags:
  - reprint
---
## 'linux  查看用户的UID和GID'
方法一: 使用 id 命令

使用 id 命令可以很轻松的通过用户名查看UID、GID，下面来讲解一下这个命令的用法。

命令格式

 
  
id [选项]... [用户名]
  
命令选项
  
-a 忽略，兼容其它版本
  
-Z, –context 只输出当前用户的安全上下文
  
-g, –group 只输出有效的GID
  
-G, –groups 输出所有的GID
  
-n, –name 对于 -ugG 输出名字而不是数值
  
-r, –real 对于 -ugG 输出真实ID而不是有效ID
  
-u, –user 只输出有效UID
  
–help 输出帮助后退出
  
–version 输出版本信息后退出
  
使用案例

 
  
heihaier@heihaier-desktop:~$ id root
  
uid=0(root) gid=0(root) groups=0(root)
  
方法二: 查看 /etc/password 文件
  
/etc/password 文件格式
  
 
  
root:x:0:0:root:/root:/bin/bash

上面是这个文件的一行实例，每个域用 : 区分，从左向右分别是
  
root 用户名: 1~32 字节长。
  
x 密码: 字符x表示密码被加密保存在 /etc/shadow 文件中。
  
0 用户ID(UID): 每个用户必需指定UID。UID 0 是保留给 root 用户的。UID 1~99是保留给其它预定义用户的。 UID 100~999是保留给系统用户的。
  
0 组ID(GID): 主组ID (保存在 /etc/group 文件中) 。
  
root 用户ID信息: 用户备注信息。
  
/root 主目录: 用户主目录。
  
/bin/bash 命令解释器(Shell): 用户默认的命令解释器的路径。
  
使用案例
  
 
  
heihaier@heihaier-desktop:~$ sudo cat /etc/passwd | grep root
  
root:x:0:0:root:/root:/bin/bash

https://blog.csdn.net/sinat_31500569/article/details/69943903