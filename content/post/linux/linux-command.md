---
title: shell command basic
author: "-"
date: 2011-04-23T08:54:55+00:00
url: shell/commaand
categories:
  - shell
tags:
  - reprint
---
## shell command basic

### ascii to binary

```bash
$ echo -n "A" | xxd -b
0000000: 01000001                                               A

$ echo -n "A" | xxd -b | awk '{print $2}'
01000001
```

[https://unix.stackexchange.com/questions/98948/ascii-to-binary-and-binary-to-ascii-conversion-tools](https://unix.stackexchange.com/questions/98948/ascii-to-binary-and-binary-to-ascii-conversion-tools)

### base64 > hex

```bash
echo "YWJj" |base64 -d|xxd
```

### Display the last users who have logged onto the system

```bash
last
```

### Display the user and group ids of your current user

```bash
id
```

### Display who is online

```bash
w
```

### Show who is logged into the system

```bash
    who
```

### Show this month's calendar

```bash
    cal
```

### printf

```bash
    export LC_NUMERIC="en_US.UTF-8"
    printf "%'f\n" 1234567.777
```

> 1,234,567.777000

#### 语言环境会影响千分位符的显示

```bash
    export LC_NUMERIC=C
    printf "%'f\n" 1234567.777
```

> 1234567.777000

#### 不保留小数

```bash
    printf("%3.0f",floatNum)
```

说明: %3.0f表明待打印的浮点数 (floatNum) 至少占3个字符宽，且不带小数点和小数部分，整数部分至少占3个位宽；

注意: 这里的3只代表整数部分至少占3位，舍弃小数点和小数点后面的部分

### file

识别文件类型，也可用来辨别一些文件的编码格式。它是通过查看文件的头部信息来获取文件类型，而不是像Windows通过扩展名来确定文件类型的
file 命令用于分析文件的类型。

如果你需要分析二进制文件，可以首先使用 file 命令来切入。我们知道，在 Linux 下，一切皆文件，但并不是所有的文件都具有可执行性，我们还有各种各样的文件，比如: 文本文件，管道文件，链接文件，socket文件，等等。

在对一个文件进行分析之前，我们可以首先使用 file 命令来分析它们的类型。当然除此之外，我们还可以看到一些其它信息。

```bash
    file /bin/pwd
```

>/bin/pwd: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=0d264bacf2adc568f0e21cbcc9576df434c44380, stripped

### ltrace

ltrace的功能是能够跟踪进程的库函数调用。

我们可以使用 ldd 命令来找到程序的依赖库，但是，一个库里少则几个，多则几千个函数，怎么知道现在程序调用的是什么函数呢？

ltrace 命令就是用来做这个事的。在下面的例子里，我们可以看到程序调用的函数，以及传递进去的参数，同时你也可以看到函数调用的输出。

```bash
    ltrace /bin/pwd
```

### strace

strace 命令可以用于追踪程序运行过程中的系统调用及信号。

通过上面的介绍，我们知道 ltrace 命令是用来追踪函数调用的。strace 命令类似，但它追踪的是系统调用。何为系统调用？简单说就是我们可以通过系统调用与内核进行交互，完成我们想要的任务。

例如，如果我们想在屏幕上打印某些字符，可以使用 printf 或 puts 函数，而这两个都是 libc 的库函数，在更底层，他们都是调用 write 这个系统调用。

```bash
    strace -f /bin/pwd
```

### hexdump

hexdump 命令用来查看二进制文件的 16 进制编码，但实际它能查看任何文件，而不限于二进制文件。

一个二进制文件，如果你直接使用文本编辑器打开的话，将看到一堆乱码。这时候，你就可以使用 hexdump 命令来查看它的内容了。

hexdump 的显示格式是: 左边是字节序号，中间是文件的 16 进制编码，如果是可打印字符的话就会显示在右边。

通过使用这个命令，我们就可以大概知道这个二进制文件里面有什么内容，后面要做什么处理就比较方便了。

hexdump -C /bin/pwd | head

### strings

strings 命令可以用来打印二进制文件中可显示的字符。

什么是可显示字符？简单说你在显示器上看到的字符都是可显示字符，比如: abcABC,.:。

我们知道，一个二进制文件里面的内容很多是非显示字符，所以无法直接用文本处理器打开。程序在被开发的时候，我们经常会加一些调试信息，比如: debug log, warn log, error log，等等。这些信息我们就可以使用 strings 命令看得到。

strings /bin/pwd | head

### objdump

objdump是用查看目标文件或者可执行的目标文件的构成的GCC工具。

我们知道，程序在开发完成之后，需要经过编译，才可以生成计算机可以识别的二进制文件。我们写的代码计算机不能直接执行，需要编译成汇编程序，计算机才能依次执行。

objdump 命令可以读取可执行文件，然后将汇编指令打印出来。所以如果你想看懂 objdump 的结果，你就需要有一些汇编基础才可以。

```bash
    objdump -d /bin/pwd | head
    objdump -dS hello.o
```

### gdb

gdb 就是所谓的 GNU debugger。

gdb 大家或多或少都有听说过。我们在使用一些 IDE 写代码的时候，可以进行打断点、步进、查看变量值等方式调试，其实这些 IDE 底层调用的也是 gdb 。

对于 gdb 的用法，可以写很多，本文就暂且不深入了。下面先演示一小段 gdb 最基础的功能。

```bash
gdb -q ./hello
```

### 查看pci设备

```bash
    lspci -k
```

### 磁盘清理

```bash
    sudo pacman -Scc
    sudo yay -Scc
```

scrot

pacman -S scrot

* 抓取区域:

scrot -s rectangle.png
[https://wiki.archlinux.org/index.php/Taking_a_screenshot_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87](https://wiki.archlinux.org/index.php/Taking_a_screenshot_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))

### delete folder

```bash
    rm -rf \***
```

### cp

```bash
    cp -r 按递归方式保留原目录结构复制文件
```

```bash
# 替换字符串
foo=foo-bar
bar=${foo/-/_}
echo $bar

#执行多个命令
ls && ls -l
sudo mount -t ntfs-3g /dev/sdc10 mnt1
ls -lt
ls -lrt
chown [-R] 账号名称: 用户组名称 文件或目录

yum install lrzsz

lsblk

ls -l /dev/disk/by-uuid/
```

## 查看挂载的USB设备

```bash
pacman -S usbutils
lsusb
```

rmdir : delete folder
  
rm -rf
  
-r, -R, -recursive
  
remove directories and their contents recursively
  
-f, -force
  
ignore nonexistent files, never prompt
  
ps
  
ps -ef
  
-a 显示现行终端机下的所有程序，包括其他用户的程序。
  
-A 显示所有程序。
  
-e 此参数的效果和指定"A"参数相同。
  
-f 用ASCII字符显示树状结构，表达程序间的相互关系。

md5sum : compute and check MD5 message digest

### 统计某文件夹下文件的个数

```bash
    ls -l |grep "^-"|wc -l
```

### 统计某文件夹下目录的个数

```bash
    ls -l |grep "^ｄ"|wc -l
```

### 统计文件夹下文件的个数，包括子文件夹里的

### ls -lR|grep "^-"|wc -l

### 统计文件夹下目录的个数，包括子文件夹里的

### ls -lR|grep "^d"|wc -l

说明:

### ls -l

### 长列表输出该目录下文件信息(注意这里的文件，不同于一般的文件，可能是目录、链接、设备文件等)

### grep "^-"

### 这里将长列表输出信息过滤一部分，只保留一般文件，如果只保留目录就是 ^d

### 一行信息对应一个文件，所以也就是文件的个数

### chrt

chrt命令 – 更改调度策略
chrt是用来操纵进程的实时属性，所有优先级值在0-99范围内的，都是实时进程，所以这个优先级范围也可以叫做实时进程优先级，而100-139范围内的是非实时进程。在系统中可以使用chrt命令来查看、设置一个进程的实时优先级状态。

语法格式: chrt [参数]

常用参数:

-m/--max    显示最小和最大有效优先级
-p/--pid    对现有的给定pid进行操作

-h/--help    显示此帮助
-V/--version    显示版本

---

[http://blog.chinaunix.net/uid-20355427-id-1700516.html](http://blog.chinaunix.net/uid-20355427-id-1700516.html)

[http://blog.csdn.net/zhouleiblog/article/details/9325913](http://blog.csdn.net/zhouleiblog/article/details/9325913)  
[https://www.linuxcool.com/chrt](https://www.linuxcool.com/chrt)  
