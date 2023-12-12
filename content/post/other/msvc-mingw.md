---
title: MSVC, MinGW, GNU
author: "-"
date: 2012-09-15T15:14:37+00:00
url: msvc/mingw/gnu
categories:
  - Inbox
tags:
  - reprint
  - remix
---
## MSVC, MinGW, GNU
  
Qt 中有两种方式编译，一种是MinGW ，另一种MSVC。

MSVC 是指微软的VC编译器。
MinGW 是指是Minimalist GNU on Windows的缩写。它是一个可自由使用和自由发布的Windows特定头文件和使用GNU工具集导入库的集合，允许你在GNU/Linux和Windows平台生成本地的Windows程序而不需要第三方C运行时库。
它们都是很好用的编译工具，但是它们兼容的并不好。当你的项目使用MinGW编译的使用，想要用一个MSVC编译生成的库时就会有问题。使用MinGW编译项目的时候，所使用的Lib也要是MinGW编译的。如果你只是开发Window平台的软件时，最好用Qt MSVC组合，这样可以使用大量的第三方lib，还有很多的构建指令，毕竟window上MSVC才是王道。
————————————————
版权声明：本文为CSDN博主「自先沉稳~」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/error_again/article/details/109765184

### GNU VS. MSVC

`winget search rust`

`Rust (MSVC)`
`Rusr (GNU)`

The GNU toolchain uses the MinGW build tools (mostly the linker) and produces binaries that use the GNU ABI. The MSVC toolchain uses the Visual Studio build tools and produces binaries that use the Microsoft ABI, making them more compatible with most other Windows binaries/libraries.

https://www.reddit.com/r/rust/comments/a63dlt/difference_between_the_gnu_and_msvc_toolchains/
