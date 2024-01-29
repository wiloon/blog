---
title: linux nm
author: "-"
date: 2019-04-05T14:10:50+00:00
url: /?p=14104
categories:
  - Inbox
tags:
  - reprint
---
## linux nm

nm 目标文件格式分析
  
nm 命令显示关于指定 File 中符号的信息，文件可以是对象文件、可执行文件或对象文件库。如果文件没有包含符号信息，nm 命令报告该情况，但不把它解释为出错条件。 nm 命令缺省情况下报告十进制符号表示法下的数字值。

### nm

nm命令主要是列出目标文件的符号 (说白了就是一些函数和全局变量等) 。

如果你编译出来的程序没有经过 strip ，那么 nm 命令可以挖掘出隐含在可执行文件中的重大秘密。它可以帮你列出文件中的变量及函数，这对于我们进行反向操作具有重大意义。

下面我们通过一小段简单的程序来讲解 nm 命令的用途。在编译这个程序时，我们加上了 -g 选项，这个选项可以使编译出来的文件包含更多有效信息。

   nm /path/to/foo

nm命令
功能：列出.o、.a、.so中的符号信息，包括符号的值，符号类型及符号名称等。所谓符号，通常指定义出的函数，全局变量等

[https://blog.csdn.net/mayue_web/article/details/115919693](https://blog.csdn.net/mayue_web/article/details/115919693)

使用：

nm [option(s)] [file(s)]
1
示例：

# 查看静态库或动态库定义了哪些函数

nm -n --defined-only xxxx.a
nm -g -C --defined-only xxxx.so
nm -D xxxx.so

# 显示hello.a 中的未定义符号，需要和其他对象文件进行链接

nm -u hello.o

# 在 ./ 目录下找出哪个库文件定义了close_socket函数

nm -A ./* 2>/dev/null | grep "T close_socket"
————————————————
版权声明：本文为CSDN博主「mayue_csdn」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/mayue_web/article/details/103879976](https://blog.csdn.net/mayue_web/article/details/103879976)

[https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/nm.html](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/nm.html)
