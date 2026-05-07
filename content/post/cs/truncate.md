---
title: 清空文件
author: "-"
date: 2026-05-07T11:12:58+08:00
url: truncate
categories:
  - Linux
tags:
  - file
  - remix
  - AI-assisted
---
## 清空文件

在处理服务器磁盘占用时, 比如有比较大的日志文件, 服务还在运行, 所以文件是不能删的, 又因为文件太大了不适合用文本编辑器打开, 比如 vi 之类, 想清空文件就要用以下方法了.

BTW: 删除一个正在使用的文件是另外一个问题...
>wiloon.com/deleteonwrite

## truncate

```bash
truncate -s 0 foo.log
```

`-s 0` 表示将文件大小设置为 0 字节，即清空文件内容。也可以指定其他大小，truncate 从文件末尾截断，保留开头部分（即最旧的数据）：

```bash
truncate -s 100M foo.log   # 保留前 100MB（最旧的数据）
truncate -s 1G foo.log     # 保留前 1GB
truncate -s 500K foo.log   # 保留前 500KB
```

如果想保留最新的 100MB，需要用 `tail`：

```bash
tail -c 100M foo.log > foo.log.tmp && mv foo.log.tmp foo.log
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

## 对正在写入的文件执行 truncate

truncate 能否正常清空一个正在被写入的文件，**取决于该进程打开文件时是否使用了 `O_APPEND` 标志**。

### 使用 O_APPEND 的进程（大多数情况）

设计良好的日志库（Go 标准库 `log`、zap、zerolog、log4j `FileAppender`、C 的 syslog 等）打开日志文件时都会加 `O_APPEND`。这个标志让每次 `write()` 在内核层面**原子地跳到文件末尾再写入**，不依赖进程自身记录的偏移量。

因此 truncate 之后：文件末尾变为 0，进程下次写入自动从 0 开始，**不产生空洞，直接清空即可**：

```bash
truncate -s 0 app.log
```

验证方法：truncate 后观察文件是否从头正常增长。如果正常增长，说明进程使用了 `O_APPEND`。

### 未使用 O_APPEND 的进程

进程的文件偏移量**不会因 truncate 而重置**。假设进程已写到 500MB 的位置，`truncate -s 0` 之后：

1. 文件大小瞬间变成 0
2. 进程继续从 500MB 的偏移量处写入
3. 文件会迅速"长回来"，0～500MB 之间是稀疏空洞（sparse hole），读取时全是零字节

结果是：**磁盘空间短暂释放，但很快又被重新占用，而且前面是空洞**。

验证方法：truncate 后文件迅速变大，且用 `od -c app.log | head` 能看到大量 `\0`。

**解决方法一：发 SIGHUP 信号**

大多数守护进程（nginx、syslog 等）收到 SIGHUP 后会重新打开日志文件，偏移量从 0 开始：

```bash
truncate -s 0 app.log
kill -HUP <pid>
```

**解决方法二：logrotate `create` 模式（默认）**

重命名旧文件，创建新文件，发信号让进程重新打开，不丢数据：

```
/var/log/app.log {
    rotate 7
    daily
    create
    postrotate
        kill -HUP <pid>
    endscript
}
```

**解决方法三：logrotate `copytruncate` 模式（进程不支持重开文件时的妥协方案）**

先复制旧文件，再截断原文件，进程无需配合，但 copy 和 truncate 之间会丢少量数据：

```
/var/log/app.log {
    copytruncate
}
```

### SIGHUP 信号

SIGHUP（Signal Hang Up）最初为**串行终端**设计。当用户的终端连接断开（挂断调制解调器、关闭 SSH 连接等），内核会向该终端的前台进程组发送 SIGHUP。进程收到 SIGHUP 的默认行为是**终止**。

守护进程启动后脱离终端，SIGHUP 对它们没有"终端断开"的意义，所以很多守护进程的作者把它**重新定义为"重新加载配置/重开日志文件"**的信号。这只是惯例，不是强制的。

| 类型                                       | 通常支持重载                 |
| ------------------------------------------ | ---------------------------- |
| nginx、apache、syslog、sshd 等系统守护进程 | ✅ 是                         |
| 自己写的后台服务（有信号处理逻辑）         | 看实现                       |
| 普通前台程序（cat、python 脚本等）         | ❌ 通常不支持，收到后直接退出 |
| Java 应用（未注册信号处理）                | ❌ JVM 默认不处理，行为不确定 |

判断方法：查文档或 man page，看是否有类似描述："Sending SIGHUP to the process causes it to reopen log files."

### 能感知文件截断的日志采集工具

日志采集侧（读取方）可以通过 inotify 或 stat 轮询感知截断事件，无需写入进程配合：

| 工具                  | 机制      | 行为                             |
| --------------------- | --------- | -------------------------------- |
| `tail -F`（大写 F）   | stat 轮询 | 检测到截断后自动从头读，无需重启 |
| `tail -f`（小写 f）   | 跟随 fd   | 不感知截断，停在原位             |
| Filebeat              | inotify   | 检测到文件缩小，重置读偏移到 0   |
| Fluent Bit / Fluentd  | inotify   | 同上，自动处理 truncate          |
| Vector                | inotify   | 同上                             |
| rsyslog `imfile` 模块 | inotify   | 可感知文件轮转和截断             |

## O_APPEND 与日志写入

`open()` 系统调用的常用标志位（open flags）：

| 分类     | 标志                               | 说明                             |
| -------- | ---------------------------------- | -------------------------------- |
| 访问模式 | `O_RDONLY` / `O_WRONLY` / `O_RDWR` | 只读 / 只写 / 读写，三选一       |
| 创建行为 | `O_CREAT`                          | 文件不存在时创建                 |
|          | `O_EXCL`                           | 配合 `O_CREAT`，文件已存在则报错 |
|          | `O_TRUNC`                          | 打开时直接截断为 0               |
| 写入模式 | `O_APPEND`                         | 每次写入前原子跳到文件末尾       |
|          | `O_SYNC` / `O_DSYNC`               | 每次写入都刷到磁盘（同步写）     |
| 其他     | `O_NONBLOCK`                       | 非阻塞 I/O                       |
|          | `O_CLOEXEC`                        | fork/exec 时自动关闭 fd          |
|          | `O_DIRECT`                         | 绕过页缓存，直接 DMA             |
|          | `O_NOFOLLOW`                       | 不跟随符号链接                   |

### O_APPEND 对日志写入的影响

**1. truncate 后的行为**

带 `O_APPEND`：每次 `write()` 在内核层面原子执行 seek-to-end + write，truncate 后文件末尾在 0，进程下次写入自动从 0 开始，不产生空洞。

不带 `O_APPEND`：进程的文件偏移量停留在 truncate 前的位置，继续从原偏移量写入，0 到原偏移量之间形成稀疏空洞（全为零字节）。

**2. 多线程并发写入的安全性**

`O_APPEND` 的 seek + write 是原子操作，多个 goroutine / 线程同时写不会导致日志行交错，不需要应用层加锁。不带 `O_APPEND` 时必须自己加锁，否则日志行会互相覆盖。

**3. O_SYNC 的额外影响**

加 `O_SYNC` 后每次 `write()` 返回前都等待数据刷到磁盘，进程崩溃不丢日志，但高并发时写入性能会急剧下降。大多数日志框架默认不用 `O_SYNC`，依赖操作系统页缓存定期刷盘。

### O_APPEND 是日志写入的正确姿势

设计良好的日志库基本都用 `O_APPEND`，包括 Go 标准库 `log`、zap、zerolog，以及 C 的 syslog、Java 的 log4j `FileAppender` 等。对于用了 `O_APPEND` 的进程，**直接 `truncate -s 0` 就能干净清空，无副作用**。

如果出现大量零字节空洞（用 `od` 或 `xxd` 可见），说明该应用没有使用 `O_APPEND`，需要 SIGHUP 或重启。

xray-core（Go 编写）打开日志文件时显式加了 `O_APPEND`，因此可以直接 truncate：

```bash
truncate -s 0 /var/log/xray/access.log
truncate -s 0 /var/log/xray/error.log
```

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
