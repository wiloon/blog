---
title: 执行 Shell 脚本, fork, exec, source, shell 执行
author: "-"
date: 2011-12-26T08:30:07+00:00
url: shell/exec
categories:
  - Linux
tags:
  - Shell

---
## 执行 Shell 脚本, fork, exec, source, shell 执行

 cx

```bash
./xxx.sh
sh xxx.sh
```

用户可以用任何编辑程序来编写Shell程序。因为Shell程序是解释执行的，所以不需要编译成目的程序。按照Shell编程的惯例，以bash 为例，程序的第一行一般为"#！/bin/bash"，其中 # 表示该行是注释，叹号 ！ 告诉Shell运行叹号之后的命令并用文档的其余部分作为输入，也就是运行/bin/bash并让/bin/bash去执行Shell程序的内容。
  
执行Shell程序的方法有3种。

### sh Shell 程序文件名

这种方法的命令格式为:

```bash
sh <foo.sh>
```

这实际上是调用一个新的bash命令解释程序，而把Shell程序文件名作为参数传递给它。新启动的Shell将去读指定的文件，可执行文件中列出的命令，当所有的命令都执行完后结束。该方法的优点是可以利用Shell调试功能。

### bash < foo.sh

格式为: bash< Shell程序名

这种方式就是利用输入重定向，使Shell命令解释程序的输入取自指定的程序文件。

### 用 chmod 命令使 Shell 程序成为可执行的，"./Shell文件名"

一个文件能否运行取决于该文档的内容本身可执行且该文件具有执行权。对于Shell程序，当用编辑器生成一个文件时，系统赋予的许可权都是644(rw-r-r-)，用"chomd 755 Shell文件名"命令将其改为可执行的，因此，当用户需要运行这个文件时，"./Shell文件名"来执行就是行了。

在这3种运行Shell程序的方法中，最好按下面的方式选择: 当刚创建一个Shell程序，对它的正确性还没有把握时，应当使用第一种方式进行调试。当一个Shell程序已经调试好时，应使用第三种方式把它固定下来，以后只要键入相应的文件名即可，并可被另一个程序所调用。

## source (.)

使用 source 命令和点号(.)是等价的, 类似于 C/C++ 中的 #include 预处理指令，都是将指定的脚本内容拷贝至当前的脚本中，由同一个 Shell 进程来执行。

source (source /directory/script.sh)
与fork的区别是不新开一个 sub-shell 来执行被调用的脚本，而是在同一个 shell 中执行。所以被调用的脚本中声明的变量和环境变量。 都可以在主脚本中得到和使用。

使用 source 执行命令时, 脚本文件可以没有执行权限, source 命令是 bash 的内置命令，不需要 (也没有) 绝对路径.  
source 命令也称为"点命令"，也就是一个点符号 ". "。 source 命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。
  
用法: 注意点后面有空格

```bash
source filename 或 . filename
```

source命令除了上述的用途之外，还有一个另外一个用途。在对编译系统核心时常常需要输入一长串的命令，如:
  
```bash
make mrproper
make menuconfig
make dep
make clean
make bzImage
```

如果把这些命令做成一个文件，让它自动顺序执行，对于需要多次反复编译系统核心的用户来说会很方便，而用source命令就可以做到这一点，它的作用就是把一个文件的内容当成shell来执行，先在linux的源代码目录下 (如/usr/src/linux-2.4.20) 建立一个文件，如make_command，在其中输入一下内容:
  
```bash
make mrproper &&
make menuconfig &&
make dep &&
make clean &&
make bzImage &&
make modules &&
make modules_install &&
cp arch/i386/boot/bzImage /boot/vmlinuz_new &&
cp System.map /boot &&
vi /etc/lilo.conf &&
lilo -v
```

文件建立好之后，每次编译核心的时候，只需要在/usr/src/linux-2.4.20下输入:

```bash
source make_command
```

即可，如果你用的不是lilo来引导系统，可以把最后两行去掉，配置自己的引导程序来引导内核。

顺便补充一点，&&命令表示顺序执行由它连接的命令，但是只有它之前的命令成功执行完成了之后才可以继续执行它后面的命令。

### 点斜杠(./)

点斜杠执行脚本是启动了另一个Shell去执行脚本 (另一个进程），所以点斜杠执行脚本时，设置的环境变量会随着进程的退出而结束，其中的环境变量设置对当前Shell不起作用。

### 点空格点斜杠(. ./)

点空格点斜杠执行脚本，是相当于source ./执行脚本，source是执行脚本当中的命令，也就是说在当前进程中执行命令，所以其中的环境变量的设置会对当前Shell其作用。

### 三种shell脚本调用方法 (fork, exec, source)

原文: <http://mindream.wang.blog.163.com/blog/static/2325122220084624318692/>

fork(/path/to/script.sh)
fork是最普通的, 就是直接在脚本里面用 /directory/script.sh 来调用script.sh这个脚本。

运行的时候开一个sub-shell执行调用的脚本，sub-shell执行的时候, parent-shell还在。

sub-shell执行完毕后返回parent-shell。sub-shell从parent-shell继承环境变量，但是sub-shell中的环境变量不会带回parent-shell。

exec (exec /path/to/script.sh)
exec与fork不同，不需要新开一个sub-shell来执行被调用的脚本。被调用的脚本与父脚本在同一个shell内执行。但是使用exec调用一个新脚本以后, 父脚本中exec行之后的内容就不会再执行了。这是exec和source的区别。

可以通过下面这两个脚本来体会三种调用方式的不同:

```bash
# !/bin/bash
A=B
echo "PID for 1.sh before exec/source/fork:$$"
export A
echo "1.sh: $A is $A"
case in
    exec)
        echo "using exec…"
        exec ./2.sh ;;
    source)
        echo "using source…"
        . ./2.sh ;;
    *)
        echo "using fork by default…"
        ./2.sh ;;
esac
echo "PID for 1.sh after exec/source/fork:$$"
echo "1.sh: $A is $A"
```

```bash
# !/bin/bash
echo "PID for 2.sh: $$"
echo "2.sh get $A=$A from 1.sh"
A=C
export A
echo "2.sh: $A is $A"
```

><https://blog.csdn.net/zdh9378/article/details/39586783>
