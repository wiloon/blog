---
title: socat
author: "-"
date: 2022-04-19 16:54:43
url: socat
categories:
  - network
tags:
  - reprint
  - remix
---
## socat

## http server, 加载本地 .html 文件

```bash
echo "foo">foo.html
socat -v -v TCP-LISTEN:8000,crlf,reuseaddr,fork SYSTEM:"echo HTTP/1.0 200; echo Content-Type\: text/plain; echo; cat foo.html"
```

<https://stackoverflow.com/questions/29739901/socat-fake-http-server-use-a-file-as-server-response>

## socat 测试 端口连通性, test a remote port is reachable with socat

```bash
# test tcp port
socat - TCP4:192.168.1.15:22,connect-timeout=2

# test udp port
#set up a server listening on UDP port 48772
socat UDP-RECV:48772 STDOUT

# test udp port
socat - UDP:localhost:48772
```

## tcp 代理

```bash
socat TCP-LISTEN:3389,fork TCP:192.168.55.2:3389
```

### 建立TCP连接

```bash
    socat - tcp:192.168.1.18:80
```

### 建立连接并发送数据

```bash
    echo "hahaha" | socat - tcp:192.168.1.18:80
```

#### IPv6

```bash
    socat - tcp:[fd00::123]:12345 
```

### http echo server

```bash
# 直接返回 pong
socat -v TCP-LISTEN:8000,crlf,reuseaddr,fork SYSTEM:"echo HTTP/1.0 200; echo Content-Type\: text/plain; echo; echo pong"
# header: Access-Control-Allow-Origin
socat -v TCP-LISTEN:8000,crlf,reuseaddr,fork SYSTEM:"echo HTTP/1.0 200; echo Content-Type\: text/plain; echo Access-Control-Allow-Origin\:*;echo; echo pong"
# 使用前选 创建 响应数据的文本文件 foo.txt
socat -v TCP-LISTEN:8000,crlf,reuseaddr,fork SYSTEM:"echo HTTP/1.0 200; echo Content-Type\: text/plain; echo; cat foo.txt"

```

### 参数

- reuseaddr: Allows other sockets to bind to an address even if parts of it (e.g. the local port) are already in use by socat.
比如上面这条命令, 用socat打开了80端口, 80端口已经在被socat使用了, 我们打开端口是要接受其它客户端连接的,使用 reuseaddr, 能让其它客户端跟80建立连接.
due to reuseaddr, it allows immediate restart after master processes termination, even if some child sockets are not completely shut down.  Option reuseaddr allows immediate restart of the server process.
- fork: fork a child process to handle all incoming client connections.
加了 fork 的参数后，就能同时应答多个链接过来的客户端，每个客户端会 fork 一个进程出来进行通信，加上 reuseaddr 可以防止链接没断开玩无法监听的问题。
每次 accept 一个链接都会 fork 出一份来不影响接收其他的新连接，这样 socat 就可以当一个端口转发服务，一直启动在那里。还可以用 supervisor 托管起来，开机自动启动。
- crlf: use CR+NL on this connection, relay data to and from stdio
- SYSTEM: `<shell-command>`, Forks a sub process that establishes communication with its parent process and invokes the specified program with system()

### socat send http request

```bash
socat - TCP:wiloon.com:80
GET / HTTP/1.1 \r\n
host: www.wiloon.com \r\n
\r\n
```

### 向zookeeper 发送 stat 查询zookeeper版本

```bash
echo stat | socat - TCP:192.168.1.xxx:2181
```

### proxy http port

```bash
socat TCP4-LISTEN:188,reuseaddr,fork TCP4:192.168.97.11:8888
```

Socat 是 Linux 下的一个多功能的网络工具,名字来由是 「Socket CAT」, 其功能与有"瑞士军刀"之称的 netcat 类似, 不过据说可以看做netcat的加强版。的确如此,它有一些netcat所不具备却又很有需求的功能,例如ssl连接这种。nc可能是因为比较久没有维护,确实显得有些陈旧了。

Socat 的主要特点就是在两个数据流之间建立通道，且支持众多协议和链接方式。如 IP、TCP、 UDP、IPv6、PIPE、EXEC、System、Open、Proxy、Openssl、Socket等。

### 安装

```bash
    pacman -S socat
    yum install -y socat
    apt-get install socat
```

### 基本语法

```bash
socat [options] <address> <address>
```

其中这两个 address 就是关键了, 如果要解释的话, address 就类似于一个文件描述符, socat 所做的工作就是在两个 address 指定的文件描述符间建立一个 pipe 用于发送和接收数据。

那么 address 的描述就是 socat 的精髓所在了, 几个常用的描述方式如下:

-, STDIN, STDOUT : 表示标准输入输出,可以就用一个横杠代替
  
/var/log/syslog : 也可以是任意路径,如果是相对路径要使用 ./,打开一个文件作为数据流。
  
TCP:: : 建立一个TCP连接作为数据流,TCP也可以替换为UDP
  
TCP-LISTEN: : 建立TCP监听端口,TCP也可以替换为UDP
  
EXEC: : 执行一个程序作为数据流。
  
以上规则中前面的TCP等都可以小写。

在这些描述后可以附加一些选项,用逗号隔开,如fork,reuseaddr,stdin,stdout,ctty等。

```bash
直接回显
socat - -

# 通过 Socat 读取文件
# 从绝对路径读取
socat - /var/www/html/flag.php

# 从相对路径读取
socat - ./flag.php

# 写文件
echo "hello" | socat - /home/user/chuck

socat当netcat
连接远程端口
nc localhost 80
socat - TCP:localhost:80

监听端口
nc -lp localhost 700
socat TCP-LISTEN:700 -

正向shell
nc -lp localhost 700 -e /bin/bash
socat TCP-LISTEN:700 EXEC:/bin/bash

反弹shell
nc localhost 700 -e /bin/bash
socat tcp-connect:localhost:700 exec:'bash -li',pty,stderr,setsid,sigint,sane
```

其他
  
其实从这里才是重点

SSL连接
  
SSL服务器

socat OPENSSL-LISTEN:443,cert=/cert.pem -
  
需要首先生成证书文件

SSL客户端

socat - OPENSSL:localhost:443
  
fork服务器
  
接下来这个例子,就是我认识socat的原因,可以将一个使用标准输入输出的单进程程序变为一个使用fork方法的多进程服务,非常方便。

socat TCP-LISTEN:1234,reuseaddr,fork EXEC:./helloworld
  
不同设备的通信
  
将U盘进行网络共享

socat -d -d /dev/ttyUSB1,raw,nonblock,ignoreeof,cr,echo=0 TCP4-LISTEN:5555,reuseaddr
  
-d -d 指的是调试信息的级别

将终端转发到COM1

socat READLINE,history=$HOME/.cmd_history /dev/ttyS0,raw,echo=0,crnl
  
socat还有个readbyte的option,这样就可以当dd用了。

小结
  
因为在Linux/UNIX中,一切都是文件,无论是socket还是其他设备。所以从理论上来说,一切能够在文件层级访问的内容都可以成为socat的数据流的来源,2个address可以任意发挥,能够做到的事情还有很多。特别是其fork的功能,确实是netcat所不能比的。

参考文献
  
借鉴的几篇博文:
  
Some Useful Socat Commands
  
Socat: A very powerful networking tool
  
Socat Examples
  
其他内容,可以参考socat man page

### 官网

<http://www.dest-unreach.org/socat/>
  
<http://brieflyx.me/2015/linux-tools/socat-introduction/>
  
<https://www.hi-linux.com/posts/61543.html>
