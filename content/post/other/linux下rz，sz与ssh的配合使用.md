---
title: Linux下rz,sz与ssh的配合使用
author: "-"
date: 2015-09-17T10:42:01+00:00
url: /?p=8297
categories:
  - Uncategorized

tags:
  - reprint
---
## Linux下rz,sz与ssh的配合使用

<http://blog.csdn.net/itegel84/article/details/5793575>

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
