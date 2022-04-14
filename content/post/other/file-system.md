---
title: 虚拟文件系统
author: "-"
date: 2014-04-14T08:06:08+00:00
url: vfs
categories:
  - OS
tags:
  - reprint
---
## 虚拟文件系统

- 为什么需要虚拟文件系统
- 虚拟文件系统
- 超级块，superblock
- inode

## 为什么需要虚拟文件系统

在 Linux 系统中一切皆文件，除了普通文件之外，目录、字符设备、块设备、套接字、进程、线程、管道等都是“文件”。
用户程序需要一个统一的操作接口屏蔽不同文件系统（ext2/3/4,xfs,vfat,socket）的差异和操作细节

在Linux中对文件的 操作可以跨文件系统而执行。如下图所示，我们可以使用 cp 命令从 fat 文件系统格式的硬盘拷贝数据到 ext2 文件系统格式的硬盘；而这样的操作涉及到两个不同的文件系统. 上层应用几乎不用关注底层的实现细节。我们只需要使用VFS暴露出来的标准的read、write等接口就可以了

通过VFS系统，Linux提供了通用的系统调用，可以跨越不同文件系统和介质之间执行，极大简化了用户访问不同文件系统的过程。

“一切皆是文件”是 Unix/Linux 的基本哲学之一。不仅普通的文件，目录、字符设备、块设备、 套接字等在 Unix/Linux 中都是以文件被对待；它们虽然类型不同，但是对其提供的却是同一套操作界面。

## 虚拟文件系统， Virtual File System，VFS

VFS 是 Linux 内核中的一个软件层，是内核的子系统之一，为用户空间的程序提供文件和文件系统操作的统一接口，屏蔽不同文件系统的差异和操作细节

借助 VFS 可以直接使用open()、read()、write() 这样的系统调用操作文件，而无须考虑具体的文件系统和实际的存储介质。

通过 VFS，Linux 提供了通用的系统调用，可以跨越不同文件系统和介质之间执行，极大简化了用户访问不同文件系统的过程。另一方面，新的文件系统、新类型的存储介质，可以无须编译的情况下，动态加载到Linux中。

"一切皆文件"是Linux的基本哲学之一，不仅是普通的文件，包括目录、字符设备、块设备、套接字等，都可以以文件的方式被对待。实现这一行为的基础，正是Linux的虚拟文件系统机制。

VFS原理
VFS之所以能够衔接各种各样的文件系统，是因为它抽象了一个通用的文件系统模型，定义了通用文件系统都支持的、概念上的接口。新的文件系统只要支持并实现这些接口，并注册到Linux内核中，即可安装和使用。

虚拟文件系统组成部分
Linux为了实现这种VFS系统，采用面向对象的设计思路，主要抽象了四种对象类型：

超级块对象：代表一个已安装的文件系统。
索引节点对象：代表具体的文件。
目录项对象：代表一个目录项，是文件路径的一个组成部分。
文件对象：代表进程打开的文件。
每个对象都包含一组操作方法，用于操作相应的文件系统。

备注：Linux将目录当做文件对象来处理，是另一种形式的文件，它里面包含了一个或多个目录项。而目录项是单独抽象的对象，主要包括文件名和索引节点号。因为目录是可以层层嵌套，以形成文件路径，而路径中的每一部分，其实就是目录项。

接下来介绍一下各个对象的作用以及相关操作。

## 超级块, superblock

存储一个已安装的文件系统的控制信息（文件系统的状态、类型、大小、区块数、索引节点数等），代表一个已安装的文件系统；每次一个实际的文件系统被安装时， 内核会从磁盘的特定位置读取一些控制信息来填充内存中的超级块对象。一个安装实例和一个超级块对象一一对应。 超级块通过其结构中的一个域s_type记录它所属的文件系统类型。

superblock：记录此 filesystem 的整体信息,包括inode/block的总量、使用量、剩余量, 以及文件系统的格式与相关信息等；

Superblock 是记录整个 filesystem 相关信息的地方, 没有 Superblock ,就没有这个 filesystem 了.

记录的信息主要有：

block 与 inode 的总量
未使用与已使用的 inode / block 数量
block 与 inode 的大小 (block 为 1, 2, 4K,inode 为 128 bytes)
filesystem 的挂载时间、最近一次写入数据的时间、最近一次检验磁盘 (fsck) 的时间等文件系统的相关信息
一个 valid bit 数值,若此文件系统已被挂载,则 valid bit 为 0 ,若未被挂载,则 valid bit 为 1


超级块
超级块用于存储文件系统的元信息，由super_block结构体表示，定义在<linux/fs.h>中，元信息里面包含文件系统的基本属性信息，比如有：

索引节点信息
挂载的标志
操作方法 s_op
安装权限
文件系统类型、大小、区块数
等等等等
其中操作方法 s_op 对每个文件系统来说，是非常重要的，它指向该超级块的操作函数表，包含一系列操作方法的实现，这些方法有：

分配inode
销毁inode
读、写inode
文件同步
等等
当VFS需要对超级块进行操作时，首先要在超级块的操作方法 s_op 中，找到对应的操作方法后再执行。比如文件系统要写自己的超级块：

superblock->s_op->write_supper(sb);
创建文件系统时，其实就是往存储介质的特定位置，写入超级块信息；而卸载文件系统时，由VFS调用释放超级块。

Linux支持众多不同的文件系统，file_system_type结构体用于描述每种文件系统的功能和行为，包括：

名称、类型等
超级块对象链表
等
当向内核注册新的文件系统时，其实是将file_system_type对象实例化，然后加入到Linux的根文件系统的目录树结构上。

索引
索引节点对象包含Linux内核在操作文件、目录时，所需要的全部信息，这些信息由inode结构体来描述，定义在<linux/fs.h>中，主要包含：

超级块相关信息
目录相关信息
文件大小、访问时间、权限相关信息
引用计数
等等
一个索引节点inode代表文件系统中的一个文件，只有当文件被访问时，才在内存中创建索引节点。与超级块类似的是，索引节点对象也提供了许多操作接口，供VFS系统使用，这些接口包括：

create(): 创建新的索引节点（创建新的文件）
link(): 创建硬链接
symlink(): 创建符号链接。
mkdir(): 创建新的目录。
等等，我们常规的文件操作，都能在索引节点中找到相应的操作接口。

## 目录项, dentry

前面提到VFS把目录当做文件对待，比如/usr/bin/vim，usr、bin和vim都是文件，不过vim是一个普通文件，usr和bin都是目录文件，都是由索引节点对象标识。

由于VFS会经常的执行目录相关的操作，比如切换到某个目录、路径名的查找等等，为了提高这个过程的效率，VFS引入了目录项的概念。一个路径的组成部分，不管是目录还是普通文件，都是一个目录项对象。/、usr、bin、vim都对应一个目录项对象。不过目录项对象没有对应的磁盘数据结构，是VFS在遍历路径的过程中，将它们逐个解析成目录项对象。

目录项由 dentry 结构体标识，定义在<linux/dcache.h>中，主要包含：

父目录项对象地址
子目录项链表
目录关联的索引节点对象
目录项操作指针
等等
目录项有三种状态：

被使用：该目录项指向一个有效的索引节点，并有一个或多个使用者，不能被丢弃。
未被使用：也对应一个有效的索引节点，但VFS还未使用，被保留在缓存中。如果要回收内存的话，可以撤销未使用的目录项。
负状态：没有对应有效的索引节点，因为索引节点被删除了，或者路径不正确，但是目录项仍被保留了。
将整个文件系统的目录结构解析成目录项，是一件费力的工作，为了节省VFS操作目录项的成本，内核会将目录项缓存起来。

## 目录项高速缓存, dentry_cache

​ 目录项不同于inode、目录项对象在磁盘上没有对应的映射。目录项对象存放在名为dentry_cache的slab分配器高速缓存中。由于磁盘中并没有目录项，所以需要动态的构造，当然就要花费时间。完成构造操作后，我们会在内存中保留它。所以你连续多次访问文件会比第一次快。这个保存它的内存才是目录项高速缓存。

管理目录项高速缓存的数据结构有两个：
一个是处于正在使用、未使用或负状态的目录项对象的集合。这用的是双向链表。

一个叫dentry_hashtable的散列表，从中能够快速获取与给定的文件名和目录名对应的目录项对象。

## 文件

文件对象是进程打开的文件在内存中的实例。Linux用户程序可以通过open()系统调用来打开一个文件，通过close()系统调用来关闭一个文件。由于多个进程可以同时打开和操作同一个文件，所以同一个文件，在内存中也存在多个对应的文件对象，但对应的索引节点和目录项是唯一的。

文件对象由file结构体表示，定义在<linux/fs.h>中，主要包含：

文件操作方法
文件对象的引用计数
文件指针的偏移
打开文件时的读写标识
等等等等
类似于目录项，文件对象也没有实际的磁盘数据，只有当进程打开文件时，才会在内存中产生一个文件对象。

每个进程都有自己打开的一组文件，由file_struct结构体标识，该结构体由进程描述符中的files字段指向。主要包括：

fdt
fd_array[NR_OPEN_DEFAULT]
引用计数
等
fd_array数组指针指向已打开的文件对象，如果打开的文件对象个数 > NR_OPEN_DEFAULT，内核会分配一个新数组，并将 fdt 指向该数组。

除此之外，内核还为所有打开文件维持一张文件表，包括：

文件状态标志
文件偏移量
等
关于多进程打开同一文件以及文件共享更详细的信息，可以阅读《UNIX环境高级编程》第三章。

3. 总结
Linux支持了很多种类的文件系统，包含本地文件系统ext3、ext4到网络文件系统NFS、HDFS等，VFS系统屏蔽了不同文件系统的操作差异和实现细节，提供了统一的实现框架，也提供了标准的操作接口，这大大降低了操作文件和接入新文件系统的难度。

4. 参考
深入理解Linux内核
Linux内核设计与实现

---

在Linux系统中一切皆文件，除了我们普通意义理解的文件之外，目录、字符设备、块设备、 套接字、进程、线程、管道等都被视为是一个“文件”。例如对于块设备，我们通过fdisk -l 显示块设备列表，其实块设备可以理解为在文件夹/dev下面的文件。只不过这些文件是特殊的文件。

root@vmhost:~# ls /dev/ -alh |grep sd
brw-rw---- 1 root disk 8, 0 Dec 31 09:38 sda
brw-rw---- 1 root disk 8, 16 Dec 31 09:38 sdb
brw-rw---- 1 root disk 8, 32 Dec 31 09:38 sdc

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


## inode

inode：记录文件的权限与属性,一个文件占用一个inode,同时记录此文件的数据所在的 block 号码；  
contains file attributes, metadata of file, pointer structure  
>wiloon.com/inode

block：实际记录文件的内容,若文件太大时,会占用多个 block .

每个 inode 与 block 都有编号,而每个文件都会占用一个 inode ,inode 内则有文件数据放置的 block 号码.所以如果能够找到文件的 inode 的话,那么自然就会知道这个文件所放置数据的 block 号码, 当然也就能够读出该文件的实际数据了.

## 索引节点高速缓存, icache

在文件系统中，有三大缓冲为了提升效率：inode缓冲区、dentry缓冲区、块缓冲。

为了加快对索引节点的索引，引入inode缓冲区

有多个链表用于管理inode节点：

inode_in_use：正在使用的inode，即有效的inode，i_count > 0且i_nlink > 0。
inode_unused：有效的节点，但是还没有使用，处于空闲状态。(数据不在pagecache中)。

inode_unused_pagecache：同上。(数据在pagecache中)。

inode_hashtable：用于inode在hash表中，提高查找效率。

anon_hash_chain：用于超级块是空的的inodes。例如：sock_alloc()函数, 通过调用fs/inode.c中get_empty_inode()创建的套接字是一个匿名索引节点，这个节点就加入到了anon_hash_chain链表。

dirty：用于保存超级块中的所有的已经修改的inodes。

硬盘里的inode diagram里的数据结构，在内存中会通过slab分配器，组织成 xxx_inode_cache，统计在meminfo的可回收的内存中。 inode表也会记录每一个inode 在硬盘中摆放的位置。这里所说的索引节点高速缓存也就是我们常说的icache.

​ 关于索引节点高速缓存的更加详细的信息，请参考其他资料：inode缓冲区. 在内核中，并不丢弃与未用目录项相关的索引节点，这是由于目录项高速缓存仍在使用它们。因此，这些索引节点对象保存在RAM中，并能够借助相应的目录项快速引用它们。

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

## imap, bmap

文件系统 imap：inode 节点位图(inodemap)管理空闲inode

摘取自骏马金龙的第4章ext文件系统机制原理剖析

在写文件(Linux中一切皆文件)时需要为其分配一个inode号。

其实，在格式化创建文件系统后，所有的inode号都已计算好（创建文件系统时会为每个块组计算好该块组拥有哪些inode号），因此产生了问题：要为文件分配哪一个inode号呢？又如何知道某一个inode号是否已经被分配了呢？

既然是"是否被占用"的问题，使用位图是最佳方案，像bmap记录block的占用情况一样。标识inode号是否被分配的位图称为inodemap简称为imap。这时要为一个文件分配inode号只需扫描imap即可知道哪一个inode号是空闲的。

这样理解更容易些，类似 bmap 块位图 一样，inode号是预先规划好的。inode号分配后，文件删除也会释放inode号。分配和释放的inode号，像是在一个地图上挖掉一块，用完再补回来一样。

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

<https://zhuanlan.zhihu.com/p/69289429>
>https://blog.51cto.com/u_15265005/2888316
>https://blog.csdn.net/wh8_2011/article/details/49883411


文件系统
​ 关于文件系统的三个易混淆的概念：后续我们逐一对三个概念进行澄清。

创建 以某种方式格式化磁盘的过程就是在其之上建立一个文件系统的过程。创建文件系统时，会在磁盘的特定位置写入 关于该文件系统的控制信息。

注册 向内核报到，声明自己能被内核支持。一般在编译内核的时侯注册；也可以加载模块的方式手动注册。注册过程实 际上是将表示各实际文件系统的数据结构struct file_system_type 实例化。

挂载 也就是我们熟悉的mount操作，将文件系统加入到Linux的根文件系统的目录树结构上；这样文件系统才能被访问。

文件系统创建
​ 以某种方式格式化磁盘的过程就是在其之上建立一个文件系统的过程。创建文件系统时，会在磁盘的特定位置写入 关于该文件系统的控制信息。用指定文件系统格式话磁盘分区后。

文件系统的注册
​ 文件系统注册就是文件系统向内核报到，声明该文件系统能被内核支持，一般是在内核的初始化阶段完成。或者在文件系统内核模块的（KO）初始化函数中完成注册。

挂载(安装)文件系统
​ 文件系统加入到Linux的根文件系统的目录树结构上，这样文件系统上面的文件才能被访问。

## 文件系统存取文件

1. 根据文件名，通过 Directory 的对应 关系，找到文件对应 的 inode number
2. 再根据  inode 读取到文件的 inode table.
3. 再根据 inode table 中的 pointer 读取到相应 的block

inode number 在单个磁盘分区中是唯一的.

