---
title: nohup, shell 的后台运行 &, 和 nohup
author: "-"
date: 2011-10-08T02:39:02+00:00
url: nohup
categories:
  - Linux

tags:
  - reprint
---
## nohup, shell 的后台运行 &, 和 nohup
```bash
# 语法: nohup Command [ Arg … ] [&]

# & 后台运行, 但是使用父进程的 stdout 和 stderr
./command0 &
# nohup 的意思是 no hup, 忽略所有发送给子命令的 SIGHUP 信号,  shell关闭时 sigup 不会被发到子进程.
nohup ./command0 &
# 使用 nohup 之后 会看到 nohup: appending output to "nohup.out",  command0 的 stdout 和 stderr 都 被重定向到 nohup.out
nohup ./command0 > /dev/null 2>&1 &

```

>https://www.jianshu.com/p/747e0d5021a2
>https://blog.csdn.net/cugxueyu/article/details/2046565


### 
hangup 名称的来由
  
在 Unix 的早期版本中，每个终端都会通过 modem 和系统通讯。当用户 logout 时，modem 就会挂断 (hang up) 电话。 同理，当 modem 断开连接时，就会给终端发送 hangup 信号来通知其关闭所有子进程。

解决方法: 
  
我们知道，当用户注销 (logout) 或者网络断开时，终端会收到 HUP (hangup) 信号从而关闭其所有子进程。因此，我们的解决办法就有两种途径: 要么让进程忽略 HUP 信号，要么让进程运行在新的会话里从而成为不属于此终端的子进程。

1. nohup

nohup 无疑是我们首先想到的办法。顾名思义，nohup 的用途就是让提交的命令忽略 hangup 信号。让我们先来看一下 nohup 的帮助信息: 

NOHUP(1) User Commands NOHUP(1)

NAME
         
nohup - run a command immune to hangups, with output to a non-tty

SYNOPSIS
         
nohup COMMAND [ARG]...
         
nohup OPTION

DESCRIPTION
         
Run COMMAND, ignoring hangup signals.

       --help display this help and exit
    
       --version
              output version information and exit
    

可见，nohup 的使用是十分方便的，只需在要处理的命令前加上 nohup 即可，标准输出和标准错误缺省会被重定向到 nohup.out 文件中。一般我们可在结尾加上`"&"`来将命令同时放入后台运行，也可用">filename 2>&1"来更改缺省的重定向文件名。
 
Unix/Linux下一般比如想让某个程序在后台运行，很多都是使用&在程序结尾来让程序自动运行。比如我们要运行MySQL在后台: 

/usr/local/MySQL/bin/MySQLd_safe -user=MySQL &
  
但是加入我们很多程序并不象MySQLd一样做成守护进程，可能我们的程序只是普通程序而已，一般这种程序使用 & 结尾，但是如果终端关闭，那么程序也会被关闭。但是为了能够后台运行，那么我们就可以使用nohup这个命令，比如我们有个test.php需要在后台运行，并且希望在后台能够定期运行，那么就使用nohup: 

nohup /root/test.php &
 
无论是否将 nohup 命令的输出重定向到终端，输出都将附加到当前目录的 nohup.out 文件中。如果当前目录的 nohup.out 文件不可写，输出重定向到 $HOME/nohup.out 文件中。如果没有文件能创建或打开以用于追加，那么 Command 参数指定的命令不可调用。如果标准错误是一个终端，那么把指定的命令写给标准错误的所有输出作为标准输出重定向到相同的文件描述符。

退出状态: 该命令返回下列出口值: 

126 可以查找但不能调用 Command 参数指定的命令。

127 nohup 命令发生错误或不能查找由 Command 参数指定的命令。

否则，nohup 命令的退出状态是 Command 参数指定命令的退出状态。

nohup命令及其输出文件

nohup命令: 如果你正在运行一个进程，而且你觉得在退出帐户时该进程还不会结束，那么可以使用nohup命令。该命令可以在你退出帐户/关闭终端之后继续运行相应的进程。nohup就是不挂起的意思( n ohang up)。

该命令的一般形式为: nohup command &

使用nohup命令提交作业

如果使用nohup命令提交作业，那么在缺省情况下该作业的所有输出都被重定向到一个名为nohup.out的文件中，除非另外指定了输出文件: 

nohup command > myout.file 2>&1 &
  
在上面的例子中，输出被重定向到myout.file文件中。
 

使用 fg %n关闭。

另外有两个常用的ftp工具 ncftpget 和 ncftpput，可以实现后台的ftp上传和下载，这样我就可以利用这些命令在后台上传和下载文件了。

转自: http://www.21andy.com/blog/20071121/677.html

https://www.ibm.com/developerworks/cn/linux/l-cn-nohup/