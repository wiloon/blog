---
title: objdump
author: "-"
date: 2016-03-04T04:53:20+00:00
url: objdump
categories:
  - Linux
tags:
  - reprint
---
## objdump

objdump 命令是 Linux 下的反汇编目标文件或者可执行文件的命令，它以一种可阅读的格式让你更多地了解二进制文件可能带有的附加信息。

objdump 是 gcc 工具，用来查看编译后目标文件的组成。

功能: 以一种可阅读的格式让你更多地了解目标文件、可执行文件可能带有的附加信息，也能完成目标文件或者可执行文件的反汇编。

示例: 

使用 objdump 查看可执行文件的汇编代码

```Bash
go build -gcflags "-N -l" test.go
objdump -S --disassemble test > test.objdump
```

查看动态库有哪些符号，包括数据段、导出的函数和引用其他库的函数

```Bash
objdump -tT xxx.so
objdump -x xxx.a
```

查看动态库依赖项

```Bash
objdump -x xxx.so | grep "NEEDED"
```

查看动态符号表

```Bash
objdump -T xxx.so
```

假如想知道 xxx.so 中是否导出了符号 yyy ，那么命令为 objdump -T xxx.so | grep "yyy" 。

查看动态符号表

```Bash
objdump -t xxx.so
```

-T 和 -t 选项在于 -T 只能查看动态符号，如库导出的函数和引用其他库的函数，而 -t 可以查看所有的符号，包括数据段的符号。

版权声明：本文为CSDN博主「mayue_csdn」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/mayue_web/article/details/103879976](https://blog.csdn.net/mayue_web/article/details/103879976)
