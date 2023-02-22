---
title: epoll, kqueue
author: "-"
date: 2018-08-28T11:23:26+00:00
url: epoll
categories:
  - OS
tags:
  - reprint
---
## epoll, kqueue

epoll 通过使用红黑树(RB-tree)搜索被监视的文件描述符(file descriptor)。

### 用户空间与内核空间

现在操作系统都是采用虚拟存储器,那么对32位操作系统而言,它的寻址空间 (虚拟存储空间) 为4G (2的32次方) 。操作系统的核心是内核,独立于普通的应用程序,可以访问受保护的内存空间,也有访问底层硬件设备的所有权限。为了保证用户进程不能直接操作内核 (kernel) ,保证内核的安全,操心系统将虚拟空间划分为两部分,一部分为内核空间,一部分为用户空间。针对linux操作系统而言,将最高的1G字节 (从虚拟地址0xC0000000到0xFFFFFFFF) ,供内核使用,称为内核空间,而将较低的3G字节 (从虚拟地址0x00000000到0xBFFFFFFF) ,供各个进程使用,称为用户空间。

### 进程切换

为了控制进程的执行,内核必须有能力挂起正在CPU上运行的进程,并恢复以前挂起的某个进程的执行。这种行为被称为进程切换。因此可以说,任何进程都是在操作系统内核的支持下运行的,是与内核紧密相关的。

从一个进程的运行转到另一个进程上运行,这个过程中经过下面这些变化:
  
1. 保存处理机上下文,包括程序计数器和其他寄存器。
2. 更新PCB信息。
3. 把进程的PCB移入相应的队列,如就绪、在某事件阻塞等队列。
4. 选择另一个进程执行,并更新其PCB。
5. 更新内存管理的数据结构。
6. 恢复处理机上下文。

### 进程的阻塞

正在执行的进程,由于期待的某些事件未发生,如请求系统资源失败、等待某种操作的完成、新数据尚未到达或无新工作做等,则由系统自动执行阻塞原语(Block),使自己由运行状态变为阻塞状态。可见,进程的阻塞是进程自身的一种主动行为,也因此只有处于运行态的进程 (获得CPU) ,才可能将其转为阻塞状态。当进程进入阻塞状态,是不占用CPU资源的。

### 缓存 I/O

缓存 I/O 又被称作标准 I/O,大多数文件系统的默认 I/O 操作都是缓存 I/O。在 Linux 的缓存 I/O 机制中,操作系统会将 I/O 的数据缓存在文件系统的页缓存 ( page cache ) 中,也就是说,数据会先被拷贝到操作系统内核的缓冲区中,然后才会从操作系统内核的缓冲区拷贝到应用程序的地址空间。

缓存 I/O 的缺点:
  
数据在传输过程中需要在应用程序地址空间和内核进行多次数据拷贝操作,这些数据拷贝操作所带来的 CPU 以及内存开销是非常大的。

### IO模式
  
刚才说了,对于一次IO访问 (以read举例) ,数据会先被拷贝到操作系统内核的缓冲区中,然后才会从操作系统内核的缓冲区拷贝到应用程序的地址空间。所以说,当一个read操作发生时,它会经历两个阶段:
  
1. 等待数据准备 (Waiting for the data to be ready)
2. 将数据从内核拷贝到进程中 (Copying the data from the kernel to the process)

正式因为这两个阶段,linux系统产生了下面五种网络模式的方案。

1. 阻塞 I/O (blocking IO)
2. 非阻塞 I/O (nonblocking IO)
3. I/O 多路复用 ( IO multiplexing)
4. 信号驱动 I/O ( signal driven IO)
5. 异步 I/O (asynchronous IO)

每一种 I/O 模型都有典型的使用场景，比如 Socket 的阻塞模式和非阻塞模式就对应于前两种模型, Linux中的 select 函数就属于 I/O 多路复用模型, 第 5 种模型 (异步 I/O) 其实很少有 UNIX 和类 UNIX 系统支持, Windows的 IOCP（I/O Completion Port，简称 IOCP）属于此模型 (异步 I/O)。至于大名鼎鼎的 Linux epoll模型，则可以看作兼具第3种和第4种模型的特性。 通常情况下我们会认为epoll比 select模型高级. 毕竟 epoll取消了轮询机制，取而代之的是回调机制（callback）。 -- 《Apache Kafka实战》 — 胡夕

注: 由于 signal driven IO 在实际中并不常用, 所以我这只提及剩下的四种 IO Model。

### 阻塞 I/O (blocking IO)  BIO,Blocking I/O

在linux中,默认情况下所有的socket都是blocking

当用户进程调用了recvfrom 这个系统调用, kernel 就开始了 IO 的第一个阶段: 准备数据 (对于网络 IO 来说, 很多时候数据在一开始还没有到达。比如, 还没有收到一个完整的UDP包。这个时候 kernel 就要等待足够的数据到来) 。这个过程需要等待, 也就是说数据被拷贝到操作系统内核的缓冲区中是需要一个过程的。而在用户进程这边,整个进程会被阻塞 (当然,是进程自己选择的阻塞) 。当kernel一直等到数据准备好了,它就会将数据从kernel中拷贝到用户内存,然后kernel返回结果,用户进程才解除block的状态,重新运行起来。

所以,blocking IO的特点就是在IO执行的两个阶段都被block了。

### 非阻塞 I/O, Non-blocking I/O, NIO

linux下,可以通过设置socket使其变为non-blocking。  
当用户进程发出read操作时,如果kernel中的数据还没有准备好,那么它并不会block用户进程,而是立刻返回一个error。从用户进程角度讲 ,它发起一个read操作后,并不需要等待,而是马上就得到了一个结果。用户进程判断结果是一个error时,它就知道数据还没有准备好,于是它可以再次发送read操作。一旦kernel中的数据准备好了,并且又再次收到了用户进程的system call,那么它马上就将数据拷贝到了用户内存,然后返回。

所以,nonblocking IO的特点是用户进程需要不断的主动询问kernel数据好了没有。

### I/O 多路复用 ( IO multiplexing)

IO multiplexing就是我们说的select,poll,epoll,有些地方也称这种IO方式为event driven IO。select/epoll的好处就在于单个process就可以同时处理多个网络连接的IO。它的基本原理就是select,poll,epoll这个function会不断的轮询所负责的所有socket,当某个socket有数据到达了,就通知用户进程。

clipboard.png

当用户进程调用了select,那么整个进程会被block,而同时,kernel会"监视"所有select负责的socket,当任何一个socket中的数据准备好了,select就会返回。这个时候用户进程再调用read操作,将数据从kernel拷贝到用户进程。

所以,I/O 多路复用的特点是通过一种机制一个进程能同时等待多个文件描述符,而这些文件描述符 ( socket 描述符) 其中的任意一个进入读就绪状态,select()函数就可以返回。

这个图和blocking IO的图其实并没有太大的不同,事实上,还更差一些。因为这里需要使用两个system call (select 和 recvfrom),而blocking IO只调用了一个system call (recvfrom)。但是,用select的优势在于它可以同时处理多个connection。

所以,如果处理的连接数不是很高的话,使用select/epoll的web server不一定比使用multi-threading + blocking IO的web server性能更好,可能延迟还更大。select/epoll的优势并不是对于单个连接能处理得更快,而是在于能处理更多的连接。)

在IO multiplexing Model中,实际中,对于每一个socket,一般都设置成为non-blocking,但是,如上图所示,整个用户的process其实是一直被block的。只不过process是被select这个函数block,而不是被socket IO给block。

## Epoll

Epoll, 位于头文件 sys/epoll.h, 是Linux 系统上的I/O 事件通知基础设施。epoll API 为Linux 系统专有,于内核2.5.44 中首次引入, glibc 于 2.3.2 版本加入支持。其它提供类似的功能的系统,包括 FreeBSD kqueue, Solaris /dev/poll等。
  
### Epoll API

Epoll API实现了与poll 类似的功能: 监测多个文件描述符上是否可以执行I/O操作。支持边缘触发ET和水平触发LT,相比poll支持监测数量更多的文件描述符。
  
poll_create: 创建Epoll实例,并返回Epoll实例关联的文件描述符。 (最新的epoll_create1扩展了epoll_create的功能)

create_ctl: 注册关注的文件描述符。注册于同一epoll实例的一组文件描述符被称为epoll set,可以通过进程对应的/proc/[pid]/fdinfo目录查看。

epoll_wait: 等待I/O事件,如果当前没有任何注册事件处于可用状态,调用线程会被阻塞。
  
水平触发LT与边缘触发ET

Epoll事件分发接口可以使用ET和LT两种模式。两种模式的差别描述如下。

典型场景:

1 管道(pipe)读端的文件描述符(rfd)注册于Epoll实例。

2 写者(Writer)向管道(pipe)写端写2KB的数据。

3 epoll_wait调用结束,返回rfd作为就绪的文件描述符。

4 管道读者(pipe reader) 从rfd读1KB的数据。

5 下一次epoll_wait调用。

### I/O 多路复用之 select、poll、epoll详解

select,poll,epoll 都是IO多路复用的机制。I/O多路复用就是通过一种机制,一个进程可以监视多个描述符,一旦某个描述符就绪 (一般是读就绪或者写就绪) ,能够通知程序进行相应的读写操作。但select,poll,epoll本质上都是同步I/O,因为他们都需要在读写事件就绪后自己负责进行读写,也就是说这个读写过程是阻塞的,而异步I/O则无需自己负责进行读写,异步I/O的实现会负责把数据从内核拷贝到用户空间。 (这里啰嗦下)

#### select

int select (int n, fd_set *readfds, fd_set*writefds, fd_set *exceptfds, struct timeval*timeout);
select 函数监视的文件描述符分3类,分别是 writefds、readfds、和exceptfds。调用后select函数会阻塞,直到有描述副就绪 (有数据 可读、可写、或者有except) ,或者超时 (timeout指定等待时间,如果立即返回设为null即可) ,函数返回。当select函数返回后,可以 通过遍历fdset,来找到就绪的描述符。

select目前几乎在所有的平台上支持,其良好跨平台支持也是它的一个优点。
select 的一个缺点在于单个进程能够监视的文件描述符的数量存在**最大限制**, 在Linux上一般为1024,可以通过修改宏定义甚至重新编译内核的方式提升这一限制, 但是这样也会造成效率的降低。

#### poll

int poll (struct pollfd *fds, unsigned int nfds, int timeout);
不同与select使用三个位图来表示三个fdset的方式,poll使用一个 pollfd的指针实现。

struct pollfd {
    int fd; /*file descriptor*/
    short events; /*requested events to watch*/
    short revents; /*returned events witnessed*/
};
pollfd 结构包含了要监视的 event 和发生的event,不再使用select“参数-值”传递的方式。同时,pollfd并没有最大数量限制 (但是数量过大后性能也是会下降) 。 和select函数一样,poll返回后,需要轮询pollfd来获取就绪的描述符。

从上面看,select和poll都需要在返回后,通过**遍历文件描述符**来获取已经就绪的socket。事实上,同时连接的大量客户端在一时刻可能只有很少的处于就绪状态,因此随着监视的描述符数量的增长,其效率也会线性下降。

#### epoll

epoll的原理就是:
你把要监控读写的文件交给内核 (epoll_add)
设置你关心的事件 (epoll_ctl) ,比如读事件
然后等 (epoll_wait) ,此时,如果没有哪个文件有你关心的事件,则休眠,直到有事件,被唤醒
然后返回那些事件实现并发,还需要配合非阻塞的读写。这样就可以一下搜集一大把文件 ( socket ) ,然后一下读写一大把文件 (不会因为某个文件慢而阻塞) ,这样来实现并发。

epoll的优势在于,由接收数据的OS来负责通知你有数据可以操作,因为OS是知道什么时候有数据的。
仍然用快递例子来说,ePoll的优势就是,你可以随便做其他的事情,当有快递来的时候,他给你打电话让你来拿,你空了的时候下来拿就好了。
不像阻塞那样需要一直在窗边看着快递来没来,也不需要像select那样不停地打电话问快递来没来。尤其是在快递比较多的时候,select需要问快递你没有你的快递,快递说有的时候,你还需要逐个问某一个包裹到没到；ePoll会直接告诉你,你的哪个包裹的快递到了。

epoll是在2.6内核中提出的,是之前的select和poll的增强版本。相对于select和poll来说,epoll更加灵活,没有描述符限制。epoll使用一个文件描述符管理多个描述符,将用户关心的文件描述符的事件存放到内核的一个事件表中,这样在用户空间和内核空间的copy只需一次。

一 epoll操作过程
epoll操作过程需要三个接口,分别如下:

int epoll_create(int size)；//创建一个epoll的句柄,size用来告诉内核这个监听的数目一共有多大
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；
int epoll_wait(int epfd, struct epoll_event* events, int maxevents, int timeout);

##### int epoll_create(int size)

创建一个epoll的句柄,size用来告诉内核这个监听的数目一共有多大,这个参数不同于select()中的第一个参数,给出最大监听的fd+1的值,参数size并不是限制了epoll所能监听的描述符最大个数,只是对内核初始分配内部数据结构的一个建议。
当创建好epoll句柄后,它就会占用一个fd值,在linux下如果查看/proc/进程id/fd/,是能够看到这个fd的,所以在使用完epoll后,必须调用close()关闭,否则可能导致fd被耗尽。

#### int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)

函数是对指定描述符fd执行op操作。

- epfd: 是epoll_create()的返回值。
- op: 表示op操作,用三个宏来表示: 添加EPOLL_CTL_ADD,删除EPOLL_CTL_DEL,修改EPOLL_CTL_MOD。分别添加、删除和修改对fd的监听事件。
- fd: 是需要监听的fd (文件描述符)
- epoll_event: 是告诉内核需要监听什么事,struct epoll_event结构如下:

struct epoll_event {
  __uint32_t events;  /* Epoll events */
  epoll_data_t data;  /* User data variable */
};

//events可以是以下几个宏的集合:
EPOLLIN : 表示对应的文件描述符可以读 (包括对端SOCKET正常关闭) ；
EPOLLOUT: 表示对应的文件描述符可以写；
EPOLLPRI: 表示对应的文件描述符有紧急的数据可读 (这里应该表示有带外数据到来) ；
EPOLLERR: 表示对应的文件描述符发生错误；
EPOLLHUP: 表示对应的文件描述符被挂断；
EPOLLET:  将EPOLL设为边缘触发(Edge Triggered)模式,这是相对于水平触发(Level Triggered)来说的。
EPOLLONESHOT: 只监听一次事件,当监听完这次事件之后,如果还需要继续监听这个socket的话,需要再次把这个socket加入到EPOLL队列里

#### int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout)

等待epfd上的io事件,最多返回maxevents个事件。
参数events用来从内核得到事件的集合,maxevents告之内核这个events有多大,这个maxevents的值不能大于创建epoll_create()时的size,参数timeout是超时时间 (毫秒,0会立即返回,-1将不确定,也有说法说是永久阻塞) 。该函数返回需要处理的事件数目,如返回0表示已超时。

### 工作模式

epoll对文件描述符的操作有两种模式: LT (level trigger) 和ET (edge trigger) 。LT模式是默认模式,LT模式与ET模式的区别如下:
LT模式: 当epoll_wait检测到描述符事件发生并将此事件通知应用程序,应用程序可以不立即处理该事件。下次调用epoll_wait时,会再次响应应用程序并通知此事件。
ET模式: 当epoll_wait检测到描述符事件发生并将此事件通知应用程序,应用程序必须立即处理该事件。如果不处理,下次调用epoll_wait时,不会再次响应应用程序并通知此事件。

1. LT模式
LT(level triggered)是缺省的工作方式,并且同时支持block和no-block socket.在这种做法中,内核告诉你一个文件描述符是否就绪了,然后你可以对这个就绪的fd进行IO操作。如果你不作任何操作,内核还是会继续通知你的。

2. ET模式
ET(edge-triggered)是高速工作方式,只支持no-block socket。在这种模式下,当描述符从未就绪变为就绪时,内核通过epoll告诉你。然后它会假设你知道文件描述符已经就绪,并且不会再为那个文件描述符发送更多的就绪通知,直到你做了某些操作导致那个文件描述符不再为就绪状态了(比如,你在发送,接收或者接收请求,或者发送接收的数据少于一定量时导致了一个EWOULDBLOCK 错误) 。但是请注意,如果一直不对这个fd作IO操作(从而导致它再次变成未就绪),内核不会发送更多的通知(only once)  
ET模式在很大程度上减少了epoll事件被重复触发的次数,因此效率要比LT模式高。epoll工作在ET模式的时候,必须使用非阻塞 socket ,以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。

## 总结

假如有这样一个例子:

1. 我们已经把一个用来从管道中读取数据的文件句柄(RFD)添加到epoll描述符
2. 这个时候从管道的另一端被写入了2KB的数据
3. 调用epoll_wait(2),并且它会返回RFD,说明它已经准备好读取操作
4. 然后我们读取了1KB的数据
5. 调用epoll_wait(2)......

LT模式:
如果是LT模式,那么在第5步调用epoll_wait(2)之后,仍然能受到通知。

ET模式:
如果我们在第1步将RFD添加到epoll描述符的时候使用了EPOLLET标志,那么在第5步调用epoll_wait(2)之后将有可能会挂起,因为剩余的数据还存在于文件的输入缓冲区内,而且数据发出端还在等待一个针对已经发出数据的反馈信息。只有在监视的文件句柄上发生了某个事件的时候 ET 工作模式才会汇报事件。因此在第5步的时候,调用者可能会放弃等待仍在存在于文件输入缓冲区内的剩余数据。

当使用epoll的ET模型来工作时,当产生了一个EPOLLIN事件后,
读数据的时候需要考虑的是当recv()返回的大小如果等于请求的大小,那么很有可能是缓冲区还有数据未读完,也意味着该次事件还没有处理完,所以还需要再次读取:

while(rs){
  buflen = recv(activeevents[i].data.fd, buf, sizeof(buf), 0);
  if(buflen < 0){
    // 由于是非阻塞的模式,所以当errno为EAGAIN时,表示当前缓冲区已无数据可读
    // 在这里就当作是该次事件已处理处.
    if(errno == EAGAIN){
        break;
    }
    else{
        return;
    }
  }
  else if(buflen == 0){
     // 这里表示对端的socket已正常关闭.
  }

 if(buflen == sizeof(buf){
      rs = 1;   // 需要再次读取
 }
 else{
      rs = 0;
 }
}
Linux中的EAGAIN含义

Linux环境下开发经常会碰到很多错误(设置errno),其中EAGAIN是其中比较常见的一个错误(比如用在非阻塞操作中)。
从字面上来看,是提示再试一次。这个错误经常出现在当应用程序进行一些非阻塞(non-blocking)操作(对文件或socket)的时候。

例如,以 O_NONBLOCK的标志打开文件/socket/FIFO,如果你连续做read操作而没有数据可读。此时程序不会阻塞起来等待数据准备就绪返回,read函数会返回一个错误EAGAIN,提示你的应用程序现在没有数据可读请稍后再试。
又例如,当一个系统调用(比如fork)因为没有足够的资源(比如虚拟内存)而执行失败,返回EAGAIN提示其再调用一次(也许下次就能成功)。

三 代码演示
下面是一段不完整的代码且格式不对,意在表述上面的过程,去掉了一些模板代码。

```c

# define IPADDRESS   "127.0.0.1"
# define PORT        8787
# define MAXSIZE     1024
# define LISTENQ     5
# define FDSIZE      1000
# define EPOLLEVENTS 100

listenfd = socket_bind(IPADDRESS,PORT);

struct epoll_event events[EPOLLEVENTS];

//创建一个描述符
epollfd = epoll_create(FDSIZE);

//添加监听描述符事件
add_event(epollfd,listenfd,EPOLLIN);

//循环等待
for ( ; ; ){
    //该函数返回已经准备好的描述符事件数目
    ret = epoll_wait(epollfd,events,EPOLLEVENTS,-1);
    //处理接收到的连接
    handle_events(epollfd,events,ret,listenfd,buf);
}

//事件处理函数
static void handle_events(int epollfd,struct epoll_event *events,int num,int listenfd,char*buf)
{
     int i;
     int fd;
     //进行遍历;这里只要遍历已经准备好的io事件。num并不是当初epoll_create时的FDSIZE。
     for (i = 0;i < num;i++)
     {
         fd = events[i].data.fd;
        //根据描述符的类型和事件类型进行处理
         if ((fd == listenfd) &&(events[i].events & EPOLLIN))
            handle_accpet(epollfd,listenfd);
         else if (events[i].events & EPOLLIN)
            do_read(epollfd,fd,buf);
         else if (events[i].events & EPOLLOUT)
            do_write(epollfd,fd,buf);
     }
}

//添加事件
static void add_event(int epollfd,int fd,int state){
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_ADD,fd,&ev);
}

//处理接收到的连接
static void handle_accpet(int epollfd,int listenfd){
     int clifd;
     struct sockaddr_in cliaddr;
     socklen_t  cliaddrlen;
     clifd = accept(listenfd,(struct sockaddr*)&cliaddr,&cliaddrlen);
     if (clifd == -1)
     perror("accpet error:");
     else {
         printf("accept a new client: %s:%d\n",inet_ntoa(cliaddr.sin_addr),cliaddr.sin_port);                       //添加一个客户描述符和事件
         add_event(epollfd,clifd,EPOLLIN);
     }
}

//读处理
static void do_read(int epollfd,int fd,char *buf){
    int nread;
    nread = read(fd,buf,MAXSIZE);
    if (nread == -1)     {
        perror("read error:");
        close(fd); //记住close fd
        delete_event(epollfd,fd,EPOLLIN); //删除监听
    }
    else if (nread == 0)     {
        fprintf(stderr,"client close.\n");
        close(fd); //记住close fd
        delete_event(epollfd,fd,EPOLLIN); //删除监听
    }
    else {
        printf("read message is : %s",buf);
        //修改描述符对应的事件,由读改为写
        modify_event(epollfd,fd,EPOLLOUT);
    }
}

//写处理
static void do_write(int epollfd,int fd,char *buf) {
    int nwrite;
    nwrite = write(fd,buf,strlen(buf));
    if (nwrite == -1){
        perror("write error:");
        close(fd);   //记住close fd
        delete_event(epollfd,fd,EPOLLOUT);  //删除监听
    }else{
        modify_event(epollfd,fd,EPOLLIN);
    }
    memset(buf,0,MAXSIZE);
}

//删除事件
static void delete_event(int epollfd,int fd,int state) {
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_DEL,fd,&ev);
}

//修改事件
static void modify_event(int epollfd,int fd,int state){
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_MOD,fd,&ev);
}
```

//注: 另外一端我就省了
四 epoll总结
在 select/poll中,进程只有在调用一定的方法后,内核才对所有监视的文件描述符进行扫描,而epoll事先通过epoll_ctl()来注册一 个文件描述符,一旦基于某个文件描述符就绪时,内核会采用类似callback的回调机制,迅速激活这个文件描述符,当进程调用epoll_wait() 时便得到通知。(此处去掉了遍历文件描述符,而是通过监听回调的的机制。这正是epoll的魅力所在。)

epoll的优点主要是一下几个方面:

1. 监视的描述符数量不受限制, 它所支持的 FD上限是最大可以打开文件的数目, 这个数字一般远大于2048, 举个例子, 在 1GB内存的机器上大约是10万左右, 具体数目可以 cat /proc/sys/fs/file-max 察看, 一般来说这个数目和系统内存关系很大。select 的最大缺点就是进程打开的 fd 是有数量限制的。这对于连接数量比较大的服务器来说根本不能满足。虽然也可以选择多进程的解决方案( Apache就是这样实现的),不过虽然linux上面创建进程的代价比较小,但仍旧是不可忽视的,加上进程间数据同步远比不上线程间同步的高效,所以也不是一种完美的方案。

IO的效率不会随着监视fd的数量的增长而下降。epoll不同于select和poll轮询的方式,而是通过每个fd定义的回调函数来实现的。只有就绪的fd才会执行回调函数。
如果没有大量的idle -connection或者dead-connection,epoll的效率并不会比select/poll高很多,但是当遇到大量的idle- connection,就会发现epoll的效率大大高于select/poll。

参考
用户空间与内核空间,进程上下文与中断上下文[总结]
进程切换
维基百科-文件描述符
Linux 中直接 I/O 机制的介绍
IO - 同步,异步,阻塞,非阻塞  (亡羊补牢篇)
Linux中select poll和epoll的区别
IO多路复用之select总结
IO多路复用之poll总结
IO多路复用之epoll总结

### Kqueue

Kqueue专用于FreeBSD系统,只能用于UFS文件系统

kqueue类似epoll,支持每个进程中有多个上下文(兴趣集)。

kqueue设计的目的并非是为了替代基于 socket 事件复用技术的select()/poll(),而是提供一般化的机制来处理多种操作系统事件。

kqueue API由两个函数调用 ( kqueue()与kevent()) 和一个辅助设置事件的宏组成。
————————————————
版权声明: 本文为CSDN博主「白夜行515」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/baiye_xing/article/details/76360247>

### LT, ET

边缘触发(Edge Trigger)和条件触发(Level Trigger)  

epoll的两种模式,电平触发和边沿触发。

1.电平触发效率较边沿触发低,电平触发模式下,当epoll_wait返回的事件没有全部相应处理完毕,内核缓冲区还存在数据时,会反复通知,直到处理完成。epoll默认使用这种模式。

2.边沿触发效率较高,内核缓冲区事件只通知一次。

<https://bingowith.me/2019/10/03/et-lt-intro/>

这两个名词应该来源于电气,用于激活电路.摘取一段爆栈网的回答:

Level Triggering: In level triggering the circuit will become active when the gating or clock pulse is on a particular level. This level is decided by the designer. We can have a negative level triggering in which the circuit is active when the clock signal is low or a positive level triggering in which the circuit is active when the clock signal is high.
Edge Triggering: In edge triggering the circuit becomes active at negative or positive edge of the clock signal. For example if the circuit is positive edge triggered, it will take input at exactly the time in which the clock signal goes from low to high. Similarly input is taken at exactly the time in which the clock signal goes from high to low in negative edge triggering. But keep in mind after the the input, it can be processed in all the time till the next input is taken.

来源.
翻译就是LT是根据设定的阈值来控制是否激发而ET是根据信号的高到低或低到高这个变化来控制.

字面意思上level就是水平指的是某值,而edge是边,是值和值之间的变迁.
用来控制操作是否进行的一种机制.

对应于epoll中的概念也类似.
拿文档中的例子:

The file descriptor that represents the read side of a pipe (rfd) is registered on the epoll instance.
A pipe writer writes 2 kB of data on the write side of the pipe.
A call to epoll_wait(2) is done that will return rfd as a ready file descriptor.
The pipe reader reads 1 kB of data from rfd.
A call to epoll_wait(2) is done.
使用LT的话,因为依旧有1KB残留所以wait会立即返回开始下一次操作,而ET这次变迁已经结束了,但因为没有处理完所以后续变化也不会再返回了.(Since the read operation done in 4 does not consume the whole buffer data, the call to epoll_wait(2) done in step 5 might block indefinitely.)

ET在使用上建议遵循以下的规则:

i with nonblocking file descriptors; and
ii by waiting for an event only after read(2) or write(2)
return EAGAIN.

非阻塞的文件描述符(FD或SD)以及要read或write在返回EAGAIN的情况下才开始这个描述符的下一次事件监听.(对于网络IO来说也可能是EWOULDBLOCK, 表示被标记为非阻塞的操作会发生阻塞的异常)

相对来说使用ET的要求和操作会需要更严谨一些,当然LT写得有问题,比如漏了一个事件的处理,可能会导致出现跑满CPU的死循环.

选择
ET的问题主要是需要更严谨的操作,而LT是更频繁的wait唤醒.
在某种程度上,ET更加’惰性’而LT更加积极,你如果不处理或者还不想处理就会反复收到事件,除非你取消注册他.
所以在不少java的NIO代码中,常常会有channel在读后取消读注册写,在写后取消写注册读的代码,当可以写,但是写的内容还没准备好时,使用LT会遇到不少问题(所以一般是准备写的内容已经好了,再给channel注册上写的兴趣).
ET在读上会更加麻烦,不读完等到返回EAGAIN,该描述符可能之后的事件触发就会有问题.
具体还需要看自己的需求和场景.
此外多线程场景下,在同一个描述符上等待ET是保证只会唤醒一个线程,但要注意多个不同的数据块请求可能会导致在一个FD/SD上返回多个事件,需要使用EPOLLONESHOT来确保只返回一个(这个flag是接受到一个事件后就解绑和FD/SD关系的).

java中只支持LT,netty通过JNI实现了ET,选择的原因在一个邮件里提到了一些Any reason why select() uses only level-triggered notification mode?.
大致的意思是ET和I/O提供的方法更加耦合,可能是为了更高的兼容性放弃了这个机制的提供吧.

这边就进行了简单的一些资料整合,没有涉及到更深的内容,如果文中有什么错误欢迎评论.

参考资料:
<https://netty.io/wiki/native-transports.html>

<http://man7.org/linux/man-pages/man7/epoll.7.html>

<https://github.com/tokio-rs/mio>

### libevent介绍

Libevent 是一个用C语言编写的、轻量级的开源高性能事件通知库,主要有以下几个亮点: 事件驱动 ( event-driven) ,高性能;轻量级,专注于网络,不如 ACE 那么臃肿庞大；源代码相当精炼、易读；跨平台,支持 Windows、 Linux、 *BSD 和 Mac Os；支持多种 I/O 多路复用技术, epoll、 poll、 dev/poll、 select 和 kqueue 等；支持 I/O,定时器和信号等事件；注册事件优先级。
Libevent 已经被广泛的应用,作为底层的网络库；比如 memcached、 Vomit、 Nylon、 Netchat等等。

---

<https://segmentfault.com/a/1190000003063859>
  
<https://zhuanlan.zhihu.com/p/22803683>

<https://zhuanlan.zhihu.com/p/36764771>

<https://www.cnblogs.com/fg123/p/5256553.html>

<http://luodw.cc/2016/01/24/epoll/>
><https://wiyi.org/linux-io-model.html>
