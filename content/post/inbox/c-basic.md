---
title:  c basic, c, c lang, c 语言
author: "-"
date: 2016-11-16T07:09:09+00:00
url: /?p=9397
categories:
  - inbox
tags:
  - reprint
---
## c basic, c, c lang, c 语言

## hello world

vim  main.c

```c
#include <stdio.h>
int main(){
  printf("hello world!\n");
  return 0;
}
```

```bash
gcc main.c
./a.out

# 也可以不使用a.out这个名字，我们自己对其进行命名：
gcc main.c -o hello
./hello
```

### 预处理(或称预编译)

预处理(或称预编译)是指在进行编译的第一遍扫描(词法扫描和语法分析)之前所作的工作。预处理指令指示在程序正式编译前就由编译器进行的操作,可放在程序中任何位置。

预处理是C语言的一个重要功能,它由预处理程序负责完成。当对一个源文件进行编译时,系统将自动引用预处理程序对源程序中的预处理部分作处理,处理完毕自动进入对源程序的编译。

C语言提供多种预处理功能,主要处理#开始的预编译指令,如宏定义(#define)、文件包含(#include)、条件编译(#ifdef)等。合理使用预处理功能编写的程序便于阅读、修改、移植和调试,也有利于模块化程序设计。

### 头文件, header

头文件是扩展名为 .h 的文件,包含了 C 函数声明和宏定义,被多个源文件中引用共享。有两种类型的头文件: 程序员编写的头文件和编译器自带的头文件。

在程序中要使用头文件,需要使用 C 预处理指令 #include 来引用它。前面我们已经看过 stdio.h 头文件,它是编译器自带的头文件。

引用头文件相当于复制头文件的内容,但是我们不会直接在源文件中复制头文件的内容,因为这么做很容易出错,特别在程序是由多个源文件组成的时候。

A simple practice in C 或 C++ 程序中,建议把所有的常量、宏、系统全局变量和函数原型写在头文件中,在需要的时候随时引用这些头文件。
引用头文件的语法
使用预处理指令 #include 可以引用用户和系统头文件。它的形式有以下两种:

# include <file>
这种形式用于引用系统头文件。它在系统的标准列表中搜索名为 file 的文件。在编译源代码时,您可以通过 -I 选项把目录前置在该列表前。

# include "file"

#### #include

# include 命令是预处理命令的一种,预处理命令可以将别的源代码内容插入到所指定的位置；可以标识出只有在特定条件下才会被编译的某一段程序代码；可以定义类似标识符功能的宏,在编译时, 预处理器会用别的文本取代该宏。
预处理器如何找到头文件
由给定的 C 语言实现版本决定 #include 命令所指定文件的搜索路径。同时,也由实现版本决定文件名是否区分大小写。对于命令中使用尖括号指定的文件 (<文件名>) , 预处理器通常会在特定的系统路径下搜索, 例如, 在 Unix 系统中, 会搜索路径 `/usr/include`, `/usr/local/include`
对于命令中用双引号指定的文件 ("文件名") , 预处理器通常首先在当前目录下寻找,也就是包含该程序其他源文件的目录。如果在当前目录下没有找到,那么预处理器也会搜索系统的 include 路径。 文件名中可以包含路径。 但如果文件名中包含了路径,则预处理器只会到该目录下寻找。

你也可以通过使用编译器命令行选项, 或在环境变量 (该变量通常称为 INCLUDE) 中加入搜索路径,为 #include 命令指定自己的搜索路径。 具体的做法请参考采用的编译器的说明文档。

C中可以通过 `#include <stdio.h >` 和 `#include "stidio.h"`, 区别是:

##### #include <stdio.h>

搜索路径: `/usr/include`, `/usr/local/include`

# include <stdio.h>, 直接到系统指定目录去查找头文件。
# include "stidio.h", 会先到当前目录查找头文件,如果没找到在到系统指定目录查找。
gcc编译时查找头文件, 按照以下路径顺序查找:

1. gcc 编译时,可以设置 -I 选项以指定头文件的搜索路径,如果指定多个路径,则按照顺序依次查找。比如,

    gcc -I /usr/local/include/node a.c

2. gcc会查找环境变量 C_INCLUDE_PATH,CPLUS_INCLUDE_PATH中指定的路径。

3. 系统默认的路径,分别是/usr/include,/usr/local/include,/usr/lib/gcc-lib/i386-linux/2.95.2/include (gcc库文件的路径,各个系统不一致) 。

同时,include也可以采用相对路径,比如,a.c需要包含/usr/local/include/node/v8.h,由于/usr/local/include是系统的默认搜索路径,所以在a.c中可以用相对路径包含,#include<node/v8.h>。

### c90,c99,c11

C90 标准
由于C语言被各大公司所使用 (包括当时处于鼎盛时期的 IBM PC) ,因此到了 1989 年,C语言由美国国家标准协会 (ANSI) 进行了标准化,此时C语言又被称为 ANSI C。

而仅过一年,ANSI C 就被国际标准化组织 ISO 给采纳了。此时,C语言在 ISO 中有了一个官方名称——ISO/IEC 9899: 1990。其中:
9899 是C语言在 ISO 标准中的代号,像 C++ 在 ISO 标准中的代号是 14882；
而冒号后面的 1990 表示当前修订好的版本是在 1990 年发布的。

对 于ISO/IEC 9899: 1990 的俗称或简称,有些地方称为 C89,有些地方称为 C90,或者 C89/90。不管怎么称呼,它们都指代这个最初的C语言国际标准。

这个版本的C语言标准作为 K&R C 的一个超集 (即 K&R C 是此标准C的一个子集) ,把后来引入的许多非官方特性也一起整合了进去。其中包括了从 C++ 借鉴的函数原型 (Function Prototypes) ,指向 void 的指针,对国际字符集以及本地语言环境的支持。在此标准中,尽管已经将函数定义的方式改为现在我们常用的那种方式,不过K&R的语法形式仍然兼容。
C99标准
在随后的几年里,C语言的标准化委员会又不断地对C语言进行改进,到了 1999 年,正式发布了 ISO/IEC 9899: 1999,简称为 C99 标准。

C99 标准引入了许多特性,包括内联函数 (inline functions) 、可变长度的数组、灵活的数组成员 (用于结构体) 、复合字面量、指定成员的初始化器、对IEEE754浮点数的改进、支持不定参数个数的宏定义,在数据类型上还增加了 long long int 以及复数类型。

毫不夸张地说,即便到目前为止,很少有C语言编译器是完整支持 C99 的。像主流的 GCC 以及 Clang 编译器都能支持高达90%以上,而微软的 Visual Studio 2015 中的C编译器只能支持到 70% 左右。
C11标准
2007 年,C语言标准委员会又重新开始修订C语言,到了 2011 年正式发布了 ISO/IEC 9899: 2011,简称为 C11 标准。

C11标准新引入的特征尽管没 C99 相对 C90 引入的那么多,但是这些也都十分有用,比如: 字节对齐说明符、泛型机制 (generic selection) 、对多线程的支持、静态断言、原子操作以及对 Unicode 的支持。

### pkg-config

pkg-config在编译应用程序和库的时候作为一个工具来使用。例如你在命令行通过如下命令编译程序时:

# gcc -o test test.c `pkg-config --libs --cflags glib-2.0`

pkg-config可以帮助你插入正确的编译选项,而不需要你通过硬编码的方式来找到glib(或其他库) 。

--cflags一般用于指定头文件,--libs一般用于指定库文件。

大家应该都知道一般用第三方库的时候,就少不了要使用到第三方的头文件和库文件。我们在编译、链接的时候,必须要指定这些头文件和库文件的位置。对于一个比较大的第三方库,其头文件和库文件的数量是比较多的,如果我们一个个手动地写,那将是相当的麻烦的。因此,pkg-config就应运而生了。pkg-config能够把这些头文件和库文件的位置指出来,给编译器使用。pkg-config主要提供了下面几个功能:

检查库的版本号。 如果所需要的库的版本不满足要求,它会打印出错误信息,避免链接错误版本的库文件
获得编译预处理参数,如宏定义、头文件的位置
获得链接参数,如库及依赖的其他库的位置,文件名及其他一些链接参数
自动加入所依赖的其他库的设置

#### 查看当前安装了哪些库(so)

    pkg-config --list-all

PKG_CONFIG_PATH是一个环境变量,它指定pkg-config将在其中搜索其.pc文件的其他路径。

此变量用于增强pkg-config的默认搜索路径。在典型的Unix系统上,它将搜索目录/usr/lib/pkgconfig和/usr/share/pkgconfig。这通常包括系统安装的模块。但是,某些本地模块可能安装在不同的前缀中,例如/usr/local。在这种情况下,必须预先设置搜索路径,以便pkg-config可以找到.pc文件。

pkg-config程序用于检索有关系统中已安装库的信息。 pkg-config的主要用途是提供编译程序和链接到库的必要细节。此元数据存储在pkg-config文件中。这些文件具有后缀.pc,并位于pkg-config工具已知的特定位置。

要检查PKG_CONFIG_PATH值,请使用以下命令:

echo $PKG_CONFIG_PATH

### sleep

头文件: #include <unistd.h>

定义函数: unsigned int sleep(unsigned int seconds);

函数说明: sleep()会令目前的进程暂停, 直到达到参数seconds 所指定的时间, 或是被信号所中断.

返回值: 若进程暂停到参数seconds 所指定的时间则返回0, 若有信号中断则返回剩余秒数.

### stdio.h

stdio 就是指 "standard input & output" (标准输入输出)

### unistd.h

符号常量

是POSIX标准定义的unix类系统定义符号常量的头文件,包含了许多UNIX系统服务的函数原型,例如read函数、write函数和getpid函数

unistd.h在unix中类似于window中的windows.h!

### 下划线

C语言中双下划线__的作用
以单下划线 (_) 表明是标准库的变量

双下划线 (__)  开头表明是编译器的变量

所以 双下划线 __ 只是C语言的一个合法标识符
不一定是变量, 也可以是函数,宏等。

同时双下划线 (__) 多用于告警提示:

FILE 包含当前程序文件名的字符串
LINE 表示当前行号的整数
DATE 包含当前日期的字符串
STDC 如果编译器遵循ANSI C标准,它就是个非零值
TIME 包含当前时间的字符串

## build

将源代码文件最终转化为可执行文件的过程，被称为构建 (Build）。

编译一般分为四步：预处理 (Preprocess）、编译 (Compile）、汇编 (Assembly）和链接 (Link）。
,

<https://wangdoc.com/clang/>  
<https://github.com/wangdoc/clang-tutorial>  
<http://world77.blog.51cto.com/414605/328263>
<https://www.cnblogs.com/clover-toeic/p/3851102.html>  
<http://c.biancheng.net/view/443.html>  
<https://blog.csdn.net/chosen0ne/article/details/7210946>  
<https://ubuntuqa.com/article/1513.html>  
<http://c.biancheng.net/cpp/html/345.html>  
