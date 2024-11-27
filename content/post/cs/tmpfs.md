---
title: linux 内存盘 tmpfs
author: "-"
date: 2018-01-16T05:10:15+00:00
url: /?p=11727
categories:
  - Inbox
tags:
  - reprint
---
## linux 内存盘 tmpfs

```bash
# archlinux tmp dir resize
sudo mount -o remount,size=10G,noatime /tmp
mount tmpfs /tmp -t tmpfs -o size=1024m
  
```

把内存当硬盘, 提速你的 linux 系统

场景: 电脑内存太大用不了那么多, 空着浪费, 所以利用起来。内存读写速度高用来缓存或者编译, 甚至存临时文件最好不过了～～

Windows 下有一种叫法叫做内存盘, Linux 自然也有, 看了 Linux 中 ramdisk, tmpfs, ramfs 比较与说明这篇文章后, 决定使用 tmpfs 文件系统。

关于 tmpfs和VM
  
linux 的内存 (VM) ,包括 ram和 swap两部分。

ram 就是你的物理内存, swap 就是在装系统的时候划分的swap分区(在win下叫做页面文件,默认位于C:\pagefiles.sys)。
  
VM也是程序所能使用的最大内存上限,tmpfs本质上也是VM,tmpfs划出VM的部分页面作为一个文件系统.
  
关于 tmpfs 和 ramdisk
  
linux 下的 ramdisk 是由内核提供的, 要使用之, mount 命令挂载即可。不需要第三方工具。但因为它会被视为块设备, 所以仍然需要格式化该文件系统。
  
ramdisk 一旦创建就会占用固定大小的物理内存, tmpfs则是动态分配。
  
tmpfs 的优点
  
因为 tmpfs 是建立在 VM 上的, 而不是物理磁盘上, 所以不需要格式化就可以使用,所以不用尝试mkfs.tmpfs了,没有这条命令。

tmpfs的大小是动态的,用多少才分配多少,删除文件则会释放相应的VM空间,=.=这一点非常令人激动。

当您的物理内存不足以支撑分配为tmpfs的大小时,它会自动使用swap的页面。

tmpfs大部分时间是驻留在物理内存中,这使得其读写速度超快。

tmpfs的缺点:
  
tmpfs的先天优势变成了他的先天劣势:

内存的特性导致位于tmpfs上的数据断电会丢失。
  
相比较硬盘的价格来说,内存无疑还是很昂贵的,所以用tmpfs的目录不要放太大的东西。
  
tmpfs的用途
  
程序运行产生的临时文件, 我觉得tmpfs天生就是为tmp目录设计的。
  
编译时的缓存目录,用内存来做真是再好不过。
  
tmpfs的用法
  
mount tmpfs /tmp -t tmpfs -o size=1024m
  
1024不是固定的,实际大小根据你的实际情况定,比如可以在系统开了很长时间很大负载的时候看看(空闲的内存和swap)一共还有多少,最好不要超过这个值。
  
这里必须有mount权限,可以用sudo来获得权限,'size='指定tmpfs动态大小的上限,如果/tmp目录(即将使用的)大小超过指定大小,一样会提示你空间不足。
  
之所以不推荐这样做,是因为mount之后/tmp会被立即清空,如果你有程序有在/tmp中打开的文件(比如socket),会出错,而且每次都要手动挂载,多麻烦(=.=#)。
  
基于以上原因,最好还是编辑/etc/fstab文件来让系统启动时帮你搞定。
  
推荐方法如下:
  
sudo gedit /etc/fstab
  
在最后添加如下内容:

mount tmpfs in /tmp/
  
tmpfs /tmp tmpfs size=1024m 0 0
  
保存,关闭,然后在下次启动时你就用上tmpfs了。
  
[https://www.jianshu.com/p/6f9b200671bb](https://www.jianshu.com/p/6f9b200671bb)
  
[https://wiki.archlinux.org/index.php/tmpfs](https://wiki.archlinux.org/index.php/tmpfs)
