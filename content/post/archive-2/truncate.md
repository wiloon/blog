---
title: 清空文件
author: "-"
date: 2017-09-01T05:11:09+00:00
url: truncate
categories:
  - OS
tags:
  - reprint
  - file
  - remix
---
## 清空文件

在处理服务器磁盘占用时, 比如有比较大的日志文件, 服务还在运行, 所以文件是不能删的, 又因为文件太大了不适合用文本编辑器打开, 比如 vi 之类, 想清空文件就要用以下方法了.

BTW: 删除一个正在使用的文件是另外一个问题...
>wiloon.com/deleteonwrite

## truncate

```bash
truncate -s 0 foo.log
```

truncate 可被用来将一个文件缩小或者扩展到某个给定的大小。  
你可以利用它和 -s 参数来特别指定文件的大小。要清空文件的内容, 则在下面的命令中将文件的大小设定为 0  

本命令缩减或扩充指定文件的大小为指定值。 参数所指定的文件如果不存在,  那么该命令会创建这个文件。

如果一个文件的大小比参数指定的大, 那么**超出**的部分就会被丢弃。 如果一个文件比参数指定的小, 那么文件会被扩充, 并且被扩充的部分 (空洞) 在被读取的时候是字节0。

truncate 函数使用前不需要使用 open 函数打开文件

## 命令格式

```c
truncate 选项 文件列表
```

命令详解: 对于长选项来说必须的参数, 对于短选项来说也是必须的。

```bash
-c, --no-create
    不创建任何文件

-o, --io-blocks
    把参数指定的大小视为 I/O 块,而不是视为字节

-r, --reference=FILE
    使用文件 FILE 的大小作为参考大小

-s, --size=SIZE
    使用 SIZE 指定文件的大小

--help display this help and exit
    显示这个帮助信息

--version
    输出版本信息,然后退出

SIZE 参数可以是 (或者是一个整数后面跟着任意的) 下面的选项: KB 1000, K 1024,
    MB 1000*1000, M 1024*1024, and so on for G, T, P, E, Z, Y.

SIZE 之前也可以加上下面的特性: 
    '+' 增加 SIZE,
    '-' 减少 SIZE,
    '<'最大为 SIZE,
    '>'最小为 SIZE,
    '/'以SIZE为除数,向下取整,
    '%'以SIZE为除数,向上取整。

注意: -r 和 -s 选项是互斥的。
```

## 示例

```bash
truncate -c --size 2000m x.dbf
# 源文件 test.db 和目标文件 test.db.bak
ll -th /root/test.db
-rw-r--r--. 1 root root 12G May 24 01:26 /root/test.db
[root@my1-222 ~]# ll -th /root/test.db.bak
-rw-r--r--. 1 root root 0 May 24 17:51 /root/test.db.bak
[root@my1-222 ~]#

# 利用truncate瞬间制造大小相同的文件
[root@my1-222 ~]# truncate -r test.db test.db.bak
[root@my1-222 ~]# ll -th /root/test.db.bak
-rw-r--r--. 1 root root 12G May 24 17:56 /root/test.db.bak
[root@my1-222 ~]#

[root@my1-222 ~]# truncate  --size 10G test.db.bak
[root@my1-222 ~]# ll -th /root/test.db.bak
-rw-r--r--. 1 root root 10G May 24 18:01 /root/test.db.bak
```

## 文件清空之后的 inode 问题

在文件的写入操作比较繁忙的时候会观察到 清空 文件 之后 用 stat 命令查看 inode信息时, 能看到 文件 长度为0 ,但是过几秒再查看时,文件 长度又变成了清空前的长度,但是 df 命令能看到磁盘空间的确被释放了

可能是因为 truncate 更新  inode之后,  inode 又被 操作系统缓存 的 inode 覆盖掉了, 而df 统计 磁盘空间并不依赖 inode 的信息, 所以会导致数据不一致

### inode 缓存

inode可能处于三种状态：
1）unused，里面没有保存有效的内容，可以被复用为新的用途；

2）in use，正在被使用，其成员i_count以及i_nlink一定大于0，此时inode与文件系统或者说设备上的文件相关联，但是自从上次与设备同步后，内容没有发生改变，即不是dirty的；

3）dirty，inode里面的内容已经与文件系统中的文件内容不一致了，即脏了，需要进行文件同步操作。

前两种状态的inode都各自位于一个全局的链表中，而第三种的inode位于super_block结构体中的一个链表中。

## du, df 统计结果不一致的问题

### df < du -b == ls -l

磁盘空间已经被释放, 但是 inode 没更新成功, 或者 inode更新成功了, 之后又被 inode 缓存覆盖

### df > du

文件从目录里删掉了, 但是还有进程在读写文件, 磁盘空间没有释放. df 是按 superblock 里的信息统计磁盘空间的, du 是按目录关联的 inode 统计的, 所以会不一致.

### 通过重定向到 Null 来清空文件内容

清空或者让一个文件成为空白的最简单方式,是像下面那样,通过 shell 重定向 null  (不存在的事物) 到该文件:

```bash
> access.log
```

Empty Large File Using Null Redirect in Linux

在 Linux 下使用 Null 重定向来清空大文件

### 使用 'true' 命令重定向来清空文件

下面我们将使用 : 符号,它是 shell 的一个内置命令,等同于 true 命令,它可被用来作为一个 no-op (即不进行任何操作) 。

另一种清空文件的方法是将 : 或者 true 内置命令的输出重定向到文件中,具体如下:

```bash
: > access.log
# 或
true > access.log
```

Empty Large File Using Linux Commands

### 使用 Linux 命令清空大文件

使用 cat/cp/dd 实用工具及 /dev/null 设备来清空文件
  
在 Linux 中, null 设备基本上被用来丢弃某个进程不再需要的输出流,或者作为某个输入流的空白文件,这些通常可以利用重定向机制来达到。

所以 /dev/null 设备文件是一个特殊的文件,它将清空送到它这里来的所有输入,而它的输出则可被视为一个空文件。

## cat

可以通过使用 cat 命令 显示 /dev/null 的内容然后重定向输出到某个文件, 以此来达到清空该文件的目的。

有其它进程正在写入的文件也可以操作, 执行之后能看到文件变小, 不影响新数据写入.

```bash
cat /dev/null > access.log
```

Empty File Using cat Command

使用 cat 命令来清空文件

## cp

下面,我们将使用 cp 命令 复制 /dev/null 的内容到某个文件来达到清空该文件的目的,具体如下所示:

```bash
cp /dev/null access.log
```

## dd

而下面的命令中, if 代表输入文件,of 代表输出文件。

```bash
dd if=/dev/null of=access.log
```

## echo

使用 echo 命令清空文件
  
在这里,你可以使用 echo 命令 将空字符串的内容重定向到文件中,具体如下:

```bash
echo "" > access.log
```

或者

```bash
echo > access.log
```

注意: 你应该记住空字符串并不等同于 null 。字符串表明它是一个具体的事物,只不过它的内容可能是空的,但 null 则意味着某个事物并不存在。

基于这个原因,当你将 echo 命令 的输出作为输入重定向到文件后,使用 cat 命令 来查看该文件的内容时,你将看到一个空白行 (即一个空字符串) 。

要将 null 做为输出输入到文件中,你应该使用 -n 选项,这个选项将告诉 echo 不再像上面的那个命令那样输出结尾的那个新行。

```bash
    echo -n "" > access.log
```

[https://www.fengbohello.top/archives/linux-truncate](https://www.fengbohello.top/archives/linux-truncate)
[https://linux.cn/article-8024-1.html#3_5958](https://linux.cn/article-8024-1.html#3_5958)
