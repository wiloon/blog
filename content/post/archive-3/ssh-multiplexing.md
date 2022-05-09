---
title: ssh Multiplexing,mux
author: "-"
date: 2020-04-21T16:48:13+00:00
url: /?p=16030

categories:
  - inbox
tags:
  - reprint
---
## ssh Multiplexing,mux

### 管理multiplexing
  
#### 查看当前的状态

```bash
ssh -O check machine1
ssh -O check 192.168.50.169 -l root
# Master running (pid=91057)

```

### 停止接受新的会话

```bash
ssh -O stop machine1
$ ssh -O stop root@47.91._._
  
# Stop listening request sent.
```

### 退出所有会话
  
```bash
ssh -O exit root@47.91._._
# Exit request sent.
```

#### Session Multiplexing

```bash
emacs /etc/ssh/ssh_config
emacs ~/.ssh/config
#---
Host *
ControlMaster auto
ControlPath   ~/.ssh/master-%r@%h:%p
ControlPersist 10m
```

<http://schin.space/ops/OPS-openssh-multiplexing/>

很多使用类Unix的用户常常头疼的一个问题是，多次登录远程主机的时候，需要重复的输入密码，尤其在登录跳板机还要输入动态token的时候，开多个会话窗口是一件很繁琐的事情

multiplexing
  
幸运的是，openssh通过multiplexing功能进行了连接优化，通过mulitiplexing可以实现多个ssh会话共用同一个tcp连接

实现multiplexing后，无论打开多少个ssh会话窗口，netstat显示的ssh连接都只有第一次会话建立的连接

$netstat -navp tcp | grep 22
  
tcp4 0 0 192.168._._.60603 47.91._._.22 ESTABLISHED 131072 131768 79974 0
  
$ps -ef|grep ssh|grep -v grep

501 79974 79973 0 8:34下午 ttys003 0:00.08 ssh root@47.91._._ -p 22

501 80150 80149 0 8:34下午 ttys004 0:00.01 ssh root@47.91._._ -p 22
  
multiplexing的实现，显然减少了多重连接建立的开销，因为每台机器可接受的连接数有限，所以在跳板机这类应用中 (虽然很多公司的堡垒机不是单机应用) ，可显著的降低成本；而另一个好处是，对于客户端来讲，由于可以复用ssh连接，因此新的会话不需要重复建立TCP连接, 进行认证授权这一过程，克隆远程对话的成本与耗时都显著下降，从而提升了工作的效率

开启multiplexing
  
与开启multiplexing相关的参数有3个，ControlMaster、ControlPath、ControlPersist

ControlMaster Enables the sharing of multiple sessions over a single network connection. When set to yes, ssh(1) will listen for connections on a control socket specified using the ControlPath argument. Additional sessions can connect to this socket using the same ControlPath with ControlMaster set to no (the default). These sessions will try to reuse the master instance's network connection rather than initiating new ones, but will fall back to connecting normally if the control socket does not exist, or is not listening.

Setting this to ask will cause ssh(1) to listen for control connections, but require confirmation using ssh-askpass(1). If the ControlPath cannot be opened, ssh(1) will continue without connecting to a master instance.

X11 and ssh-agent(1) forwarding is supported over these multiplexed connections, however the display and agent forwarded will be the one belonging to the master connection i.e. it is not possible to forward multiple displays or agents.

Two additional options allow for opportunistic multiplexing: try to use a master connection but fall back to creating a new one if one does not already exist. These options are: auto and autoask. The latter requires confirmation like the ask option.

ControlMaster 用来管理是否启用multiplexing，有2个可选参数: auto 与 autoask，前者会在没有 socket 文件时自动创建一个，后者在开启新的会话时会要求输入密码

ControlPath Specify the path to the control socket used for connection sharing as described in the ControlMaster section above or the string none to disable connection sharing. Arguments to ControlPath may use the tilde syntax to refer to a user's home directory or the tokens described in the TOKENS section. It is recommended that any ControlPath used for opportunistic connection sharing include at least %h, %p, and %r (or alternatively %C) and be placed in a directory that is not writable by other users. This ensures that shared connections are uniquely identified.

ControlPath 用来指定muliplexing共用socket文件的路径，path支持~来表示home目录，也支持TOKENS: %%, %C, %h, %i, %L, %l, %n, %p, %r, and %u. ControlPath应该尽量保证其他用户对socket文件没有写权限

%% A literal '%'.
  
%C Shorthand for %l%h%p%r.
  
%h The remote hostname.
  
%i The local user ID.
  
%L The local hostname.
  
%l The local hostname, including the domain name.
  
%n The original remote hostname, as given on the command line.
  
%p The remote port.
  
%r The remote username.
  
%u The local username.
  
ControlPersist When used in conjunction with ControlMaster, specifies that the master connection should remain open in the background (waiting for future client connections) after the initial client connection has been closed. If set to no, then the master connection will not be placed into the background, and will close as soon as the initial client connection is closed. If set to yes or 0, then the master connection will remain in the background indefinitely (until killed or closed via a mechanism such as the "ssh -O exit"). If set to a time in seconds, or a time in any of the formats documented in sshd_config(5), then the backgrounded master connection will automatically terminate after it has remained idle (with no client connections) for the specified time.

ControlPersist用来指定socket的有效时间，设置为yes会等待最后一个session关闭时释放连接，设置为no会在第一个session关闭时释放连接，设置为具体的时间X时，会在等待X时间结束时释放连接

一般的配置如下

Host *
  
ControlMaster auto
  
ControlPath ~/.ssh/ssh-%r@%h
  
ControlPersist yes
  
当建立一个新的连接时，会在~/.ssh/目录下看到一个socket文件

$ls -l
  
srw--- 1 chason wheel 0 1 1 12:52 ssh-root@47.91._._
  
$file ssh-root@47.91._._
  
ssh-root@47.91._._: socket
  
### ssh agnet not working
<https://superuser.com/questions/840340/ssh-agent-forwarding-not-working-even-when-using-ssh-a>
