---
author: "-"
date: "2021-01-06 22:40:46" 
title: "gdb"
categories:
  - inbox
tags:
  - reprint
---
## "gdb"

GDB是什么
GDB 全称"GNU symbolic debugger"，从名称上不难看出，它诞生于 GNU 计划 (同时诞生的还有 GCC、Emacs 等) ，是 Linux 下常用的程序调试器。发展至今，GDB 已经迭代了诸多个版本，当下的 GDB 支持调试多种编程语言编写的程序，包括 C、C++、Go、Objective-C、OpenCL、Ada 等。实际场景中，GDB 更常用来调试 C 和 C++ 程序。
Windows 操作系统中，人们更习惯使用一些已经集成好的开发环境 (IDE) ，如 VS、VC、Dev-C++ 等，它们的内部已经嵌套了相应的调试器。

GDB的吉祥物: 弓箭鱼
图 1 GDB 的吉祥物: 弓箭鱼

总的来说，借助 GDB 调试器可以实现以下几个功能: 
程序启动时，可以按照我们自定义的要求运行程序，例如设置参数和环境变量；
可使被调试程序在指定代码处暂停运行，并查看当前程序的运行状态 (例如当前变量的值，函数的执行结果等) ，即支持断点调试；
程序执行过程中，可以改变某个变量的值，还可以改变代码的执行顺序，从而尝试修改程序中出现的逻辑错误。


GDB (GNU Debugger) 是UNIX及UNIX-like下的强大调试工具，可以调试ada, c, c++, asm, minimal, d, fortran, objective-c, go, java,pascal等语言。

对于C程序来说，需要在编译时加上-g参数，保留调试信息，否则不能使用GDB进行调试。
但如果不是自己编译的程序，并不知道是否带有-g参数，如何判断一个文件是否带有调试信息呢？

gdb 文件
例如: 

$ gdb helloworld
Reading symbols from helloWorld...(no debugging symbols found)...done.
如果没有调试信息，会提示no debugging symbols found。
如果是下面的提示: 

Reading symbols from helloWorld...done.
则可以进行调试。

readelf查看段信息
例如: 

```bash
readelf -S helloWorld|grep debug
```
```
[28] .debug_aranges    PROGBITS         0000000000000000  0000106d
[29] .debug_info       PROGBITS         0000000000000000  0000109d
[30] .debug_abbrev     PROGBITS         0000000000000000  0000115b
[31] .debug_line       PROGBITS         0000000000000000  000011b9
[32] .debug_str        PROGBITS         0000000000000000  000011fc
```


  file查看strip状况
下面的情况也是不可调试的: 

$ file helloWorld
helloWorld: (省略前面内容) stripped
如果最后是stripped，则说明该文件的符号表信息和调试信息已被去除，不能使用gdb调试。但是not stripped的情况并不能说明能够被调试。



