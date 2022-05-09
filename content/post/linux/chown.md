---
title: chown 更改文件拥有者
author: "-"
date: 2011-12-03T09:34:13+00:00
url: /?p=1705
categories:
  - Linux
tags:
  - reprint
---
## chown 更改文件拥有者

如何更改一个文件的拥有者呢？很简单。既然改变用户组是change group，那么改变拥有者就是change owner (改变拥有者) ，这就是chown这个命令的用途。要注意的是，用户必须是已经在系统中，也就是在/etc/passwd这个文件中有记录的用户名称才可以更改。
  
chown的用途很多，还可以直接修改用户组的名称。如果要将目录下的所有子目录或文件同时更改文件拥有者的话，直接加上-R的参数即可。下面我们来看看语法与范例。

```bash
chown [-R] 账户名称 文件或目录
chown [-R] 账户名称:用户组名称 文件或目录
```

参数: -R : 进行递归的持续更改，即将同子目录下的所有文件、目录都更新问这个用户组。通常用在更改某一目录的情况。
  
范例:

```bash
chown  root:root  install.log

# 按UID改owner
chown -R 200:200 /root/foo
```

我们知道如何改变文件的用户组与拥有者了，那么什么时候要使用chown或chgrp呢？或许你你会觉得奇怪，但是，确实有时候需要更改文件的拥有者。最常见的例子就是将文件复制给其他人，我们使用最简单的cp来进行说明:

[root@linux ~]#cp 源文件 目的文件 假设今天要讲.bashrc文件复制成为.bashrc_test，并给bin这个人，您可以这样做:

[root@linux ~]# cp .bashrc .bashrc_test
  
[root@linux ~]#ls –al .bashrc*
  
-rw-r-r- 1 root root 24343 Jun 23 08:33 .bashrc
  
-rw-r-r- 1 root root 24343 Jun 23 08:33 .bashrc_test 怎么办？.bashrc_test还是属于root所有，即使将文件拿给bin用户了，他仍然无法修改，所以必须修改这个文件的拥有者与用户组
