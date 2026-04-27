---
title: inode
author: "-"
date: 2026-04-27T11:17:51+08:00
url: inode
categories:
  - Linux
tags:
  - file
  - remix
  - AI-assisted

---
## inode

>An inode stores all the information about a regular file, directory, or other file system object, except its data and name.

每个文件都对应一个 inode, inode 存储了除文件名和文件内容之外的所有信息。

inode (发音: eye-node) 译成中文就是索引节点, 它用来存放文件和目录的基本信息, 包含时间、档名、使用者，群组，权限， 一个文件占用一个inode,同时记录此文件的数据所在的 block 号码；

[http://www.ruanyifeng.com/blog/2011/12/inode.html](http://www.ruanyifeng.com/blog/2011/12/inode.html)

inode是什么？

inode是一个重要概念, 是理解 Unix/Linux 文件系统和硬盘储存的基础。

我觉得,理解 inode, 不仅有助于提高系统操作水平, 还有助于体会 Unix 设计哲学, 即如何把底层的复杂性抽象成一个简单概念, 从而大大简化用户接口。

下面就是我的inode学习笔记,尽量保持简单。

理解inode

作者: 阮一峰

## inode是什么？

Inode 用于存储文件或目录的信息.

理解inode, 要从文件储存说起。

## 扇区 (Sector)

文件储存在硬盘上, 硬盘的最小存储单位叫做"扇区" (Sector) 。每个扇区储存 512 字节。（现在新的硬盘每个扇区有4K）

注意：硬盘的最小存储单位就是扇区了，而且硬盘本身并没有 block 的概念。

文件系统不是一个扇区一个扇区的来读数据，太慢了，所以有了 block（块）的概念，它是一个块一个块的读取的，block 才是文件存取的最小单位。

文件数据存储在硬盘上，硬盘的最小存储单位叫做"扇区"（512Bytes）。OS读取硬盘的时候，为了提高效率会一次性读取一个"块"（8*扇区=4K）。所以一个大文件的数据内容在磁盘上可能不是连续空间的，就需要inode来把各个Block串联起来。

操作系统读取硬盘的时候, 不会一个个扇区地读取, 这样效率太低, 而是一次性连续读取多个扇区, 即一次性读取一个"块" (block) 。这种由多个扇区组成的"块", 是文件存取的最小单位。"块"的大小,最常见的是 4KB, 即连续八个 sector 组成一个 block。

文件数据都储存在"块"中, 那么很显然, 我们还必须找到一个地方储存文件的元信息, 比如文件的创建者、文件的创建日期、**文件的大小**等等。 这种储存文件元信息的区域就叫做 inode, 中文译名为"索引节点"。

每一个文件都有对应的 inode, 里面包含了与该文件有关的一些信息。

### inode 的内容  

inode 包含文件的元信息(meta data), 每个文件都对应一个 inode，inode 存储了除**文件名**和**文件内容**之外的所有信息。

- 文件的长度/size (字节数)
- 文件拥有者的 User ID
- 文件的 Group ID
- 文件类型和文件的读、写、执行权限
- 文件的时间戳, 共有三个: ctime 指 inode 上一次变动的时间, mtime指文件内容上一次变动的时间, atime指文件上一次打开的时间。
- 链接/link 数, 即有多少文件名指向这个 inode
- 存储位置指针, 文件的 data block 的位置

### 可以用 stat 命令,查看某个文件的 inode 信息

    stat foo.txt

总之,除了文件名以外的所有文件信息, 都存在 inode 之中。至于为什么没有文件名,下文会有详细解释。

三、inode 的大小

inode 也会消耗硬盘空间,所以硬盘格式化的时候,操作系统自动将硬盘分成两个区域。一个是数据区,存放文件数据；另一个是inode区 (inode table) ,存放inode所包含的信息。

每个inode节点的大小,一般是128字节或256字节。inode节点的总数,在格式化时就给定(现代OS可以动态变化),一般是每1KB或每2KB就设置一个inode。假定在一块1GB的硬盘中,每个inode节点的大小为128字节,每1KB就设置一个inode,那么inode table的大小就会达到128MB,占整块硬盘的12.8%。

查看每个硬盘分区的inode总数和已经使用的数量,可以使用df命令。

df -i
查看每个inode节点的大小,可以用如下命令:

sudo dumpe2fs -h /dev/hda | grep "Inode size"

由于每个文件都必须有一个inode,因此有可能发生inode已经用光,但是硬盘还未存满的情况。这时,就无法在硬盘上创建新文件。

四、inode号码

每个inode都有一个号码,操作系统用inode号码来识别不同的文件。

### 文件名

这里值得重复一遍, Unix/Linux系统内部不使用文件名,而使用inode号码来识别文件。对于系统来说,文件名只是 inode 号码便于识别的别称或者绰号。

表面上,用户通过文件名,打开文件。实际上,系统内部这个过程分成三步: 首先,系统找到这个文件名对应的inode号码；其次,通过inode号码,获取inode信息；最后,根据inode信息,找到文件数据所在的block,读出数据。

使用ls -i命令,可以看到文件名对应的inode号码:

ls -i example.txt

linux的文件名是保存在目录文件上的,

文档信息
版权声明: 自由转载-非商用-非衍生-保持署名 (创意共享3.0许可证)
发表日期:  2011年12月 4日
[https://www.ruanyifeng.com/blog/2011/12/inode.html](https://www.ruanyifeng.com/blog/2011/12/inode.html)

#### 目录文件

Unix/Linux系统中,目录 (directory) 也是一种文件。打开目录,实际上就是打开目录文件。

目录文件的结构非常简单,就是一系列目录项 (dirent) 的列表。每个目录项,由两部分组成: 所包含文件的**文件名**,以及该文件名对应的 **inode**。

ls 命令只列出目录文件中的所有文件名:

ls /etc

ls -i 命令列出整个目录文件,即文件名和inode

ls -i /etc

如果要查看文件的详细信息,就必须根据inode号码,访问inode节点,读取信息。ls -l命令列出文件的详细信息。

ls -l /etc

理解了上面这些知识,就能理解目录的权限。目录文件的读权限 (r) 和写权限 (w) ,都是针对目录文件本身。由于目录文件内只有文件名和inode号码,所以如果只有读权限,只能获取文件名,无法获取其他信息,因为其他信息都储存在inode节点中,而读取inode节点内的信息需要目录文件的执行权限 (x) 。

## 硬链接, hard link

硬链接在硬盘中是同一个 inode 存在，在目录文件中多了一个目录和该 inode 对应。links 数 增加， link 数可以用命令 stat 查看，如 stat foo.txt

### 硬链接特性

硬链接不能跨本地文件系统
硬链接不能针对目录

一般情况下,文件名和 inode 是**一一对应**关系, 每个 inode 对应一个文件名。但是, Unix/Linux系统允许, 多个文件名指向同一个inode。

这意味着,可以用不同的文件名访问同样的内容；对文件内容进行修改,会影响到所有文件；但是,删除一个文件名, 不影响另一个文件名的访问。这种情况就被称为"硬链接" (hard link) 。

ln命令可以创建硬链接:

    ln 源文件 目标文件

运行上面这条命令以后,源文件与目标文件的inode号码相同,都指向同一个inode。inode信息中有一项叫做"链接数",记录指向该inode的文件名总数,这时就会增加1。

反过来,删除一个文件名,就会使得inode节点中的"链接数"减1。当这个值减到0,表明没有文件名指向这个inode,系统就会回收这个inode号码,以及其所对应block区域。

这里顺便说一下目录文件的"链接数"。创建目录时,默认会生成两个目录项: "."和".."。前者的inode号码就是当前目录的inode号码,等同于当前目录的"硬链接"；后者的inode号码就是当前目录的父目录的inode号码,等同于父目录的"硬链接"。所以,任何一个目录的"硬链接"总数,总是等于2加上它的子目录总数 (含隐藏目录) 。

### 软链接, 符号链接, symbolic link, symlink

除了硬链接，linux 系统还提供了一种符号链接。符号链接并不增加目标文件 i 节点的链接数。符号链接本身也是一个文件，其中存储了目标文件的完整路径，类似于windows系统中的快捷方式。符号链接与硬链接的另一个区别是符号链接可以对目录建立链接，而硬链接不能对目录建立链接。因为如果允许对目录建立硬链接，有可能形成链接环。

文件 A 和文件 B 的 inode 号码虽然不一样, 但是文件 A 的内容是文件B的路径。 读取文件 A 时, 系统会自动将访问者导向文件 B 。 因此, 无论打开哪一个文件, 最终读取的都是文件 B 。 这时, 文件 A 就称为文件 B 的 "软链接" ( soft link ) 或者" 符号链接 ( symbolic link ) 。

这意味着, 文件 A 依赖于文件 B 而存在, 如果删除了文件 B, 打开文件A就会报错: "No such file or directory"。这是软链接与硬链接最大的不同: 文件A指向文件B的文件名,而不是文件B的inode号码,文件B的inode"链接数"不会因此发生变化。

ln -s 命令可以创建软链接。

ln -s 源文文件或目录 目标文件或目录

八、inode 的特殊作用

由于inode号码与文件名分离,这种机制导致了一些Unix/Linux系统特有的现象。

1. 有时,文件名包含特殊字符,无法正常删除。这时,直接删除inode节点,就能起到删除文件的作用。

2. 移动文件或重命名文件,只是改变文件名,不影响inode号码。

3. 打开一个文件以后,系统就以inode号码来识别这个文件,不再考虑文件名。因此,通常来说,系统无法从inode号码得知文件名。

第3点使得软件更新变得简单,可以在不关闭软件的情况下进行更新,不需要重启。因为系统通过inode号码,识别运行中的文件,不通过文件名。更新的时候,新版文件以同样的文件名,生成一个新的inode,不会影响到运行中的文件。等到下一次运行这个软件的时候,文件名就自动指向新版文件,旧版文件的inode则被回收

#### 怎么判断是软链接还是硬链接

软链接可以用 ls -l 查看， 软连接开头是l, 文件名显示时有“->”指向  
硬链接是无法判断的，前后两个文件地位是相等的，没有谁是谁的硬链接的说法

硬链接和源文件的 i节点号是一样的，可以用下面的的命令查看，但是你也不能区分哪个是源文件，哪个是硬链接，因为他们地位是相等的，只能看出这个文件创建了硬链接

    ls -li

硬链接不能跨文件系统，不能作用于目录。多个文件同时指向一个inode号。
软连接可以跨文件系统，可以作用于目录和文件。

### 目录

在Linux操作系统中,目录就是目录文件。目录项中存放文件名和一个指向inode的指针。  
一个目录项主要包括了文件名和inode,索引节点号是指向inode表( system inode table )中对应的索引节点的。  
[https://unix.stackexchange.com/questions/117325/where-are-filenames-stored-on-a-filesystem](https://unix.stackexchange.com/questions/117325/where-are-filenames-stored-on-a-filesystem)

[https://zhuanlan.zhihu.com/p/143430585](https://zhuanlan.zhihu.com/p/143430585)

[https://www.h5w3.com/84540.html](https://www.h5w3.com/84540.html)

[https://www.jianshu.com/p/d60a2b44e78e](https://www.jianshu.com/p/d60a2b44e78e)

[https://www.leftpocket.cn/post/linux/cp/](https://www.leftpocket.cn/post/linux/cp/)

## inode 文件权限和类型

[https://man7.org/linux/man-pages/man7/inode.7.html](https://man7.org/linux/man-pages/man7/inode.7.html) > The file type and mode

## inode 在硬盘上是什么

inode 不是一个文件，它是硬盘上的一块**固定大小的数据结构**（通常 256 字节），存放在专门划分的 inode table 区域里。

inode table 就是一个连续的二进制数组，没有文件的概念，就像内存里的一个数组，第 N 个槽位就是第 N 号 inode 的数据。

以 ext4 为例，硬盘分区的布局：

```
硬盘分区
├── 超级块 (superblock)        ← 记录整个文件系统的元信息
├── inode 区 (inode table)     ← 存放所有 inode，每个 256 字节
│   ├── inode #1  (根目录)
│   ├── inode #2  (某个文件)
│   └── ...
└── 数据区 (data blocks)       ← 存放文件的实际内容
    ├── block #0
    ├── block #1
    └── ...
```

## 读文件时如何定位数据边界

inode 里存的不只是"指针"，而是**这个文件所有 block 的地址列表**加上文件大小。读文件时内核知道：

- 从哪些 block 读（地址列表）
- 读多少字节（文件大小字段）

ext4 的 inode 用多级指针描述 block 列表：

```
inode
├── 文件大小: 12345 字节        ← 决定"在哪里结束"
├── 直接指针 × 12              → block 地址（直接存数据）
├── 一级间接指针               → 指向一个 block，该 block 里存 block 地址列表
├── 二级间接指针               → 指向地址列表的列表
└── 三级间接指针               → 再嵌套一层
```

现代 ext4 实际上用 **extent** 替代了多级指针，用 `(起始block, 长度)` 描述连续区域，更高效，但原理相同。

## inode 在不同文件系统中的差异

inode 是 Unix/Linux VFS（虚拟文件系统）层的抽象概念，具体存储方式完全取决于底层文件系统：

- **ext2/ext3/ext4**：格式化时预分配固定数量的 inode，存放在专门的 inode table 区域；inode 总数固定，可能出现"inode 用完但磁盘还有空间"的情况
- **XFS**：按需动态分配 inode，不预先占满空间
- **btrfs**：inode 作为普通的 B-tree 节点存储，没有独立的 inode table，理论上 inode 数量无上限
- **FAT32/exFAT**：根本没有 inode 概念，文件元数据直接存在目录项里
- **NTFS**：用 MFT（Master File Table）替代 inode table，概念类似但实现不同
- **NFS/CIFS**：inode 号由服务端文件系统决定，客户端看到的是映射值，可能不稳定

## 进程关闭后内核何时释放磁盘空间

进程关闭文件描述符时（`close()` 系统调用，或进程退出时内核自动关闭所有 fd），内核立即执行：

```
进程调用 close(fd) 或进程退出
  → 内核将该 inode 的引用计数 - 1
  → 检查引用计数是否为 0
      ├── 不为 0 → 什么都不做
      └── 为 0  → 立即释放：
                   1. 将 inode 占用的所有 data block 标记为空闲（写入 block bitmap）
                   2. 将 inode 本身标记为空闲（写入 inode bitmap）
                   3. 更新超级块中的空闲计数
```

bitmap 的修改会先写到内核的 page cache，由 writeback 线程在几秒内刷到硬盘，但 `df` 命令马上就能看到空间增加，因为内存中 bitmap 已经更新。

## 非正常关机与 journal

非正常关机（断电）可能导致内核已决定释放某个 inode 的 blocks，但 bitmap 修改还在 page cache 里没刷盘，重启后这些修改丢失，硬盘上的 bitmap 仍然显示那些 block 是"已占用"。

ext4 通过日志（journal）解决这个问题。每次元数据修改先写到 journal 区域：

```
修改元数据
  → 写 journal record 到硬盘
  → 写 commit block（标志事务完整）
  → 修改实际的 inode table / bitmap（异步刷盘）
  → journal 记录标记为可复用
```

重启时内核检查 journal：

- commit block 已写入 → 重放这条 journal，修复元数据
- commit block 未写入 → 丢弃这条 journal，操作整体回滚

commit block 的写入是可信的，因为硬盘的单个扇区写入是原子的（要么写完，要么不写）。

## orphan inode：升级共享库后断电的场景

以升级 `libexpat.so` 为例，pacman 删除旧目录项后，若此时有进程还打开着旧文件，旧 inode 的 link count 降为 0 但 open count > 0。ext4 会立即将该 inode 号写入超级块里的 **orphan list**（通过 journal 落盘）：

```
pacman 删除旧目录项
  → 旧 inode link count = 0，open count > 0
  → ext4 把旧 inode 号写入 orphan list（落盘）
  → 正常情况：进程退出 → 释放 blocks，从 orphan list 移除
  → 断电情况：orphan list 保留在硬盘上
```

重启时内核挂载 ext4 会检查 orphan list，发现 link count = 0、无人打开的 inode，立即释放其 data blocks 并从 orphan list 移除。整个过程对用户不可见，不会造成磁盘空间永久泄漏。
