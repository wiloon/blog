---
title: SSH端口转发
author: "-"
date: 2015-01-18T05:43:22+00:00
url: /?p=7259
categories:
  - Uncategorized

tags:
  - reprint
---
## SSH端口转发
SSH端口转发
2014/11/12 VMUNIX
ssh是个多用途的工具，不仅可以远程登录，还可以搭建socks代理、进行内网穿透，这是利用它的端口转发功能来实现的。

所谓ssh端口转发，就是在ssh连接的基础上，指定 ssh client 或 ssh server 的某个端口作为源地址，所有发至该端口的数据包都会透过ssh连接被转发出去；至于转发的目标地址，既可以指定，也可以不指定，如果指定了目标地址，称为定向转发，如果不指定目标地址则称为动态转发：

定向转发
定向转发把数据包转发到指定的目标地址。目标地址不限定是ssh client 或 ssh server，既可以是二者之一，也可以是二者以外的其他机器
动态转发
动态转发不指定目标地址，数据包转发的目的地是动态决定的
因为ssh端口转发是基于ssh连接的，所以如果ssh连接断开，那么设置好的端口转发也会随之停止。

在设置端口转发之前，必须确认ssh的端口转发功能是打开的。

怎样打开ssh的端口转发功能？
ssh端口转发功能默认是打开的。控制它的开关叫做 AllowTcpForwarding，位于ssh server的配置文件 /etc/ssh/sshd_config 里：
    AllowTcpForwarding yes
如果修改的话需要重启sshd服务才会生效。

怎样设置端口转发？
设置端口转发之前要注意 iptables 设置，确保相应的端口未被屏蔽，如果嫌麻烦的话也可以临时禁用 iptables：
# service iptables stop

定向转发和动态转发的设置方法是不一样的，以下分别介绍。

设置定向转发
定向转发可以把一个 IP:Port 定向映射到另一个 IP:Port，源和目的都必须指定。源地址既可以是 ssh client 的某个端口，也可以是 ssh server 的某个端口：

如果源地址是 ssh client 的某个端口，称为本地转发（Local Port Forwarding），发往 ssh client 指定端口的数据包会经过 ssh server 进行转发；
如果源地址是 ssh server 的某个端口，则称为远程转发（Remote Port Forwarding），发往 ssh server 指定端口的数据包会经过 ssh client 进行转发.
ssh-port-forwarding

设置本地转发：
先看一下基本命令：

在ssh client上执行：
{ssh client}# ssh -g -N -f -o ServerAliveInterval=60 \
-L <local port>:<remote host>:<remote port> username@<ssh server>
参数的含义在后面有解释。

我们以下面的示意图为例：你想telnet连接{remote host}，但是无法直达，你只能直接连接ssh client，于是试图通过{ssh client}到{ssh server}这条通道中转：

{you} — {ssh client} — {ssh server} — {remote host}

我们要做的是在{ssh client}上执行以下命令：

{ssh client} # ssh -g -L 2323:<remote-host>:23 username@<ssh-server>

输入口令之后，就跟普通的ssh登录一样，我们进入了shell，在shell中可以正常操作，不同之处是，它同时还把 {ssh client} 的2323端口映射到了{remote host} 的23端口——亦即telnet端口，此后执行”telnet <ssh client> 2323″就相当于”telnet <remote-host>”，只要shell不退出，这个定向转发就一直有效。

注1：如果以上命令不加”-g”选项，那么SSH Client上的监听端口2323会绑定在127.0.0.1上，意味着只有SSH Client自己才能连上。加上”-g”选项之后，SSH Client才允许网络上其他机器连接2323端口。
注2：以上命令会生成一个shell，有时候并不符合我们的需要，因为多数时候我们只想要一个端口转发功能，挂一个shell是个累赘，而且shell一退出，端口转发也停了。这就是为什么我们需要”-N -f”选项的原因：
-N 告诉ssh client，这个连接不需要执行任何命令，仅做端口转发
-f 告诉ssh client在后台运行
注3：为了避免长时间空闲导致ssh连接被断开，我们可以加上”-o ServerAliveInterval=60″选项，每60秒向ssh server发送心跳信号。还有一个TCPKeepAlive选项的作用是类似的，但是不如ServerAliveInterval 好，因为TCPKeepAlive在TCP层工作，发送空的TCP ACK packet，有可能会被防火墙丢弃；而ServerAliveInterval 在SSH层工作，发送真正的数据包，更可靠些。
如果不是以root身份设置端口转发的话，转发端口只能使用大于1024的端口号。
设置远程转发：
先看一下基本命令，分为两部分：

在ssh server上：
编辑 /etc/ssh/sshd_config，设置以下内容然后重启sshd服务
    GatewayPorts yes
在ssh client上执行：
{ssh client}# ssh -f -N -o ServerAliveInterval=60 \
-R <ssh server port>:<remote host>:<remote port> username@<ssh server>

这次的实例如下所示，你想用telnet连接{remote host}，但是无法直达，于是试图通过{ssh server}到{ssh client}这条通道中转，注意与前面介绍的本地转发的不同之处是，本地转发的案例中你只能直接连接到 ssh client，而这里你只能直接连到 ssh server：

{you} — {ssh server} — {ssh client} — {remote host}

我们要做的是在{ssh client}上执行以下命令：

{ssh client} # ssh -f -N -R 2323:<remote-host>:23 username@<ssh-server>

输入口令之后，{ssh server}的2323端口映射到了{remote host}的23端口——亦即telnet端口，此后执行”telnet <ssh server> 2323″就相当于”telnet <remote-host>”。

本地转发与远程转发的区别与适用场景
定向转发（包括本地转发和远程转发）通常用于内网穿透，本地转发和远程转发的区别就在于监听端口是开在ssh client上还是ssh server上。常见的使用场景是：

如果ssh client在内网里面，ssh server在Internet上，你想让Internet上的机器穿进内网之中，那就使用远程转发；
如果ssh server在内网里面，ssh client在外面，你想穿进内网就应该使用本地转发。
设置动态转发
定向转发（包括本地转发和远程转发）的局限性是必须指定某个目标地址，如果我们需要借助一台中间服务器访问很多目标地址，一个一个地定向转发显然不是好办法，这时我们要用的是ssh动态端口转发，它相当于建立一个SOCKS服务器。

先看一下基本命令：

在ssh client上执行：
{ssh client}# ssh -f -N -o ServerAliveInterval=60 \
-D <ssh client port> username@<ssh server>

实际使用时有两种常见场景：

你把自己的机器(127.0.0.1)当作 sock5 代理服务器：
{you / ssh client} — {ssh server} — {other hosts}
命令如下：

{ssh client} # ssh -f -N -D 1080 username@<ssh-server>

这种情况下，我们得到的socks5代理服务器是：127.0.0.1:1080，仅供ssh client自己使用。
然后你就可以在浏览器中或其他支持socks5代理的软件中进行设置。

ssh client 和 ssh server 是同一台机器，并充当socks5代理：
{you} — {ssh client / ssh server} — {other hosts}
命令如下：

{ssh client} # ssh -f -N -g -D 1080 username@127.0.0.1

这种情况下，我们得到的socks5代理服务器是：
{ssh client IP}:1080，可供网络上其他机器使用，只要能连接ssh client即可。

通过SSH建立的SOCKS服务器使用的是SOCKS5协议，在为应用程序设置SOCKS代理的时候要注意。

>http://linuxperf.com/?p=30

