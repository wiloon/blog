---
title: 文件描述符, file descriptors, fd, 句柄
author: "-"
date: 2017-03-24T01:49:22+00:00
url: fd
categories:
  - OS
tags:
  - reprint
  - file


---
## 文件描述符, file descriptors, fd, 句柄
对文件描述符的理解一般都是从处理 "too many open files" 开始的  

### 文件描述符, file descriptors & 文件描述符表
文件描述符 (file descriptor, fd) 是linux内核对已打开文件的一个抽象标记(索引), 所有 I/O 系统调用对已打开文件的操作都要用到它。这里的 “文件” 仍然是广义的, 即除了普通文件和目录外, 还包括管道、FIFO (命名管道) 、Socket、终端、设备, 链接等。
 
文件描述符是一个非负整数 (通常是小整数) ,并且 0、1、2 三个描述符总是默认分配给标准输入、标准输出和标准错误。这就是常用的 `nohup ./my_script > my_script.log 2>&1 &` 命令里2和1的由来。如果此时去打开一个新的文件, 它的文件描述符会是3。POSIX 标准要求每次打开文件时 (含socket) 必须使用当前进程中最小可用的文件描述符号码.

所有执行I/O操作的系统调用都通过文件描述符。

每个进程都会预留3个默认的 fd: stdin(标准输入)、stdout(标准输出)、stderr(标准错误); 它们的值分别是 0, 1, 2

Integer   value	Name	      symbolic constant	file stream
0	        Standard input	  STDIN_FILENO	stdin
1	        Standard output	  STDOUT_FILENO	stdout
2	        Standard error	  STDERR_FILENO	stderr

#### 文件描述符表, file descriptors table
Linux系统中的每个进程会在其进程控制块 (PCB) 内维护属于自己的文件描述符表 (file descriptor table). 表中每个条目包含两个域: 一是控制该描述符的标记域 (flags, O_APPEND 之类的flag) ,二是指向系统级别的打开文件表中对应条目的指针。那么打开文件表又是什么呢？

#### 打开文件表, file table,open file table  & 文件句柄
file table是全局唯一的表，由系统内核维护。这个表记录了所有进程打开的文件的状态(是否可读、可写等状态)，同时它也映射到 inode table 中的entry。

内核会维护系统内所有打开的文件及其相关的元信息,该结构称为打开文件表 (open file table) 。表中每个条目包含以下域: 

- 文件的偏移量。POSIX API 中的read()/write()/lseek()函数都会修改该值；
- 打开文件时的状态和权限标记。通过 open() 函数的参数传入；
- 文件的访问模式 (只读、只写、读+写等) 。通过open()函数的参数传入；
- 指向其对应的 inode 对象的指针。内核也会维护系统级别的 inode 表 (inode table), 关于inode的细节请参考这篇文章。 <https://www.jianshu.com/p/d60a2b44e78e>
- 文件描述符表、打开文件表、inode表之间的关系可以用书中的下图来表示。注意图中的fd 0、1、2...只是示意下标,不代表三个标准描述符。

[![7n59f0.jpg](https://s4.ax1x.com/2022/01/12/7n59f0.jpg)](https://imgtu.com/i/7n59f0)

可见,一个打开的文件可以对应多个文件描述符 (不管是同进程还是不同进程) , 一个inode也可以对应多个打开的文件。打开文件表中的一行称为一条文件描述 (file description) ,也经常称为文件句柄 (file handle) 。

多嘴一句,“句柄”这个词在UNIX世界中并不很正式,但在Windows里遍地都是。Windows NT内核会将内存中的所有对象 (文件、窗口、菜单、图标等一切东西) 的地址列表维护成整数索引,这个整数就叫做句柄,逻辑上讲类似于“指针的指针”,感觉上还是有一些相通的地方的。

### inode table, inode 区

inode table 同样是全局唯一的，它指向了真正的文件地址 (磁盘中的位置)，每个entry全局唯一。

### 文件描述限制
在编写文件操作的或者网络通信的软件时,初学者一般可能会遇到"Too many open files"的问题。这主要是因为文件描述符是系统的一个重要资源,虽然说系统内存有多少就可以打开多少的文件描述符,但是在实际实现过程中内核是会做相应的处理的,一般最大打开文件数会是系统内存的10% (以KB来计算)  (称之为系统级限制) ,查看系统级别的最大打开文件数可以使用sysctl -a | grep fs.file-max 命令查看。与此同时,内核为了不让某一个进程消耗掉所有的文件资源,其也会对单个进程最大打开文件数做默认值处理 (称之为用户级限制) ,默认值一般是1024,使用ulimit -n命令可以查看。在Web服务器中,通过更改系统默认值文件描述符的最大值来优化服务器是最常见的方式之一,具体优化方式请查看 http://blog.csdn.net/kumu_linux/article/details/7877770

### 文件描述符和打开文件之间的关系
每一个文件描述符会与一个打开文件相对应,同时,不同的文件描述符也会指向同一个文件。相同的文件可以被不同的进程打开也可以在同一个进程中被多次打开。系统为每一个进程维护了一个文件描述符表,该表的值都是从0开始的,所以在不同的进程中你会看到相同的文件描述符,这种情况下相同文件描述符有可能指向同一个文件,也有可能指向不同的文件。具体情况要具体分析,要理解具体其概况如何,需要查看由内核维护的3个数据结构。
  
1. 进程级的文件描述符表
2. 系统级的打开文件描述符表
3. 文件系统的inode表

进程级的描述符表的每一条目记录了单个文件描述符的相关信息。
  
1. 控制文件描述符操作的一组标志。 (目前,此类标志仅定义了一个,即close-on-exec标志) 
2. 对打开文件句柄的引用

内核对所有打开的文件的文件维护有一个系统级的描述符表格 (open file description table) 。有时,也称之为打开文件表 (open file table) ,并将表格中各条目称为打开文件句柄 (open file handle) 。一个打开文件句柄存储了与一个打开文件相关的全部信息,如下所示: 
  
1. 当前文件偏移量 (调用read()和write()时更新,或使用lseek()直接修改) 
2. 打开文件时所使用的状态标识 (即,open()的flags参数) 
3. 文件访问模式 (如调用open()时所设置的只读模式、只写模式或读写模式) 
4. 与信号驱动相关的设置
5. 对该文件inode对象的引用
6. 文件类型 (例如: 常规文件、 socket 或FIFO) 和访问权限
7. 一个指针,指向该文件所持有的锁列表
8. 文件的各种属性,包括文件大小以及与不同类型操作相关的时间戳

下图展示了文件描述符、打开的文件句柄以及i-node之间的关系,图中,两个进程拥有诸多打开的文件描述符。

[![RYLGlt.png](https://z3.ax1x.com/2021/06/27/RYLGlt.png)](https://imgtu.com/i/RYLGlt)

在进程A中,文件描述符1和20都指向了同一个打开的文件句柄 (标号23) 。这可能是通过调用dup(), dup2(), 
fcntl() 或者对同一个文件多次调用了open()函数而形成的。
  
进程A的文件描述符2和进程B的文件描述符2都指向了同一个打开的文件句柄 (标号73) 。这种情形可能是在调用fork()后出现的 (即,进程A, B是父子进程关系) ,或者当某进程通过UNIX域 socket 将一个打开的文件描述符传递给另一个进程时,也会发生。再者是不同的进程独自去调用open函数打开了同一个文件,此时进程内部的描述符正好分配到与其他进程打开该文件的描述符一样。
  
此外,进程A的描述符0和进程B的描述符3分别指向不同的打开文件句柄,但这些句柄均指向i-node表的相同条目 (1976) ,换言之,指向同一个文件。发生这种情况是因为每个进程各自对同一个文件发起了open()调用。同一个进程两次打开同一个文件,也会发生类似情况。

### 总结
1. 由于进程级文件描述符表的存在, 不同的进程中会出现相同的文件描述符,它们可能指向同一个文件,也可能指向不同的文件
2. 两个不同的文件描述符,若指向同一个打开文件句柄,将共享同一文件偏移量。因此,如果通过其中一个文件描述符来修改文件偏移量 (由调用read()、write()或lseek()所致) ,那么从另一个描述符中也会观察到变化,无论这两个文件描述符是否属于不同进程,还是同一个进程,情况都是如此。
3. 要获取和修改打开的文件标志 (例如: O_APPEND、O_NONBLOCK 和 O_ASYNC) ,可执行fcntl()的F_GETFL和F_SETFL操作,其对作用域的约束与上一条颇为类似。
4. 文件描述符标志 (即,close-on-exec) 为进程和文件描述符所私有。对这一标志的修改将不会影响同一进程或不同进程中的其他文件描述符

### 查看进程打开文件描述符
```bash
#PID: 12222
ls -l /proc/12222/fd/ 
lsof -p 12222
```

### 系统级别的最大打开文件数
```bash
sysctl -a | grep fs.file-max
```

### 用户级限制
```bash
ulimit -n 2048
```

---

### 文件I/O API & 文件指针
说了这么多,用最基础的POSIX库函数写个示例程序吧。它将一个文件中的内容读出来,并原封不动地写入另外一个文件。
```c
#include <fcntl.h>
#include <sys/stat.h>
#define BUF_SIZE 1024
 
int main(int argc,char *argv[]) {
  int inputFd, outputFd;
  char buf[BUF_SIZE];
  ssize_t numRead;
 
  inputFd = open("data.txt", O_RDONLY);
  if (inputFd == -1) {
    exit(EXIT_FAILURE);
  }
  outputFd = open(
    "data_copy.txt", 
    O_CREAT | O_WRONLY | O_TRUNC,
    S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH
  );
  if (outputFd == -1) {
    exit(EXIT_FAILURE);
  }
 
  while ((numRead = read(inputFd, buf, BUF_SIZE)) > 0) {
    if (write(outputFd, buf, numRead) != numRead) {
      exit(EXIT_FAILURE);
    }
  }
  
  close(inputFd);
  close(outputFd);
  exit(EXIT_SUCCESS);
}
```

严格来讲,POSIX 提供的这些函数只是用户与内核之前的桥梁,实际仍位于系统调用层之上。但是现实应用中,我们一般也把它们叫做系统调用了 (尽管不太正确) 。

要使用open()/read()/write()/close()这些系统调用,必须引入fcntl.h头文件。open()返回的是文件描述符,其参数中传入的flags和mode值也会保存在打开文件表中。在整个读、写并最终关闭文件的过程中,操作的也都是文件描述符。

那么我们在大学C语言课程上学习的“文件指针” (file pointer) 又是什么呢？这个就比较简单,继续看下面的栗子。

```c
#include <stdio.h>
#include <stdlib.h>
#define BUF_SIZE 1024
 
int main(int argc,char *argv[]) {
  char buf[BUF_SIZE];
  FILE *inputFp;
  size_t numRead;
 
  inputFp = fopen("data.txt", "r");
  if (inputFp == NULL) {
    exit(EXIT_FAILURE);
  }
 
  while (!feof(inputFp)) {
    numRead = fread(buf, sizeof(char), sizeof(buf), inputFp);
    printf("%ld\t%s", numRead, buf);
  }
 
  fclose(inputFp);
  exit(EXIT_SUCCESS);
}
```
可见,文件指针就是FILE结构体的指针,与前两个概念不属于同一层。当通过文件指针操作文件时,需要调用C语言stdio.h中提供的文件API (fopen()、fread()等) ,而C标准库最终调用了POSIX的库函数。并且“file pointer”这个词里的“file”指的是狭义的文件,不包括管道、设备等其他东西,所以单纯用C API只能操作普通文件。

FILE结构体中是包含了文件描述符的,所以C语言也提供了互相转换的方法: 

int inputFd;
FILE *inputFp;
 
inputFd = fileno(inputFp);
inputFp = fdopen(inputFd, "r");
文件描述符和文件句柄的限制
文章开头提到了"too many open files"这条报错信息,它的实际含义是文件描述符数量超限。用ulimit -a命令打印出各限制值: 

~ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 127961
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 65535
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 127961
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
其中open files一行就表示当前用户、当前终端、单个进程能拥有的文件描述符的数量阈值 (很多文章都描述错了这一点) ,可以用ulimit -n [阈值]命令来临时修改,退出登录即失效。如果想要永久修改,可以将ulimit -n [阈值]写入用户的.bash_profile文件或/etc/profile中,也可以修改/etc/security/limits.conf: 

~ vim /etc/security/limits.conf
# 用户名 软/硬限制 限制项 阈值
root soft nofile 65535
root hard nofile 65535
那么如何列出各个进程的文件描述符呢？可以利用lsof (list open files) 命令。这个命令的用法很丰富,本文暂时不表。

既然有了进程级别的描述符数量限制,也就有系统级别的文件句柄数量限制。可以这样查看其阈值,以及当前已分配的句柄数: 

~ cat /proc/sys/fs/file-max
3247469        # 阈值
~ cat /proc/sys/fs/file-nr
# 已分配且使用中 / 已分配但未使用 / 阈值
2976    0   3247469
如果需要临时修改,可以直接向file-max写入新值。永久生效的方法是修改/etc/sysctl.conf: 

~ vim /etc/sysctl.conf
fs.file-max = 5242880
# 立即生效
~ sysctl -p
The End
最后总结一下吧。

文件描述符是进程级别的,文件句柄是系统级别的,不能混用。它们在不同级别表示已打开的文件。
文件描述符与文件句柄直接关联,文件句柄与inode直接关联。
文件描述符在POSIX系统调用中直接可见,文件指针是C语言在其基础上的包装。
文件句柄在UNIX里不是个正式概念,所以无论在系统还是C语言API中都不显式存在。
————————————————
版权声明: 本文为CSDN博主「LittleMagics」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/nazeniwaresakini/article/details/104220111


在操作系统层面上,文件操作也有类似于FILE的一个概念,在Linux里,这叫做文件描述符(File Descriptor),而在Windows里,叫做句柄(Handle)(以下在没有歧义的时候统称为句柄)。用户通过某个函数打开文件以获得句柄,此 后用户操纵文件皆通过该句柄进行。

设计这么一个句柄的原因在于句柄可以防止用户随意读写操作系统内核的文件对象。无论是Linux还是Windows,文件句柄总是和内核的文件对象相关联的,但如何关联细节用户并不可见。内核可以通过句柄来计算出内核里文件对象的地址,但此能力并不对用户开放。

下面举一个实际的例子,在Linux中,值为0、1、2的fd分别代表标准输入、标准输出和标准错误输出。在程序中打开文件得到的fd从3开始增长。 fd具体是什么呢?在内核中,每一个进程都有一个私有的"打开文件表",这个表是一个指针数组,每一个元素都指向一个内核的打开文件对象。而fd,就是这 个表的下标。当用户打开一个文件时,内核会在内部生成一个打开文件对象,并在这个表里找到一个空项,让这一项指向生成的打开文件对象,并返回这一项的下标 作为fd。由于这个表处于内核,并且用户无法访问到,因此用户即使拥有fd,也无法得到打开文件对象的地址,只能够通过系统提供的函数来操作。

在C语言里,操纵文件的渠道则是FILE结构,不难想象,C语言中的FILE结构必定和fd有一对一的关系,每个FILE结构都会记录自己唯一对应的fd。
  
句柄 http://zh.wikipedia.org/wiki/%E5%8F%A5%E6%9F%84

在程序设计 中,句柄是一种特殊的智能指针 。当一个应用程序 要引用其他系统(如数据库、操作系统 )所管理的内存 块或对象 时,就要使用句柄。

句柄与普通指针 的区别在于,指针包含的是引用对象 的内存地址 ,而句柄则是由系统所管理的引用标识,该标识可以被系统重新定位到一个内存地址 上。这种间接访问对象 的模式增强了系统对引用对象 的控制。 (参见封装 )。

在上世纪80年代的操作系统 (如Mac OS 和Windows ) 的内存管理 中,句柄被广泛应用。Unix 系统的文件描述符 基本上也属于句柄。和其它桌面环境 一样,Windows API 大量使用句柄来标识系统中的对象 ,并建立操作系统与用户空间 之间的通信渠道。例如,桌面上的一个窗体由一个HWND 类型的句柄来标识。

如今,内存 容量的增大和虚拟内存 算法使得更简单的指针 愈加受到青睐,而指向另一指针的那类句柄受到冷淡。尽管如此,许多操作系统 仍然把指向私有对象 的指针以及进程传递给客户端 的内部数组 下标称为句柄。

操作file descriptors 的 system call
open()
read()
write()
select()
poll()


http://www.blogjava.net/shijian/archive/2012/04/06/373463.html
  
http://blog.csdn.net/cywosp/article/details/38965239

 
版权声明: 本文为CSDN博主「cywosp」的原创文章,遵循 CC 4.0 BY-SA 版权协议,转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/cywosp/article/details/38965239

### 引用来源
Michael Kerrisk所著《The Linux Programming Interface: A Linux and UNIX System Programming Handbook》的第4、5两章。

http://www.cxyzjd.com/article/nazeniwaresakini/104220111  
>https://wiyi.org/linux-file-descriptor.html
