---
title: archlinux 64位上运行32位程序
author: "-"
date: 2015-05-29T23:55:49+00:00
url: /?p=7728
categories:
  - Uncategorized
tags:
  - Arch Linux

---
## archlinux 64位上运行32位程序

<http://blog.csdn.net/cnsword/article/details/7447670>

archlinux纯64位版是没有办法直接运行32位程序的。因为缺少最主要的glibc的32位版本的支持。

要想使archlinux64支持32位程序,只需要将32位的源添加进来就可以。

/etc/pacman.conf中增加

print?
  
[multilib]
  
Include = /etc/pacman.d/mirrorlist

如果是chakra需要将repo的名称修改为lib32和lib32-test

print?
  
[lib32]
  
Include = /etc/pacman.d/mirrorlist
  
这样

这样通过pacman安装lib32-glibc库就能提供基本的32位支持了,如果需要32位桌面环境库,安装lib32-gtk或者lib-kde就可以了。看出规律来了吧,这些库的前缀都是lib32-。下一步就可以自由的使用了。
