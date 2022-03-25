---
title: zmodem, rz, sz
author: "-"
date: 2018-03-08T04:14:26+00:00
url: zmodem
categories:
  - Uncategorized

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

zssh的全名叫ZMODEM SSH.看名字就知道,使用的zmodem,我们习惯了SecureCRT,直接就可以用来发送文件,比使用scp方便很多。

zmodem协议方便主要表示在以下点

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

SecureCRT可以使用linux下的zmodem协议来快速的传送文件. 在传送之前先设置好上传和下载的目录: 
options->session options ->Terminal->Xmodem/Zmodem 下

Zmodem传输数据会使用到2个命令: 

  sz: 将选定的文件发送 (send) 到本地机器

  rz: 运行该命令会弹出一个文件选择窗口,从本地选择文件上传到服务器(receive)
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

