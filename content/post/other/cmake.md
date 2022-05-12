---
title: CMake
author: "-"
date: 2013-02-24T03:15:38+00:00
url: /?p=5241
categories:
  - Linux
tags:$
  - reprint
---
## CMake

### build

先创建一个叫build的文件夹 (这个并非必须，因为cmake命令指向CMakeLists.txt所在的目录，例如cmake .. 表示CMakeLists.txt在当前目录的上一级目录。cmake后会生成很多编译的中间文件以及makefile文件，所以一般建议新建一个新的目录，专门用来编译) ，然后执行下列操作: 

    mkdir build
    cd build 
    cmake .. 
    make 

你或许听过好几种 Make 工具，例如 GNU Make ，QT 的 qmake ，微软的 MS nmake，BSD Make (pmake) ，Makepp，等等。这些 Make 工具遵循着不同的规范和标准，所执行的 Makefile 格式也千差万别。这样就带来了一个严峻的问题: 如果软件想跨平台，必须要保证能够在不同平台编译。而如果使用上面的 Make 工具，就得为每一种标准写一次 Makefile ，这将是一件让人抓狂的工作。

CMake 就是针对上面问题所设计的工具: 它首先允许开发者编写一种平台无关的 CMakeList.txt 文件来定制整个编译流程，然后再根据目标用户的平台进一步生成所需的本地化 Makefile 和工程文件，如 Unix 的 Makefile 或 Windows 的 Visual Studio 工程。从而做到"Write once, run everywhere"。显然，CMake 是一个比上述几种 make 更高级的编译配置工具。一些使用 CMake 作为项目架构系统的知名开源项目有 VTK、ITK、KDE、OpenCV、OSG 等 [1]。

---

CMake是一个跨平台的安装(编译)工具,可以用简单的语句来描述所有平台的安装(编译过程)。他能够输出各种各样的makefile或者project文件,能测试编译器所支持的C++特性,类似UNIX下的automake。只是 CMake 的组态档取名为 CmakeLists.txt。Cmake 并不直接建构出最终的软件，而是产生标准的建构档 (如 Unix 的 Makefile 或 Windows Visual C++ 的 projects/workspaces) ，然后再依一般的建构方式使用。这使得熟悉某个集成开发环境 (IDE) 的开发者可以用标准的方式建构他的软件，这种可以使用各平台的原生建构系统的能力是 CMake 和 SCons 等其他类似系统的区别之处。


CMake 可以编译源代码、制作程式库、产生适配器 (wrapper) 、还可以用任意的顺序建构执行档。CMake 支援 in-place 建构 (二进档和源代码在同一个目录树中) 和 out-of-place 建构 (二进档在别的目录里) ，因此可以很容易从同一个源代码目录树中建构出多个二进档。CMake 也支持静态与动态程式库的建构。


"CMake"这个名字是"cross platform make"的缩写。虽然名字中含有"make"，但是CMake和Unix上常见的"make"系统是分开的，而且更为高阶。CMake是为了解决美国国家医学图书馆出资的Visible Human Project专案下的Insight Segmentation and Registration Toolkit  (ITK)  软件的跨平台建构的需求而创造出来的，其设计受到了Ken Martin开发的pcmaker所影响。pcmaker当初则是为了支援Visualization Toolkit这个开放源代码的三维图形和视觉系统才出现的，今日VTK也采用了CMake。在设计CMake之时，Kitware公司的Bill Hoffman采用了pcmaker的一些重要想法，加上更多他自己的点子，想把GNU建构系统的一些功能整合进来。CMake最初的实作是在2000年中作的，在2001年初有了急速的进展，许多改良是来自其他把CMake整合到自己的系统中的开发者，比方说，采用CMake作为建构环境的VXL社群就贡献了很多重要的功能，Brad King为了支援CABLE和GCC-XML这套自动包装工具也加了几项功能，奇异公司的研发部门则用在内部的测试系统DART，还有一些功能是为了让VTK可以过渡到CMake和支援 ("美国Los Alamos国家实验室"&"洛斯阿拉莫斯国家实验室") 的Advanced Computing Lab的平行视觉系统ParaView而加的。


CMakeLists.txt

target_link_libraries: 指定链接的时候用哪些库

语法

    target_link_libraries(<target> ... <item>... ...)

示例

```c
add_executable(gsaslx main.c)
// <item> 可以用绝对路径
target_link_libraries(gsaslx /lib/x86_64-linux-gnu/libgsasl.so.7)
```

### adding source files

vim CMakeLists.txt

```bash
add_executable(gsaslx2 main.c)

target_link_libraries(gsaslx2 /usr/local/lib/libgsasl.so.7.9.6)
include_directories("/home/wiloon/tmp/gsasl-1.8.0/")

```
>https://stackoverflow.com/questions/40622244/clion-enable-debugging-of-external-libraries-by-adding-source-files


https://www.hahack.com/codes/cmake/   
http://www.cmake.org/   
https://zhuanlan.zhihu.com/p/59161370  
>https://cmake.org/cmake/help/latest/command/target_link_libraries.html
