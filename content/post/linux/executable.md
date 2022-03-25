---
title: 可执行文件
author: "-"
date: 2012-03-01T04:36:04+00:00
url: executable
categories:
  - OS

tags:
  - reprint
---
## 可执行文件

目标文件与可执行文件格式的小历史
目标文件与可执行文件的格式和操作系统和编译器密切相关，不同的系统平台下会有不同的格式，但是这些格式又大同小异，可以说，目标文件与可执行文件格式的历史几乎是操作系统的发展史。

COFF是由Unix System V Release 3首次提出并使用的格式规范，后来Microsoft在其基础上，制定了PE格式标准，并将其应用于自家的Windows NT系统。后台，System V Release 4 在 COFF的基础上引入了ELF格式，目前流行的Linux系统也是以ELF作为基本的可执行文件格式。这也是为什么目前PE和ELF如此相似的原因，因为它们都是源于同一种可执行文件格式COFF。

在COFF之前，Unix最早的可执行文件格式是a.out格式，中文意为汇编器输出。因其设计简单，以至于后来共享库出现的时候，a.out格式变得捉襟见肘，难以满足共享库实现的要求，于是从Unix System V Release 3开始被COFF取代。由于COFF格式的设计非常通用，以至于COFF的继承者PE和ELF目前还在被广泛地使用。COFF的主要贡献是在目标文件中引入了“段”的机制，不同的目标文件可以拥有不同数量及不同类型的段。另外，还定义了调试数据的格式。


可执行文件(Executable File)是指可以由操作系统直接加载执行的文件，在Windows操作系统中可执行文件就是PE文件结构，在Linux下则是ELF文件

PE文件整体结构
PE结构可以大致分为:

DOS部分
PE文件头
节表(块表)
节数据(块数据)
调试信息

PE文件种类如下表所示：
种类	主扩展名
可执行系列	EXE, SCR
库系列	DLL, OCX, CPL, DRV
驱动程序系列	SYS, VXD
对象文件系列	OBJ

在Windows下所谓PE文件即Portable Executable，意为可移植的可执行的文件。常见的.EXE、.DLL、.OCX、.SYS、.COM都是PE文件。PE文件有一个共同特点：前两个字节为4D 5A (MZ）。如果一个文件前两个字节不是4D 5A则其肯定不是可执行文件。比如用16进制文本编辑器打开一个“.xls”文件其前两个字节为：0XD0 0XCF；打开一个“.pdf”其前两个字节为：0X25 0X50。
————————————————
版权声明：本文为CSDN博主「Apollon_krj」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/Apollon_krj/article/details/77069342

>https://www.ascotbe.com/2020/03/23/PortableExecutable/


### ELF (Executable Linkable Format）

ELF (Executable Linkable Format）：linux下的可执行文件格式，按照ELF格式编写的文件包括：.so、.a等

### Mach-O
Mach-O：IOS／MacOS下可执行文件格式，平时常见的.app或者ipa只是zip压缩包并非可执行文件，可执行文件在压缩包中。在mac下使用file命令打印任意可执行文件便可以看到如下内容：


> file /Applications/filename.app/Contents/MacOS/filename
Mach-O 64-bit executable x86_64

作者：无边小猪
链接：https://www.jianshu.com/p/21850560caf0
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


msi实际上一个压缩包, 不是PE文件  
.msi文件是需要Windows Installer(msiexec.exe)来安装的

>https://bbs.csdn.net/topics/390722531
