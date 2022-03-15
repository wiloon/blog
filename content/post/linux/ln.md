---
title: 'ln  软连接和硬连接'
author: "-"
date: 2011-07-13T13:44:30+00:00
url: /?p=353
categories:
  - Linux

tags:
  - reprint
---
## 'ln  软连接和硬连接'
```bash
#原文件: foo
#symbolic link : bar
#软连接
ln -s foo bar

#硬连接
ln foo bar

# 删除链结
unlink link0
  
```

Linux链接分两种，一种被称为硬链接 (Hard Link) ，另一种被称为符号链接 (soft link, Symbolic Link) 。默认情况下，ln命令产生硬链接。

【硬连接】
  
硬连接指通过索引节点来进行连接。在Linux的文件系统中，保存在磁盘分区中的文件不管是什么类型都给它分配一个编号，称为索引节点号(Inode Index)。在Linux中，多个文件名指向同一索引节点是存在的。一般这种连接就是硬连接。硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止"误删"的功能。其原因如上所述，因为对应该目录的索引节点有一个以上的连接。只删除一个连接并不影响索引节点本身和其它的连接，只有当最后一个连接被删除后，文件的数据块及目录的连接才会被释放。也就是说，文件真正删除的条件是与之相关的所有硬连接文件均被删除。

【软连接】
  
另外一种连接称之为符号连接 (Symbolic Link) ，也叫软连接。软链接文件有类似于Windows的快捷方式。它实际上是一个特殊的文件。在符号连接中，文件实际上是一个文本文件，其中包含的有另一文件的位置信息。

2.通过实验加深理解
  
[oracle@Linux]$ touch f1 #创建一个测试文件f1
  
[oracle@Linux]$ ln f1 f2 #创建f1的一个硬连接文件f2
  
[oracle@Linux]$ ln -s f1 f3 #创建f1的一个符号连接文件f3
  
[oracle@Linux]$ ls -li # -i参数显示文件的inode节点信息
  
total 0
  
9797648 -rw-r-r- 2 oracle oinstall 0 Apr 21 08:11 f1
  
9797648 -rw-r-r- 2 oracle oinstall 0 Apr 21 08:11 f2
  
9797649 lrwxrwxrwx 1 oracle oinstall 2 Apr 21 08:11 f3 -> f1

从上面的结果中可以看出，硬连接文件f2与原文件f1的inode节点相同，均为9797648，然而符号连接文件的inode节点不同。

[oracle@Linux]$ echo "I am f1 file" >>f1
  
[oracle@Linux]$ cat f1
  
I am f1 file
  
[oracle@Linux]$ cat f2
  
I am f1 file
  
[oracle@Linux]$ cat f3
  
I am f1 file
  
[oracle@Linux]$ rm -f f1
  
[oracle@Linux]$ cat f2
  
I am f1 file
  
[oracle@Linux]$ cat f3
  
cat: f3: No such file or directory

通过上面的测试可以看出: 当删除原始文件f1后，硬连接f2不受影响，但是符号连接f1文件无效

3.总结
  
依此您可以做一些相关的测试，可以得到以下全部结论: 
  
1).删除符号连接f3,对f1,f2无影响；
  
2).删除硬连接f2，对f1,f3也无影响；
  
3).删除原文件f1，对硬连接f2没有影响，导致符号连接f3失效；
  
4).同时删除原文件f1,硬连接f2，整个文件会真正的被删除。

ln是linux中又一个非常重要命令，它的功能是为某一个文件在另外一个位置建立一个同不的链接，这个命令最常用的参数是-s，具体用法是: ln –s 源文件 目标文件。
  
当我们需要在不同的目录，用到相同的文件时，我们不需要在每一个需要的目录下都放一个必须相同的文件，我们只要在某个固定的目录，放上该文件，然后在其它的目录下用ln命令链接 (link) 它就可以，不必重复的占用磁盘空间。例如: ln –s /bin/less /usr/local/bin/less
  
-s 是代号 (symbolic) 的意思。
  
这里有两点要注意: 第一，ln命令会保持每一处链接文件的同步性，也就是说，不论你改动了哪一处，其它的文件都会发生相同的变化；第二，ln的链接又软链接和硬链接两种，软链接就是ln –s \*\* \*\*，它只会在你选定的位置上生成一个文件的镜像，不会占用磁盘空间，硬链接ln \*\* \*\*，没有参数-s， 它会在你选定的位置上生成一个和源文件大小相同的文件，无论是软链接还是硬链接，文件都保持同步变化。
  
如果你用ls察看一个目录时，发现有的文件后面有一个@的符号，那就是一个用ln命令生成的文件，用ls –l命令去察看，就可以看到显示的link的路径了。
  
指令详细说明
  
指令名称 : ln
  
使用权限 : 所有使用者
  
使用方式 : ln [options] source dist，其中 option 的格式为 :
  
[-bdfinsvF] [-S backup-suffix] [-V {numbered,existing,simple}]
  
[-help] [-version] [-]
  
说明 : Linux/Unix 档案系统中，有所谓的连结(link)，我们可以将其视为档案的别名，而连结又可分为两种 : 硬连结(hard link)与软连结(symbolic link)，硬连结的意思是一个档案可以有多个名称，而软连结的方式则是产生一个特殊的档案，该档案的内容是指向另一个档案的位置。硬连结是存在同一个档案系统中，而软连结却可以跨越不同的档案系统。
  
ln source dist 是产生一个连结(dist)到 source，至于使用硬连结或软链结则由参数决定。
  
不论是硬连结或软链结都不会将原本的档案复制一份，只会占用非常少量的磁碟空间。
  
-f : 链结时先将与 dist 同档名的档案删除
  
-d : 允许系统管理者硬链结自己的目录
  
-i : 在删除与 dist 同档名的档案时先进行询问
  
-n : 在进行软连结时，将 dist 视为一般的档案
  
-s : 进行软链结(symbolic link)
  
-v : 在连结之前显示其档名
  
-b : 将在链结时会被覆写或删除的档案进行备份
  
-S SUFFIX : 将备份的档案都加上 SUFFIX 的字尾
  
-V METHOD : 指定备份的方式
  
-help : 显示辅助说明
  
-version : 显示版本
  
范例 :

将档案 yy 产生一个 hard link : zz
  
ln yy xx

http://www.cnblogs.com/itech/archive/2009/04/10/1433052.html