---
title: fdisk for linux
author: "-"
date: 2015-05-04T09:53:34+00:00
url: /?p=7609
categories:
  - Inbox
tags:
  - Linux

---
## fdisk for linux

```bash
sudo fdisk -l

sudo fdisk /dev/sdb
p (print the partition table)
d (delete partition)

n (create partition)
p (primary) 
enter (default first sector)
enter (default last sector)

t
83 (config partition type,83 (Linux))
c  W95 FAT32 (LBA)
7 HPFS/NTFS/exFAT

a (set bootable)
w
write to disk and exit

sudo mkfs.msdos -F 32 /dev/sdx1
sudo mkfs.ntfs /dev/sdx1
sudo mkfs.ext4 /dev/sdx3
sudo mkswap /dev/sda2
```

<http://blog.csdn.net/zhangkekf/article/details/10417203>

我的需求是,将新硬盘只分一个区来使用

fdisk -l   #查看硬盘挂在情况

Disk /dev/xvda: 21.5 GB, 21474836480 bytes
  
255 heads, 63 sectors/track, 2610 cylinders
  
Units = cylinders of 16065 * 512 = 8225280 bytes
  
Sector size (logical/physical): 512 bytes / 512 bytes
  
I/O size (minimum/optimal): 512 bytes / 512 bytes
  
Disk identifier: 0x00073f45

Device Boot      Start         End      Blocks   Id  System
  
/dev/xvda1   *           1        2611    20970496   83  Linux

Disk /dev/xvdb: 536.9 GB, 536870912000 bytes
  
255 heads, 63 sectors/track, 65270 cylinders
  
Units = cylinders of 16065 * 512 = 8225280 bytes
  
Sector size (logical/physical): 512 bytes / 512 bytes
  
I/O size (minimum/optimal): 512 bytes / 512 bytes
  
Disk identifier: 0x00000000

从上述返回的信息看到,第二块硬盘 /dev/xvdb 未挂载,

fdisk /dev/xvdb  #对第二块硬盘进行操作

Command (m for help): n  #新增加一个分区
  
Command action
  
e   extended
  
p   primary partition (1-4)

p  #选择"增加主分区"
  
Partition number (1-4):1     #选择作为1号分区

First cylinder (1-65270, default 1):   #直接回车,新的分区从硬盘的第1扇区开始
  
Using default value 1
  
Last cylinder, +cylinders or +size{K,M,G} (1-65270, default 65270):   #直接回车,新的分区到硬盘的末尾结束,即整块硬盘只分一个区,也是主分区。
  
Using default value 65270

Command (m for help): t   #选择分区类型
  
Selected partition 1
  
Hex code (type L to list codes): 83   #选择第83号分区类型 (linux类型)

Command (m for help): w  #保存到硬盘
  
The partition table has been altered!

Calling ioctl() to re-read partition table.
  
Syncing disks.

fdisk -l   #再次查看硬盘挂载情况,可发现新的硬盘已经ready

Disk /dev/xvda: 21.5 GB, 21474836480 bytes
  
255 heads, 63 sectors/track, 2610 cylinders
  
Units = cylinders of 16065 * 512 = 8225280 bytes
  
Sector size (logical/physical): 512 bytes / 512 bytes
  
I/O size (minimum/optimal): 512 bytes / 512 bytes
  
Disk identifier: 0x00073f45

Device Boot      Start         End      Blocks   Id  System
  
/dev/xvda1   *           1        2611    20970496   83  Linux

Disk /dev/xvdb: 536.9 GB, 536870912000 bytes
  
255 heads, 63 sectors/track, 65270 cylinders
  
Units = cylinders of 16065 * 512 = 8225280 bytes
  
Sector size (logical/physical): 512 bytes / 512 bytes
  
I/O size (minimum/optimal): 512 bytes / 512 bytes
  
Disk identifier: 0x30550159

Device Boot      Start         End      Blocks   Id  System
  
/dev/xvdb1               1       65270   524281243+  83  Linux

mkfs -t ext4 -c /dev/xvdb1    #格式化硬盘

格式化中。。。

以下内容转载自: <http://lbyzx123.iteye.com/blog/835004>

关于硬盘分区: 主分区 (包含扩展分区) 、逻辑分区,主分区最多有4个 (包含扩展分区) 。

因此我们在对硬盘分区时最好划分主分区连续,比如说: 主分区一、主分区二、扩展分区。

此文章以fdisk工具为例,对一个硬盘划分。

1. fdisk -l 查看系统上的硬盘,找到需要分区的硬盘后比如说: /dev/sdb.

然后,fdisk /dev/sdb

进入该设备。此时出现:

Command (m for help):

查看帮助信息: 输入m,看到如下信息

Command action
  
a   toggle a bootable flag
  
b   edit bsd disklabel
  
c   toggle the dos compatibility flag
  
d   delete a partition   注: 这是删除一个分区的动作；
  
l   list known partition types 注: l是列出分区类型,以供我们设置相应分区的类型；
  
m   print this menu 注: m 是列出帮助信息；
  
n   add a new partition 注: 添加一个分区；
  
o   create a new empty DOS partition table
  
p   print the partition table 注: p列出分区表；
  
q   quit without saving changes 注: 不保存退出；
  
s   create a new empty Sun disklabel
  
t   change a partition's system id 注: t 改变分区类型；
  
u   change display/entry units
  
v   verify the partition table
  
w   write table to disk and exit 注: 把分区表写入硬盘并退出；
  
x   extra functionality (experts only) 注: 扩展应用,专家功能；

具体每个参数的含义,请仔细阅读。常用的就是: d l m p q t w

2. 列出当前操作硬盘的分区情况,用p

Command (m for help): p

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+   c W95 FAT32 (LBA)
  
/dev/sda2              26         125      806400    5 Extended
  
/dev/sda5              26          50      201568+ 83 Linux
  
/dev/sda6              51          76      200781   83 Linux
  
3. 通过fdisk的d指令来删除一个分区

Command (m for help): p    注: 列出分区情况；

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+   c W95 FAT32 (LBA)
  
/dev/sda2              26         125      806400    5 Extended

/dev/sda5              26          50      201568+ 83 Linux
  
/dev/sda6              51          76      200781   83 Linux

Command (m for help): d 注: 执行删除分区指定；
  
Partition number (1-6): 6 注: 我想删除 sda6 ,就在这里输入 6 ；

Command (m for help): p 注: 再查看一下硬盘分区情况,看是否删除了？

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes
  
Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+   c W95 FAT32 (LBA)
  
/dev/sda2              26         125      806400    5 Extended
  
/dev/sda5              26          50      201568+ 83 Linux

Command (m for help):
  
警告: 删除分区时要小心,请看好分区的序号,如果您删除了扩展分区,扩展分区之下的逻辑分区都会删除；所以操作时一定要小心；如果知道自己操作错了,请不要惊慌,用q不保存退出；切记切记！！！！在分区操作错了之时,千万不要输入w保存退出！！！

4. 通过fdisk的n指令增加一个分区

Command (m for help): p

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+   c W95 FAT32 (LBA)
  
/dev/sda2              26         125      806400    5 Extended
  
/dev/sda5              26          50      201568+ 83 Linux

Command (m for help): n 注: 增加一个分区；
  
Command action
  
l   logical (5 or over) 注: 增加逻辑分区,分区编号要大于5；为什么要大于5,因为已经有sda5了；
  
p   primary partition (1-4) 注: 增加一个主分区；编号从 1-4 ；但sda1 和sda2都被占用,所以只能从3开始；
  
p
  
Partition number (1-4): 3
  
No free sectors available 注: 失败中,为什么失败？
  
注: 我试图增加一个主分区,看来是失败了,为什么失败？因为我们看到主分区+扩展分区把整个磁盘都用光了,看扩展分区的End的值,再看一下 p输出信息中有125 cylinders；最好还是看前面部份；那里有提到； 所以我们只能增加逻辑分区了；
  
Command (m for help): n
  
Command action
  
l   logical (5 or over)
  
p   primary partition (1-4)
  
l   注: 在这里输入l,就进入划分逻辑分区阶段了；
  
First cylinder (51-125, default 51):   注: 这个就是分区的Start 值；这里最好直接按回车,如果您输入了一个非默认的数字,会造成空间浪费；
  
Using default value 51
  
Last cylinder or +size or +sizeM or +sizeK (51-125, default 125): +200M 注: 这个是定义分区大小的,+200M 就是大小为200M ；当然您也可以根据p提示的单位cylinder的大小来算,然后来指定 End的数值。回头看看是怎么算的；还是用+200M这个办法来添加,这样能直观一点。如果您想添加一个10G左右大小的分区,请输入 +10000M ；

Command (m for help):
  
5. 通过fdisk的t指令指定分区类型

Command (m for help): t 注: 通过t来指定分区类型；
  
Partition number (1-6): 6 注: 要改变哪个分区类型呢？我指定了6,其实也就是sda6
  
Hex code (type L to list codes):L 注: 在这里输入L,就可以查看分区类型的id了；
  
Hex code (type L to list codes): b 注: 如果我想让这个分区是 W95 FAT32 类型的,通过L查看得知 b是表示的是,所以输入了b；
  
Changed system type of partition 6 to b (W95 FAT32) 注: 系统信息,改变成功；是否是改变了,请用p查看；

Command (m for help): p

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+   c W95 FAT32 (LBA)
  
/dev/sda2              26         125      806400    5 Extended
  
/dev/sda5              26          50      201568+ 83 Linux
  
/dev/sda6              51          75      201568+   b W95 FAT32
  
6. fdisk 的退出,用q或者 w

其中 q是 不保存退出,w是保存退出
  
7. 一个添加分区的例子

本例中我们会添加两个200M的主分区,其它为扩展分区,在扩展分区中我们添加两个200M大小的逻辑分区；
  
Command (m for help): p 注: 列出分区表；

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System

Command (m for help): n 注: 添加分区；
  
Command action
  
e   extended
  
p   primary partition (1-4)
  
p 注: 添加主分区；
  
Partition number (1-4): 1 注: 添加主分区1；
  
First cylinder (1-125, default 1):   注: 直接回车,主分区1的起始位置；默认为1,默认就好；
  
Using default value 1
  
Last cylinder or +size or +sizeM or +sizeK (1-125, default 125): +200M   注: 指定分区大小,用+200M来指定大小为200M

Command (m for help): n 注: 添加新分区；
  
Command action
  
e   extended
  
p   primary partition (1-4)
  
p 注: 添加主分区
  
Partition number (1-4): 2 注: 添加主分区2；
  
First cylinder (26-125, default 26):
  
Using default value 26
  
Last cylinder or +size or +sizeM or +sizeK (26-125, default 125): +200M 注: 指定分区大小,用+200M来指定大小为200M

Command (m for help): n
  
Command action
  
e   extended
  
p   primary partition (1-4)
  
e 注: 添加扩展分区；
  
Partition number (1-4): 3 注: 指定为3 ,因为主分区已经分了两个了,这个也算主分区,从3开始；
  
First cylinder (51-125, default 51): 注: 直接回车；
  
Using default value 51
  
Last cylinder or +size or +sizeM or +sizeK (51-125, default 125):   注: 直接回车,把其余的所有空间都给扩展分区；
  
Using default value 125

Command (m for help): p

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+ 83 Linux
  
/dev/sda2              26          50      201600   83 Linux
  
/dev/sda3              51         125      604800    5 Extended

Command (m for help): n
  
Command action
  
l   logical (5 or over)
  
p   primary partition (1-4)
  
l 注: 添加逻辑分区；
  
First cylinder (51-125, default 51):
  
Using default value 51
  
Last cylinder or +size or +sizeM or +sizeK (51-125, default 125): +200M 注: 添加一个大小为200M大小的分区；

Command (m for help): n
  
Command action
  
l   logical (5 or over)
  
p   primary partition (1-4)
  
l 注: 添加一个逻辑分区；
  
First cylinder (76-125, default 76):
  
Using default value 76
  
Last cylinder or +size or +sizeM or +sizeK (76-125, default 125): +200M 注: 添加一个大小为200M大小的分区；

Command (m for help): p 列出分区表；

Disk /dev/sda: 1035 MB, 1035730944 bytes
  
256 heads, 63 sectors/track, 125 cylinders
  
Units = cylinders of 16128 * 512 = 8257536 bytes

Device Boot      Start         End      Blocks   Id System
  
/dev/sda1               1          25      201568+ 83 Linux
  
/dev/sda2              26          50      201600   83 Linux
  
/dev/sda3              51         125      604800    5 Extended
  
/dev/sda5              51          75      201568+ 83 Linux
  
/dev/sda6              76         100      201568+ 83 Linux
  
然后我们根据前面所说通过t指令来改变分区类型； 最后不要忘记w保存退出；
  
五、对分区进行格式化,以及加载;
  
先提示一下；用 mkfs.bfs mkfs.ext2 mkfs.jfs mkfs.msdos mkfs.vfatmkfs.cramfs mkfs.ext3 mkfs.minix mkfs.reiserfs mkfs.xfs 等命令来格式化分区,比如我想格式化 sda6为ext3文件系统,则输入；

[root@localhost beinan]# mkfs -t ext3 -c /dev/sda6   具体参数含义,请man mkfs。
  
如果我想加载 sda6到目前系统来存取文件,应该有mount 命令,但首先您得建一个挂载目录；比如 /mnt/sda6 ；
  
[root@localhost beinan]# mkdir /mnt/sda6
  
[root@localhost beinan]# mount /dev/sda6 /mnt/sda6
  
[root@localhost beinan]# df -lh
  
Filesystem            容量 已用 可用 已用% 挂载点
  
/dev/hda8              11G 8.4G 2.0G 81% /
  
/dev/shm              236M     0 236M   0% /dev/shm
  
/dev/hda10             16G 6.9G 8.3G 46% /mnt/hda10
  
/dev/sda6             191M 5.6M 176M   4% /mnt/sda6
