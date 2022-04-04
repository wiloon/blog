---
title: /dev/shm
author: "-"
date: 2017-05-31T05:33:43+00:00
url: /?p=10406

categories:
  - inbox
tags:
  - reprint
---
## /dev/shm
http://dbua.iteye.com/blog/1271574

1.linux下的/dev/shm是什么？
  
/dev/shm/是linux下一个目录,/dev/shm目录不在磁盘上,而是在内存里,因此使用linux /dev/shm/的效率非常高,直接写进内存。
  
我们可以通过以下两个脚本来验证linux /dev/shm的性能: 
  
[root@db1 oracle]# ls -l linux_11gR2_grid.zip
  
-rw-r-r- 1 oracle dba 980831749 Jul 11 20:18 linux_11gR2_grid.zip
  
[root@db1 oracle]# cat mycp.sh
  
#!/bin/sh
  
echo `date`
  
cp linux_11gR2_grid.zip ..
  
echo `date`
  
[root@db1 oracle]# ./mycp.sh
  
Fri Jul 15 18:44:17 CST 2011
  
Fri Jul 15 18:44:29 CST 2011

[root@db1 shm]# df -h
  
Filesystem Size Used Avail Use% Mounted on
  
/dev/mapper/rootvg-lv01
                         
97G 9.2G 83G 10% /
  
/dev/sda1 99M 15M 80M 16% /boot
  
tmpfs 2.0G 0 2.0G 0% /dev/shm

[root@db1 oracle]# cat mycp1.sh
  
#!/bin/sh
  
echo `date`
  
cp linux_11gR2_grid.zip /dev/shm
  
echo `date`
  
[root@db1 oracle]# ./mycp1.sh
  
Fri Jul 15 18:44:29 CST 2011
  
Fri Jul 15 18:44:30 CST 2011
  
[root@db1 oracle]# df -h
  
Filesystem Size Used Avail Use% Mounted on
  
/dev/mapper/rootvg-lv01

97G 9.2G 83G 10% /
  
/dev/sda1 99M 15M 80M 16% /boot
  
tmpfs 2.0G 937M 1.1G 46% /dev/shm
  
[root@db1 oracle]#
  
可以看出,在对一个将近1g为文件的复制,拷到磁盘上与拷到/dev/shm下还是有很大差距的。
  
tmpfs有以下特点: 
  
1.tmpfs 是一个文件系统, 而不是块设备；您只是安装它, 它就可以使用了。
  
2.动态文件系统的大小。
  
3.tmpfs 的另一个主要的好处是它闪电般的速度。因为典型的 tmpfs 文件系统会完全驻留在 RAM 中,读写几乎可以是瞬间的。
  
4.tmpfs 数据在重新启动之后不会保留,因为虚拟内存本质上就是易失的。所以有必要做一些脚本做诸如加载、绑定的操作。
  
2.linux /dev/shm 默认容量
  
linux下/dev/shm的容量默认最大为内存的一半大小,使用df -h命令可以看到。但它并不会真正的占用这块内存,如果/dev/shm/下没有任何文件,它占用的内存实际上就是0字节；如果它最大为1G,里头放有100M文件,那剩余的900M仍然可为其它应用程序所使用,但它所占用的100M内存,是绝不会被系统回收重新划分的,否则谁还敢往里头存文件呢？
  
通过df -h查看linux /dev/shm的大小
  
[root@db1 shm]# df -h /dev/shm
  
Filesystem Size Used Avail Use% Mounted on
  
tmpfs 1.5G 0 1.5G 0% /dev/shm
  
3.linux /dev/shm 容量(大小)调整
  
linux /dev/shm容量(大小)是可以调整,在有些情况下(如oracle数据库)默认的最大一半内存不够用,并且默认的inode数量很低一般都要调高些,这时可以用mount命令来管理它。
  
mount -o size=1500M -o nr_inodes=1000000 -o noatime,nodiratime -o remount /dev/shm
  
在2G的机器上,将最大容量调到1.5G,并且inode数量调到1000000,这意味着大致可存入最多一百万个小文件
  
通过/etc/fstab文件来修改/dev/shm的容量(增加size选项即可),修改后,重新挂载即可: 
  
[root@db1 shm]# grep tmpfs /etc/fstab
  
tmpfs /dev/shm tmpfs defaults,size=2G 0 0
  
[root@db1 /]# umount /dev/shm
  
[root@db1 /]# mount /dev/shm
  
[root@db1 /]# df -h /dev/shm
  
Filesystem Size Used Avail Use% Mounted on
  
tmpfs 2.0G 0 2.0G 0% /dev/shm

[root@db1 /]# # mount -o remount /dev/shm
  
[root@db1 /]# df -h
  
Filesystem Size Used Avail Use% Mounted on
  
/dev/mapper/rootvg-lv01
                         
97G 9.2G 83G 10% /
  
/dev/sda1 99M 15M 80M 16% /boot
  
tmpfs 2.0G 0 2.0G 0% /dev/shm
  
附: tmpfs文档
  
Tmpfs is a file system which keeps all files in virtual memory.
  
Everything in tmpfs is temporary in the sense that no files will be
  
created on your hard drive. If you unmount a tmpfs instance,
  
everything stored therein is lost.
  
tmpfs puts everything into the kernel internal caches and grows and
  
shrinks to accommodate the files it contains and is able to swap
  
unneeded pages out to swap space. It has maximum size limits which can
  
be adjusted on the fly via 'mount -o remount …'
  
If you compare it to ramfs (which was the template to create tmpfs)
  
you gain swapping and limit checking. Another similar thing is the RAM
  
disk (/dev/ram*), which simulates a fixed size hard disk in physical
  
RAM, where you have to create an ordinary filesystem on top. Ramdisks
  
cannot swap and you do not have the possibility to resize them.
  
Since tmpfs lives completely in the page cache and on swap, all tmpfs
  
pages currently in memory will show up as cached. It will not show up
  
as shared or something like that. Further on you can check the actual
  
RAM+swap use of a tmpfs instance with df(1) and du(1).
  
tmpfs has the following uses:
  
1) There is always a kernel internal mount which you will not see at
  
all. This is used for shared anonymous mappings and SYSV shared
  
memory.
  
This mount does not depend on CONFIG_TMPFS. If CONFIG_TMPFS is not
  
set, the user visible part of tmpfs is not build. But the internal
  
mechanisms are always present.
  
2) glibc 2.2 and above expects tmpfs to be mounted at /dev/shm for
  
POSIX shared memory (shm_open, shm_unlink). Adding the following
  
line to /etc/fstab should take care of this:
  
tmpfs /dev/shm tmpfs defaults 0 0
  
Remember to create the directory that you intend to mount tmpfs on
  
if necessary (/dev/shm is automagically created if you use devfs).
  
This mount is _not_ needed for SYSV shared memory. The internal
  
mount is used for that. (In the 2.3 kernel versions it was
  
necessary to mount the predecessor of tmpfs (shm fs) to use SYSV
  
shared memory)
  
3) Some people (including me) find it very convenient to mount it
  
e.g. on /tmp and /var/tmp and have a big swap partition. But be
  
aware: loop mounts of tmpfs files do not work due to the internal
  
design. So mkinitrd shipped by most distributions will fail with a
  
tmpfs /tmp.
  
4) And probably a lot more I do not know about 🙂
  
tmpfs has a couple of mount options:
  
size: The limit of allocated bytes for this tmpfs instance. The
  
default is half of your physical RAM without swap. If you
  
oversize your tmpfs instances the machine will deadlock
  
since the OOM handler will not be able to free that memory.
  
nr_blocks: The same as size, but in blocks of PAGECACHE_SIZE.
  
nr_inodes: The maximum number of inodes for this instance. The default
  
is half of the number of your physical RAM pages.
  
These parameters accept a suffix k, m or g for kilo, mega and giga and
  
can be changed on remount.
  
To specify the initial root directory you can use the following mount
  
options:
  
mode: The permissions as an octal number
  
uid: The user id
  
gid: The group id
  
These options do not have any effect on remount. You can change these
  
parameters with chmod(1), chown(1) and chgrp(1) on a mounted filesystem.
  
So 'mount -t tmpfs -o size=10G,nr_inodes=10k,mode=700 tmpfs /mytmpfs'
  
will give you tmpfs instance on /mytmpfs which can allocate 10GB
  
RAM/SWAP in 10240 inodes and it is only accessible by root.
  
TODOs:
  
1) give the size option a percent semantic: If you give a mount option
  
size=50% the tmpfs instance should be able to grow to 50 percent of
  
RAM + swap. So the instance should adapt automatically if you add
  
or remove swap space.
  
2) loop mounts: This is difficult since loop.c relies on the readpage
  
operation. This operation gets a page from the caller to be filled
  
with the content of the file at that position. But tmpfs always has
  
the page and thus cannot copy the content to the given page. So it
  
cannot provide this operation. The VM had to be changed seriously
  
to achieve this.
  
3) Show the number of tmpfs RAM pages. (As shared?)
  
Author:
  
Christoph Rohland , 1.12.01