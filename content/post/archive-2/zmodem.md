---
title: zmodem, rz, sz
author: "-"
date: 2018-03-08T04:14:26+00:00
url: zmodem
categories:
  - Inbox
tags:
  - reprint
---
## zmodem, rz, sz

### install
    pacman -S lrzsz
    yum install lrzsz

### konsole
    Edit>Zmodem upload ( ctrl + alt + U )
http://www.cnblogs.com/strikebone/p/3454679.html

zssh 的全名叫 ZMODEM SSH. 看名字就知道, 使用的 zmodem

zmodem 协议方便主要表示在以下点

其一,不需要输入很长的命令和密码,直接使用rz,sz加文件名,就能实现文件的收发。速度还很快。

其二,在中转了一台主机时,要在目标主机和本地主机之类,要传送文件,scp相当的麻烦,需要输入多次命令用户密码.但sz直接可以穿透。

好了,讲使用,如下,和使用ssh完全一样,只是打命令时,变成了zssh

#zssh root@192.168.1.1

好了,在进入后,你需要上传文件的话。先
  
#ctrl+@
  
zssh >//这里切换到了本地机器

zssh>pwd //看一下本地机器的目录在那

zssh>ls //看一下有那些文件

zssh>sz 123.txt //上传本地机器的当前目录的123.txt到远程机器的当前目录

下载文件的话

#sz filename //在远程机器上,启动sz, 准备发送文件

看到一堆乱码
  
然后在
  
#ctrl+@
  
zssh > pwd //看看在那个目录,cd 切换到合适的目录

zssh > rz //接住对应的文件

我靠, 这个rz , sz的命令太难理解了. 还好有高手指点.


文件传输协议: 

文件传输是数据交换的主要形式。在进行文件传输时,为使文件能被正确识别和传送,我们需要在两台计算机之间建立统一的传输协议。这个协议包括了文件的识别、传送的起止时间、错误的判断与纠正等内容。

在SecureCRT下的传输协议有ASCII、Xmodem、Ymodem、Zmodem4种。

 (1) ASCII: 这是最快的传输协议,但只能传送文本文件。

 (2) Xmodem: 这种古老的传输协议速度较慢,但由于使用了CRC错误侦测方法,传输的准确率可高达99.6%。

 (3) Ymodem: 这是Xmodem的改良版,使用了1024位区段传送,速度比Xmodem要快。

 (4) Zmodem: Zmodem采用了串流式 (streaming) 传输方式,传输速度较快,而且还具有自动改变区段大小和断点续传、快速错误侦测等功能。这是目前最流行的文件传输协议。

SecureCRT 可以使用 linux 下的 zmodem 协议来快速的传送文件. 在传送之前先设置好上传和下载的目录: 
options->session options ->Terminal->Xmodem/Zmodem 下

Zmodem 传输数据会使用到2个命令: 

- sz: 将选定的文件发送 (send) 到本地机器
- rz: 运行该命令会弹出一个文件选择窗口,从本地选择文件上传到服务器(receive)

sz命令
用途说明: sz命令是利用ZModem协议来从Linux服务器传送文件到本地,一次可以传送一个或多个文件。相对应的从本地上传文件到Linux服务器,可以使用rz命令。

常用参数
-a 以文本方式传输 (ascii) 。

-b 以二进制方式传输 (binary) 。

-e 对控制字符转义 (escape) ,这可以保证文件传输正确。

如果能够确定所传输的文件是文本格式的,使用 sz -a files

如果是二进制文件,使用 sz -be files

rz命令
-b 以二进制方式,默认为文本方式。 (Binary (tell it like it is) file transfer override.) 

-e 对所有控制字符转义。 (Force sender to escape all control characters; normally XON, XOFF, DLE, CR-@-CR, and Ctrl-X are escaped.) 

如果要保证上传的文件内容在服务器端保存之后与原始文件一致,最好同时设置这两个标志,如下所示方式使用: 

rz -be
此命令执行时,会弹出文件选择对话框,选择好需要上传的文件之后,点确定,就可以开始上传的过程了。上传的速度取决于当时网络的状况。

如果执行完毕显示“0错误”,文件上传就成功了,其他显示则表示文件上传出现问题了。

参考: http://www.tuicool.com/articles/Enqem2
http://www.daniel-journey.com/archives/1325


https://blog.csdn.net/jobschen/article/details/46788899

## Zmodem

Zmodem: Zmodem采用了串流式 (streaming) 传输方式，传输速度较快，而且还具有自动改变区段大小和断点续传、快速错误侦测等功能。这是目前最流行的文件传输协议

SecureCRT 默认上传下载目录

options->session options ->Terminal->Xmodem/Zmodem

Zmodem transfer canceled by remote side
  
在服务器上使用rz上传本地的文件到服务器时，出现一坨乱码，并报如下错误: 

"Zmodem transfer canceled by remote side "
  
网上查资料，根据大家建议的方法在rz上传文件的时候，加上-be参数即可解决问题。

rz -be file
  
参数解释: 

-b 以二进制方式传输 (binary) 。

-e 对控制字符转义 (escape) ，这可以保证文件传输正确。

参考网址: http://chenpeng.info/html/3473

https://blog.csdn.net/shanliangliuxing/article/details/7834937
  
https://blog.51cto.com/damaicha/1868613

## Linux sz

[http://codingstandards.iteye.com/blog/827637](http://codingstandards.iteye.com/blog/827637)

我使用过的Linux命令之sz - 下载文件，无需ftp/sftp

博客分类: Linux命令

LinuxCC++C#Web

我使用过的Linux命令之sz - 下载文件，无需ftp/sftp

本文链接: [http://codingstandards.iteye.com/blog/827637](http://codingstandards.iteye.com/blog/827637)    (转载请注明出处)

用途说明

sz命令是利用ZModem协议来从Linux服务器传送文件到本地，一次可以传送一个或多个文件。相对应的从本地上传文件到Linux服务器，可以使用rz命令。参见《我使用过的Linux命令之rz - 批量上传文件，简单易用 》。

常用参数

-a 以文本方式传输 (ascii) 。

-b 以二进制方式传输 (binary) 。

-e 对控制字符转义 (escape) ，这可以保证文件传输正确。

-c command

-i command 在接收端 (本地) 执行命令，但我没有尝试成功。

如果能够确定所传输的文件是文本格式的，使用 sz -a files

如果是二进制文件，使用 sz -be files

下载完了之后文件在哪个地方呢？

SecureCRT中，选择菜单项"选项(O)"下的"会话选项(S)"，左边切到"Xmodem/Zmodem"，即可看到上传和下载目录设置，也可更改。默认上传目录为 C:\Program Files\SecureCRT\upload，下载目录为 C:\Program Files\SecureCRT\download。

但在Vista下，到C:\Program Files\SecureCRT\download去看的时候并没有找到下载的文件，搜索了一下发现它们在下面的目录中: C:\Users\*\*\*\AppData\Local\VirtualStore\Program Files\SecureCRT\download，其中\*\**为用户名。

使用示例

示例一 批量下载文本文件

本例演示了下载文本文件，比如c源代码。

[root@web src]# ls *.c

httptunnel_codec.c  s_agent2.c  s_conf.c  s_htserv.c  s_pop3.c    s_smtp.c   s_tcpfwd.c  s_telnet.c  s_user.c  s_xort.c

iSurf.c             s_agent.c   s_ftp.c   s_http.c    s_run.c     s_socks.c  s_tcpgum.c  s_term.c    s_via3.c

proxycfg.c          s_bridge.c  s_host.c  s_mime.c    s_server.c  s_task.c   s_tcphub.c  surf.c      s_via.c

[root@web src]# sz -a *.c

rz

正在开始 zmodem 传输。 按 Ctrl+C 取消。

正在传输 httptunnel_codec.c...

100%      22 KB    5 KB/s 00:00:04       0 错误

正在传输 iSurf.c...

100%     890 bytes  890 bytes/s 00:00:01       0 错误

正在传输 proxycfg.c...

100%       1 KB    1 KB/s 00:00:01       0 错误

正在传输 s_agent2.c...

100%       4 KB    1 KB/s 00:00:03       0 错误

正在传输 s_agent.c...

100%       6 KB    3 KB/s 00:00:02       0 错误

正在传输 s_bridge.c...

100%       6 KB    0 KB/s 00:00:10       0 错误

100%       6 KB    0 KB/s 00:00:10       0 错误

正在传输 s_conf.c...

100%       9 KB    0 KB/s 00:00:41       0 错误

正在传输 s_ftp.c...

100%      18 KB    0 KB/s 00:04:26       0 错误

[root@web src]# **01000000039a32

-bash: **01000000039a32: command not found

[root@web src]#

由于网络不稳定，被自动终止掉了。

[root@web src]#

[root@web src]#

[root@web src]#

[root@web src]# sz -a *.c

rz

正在开始 zmodem 传输。 按 Ctrl+C 取消。

正在传输 httptunnel_codec.c...

100%      22 KB    2 KB/s 00:00:10       0 错误

正在传输 iSurf.c...

100%     890 bytes  890 bytes/s 00:00:01       0 错误

正在传输 proxycfg.c...

100%       1 KB    1 KB/s 00:00:01       0 错误

100%       1 KB    1 KB/s 00:00:01       0 错误

正在传输 s_agent2.c...

100%       4 KB    2 KB/s 00:00:02       0 错误

100%       4 KB    2 KB/s 00:00:02       0 错误

正在传输 s_agent.c...

100%       6 KB    6 KB/s 00:00:01       0 错误

正在传输 s_bridge.c...

100%       6 KB    1 KB/s 00:00:04       0 错误

正在传输 s_conf.c...

100%       9 KB    4 KB/s 00:00:02       0 错误

正在传输 s_ftp.c...

100%      18 KB    4 KB/s 00:00:04       0 错误

正在传输 s_host.c...

100%       3 KB    1 KB/s 00:00:02       0 错误

正在传输 s_htserv.c...

100%       8 KB    2 KB/s 00:00:04       0 错误

正在传输 s_http.c...

100%      32 KB    3 KB/s 00:00:09       0 错误

正在传输 s_mime.c...

100%       1 KB    1 KB/s 00:00:01       0 错误

100%       1 KB    1 KB/s 00:00:01       0 错误

正在传输 s_pop3.c...

100%       3 KB    3 KB/s 00:00:01       0 错误

正在传输 s_run.c...

100%     900 bytes  900 bytes/s 00:00:01       0 错误

正在传输 s_server.c...

100%       5 KB    2 KB/s 00:00:02       0 错误

正在传输 s_smtp.c...

100%     990 bytes  990 bytes/s 00:00:01       0 错误

正在传输 s_socks.c...

100%      19 KB   19 KB/s 00:00:01       0 错误

正在传输 s_task.c...

100%       1 KB    1 KB/s 00:00:01       0 错误

100%       1 KB    1 KB/s 00:00:01       0 错误

正在传输 s_tcpfwd.c...

100%      10 KB    5 KB/s 00:00:02       0 错误

正在传输 s_tcpgum.c...

100%       8 KB    4 KB/s 00:00:02       0 错误

正在传输 s_tcphub.c...

100%      11 KB   11 KB/s 00:00:01       0 错误

正在传输 s_telnet.c...

100%       3 KB    3 KB/s 00:00:01       0 错误

正在传输 s_term.c...

100%       7 KB    7 KB/s 00:00:01       0 错误

正在传输 surf.c...

100%       2 KB    2 KB/s 00:00:01       0 错误

正在传输 s_user.c...

100%       6 KB    3 KB/s 00:00:02       0 错误

正在传输 s_via3.c...

100%       1 KB    1 KB/s 00:00:01       0 错误

正在传输 s_via.c...

100%       5 KB    2 KB/s 00:00:02       0 错误

正在传输 s_xort.c...

100%       4 KB    4 KB/s 00:00:01       0 错误

奫root@web src]#

示例二 下载二进制文件

本例演示了下载二进制文件，先将前面的c源代码压缩到一个zip文件。

[root@web src]# zip source.zip *.c

adding: httptunnel_codec.c (deflated 88%)

adding: iSurf.c (deflated 58%)

adding: proxycfg.c (deflated 56%)

adding: s_agent2.c (deflated 69%)

adding: s_agent.c (deflated 73%)

adding: s_bridge.c (deflated 74%)

adding: s_conf.c (deflated 74%)

adding: s_ftp.c (deflated 79%)

adding: s_host.c (deflated 73%)

adding: s_htserv.c (deflated 76%)

adding: s_http.c (deflated 75%)

adding: s_mime.c (deflated 61%)

adding: s_pop3.c (deflated 66%)

adding: s_run.c (deflated 58%)

adding: s_server.c (deflated 69%)

adding: s_smtp.c (deflated 52%)

adding: s_socks.c (deflated 79%)

adding: s_task.c (deflated 65%)

adding: s_tcpfwd.c (deflated 75%)

adding: s_tcpgum.c (deflated 73%)

adding: s_tcphub.c (deflated 75%)

adding: s_telnet.c (deflated 65%)

adding: s_term.c (deflated 72%)

adding: surf.c (deflated 58%)

adding: s_user.c (deflated 72%)

adding: s_via3.c (deflated 52%)

adding: s_via.c (deflated 71%)

adding: s_xort.c (deflated 70%)

[root@web src]# ls -l source.zip

-rw-r-r- 1 root root 57027 11-28 21:37 source.zip

[root@web src]# sz -be source.zip

rz

正在开始 zmodem 传输。 按 Ctrl+C 取消。

正在传输 source.zip...

100%      55 KB    3 KB/s 00:00:15       0 错误

奜O[root@web src]#

问题思考

相关资料

【1】Linux宝库 rz/sz

【2】密州居士 linux上面的sz,rz命令与ssh的配合

【3】本系列 我使用过的Linux命令之rz - 批量上传文件，简单易用

## Linux下rz,sz与ssh的配合使用

[http://blog.csdn.net/itegel84/article/details/5793575](http://blog.csdn.net/itegel84/article/details/5793575)

Linux下rz,sz与ssh的配合使用

linuxsshwindows文件传输工具服务器工具

一般来说,linux服务器大多是通过ssh客户端来进行远程的登陆和管理的,使用ssh登陆linux主机以后,如何能够快速的和本地机器进行文件的交互呢,也就是上传和下载文件到服务器和本地；

与ssh有关的两个命令可以提供很方便的操作:

sz: 将选定的文件发送 (send) 到本地机器

rz: 运行该命令会弹出一个文件选择窗口,从本地选择文件上传到服务器(receive)

rz,sz是便是Linux/Unix同Windows进行ZModem文件传输的命令行工具

windows端需要支持ZModem的telnet/ssh客户端 (比如SecureCRT)

运行命令rz,即是接收文件,SecureCRT就会弹出文件选择对话框,选好文件之后关闭对话框,文件就会上传到当前目录

注意: 单独用rz会有两个问题: 上传中断、上传文件变化 (md5不同) ,解决办法是上传是用rz -be,并且去掉弹出的对话框中"Upload files as ASCII"前的勾选。

-b binary 用binary的方式上传下载,不解释字符为ascii

-e 强制escape 所有控制字符,比如Ctrl+x,DEL等

运行命令sz file1 file2就是发文件到windows上 (保存的目录是可以配置)  比ftp命令方便多了,而且服务器不用再开FTP服务了

PS: Linux上rz/sz这两个小工具安装 lrzsz-x.x.xx.rpm 即可

当然,还可以设置一下目录了:

在SecureCRT设置一下上传和下载的默认目录

options–>session options–>file transfer 下可以设置上传和下载的目录

剩下的你只要在用SecureCRT登陆linux终端的时候:

发送文件到客户端: sz filename

zmodem接收可以自行启动.

从客户端上传文件到linux服务端:

只要服务端执行 : rz

然后在 SecureCRT 里选文件发送,协议 zmodem

------

Linux下和Windows之间的文件传输工具rz/sz(lrz/lsz) 介绍

【什么是rz/sz (lsz/lrz)】

简单说就是,可以很方便地用这两个sz/rz工具,实现Linux下和Windows之间的文件传输(发送和接收),速度大概为10KB/s,适合中小文件。rz/sz 通过Zmodem协议传输数据。

【为什么要用rz/sz】

普通Linux和Windows之间的文件共享方法,主要有建立nfs实现文件共享,和tftp之类的方法,但是都很麻烦,而如果只是小文件 (几十 K,几百K) ,那么直接用rz/sz,就显得极其地方便了。大文件的话,还是要考虑上面说得,其他的共享方法了,毕竟,rz/sz速度只有10K左右,传大文件会累死人的。。。

【如何使用】

(1) 在Windows下,用SecureCRT (或者Windows自带的超级终端) 连接Com端口到开发板,或者ssh等协议连接到Linux服务器上。

(2) 在Linux端,安装了rz/sz (lrz/lsz)工具后 (嵌入式开发中,多数已经将编译好的rz/sz工具放到rootfs中了,普通的Linux系统,如果没有,可以下载源码,自己安装) ,就可以直接运行rz/sz,实现和Windows之间的文件传输了:

A、从windows中拷贝/下载文件到Linux (开发板) :

运行rz后,会自动弹出WIndows下的文件选择对话框,选择对应文件后,添加,然后确定,就开始传输,将windows中的文件,拷贝到Linux中了。

B、将Linux中的文件拷贝到Windows中某个文件夹:

执行sz file_name 就可以将Linux当前文件夹下的文件file_name拷贝到Windows的对应目录中了,其中,Windows目录是由你当前运行的工具中设定的。

此处我用的是SecureCRT,具体的更改 rz上传/sz下载 的默认的路径的方法:

右键点击当前会话session -> Session Options -> Terminal -> Xmodem/Zmodem ->Directories :

Upload : 你要设置的路径

Download:你要设置的路径
