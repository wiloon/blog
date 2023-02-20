---
title: tcp reset, rst
author: "-"
date: 2020-04-16T10:28:01+00:00
url: tcp/reset
categories:
  - Network
tags:
  - reprint
  - remix
  - tcp
---
## tcp reset, rst

在谈 RST 攻击前，必须先了解 TCP: 如何通过三次握手建立 TCP 连接、四次握手怎样把全双工的连接关闭掉、滑动窗口是怎么传输数据的、TCP 的 flag 标志位里 RST 在哪些情况下出现。下面我会画一些尽量简化的图来表达清楚上述几点，之后再了解下 RST 攻击是怎么回事。
  
## TCP是什么？
  
TCP 是在 IP 网络层之上的传输层协议，用于提供 port 到 port 面向连接的可靠的字节流传输。我来用土语解释下上面的几个关键字:
  
port到port: IP层只管数据包从一个IP到另一个IP的传输，IP层之上的TCP层加上端口后，就是面向进程了，每个port都可以对应到用户进程。
  
可靠: TCP会负责维护实际上子虚乌有的连接概念，包括收包后的确认包、丢包后的重发等来保证可靠性。由于带宽和不同机器处理能力的不同，TCP要能控制流量。
  
字节流: TCP会把应用进程传来的字节流数据切割成许多个数据包，在网络上发送。IP包是会失去顺序或者产生重复的，TCP协议要能还原到字节流本来面目。
  
从上面我用PowerPoint画的TCP协议图可以看到，标志位共有六个，其中RST位就在TCP异常时出现，也是我这篇文章重点关注的地方。
  
## 通过三次握手建立连接
  
下面我通过A向B建立TCP连接来说明三次握手怎么完成的。
  
为了能够说清楚下面的RST攻击，需要结合上图说说: SYN标志位、序号、滑动窗口大小。
  
建立连接的请求中，标志位SYN都要置为1，在这种请求中会告知MSS段大小，就是本机希望接收TCP包的最大大小。
  
发送的数据TCP包都有一个序号。它是这么得来的: 最初发送SYN时，有一个初始序号，根据RFC的定义，各个操作系统的实现都是与系统时间相关的。之后，序号的值会不断的增加，比如原来的序号是100，如果这个TCP包的数据有10个字节，那么下次的TCP包序号会变成110。
  
滑动窗口用于加速传输，比如发了一个seq=100的包，理应收到这个包的确认ack=101后再继续发下一个包，但有了滑动窗口，只要新包的seq与没有得到确认的最小seq之差小于滑动窗口大小，就可以继续发。
  
## 滑动窗口
  
滑动窗口毫无疑问是用来加速数据传输的。TCP要保证"可靠"，就需要对一个数据包进行ack确认表示接收端收到。有了滑动窗口，接收端就可以等收到许多包后只发一个ack包，确认之前已经收到过的多个数据包。有了滑动窗口，发送端在发送完一个数据包后不用等待它的ack，在滑动窗口大小内可以继续发送其他数据包。举个例子来看吧。
  
大家看上图，标志位为.表示所有的flag都为0。标志位P表示flag为PSH的TCP包，用于快速传输数据。
  
前三个包是三次握手，客户端表示自己的滑动窗口大小是65535 (我的XP机器) ，服务器端表示滑动窗口是5840 (屏幕宽了，没截出来) 。从第四个包开始，客户端向服务器发送PSH包，数据长度是520字节，服务器发了ack确认包。注意此时win窗口大小发生了改变哈。以此类推。
  
倒数第二、三包，服务器在滑动窗口内连续向客户端发包，客户端发送的ack 124同时确认了之前的两个包。这就是滑动窗口的功能了。
  
如果谈到TCP攻击就需要注意，TCP的各种实现中，在滑动窗口之外的seq会被扔掉！下面会讲这个问题。
  
## 四次握手的正常TCP连接关闭
  
先画张简单的正常关闭连接状态变迁图。
  
FIN标志位也看到了，它用来表示正常关闭连接。图的左边是主动关闭连接方，右边是被动关闭连接方，用netstat命令可以看到标出的连接状态。
  
FIN是正常关闭，它会根据缓冲区的顺序来发的，就是说缓冲区FIN之前的包都发出去后再发FIN包，这与RST不同。
  
## RST 标志位
  
RST 表示复位，用来**异常**的关闭连接，在 TCP 的设计中它是不可或缺的。就像上面说的一样，发送 RST 包关闭连接时，不必等**缓冲区**的包都发出去 (不像上面的 FIN 包) ，直接丢弃缓存区的包发送 RST 包。而接收端收到 RST 包后，也不必发送 ACK 包来确认。
  
TCP 处理程序会在自己认为的异常时刻发送 RST 包。例如，A 向 B 发起连接，但 B 之上并未监听相应的端口，这时 B 操作系统上的 TCP 处理程序会发 RST 包。  
又比如，AB 正常建立连接了，正在通讯时，A 向 B 发送了 FIN 包要求关连接，B 发送 ACK 后，网断了，A 通过若干原因放弃了这个连接 (例如进程重启) 。网通了后，B 又开始发数据包，A 收到后表示压力很大，不知道这野连接哪来的，就发了个 RST 包强制把连接关了，B 收到后会出现 **connect reset by peer** 错误。
  
## RST 攻击

A 和服务器 B 之间建立了 TCP 连接，此时 C 伪造了一个 TCP 包发给 B，使 B 异常的断开了与 A 之间的 TCP 连接，就是 RST 攻击了。实际上从上面 RST 标志位的功能已经可以看出这种攻击如何达到效果了。  
那么伪造什么样的TCP包可以达成目的呢？我们至顶向下的看。  
假定 C 伪装成 A 发过去的包，这个包如果是 RST 包的话，毫无疑问，B 将会丢弃与 A 的缓冲区上所有数据，强制关掉连接。  
如果发过去的包是 SYN 包，那么，B 会表示 A 已经发疯了 (与OS的实现有关) ，正常连接时又来建新连接，B 主动向 A 发个 RST 包，并在自己这端强制关掉连接。  
这两种方式都能够达到复位攻击的效果。似乎挺恐怖，然而关键是，如何能伪造成 A 发给 B 的包呢？这里有两个关键因素，源端口和序列号。  
一个 TCP 连接都是四元组，由源 IP、源端口、目标 IP、目标端口唯一确定一个连接。所以，如果 C 要伪造 A 发给 B 的包，要在上面提到的 IP 头和 TCP 头，把源 IP、源端口、目标 IP、目标端口都填对。这里 B 作为服务器，IP 和端口是公开的，A 是我们要下手的目标，IP 当然知道，但 A 的源端口就不清楚了，因为这可能是 A 随机生成的。当然，如果能够对常见的 OS 如 windows 和 linux 找出生成 source port 规律的话，还是可以搞定的。  
序列号问题是与滑动窗口对应的，伪造的 TCP 包里需要填序列号，如果序列号的值不在 A 之前向 B 发送时 B 的滑动窗口内，B 是会主动丢弃的。所以我们要找到能落到当时的 AB 间滑动窗口的序列号。这个可以暴力解决，因为一个 sequence 长度是 32 位，取值范围 0-4294967296，如果窗口大小像上图中我抓到的 windows下的65535的话，只需要相除，就知道最多只需要发 65537 (4294967296/65535=65537) 个包就能有一个序列号落到滑动窗口内。RST 包是很小的，IP 头 + TCP 头也才 40 字节，算算我们的带宽就知道这实在只需要几秒钟就能搞定。

版权声明: 本文为CSDN博主「Sunface撩技术」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: <https://blog.csdn.net/erlib/java/article/details/50132307>

## 关闭一个 TCP 连接, killcx

要伪造一个能关闭 TCP 连接的 RST 报文，必须同时满足「四元组相同」和「序列号正好落在对方的滑动窗口内」这两个条件。

直接伪造符合预期的序列号是比较困难，因为如果一个正在传输数据的 TCP 连接，滑动窗口时刻都在变化，因此很难刚好伪造一个刚好落在对方滑动窗口内的序列号的 RST 报文。

办法还是有的，我们可以伪造一个四元组相同的 SYN 报文，来拿到“合法”的序列号！

正如我们最开始学到的，如果处于 establish 状态的服务端，收到四元组相同的 SYN 报文后，会回复一个 Challenge ACK，这个 ACK 报文里的「确认号」，正好是服务端下一次想要接收的序列号，说白了，就是可以通过这一步拿到服务端下一次预期接收的序列号。

然后用这个确认号作为 RST 报文的序列号，发送给服务端，此时服务端会认为这个 RST 报文里的序列号是合法的，于是就会释放连接！

在 Linux 上有个叫 killcx 的工具，就是基于上面这样的方式实现的，它会主动发送 SYN 包获取 SEQ/ACK 号，然后利用 SEQ/ACK 号伪造两个 RST 报文分别发给客户端和服务端，这样双方的 TCP 连接都会被释放，这种方式活跃和非活跃的 TCP 连接都可以杀掉。

使用方式也很简单，只需指明客户端的 IP 和端口号。

```bash
./killcx <IP地址>:<端口号>
```

killcx 工具的工作原理，如下图。

它伪造客户端发送 SYN 报文，服务端收到后就会回复一个携带了正确「序列号和确认号」的 ACK 报文（Challenge ACK），然后就可以利用这个 ACK 报文里面的信息，伪造两个 RST 报文：

用 Challenge ACK 里的确认号伪造 RST 报文发送给服务端，服务端收到 RST 报文后就会释放连接。
用 Challenge ACK 里的序列号伪造 RST 报文发送给客户端，客户端收到 RST 也会释放连接。
正是通过这样的方式，成功将一个 TCP 连接关闭了！

<https://bbs.huaweicloud.com/blogs/301407>

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

<https://zhuanlan.zhihu.com/p/30791159>

## TCP 连接中出现 RST 的情况

It's fatal. The remote server has sent you a RST packet, which indicates an immediate dropping of the connection, rather than the usual handshake. This bypasses the normal half-closed state transition. I like this description:

"Connection reset by peer" is the TCP/IP equivalent of slamming the phone back on the hook. It's more polite than merely not replying, leaving one hanging. But it's not the FIN-ACK expected of the truly polite TCP/IP converseur.

><https://stackoverflow.com/questions/1434451/what-does-connection-reset-by-peer-mean>
><https://my.oschina.net/costaxu/blog/127394>

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

```c
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
  
```

这段代码更简单,就是打开一个socket然后连接一个服务器并发送5000个字节。刚才我们看服务器的代码,每次只接收4096个字节,那么就是说客户端发送的剩下的4个字节服务端的应用程序没有接收到,服务器端的socket就被关闭掉,这种情况下会发生什么状况呢,还是抓包看一看。

前三行就是TCP的3次握手,从第四行开始看,客户端的49660端口向服务器的9877端口发送了5000个字节的数据,然后服务器端发送了一个ACK进行了确认,紧接着服务器向客户端发送了一个RST断开了连接。和我们的预期一致。

4 在一个已关闭的socket上收到数据
  
如果某个socket已经关闭,但依然收到数据也会产生RST。

代码如下:

客户端:

```c
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
```
  
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
>
><http://russelltao.iteye.com/blog/1405349>

### TCP客户-服务器程序例子
>
><http://blog.csdn.net/youkuxiaobin/article/details/6917880>
