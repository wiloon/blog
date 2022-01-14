---
title: swap
author: "-"
date: 2017-10-13T06:27:00+00:00
url: /?p=11259
categories:
  - Uncategorized

---
## swap
```bash
# 启用swap分区: 
swapon /dev/sda2
# 查看swap使用情况
swapon
# summary
swapon -s|column -t
# add swap to /etc/fstab
# /dev/sda2
UUID=ed325732-b768-4680-a4ff-24dd0da24509       none            swap            defaults        0 0
```

<http://coolnull.com/3699.html>

一．SWAP说明
  
1.1 SWAP概述
  
当系统的物理内存不够用的时候,就需要将物理内存中的一部分空间释放出来,以供当前运行的程序使用。那些被释放的空间可能来自一些很长时间没有什么操作的程序,这些被释放的空间被临时保存到Swap空间中,等到那些程序要运行时,再从Swap中恢复保存的数据到内存中。这样,系统总是在物理内存不够时,才进行Swap交换。这个是SWAP 交换分区的作用。 实际上,我们更关注的应该是SWAP分区的大小问题。 设置多大才是最优的。

一般来说可以按照如下规则设置swap大小: 
  
4G以内的物理内存,SWAP 设置为内存的2倍。
  
4-8G的物理内存,SWAP 等于内存大小。
  
8-64G 的物理内存,SWAP 设置为8G。
  
64-256G物理内存,SWAP 设置为16G。

实际上,系统中交换分区的大小并不取决于物理内存的量,而是取决于系统中内存的负荷,所以在安装系统时要根据具体的业务来设置SWAP的值。

1.2 系统在什么情况下才会使用SWAP？
  
实际上,并不是等所有的物理内存都消耗完毕之后,才去使用swap的空间,什么时候使用是由swappiness 参数值控制。

[root@rhce ~]# cat /proc/sys/vm/swappiness
  
该值默认值是60.
  
swappiness=0的时候表示最大限度使用物理内存,然后才是 swap空间,
  
swappiness＝100的时候表示积极的使用swap分区,并且把内存上的数据及时的搬运到swap空间里面。

1.3 如何修改swappiness参数？
  
临时修改: 

[root@rhce ~]# sysctl vm.swappiness=10
  
vm.swappiness = 10
  
[root@rhce ~]# cat /proc/sys/vm/swappiness
  
这里我们的修改已经生效,但是如果我们重启了系统,又会变成60.

永久修改: 
  
在/etc/sysctl.conf文件里添加如下参数,

vm.swappiness=10
  
或echo 'vm.swappiness=10' >>/etc/sysctl.conf
  
保存,重启,就生效了。

二．管理SWAP
  
2.1 查看系统当前SWAP空间大小

[root@coolnull ~]# free -m
              
total used free shared buffers cached
  
Mem: 1954 1923 31 0 21 1345
  
-/+ buffers/cache: 555 1399
  
Swap: 1999 21 1978
  
free命令默认单位为k, -m 单位为M。 我们这里的swap使用了21M的空间。

2.2 查看SWAP使用情况
  
假设我们的系统出现了性能问题,我们通过vmstat命令看到有大量的swap,而我们的物理内存又很充足,那么我们可以手工把swap空间释放出来。让进程去使用物理内存,从而提高性能。

    vmstat 1 5
  
procs ----memory---- -swap---io-- -system- --cpu--
   
r b swpd free buff cache si so bi bo in cs us sy id wa st
   
0 0 22272 32620 22032 1378312 0 0 33 38 0 41 1 2 96 0 0
   
0 0 22272 32612 22032 1378340 0 0 0 0 902 1627 0 5 95 0 0
   
0 0 22272 32612 22032 1378340 0 0 0 0 905 1636 1 8 91 0 0
   
0 0 22272 32612 22032 1378340 0 0 0 32 907 1616 0 6 94 0 0
   
0 0 22272 32612 22032 1378340 0 0 0 0 924 1651 0 8 92 0 0

2.3 验证swap状态,swapon –s等于cat/proc/swaps

[root@coolnull ~]# swapon -s
  
Filename Type Size Used Priority
  
/dev/sda2 partition 2047992 22272 -1

[root@coolnull ~]# cat /proc/swaps
  
Filename Type Size Used Priority
  
/dev/sda2 partition 2047992 22272 -1
  
这里/dev/sda2是我们在安装操作系统时划分的磁盘分区。实际上,我们也可以使用文件来做为交换分区。具体后面会演示。

2.4 关闭swap交换分区: 

[root@coolnull ~]# swapoff/dev/sda2
  
[root@coolnull ~]# swapon -s
  
Filename Type Size Used Priority

2.5 启用swap分区: 

[root@coolnull ~]# swapon /dev/sda2
  
简单的说ext分区是否启用由mount及umount控制。swap分区是否启动,由swapon及swapoff控制。我们对swap 空间的释放,也是通过关闭swap分区,在启动swap 分区来实现的。

2.6查看/etc/fstab 文件,swap是否开机启动在这里配置

[root@coolnull ~]# cat /etc/fstab
  
/dev/sda2 none swap defaults 0 0

三. 增加swap空间
  
3.1 使用文件来作为SWAP 交换分区,这里我们使用文件添加一个交换区,具体操作如下: 
  
在根目录下生成一个文件: swap-file,大小1G: 

[root@coolnull u01]# dd if=/dev/zero of=/swap-file bs=1M count=1024
  
1024+0 records in
  
1024+0 records out
  
1073741824 bytes (1.1 GB) copied, 5.91518 s, 182MB/s
  
[root@coolnull u01]# cd /
  
[root@coolnull /]# ls
  
bin cgroup etc lib lost+found misc net proc sbin srv sys u01 usr
  
boot dev home lib64 media mnt opt root selinux swap-file tmp u02 var
  
[root@coolnull /]#

修改swap-file文件的权限,听说是为了增加安全。这里我是不能理解,如果改成只有root可读写的话那些非root用户执行的程序怎么办

# chown root:root /swap-file

# chmod 0600 /swap-file

将生成的文件格式化成交换分区: 

[root@coolnull /]# mkswap /swap-file
  
mkswap: /swap-file: warning: don't erase bootbitssectors
          
onwhole disk. Use -f to force.
  
Setting up swapspace version 1, size = 1048572 KiB
  
no label, UUID=653bbeb5-4abb-4295-b110-5847e073140d
  
这里没有分区的lable,只有一个UUID。

启动swap分区并查看状态: 

[root@coolnull /]# swapon /swap-file
  
[root@coolnull /]# swapon -s
  
Filename Type Size Used Priority
  
/dev/sda2 partition 2047992 0 -1
  
/swap-file file 1048568 0 -2
  
这里我们就看到了2个swap。

但是这个只对当前有效,如果想下次重启系统后还继续有效,需要将配置写入到/etc/fstab文件中。
  
在/etc/fstab文件中添加如下内容: 

UUID=653bbeb5-4abb-4295-b110-5847e073140d swap swap defaults 0 0
  
或者: 
  
/swap-file swap swap defaults 0 0

3.2使用磁盘添加swap
  
这个后面添加

四、停用swap交换分区: 

[root@coolnull ~]# swapoff /dev/sda2 //如果是文件则swapoff /swap-file
  
[root@coolnull ~]# swapon -s
  
Filename Type Size Used Priority
  
附录: 
  
Linux Add a Swap File – Howto
  
Do We Really Still Need Swap Space?
  
Knowledge Base:Is swap space really necessary

https://blog.csdn.net/tianlesoftware/article/details/8741873