---
title: undefined reference to ...
author: "-"
date: 2012-03-22T03:42:56+00:00
url: /?p=2599
categories:
  - linux
tags:
  - linux

---
## undefined reference to ...

>https://zhuanlan.zhihu.com/p/81681440


/usr/bin/ld: cannot find -lxxx 的解决办法
在软件编译过程中，经常会碰到类似这样的编译错误：
/usr/bin/ld: cannot find -lhdf5

这表示找不到库文件 libhdf5.so，若是其它库文件，则是 cannot find -lxxx 了，其中 xxx 是库文件的名字。

将库文件所在路径添加到gcc的搜索路径
使用以下命令查询gcc能否搜寻到指定的库文件:

gcc -lgsasl --verbose

查询库文件 libhdf5.so 是否能在搜索路径中找到。


使用 /etc/ld.so.conf 配置文件
将库文件所在的路径加入到 /etc/ld.so.conf 尾部，并使之生效：

$ sudo echo '/opt/biosoft/hdf5-1.8.15-patch1/lib/' >> /etc/ld.so.conf
libhdf5.so 在路径 /opt/biosoft/hdf5-1.8.15-patch1/lib/ 下，将该路径加添加到配置文件中
$ sudo ldconfig
运行该命令，重新载入 /ext/ld.so.conf 中的路径，使修改生效。


ls -l /lib/x86_64-linux-gnu


cat /etc/ld.so.conf
include /etc/ld.so.conf.d/*.conf

ls -l /lib/x86_64-linux-gnu