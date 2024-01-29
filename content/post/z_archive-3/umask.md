---
title: umask
author: "-"
date: 2020-03-15T14:43:43+00:00
url: /?p=15761
categories:
  - Inbox
tags:
  - reprint
---
## umask
umask 值用于设置用户在创建文件时的默认权限，当我们在系统中创建目录或文件时，目录或文件所具有的默认权限就是由umask值决定的。

对于root用户，系统默认的umask值是0022；对于普通用户，系统默认的umask值是0002。执行umask命令可以查看当前用户的umask值。

    umask
    > 0022

umask值一共有4组数字，其中第1组数字用于定义特殊权限，我们一般不予考虑，与一般权限有关的是后3组数字。

https://www.cnblogs.com/wish123/p/7073114.html