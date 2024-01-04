---
title: linux 目录
author: "-"
date: 2012-02-05T10:42:19+00:00
url: linux/dir
categories:
  - Linux
tags:
  - reprint
  - remix
---
## linux 目录, Filesystem Hierarchy Standard (FHS)

https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

[https://my.oschina.net/njzjf/blog/317331](https://my.oschina.net/njzjf/blog/317331)

## /

根目录，一般根目录下只存放目录，不要存放文件，/etc、/bin、/dev、/lib、/sbin 应该和根目录放置在一个分区中

## /bin

In Arch Linux the /bin is a symlink to /usr/bin

### /mnt

这个目录一般是用于存放挂载储存设备的挂载目录的，比如有 cdrom 等目录。可以参看 /etc/fstab 的定义。有时我们可以把让系统开机自动挂载文件系统，把挂载点放在这里也是可以的。主要看/etc/fstab中怎么定义了；比如光驱可以挂载到/mnt/cdrom 。

### /opt

表示的是可选择的意思，有些软件包也会被安装在这里，也就是自定义软件包，比如在 Fedora Core 5.0中，OpenOffice 就是安装在这里。有些我们自己编译的软件包，就可以安装在这个目录中；通过源码包安装的软件，可以通过 ./configure -prefix=/opt/目录 。

/opt目录用来安装附加软件包，是用户级的程序目录，可以理解为D:/Software。安装到/opt目录下的程序，它所有的数据、库文件等等都是放在同个目录下面。opt有可选的意思，这里可以用于放置第三方大型软件（或游戏），当你不需要时，直接rm -rf掉即可。在硬盘容量不够时，也可将/opt单独挂载到其他磁盘上使用。

/proc 操作系统运行时，进程 (正在运行中的程序) 信息及内核信息 (比如cpu、硬盘分区、内存信息等) 存放在这里。/proc目录伪装的文件系统proc的挂载目录，proc并不是真正的文件系统，它的定义可以参见 /etc/fstab 。

## /root

启动Linux时使用的一些核心文件。如操作系统内核、引导程序Grub等。

## /home

存储普通用户的个人文件

bin - 系统启动时需要的执行文件 (二进制)

sbin - 可执行程序的目录，但大多存放涉及系统管理的命令。只有root权限才能执行

proc - 虚拟，存在linux内核镜像；保存所有内核参数以及系统配置信息

1 - 进程编号

## /lib

软链 /usr/lib

## /lib64

软链 /usr/lib

## /snap

软链 /var/lib/snapd/snap

modules - 可加载模块，系统崩溃后重启所需模块

dev - 设备文件目录

etc - 配置文件

skel - home 目录建立，该目录初始化

sysconfig - 网络，时间，键盘等配置目录

var

file

lib - 该目录下的文件在系统运行时，会改变

local - 安装在/usr/local的程序数据，变化的

lock - 文件使用特定外设或文件，为其上锁，其他文件暂时不能访问

log - 记录日志

run - 系统运行合法信息

spool - 打印机、邮件、代理服务器等假脱机目录

tmp

catman - 缓存目录

mnt - 临时用于挂载文件系统的地方。一般情况下这个目录是空的，而在我们将要挂载分区时在这个目录下建立目录，再将我们将要访问的设备挂载在这个目录上，这样我们就可访问文件了。

tmp - 临时文件目录，系统启动后的临时文件存放在/var/tmp

lost+found - 在文件系统修复时恢复的文件

## /sbin, /usr/sbin, /usr/local/sbin

In Arch Linux the /sbin is a symlink to /usr/bin

这个目录是用来存放系统管理员的系统管理程序。大多是涉及系统管理的命令的存放，是超级权限用户 root 的可执行命令存放地，普通用户无权限执行这个目录下的命令，这个目录和 `/usr/sbin`, `/usr/X11R6/sbin` 或 `/usr/local/sbin` 目录是相似的；我们记住就行了，凡是目录sbin中包含的都是 root 权限才能执行的。

/sbin 一般是指超级用户指令。主要放置一些系统管理的必备程序例如: cfdisk、dhcpcd、dump、e2fsck、fdisk、halt、ifconfig、ifup、 ifdown、init、insmod、lilo、lsmod、mke2fs、modprobe、quotacheck、reboot、rmmod、 runlevel、shutdown等。

/usr/sbin   放置一些用户安装的系统管理的必备程式例如: dhcpd、httpd、imap、in.*d、inetd、lpd、named、netconfig、nmbd、samba、sendmail、squid、swap、tcpd、tcpdump等。
如果新装的系统，运行一些很正常的诸如: shutdown，fdisk的命令时，悍然提示: bash:command not found。那么
首先就要考虑root 的$PATH里是否已经包含了这些环境变量。
可以查看PATH，如果是: PATH=$PATH:$HOME/bin则需要添加成如下:
PATH=$PATH:$HOME/bin:/sbin:/usr/bin:/usr/sbin

### traditional saying

放置系统管理员使用的/基本的系统命令/可执行命令，如fdisk、shutdown、mount等, 用于启动系统，修复系统, 与 /bin 不同的是，这几个目录是给系统管理员 root 使用的命令，一般用户只能 "查看" 而不能设置和使用。

/tmp: 一般用户或正在执行的程序临时存放文件的目录,任何人都可以访问,重要数据不可放置在此目录下

/srv: 服务启动之后需要访问的数据目录，如www服务需要访问的网页数据存放在/srv/www内

## /usr

系统级的目录，可以理解为 C:/Windows/

在早期的 Unix 实现中, usr 目录用于存放用户相关的数据相当于现在的 /home 目录, /usr 目录现在用于存放用户空间的程序和数据
usr 并不是 user 用户的缩写，而是 User System Resources 的缩写

存放应用程序，/usr/bin 存放应用程序，/usr/share 存放共享数据，/usr/lib 存放不能直接运行的，却是许多程序运行所必需的一些函数库文件。/usr/local:存放软件升级包。/usr/share/doc:系统说明文件存放目录。/usr/share/man: 程序说明文件存放目录，使用 man ls时会查询/usr/share/man/man1/ls.1.gz的内容建议单独分区，设置较大的磁盘空间

## /usr/bin

系统启动时需要的执行文件 (二进制)  
/bin 下存放一些普通的基本命令, /bin 下的命令管理员和一般的用户都可以使用。
几乎所有用户所用命令，另外存在与 /bin，/usr/local/bin  
可执行二进制文件的目录，如常用的命令 ls、tar、mv、cat 等。

/usr/bin 是你在后期安装的一些软件的运行脚本。主要放置一些应用软体工具的必备执行档例如c++、g++、gcc、chdrv、diff、dig、du、eject、elm、free、gnome*、 gzip、htpasswd、kfm、ktop、last、less、locale、m4、make、man、mcopy、ncftp、 newaliases、nslookup passwd、quota、smb*、wget等。

/boot: 放置linux系统启动时用到的一些文件。/boot/vmlinuz为linux的内核文件，以及/boot/gurb。建议单独分区，分区大小100M即可

/dev: 存放linux系统下的设备文件，访问该目录下某个文件，相当于访问某个设备，常用的是挂载光驱mount /dev/cdrom /mnt。

/etc: 系统配置文件存放的目录，不建议在此目录下存放可执行文件，重要的配置文件有/etc/inittab、/etc/fstab、/etc/init.d、/etc/X11、/etc/sysconfig、/etc/xinetd.d修改配置文件之前记得备份。

注: /etc/X11存放与x windows有关的设置。

/home: 系统默认的用户家目录，新增用户账号时，用户的家目录都存放在此目录下，~表示当前用户的家目录，~test表示用户test的家目录。建议单独分区，并设置较大的磁盘空间，方便用户存放数据

/lib:/usr/lib:/usr/local/lib: 系统使用的函数库的目录，程序在执行过程中，需要调用一些额外的参数时需要函数库的协助，比较重要的目录为/lib/modules。

/lost+fount: 系统异常产生错误时，会将一些遗失的片段放置于此目录下，通常这个目录会自动出现在装置目录下。如加载硬盘于/disk 中，此目录下就会自动产生目录/disk/lost+found

/mnt:/media: 光盘默认挂载点，通常光盘挂载于/mnt/cdrom下，也不一定，可以选择任意位置进行挂载。

/proc: 此目录的数据都在内存中，如系统核心，外部设备，网络状态，由于数据都存放于内存中，所以不占用磁盘空间，比较重要的目录有/proc/cpuinfo、/proc/interrupts、/proc/dma、/proc/ioports、/proc/net/*等

/root: 系统管理员root的家目录，系统第一个启动的分区为/，所以最好将/root和/放置在一个分区下。

## /usr/lib

程序和核心模块的公共库  
理解为 C:/Windows/System32。

## /usr/local

- /usr/local/bin 二进制文件
- /usr/local/etc 配置文件

本地安装软件保存位置

用户级的程序目录，可以理解为 C:/Progrem Files/。用户自己编译的软件默认会安装到这个目录下。
这里主要存放那些手动安装的软件，即不是通过 apt-get 安装的软件。它和 /usr 目录具有相类似的目录结构。让软件包管理器来管理 /usr 目录，而把自定义的脚本 (scripts) 放到 /usr/local 目录下面。

## /usr/include

存放 C/C++ 头文件的目录

bin -

sbin - 系统管理员命令，与用户相关，例如，大部分服务器程序

man - 手工生成的目录

info - 信息文档

doc - 不同包文档信息

tmp

X11R6 - 该目录用于保存运行X-Window所需的所有文件。该目录中还包含用于运行GUI要的配置文件和二进制文件。

X386- 功能同X11R6，X11 发行版5 的系统文件

boot - 引导加载器所需文件，系统所需图片保存于此

## /var

放置系统执行过程中**经常变化**的文件，如随时更改的日志文件

- /var/log，/var/log/message:
- 所有的登录文件存放目录，
- /var/spool/mail: 邮件存放的目录，
- /var/run: 程序或服务启动后，其PID存放在该目录下。建议单独分区，设置较大的磁盘空间
- /var/lib/redis: redis 的数据文件

其实转这个帖子就像探究一个问题，就是我们自行开发的软件应该放在哪个目录比较合适

1. /home 目录下 理由是我们在安装linux系统时给这个目录单独分区，空间大，所以放在这个目录下
2. /opt 目录下，大多数都这么搞；
3. /usr 目录下

二进制 /usr/local/bin/foo
配置文件 /etc/foo/config.toml
db      /var/lib/foo/foo.db
日志    /var/log/foo/debug.log

[https://blog.csdn.net/kkdelta/article/details/7708250](https://blog.csdn.net/kkdelta/article/details/7708250)

而/usr/bin,/usr/sbin与/sbin /bin目录的区别在于:

/bin,/sbin目录是在系统启动后挂载到根文件系统中的，所以/sbin,/bin目录必须和根文件系统在同一分区；

/usr/bin,usr/sbin可以和根文件系统不在一个分区。

/usr/sbin存放的一些非必须的系统命令；/usr/bin存放一些用户命令，如led(控制LED灯的)。

转下一位网友的解读，个人认为诠释得很到位:

/bin 是系统的一些指令。bin为binary的简写主要放置一些系统的必备执行档例如:cat、cp、chmod df、dmesg、gzip、kill、ls、mkdir、more、mount、rm、su、tar等。


## /root

Linux超级权限用户root的家目录。

## /selinux

好像是对SElinux的一些配置文件目录，SElinux可以让你的linux更加安全。

## /srv

服务启动后，所需访问的数据目录，举个例子来说，www服务启动读取的网页数据就可以放在/srv/www中

### /sys

Linux 内核中设计较新的一种虚拟的基于内存的文件系统，它的作用与 proc 有些类似，但除了与 proc 相同的具有查看和设定内核参数功能之外，还有为 Linux 统一设备模型作为管理之用。

## /tmp

临时文件目录，用来存放不同程序执行时产生的临时文件。有时用户运行程序的时候，会产生临时文件。/tmp就用来存放临时文件的。/var/tmp目录和这个目录相似。

## /usr

这是linux系统中占用硬盘空间最大的目录。用户的很多应用程序和文件都存放在这个目录下。在这个目录下，你可以找到那些不适合放在/bin或/etc目录下的额外的工具。比如像游戏啊，一些打印工具拉等等。 /usr目录包含了许多子目录:  /usr/bin目录用于存放程序;/usr/share用于存放一些共享的数据，比如音乐文件或者图标等等;/usr/lib目录用于存放那些不能直接 运行的，但却是许多程序运行所必需的一些函数库文件。你的软件包管理器(应该是"新立得"吧)会自动帮你管理好/usr目录的。

## /usr/local

这里主要存放那些手动安装的软件，即不是通过"新立得"或apt-get安装的软件。它和/usr目录具有相类似的目录结构。让软件包管理器来管理/usr目录，而把自定义的脚本(scripts)放到/usr/local目录下面，我想这应该是个不错的主意。

## /usr/share

系统共用的东西存放地，比如 /usr/share/fonts 是字体目录，/usr/share/doc和/usr/share/man帮助文件。

## /var

这个目录的内容是经常变动的，看名字就知道，我们可以理解为vary的缩写，/var下有/var/log 这是用来存放系统日志的目录。/var/ www目录是定义Apache服务器站点存放目录；/var/lib 用来存放一些库文件，比如MySQL的，以及MySQL数据库的的存放地。
