---
author: "-"
date: "2020-11-06 16:07:26" 
title: tcp rst, Reset
categories:
  - network
tags:
  - reprint
---
## "tcp rst"

在TCP协议中,rst 段标识复位,用来异常的关闭连接。在TCP的设计中它是不可或缺的, 发送rst段关闭连接时,不必等缓冲区的数据都发送出去, 直接丢弃缓冲区中的数据。而接收端收到 rst 段后,也不必发送 ack 来确认。
监听的一端为服务端,主动连接的一端为客户端。

tcp是全双工的数据通信,也就是说任意一端的连接都可以主动的向对端发送数据。

## 目标端口未监听

服务器程序端口未打开而客户端来连接。这种情况是最为常见和好理解的一种了。去 telnet 一个未打开的 TCP 的端口可能会出现这种错误。这个和操作系统的实现有关。在某些情况下, 操作系统也会完全不理会这些发到未打开端口请求。

比如在下面这种情况下, 主机 241 向主机 114 发送一个 SYN 请求, 表示想要连接主机 114 的 40000 端口, 但是主机 114 上根本没有打开 40000 这个端口, 于是就向主机 241 发送了一个 RST。 这种情况很常见。 特别是服务器程序 core dump 之后重启之前连续出现 RST 的情况会经常发生。

当然在某些操作系统的主机上, 未必是这样的表现。 比如向一台 WINDOWS7 的主机发送一个连接不存在的端口的请求, 这台主机就不会回应。

## 目的主机或者网络路径中防火墙拦截

如果目的主机或者网络路径中显式的设置了对数据包的拦截。

## socket接收缓冲取 Recv-Q 中的数据未完全被应用程序读取时关闭该 socket

python端的socket Recv-Q中有nc发送过来的10个字节未被应用read消费掉。


此时,python调用cli的close方法,则会产生rst

## 向已关闭的socket发送数据

socket调用close,表示本方既没有发送的需求,也没有接收的需求。不同于shutdown

sock connect到60000端口,然后服务端cli调用close,关闭连接。

当前服务端连接处于 FIN_WAIT2 状态。


客户端通过 sock.send 向已关闭的连接发送数据,则会产生 rst。

## 向已关闭的连接发送FIN

cli.close关闭服务端连接,当前服务端连接处于FIN_WAIT2状态,等待对端的FIN段。


服务端的连接在FIN_WAIT2状态超时,当前服务端的连接实际上已经消逝。


此时,客户端调用sock.close()关闭连接,则服务端产生rst。

## 向已经消逝的连接中发送数据
消逝连接指的是,当前这个连接状态操作系统已经不再维护,其数据结构内核已经注销。

比如情况5中socket FIN_WAIT2超时后,其实该连接已经不存在。

再比如半打开(Half Open)连接的对端,由于某种原因已经不存在。

最近在工作中遇到一个由于服务端accept()调用过慢导致的已连接队列满,而客户端是半开打(Half Open)连接的情况下产生rst。

注: 为了方便模拟已连接队列满的情况,将listen socket的backlog参数设置为1。


服务端监听6000端口,并不进行accept。

通过ss命令,可以看到端口 60000 的 Send-Q 为1,代表当前listen socket的已连接队列为1。


通过nc进行连接60000端口,可以看到两个连接都正常建立起来,其中服务端两个连接状态处于ESTABLISHD,但是服务端的PID为-,表示当前socket并没有和进程绑定。

通过ss命令,可以看到,60000端口的Listen socket的Recv-Q的值为2,该值表示已连接队列中有2个连接没有被应用accept取走。


第3个客户端使用nc进行连接,通过netstat查看网络状态,可以看到当前客户端已经完成了握手,而服务端因为已连接队列满,而处于SYN_RECV状态。

SYN_RECV状态的连接存在于listen socket的半连接队列中。


服务端SYN_RECV状态的连接超时以后消逝,而当前第3个nc客户端的连接依然处于ESTABLISHED状态,实际上是一个半打开(Half Open)连接。


对半打开连接进行send操作,则会产生rst。

### rst与 broken pipe
对已关闭的管道进行操作会产生SIGPIPE信号。

网络编程中,对已经收到rst的连接进行io操作会产生SIGPIPE信号。


nc作为服务端监听60000端口,python sock进行连接。


nc服务端进程退出。


向已关闭的连接调用send将产生rst。


向已接收到rst的连接进行send将产生SIGPIPE信号。


https://zhuanlan.zhihu.com/p/30791159


## TCP 连接中出现 RST 的情况

It's fatal. The remote server has sent you a RST packet, which indicates an immediate dropping of the connection, rather than the usual handshake. This bypasses the normal half-closed state transition. I like this description:

"Connection reset by peer" is the TCP/IP equivalent of slamming the phone back on the hook. It's more polite than merely not replying, leaving one hanging. But it's not the FIN-ACK expected of the truly polite TCP/IP converseur.

>https://stackoverflow.com/questions/1434451/what-does-connection-reset-by-peer-mean


>https://my.oschina.net/costaxu/blog/127394

在TCP协议中RST表示复位 ,用来异常的关闭连接, 在TCP的设计中它是不可或缺的。 发送 RST 包关闭连接时, 不必等缓冲区的包都发出去, 直接就丢弃缓存区的包发送RST包。 而接收端收到 RST 包后, 也不必发送ACK包来确认。

其实在网络编程过程中, 各种RST错误其实是比较难排查和找到原因的。下面我列出几种会出现RST的情况。

## 请求超时
  
曾经遇到过这样一个情况:一个客户端连接服务器, connect 返回-1并且 error=EINPROGRESS。 直接 telnet 发现网络连接没有问题。ping没有出现丢包。用抓包工具查看, 客户端是在收到服务器发出的SYN之后就莫名其妙的发送了 RST。

比如像下面这样: 

有 89、27 两台主机。主机89向主机27发送了一个 SYN, 表示希望连接 8888 端口,主机27回应了主机89一个SYN表示可以连接。但是主机27却很不友好,莫名其妙的发送了一个RST表示我不想连接你了。

后来经过排查发现,在主机89上的程序在建立了socket之后,用setsockopt的SO_RCVTIMEO选项设置了recv的超时时间为100ms。而我们看上面的抓包结果表示,从主机89发出SYN到接收SYN的时间多达110ms。 (从15:01:27.799961到15:01:27.961886, 小数点之后的单位是微秒) 。因此主机89上的程序认为接收超时,所以发送了RST拒绝进一步发送数据。

## 提前关闭
  
关于TCP,我想我们在教科书里都读到过一句话,'TCP是一种可靠的连接'。 而这可靠有这样一种含义,那就是操作系统接收到的来自TCP连接中的每一个字节,我都会让应用程序接收到。如果应用程序不接收怎么办？你猜对了,RST。

看两段程序: 

```c
//server.c

int main(int argc, char** argv)
  
{
      
int listen_fd, real_fd;
      
struct sockaddr_in listen_addr, client_addr;
      
socklen_t len = sizeof(struct sockaddr_in);
      
listen_fd = socket(AF_INET, SOCK_STREAM, 0);
      
if(listen_fd == -1)
      
{
          
perror("socket failed ");
          
return -1;
      
}
      
bzero(&listen_addr,sizeof(listen_addr));
      
listen_addr.sin_family = AF_INET;
      
listen_addr.sin_addr.s_addr = htonl(INADDR_ANY);
      
listen_addr.sin_port = htons(SERV_PORT);
      
bind(listen_fd,(struct sockaddr _)&listen_addr, len);
      
listen(listen_fd, WAIT_COUNT);
      
while(1)
      
{
          
real_fd = accept(listen_fd, (struct sockaddr_)&client_addr, &len);
          
if(real_fd == -1)
          
{
              
perror("accpet fail ");
              
return -1;
          
}
          
if(fork() == 0)
          
{
              
close(listen_fd);
              
char pcContent[4096];
              
read(real_fd,pcContent,4096);
              
close(real_fd);
              
exit(0);
          
}
          
close(real_fd);
      
}
      
return 0;
  
}
```
  
这一段是 server 的最简单的代码。逻辑很简单, 监听一个TCP端口然后当有客户端来连接的时候fork一个子进程来处理。注意看的是这一段fork里面的处理: 

char pcContent[4096];
  
read(real_fd,pcContent,4096);
  
close(real_fd);
  
每次只是读socket的前4096个字节,然后就关闭掉连接。

然后再看一下client的代码: 

//client.c
  
int main(int argc, char** argv)
  
{
      
int send_sk;
      
struct sockaddr_in s_addr;
      
socklen_t len = sizeof(s_addr);
      
send_sk = socket(AF_INET, SOCK_STREAM, 0);
      
if(send_sk == -1)
      
{
          
perror("socket failed ");
          
return -1;
      
}
      
bzero(&s_addr, sizeof(s_addr));
      
s_addr.sin_family = AF_INET;

    inet_pton(AF_INET,SER_IP,&s_addr.sin_addr);  
    s_addr.sin_port = htons(SER_PORT);  
    if(connect(send_sk,(struct sockaddr*)&s_addr,len) == -1)  
    {  
        perror("connect fail  ");  
        return -1;  
    }  
    char pcContent[5000]={0};
    write(send_sk,pcContent,5000);
    sleep(1);
    close(send_sk);
    

}
  
这段代码更简单,就是打开一个socket然后连接一个服务器并发送5000个字节。刚才我们看服务器的代码,每次只接收4096个字节,那么就是说客户端发送的剩下的4个字节服务端的应用程序没有接收到,服务器端的socket就被关闭掉,这种情况下会发生什么状况呢,还是抓包看一看。

前三行就是TCP的3次握手,从第四行开始看,客户端的49660端口向服务器的9877端口发送了5000个字节的数据,然后服务器端发送了一个ACK进行了确认,紧接着服务器向客户端发送了一个RST断开了连接。和我们的预期一致。

4 在一个已关闭的socket上收到数据
  
如果某个socket已经关闭,但依然收到数据也会产生RST。

代码如下: 

客户端: 

int main(int argc, char** argv)
  
{
      
int send_sk;
      
struct sockaddr_in s_addr;
      
socklen_t len = sizeof(s_addr);
      
send_sk = socket(AF_INET, SOCK_STREAM, 0);
      
if(send_sk == -1)
      
{
          
perror("socket failed ");
          
return -1;
      
}
      
bzero(&s_addr, sizeof(s_addr));
      
s_addr.sin_family = AF_INET;

    inet_pton(AF_INET,SER_IP,&s_addr.sin_addr);  
    s_addr.sin_port = htons(SER_PORT);  
    if(connect(send_sk,(struct sockaddr*)&s_addr,len) == -1)  
    {  
        perror("connect fail  ");  
        return -1;  
    }  
    char pcContent[4096]={0};
    write(send_sk,pcContent,4096);
    sleep(1);
    write(send_sk,pcContent,4096);
    close(send_sk);
    

}
  
服务端: 
  
int main(int argc, char** argv)
  
{
      
int listen_fd, real_fd;
      
struct sockaddr_in listen_addr, client_addr;
      
socklen_t len = sizeof(struct sockaddr_in);
      
listen_fd = socket(AF_INET, SOCK_STREAM, 0);
      
if(listen_fd == -1)
      
{
          
perror("socket failed ");
          
return -1;
      
}
      
bzero(&listen_addr,sizeof(listen_addr));
      
listen_addr.sin_family = AF_INET;
      
listen_addr.sin_addr.s_addr = htonl(INADDR_ANY);
      
listen_addr.sin_port = htons(SERV_PORT);
      
bind(listen_fd,(struct sockaddr _)&listen_addr, len);
      
listen(listen_fd, WAIT_COUNT);
      
while(1)
      
{
          
real_fd = accept(listen_fd, (struct sockaddr_)&client_addr, &len);
          
if(real_fd == -1)
          
{
              
perror("accpet fail ");
              
return -1;
          
}
          
if(fork() == 0)
          
{
              
close(listen_fd);
              
char pcContent[4096];
              
read(real_fd,pcContent,4096);
              
close(real_fd);
              
exit(0);
          
}
          
close(real_fd);
      
}
      
return 0;
  
}
  
客户端在服务端已经关闭掉socket之后,仍然在发送数据。这时服务端会产生RST。

总结
  
总结,本文讲了几种TCP连接中出现RST的情况。实际上肯定还有无数种的RST发生,我以后会慢慢收集把更多的例子加入这篇文章。

参考文献: 
  
### 从TCP协议的原理来谈谈RST攻击 
>http://russelltao.iteye.com/blog/1405349

### TCP客户-服务器程序例子
>http://blog.csdn.net/youkuxiaobin/article/details/6917880

