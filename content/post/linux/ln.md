---
title: 'ln link 软连接和硬连接'
author: "-"
date: 2011-07-13T13:44:30+00:00
url: link
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

## 硬连接
  
硬连接指通过索引节点(inode)来进行连接。在Linux的文件系统中，保存在磁盘分区中的文件不管是什么类型都给它分配一个编号，称为索引节点号(Inode Index)。在Linux中，多个文件名指向同一索引节点是存在的。一般这种连接就是硬连接。硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止"误删"的功能。其原因如上所述，因为对应该目录的索引节点有一个以上的连接。只删除一个连接并不影响索引节点本身和其它的连接，只有当最后一个连接被删除后，文件的数据块及目录的连接才会被释放。也就是说，文件真正删除的条件是与之相关的所有硬连接文件均被删除。

## 软连接
  
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

<http://www.cnblogs.com/itech/archive/2009/04/10/1433052.html>

## unlink

rm底层也是执行unlink系统调用

unlink 命令
unlink 命令的 man page 中说明其调用了 unlink(file) 系统调用，于是追根溯源，查看 unlink 系统调用的man page，得到了以下信息：

unlink() deletes a name from the filesystem. If that name was the last link to a file and no processes have the file open the file is deleted and the space it was using is made available for reuse.

If the name was the last link to a file but any processes still have the file open the file will remain in existence until the last file descriptor referring to it is closed.

If the name referred to a symbolic link the link is removed.
If the name referred to a socket, fifo or device the name for it is removed but processes which have the object open may continue to use it.

可以看出，unlink 用于删除文件名。删除文件名是指在原目录下不再含有此文件名。要注意的是，这里的表述是删除文件名，并不一定删除磁盘上文件的内容。只有在文件的链接数为1，即当前文件名是文件的最后一个链接并且有没有进程打开此文件的时候，unlink() 才会真正删除文件内容。用 unlink 真正的删除一个文件内容，必须同时满足以上两个条件。

如果文件链接数为1，但是仍然有进程打开这一文件，那么 unlink 后，虽然在原目录中已经没有了被删除文件的名字，但是实际上系统还是保留了这一文件，直到打开这一文件的所有进程全部关闭此文件后，系统才会真正删除磁盘上的文件内容。由此可见，用unlink直接删除打开的文件是安全的。删除已经打开的文件，对使用此文件的进程，不会有任何影响，也不会导致进程崩溃（注意这里讨论的是删除已被打开的文件，通常是数据文件，并未讨论删除正在运行的可执行文件）。

对于符号链接，unlink 删除的是符号链接本身，而不是其指向的文件。

rm 命令
rm 命令也是删除文件。为了查看rm 与 unlink 的区别，用 strace 跟踪执行 rm 命令时使用的系统调用：

```bash
strace rm data.txt 2>&1 | grep 'data.txt'
```

execve("/bin/rm", ["rm", "data.txt"], [/* 13 vars */]) = 0
lstat("data.txt", {st_mode=S_IFREG|0644, st_size=10, ...}) = 0
stat("data.txt", {st_mode=S_IFREG|0644, st_size=10, ...}) = 0
access("data.txt", W_OK)                = 0
unlink("data.txt")                      = 0
跟踪 unlink 命令的结果：

```bash
strace unlink data.txt 2>&1 | grep 'data.txt'
```

execve("/bin/unlink", ["unlink", "data.txt"], [/* 13 vars */]) = 0
unlink("data.txt")
可以看出，在linux 中，rm 命令比 unlink 命令多了一些权限的检查，之后也是调用了 unlink() 系统调用。在文件允许删除的情况下，rm 命令和 unlink 命令其实是没有区别的。

rename 命令
rename 命令通常用于重命名文件，由于本文研究的是文件的移动和删除，因而只需关注 rename 最简单的使用方法：

```bash
strace rename data.txt  dest_file data.txt 2>&1 | egrep  'data.txt|dest_file'
```

execve("/usr/bin/rename", ["rename", "data.txt", "dest_file", "data.txt"], [/* 13 vars */]) = 0
rename("data.txt", "dest_file")         = 0
可以看出，rename 就是对 rename() 系统调用的封装。

查看 man page 可以看出，当目标文件已经存在时，在权限允许的情况下，rename() 会直接覆盖原来的文件。这里“覆盖原有文件”可能有两种情况：

将原文件清空后写入
删除了旧文件后新建一个同名文件
通过执行下面的命令可以区分出 rename() 执行的 “覆盖” 到底是哪一种情况：

可见，在目标文件 dest_file 已经存在的情况下，执行 rename 后，dest_file 的 i 节点号发生了变化，因而rename() 系统调用的作用类似于上述第二种情形：即删除文件后再新建一个同名文件。

mv 命令
mv 命令通常用于重命名文件。当目标文件不存在时，跟踪其执行过程：

```bash
strace mv data.txt  dest_file 2>&1 | egrep  'data.txt|dest_file'
```

execve("/bin/mv", ["mv", "data.txt", "dest_file"], [/* 13 vars */]) = 0
stat("dest_file", 0x7ffe1b4aab50)       = -1 ENOENT (No such file or directory)
lstat("data.txt", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
lstat("dest_file", 0x7ffe1b4aa900)      = -1 ENOENT (No such file or directory)
rename("data.txt", "dest_file")         = 0
当目标文件存在时：

```bash
strace mv src_data data.txt 2>&1 | egrep 'src_data|data.txt'
```

execve("/bin/mv", ["mv", "src_data", "data.txt"], [/* 13 vars */]) = 0
stat("data.txt", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
lstat("src_data", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
lstat("data.txt", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
stat("data.txt", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
access("data.txt", W_OK)                = 0
rename("src_data", "data.txt")          = 0
可以看出，mv 的主要功能就是检查初始文件和目标文件是否存在及是否有访问权限，之后执行 rename 系统调用，因而，当目标文件存在时，mv 的行为由 rename() 系统调用决定，即类似于删除文件后再重建一个同名文件。

cp 命令
对于cp 命令，当目标文件不存在时：

```bash
strace cp data.txt dest_data 2>&1 | egrep 'data.txt|dest_data'
```

execve("/bin/cp", ["cp", "data.txt", "dest_data"], [/* 13 vars */]) = 0
stat("dest_data", 0x7fff135827f0)       = -1 ENOENT (No such file or directory)
stat("data.txt", {st_mode=S_IFREG|0644, st_size=726, ...}) = 0
stat("dest_data", 0x7fff13582640)       = -1 ENOENT (No such file or directory)
open("data.txt", O_RDONLY)              = 3
open("dest_data", O_WRONLY|O_CREAT, 0100644) = 4
当目标文件存在时：

可见，如果目标文件存在，在执行cp 命令之后，文件的 inode 号并没有改变，并且可以看出，cp 使用了 open 及O_TRUNC 参数打开了目标文件。因而当目标文件已经存在时，cp 命令实际是清空了目标文件内容，之后把新的内容写入目标文件。

结语
至此，我们已经了解了常用的文件操作命令的原理，特别需要关注的是 cp 命令。当目标文件存在时，cp 命令并不是先删除已经存在的目标文件，而是将原目标文件内容清空后再写入。了解这一点对下一篇研究 “覆盖使用中的文件” 将会非常有帮助。

本篇的主要目的是让读者了解 linux 下文件系统的组织方式及常用的操作文件命令的工作原理。有了本篇的知识后，我们就可以深入的研究 ”覆盖或删除正在被使用的文件“ 时操作系统的的行为了，也就能理解在用 cp 命令更新可执行文件时出现 ”Text file busy“ 的原因了。具体的内容，将会在下篇中说明。

><https://zhuanlan.zhihu.com/p/25600743>
