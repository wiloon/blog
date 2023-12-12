---
title: gdb
author: "-"
date: "2006-01-02 15:04:05"
url: gdb
categories:
  - Development
tags:
  - Reprint
---
## gdb

GDB是Linux下非常好用且强大的调试工具。GDB可以调试C、C++、Go、java、 objective-c、PHP等语言。对于一名Linux下工作的c/c++程序员，GDB是必不可少的工具

```Bash
readelf -S main|grep debug
```

```Bash
# 查看寄存器的值
i registers
# 以上输出不包括浮点寄存器和向量寄存器的内容。使用“i all-registers”命令，可以输出所有寄存器的内容
i all-registers
# 打印单个寄存器的值，可以使用“i registers regname”或者“p $regname”，例如：
i registers rsi
```

```Bash
# 用 gdb 调试 hello
gdb ./hello
# 在 _start 函数处添加一个断点
(gdb) b _start
# run
(gdb) r
# 显示汇编代码, => 表示下一步要执行的行
(gdb) disassemble /m _start
# 逐指令往后运行
(gdb) stepi
# 查看寄存器的值
(gdb) i registers
```