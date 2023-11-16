---
title: ext4 的"打洞"功能 (punch hole) , 稀疏文件
author: "-"
date: 2011-12-18T08:16:49+00:00
url: ext4
categories:
  - filesystem
tags:
  - reprint
---
## ext4 的"打洞"功能 (punch hole) , 稀疏文件

Linux 中有一种文件叫做 sparse file，它可以延迟分配磁盘空间，类似于我们用的虚拟机，在创建虚拟机的时候，可以分配20G的磁盘空间，但是你创建完后，去查看宿主机磁盘占用，确实际没有占用那么多。

### 稀疏文件 (Sparse File)

Sparse files are common in Linux/Unix and are also supported by Windows (e.g. NTFS) and macOSes (e.g. HFS+). Sparse files uses storage efficiently when the files have a lot of holes (contiguous ranges of bytes having the value of zero) by storing only metadata for the holes instead of using real disk blocks. They are especially in case like allocating VM images.
稀疏文件 (Sparse File) 是一种计算机文件，是UNIX类和NTFS等文件系统的一个特性。它的原理是当用户需要申请一块很大的存储空间时，此时文件系统为了节省存储资源，提高资源利用率，不会分配实际存储空间，只有真正写入数据时，操作系统才一点一点地分配空间，以64KB为单位增量增长 (不同文件系统不同) 。它最经典的应用就是为虚拟机创建虚拟硬盘 (thin provision) 和数据库快照，以及日志文件和科学应用中

一个文件的长度和它实际所占用的磁盘空间很可能是不同的，这主要涉及到稀疏文件(sparse file)和文件打洞(hole punching)的概念。这两个特性需要操作系统和文件系统的支持，目前Linux的 ext4, XFS 等文件系统都支持这两个特性。

#### 创建稀疏文件

```bash
dd of=foo.bin bs=1k seek=5120 count=0
```

#### 查看

```bash
du --block-size=1 sparse-file
ls -l sparse-file
ls -slh sparse-file
```

了解系数文件最直观的例子是，创建一个文件，然后用lseek定位到较大的偏移量，在这个偏移量实际写一些内容，这时实际占用的磁盘空间很小，但文件的长度却比较大。比如

```bash
#include <fcntl.h>
#include 

int main()
{
    // 打开两个文件file_normal和file_sparse
    int fd = open("file_normal", O_RDWR|O_CREAT, 0755);
    int fd_sparse = open("file_sparse", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);

    // 一个从0写入3个字节，一个从1000偏移写入3个字节
    lseek(fd, 0, SEEK_SET);
    lseek(fd_sparse, 100000, SEEK_SET);
    write(fd, "ABCDEFG", 3);
    write(fd_sparse, "ABCDEFG", 3);
    close(fd);
    close(fd_sparse);
    return 0;
}

#include <fcntl.h>
#include 
 
int main()
{
    // 打开两个文件file_normal和file_sparse
    int fd = open("file_normal", O_RDWR|O_CREAT, 0755);
    int fd_sparse = open("file_sparse", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
 
    // 一个从0写入3个字节，一个从1000偏移写入3个字节
    lseek(fd, 0, SEEK_SET);
    lseek(fd_sparse, 100000, SEEK_SET);
    write(fd, "ABCDEFG", 3);
    write(fd_sparse, "ABCDEFG", 3);
    close(fd);
    close(fd_sparse);
    return 0;
}
```

ls的-s选项可以在第一列打印出文件所占的磁盘空间:

zjc@~$ ./sparse_file
zjc@~$ ls -lsh file*
4.0K -rwxr-xr-x. 1 zjc zjc 3 9月 28 11:45 file_normal
4.0K -rwxr-xr-x. 1 zjc zjc 98K 9月 28 11:45 file_sparse

zjc@~$ ./sparse_file
zjc@~$ ls -lsh file*
4.0K -rwxr-xr-x. 1 zjc zjc 3 9月 28 11:45 file_normal
4.0K -rwxr-xr-x. 1 zjc zjc 98K 9月 28 11:45 file_sparse

可以看到，两个文件的长度分别为3字节和98K字节，但是占用的磁盘空间却是相同的，即文件系统的最小存储单元4 KB。这时因为file_sparse在100000偏移量前根本没有使用磁盘块。

文件打洞 (Hole Punching)
上边例子中稀疏文件，是通过在空文件中的某个偏移量写入了3个字节得到的。而某些情况下，一个文件开始并非稀疏的，它已经占用了若干的磁盘空间，这时如果文件中间的一些数据没有用了，我们为了减小文件所占用的磁盘空间，就只能通过文件打洞 (Hole Punching)的方式将非稀疏文件转为稀疏文件。

具体方法是通过fallocate系统调用。通过man 2 fallocate，我们可以看到fallocate调用的原型如下: [1]

# define _GNU_SOURCE /* See feature_test_macros(7) */
# include

int fallocate(int fd, int mode, off_t offset, off_t len);

# define _GNU_SOURCE /* See feature_test_macros(7) */
# include

int fallocate(int fd, int mode, off_t offset, off_t len);

此调用的常规用法可以称为“allocation”:  指定mode为0，此时会将文件的[offset, offset+len)区域的内容写为0。

我们要用它做文件打洞，这种用法可以对应地称为“deallocation”: 我们指定mode为FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE，这时[offset, offset+len)区域中的块就会被“打洞”，从而减小文件的磁盘占用。

正是由于fallocate系统调用的“allocation”模式将的文件的一段全置零，所以我们正好可以用这一个调用先“allocation”，再“deallocation”测试文件打洞功能。

注意: 虽然man page中写明只包含fcntl.h即可，但是在我的CentOS 7系统中还需要包含linux/falloc.h，否则会出现以下编译错误:

hole_punching.c: In function 'main':
hole_punching.c:33:25: error: 'FALLOC_FL_PUNCH_HOLE' undeclared (first use in this function)
ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
^
hole_punching.c:33:25: note: each undeclared identifier is reported only once for each function it appears in
hole_punching.c:33:46: error: 'FALLOC_FL_KEEP_SIZE' undeclared (first use in this function)
ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);

hole_punching.c: In function 'main':
hole_punching.c:33:25: error: 'FALLOC_FL_PUNCH_HOLE' undeclared (first use in this function)
ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
^
hole_punching.c:33:25: note: each undeclared identifier is reported only once for each function it appears in
hole_punching.c:33:46: error: 'FALLOC_FL_KEEP_SIZE' undeclared (first use in this function)
ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);

我们测试的例程如下:

# include <stdio.h>
# include <unistd.h>
# include <fcntl.h>
// 注意在CentOS 7中还需要包含linux/falloc.h:
# include
# include <sys/stat.h>
# include

int main()
{
    off_t offset;
    int ret;
    struct stat st;

    // do allocation
    printf("===== Allocation =====\n");
    int fd = open("./file_nohole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);

    // do dedallocation
    printf("==== Deallocation ====\n");
    fd = open("./file_withhole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);
    return 0;
}

# include <stdio.h>
# include <unistd.h>
# include <fcntl.h>
// 注意在CentOS 7中还需要包含linux/falloc.h:
# include
# include <sys/stat.h>
# include

int main()
{
    off_t offset;
    int ret;
    struct stat st;

    // do allocation
    printf("===== Allocation =====\n");
    int fd = open("./file_nohole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);
 
    // do dedallocation
    printf("==== Deallocation ====\n");
    fd = open("./file_withhole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);
    return 0;
}

运行结果:

zjc@~$ ./hole_punching
===== Allocation =====
SEEK_END offset: 1024000
fstat: file size 1024000, 2000 allocated (1024000 Bytes).
==== Deallocation ====
SEEK_END offset: 1024000
fstat: file size 1024000, 800 allocated (409600 Bytes).

zjc@~$ ls -lsh file*
1000K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_nohole
400K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_withhole

zjc@~$ ./hole_punching
===== Allocation =====
SEEK_END offset: 1024000
fstat: file size 1024000, 2000 allocated (1024000 Bytes).
==== Deallocation ====
SEEK_END offset: 1024000
fstat: file size 1024000, 800 allocated (409600 Bytes).

zjc@~$ ls -lsh file*
1000K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_nohole
400K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_withhole

可以看到无论是用struct stat中的st_blocks字段还是ls的-s选项，都告诉我们”file_withhole”这个文件被打出了一个600 KB的洞(1000 K –> 400 K)。

打洞在MySQL页压缩中的应用
在我以前的文章中曾经分析过MySQL InnoDB的透明页压缩 [2]，这种压缩机制就是基于文件打洞的。详细可以看下那篇博客，下边在简单说明下:

InnoDB以InnoDB页为单元进行存储，对于一般的情况，InnoDB页默认为16KB，文件系统默认为4KB。当InnoDB要存储一个页时，会对16KB进行压缩，压缩后大小为12KB，那么12KB到16KB之间的内容会首先被填零，然后用fallocate作“deallocation”打洞，这样额外的一个文件系统块就因压缩而被节约了；同样，若压缩后的页小于8 KB或小于4 KB，那么分别就可以节约8 KB 或 12 KB。

[1] fallocate – manipulate file space, [http://man7.org/linux/man-pages/man2/fallocate.2.html](http://man7.org/linux/man-pages/man2/fallocate.2.html)

[2] MySQL InnoDB透明页压缩的简单分析, [http://blog.jcix.top/2017-04-16/transparent_page_compression/](http://blog.jcix.top/2017-04-16/transparent_page_compression/)

### sparse 文件的传输

scp不能识别sparse文件，传输一个sparse文件时会自动填满空洞 (即预分配的空间) ，然后发送整个实际大小文件内容，这就是为啥文件会变大的原因；2)
如果需要执行远程传输，rsync命令的sparse参数支持sparse文件处理，但是有一个弊端，虽然目标文件保留了其sparse特性，节省了目标主机的存储空间，但并没有节省网络传输带宽，依然会传输3.2T的数据，rsync不能过滤掉空洞数据的传输；

使用tar命令的S参数把整个文件夹打包压缩后拷贝到目标服务器再做解压，对于数据量小的变更可以参照这个；

cp命令能够自动探测文件是否为sparse文件，空洞数据不会拷贝，并且能够保留sparce文件副本的稀疏性质。在本次变更中，可以在源目标服务器上挂载一块磁盘，执行cp复制后再将这块磁盘挂载到目标服务器中。

---

最近看ext4代码，注意到了 punch hole  (打洞) 功能，就是可以把文件中间的一部分内容释放掉，但是剩余部分的文件偏移不变。

于是我问马涛同学这个punch hole一般用在什么场合。

马涛: 可以用在虚拟机上，比如你从虚拟机里删掉了一个大文件，虚拟机可以用 punch hole 在虚拟硬盘把这个文件占用的空间释放掉

我: 有哪款虚拟机这样做？

马涛: 这是文件系统提供给虚拟机的一个feature，虚拟机有了这个feature的支持就可以节省硬盘空间。比如 host 上装了多台虚拟机, 每个虚拟机都通过punch hole 的方式来删除自己虚拟的大文件，这样一段时间后，虽然各虚拟硬盘加起来空间很大，但是实际占用的空间就很小。应该有虚拟机是这样做的，这个我没注意。
  
我: 除了虚拟化呢？还有别的应用场景吗？

马涛: 嗯....云计算应该也又用的吧

我: 虚拟化，云计算，这都是新概念，早期做这个punch hole是干啥用的，就是早期的应用有吗？

马涛: ....早期就是因为有了truncate来去掉文件的尾巴，那么出于逻辑完整，就需要一个调用来去掉文件的头或者中间，于是就有了这个punch hole

我: 喔

事后我想了想，如果一个大文件，用户决定了文件中间的一段内容以后不需要再用到了可以删除了，在没有punch hole支持的情况下，似乎只能先mmap，然后 memove 把中间的内容覆盖掉, 然后truncate缩短文件内容. 而如果有了punch hole的支持, 只需一个系统调用没有内存移动的开销，非常高效，虽然文件用 ls 看起来还是那么大，但实际占用空间 (用 du -sh 看)  已经缩短了。

也许数据库，搜索引擎里的大文件可以用上，我猜。

---

[http://donghao.org/2011/07/ext4aoaupunch-hole.html](http://donghao.org/2011/07/ext4aoaupunch-hole.html)  
[http://blog.jcix.top/2018-09-28/hole_punching/](http://blog.jcix.top/2018-09-28/hole_punching/)  

---------------------
原文来自【学领未来】，转载时请保留原文链接。
链接: [http://bbs.learnfuture.com/topic/7650](http://bbs.learnfuture.com/topic/7650)

---

[http://blog.csdn.net/shenlanzifa/article/details/44016537](http://blog.csdn.net/shenlanzifa/article/details/44016537)

我们知道lseek()系统调用可以改变文件的偏移量，但如果程序调用使得文件偏移量跨越了文件结尾，然后再执行I/O操作，将会发生什么情况？ read()调用将会返回0，表示文件结尾。令人惊讶的是，write()函数可以在文件结尾后的任意位置写入数据。在这种情况下，对该文件的下一次写将延长该文件，并在文件中构成一个空洞，这一点是允许的。从原来的文件结尾到新写入数据间的这段空间被成为文件空洞。调用write后文件结尾的位置已经发生变化。

在Linux系统之中，文件结束符EOF根本不是一个字符，而是当系统读取到文件结尾，所返回的一个信号值 (也就是-1) ，至于系统怎么知道文件的结尾，资料上说是通过比较文件的长度。

文件空洞占用任何磁盘空间，直到后续某个时点，在文件空洞中写入了数据，文件系统才会为之分配磁盘块。空洞的存在意味着一个文件名义上的大小可能要比其占用的磁盘存储总量要大 (有时大出许多) 。向文件空洞中写入字节，内核需要为其分配存储单元，即使文件大小不变，系统的可用磁盘空间也将减少。这种情况并不常见，但也需要了解。

下面看一个例子:  (转自[http://blog.csdn.NET/wangxiaoqin00007/article/details/6617801](http://blog.csdn.NET/wangxiaoqin00007/article/details/6617801))
  
ls -l file 查看文件逻辑大小
  
du -c file 查看文件实际占用的存储块多少
  
od -c file 查看文件存储的内容

空洞文件就是有空洞的文件,在日常的常识中,我们使用的文件存放在硬盘分区上的时候,有多大的内容就会占用多大的空间,比如这个文本文件里面写有1000个asc字符,那么就会占用磁盘上1000B的存储空间,为了便于管理文件,文件系统都是按块大小来分配给文件的,假如这个文件系统一个块是4096的话,那么这个文件就会占用一个块的,无论实际的内容是1B还是4000B.如果我们有一个4MB的文件,那么它会在分区中占用:4MB/4096B=1000个块.
  
现在我们先做一个实际的无空洞文件来看看:
  
# dd if=/dev/urandom of=testfile1 bs=4096 count=1000
  
这个命令会从/dev/urandom文件复制1000个块,每块大小4096,到testfile1文件去.
  
好了,我们已经有了testfile1这么一个4M的文件了,里面填充了一些随机的内容,你可以more一下.
  
然后用ls -l查看这个文件的大小是4096000,用du -h testfile1来查看的话,文件占用的磁盘大小是4M,两者是一样的.

下来是我们的重点,空洞文件,假如我们有一个文件,它有4M的大小,但是它里边很大一部分都是没有存放数据的,这样可不可以呢?试一下:
  
# dd if=/dev/urandom of=testfile2 bs=4096 seek=999 count=1
  
这个命令跟前一个命令相似,不同的是,它其实复制了1个块的内容,前面的999个块都跳过了.
  
我们ls -l一下,发现文件的大小还是4096000,用du -h testfile2查看,占用的块大小是4K
  
我们发现,虽然文件是4M,但是实际在磁盘上只占用了4K的大小,这就是空洞文件的神奇之处.

实际中的空洞文件会在哪里用到呢?常见的场景有两个:
  
一是在下载电影的时候,发现刚开始下载,文件的大小就已经到几百M了.
  
二是在创建虚拟机的磁盘镜像的时候,你创建了一个100G的磁盘镜像,但是其实装起来系统之后,开始也不过只占用了3,4G的磁盘空间,如果一开始把100G都分配出去的话,无疑是很大的浪费.

然后讲一下底层的实现吧,其实这个功能关键得文件系统支持,貌似FAT就不可以吧,linux下一直都很好的支持这一特性,我们举个最简单的ext的例子吧,ext中记录文件实际内容的对应信息的东西是一个叫索引表的东西,里面有十几个条目,每个条目存放对应文件内容块的块号,这样就可以顺序找到对应的文件内容了,大家可能说,几M的一个文件,十几个项哪够啊,不必担心,一般索引表前面几个项目是直接指向文件内容的,如果这几个不够的话,往后的第一个项目不会指向文件内容块,而会指向一个存放项目的块,这样一下多出N个项目来,如果这样还不够,下面的那个是存放指向指向的项目,不好意思,我也绕晕了,总之,前面的是直接指向,下面这个是二级指向,再下面的是二级指向,以此类推,这样,文件系统就可以处理T数量级别的文件,看下图:

到了空洞文件这里呢,我们只需要把指向没有文件内容部分的索引项目置NULL就好了,这样就不会指向实际的数据块了,也不会占用磁盘空间了,就这么easy~
  
至于btrfs这些新一代文件系统呢,在空洞文件这里的原理跟ext还是类似的.
  
最后介绍一下linux对空洞文件的处理,经过我最近的一些测试所得:
  
在同一文件系统ext4下,cat一个空洞文件到新文件,新文件不再是空洞文件,cp一个空洞文件到新文件,新文件仍然是空洞文件.
  
在btrfs跟ext4之间做的结果同上面是一致的,但是在不同文件系统之间cp,因为不同文件系统分配的最小单元不同,所以du结果会不同.
  
在nfs的客户端下,在nfs目录下去cp,新文件仍然是空洞文件!!!但是cp会逐个的去比较文件的内容,所以,受网络状况搞得影响,过程有时候会很慢.

## 查看文件是否是 sparse file

```bash
find foo.bar -type f -printf "%S\t%p\n"

```

如上，通过 find 命令，find 命令通过 %S 输出的结果中，最左边一列显示的值是（BLOCK-SIZE*st_blocks/st_size），sparse file 的大小通常是小于 1.0 的。
