---
title: swap
author: "-"
date: 2017-10-13T06:27:00+00:00
url: swap
categories:
  - Linux
tags:
  - Linux
---
## swap

### 查看 swap 使用情况, 没有输出的话就是没有启用 swap

```bash
swapon
free -m
cat /proc/swaps
vmstat 1 5

```

```bash
NAME      TYPE      SIZE USED PRIO
/dev/vda2 partition 1.9G 1.5G   -1
# PRIO, Priority
# /dev/vda2 是安装操作系统时划分的磁盘分区, 也可以使用文件来做为交换分区

```

```bash
# 启用 swap 分区
swapon /dev/vda2
# 如果是文件则
swapon /swap-file
swapoff /swap-file

# -s, --summary
swapon -s|column -t
# add swap to /etc/fstab, 启动之后自动挂载 swap 分区
# /dev/sda2, swap分区
UUID=ed325732-b768-4680-a4ff-24dd0da24509       none            swap            defaults        0 0
# swap 文件的配置
/swap-file       none            swap            defaults        0 0

# 关闭swap交换分区
swapoff /dev/vda2
```

### priority

swap分区的优先级 (priority）有啥用？
在使用多个swap分区或者文件的时候，还有一个优先级的概念 (Priority）。

在swapon的时候，我们可以使用-p参数指定相关swap空间的优先级，值越大优先级越高，可以指定的数字范围是－1到32767。

内核在使用swap空间的时候总是先使用优先级高的空间，后使用优先级低的。

当然如果把多个swap空间的优先级设置成一样的，那么两个swap空间将会以轮询方式并行进行使用。

如果两个swap放在两个不同的硬盘上，相同的优先级可以起到类似RAID0的效果，增大swap的读写效率。

另外，编程时使用mlock()也可以将指定的内存标记为不会换出，具体帮助可以参考man 2 mlock。

<https://www.cnblogs.com/276815076/p/5564085.html>
<http://coolnull.com/3699.html>

### SWAP

当系统的物理内存不够用的时候,就需要将物理内存中的一部分空间释放出来,以供当前运行的程序使用。那些被释放的空间可能来自一些很长时间没有什么操作的程序,这些被释放的空间被临时保存到Swap空间中,等到那些程序要运行时,再从Swap中恢复保存的数据到内存中。这样,系统总是在物理内存不够时,才进行Swap交换。这个是SWAP 交换分区的作用。 实际上,我们更关注的应该是SWAP分区的大小问题。 设置多大才是最优的。

一般来说可以按照如下规则设置swap大小:
  
4G以内的物理内存,SWAP 设置为内存的2倍。
  
4-8G的物理内存,SWAP 等于内存大小。
  
8-64G 的物理内存,SWAP 设置为8G。
  
64-256G物理内存,SWAP 设置为16G。

实际上,系统中交换分区的大小并不取决于物理内存的量,而是取决于系统中内存的负荷,所以在安装系统时要根据具体的业务来设置SWAP的值。

### 系统在什么情况下才会使用SWAP？
  
实际上,并不是等所有的物理内存都消耗完毕之后,才去使用swap的空间,什么时候使用是由 swappiness 参数值控制。

    cat /proc/sys/vm/swappiness

该值默认值是 60
  
swappiness=0 的时候表示最大限度使用物理内存,然后才是 swap空间,
  
swappiness＝100 的时候表示积极的使用swap分区,并且把内存上的数据及时的搬运到swap空间里面。

### 如何修改swappiness参数？
  
临时修改:

    sysctl vm.swappiness=10
  
vm.swappiness = 10
  
    cat /proc/sys/vm/swappiness
  
这里我们的修改已经生效,但是如果我们重启了系统,又会变成60.

永久修改:
  
在 /etc/sysctl.conf 文件里添加如下参数,

vm.swappiness=10
  
或echo 'vm.swappiness=10' >> /etc/sysctl.conf
  
保存,重启,就生效了。

### 增加swap空间
  
使用文件来作为SWAP 交换分区, 这里我们使用文件添加一个交换区,具体操作如下:
  
在根目录下生成一个文件: swap-file,大小1G:

    dd if=/dev/zero of=/swap-file bs=1M count=1024
  
1024+0 records in
  
1024+0 records out
  
1073741824 bytes (1.1 GB) copied, 5.91518 s, 182MB/s
  
[root@coolnull u01]# cd /
  
[root@coolnull /]# ls
  
bin cgroup etc lib lost+found misc net proc sbin srv sys u01 usr
  
boot dev home lib64 media mnt opt root selinux swap-file tmp u02 var
  
[root@coolnull /]#

修改swap-file文件的权限,听说是为了增加安全。这里我是不能理解,如果改成只有root可读写的话那些非root用户执行的程序怎么办

    chown root:root /swap-file

    chmod 0600 /swap-file

将生成的文件格式化成交换分区:

    mkswap /swap-file
  
mkswap: /swap-file: warning: don't erase bootbitssectors

onwhole disk. Use -f to force.
  
Setting up swapspace version 1, size = 1048572 KiB
  
no label, UUID=653bbeb5-4abb-4295-b110-5847e073140d
  
这里没有分区的lable,只有一个UUID。

### 使用磁盘添加 swap
  
这个后面添加

四、停用swap交换分区:

[root@coolnull ~]# swapoff /dev/sda2 //如果是文件则swapoff /swap-file
  
[root@coolnull ~]# swapon -s
  
Filename Type Size Used Priority
  
附录:
  
Linux Add a Swap File – Howto
  
Do We Really Still Need Swap Space?
  
Knowledge Base:Is swap space really necessary

<https://blog.csdn.net/tianlesoftware/article/details/8741873>
