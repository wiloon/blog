---
author: "-"
date: "2020-11-02 15:57:36" 
title: "IO同步函数: sync, fsync, fdatasync"
categories:
  - inbox
tags:
  - reprint
---
## "IO同步函数: sync, fsync, fdatasync"
## IO同步函数: sync、fsync、fdatasync
传统的UNIX或LINUX系统实现在内核中设有缓冲区高速缓存或页面高速缓存，大多数磁盘I/O都通过缓冲进行。当将数据写入文件时，内核通常先将该数据复制到其中一个缓冲区中，如果该缓冲区尚未写满，则并不将其排入输出队列，而是等待其写满或者当空闲内存不足内核需要重用该缓冲区以便存放其他磁盘块数据时，再将该缓冲排入输出队列，然后待其到达队首时，才进行实际的I/O操作。这种输出方式被称为延迟写 (delayed write) 。

当调用 write() 函数写出数据时，数据一旦写到该缓冲区 (仅仅是写到缓冲区) ，函数便马上返回。此时写出的数据能够用read()读回，也能够被其它进程读到，可是并不意味着它们已经被写到了外部永久存储介质上。即使调用close()关闭文件后也可能如此，由于缓冲区的数据可能还在等待输出。因此。从数据被实际写到磁盘的角度来看。用write()写出的文件数据与外部存储设备并非全然同步的。不同步的时间间隔非常短，一般仅仅有几秒或十几秒，详细取决于写出的数据量和I/O数据缓冲区的状态。虽然不同步的时间间隔非常短，可是假设在此期间发生掉电或者系统崩溃，则会导致所写数据来不及写至磁盘而丢失的情况。

注意: 内核将缓冲区中的数据"写"到标准输入磁盘文件里，这里"写"不是将缓冲区中的数据移动到磁盘文件里，而是复制到磁盘文件里，也就说此时缓冲区内容还没有被清除。做出这一设计也是有其道理的，假设写出到磁盘文件上，磁盘坏了或满了等等，总之就是无法将数据送出，假如缓冲区内容被清除，那数据就丢掉了。也就是说内核会等待写入磁盘动作完毕后，才放心的将缓冲区的数据删除掉。

延迟写减少了磁盘写次数，但是却降低了文件内容的更新速度，使得欲写到文件中的数据在一段时间内并没有写到磁盘上。当系统发生故障时，这种延迟可能造成文件更新内容的丢失。为了保证磁盘上实际文件系统与缓冲区高速缓存中内容的一致性，UNIX系统提供了 sync、fsync 和 fdatasync 三个函数:
### sync
sync 函数只是将所有修改过的块缓冲区加入写队列，然后就返回，它并不等待实际写磁盘操作结束。所以不要觉得调用了sync 函数，就觉得数据已安全的送到磁盘文件上，有可能会出现故障，可是 sync 函数是无法得知的.通常称为 update 的系统守护进程会周期性地 (一般每隔30秒) 调用 sync 函数。这就保证了定期冲洗内核的块缓冲区。命令 sync(1) 也调用 sync 函数。sync是全局的，对整个系统都 flush。

### fsync
fsync 函数只针对单个文件，只对由文件描述符 filedes 指定的单一文件起作用，并且等待写磁盘操作结束，然后返回。fsync 不仅会同步更新文件数据，还会同步更新文件的属性 (比如 atime,mtime 等) 。fsync 可用于数据库这样的应用程序，这种应用程序需要确保将修改过的块立即写到磁盘上。

### fdatasync
fdatasync 当初设计是考虑到有特殊的时候一些基本的元数据比如 atime，mtime 这些不会对以后读取造成不一致性，因此少了这些元数据的同步可能会在性能上有提升。该函数类似于 fsync，但它只影响文件的数据部分, 如果该写操作并不影响读取刚写入的数据，则不需等待文件属性被更新。
对于提供事务支持的数据库，在事务提交时，都要确保事务日志 (包含该事务所有的修改操作以及一个提交记录) 完全写到硬盘上，才认定事务提交成功并返回给应用层。

---

一个简单的问题: 在*nix操作系统上，怎样保证对文件的更新内容成功持久化到硬盘？
1. write不够，需要 fsync
一般情况下，对硬盘 (或者其他持久存储设备) 文件的write操作，更新的只是内存中的页缓存 (page cache) ，而脏页面不会立即更新到硬盘中，而是由操作系统统一调度，如由专门的 flusher 内核线程在满足一定条件时 (如一定时间间隔、内存中的脏页达到一定比例) 内将脏页面同步到硬盘上 (放入设备的IO请求队列) 。
因为 write 调用不会等到硬盘IO完成之后才返回，因此如果OS在write调用之后、硬盘同步之前崩溃，则数据可能丢失。虽然这样的时间窗口很小，但是对于需要保证事务的持久化 (durability) 和一致性 (consistency) 的数据库程序来说，write()所提供的"松散的异步语义"是不够的，通常需要OS提供的同步IO (synchronized-IO) 原语来保证: 

#include <unistd.h>
int fsync(int fd);
fsync的功能是确保文件fd所有已修改的内容已经正确同步到硬盘上，该调用会阻塞等待直到设备报告IO完成。

PS: 如果采用内存映射文件的方式进行文件IO (使用mmap，将文件的page cache直接映射到进程的地址空间，通过写内存的方式修改文件) ，也有类似的系统调用来确保修改的内容完全同步到硬盘之上: 

#incude <sys/mman.h>
int msync(void *addr, size_t length, int flags)
msync需要指定同步的地址区间，如此细粒度的控制似乎比fsync更加高效 (因为应用程序通常知道自己的脏页位置) ，但实际上 (Linux) kernel中有着十分高效的数据结构，能够很快地找出文件的脏页，使得fsync只会同步文件的修改内容。

2.fsync的性能问题，与fdatasync
除了同步文件的修改内容 (脏页) ，fsync还会同步文件的描述信息 (metadata，包括size、访问时间st_atime & st_mtime等等) ，因为文件的数据和metadata通常存在硬盘的不同地方，因此fsync至少需要两次IO写操作，fsync的man page这样说: 
"Unfortunately fsync() will always initialize two write operations : one for the newly written data and another one in order to update the modification time stored in the inode. If the modification time is not a part of the transaction concept fdatasync() can be used to avoid unnecessary inode disk write operations."

多余的一次IO操作，有多么昂贵呢？根据Wikipedia的数据，当前硬盘驱动的平均寻道时间 (Average seek time) 大约是3~15ms，7200RPM硬盘的平均旋转延迟 (Average rotational latency) 大约为4ms，因此一次IO操作的耗时大约为10ms左右。这个数字意味着什么？下文还会提到。

Posix同样定义了fdatasync，放宽了同步的语义以提高性能: 

#include <unistd.h>
int fdatasync(int fd);
fdatasync的功能与fsync类似，但是仅仅在必要的情况下才会同步metadata，因此可以减少一次IO写操作。那么，什么是"必要的情况"呢？根据man page中的解释: 
"fdatasync does not flush modified metadata unless that metadata is needed in order to allow a subsequent data retrieval to be corretly handled."
举例来说，文件的尺寸 (st_size) 如果变化，是需要立即同步的，否则OS一旦崩溃，即使文件的数据部分已同步，由于metadata没有同步，依然读不到修改的内容。而最后访问时间(atime)/修改时间(mtime)是不需要每次都同步的，只要应用程序对这两个时间戳没有苛刻的要求，基本无伤大雅。

函数open的参数O_SYNC/O_DSYNC有着和fsync/fdatasync类似的含义: 使每次write都会阻塞等待硬盘IO完成。
O_SYNC 使每次write等待物理I/O操作完成，包括由write操作引起的文件属性更新所需的I/O。
O_DSYNC 使每次write等待物理I/O操作完成，但是如果该写操作并不影响读取刚写入的数据，则不需等待文件属性被更新。

O_DSYNC和O_SYNC标志有微妙的区别: 
仅当文件属性需要更新以反映文件数据变化 (例如，更新文件大小以反映文件中包含了更多数据) 时，O_DSYNC标志才影响文件属性。而设置O_SYNC标志后，数据和属性总是同步更新。当文件用O_DSYN标志打开，在重写其现有的部分内容时，文件时间属性不会同步更新。于此相反，文件如果是用O_SYNC标志打开的，那么对于该文件的每一次write都将在write返回前更新文件时间，这与是否改写现有字节或追加文件无关。相对于fsync/fdatasync，这样的设置不够灵活，应该很少使用。
 (实际上，Linux对O_SYNC/O_DSYNC做了相同处理，没有满足Posix的要求，而是都实现了fdatasync的语义) 

3.使用fdatasync优化日志同步
文章开头时已提到，为了满足事务要求，数据库的日志文件是常常需要同步IO的。由于需要同步等待硬盘IO完成，所以事务的提交操作常常十分耗时，成为性能的瓶颈。
在Berkeley DB下，如果开启了AUTO_COMMIT (所有独立的写操作自动具有事务语义) 并使用默认的同步级别 (日志完全同步到硬盘才返回) ，写一条记录的耗时大约为5~10ms级别，基本和一次IO操作 (10ms) 的耗时相同。
我们已经知道，在同步上fsync是低效的。但是如果需要使用fdatasync减少对metadata的更新，则需要确保文件的尺寸在write前后没有发生变化。日志文件天生是追加型 (append-only) 的，总是在不断增大，似乎很难利用好fdatasync。

且看Berkeley DB是怎样处理日志文件的: 

1.每个log文件固定为10MB大小，从1开始编号，名称格式为"log.%010d"
2.每次log文件创建时，先写文件的最后1个page，将log文件扩展为10MB大小
3.向log文件中追加记录时，由于文件的尺寸不发生变化，使用fdatasync可以大大优化写log的效率
4.如果一个log文件写满了，则新建一个log文件，也只有一次同步metadata的开销
man手册关于fsync，fdatasync部分
fsync() transfers ("flushes") all modified in-core data of (i.e., modified buffer cache pages for) the file referred to by the file descriptor fd to the disk device (or other permanent storage device) so that all changed information can be retrieved even after the system crashed or was rebooted. This includes writing through or flushing a disk cache if present. The call blocks until the device reports that the transfer has completed. It also flushes metadata information associated with the file (see stat(2)).Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk. For that an explicit fsync() on a file descriptor for the directory is also needed.

fdatasync() is similar to fsync(), but does not flush modified metadata unless that metadata is needed in order to allow a subsequent data retrieval to be correctly handled. For example, changes to st_atime or st_mtime (respectively, time of last access and time of last modification; see stat(2)) do not require flushing because they are not necessary for a subsequent data read to be handled correctly. On the other hand, a change to the file size (st_size, as made by say ftruncate(2)), would require a metadata flush.The aim of fdatasync() is to reduce disk activity for applications that do not require all metadata to be synchronized with the disk.

Linux、unix在内核中设有缓冲区、高速缓冲或页面高速缓冲，大多数磁盘I/O都通过缓冲进行，采用延迟写技术。
sync: 将所有修改过的快缓存区排入写队列，然后返回，并不等待实际写磁盘操作结束；
fsync: 只对有文件描述符制定的单一文件起作用，并且等待些磁盘操作结束，然后返回；内核I/O缓冲区是由操作系统管理的空间，而流缓冲区是由标准I/O库管理的用户空间.fflush()只刷新位于用户空间中的流缓冲区.fflush()返回后，只保证数据已不在流缓冲区中，并不保证它们一定被写到了磁盘.此时，从流缓冲区刷新的数据可能已被写至磁盘，也可能还待在内核I/O缓冲区中.要确保流I/O写出的数据已写至磁盘，那么在调用fflush()后还应当调用fsync().
fdatasync: 类似fsync，但它只影响文件的数据部分。fsync还会同步更新文件的属性；
fflush: 标准I/O函数 (如: fread，fwrite) 会在内存建立缓冲，该函数刷新内存缓冲，将内容写入内核缓冲，要想将其写入磁盘，还需要调用fsync。 (先调用fflush后调用fsync，否则不起作用) 。
fflush()与fsync()的联系: 
内核I/O缓冲区是由操作系统管理的空间，而流缓冲区是由标准I/O库管理的用户空间.fflush()仅仅刷新位于用户空间中的流缓冲区.fflush()返回后。仅仅保证数据已不在流缓冲区中，并不保证它们一定被写到了磁盘.此时。从流缓冲区刷新的数据可能已被写至磁盘。也可能还待在内核I/O缓冲区中.要确保流I/O写出的数据已写至磁盘，那么在调用fflush()后还应当调用fsync()。

总结
1.调用系统函数write时有写延迟，write负责把东西写到缓存区上，sync负责把缓存区上的东西排到写队列中(缓冲区->写队列)，在由守护进程负责把队列里的东西写到磁盘上，而sync函数在把缓存区上的东西排到写队列后不管写队列中的内容是否写到磁盘上都立即返回。如果是对所有的缓冲区发出写硬盘的命令，应该使用sync函数，但应该注意该函数仅仅只是把该命令放入队列就返回了，在编程时需要注意。

2.fsync函数则是对指定文件的操作，而且必须等到写队列中的内容都写到磁盘后才返回，并且更新文件inode结点里的内容。如果是要把一个已经打开的文件所做的修改提交到硬盘，应调用fsync函数，该函数会在数据实际写入硬盘后才返回，因此是最安全最可靠的方式。如果是针对一个已经打开的文件流操作，则应该首先调用fflush函数把修改同步到内核缓冲区，然后再调用fsync把修改真正的同步到硬盘。

3.fdatasync和fsync类似，但是这个函数只更新data块里的内容。

参考: https://blog.csdn.net/letterwuyu/article/details/80927226