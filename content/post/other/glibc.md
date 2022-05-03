---
title: glibc
author: "-"
date: 2011-10-26T14:25:39+00:00
url: glibc
categories:
  - Linux

tags:
  - reprint
  - c


---
## glibc

glibc 是非常底层的系统库，千万不要自己手动更新，网上有很多教训。

glibc是linux下面c标准库的实现，即GNU C Library。glibc本身是GNU旗下的C标准库，后来逐渐成为了Linux的标准c库，而Linux下原来的标准c库Linux libc逐渐不再被维护。Linux下面的标准c库不仅有这一个，如uclibc、klibc，以及上面被提到的Linux libc，但是glibc无疑是用得最多的。glibc在/lib目录下的.so文件为libc.so.6。

glib
glib是GTK+的基础库，它由基础类型、对核心应用的支持、实用功能、数据类型和对象系统五个部分组成，可以在[<http://www.gtk.org> gtk网站]下载其源代码。是一个综合用途的实用的轻量级的C程序库，它提供C语言的常用的数据结构的定义、相关的处理函数，有趣而实用的宏，可移植的封装和一些运行时机能，如事件循环、线程、动态调用、对象系统等的API。GTK+是可移植的，当然glib也是可移植的，你可以在linux下，也可以在windows下使用它。使用gLib2.0 (glib的2.0版本) 编写的应用程序，在编译时应该在编译命令中加入pkg-config --cflags --libs glib-2.0，如:

gcc pkg-config --cflags --libs glib-2.0 hello.c -o hello
使用glib最有名的就是GNOME了。

eglibc
eglic是二进制兼容glibc的，就是说如果代码使用的是eglic的库，那么换成glic之后无需重新编译。glibc为了实现最优化处理，致使在空间占用上越来越为人诟病。eglibc的主要特性是更好的支持嵌入式架构，支持不同的shell(GLIBC只支持bash)，支持-Os，可配置组件，稳定分支修正了一些重要Bug等。

### 查看 glibc 版本

```bash
ll /lib64/libc.so.6
ldd --version
# ldd --version    //ldd命令为glibc提供
dpkg -s libc6 | grep Ver
```

><https://nieyong.github.io/wiki_ny/glibc,%20eglibc%E5%92%8C%20glib%E7%9A%84%E5%8C%BA%E5%88%AB.html>  
><https://shixiangwang.github.io/home/cn/post/2020-09-28-note-about-glibc/>  
