---
title: ulimit, Linux 下设置最大文件打开数 nofile, nr_open
author: "-"
date: 2017-02-20T01:15:40+00:00
url: ulimit
categories:
  - Linux
tags:
  - reprint
  - remix

---
## ulimit, Linux 下设置最大文件打开数 nofile, nr_open

- ulimit
- file-max
- nr_open
- soft limit
- hard limit
- shell 级限制
- 用户级限制
- systemd 的 ulimit 配置

ulimit 是用于获取或者修改 shell 和 shell 创建的进程的 资源限制的一个 linux 内置命令, 是系统调用 setrlimit 的封装.

ulimit 控制的是 **shell 级**的限制

## 格式

```bash
ulimit [-SHabcdefiklmnpqrstuvxPT] [limit]
```

## ulimit 参数

- -a: 显示当前所有的 limit 信息。
- -n: 显示可以打开最大文件描述符的数量。ulimit -n 128: 设置最大可以使用 128 个文件描述符。
- -s: 线程栈大小,以 Kbytes 为单位. ulimit – s 512；限制线程栈的大小为 512 Kbytes.
  - 操作系统栈大小 (ulimit -s) : 这个配置只影响进程的初始线程；后续用pthread_create创建的线程都可以指定栈大小。
- -H: use the hard resource limit
- -S: 设置软资源限制,设置后可以增加,但是不能超过硬资源设置。 ulimit – Sn 32；限制软资源,32 个文件描述符。

- -c 最大的 core 文件的大小, 以 blocks 为单位。 ulimit – c unlimited； 对生成的 core 文件的大小不进行限制。
- -d 进程最大的数据段的大小,以 Kbytes 为单位。 ulimit -d unlimited；对进程的数据段大小不进行限制。
- -f 进程可以创建文件的最大值,以 blocks 为单位。 ulimit – f 2048；限制进程可以创建的最大文件大小为 2048 blocks。
- -l 最大可加锁内存大小,以 Kbytes 为单位。 ulimit – l 32；限制最大可加锁内存大小为 32 Kbytes。
- -m 最大内存大小,以 Kbytes 为单位。 ulimit – m unlimited；对最大内存不进行限制。
- -p 管道缓冲区的大小,以 Kbytes 为单位。 ulimit – p 512；限制管道缓冲区的大小为 512 Kbytes。
- -t 最大的 CPU 占用时间,以秒为单位。 ulimit – t unlimited；对最大的 CPU 占用时间不进行限制。
- -u 用户最大可用的进程数。 ulimit – u 64；限制用户最多可以使用 64 个进程。
- -v 进程最大可用的虚拟内存, 以 Kbytes 为单位。 ulimit – v 200000；限制最大可用的虚拟内存为 200000 Kbytes。

执行的时候不加 [limit] 部分会打印当前值, 不加任何参数的话, 默认是 -f

## 文件句柄数

直接参考 ulimit 的帮助文档 (注意: 不是 man ulimit, 而是 help ulimit, ulimit 是内置命令, 前者提供的是 C 语言的 ulimit 帮助 ) :  

>Modify shell resource limits. Provides control over the resources available to the shell and processes it creates, on systems that allow such control.  

可以看出, ulimit 提供了对 shell (或 shell 创建的进程) 可用资源的管理。除了打开文件数之外, 可管理的资源有:
最大写入文件大小、最大堆栈大小、core dump 文件大小、cpu 时间限制、 最大虚拟内存大小等等, help ulimit 会列出每个 option 限制的资源  

### 什么是 soft limit 和 hard limit

A hard limit is the maximum allowed to a user, set by the superuser/root. This value is set in the file /etc/security/limits.conf. Think of it as an upper bound or ceiling or roof.
A soft limit is the effective value right now for that user. The user can increase the soft limit on their own in times of needing more resources, but cannot set the soft limit higher than the hard limit.

hard limit 和 soft limit 都是对单个用户的限制, soft limit 设置的值不能大于 hard limit

### 示例

```bash
ulimit -a
# open files (-n) 1024

# view hard limits
ulimit -Hn
ulimit -H -n

# view soft limits
ulimit -Sn
ulimit -S -n

# set hard limit, 设置当前shell的最大文件数,shell 退出时失效
ulimit -Hn 2048

# set soft limit, 设置当前shell的最大文件数,shell 退出时失效
ulimit -Sn 2048

# hard limit, soft limit 一起设置
ulimit -n 65535
# 查看某一个进程的 limit
cat /proc/PID/limits
```

#### 永久设置

一条记录包含 4 列,分别是范围 domain (即生效的范围, 可以是用户名、group 名或 * 代表所有非 root 用户) ；t 类型 type: 即 soft、hard, 或者-代表同时设置 soft 和 hard；项目 item, 即 ulimit 中的资源控制项目,名字枚举可以参考文件中的注释；最后就是 value。比如将所有非 root 用户的 nofile 设置为 100000

#### 编辑 vim /etc/security/limits.conf 在最后加入

/etc/security/limits.d/ 中可以配置, 系统是先加载limits.conf然后按照英文字母顺序加载limits.d目录下的配置文件,后加载配置覆盖之前的配置。

如果 limits.conf 里不做任何限制, 则重新登录进来后, ulimit -Sn 显示为 1024。

不过,在CentOS 7 / RHEL 7, archlinux 等系统中, 使用 Systemd 替代了之前的 SysV, 因此 /etc/security/limits.conf 文件的配置作用域缩小了一些。limits.conf这里的配置,只适用于通过PAM认证登录用户的资源限制,它对systemd的service的资源限制不生效。登录用户的限制,与上面讲的一样,通过 /etc/security/limits.conf 和 limits.d 来配置即可。

```bash
# 或者只加入, -"字符设定, 则 hard 和 soft 设定会同时被设定。
 * - nofile 8192

# 最前的 * 表示所有用户, 可根据需要设置某一用户, 例如
* soft nofile 4096
* hard nofile 4096

# 用户级限制， 设置某一个用户的文件数
wiloon soft nofile 8192
wiloon hard nofile 8192

# 修改后重启生效

# limits.conf, 其它设置
* soft nproc 100000
* hard nproc 100000
* soft core 100000
* hard core 100000
```

### 查看某一运行中进程的资源限制

```bash
cat /proc/<PID>/limits
```

### 查看当前系统打开的文件数量

losf 命令虽然作用是 "list open files", 但用 lsof | wc -l 统计打开文件数上非常不准确。主要原因是，某些情况下,一行可能显示的是线程, 而不是进程, 对于多线程的情况, 就会误以为一个文件被重复打开了很多次
  
子进程会共享 file handler
  
如果用 lsof 统计, 必须使用精巧的过滤条件。更简单和准确的方法是, 通过 /proc 目录查看。 获取系统打开文件数, 直接查看 /proc/sys/file-nr, 其中第一个数字就是打开的 file 数 ( file-nr 说明参考: www.kernel.org/doc/Documen…)。 要查看一个进程的打开文件数, 直接查看目录 /proc/$pid/fd 里的文件数即可:

```bash
lsof | wc -l
watch "lsof | wc -l"
cat /proc/sys/fs/file-nr

# 查看某一进程的打开文件数量
lsof -p pid | wc -l
ls -l /proc/<PID>/fd |wc -l

# ulimit 不加参数
# If no option is given, then -f is assumed. 进程可以创建文件的最大值
# 默认会打印出 unlimited
```

### Java 的 nofile

JDK 的实现中, 会直接将 nofile 的 soft 先改成了和 hard 一样的值
  
<https://stackoverflow.com/questions/30487284/how-and-when-and-where-jvm-change-the-max-open-files-value-of-linux>

## file-max, 控制内核总共可以打开的文件数

```bash
/proc/sys/fs/file-max
```

file-max 似乎跟内存大小有关，16G 内存的机器，查到的默认值 是 9223372036854775807， 9京

系统级的限制打开文件数量(文件描述符数量)的配置  
所有用户打开文件描述符的总和  
控制内核总共可以打开的文件数  
一般修改 /proc/sys/fs/file-max 后, 应用程序需要把 /proc/sys/fs/inode-max 设置为 /proc/sys/fs/fs/file-max 值的 3-4 倍, 否则可能导致 inode 数不够用。

man proc, 可得到 file-max 的描述:
  
/proc/sys/fs/file-max
  
This file defines a system-wide limit on the number of open files for all processes. (See also setrlimit(2), which can be used by a process to set the per-process limit, RLIMIT_NOFILE, on the number of files it may open.) If you get lots of error messages about running out of file handles, try increasing this value

即 file-max 是设置系统所有进程一共可以打开的文件数量。 同时一些程序可以通过 setrlimit 调用, 设置每个进程的限制。 如果遇到`文件描述符耗尽`的错误信息, 是应该增加这个值。

```bash
#临时修改
echo  6553560 > /proc/sys/fs/file-max

# 或修改 /etc/sysctl.d/10-default.conf, 加入
fs.file-max = 6553560  #重启生效或者用sysctl -p 加载配置文件.
```

### fs.nr_open, /proc/sys/fs/nr_open

file-max 是内核可分配的最大文件数,  
nr_open 是单个进程可分配的最大文件数,  
所以在我们使用 ulimit 或 limits.conf 来设置时, 如果要超过默认的 1048576 值时需要先增大 nr_open 值 (sysctl -w fs.nr_open=100000000 或者直接写入 sysctl.conf 文件)

### ulimit

file-handles (即文件句柄)
  
file discriptor (FD,即文件描述符)

Provides control over the resources available to the shell and to processes started by it, on systems that allow such control.
  
即设置当前shell以及由它启动的进程的资源限制。
  
显然,对服务器来说, file-max, ulimit 都需要设置, 否则就可能出现文件描述符用尽的问题, 为了让机器在重启之后仍然有效, 强烈建立作以下配置, 以确保file-max, ulimit的值正确无误

在 bash 中, 有个ulimit 命令, 提供了对 shell 及该shell 启动的进程的可用资源控制。主要包括打开文件描述符数量、用户的最大进程数量、coredump文件的大小等。

## Systemd ulimit 配置
  
### 全局的配置
  
/etc/systemd/system.conf
  
/etc/systemd/user.conf
  
systemd.conf.d/*.conf 中的配置会覆盖 system.conf。

DefaultLimitCORE=infinity
  
DefaultLimitNOFILE=100000
  
DefaultLimitNPROC=100000

注意: 修改了system.conf 后,需要重启系统才会生效。

针对单个Service, 也可以设置, 以 nginx 为例。
  
编辑 /usr/lib/systemd/system/nginx.service 文件, 或者 /usr/lib/systemd/system/nginx.service.d/my-limit.conf 文件,做如下配置:

[Service]
  
LimitCORE=infinity
  
LimitNOFILE=100000
  
LimitNPROC=100000

然后运行如下命令,才能生效。

sudo systemctl daemon-reload
  
sudo systemctl restart nginx.service

soft nofile 表示软限制, hard nofile 表示硬限制, 软限制要小于等于硬限制。上面两行语句表示, root用户的软限制为1000, 硬限制为1200, 即表示root 用户能打开的最大文件数量为 1000, 不管它开启多少个shell。

## 系统级限制
  
修改 cat /proc/sys/fs/file-max

但是呢,有很多很重要的细节,有很多错误的描述,一塌糊涂,因此特的在这里做一个说明。
  
一 ulimit -n
  
网上很多人说,ulimit -n限制用户单个进程的问价打开最大数量。严格来说,这个说法其实是错误的。看看ulimit官方描述:
  
Provides control over the resources available to the shell and to processes started by it, on systems that allow such control. The -H and -S options specify that the hard or soft limit is set for the given resource. A hard limit cannot be increased once it is set; a soft limit may be increased up to the value of the hard limit. If neither -H nor -S is specified, both the soft and hard limits are set. The value of limit can be a number in the unit specified for the resource or one of the special values hard, soft, or unlimited, which stand for the current hard limit, the current soft limit, and no limit, respectively.
  
If limit is omitted, the current value of the soft limit of the resource is printed, unless the -H option is given. When more than one resource is specified, the limit name and unit are printed before the value.

人家从来就没说过是限制用户的单个进程的最大文件打开数量,看看红色部分,是限制当前shell以及该shell启动的进程打开的文件数量。为什么会给人限制单个线程的最大文件数量的错觉,因为很多情况下,在一个shell环境里,虽然可能会有多个进程,但是非常耗费文件句柄的进程不会很多,只是其中某个进程非常耗费文件句柄,比如服务器上运行着一个tomcat,那么就是java进程要占用大多数文件句柄。此时ulimit设置的最大文件数和java进程耗费的最大文件数基本是对应的,所以会给人这样的一个错觉。

还有,很多文章称ulimit -n 只允许设置得越来越小,比如先执行了ulimit -n 1000,在执行ulimit -n 1001,就会报"cannot modify limit: Operation not permitted"错误。这个其实也是不准确的说法。首先要搞清楚,任何用户都可以执行ulimit,但root用户和非root用户是非常不一样的。
  
非root用户只能越设置越小,不能越设置越大
  
我在机器上以非root先执行:
  
[wxx@br162 etc]$ ulimit -n 900
  
[wxx@br162 etc]$
  
执行成功,再增大:
  
[wxx@br162 etc]$ ulimit -n 901
  
-bash: ulimit: open files: cannot modify limit: Operation not permitted
  
[wxx@br162 etc]$
  
增加失败,如果减少则是OK的:
  
[wxx@br162 etc]$ ulimit -n 899
  
[wxx@br162 etc]$
  
如果再增加到900是不行的:
  
[wxx@br162 etc]$ ulimit -n 900
  
-bash: ulimit: open files: cannot modify limit: Operation not permitted
  
[wxx@br162 etc]$

root用户不受限制
  
首先切换到root:
  
[wxx@br162 etc]$ sudo su –
  
[root@br162 ~]#
  
查看下当前限制:
  
[root@br162 ~]# ulimit -n
  
1000000
  
[root@br162 ~]#
  
增大:
  
[root@br162 ~]# ulimit -n 1000001
  
[root@br162 ~]#可以成功增大,再减小:
  
[root@br162 ~]# ulimit -n 999999
  
[root@br162 ~]#
  
减小也是成功的,再增大:
  
[root@br162 ~]# ulimit -n 1000002
  
[root@br162 ~]#也是ok的,可见root是不受限制的。
  
二 /etc/security/limits.conf
  
网上还有缪传,ulimit -n 设定的值不能超过limits.conf里设定的文件打开数 (即soft nofile)
  
好吧,其实这要分两种情况,root用户是可以超过的, 比如当前limits.conf设定如下:
  
root soft nofile 2000
  
root hard nofile 2001
  
但是我用root将最大文件数设定到5000是成功的:
  
[root@zk203 ~]# ulimit -n 5000
  
[root@zk203 ~]# ulimit -n
  
5000
  
[root@zk203 ~]#
  
但是非root用户是不能超出limits.conf的设定,我切换到wxx,执行命令如下:
  
[wxx@zk203 ~]# ulimit -n 5000
  
-bash: ulimit: open files: cannot modify limit: Operation not permitted
  
[wxx@zk203 etc]$
  
所以网上的说法是错误的,即使非root用户的最大文件数设置不能超过limits.conf的设置,这也只是一个表象,实际上是因为,每个用户登录进来,ulimit -n的默认值是limits.conf的 soft nofile指定的,但是对于非root用户,ulimit -n只能越来越小,不能越来越大,其实这个才是真正的原因,但是结果是一样的。

修改了limits.conf需要重启系统？
  
这个说法非常搞笑,修改了limits.conf,重新登录进来就生效了。在机器上试试就知道了,好多人真的很懒,宁愿到处问也不愿意花一分钟时间实际操作一下。

三 /proc/sys/fs/file-max
  
网上说,ulimit -n 和limits.conf里最大文件数设定不能超过/proc/sys/fs/file-max的值,这也是搞笑了,/proc/sys/fs/file-max是系统给出的建议值,系统会计算资源给出一个和合理值,一般跟内存有关系,内存越大,改值越大,但是仅仅是一个建议值,limits.conf的设定完全可以超过/proc/sys/fs/file-max。
  
[root@zk203 ~]# cat /proc/sys/fs/file-max
  
1610495
  
我将limits.conf里文件最大数量设定为1610496,保存后,打印出来:
  
[root@zk203 ~]# cat /etc/security/limits.conf
  
root soft nofile1610496root hard nofile1610496

四 总结一下
  
/proc/sys/fs/file-max限制不了/etc/security/limits.conf
  
只有root用户才有权限修改/etc/security/limits.conf
  
对于非root用户, /etc/security/limits.conf会限制ulimit -n,但是限制不了root用户
  
对于非root用户,ulimit -n只能越设置越小,root用户则无限制

### soft, hard

在命令上,ulimit通过-S和-H来区分soft和hard。如果没有指定-S或-H,在显示值时指的是soft,而在设置的时候指的是同时设置soft和hard值。

但soft和hard的区别是什么是什么呢？下面这段解释较为准确 (来自man 2 getrlimit )

The soft limit is the value that the kernel enforces for the corresponding resource. The hard limit acts as a ceiling for the soft limit: an unprivileged process may set only its soft limit to a value in the range from 0 up to the hard limit, and\*\* (irre‐versibly) \*\*lower its hard limit. A privileged process (under Linux: one with the CAP_SYS_RESOURCE capability) may make arbitrary changes to either limit value.

归纳soft和hard的区别:

无论何时,soft总是小于等于hard
  
无论是超过了soft还是hard,操作都会被拒绝。结合第一点,这句话等价于: 超过了soft限制,操作会被拒绝。
  
一个process可以修改当前process的soft或hard。但修改需满足规则:

修改后soft不能超过hard。也就是说soft增大时,不能超过hard；
  
hard降低到比当前soft还小,那么soft也会随之降低。
  
非root或root进程都可以将soft可以在[0-hard]的范围内任意增加或降低。
  
非root进程可以降低hard,但不能增加hard。即nofile原来是1000,修改为了900,再修改为1000是不可能的。 (这是一个单向的,有去无回的操作)
  
root进程可以任意修改hard值。

soft和hard在控制上其实并没有区别,都会限制资源的使用,但soft可以被进程在使用前自己修改。

### ulimit 的修改与生效

知道ulimit很好,但更重要的是怎么修改,这是工作中常见的任务。
  
关于ulimit的生效,抓住几点即可:

ulimit的值总是继承父进程的设置。
  
ulimit命令可修改当前shell进程的设置。这也说明,为了保证下次生效,修改的地方要具有持久性 (至少相当于目标进程而言) ,比如.bashrc,或进程的启动脚本)
  
从第2点也可以推出,运行中的进程,不受ulimit的修改影响。
  
增加hard值,只能通过root完成

作者: maoshuai
  
链接: <https://juejin.im/post/5d4cf32f6fb9a06b1d21312c>
  
来源: 掘金
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

<https://juejin.im/post/5d4cf32f6fb9a06b1d21312c>

<http://www.wiloon.com/?p=9913>

<http://www.wiloon.com/?p=9913&embed=true#?secret=NZmp3nWOGQ>
  
<http://jameswxx.iteye.com/blog/2096461>
  
<https://www.ibm.com/developerworks/cn/linux/l-cn-ulimit/>

<http://smilejay.com/2016/06/centos-7-systemd-conf-limits/>

<http://smilejay.com/2016/06/centos-7-systemd-conf-limits/embed/#?secret=ik43aqQV8y>

<https://zhangxugg-163-com.iteye.com/blog/1108402>

<https://www.cnblogs.com/zengkefu/p/5635153.html>

<https://liqiang.io/post/what-is-soft-limit-and-hard-limit-for-ulimit-590cff7d>

<https://unix.stackexchange.com/questions/80598/ulimit-rlimit-in-linux-are-they-the-same-thing>

<https://pubs.opengroup.org/onlinepubs/009695399/functions/ulimit.html>

<https://linux.die.net/man/2/setrlimit>
