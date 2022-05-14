---
title: unix domain socket, UDS
author: "-"
date: 2015-08-26T00:50:32+00:00
url: uds
categories:
  - Linux
tags:
  - reprint
---
## unix domain socket, UDS

    ss -nxp
    ss -nxlp

http://blog.csdn.net/bingqingsuimeng/article/details/8470029

http://blog.chinaunix.net/uid-20511624-id-1659107.html


什么是Socket
  
Socket接口是TCP/IP网络的API，Socket接口定义了许多函数或例程，程式员能够用他们来研发TCP/IP网络上的应用程式。要学Internet上的TCP/IP网络编程，必须理解Socket接口。
  
Socket接口设计者最先是将接口放在Unix操作系统里面的。假如了解 Unix 系统的输入和输出的话，就很容易了解 Socket 了。网络的 Socket数据传输是一种特别的I/O，Socket也是一种文档描述符。Socket也具备一个类似于打开文档的函数调用Socket()，该函数返回一个整型的Socket描述符，随后的连接建立、数据传输等操作都是通过该Socket实现的。常用的Socket类型有两种: 流式Socket  (SOCK_STREAM) 和数据报式Socket (SOCK_DGRAM) 。流式是一种面向连接的Socket，针对于面向连接的TCP服务应用；数据报式Socket是一种无连接的Socket，对应于无连接的UDP服务应用。
  
Socket 建立
  
为了建立Socket，程式能够调用Socket函数，该函数返回一个类似于文档描述符的句柄。socket函数原型为: 
  
int socket(int domain, int type, int protocol);
  
domain指明所使用的协议族，通常为PF_INET，表示互连网协议族 (TCP/IP协议族) ；type参数指定socket的类型:  SOCK_STREAM 或SOCK_DGRAM，Socket接口还定义了原始Socket (SOCK_RAW) ，允许程式使用低层协议；protocol通常赋值"0"。 Socket()调用返回一个整型socket描述符，您能够在后面的调用使用他。
  
Socket描述符是个指向内部数据结构的指针，他指向描述符表入口。调用Socket函数时，socket执行体将建立一个Socket，实际上"建立一个Socket"意味着为一个Socket数据结构分配存储空间。Socket执行体为您管理描述符表。
  
两个网络程式之间的一个网络连接包括五种信息: 通信协议、本地协议地址、本地主机端口、远端主机地址和远端协议端口。Socket数据结构中包含这五种信息。
  
Socket配置
  
通过socket调用返回一个socket描述符后，在使用socket进行网络传输以前，必须配置该socket。面向连接的socket客户端通过调用Connect函数在socket数据结构中保存本地和远端信息。无连接socket的客户端和服务端连同面向连接socket的服务端通过调用 bind函数来配置本地信息。
  
Bind函数将socket和本机上的一个端口相关联，随后您就能够在该端口监听服务请求。Bind函数原型为: 
  
int bind(int sockfd,struct sockaddr *my_addr, int addrlen);
  
Sockfd是调用socket函数返回的socket描述符,my_addr是个指向包含有本机IP地址及端口号等信息的sockaddr类型的指针；addrlen常被配置为sizeof(struct sockaddr)。
  
struct sockaddr结构类型是用来保存socket信息的: 
  
struct sockaddr {
  
unsigned short sa_family; /* 地址族， AF_xxx */
  
char sa_data[14]; /* 14 字节的协议地址 */
  
};
  
sa_family一般为AF_INET，代表Internet (TCP/IP) 地址族；sa_data则包含该socket的IP地址和端口号。
  
另外更有一种结构类型: 
  
struct sockaddr_in {
  
short int sin_family; /* 地址族 */
  
unsigned short int sin_port; /* 端口号 */
  
struct in_addr sin_addr; /* IP地址 */
  
unsigned char sin_zero[8]; /* 填充0 以保持和struct sockaddr同样大小 */
  
};
  
这个结构更方便使用。sin_zero用来将sockaddr_in结构填充到和struct sockaddr同样的长度，能够用bzero()或memset()函数将其置为零。指向sockaddr_in 的指针和指向sockaddr的指针能够相互转换，这意味着假如一个函数所需参数类型是sockaddr时，您能够在函数调用的时候将一个指向 sockaddr_in的指针转换为指向sockaddr的指针；或相反。
  
使用bind函数时，能够用下面的赋值实现自动获得本机IP地址和随机获取一个没有被占用的端口号: 
  
my_addr.sin_port = 0; /* 系统随机选择一个未被使用的端口号 */
  
my_addr.sin_addr.s_addr = INADDR_ANY; /* 填入本机IP地址 */
  
通过将my_addr.sin_port置为0，函数会自动为您选择一个未占用的端口来使用。同样，通过将my_addr.sin_addr.s_addr置为INADDR_ANY，系统会自动填入本机IP地址。
  
注意在使用bind函数是需要将sin_port和sin_addr转换成为网络字节优先顺序；而sin_addr则无需转换。
  
电脑数据存储有两种字节优先顺序: 高位字节优先和低位字节优先。Internet上数据以高位字节优先顺序在网络上传输，所以对于在内部是以低位字节优先方式存储数据的机器，在Internet上传输数据时就需要进行转换，否则就会出现数据不一致。
  
下面是几个字节顺序转换函数: 
  
·htonl(): 把32位值从主机字节序转换成网络字节序
  
·htons(): 把16位值从主机字节序转换成网络字节序
  
·ntohl(): 把32位值从网络字节序转换成主机字节序
  
·ntohs(): 把16位值从网络字节序转换成主机字节序
  
Bind()函数在成功被调用时返回0；出现错误时返回"-1"并将errno置为相应的错误号。需要注意的是，在调用bind函数时一般不要将端口号置为小于1024的值，因为1到1024是保留端口号，您能够选择大于1024中的任何一个没有被占用的端口号。
  
连接建立
  
面向连接的客户程式使用Connect函数来配置socket并和远端服务器建立一个TCP连接，其函数原型为: 
  
int connect(int sockfd, struct sockaddr *serv_addr,int addrlen);
  
Sockfd 是socket函数返回的socket描述符；serv_addr是包含远端主机IP地址和端口号的指针；addrlen是远端地质结构的长度。 Connect函数在出现错误时返回-1，并且配置errno为相应的错误码。进行客户端程式设计无须调用bind()，因为这种情况下只需知道目的机器的IP地址，而客户通过哪个端口和服务器建立连接并无需关心，socket执行体为您的程式自动选择一个未被占用的端口，并通知您的程式数据什么时候到打断口。
  
Connect函数启动和远端主机的直接连接。只有面向连接的客户程式使用socket时才需要将此socket和远端主机相连。无连接协议从不建立直接连接。面向连接的服务器也从不启动一个连接，他只是被动的在协议端口监听客户的请求。
  
Listen函数使socket处于被动的监听模式，并为该socket建立一个输入数据队列，将到达的服务请求保存在此队列中，直到程式处理他们。
  
int listen(int sockfd， int backlog);
  
Sockfd 是Socket系统调用返回的socket 描述符；backlog指定在请求队列中允许的最大请求数，进入的连接请求将在队列中等待accept()他们 (参考下文) 。Backlog对队列中等待服务的请求的数目进行了限制，大多数系统缺省值为20。假如一个服务请求到来时，输入队列已满，该socket将拒绝连接请求，客户将收到一个出错信息。
  
当出现错误时listen函数返回-1，并置相应的errno错误码。
  
accept()函数让服务器接收客户的连接请求。在建立好输入队列后，服务器就调用accept函数，然后睡眠并等待客户的连接请求。
  
int accept(int sockfd, void \*addr, int \*addrlen);
  
sockfd是被监听的socket描述符，addr通常是个指向sockaddr_in变量的指针，该变量用来存放提出连接请求服务的主机的信息 (某台主机从某个端口发出该请求) ；addrten通常为一个指向值为sizeof(struct sockaddr_in)的整型指针变量。出现错误时accept函数返回-1并置相应的errno值。
  
首先，当accept函数监控的 socket收到连接请求时，socket执行体将建立一个新的socket，执行体将这个新socket和请求连接进程的地址联系起来，收到服务请求的初始socket仍能够继续在以前的 socket上监听，同时能够在新的socket描述符上进行数据传输操作。
  
数据传输
  
Send()和recv()这两个函数用于面向连接的socket上进行数据传输。
  
Send()函数原型为: 
  
int send(int sockfd, const void *msg, int len, int flags);
  
Sockfd是您想用来传输数据的socket描述符；msg是个指向要发送数据的指针；Len是以字节为单位的数据的长度；flags一般情况下置为0 (关于该参数的用法可参照man手册) 。
  
Send()函数返回实际上发送出的字节数，可能会少于您希望发送的数据。在程式中应该将send()的返回值和欲发送的字节数进行比较。当send()返回值和len不匹配时，应该对这种情况进行处理。
  
char *msg = "Hello!";
  
int len, bytes_sent;
  
……
  
len = strlen(msg);
  
bytes_sent = send(sockfd, msg,len,0);
  
……
  
recv()函数原型为: 
  
int recv(int sockfd,void *buf,int len,unsigned int flags);
  
Sockfd是接受数据的socket描述符；buf 是存放接收数据的缓冲区；len是缓冲的长度。Flags也被置为0。Recv()返回实际上接收的字节数，当出现错误时，返回-1并置相应的errno值。
  
Sendto()和recvfrom()用于在无连接的数据报socket方式下进行数据传输。由于本地socket并没有和远端机器建立连接，所以在发送数据时应指明目的地址。
  
sendto()函数原型为: 
  
int sendto(int sockfd, const void \*msg,int len,unsigned int flags,const struct sockaddr \*to, int tolen);
  
该函数比send()函数多了两个参数，to表示目地机的IP地址和端口号信息，而tolen常常被赋值为sizeof (struct sockaddr)。Sendto 函数也返回实际发送的数据字节长度或在出现发送错误时返回-1。
  
Recvfrom()函数原型为: 
  
int recvfrom(int sockfd,void \*buf,int len,unsigned int flags,struct sockaddr \*from,int *fromlen);
  
from是个struct sockaddr类型的变量，该变量保存源机的IP地址及端口号。fromlen常置为sizeof (struct sockaddr)。当recvfrom()返回时，fromlen包含实际存入from中的数据字节数。Recvfrom()函数返回接收到的字节数或当出现错误时返回-1，并置相应的errno。
  
假如您对数据报socket调用了connect()函数时，您也能够利用send()和recv()进行数据传输，但该socket仍然是数据报socket，并且利用传输层的UDP服务。但在发送或接收数据报时，内核会自动为之加上目地和源地址信息。
  
结束传输
  
当任何的数据操作结束以后，您能够调用close()函数来释放该socket，从而停止在该socket上的任何数据操作: 
  
close(sockfd);
  
您也能够调用shutdown()函数来关闭该socket。该函数允许您只停止在某个方向上的数据传输，而一个方向上的数据传输继续进行。如您能够关闭某socket的写操作而允许继续在该socket上接受数据，直至读入任何数据。
  
int shutdown(int sockfd,int how);
  
Sockfd是需要关闭的socket的描述符。参数 how允许为shutdown操作选择以下几种方式: 
  
·0---不允许继续接收数据
  
·1---不允许继续发送数据
  
·2---不允许继续发送和接收数据，
  
·均为允许则调用close ()
  
shutdown在操作成功时返回0，在出现错误时返回-1并置相应errno。
  
Socket编程实例
  
代码实例中的服务器通过socket连接向客户端发送字符串"Hello, you are connected!"。只要在服务器上运行该服务器软件，在客户端运行客户软件，客户端就会收到该字符串。
  
该服务器软件代码如下: 
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#define SERVPORT 3333 /*服务器监听端口号 */
  
#define BACKLOG 10 /* 最大同时连接请求数 */
  
main()
  
{
  
int sockfd,client_fd; /*sock_fd: 监听socket；client_fd: 数据传输socket */
  
struct sockaddr_in my_addr; /* 本机地址信息 */
  
struct sockaddr_in remote_addr; /* 客户端地址信息 */
  
if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
  
perror("socket创建出错！"); exit(1);
  
}
  
my_addr.sin_family=AF_INET;
  
my_addr.sin_port=htons(SERVPORT);
  
my_addr.sin_addr.s_addr = INADDR_ANY;
  
bzero(&(my_addr.sin_zero),8);
  
if (bind(sockfd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr)) == -1) {
  
perror("bind出错！");
  
exit(1);
  
}
  
if (listen(sockfd, BACKLOG) == -1) {
  
perror("listen出错！");
  
exit(1);
  
}
  
while(1) {
  
sin_size = sizeof(struct sockaddr_in);
  
if ((client_fd = accept(sockfd, (struct sockaddr *)&remote_addr, &sin_size)) == -1) {
  
perror("accept出错");
  
continue;
  
}
  
printf("received a connection from %s\n", inet_ntoa(remote_addr.sin_addr));
  
if (!fork()) { /* 子进程代码片段 */
  
if (send(client_fd, "Hello, you are connected!\n", 26, 0) == -1)
  
perror("send出错！");
  
close(client_fd);
  
exit(0);
  
}
  
close(client_fd);
  
}
  
}
  
}
  
服务器的工作流程是这样的: 首先调用socket函数创建一个Socket，然后调用bind函数将其和本机地址连同一个本地端口号绑定，然后调用 listen在相应的socket上监听，当accpet接收到一个连接服务请求时，将生成一个新的socket。服务器显示该客户机的IP地址，并通过新的socket向客户端发送字符串"Hello，you are connected!"。最后关闭该socket。
  
代码实例中的fork()函数生成一个子进程来处理数据传输部分，fork()语句对于子进程返回的值为0。所以包含fork函数的if语句是子进程代码部分，他和if语句后面的父进程代码部分是并发执行的。
  
客户端程式代码如下: 
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#define SERVPORT 3333
  
#define MAXDATASIZE 100 /*每次最大数据传输量 */
  
main(int argc, char *argv[]){
  
int sockfd, recvbytes;
  
char buf[MAXDATASIZE];
  
struct hostent *host;
  
struct sockaddr_in serv_addr;
  
if (argc h_addr);
  
bzero(&(serv_addr.sin_zero),8);
  
if (connect(sockfd, (struct sockaddr *)&serv_addr, \
  
sizeof(struct sockaddr)) == -1) {
  
perror("connect出错！");
  
exit(1);
  
}
  
if ((recvbytes=recv(sockfd, buf, MAXDATASIZE, 0)) ==-1) {
  
perror("recv出错！");
  
exit(1);
  
}
  
buf[recvbytes] = '\0';
  
printf("Received: %s",buf);
  
close(sockfd);
  
}
  
客户端程式首先通过服务器域名获得服务器的IP地址，然后创建一个socket，调用connect函数和服务器建立连接，连接成功之后接收从服务器发送过来的数据，最后关闭socket。
  
函数gethostbyname()是完成域名转换的。由于IP地址难以记忆和读写，所以为了方便，人们常常用域名来表示主机，这就需要进行域名和IP地址的转换。函数原型为: 
  
struct hostent \*gethostbyname(const char \*name);
  
函数返回为hosten的结构类型，他的定义如下: 
  
struct hostent {
  
char \*h_name; /* 主机的官方域名 */
  
char *\*h_aliases; /* 一个以NULL结尾的主机别名数组 */
  
int h_addrtype; /* 返回的地址类型，在Internet环境下为AF-INET */
  
int h_length; /* 地址的字节长度 */
  
char *\*h_addr_list; /* 一个以0结尾的数组，包含该主机的任何地址*/
  
};
  
#define h_addr h_addr_list[0] /*在h-addr-list中的第一个地址*/
  
当 gethostname()调用成功时，返回指向struct hosten的指针，当调用失败时返回-1。当调用gethostbyname时，您不能使用perror()函数来输出错误信息，而应该使用herror()函数来输出。
  
无连接的客户/服务器程式的在原理上和连接的客户/服务器是相同的，两者的区别在于无连接的客户/服务器中的客户一般无需建立连接，而且在发送接收数据时，需要指定远端机的地址。
  
阻塞和非阻塞
  
阻塞函数在完成其指定的任务以前不允许程式调用另一个函数。例如，程式执行一个读数据的函数调用时，在此函数完成读操作以前将不会执行下一程式语句。当服务器运行到accept语句时，而没有客户连接服务请求到来，服务器就会停止在accept语句上等待连接服务请求的到来。这种情况称为阻塞 (blocking) 。而非阻塞操作则能够立即完成。比如，假如您希望服务器仅仅注意检查是否有客户在等待连接，有就接受连接，否则就继续做其他事情，则能够通过将Socket配置为非阻塞方式来实现。非阻塞socket在没有客户在等待时就使accept调用立即返回。
  
#include
  
#include
  
……
  
sockfd = socket(AF_INET,SOCK_STREAM,0);
  
fcntl(sockfd,F_SETFL,O_NONBLOCK)；
  
……
  
通过配置socket为非阻塞方式，能够实现"轮询"若干Socket。当企图从一个没有数据等待处理的非阻塞Socket读入数据时，函数将立即返回，返回值为-1，并置errno值为EWOULDBLOCK。但是这种"轮询"会使CPU处于忙等待方式，从而降低性能，浪费系统资源。而调用 select()会有效地解决这个问题，他允许您把进程本身挂起来，而同时使系统内核监听所需要的一组文档描述符的任何活动，只要确认在任何被监控的文档描述符上出现活动，select()调用将返回指示该文档描述符已准备好的信息，从而实现了为进程选出随机的变化，而不必由进程本身对输入进行测试而浪费 CPU开销。Select函数原型为:
  
int select(int numfds,fd_set \*readfds,fd_set \*writefds，
  
fd_set \*exceptfds,struct timeval \*timeout);
  
其中readfds、writefds、exceptfds分别是被select()监控的读、写和异常处理的文档描述符集合。假如您希望确定是否能够从标准输入和某个socket描述符读取数据，您只需要将标准输入的文档描述符0和相应的sockdtfd加入到readfds集合中；numfds的值是需要检查的号码最高的文档描述符加1，这个例子中numfds的值应为sockfd+1；当select返回时，readfds将被修改，指示某个文档描述符已准备被读取，您能够通过FD_ISSSET()来测试。为了实现fd_set中对应的文档描述符的配置、复位和测试，他提供了一组宏: 
  
FD_ZERO(fd_set *set)--清除一个文档描述符集；
  
FD_SET(int fd,fd_set *set)--将一个文档描述符加入文档描述符集中；
  
FD_CLR(int fd,fd_set *set)--将一个文档描述符从文档描述符集中清除；
  
FD_ISSET(int fd,fd_set *set)--试判断是否文档描述符被置位。
  
Timeout参数是个指向struct timeval类型的指针，他能够使select()在等待timeout长时间后没有文档描述符准备好即返回。struct timeval数据结构为: 
  
struct timeval {
  
int tv_sec; /* seconds */
  
int tv_usec; /* microseconds */
  
};
  
POP3客户端实例
  
下面的代码实例基于POP3的客户协议，和邮件服务器连接并取回指定用户帐号的邮件。和邮件服务器交互的命令存储在字符串数组POPMessage中，程式通过一个do-while循环依次发送这些命令。
  
```c
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#include
  
#define POP3SERVPORT 110
  
#define MAXDATASIZE 4096
  
main(int argc, char *argv[]){
  
int sockfd;
  
struct hostent *host;
  
struct sockaddr_in serv_addr;
  
char *POPMessage[]={
  
"USER userid\r\n",
  
"PASS password\r\n",
  
"STAT\r\n",
  
"LIST\r\n",
  
"RETR 1\r\n",
  
"DELE 1\r\n",
  
"QUIT\r\n",
  
NULL
  
};
  
int iLength;
  
int iMsg=0;
  
int iEnd=0;
  
char buf[MAXDATASIZE];
  
if((host=gethostbyname("your.server"))==NULL) {
  
perror("gethostbyname error");
  
exit(1);
  
}
  
if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
  
perror("socket error");
  
exit(1);
  
}
  
serv_addr.sin_family=AF_INET;
  
serv_addr.sin_port=htons(POP3SERVPORT);
  
serv_addr.sin_addr = \*((struct in_addr \*)host->h_addr);
  
bzero(&(serv_addr.sin_zero),8);
  
if (connect(sockfd, (struct sockaddr *)&serv_addr,sizeof(struct sockaddr))==-1){
  
perror("connect error");
  
exit(1);
  
}
  
do {
  
send(sockfd,POPMessage[iMsg],strlen(POPMessage[iMsg]),0);
  
printf("have sent: %s",POPMessage[iMsg]);
  
iLength=recv(sockfd,buf+iEnd,sizeof(buf)-iEnd,0);
  
iEnd+=iLength;
  
buf[iEnd]='\0';
  
printf("received: %s,%d\n",buf,iMsg);
  
iMsg++;
  
} while (POPMessage[iMsg]);
  
close(sockfd);
  
}
  
```
Unix/Linux环境下的Socket编程
  
网络的Socket数据传输是一种特别的I/O，Socket也是一种文档描述符。 Socket也具备一个类似于打开文档的函数调用Socket()，该函数返回一个整型的Socket描述符，随后的连接建立、数据传输等操作都是通过该 Socket实现的。常用的Socket类型有两种: 流式Socket  (SOCK_STREAM) 和数据报式Socket (SOCK_DGRAM) 。流式是一种面向连接的Socket，针对于面向连接的TCP服务应用；数据报式Socket是一种无连接的Socket，对应于无连接的UDP服务应用。
  
Socket描述符是个指向内部数据结构的指针，他指向描述符表入口。调用Socket函数时，socket执行体将建立一个Socket，实际上"建立一个Socket"意味着为一个Socket数据结构分配存储空间。Socket执行体为您管理描述符表。两个网络程式之间的一个网络连接包括五种信息: 通信协议、本地协议地址、本地主机端口、远端主机地址和远端协议端口。Socket数据结构中包含这五种信息。
  
struct sockaddr结构类型是用来保存socket信息的: 
  
struct sockaddr {
  
unsigned short sa_family; /* 地址族， AF_xxx */
  
char sa_data[14]; /* 14 字节的协议地址 */
  
};
  
sa_family一般为AF_INET，代表Internet (TCP/IP) 地址族；sa_data则包含该socket的IP地址和
  
端口号。
  
另外更有一种结构类型: 
  
struct sockaddr_in {
  
short int sin_family; /* 地址族 */
  
unsigned short int sin_port; /* 端口号 */
  
struct in_addr sin_addr; /* IP地址 */
  
unsigned char sin_zero[8]; /* 填充0 以保持和struct sockaddr同样大小 */
  
};
  
能够用bzero()或memset()函数将其置为零。指向sockaddr_in 的指针和指向sockaddr的指针能够相
  
互转换，这意味着假如一个函数所需参数类型是sockaddr时，您能够在函数调用的时候将一个指向
  
sockaddr_in的指针转换为指向sockaddr的指针；或相反。
  
在使用bind函数是需要将sin_port和sin_addr转换成为网络字节优先顺序；而sin_addr则无需转换。
  
电脑数据存储有两种字节优先顺序: 高位字节优先和低位字节优先。Internet上数据以高位字节
  
优先顺序在网络上传输，所以对于在内部是以低位字节优先方式存储数据的机器，在Internet上传输数
  
据时就需要进行转换，否则就会出现数据不一致。
  
下面是几个字节顺序转换函数: 
  
·htonl(): 把32位值从主机字节序转换成网络字节序
  
·htons(): 把16位值从主机字节序转换成网络字节序
  
·ntohl(): 把32位值从网络字节序转换成主机字节序
  
·ntohs(): 把16位值从网络字节序转换成主机字节序
  
Bind()函数在成功被调用时返回0；出现错误时返回"-1"并将errno置为相应的错误号。需要注意的
  
是，在调用bind函数时一般不要将端口号置为小于1024的值，因为1到1024是保留端口号，您能够选择
  
大于1024中的任何一个没有被占用的端口号。
  
连接建立
  
面向连接的客户程式使用Connect函数来配置socket并和远端服务器建立一个TCP连接，其函数原型为: int connect(int sockfd, struct sockaddr *serv_addr,int addrlen); Sockfd是socket函数返回的socket描述符；serv_addr是包含远端主机IP地址和端口号的指针；addrlen是远端地址结构的长度。Connect函数在出现错误时返回-1，并且配置errno为相应的错误码。进行客户端程式设计无须调用bind()，因为这种情况下只需知道目的机器的IP地址，而客户通过哪个端口和服务器建立连接并无需关心，socket执行体为您的程式自动选择一个未被占用的端口，并通知您的程式数据什么时候到打断口。Connect 函数启动和远端主机的直接连接。只有面向连接的客户程式使用socket时才需要将此socket和远端主机相连。无连接协议从不建立直接连接。面向连接的务器也从不启动一个连接，他只是被动的在协议端口监听客户的请求。
  
Listen函数使socket处于被动的监听模式，并为该socket建立一个输入数据队列，将到达的服务请求
  
保存在此队列中，直到程式处理他们。 int listen(int sockfd， int backlog); Sockfd 是Socket系统调用返回的socket 描述符；backlog指定在请求队列中允许的最大请求数，进入的连接请求将在队列中等待accept()他们 (参考下文) 。Backlog对队列中等待服务的请求的数目进行了限制，大多数系统缺省值为20。假如一个服务请求到来时，输入队列已满，该 socket将拒绝连接请求，客户将收到一个出错信息。当出现错误时listen函数返回-1，并置相应的errno错误码。

accept()函数让服务器接收客户的连接请求。在建立好输入队列后，服务器就调用accept函数，然后
  
睡眠并等待客户的连接请求。int accept(int sockfd, void \*addr, int \*addrlen); sockfd是被监听的socket描述符，addr通常是个指向sockaddr_in变量的指针，该变量用来存放提出连接请求服务的主机的信息 (某台主机从某个端口发出该请求) ；addrlen通常为一个指向值为sizeof(struct sockaddr_in)的整型指针变量。出现错误时accept函数返回-1并置相应的errno值。当accept函数监控的socket收到连接请求时，socket执行体将建立一个新的socket，执行体将这个新socket和请求连接进程的地址联系起来，收到服务请求的初始socket仍能够继续在以前的 socket上监听，同时能够在新的socket描述符上进行数据传输操作。
  
数据传输
  
(面向连接TCP)
  
send()和recv()这两个函数用于面向连接的socket上进行数据传输。Send()函数原型为: 
  
int send(int sockfd, const void *msg, int len, int flags); Sockfd是您想用来传输数据的socket描述符；msg是个指向要发送数据的指针；Len是以字节为单位的数据的长度；flags一般情况下置为0。Send()函数返回实际上发送出的字节数，可能会少于您希望发送的数据。在程式中应该将send()的返回值和欲发送的字节数进行比较。当send()返回值和len不匹配时，应该对这种情况进行处理。
  
int recv(int sockfd,void *buf,int len,unsigned int flags); Sockfd是接受数据的socket描述符；buf 是存放接收数据的缓冲区；len是缓冲的长度。Flags也被置为0。Recv()返回实际上接收的字节数，当出现错误时，返回-1并置相应的errno值。
  
(无连接UDP)
  
sendto()和recvfrom()用于在无连接的数据报socket方式下进行数据传输。由于本地socket并没有和远端机器建立连接，所以在发送数据时应指明目的地址。
  
int sendto(int sockfd, const void \*msg,int len,unsigned int flags,const struct sockaddr \*to, int tolen);该函数比send()函数多了两个参数，to表示目地机的IP地址和端口号信息，而tolen常常被赋值为sizeof (struct sockaddr)。sendto函数也返回实际发送的数据字节长度或在出现发送错误时返回-1。
  
int recvfrom(int sockfd,void \*buf,int len,unsigned int flags,struct sockaddr \*from,int *fromlen); from是个struct sockaddr类型的变量，该变量保存源机的IP地址及端口号。fromlen常置为sizeof (struct sockaddr)。当recvfrom()返回时，fromlen包含实际存入from中的数据字节数。
  
Recvfrom()函数返回接收到的字节数或当出现错误时返回-1，并置相应的errno。
  
结束传输
  
当任何的数据操作结束以后，您能够调用close()函数来释放该socket，从而停止在该socket上的任
  
何数据操作: close(sockfd); 也能够调用shutdown()函数来关闭该socket。该函数允许您只停止在某个方向上的数据传输，而一个方向上的数据传输继续进行。如您能够关闭某socket的写操作而允许继续在该socket上接受数据，直至读入任何数据。Sockfd 是需要关闭的socket的描述符。参数 how允许为shutdown操作选择以下几种方式: 0---不允许继续接收数据 1---不允许继续发送数据 2---不允许继续发送和接收数据，均为允许则调用close () shutdown在操作成功时返回0，在出现错误时返回-1并置相应errno。


socket API原本是为网络通讯设计的，但后来在socket的框架上发展出一种IPC机制，就是UNIXDomain Socket。虽然网络socket也可用于同一台主机的进程间通讯 (通过loopback地址127.0.0.1) ，但是UNIX Domain Socket用于IPC更有效率: 不需要经过网络协议栈，不需要打包拆包、计算校验和、维护序号和应答等，只是将应用层数据从一个进程拷贝到另一个进程。这是因为，IPC机制本质上是可靠的通讯，而网络协议是为不可靠的通讯设计的。UNIX Domain Socket也提供面向流和面向数据包两种API接口，类似于TCP和UDP，但是面向消息的UNIX Domain Socket也是可靠的，消息既不会丢失也不会顺序错乱。

UNIX Domain Socket是全双工的，API接口语义丰富，相比其它IPC机制有明显的优越性，目前已成为使用最广泛的IPC机制，比如X Window服务器和GUI程序之间就是通过UNIX Domain Socket通讯的。

使用UNIX Domain Socket的过程和网络socket十分相似，也要先调用socket()创建一个socket文件描述符，address family指定为AF_UNIX，type可以选择SOCK_DGRAM或SOCK_STREAM，protocol参数仍然指定为0即可。

UNIX Domain Socket与网络socket编程最明显的不同在于地址格式不同，用结构体sockaddr_un表示，网络编程的socket地址是IP地址加端口号，而UNIX Domain Socket的地址是一个socket类型的文件在文件系统中的路径，这个socket文件由bind()调用创建，如果调用bind()时该文件已存在，则bind()错误返回。
  
今天我们介绍如何编写Linux下的TCP程序，关于UDP程序可以参考这里: 

http://blog.csdn.net/htttw/article/details/7519971
  
本文绝大部分是参考《Linux程序设计(第4版)》的第15章 socket 
  
服务器端的步骤如下: 

1. socket:       建立一个socket

2. bind:           将这个socket绑定在某个文件上 (AF_UNIX) 或某个端口上 (AF_INET) ，我们会分别介绍这两种。

3. listen:         开始监听

4. accept:       如果监听到客户端连接，则调用accept接收这个连接并同时新建一个socket来和客户进行通信

5. read/write: 读取或发送数据到客户端

6. close:         通信完成后关闭socket

客户端的步骤如下: 

1. socket:       建立一个socket
  
2. connect:    主动连接服务器端的某个文件 (AF_UNIX) 或某个端口 (AF_INET) 


3. read/write: 如果服务器同意连接 (accept) ，则读取或发送数据到服务器端

4. close:         通信完成后关闭socket
  
上面是整个流程，我们先给出一个例子，具体分析会在之后给出。例子实现的功能是客户端发送一个字符到服务器，服务器将这个字符+1后送回客户端，客户端再把它打印出来: 

Makefile: 


 

all: tcp_client.c tcp_server.c
  
gcc -g -Wall -o tcp_client tcp_client.c
  
gcc -g -Wall -o tcp_server tcp_server.c

clean:
  
rm -rf *.o tcp_client tcp_server

tcp_server.c: 


[cpp][/cpp] 

#include <sys/types.h>
  
#include <sys/socket.h>
  
#include <sys/un.h>
  
#include <unistd.h>
  
#include <stdlib.h>
  
#include <stdio.h>

int main()
  
{
  
/* delete the socket file */
  
unlink("server_socket");

/* create a socket */
  
int server_sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

struct sockaddr_un server_addr;
  
server_addr.sun_family = AF_UNIX;
  
strcpy(server_addr.sun_path, "server_socket");

/* bind with the local file */
  
bind(server_sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));

/* listen */
  
listen(server_sockfd, 5);

char ch;
  
int client_sockfd;
  
struct sockaddr_un client_addr;
  
socklen_t len = sizeof(client_addr);
  
while(1)
  
{
  
printf("server waiting:\n");

/* accept a connection */
  
client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_addr, &len);

/* exchange data */
  
read(client_sockfd, &ch, 1);
  
printf("get char from client: %c\n", ch);
  
++ch;
  
write(client_sockfd, &ch, 1);

/* close the socket */
  
close(client_sockfd);
  
}

return 0;
  
}

tcp_client.c: 


[cpp][/cpp] 

#include <sys/types.h>
  
#include <sys/socket.h>
  
#include <sys/un.h>
  
#include <unistd.h>
  
#include <stdlib.h>
  
#include <stdio.h>

int main()
  
{
  
/* create a socket */
  
int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

struct sockaddr_un address;
  
address.sun_family = AF_UNIX;
  
strcpy(address.sun_path, "server_socket");

/* connect to the server */
  
int result = connect(sockfd, (struct sockaddr *)&address, sizeof(address));
  
if(result == -1)
  
{
  
perror("connect failed: ");
  
exit(1);
  
}

/* exchange data */
  
char ch = 'A';
  
write(sockfd, &ch, 1);
  
read(sockfd, &ch, 1);
  
printf("get char from server: %c\n", ch);

/* close the socket */
  
close(sockfd);

return 0;
  
}


如果我们首先运行tcp_client，会提示没有这个文件: 
  
因为我们是以AF_UNIX方式进行通信的，这种方式是通过文件来将服务器和客户端连接起来的，因此我们应该先运行tcp_server，创建这个文件，默认情况下，这个文件会创建在当前目录下，并且第一个s表示它是一个socket文件: 

程序运行的结果如下图: 
  
下面我们详细讲解: 

1.

我们调用socket函数创建一个socket: 

int socket(int domain, int type, int protocol)

domain: 指定socket所属的域，常用的是AF_UNIX或AF_INET

AF_UNIX表示以文件方式创建socket，AF_INET表示以端口方式创建socket (我们会在后面详细讲解AF_INET) 
  
type: 指定socket的类型，可以是SOCK_STREAM或SOCK_DGRAM

SOCK_STREAM表示创建一个有序的，可靠的，面向连接的socket，因此如果我们要使用TCP，就应该指定为SOCK_STREAM

SOCK_DGRAM表示创建一个不可靠的，无连接的socket，因此如果我们要使用UDP，就应该指定为SOCK_DGRAM
  
protocol: 指定socket的协议类型，我们一般指定为0表示由第一第二两个参数自动选择。
  
socket()函数返回新创建的socket，出错则返回-1

2.

地址格式: 

常用的有两种socket域: AF_UNIX或AF_INET，因此就有两种地址格式: sockaddr_un和sockaddr_in，分别定义如下: 


[cpp][/cpp] 

struct sockaddr_un
  
{
  
sa_family_t sun_family;  /* AF_UNIX */
  
char sun_path[];         /* pathname */
  
}

struct sockaddr_in
  
{
  
short int sin_family;          /* AF_INET */
  
unsigned short int sin_port;   /* port number */
  
struct in_addr sin_addr;       /* internet address */
  
}

其中in_addr正是用来描述一个ip地址的: 


[cpp][/cpp] 

struct in_addr
  
{
  
unsigned long int s_addr;
  
}


从上面的定义我们可以看出，sun_path存放socket的本地文件名，sin_addr存放socket的ip地址，sin_port存放socket的端口号。
  
3.

创建完一个socket后，我们需要使用bind将其绑定: 

int bind(int socket, const struct sockaddr * address, size_t address_len)

如果我们使用AF_UNIX来创建socket，相应的地址格式是sockaddr_un，而如果我们使用AF_INET来创建socket，相应的地址格式是sockaddr_in，因此我们需要将其强制转换为sockaddr这一通用的地址格式类型，而sockaddr_un中的sun_family和sockaddr_in中的sin_family分别说明了它的地址格式类型，因此bind()函数就知道它的真实的地址格式。第三个参数address_len则指明了真实的地址格式的长度。

bind()函数正确返回0，出错返回-1
  
4.

接下来我们需要开始监听了: 

int listen(int socket, int backlog)

backlog: 等待连接的最大个数，如果超过了这个数值，则后续的请求连接将被拒绝

listen()函数正确返回0，出错返回-1
  
5.

接受连接: 

int accept(int socket, struct sockaddr \* address, size_t \* address_len)

同样，第二个参数也是一个通用地址格式类型，这意味着我们需要进行强制类型转化

这里需要注意的是，address是一个传出参数，它保存着接受连接的客户端的地址，如果我们不需要，将address置为NULL即可。

address_len: 我们期望的地址结构的长度，注意，这是一个传入和传出参数，传入时指定我们期望的地址结构的长度，如果多于这个值，则会被截断，而当accept()函数返回时，address_len会被设置为客户端连接的地址结构的实际长度。
  
另外如果没有客户端连接时，accept()函数会阻塞

accept()函数成功时返回新创建的socket描述符，出错时返回-1
  
6.

客户端通过connect()函数与服务器连接: 

int connect(int socket, const struct sockaddr * address, size_t address_len)

对于第二个参数，我们同样需要强制类型转换

address_len指明了地址结构的长度
  
connect()函数成功时返回0，出错时返回-1
  
7.

双方都建立连接后，就可以使用常规的read/write函数来传递数据了

8.

通信完成后，我们需要关闭socket: 

int close(int fd)

close是一个通用函数 (和read，write一样) ，不仅可以关闭文件描述符，还可以关闭socket描述符