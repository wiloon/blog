---
title: Meson
author: "-"
date: 2014-05-26T09:16:52+00:00
url: Meson
categories:
  - Uncategorized
tags:
  - Java

---
## Meson

一、什么是Meson
Meson（The Meson Build System）是个项目构建系统，如Makefile，automake，CMake...。Meson是一个Python实现的开源项目，其思想是，开发人员花费在构建调试上的每一秒都是浪费，同样等待构建过程直到真正开始编译都是不值得的。

因此，Meson的设计目的是在用户友好的同时不损害性能，Meson提供客户语言（custom language）作为主要工具，用户可以使用它完成项目构建的描述。客户语言的设计目标是简单（simplicity）、清晰（clarity）、简洁（conciseness），其中很多灵感来源于Python语言。

Meson的另个一主要设计目的是为现代编程工具提供优秀的支持和最好的实现。这包括一些特性如：单元测试（unit testing）、代码覆盖率报告（code coverage reporting）、头文件预编译（precompiled headers）。用户不需要寻找三方宏指令（third party macros）或编写shell脚本来实现这些特性，Meson只要开箱即用（work out of the box）。

二、Meson有什么特点
对Linux，macOS，Windows，GCC，Clang，Visual Studio等提供多平台支持
支持的语言包括C，C ++，D，Fortran，Java，Rust
在非常易读且用户友好的非图灵完整DSL中构建定义
适用于许多操作系统和裸机的交叉编译
针对极快的完整和增量构建进行了优化，而不会牺牲正确性
内置的多平台依赖提供程序，可与发行版软件包一起使用
好玩！
————————————————
版权声明：本文为CSDN博主「espresso_yu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u010074726/article/details/108695256