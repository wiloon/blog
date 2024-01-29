---
title: ld.so.conf
author: "-"
date: 2016-12-24T10:27:20+00:00
url: /?p=9613
categories:
  - Inbox
tags:
  - reprint
---
## ld.so.conf
http://lsscto.blog.51cto.com/779396/904078

```bash
# 列出所有已经安装的共享库
ldconfig -p | less

```
 
Linux 共享库

Linux 系统上有两类根本不同的 Linux 可执行程序。第一类是静态链接的可执行程序。静态可执行程序包含执行所需的所有函数 — 换句话说,它们是"完整的"。因为这一原因,静态可执行程序不依赖任何外部库就可以运行。

第二类是动态链接的可执行程序。

静态可执行程序与动态可执行程序比较

我们可以用 ldd 命令来确定某一特定可执行程序是否为静态链接的: 
  
# ldd /sbin/sln
  
not a dynamic executable
  
"not a dynamic executable"是 ldd 说明 sln 是静态链接的一种方式。现在,让我们比较 sln 与其非静态同类 ln 的大小: 
  
# ls -l /bin/ln /sbin/sln
  
-rwxr-xr-x       1 root         root               23000 Jan 14 00:36 /bin/ln
  
-rwxr-xr-x       1 root         root             381072 Jan 14 00:31 /sbin/sln
  
如您所见,sln 的大小超过 ln 十倍。ln 比 sln 小这么多是因为它是动态可执行程序。动态可执行程序是不完整的程序,它依靠外部共享库来提供运行所需的许多函数。

动态链接相关性

要查看 ln 依赖的所有共享库的列表,可以使用 ldd 命令: 
  
# ldd /bin/ln
  
libc.so.6 => /lib/libc.so.6 (0x40021000)
  
/lib/ld-linux.so.2 => /lib/ld-linux.so.2 (0x40000000)

如您所见,ln 依赖外部共享库 libc.so.6 和 ld-linux.so.2。通常,动态链接的程序比其静态链接的等价程序小得多。不过,静态链接的程序可以在某些低级维护任务中发挥作用。例如,sln 是修改位于 /lib 中的不同库符号链接的极佳工具。但通常您会发现几乎所有 Linux 系统上的可执行程序都是某种动态链接的变体。

动态装入器

那么,如果动态可执行程序不包含运行所需的所有函数,Linux 的哪部分负责将这些程序和所有必需的共享库一起装入,以使它们能正确执行呢？答案是动态装入器 (dynamic loader) ,它实际上是您在 ln 的 ldd 清单中看到的作为共享库相关性列出的 ld-linux.so.2 库。动态装入器负责装入动态链接的可执行程序运行所需的共享库。现在,让我们迅速查看一下动态装入器如何在系统上找到适当的共享库。

ld.so.conf

动态装入器找到共享库要依靠两个文件 — /etc/ld.so.conf 和 /etc/ld.so.cache。如果您对 /etc/ld.so.conf 文件进行 cat 操作,您可能会看到一个与下面类似的清单: 

$ cat /etc/ld.so.conf

/usr/X11R6/lib

/usr/lib/gcc-lib/i686-pc-linux-gnu/2.95.3

/usr/lib/mozilla

/usr/lib/qt-x11-2.3.1/lib

/usr/local/lib

ld.so.conf 文件包含一个所有目录 (/lib 和 /usr/lib 除外,它们会自动包含在其中) 的清单,动态装入器将在其中查找共享库。

ld.so.cache

但是在动态装入器能"看到"这一信息之前,必须将它转换到 ld.so.cache 文件中。可以通过运行 ldconfig 命令做到这一点: 

# ldconfig

当 ldconfig 操作结束时,您会有一个最新的 /etc/ld.so.cache 文件,它反映您对 /etc/ld.so.conf 所做的更改。从这一刻起,动态装入器在寻找共享库时会查看您在 /etc/ld.so.conf 中指定的所有新目录。
  
ldconfig 技巧
  
要查看 ldconfig 可以"看到"的所有共享库,请输入: 
  
# ldconfig -p | less

还有另一个方便的技巧可以用来配置共享库路径。有时候您希望告诉动态装入器在尝试任何 /etc/ld.so.conf 路径以前先尝试使用特定目录中的共享库。在您运行的较旧的应用程序不能与当前安装的库版本一起工作的情况下,这会比较方便。

LD_LIBRARY_PATH

要指示动态装入器首先检查某个目录,请将 LD_LIBRARY_PATH 变量设置成您希望搜索的目录。多个路径之间用冒号分隔；例如: 

# export LD_LIBRARY_PATH="/usr/lib/old:/opt/lib"

导出 LD_LIBRARY_PATH 后,如有可能,所有从当前 shell 启动的可执行程序都将使用 /usr/lib/old 或 /opt/lib 中的库,如果仍不能满足一些共享库相关性要求,则转回到 /etc/ld.so.conf 中指定的库。