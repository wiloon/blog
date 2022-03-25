---
title: STDIN STDOUT, STDERR
author: "-"
date: 2011-11-19T07:35:23+00:00
url: /?p=1543
categories:
  - Linux

tags:
  - reprint
---
## STDIN STDOUT, STDERR
Unix/Linux/BSD 都有三个特别文件，分别
1) 标准输入 即 STDIN , 在 /dev/stdin ,
   一般指键盘输入, shell里代号是 0
2) 标准输出 STDOUT, 在 /dev/stdout,
   一般指终端(terminal), 就是显示器, shell里代号是 1
3) 标准错误 STDERR, 在 /dev/stderr
   也是指终端(terminal), 不同的是, 错误信息送到这里
   shell里代号是 2


stdout和stderr
有人说stdio是带缓冲的，stderr是不带缓冲的，这并不是指fd=1和fd=2这两个设备文件，这两个设备是字符设备，本身没有缓存。并且你看一个进程的1和2两个fd指向的其实是同一个终端设备文件：

[root@ubuntu]arm-code:$ ls -l /proc/8669/fd/
total 0
lrwx------ 1 root root 64  4月 25 20:57 0 -> /dev/pts/7
lrwx------ 1 root root 64  4月 25 20:57 1 -> /dev/pts/7
lrwx------ 1 root root 64  4月 25 20:57 2 -> /dev/pts/7

所以，细想一下就知道，向1或2两个fd写东西，在内核里走的是完全相同的路径，不可能存在一会儿缓存一会儿不缓存的情况。

那上面说的“缓存”到底是什么东西呢？

如果你调用printf()或fwrite(…, stdout)，进入标准库后会先把要写的内容放到一个缓存里，直到遇到回车 (或缓存满，比如缓冲最大1024字节）或者程序退出 (return和exit()会刷stdout缓存），才会调用write系统调用进到内核设备驱动实际去写。这样可以降低write系统调用的频率，而向stderr写东西就不在标准库里做缓存而是立即调用write去写了。我们说stdout是行缓冲的，stderr是无缓冲的，就是这个意思，注意这里的stdout和stderr是指标准库里的FILE结构的指针，而不是标准输出和标准错误设备。

所以下面的程序，每个字符串都没有加回车，你就会看到先打印"ddddd"，再一起打印"aaaaabbbbbccccc"。换成printf/perror或fprintf(stdout, …)/fprintf(stderr, …)也是一样的结果。而你用write(1, …)和write(2, …)都是直接调用系统调用进内核，每次都会立即打印出来。

int main()
{
    fwrite("aaaaa", 5, 1, stdout);
    fwrite("bbbbb", 5, 1, stdout);
    fwrite("ccccc", 5, 1, stdout);
    fwrite("ddddd", 5, 1, stderr); //stderr

    return 0;
}

缓冲类型
标准库中的stream (即FILE结构的流文件）有三种缓冲类型：
全缓冲 (block buffered）：以缓冲大小为限，例如4096字节，则你fwrite到4KB后标准库才会调用一次write去写。
行缓冲 (line buffered）：以换行为限，当遇到newline的时候标准库才会调用一次write去写。不过如前面所说，行缓冲区也有大小限制，例如1024字节，缓冲满了也会去write。
无缓冲 (unbuffered）：在标准库中不开辟缓冲区。

你也可以主动去清缓冲，使用fflush()即可：

#include <stdio.h>
int fflush(FILE *stream);
1
2
对于输出流 (例如向stdio或其他文件写东西），fflush(stream)将文件在用户态标准库的缓冲全部刷到内核里。对输入流，fflush(stream)则丢弃所有尚未被应用程序拿到的缓冲数据。
如果参数stream为NULL，则fflush对所有打开的输出流文件做刷缓冲操作。
除了fflush()，在对一个文件进行fseek()或fread()时，也会触发调用write将缓冲写进内核。

注：调用**fclose()**关闭文件前也会调用fflush()刷用户态缓冲的，并释放缓冲区内存 (fopen()打开文件的时候，会为这个fp申请缓冲用的空间，如4KB，每个fp有自己的缓冲区）。
另外我实验exit()和return退出程序后也会清所有打开文件的缓冲区，而_exit()不会。如果程序异常退出 (如未处理的Ctrl+C信号）也不会清缓冲区。

默认情况下，从终端的输入输出流都是行缓冲的，体现在诸如printf()/getchar()/putchar()等函数；stderr总是无缓冲的；其他文件流是全缓冲的。

你可以通过setvbuf()等函数修改stream的缓冲类型和缓冲区大小：

#include <stdio.h>
void setbuf(FILE *stream, char *buf);
void setbuffer(FILE *stream, char *buf, size_t size);
void setlinebuf(FILE *stream);
int setvbuf(FILE *stream, char *buf, int mode, size_t size);

再补充一点，我们目前提到的都是用户态的文件缓冲，flush之后能保证将写入内容提交给了内核。但对于块设备文件系统中的文件，仍不保证能真正写到磁盘文件中，因为内核的page cache还会做一层缓存。
————————————————
版权声明：本文为CSDN博主「落尘纷扰」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/jasonchen_gbd/article/details/80795645



>https://blog.csdn.net/jasonchen_gbd/article/details/80795645
