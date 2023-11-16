---
title: GCC
author: "-"
date: 2012-02-26T03:13:40+00:00
url: GCC
categories:
  - Linux
tags:
  - reprint
---
## GCC

GCC (GNU Compiler Collection ) ，GCC是一系列编译器的集合, 是Linux操作系统的核心组件之一。是一套由 GNU 开发的编程语言编译器。它是一套GNU编译器套装以 GPL 及 LGPL 许可证所发行的自由软件，也是 GNU计划的关键部分，亦是自由的类Unix及苹果电脑 Mac OS X 操作系统的标准编译器。GCC 原名为 GNU C 语言编译器，因为它原本只能处理 C语言。GCC 很快地扩展，变得可处理 C++。之后也变得可处理 Fortran、Pascal、Objective-C、Java, 以及 Ada与其他语言。

GCC最初名为GNU C Compiler，当时它只是一款C语言的编译器，不过随着后续迭代，它支持C++、Fortran、Go等语言，GCC也因此成为一个编译器集合。GCC有以下特点：

GCC支持的编程语言多。比如，g++ 是 C++ 编译器，gfortran是 Fortran 编译器。
GCC支持的硬件全。GCC可以将源代码编译成x86_64、ARM、PowerPC等硬件架构平台的可执行文件。
GCC支持众多业界标准。GCC能很快支持最新的C++标准，GCC支持OpenMP、OpenACC。

虽然编译器并非只有GCC一种，macOS上有Clang，Windows上有MSVC，但GCC的这些特点让它从众多编译器间脱颖而出，很多开源软件会选择GCC完成编译工作。

刚才提到，软件构建的过程比较复杂，GCC的一些“兄弟”工具提供了很多支持功能：

GNU Make：一款自动化编译和构建工具，多文件、多模块的大型软件工程经常需要使用GNU Make。
GDB：GNU Debugger，用于调试。
GNU Binutils：一组二进制工具集，包括链接器ld、汇编器as等，GNU Bintuils可以和GCC、GNU Make一起完成构建过程。我们将在下文使用这些工具。
综上，GCC在Linux操作系统占有举足轻重的地位。

### 预处理

使用预处理器cpp工具进行预处理。注意，这里的cpp是C Preprocessor的缩写，并不是C-plus-plus的意思。

cpp hello.c -o hello.i

预编译主要处理源代码中以#开始的预编译指令，主要处理规则如下：

处理#include 预编译指令，将被包含的文件插入到该预编译指令的位置。这是一个递归的过程，如果被包含的文件还包含了其他文件，会递归地完成这个过程。
处理条件预编译指令，比如#if、#ifdef、#elif、#else、#endif。
删除#define，展开所有宏定义。
添加行号和文件名标识，以便于在编译过程中产生编译错误或者调试时都能够生成行号信息。

编译
编译的过程主要是进行词法分析、语法分析、语义分析，这背后涉及编译原理等一些内容。这里只进行编译，不汇编，可以生成硬件平台相关的汇编语言。

$ gcc -S hello.i -o hello.s
gcc其实已经做了封装，背后是使用一个名为cc1的工具，cc1并没有放在默认的路径里。Ubuntu 16.04系统上，cc1位于：/usr/lib/gcc/x86_64-linux-gnu/5.4.0/cc1：

$ /usr/lib/gcc/x86_64-linux-gnu/5.4.0/cc1 hello.i -o hello.s

汇编
得到汇编代码后，离二进制可执行文件仅有一步之遥，我们可以用as工具将汇编语言翻译成二进制机器码：

$ as hello.s -o hello.o

虽然这个文件已经是二进制的机器码了，但是它仍然不能执行，因为它缺少系统运行所必须的库，比如C语言printf()对应的汇编语言的puts函数。确切的说，系统还不知道puts函数在内存中的具体位置。如果我们在一份源代码中使用了外部的函数或者变量，还需要重要的一步：链接。

链接
很多人不太了解链接，但这一步却是C/C++开发中经常使用的部分。

下面的命令进行链接，生成名为hello的可执行文件：

$ gcc hello.o -o hello
上面的命令基于动态链接的方式，生成的hello已经是一个可执行文件。实际上，这个命令隐藏了很多背后的内容。printf()方法属于libc库，上面的命令并没有体现出来如何将hello.o团队和libc库链接的过程。为了体现链接，我们使用链接器ld，将多个模块链接起来，生成名为myhello的可执行文件：

$ ld -o myhello hello.o /usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o /usr/lib/x86_64-linux-gnu/crtn.o -lc -dynamic-linker /lib64/ld-linux-x86_64.so.2

我们终于将一份源代码编译成了可执行文件！这个命令有点长，涉及到文件和路径也有点多，它将多个文件和库链接到myhello中。crt1.o、crti.o和crtn.o是C运行时所依赖的环境。如果提示crt1.o这几个文件找不到，可以使用find命令来查找：

$ find /usr/lib -name 'crt1.o'

### Hello World背后的故事：如何在Linux上编译C语言程序

[https://lulaoshi.info/blog/compile-c-hello-world-on-linux](https://lulaoshi.info/blog/compile-c-hello-world-on-linux)  

### 查询gcc能否搜寻到指定的库文件

    gcc -lhdf5 --verbose
