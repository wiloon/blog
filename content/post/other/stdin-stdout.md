---
title: "STDIN, STDOUT, STDERR"
author: "-"
date: 2011-11-19T07:35:23+00:00
lastmod: 2026-07-26T12:57:09+08:00
url: stdin-stdout
categories:
  - Linux
tags:
  - stdio
  - buffering
  - remix
  - AI-assisted
aliases:
  - /p1543/
  - /p4276/
---

## 三个标准文件

Unix/Linux/BSD 都有三个特别文件：

| 文件 | 设备路径 | 说明 | shell 里的代号（fd） |
| ---- | ---- | ---- | ---- |
| 标准输入 STDIN | `/dev/stdin` | 一般指键盘输入 | 0 |
| 标准输出 STDOUT | `/dev/stdout` | 一般指终端（显示器） | 1 |
| 标准错误 STDERR | `/dev/stderr` | 也指终端，专门用来发送错误信息 | 2 |

## stdin 与文件描述符表、pty、键盘的关系

stdin 不是一个独立的东西，它是**文件描述符表**（file descriptor table，每个进程私有）里 fd 0 这个槽位的习惯叫法。fd 0 具体指向什么取决于进程是怎么启动的——可能重定向到文件、接在管道后面，也可能像交互式 shell 一样连到终端。

在交互式终端场景下，从键盘到 stdin 的完整链路是：

```text
键盘硬件
   │  内核输入子系统 (evdev)
   ▼
终端模拟器进程 / SSH 客户端-服务端        <- 用户态进程，把按键翻译成字符
   │  write() 进 /dev/ptmx（pty master 端）
   ▼
内核 pty 子系统转发 master -> slave
   ▼
/dev/pts/N（pty slave，字符设备，内核模拟出来的）
   ▼
shell 进程的 fd 0（即 stdin）read() 读到这些字节
```

要点：

- **fd 0 是文件描述符表里的一个槽位，stdin 只是它的别名**，不存在"stdin 关联到 fd0"这种额外的中间层
- fd 0 底层通常指向 `/dev/pts/N`——**pty slave**，是内核用 pty 机制模拟出来的字符设备，不是真实硬件；关于字符设备本身见 [BDEV, CDEV](../linux/bdev-cdev.md)
- pty slave 并不直接连接键盘：真正拿到键盘输入、把字节流写进 pty master 的，是终端模拟器或 SSH 链路这个用户态进程；这一点和真实串口终端、虚拟控制台（`/dev/tty1` 等，内核直接处理键盘输入）不同，详见 [Linux TTY 与伪终端 PTY](../linux/linux-tty.md)
- 进程通过 stdin 读到的字节流，最终来源是键盘，但中间经过了终端模拟器/SSH → pty master → 内核转发 → pty slave 这几跳，并不是直连

## stdout 与 stderr 其实指向同一个设备

有人说 stdout 是带缓冲的，stderr 是不带缓冲的，这并不是指 fd=1 和 fd=2 这两个设备文件本身——它们都是字符设备，本身没有缓存。一个进程的 fd 1 和 fd 2 通常指向同一个终端设备文件：

```bash
ls -l /proc/8669/fd/
```

```text
total 0
lrwx------ 1 root root 64  4月 25 20:57 0 -> /dev/pts/7
lrwx------ 1 root root 64  4月 25 20:57 1 -> /dev/pts/7
lrwx------ 1 root root 64  4月 25 20:57 2 -> /dev/pts/7
```

细想一下就知道，向 fd 1 或 fd 2 写东西，在内核里走的是完全相同的路径，不可能存在一会儿缓存一会儿不缓存的情况。

## 真正的缓冲发生在用户态标准库

调用 `printf()` 或 `fwrite(..., stdout)` 时，进入标准库后会先把要写的内容放到一个缓存里，直到遇到回车（或缓存满，比如缓冲最大 1024 字节）或者程序退出（`return` 和 `exit()` 会刷 stdout 缓存），才会调用 `write` 系统调用进到内核设备驱动实际去写。这样可以降低 `write` 系统调用的频率。而向 stderr 写东西不在标准库里做缓存，是立即调用 `write` 去写的。

我们说 stdout 是行缓冲的、stderr 是无缓冲的，就是这个意思——这里的 stdout 和 stderr 指标准库里 `FILE` 结构的指针，而不是标准输出和标准错误设备本身。

下面的程序里每个字符串都没有加回车：

```c
int main()
{
    fwrite("aaaaa", 5, 1, stdout);
    fwrite("bbbbb", 5, 1, stdout);
    fwrite("ccccc", 5, 1, stdout);
    fwrite("ddddd", 5, 1, stderr); // stderr, written immediately

    return 0;
}
```

实际观察到的现象是先打印 `ddddd`，再一起打印 `aaaaabbbbbccccc`。换成 `printf`/`perror` 或 `fprintf(stdout, ...)`/`fprintf(stderr, ...)` 也是一样的结果。而用 `write(1, ...)` 和 `write(2, ...)` 都是直接调用系统调用进内核，每次都会立即打印出来。

## 缓冲类型

标准库中的 stream（即 `FILE` 结构的流文件）有三种缓冲类型：

- **全缓冲（block buffered）**：以缓冲大小为限，例如 4096 字节，fwrite 到 4KB 后标准库才会调用一次 `write` 去写
- **行缓冲（line buffered）**：以换行为限，遇到 newline 时标准库才会调用一次 `write` 去写；不过行缓冲区也有大小限制，例如 1024 字节，缓冲满了也会去 `write`
- **无缓冲（unbuffered）**：标准库中不开辟缓冲区

默认情况下，从终端的输入输出流都是行缓冲的，体现在诸如 `printf()`/`getchar()`/`putchar()` 等函数；`stderr` 总是无缓冲的；其他文件流是全缓冲的。

## 主动刷新缓冲：fflush()

```c
#include <stdio.h>
int fflush(FILE *stream);
```

- 对于输出流（例如向 stdout 或其他文件写东西），`fflush(stream)` 将文件在用户态标准库的缓冲全部刷到内核里
- 对输入流，`fflush(stream)` 则丢弃所有尚未被应用程序拿到的缓冲数据
- 如果参数 `stream` 为 `NULL`，则 `fflush` 对所有打开的输出流文件做刷缓冲操作
- 除了 `fflush()`，对一个文件进行 `fseek()` 或 `fread()` 时，也会触发调用 `write` 将缓冲写进内核

调用 `fclose()` 关闭文件前也会调用 `fflush()` 刷用户态缓冲，并释放缓冲区内存（`fopen()` 打开文件时会为这个 `fp` 申请缓冲用的空间，如 4KB，每个 `fp` 有自己的缓冲区）。

另外，实验证明 `exit()` 和 `return` 退出程序后也会清所有打开文件的缓冲区，而 `_exit()` 不会。如果程序异常退出（如未处理的 Ctrl+C 信号）也不会清缓冲区。

## 用 setvbuf() 等函数修改缓冲类型

```c
#include <stdio.h>
void setbuf(FILE *stream, char *buf);
void setbuffer(FILE *stream, char *buf, size_t size);
void setlinebuf(FILE *stream);
int setvbuf(FILE *stream, char *buf, int mode, size_t size);
```

## 补充：内核 page cache

以上提到的都是用户态的文件缓冲，`fflush` 之后能保证将写入内容提交给了内核。但对于块设备文件系统中的文件，仍不保证能真正写到磁盘文件中，因为内核的 page cache 还会做一层缓存。

---

作者: 落尘纷扰  
链接: [https://blog.csdn.net/jasonchen_gbd/article/details/80795645](https://blog.csdn.net/jasonchen_gbd/article/details/80795645)  
来源: CSDN  
著作权归作者所有，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-26 | 补充 front matter（`lastmod`、内容标签）；标题整理为 `STDIN, STDOUT, STDERR`；正文重新分节（标准文件表格化、代码块加语言标识、缓冲类型改列表）；合并末尾重复的来源链接为规范引用格式；标签 `reprint` 改为 `remix` + `AI-assisted` | 原文档缺少 `lastmod`，代码/命令未用 fenced code block，末尾重复引用来源链接，全文未分节不便阅读 |
