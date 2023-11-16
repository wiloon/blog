---
title: linux AIO
author: "-"
date: 2012-06-12T12:44:17+00:00
url: linux/aio
categories:
  - Linux
tags:
  - reprint
---
## linux AIO

glibc 的 aio 有 bug , kernel 的 aio 只能以 O_DIRECT 方式做直接 IO , libeio 也是 beta 阶段。epoll 是成熟的，但是 epoll 本身是同步的。Linux 上目前没有像 IOCP 这样的成熟异步 IO 实现。

作者：cholerae
链接：[https://www.zhihu.com/question/26943558/answer/125159376](https://www.zhihu.com/question/26943558/answer/125159376)
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

在高性能的服务器编程中，IO 模型理所当然的是重中之重，需要谨慎选型的，对于网络套接字，我们可以采用epoll 的方式来轮询，尽管epoll也有一些缺陷，但总体来说还是很高效的，尤其来大量套接字的场景下；但对于Regular File 来说，是不能够用采用 poll/epoll 的，即O_NOBLOCK 方式对于传统文件句柄是无效的，也就是说我们的 open ,read, mkdir 之类的Regular File操作必定会导致阻塞.在多线程、多进程模型中，可以选择以同步阻塞的方式来进行IO操作，任务调度由操作系统来保证公平性，但在单进程/线程模型中，以nodejs 为例 ，假如 我们需要在一个用户请求中处理10个文件：

function fun() {

 fs.readFileSync();

 fs.readFileSync();

 …

 }
这时候进程至少会阻塞10次，而这可能会导致其他的上千个用户请求得不到处理，这当然是不能接受的.

Linux AIO 早就被提上议程，目前比较知名的有 Glibc 的 AIO   与 Kernel Native AIO
Glibc AIO: [http://www.ibm.com/developerworks/linux/library/l-async/](http://www.ibm.com/developerworks/linux/library/l-async/)
Kernel Native AIO: [http://lse.sourceforge.net/io/aio.html](http://lse.sourceforge.net/io/aio.html)

在Glibc AIO 的实现中， 用多线程同步来模拟 异步IO ，以上述代码为例，它牵涉了3个线程，
主线程（23908）新建 一个线程（23909）来调用 阻塞的pread函数，当pread返回时，又创建了一个线程（23910）来执行我们预设的异步回调函数， 23909 等待23910结束返回，然后23909也结束执行..

实际上，为了避免线程的频繁创建、销毁，当有多个请求时，Glibc AIO 会使用线程池，但以上原理是不会变的，尤其要注意的是：我们的回调函数是在一个单独线程中执行的.
Glibc AIO 广受非议，存在一些难以忍受的缺陷和bug，饱受诟病，是极不推荐使用的.
详见：[http://davmac.org/davpage/linux/async-io.html](http://davmac.org/davpage/linux/async-io.html)

在Linux 2.6.22+ 系统上，还有一种 Kernel AIO 的实现，与 Glibc 的多线程模拟不同 ，它是真正的做到内核的异步通知，比如在较新版本的Nginx 服务器上，已经添加了AIO方式 的支持.

[http://wiki.nginx.org/HttpCoreModule](http://wiki.nginx.org/HttpCoreModule)
aio
syntax: aio [on|off|sendfile]
default: off
context: http, server, location
This directive is usable as of Linux kernel 2.6.22. For Linux it is required to use directio, this automatically disables sendfile support.

location /video {
aio on;
directio 512;
output_buffers 1 128k;
}

听起来Kernel Native AIO 几乎提供了近乎完美的异步方式，但如果你对它抱有太高期望的话，你会再一次感到失望.

目前的Kernel AIO 仅支持 O_DIRECT 方式来对磁盘读写，这意味着，你无法利用系统的缓存，同时它要求读写的的大小和偏移要以区块的方式对齐,参考nginx 的作者 Igor Sysoev 的评论： [http://forum.nginx.org/read.php?2,113524,113587#msg-113587](http://forum.nginx.org/read.php?2,113524,113587#msg-113587)

nginx supports file AIO only in 0.8.11+, but the file AIO is functional
on FreeBSD only. On Linux AIO is supported by nginx only on kerenl
2.6.22+ (although, CentOS 5.5 has backported the required AIO features).
Anyway, on Linux AIO works only if file offset and size are aligned
to a disk block size (usually 512 bytes) and this data can not be cached
in OS VM cache (Linux AIO requires DIRECTIO that bypass OS VM cache).
I believe a cause of so strange AIO implementaion is that AIO in Linux
was developed mainly for databases by Oracle and IBM.

同时注意上面的橙色字部分，启用AIO 就会关闭sendfile -这是显而易见的，当你用Nginx作为静态服务器，你要么选择以AIO 读取文件到用户缓冲区，然后发送到套接口，要么直接调用sendfile发送到套接口,sendfile 虽然会导致短暂的阻塞，但开启AIO 却无法充分的利用缓存，也丧失了零拷贝的特征 ;当你用Nginx作为动态服务器，比如　fastcgi + php 时，这时php脚本中文件的读写是由php 的 文件接口来操作的，这时候是多进程+同步阻塞模型，和文件异步模式扯不上关系的.

所以现在Linux 上，没有比较完美的异步文件IO 方案，这时候苦逼程序员的价值就充分体现出来了，libev 的作者 Marc Alexander Lehmann 老大就重新实现了一个AIO library ：

[http://software.schmorp.de/pkg/libeio.html](http://software.schmorp.de/pkg/libeio.html)

>[http://www.wzxue.com/linux-kernel-aio](http://www.wzxue.com/linux-kernel-aio)
