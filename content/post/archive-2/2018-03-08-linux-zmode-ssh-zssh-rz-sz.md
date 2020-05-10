---
title: linux, zmodem ssh, zssh, rz, sz
author: wiloon
type: post
date: 2018-03-08T04:14:26+00:00
url: /?p=11974
categories:
  - Uncategorized

---
http://www.cnblogs.com/strikebone/p/3454679.html

zssh的全名叫ZMODEM SSH.看名字就知道，使用的zmodem，我们习惯了SecureCRT,直接就可以用来发送文件，比使用scp方便很多。

zmodem协议方便主要表示在以下点

其一,不需要输入很长的命令和密码，直接使用rz,sz加文件名，就能实现文件的收发。速度还很快。

其二,在中转了一台主机时，要在目标主机和本地主机之类，要传送文件，scp相当的麻烦，需要输入多次命令用户密码.但sz直接可以穿透。

好了，讲使用,如下，和使用ssh完全一样，只是打命令时，变成了zssh

#zssh root@192.168.1.1

好了，在进入后，你需要上传文件的话。先
  
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