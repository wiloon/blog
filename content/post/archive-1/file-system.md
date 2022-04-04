---
title: 文件系统
author: "-"
date: 2014-04-14T08:06:08+00:00
url: filesystem
categories:
  - OS
tags:
  - reprint
---
## 文件系统，block组，block，bmap，inode，inode table，imap

## 虚拟文件系统(VFS)

>https://blog.51cto.com/u_15265005/2888316

SunnyZhang的IT世界2021-06-10 11:12:32
文章标签Linux系统Linux教程文章分类Linux系统/运维阅读数340

概述
本文将介绍一下Linux的VFS虚拟机文件系统，主要介绍该文件系统在Linux中的作用及概要实现。我们知道在Linux系统中一切皆文件，如果说文件系统是Linux系统的基石一点也不过分。在Linux系统中基本上把其中的所有内容都看作文件，除了我们普通意义理解的文件之外，目录、字符设备、块设备、 套接字、进程、线程、管道等都被视为是一个“文件”。例如对于块设备，我们通过fdisk -l显示块设备列表，其实块设备可以理解为在文件夹/dev下面的文件。只不过这些文件是特殊的文件。

root@vmhost:~# ls /dev/ -alh |grep sd
brw-rw---- 1 root disk 8, 0 Dec 31 09:38 sda
brw-rw---- 1 root disk 8, 16 Dec 31 09:38 sdb
brw-rw---- 1 root disk 8, 32 Dec 31 09:38 sdc
1.
2.
3.
4.
如上面代码所示，每个块设备的前面有一个字符串brw-rw----，这个用于描述文件的属性，其中b字符表示这个文件是一个块设备，如果是d字符则表示是一个文件夹。同样，还有其它类型的设备也是一文件的形式进行表示的。那么Linux的文件系统要支持如此之多类型的文件是怎么做到的呢？那就是通过虚拟文件系统（Virtual File System简称VFS）。

 

Linux 虚拟文件系统(VFS)分析_Linux教程

图1 虚拟文件系统总图

VFS是一个抽象层，其向上提供了统一的文件访问接口，而向下则兼容了各种不同的文件系统。不仅仅是诸如Ext2、Ext4、XFS和Btrfs等常规意义上的文件系统，还包括伪文件系统和设备等等内容。由图1可以看出，虚拟文件系统位于应用与具体文件系统之间，其主要起适配的作用。对于应用程序来说，其访问的接口是完全一致的（例如open、read和write等），并不需要关系底层的文件系统细节。也就是一个应用可以对一个文件进行任何的读写，不用关心文件系统的具体实现。另外，VFS实现了一部分公共的功能，例如页缓存和inode缓存等，从而避免多个文件系统重复实现的问题。

VFS的存在可以让Linux操作系统实现非常复杂的文件系统关联关系。如图2所示，该系统根文件系统是Ext3文件系统，而在其/mnt目录下面又分别挂载了Ext4文件系统和XFS文件系统。最后形成了一个由多个文件系统组成的文件系统树。

Linux 虚拟文件系统(VFS)分析_Linux系统_02

图2 文件系统目录树

从VFS到具体文件系统
前文我们介绍到VFS是一个抽象层，VFS建立了应用程序与具体文件系统的联系，其提供了统一的访问接口实现对具体文件系统的访问（例如Ext2文件系统）。那么两者是怎么关联起来的呢？这里涉及如下几个处理流程：

挂载，也就是具体文件系统（例如Ext2）的挂载
打开文件，我们在访问一个文件之前首先要打开它（open）
文件访问，进行文件的读写操作（read或者write）
其中第1个流程其实是建立VFS和诸如Ext4文件系统的关联，这样当用户在后面打开某个文件的时候，VFS就知道应该调用那个文件系统的函数实现。而第2个流程则是初始化文件系统必要的数据结构和操作函数（例如read和write等），为后面的具体操作做准备。挂载的流程比较复杂，本文先概括的介绍一下，后续再做详细介绍。

挂载也是用户态发起的命令，就是我们知道的mount命令，该命令执行的时候需要指定文件系统的类型（本文假设Ext2）和文件系统数据的位置（也就是设备）。通过这些关键信息，VFS就可以完成Ext2文件系统的初始化，并将其关联到当前已经存在的文件系统中，也就是建立其图2所示的文件系统树。

本文不介绍代码细节，仅仅从数据结构方面介绍一下Linux文件系统挂载的具体原理。如图3是虚拟文件系统涉及的主要的数据结构。在挂载的过程中，最为重要的数据结构是vfsmount，它代表一个挂载点。其次是dentry和inode，这两个都是对文件的表示，且都会缓存在哈希表中以提高查找的效率。其中inode是对磁盘上文件的唯一表示，其中包含文件的元数据（管理数据）和文件数据等内容，但不含文件名称。而dentry则是为了Linux内核中查找文件方便虚拟出来的一个数据结构，其中包含文件名称、子目录（如果存在的话）和关联的inode等信息。

## superblock

superblock：记录此 filesystem 的整体信息,包括inode/block的总量、使用量、剩余量, 以及文件系统的格式与相关信息等；

Superblock 是记录整个 filesystem 相关信息的地方, 没有 Superblock ,就没有这个 filesystem 了.

记录的信息主要有：

block 与 inode 的总量
未使用与已使用的 inode / block 数量
block 与 inode 的大小 (block 为 1, 2, 4K,inode 为 128 bytes)
filesystem 的挂载时间、最近一次写入数据的时间、最近一次检验磁盘 (fsck) 的时间等文件系统的相关信息
一个 valid bit 数值,若此文件系统已被挂载,则 valid bit 为 0 ,若未被挂载,则 valid bit 为 1

## inode

inode：记录文件的权限与属性,一个文件占用一个inode,同时记录此文件的数据所在的 block 号码；  
contains file attributes, metadata of file, pointer structure  
>wiloon.com/inode

block：实际记录文件的内容,若文件太大时,会占用多个 block .

每个 inode 与 block 都有编号,而每个文件都会占用一个 inode ,inode 内则有文件数据放置的 block 号码.所以如果能够找到文件的 inode 的话,那么自然就会知道这个文件所放置数据的 block 号码, 当然也就能够读出该文件的实际数据了.

## file

can be considered a table with 2 columns, filename and its inode, inode points to the raw data blocks on the block device

## directory

(just a special file, container for other filenames. It contains an array of filenames and inode numbers for each filename. Also it describes the relationship between parent and children.)

A directory is just a special file which contains an array of filenames and inode numbers. When the directory was created, the file system allocated 1 inode to the directory with a "filename" (dir name in fact). The inode points to a single data block (minimum overhead), which is 4096 bytes. That's why you see 4096 / 4.0K when using ls.

## data block (数据区块)

block 基本限制

原则上,block 的大小与数量在格式化完就不能够再改变了(除非重新格式化)
每个 block 内最多只能够放置一个文件的数据
若文件大于 block 的大小,则一个文件会占用多个 block 数量
若文件小于 block ,则该 block 的剩余容量就不能够再被使用了(磁盘空间会浪费)
在 Ext2 文件系统中所支持的 block 大小有 1K, 2K 及 4K 三种而已, ext4 的 block 4k

## inode table

inode 数据内容：

该文件的存取模式(read/write/excute)
该文件的拥有者与群组(owner/group)
该文件的容量
该文件创建或状态改变的时间(ctime)
最近一次的读取时间(atime)
最近修改的时间(mtime)
定义文件特性的旗标(flag),如 SetUID...
该文件真正内容的指向 (pointer)
inode 的特色点：

每个 inode 大小均固定为 128 bytes
每个文件都仅会占用一个 inode 而已
承上,因此文件系统能够创建的文件数量与 inode 的数量有关
系统读取文件时需要先找到 inode,并分析 inode 所记录的权限与用户是否符合,若符合才能够开始实际读取 block 的内容
系统将 inode 记录 block 号码的区域定义为12个直接，一个间接, 一个双间接与一个三间接记录区,如下图所示：



## imap

文件系统 imap：inode 节点位图(inodemap)管理空闲inode

摘取自骏马金龙的第4章ext文件系统机制原理剖析

在写文件(Linux中一切皆文件)时需要为其分配一个inode号。

其实，在格式化创建文件系统后，所有的inode号都已计算好（创建文件系统时会为每个块组计算好该块组拥有哪些inode号），因此产生了问题：要为文件分配哪一个inode号呢？又如何知道某一个inode号是否已经被分配了呢？

既然是"是否被占用"的问题，使用位图是最佳方案，像bmap记录block的占用情况一样。标识inode号是否被分配的位图称为inodemap简称为imap。这时要为一个文件分配inode号只需扫描imap即可知道哪一个inode号是空闲的。

这样理解更容易些，类似bmap块位图一样，inode号是预先规划好的。inode号分配后，文件删除也会释放inode号。分配和释放的inode号，像是在一个地图上挖掉一块，用完再补回来一样。

imap存在着和bmap和inode table一样需要解决的问题：如果文件系统比较大，imap本身就会很大，每次存储文件都要进行扫描，会导致效率不够高。同样，优化的方式是将文件系统占用的block划分成块组，每个块组有自己的imap范围。

>https://www.jianshu.com/p/4a07b2c26879

## Superblock, 超级块

A superblock is a record of the characteristics of a filesystem, including its size, the block size, the empty and the filled blocks and their respective counts, the size and location of the inode tables, the disk block map and usage information, and the size of the block groups.

Superblock 记录整个文件系统的整体信息，包括inode与数据块的总量，使用量，剩余量，以及文件系统的格式和相关信息，每个block group中都可能包含了superblock，但是除了第1个Primary superblock有用外，其它的superblock作为第1个superblock的备份，称呼为Backup superblock。

>http://www.linfo.org/superblock

## 硬盘 SuperBlock 损坏修复

### 找到super block 备份

```bash
#查看文件系统备份Superblock
mke2fs -n /dev/sdb
#查看文件系统备份Superblock
dumpe2fs /dev/sdb1 | grep --before-context=1 superblock

arch# dumpe2fs /dev/sdb1 | grep --before-context=1 superblock
dumpe2fs 1.45.5 (07-Jan-2020)
Group 0: (Blocks 0-32767) csum 0xb451 [ITABLE_ZEROED]
  Primary superblock at 0, Group descriptors at 1-38
--
Group 1: (Blocks 32768-65535) csum 0x5489 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 32768, Group descriptors at 32769-32806
--
Group 3: (Blocks 98304-131071) csum 0x2257 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 98304, Group descriptors at 98305-98342
--
Group 5: (Blocks 163840-196607) csum 0x57e3 [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 163840, Group descriptors at 163841-163878
--
Group 7: (Blocks 229376-262143) csum 0xcfeb [INODE_UNINIT, ITABLE_ZEROED]
  Backup superblock at 229376, Group descriptors at 229377-229414
...
```

从上面操作可以看出，在第1、3、4、7、9这几个Block Group上存放有superblock备份

```bash
fsck -b 8193 /dev/sdb1
e2fsck -b 214990848 -y /dev/sdb
```

当你的系统出现 superblock corrupt 而无法启动时: 
  
1.用应急盘启动,先看fdisk的结果.如果你的分区表看起来正常,那么恢复的可能性就比较大,如果出现cannot open /dev/sda2的提示,那么想一想你的scsi卡启动没有,如果没有,那么你可以试着用小红帽的安装光盘启动,记住,仅仅是看分区表,千万不要写它.然后把分区情况详细记录下来.

2.试着e2fsck /dev/hda2,(先不要加-p -y 之类的参数,)用手动进行修复,同时也可以了解具体是文件系统的那些地方损坏了,如果你的运气好,e2fsck过去了,/dev/hda2已经基本修复,当然修复的可能是99.9%,也可能是99%这就看文件系统的损坏程度乐,不过现在可以说你的数据已经都找回来了.剩下的事就是mount上把数据备份出来以防万一.

3.如果e2fsck没过去(确保你的硬盘已经正确驱动乐),也不要着急,因为 superblock 在硬盘中有很多地方有备份,现在你最好把硬盘卸下来挂到另一个好的linux系统上,当然同样要保证硬盘被正确驱动乐.先用e2fsck /dev/hda2,如果结果和前面一样，就用e2fsck -b xxx -f /dev/hda2, xxx是硬盘上 superblock 的备份块,xxx=n*8192+1,n=1,2,3...一般来讲,如果系统瘫痪的真正原因是superblock损坏，这种办法就应该可以恢复你的数据了。如果执行后的结果还是不能通过,那么往下一步.

4.利用dd命令.先dd if=/dev/hda2 of=/tmp/rescue conv=noerror(/tmp/rescue是一个文件),把重要的数据拷出来,当然,这个盘要比你损坏的盘大一点,否则拷不下.另外,上面的dd命令在不同的境况下if和of应作相应的修改，写在这里只是一个例子，总之在用dd之前最好先看看man.刚才你已经看到你的分区表了,现在找一个和你的硬盘一样的硬盘,应该是一摸一样 (大小，型号),在这块硬盘上按照坏盘上的分区表分区，分的区也应该是也是一模一样然后用dd命令把坏盘上superblock location后的东西全部拷到好盘的superblock location后，上帝保佑你，当你再次启动系统时就可以看到熟悉的数据了,有人用这种方法恢复了99%以上的数据,不过好在这种方法(包括前面的方法)没有动那块坏盘上的数据,如果还是没有恢复,那没你还有最后一种选择.

在手册页里称这种方法为last-ditch recovery method,就是说这是最后的恢复方法，只有当你已经尝试了其他的方法,都没有能恢复你的数据的情况下才用,因为这需要冒一定的风险.
把你的硬盘挂在一台好的linux box上，运行: #mke2fs -S /dev/hda2(如果你的数据在hda2里) 这条命令只重建superblock，而不碰inode表，不过这仍有一定的风险。good luck to you all.当时也有人建议我如果实在不行的话就重装系统 (不动分区也不格式化) ，这也可能有效，但你也应该清楚这种方法就像mke2fs -S /dev/hd*一样是有风险的。

一点建议:
  
如果你的硬盘不是可以轻易就重做的，最好在建立一个新的系统后: 
  
1。拿出笔和纸,把你的分区信息详细记录下来.
  
1. 用mkbootdisk做好现在这个系统的启动盘并测试.特别是如果你用的硬盘是scsi的。
  
2. 在用mke2fs建立一个文件系统后将屏幕上的superblock所在位置记录下来。
  
3. 用crontab对重要数据进行备份。ext2文件系统 (包括其他的unix文件系统) 是很强壮的，但你仍然应该小心。

RedHat官方解释: 
  
解决方法:
  
通常在作磁盘操作之前应该备份磁盘的数据，在作这个操作之前也应该把磁盘上的所有内容备份到另一个磁盘中。就是说如果这个故障盘是20g的话，就需要一个20G的备份空间。备份的命令如下: 
  
#dd if=/dev/baddrive of=/storagearea
  
然后可以在已经卸载的故障盘上运行如下命令找到备份的superblock.
  
#mke2fs -n /dev/badparition
  
再运行mke2fs命令的时候需要把参数设置成为文件系统创建时所用的参数。如果当初使用的是默认值， 那就可以使用如下命令: 
  
#mke2fs -n -b 4000 /dev/hdb1
  
可以看到有如下的输出:
  
Filesystem label=
  
OS type: Linux
  
Block size=1024 (log=0)
  
Fragment size=1024 (log=0)
  
122400 inodes, 488848 blocks
  
24442 blocks (5.00%) reserved for the super user
  
First data block=1
  
60 block groups
  
8192 blocks per group, 8192 fragments per group
  
2040 inodes per group
  
Superblock backups stored on blocks:
          
8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409
  
从输出可知superblock存在于: 8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409.

http://blog.sina.com.cn/s/blog_709df8c80100ldup.html
  
http://homepage.smc.edu/morgan_david/cs40/analyze-ext2.htm?spm=a2c4e.10696291.0.0.169219a4BS6PeP

>https://www.cnblogs.com/xumenger/p/4491425.html

作者：CodeMyLove
链接：https://www.jianshu.com/p/477c5b583fbe
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

FAT 格式
闪盘使用的文件系统一般为 FAT 格式.FAT 这种格式的文件系统并没有 inode 存在,所以 FAT 没有办法将这个文件的所有 block 在一开始就读取出来.每个 block 号码都记录在前一个
block 当中

