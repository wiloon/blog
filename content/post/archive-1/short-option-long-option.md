---
title: 长选项, 短选项, short options, long options
author: "-"
date: 2019-07-24T05:44:05+00:00
url: /?p=5703
categories:
  - Web
tags:
  - reprint
---
## 长选项, 短选项, short options, long options

1.Linux命令长选项"--"和短选项"-"和没有"-"选项背景：
在解释这些区别之前我们先了解一下有关linux的背景知识，这个需要大家先认真看完就会对这些区别有更深入的了解，对linux也有更深的了解：

（1）Unix操作系统在操作风格上主要分为System V和BSD(目前一般采用BSD的第4个版本SVR4)，前者的代表的操作系统有Solaris操作系统，在Solaris1.X之前，Solaris采用的是BSD风格，2.x之后才投奔System V阵营。后者的代表的操作系统有FreeBSD。

（A）System V它最初由AT&T开发，曾经也被称为AT&T System V，是Unix操作系统众多版本中的一支。在1983年第一次发布，一共发行了4个System V的主要版本，System V Release4，或者称为SVR4，是最成功的版本，该版本有些风格成为一些UNIX共同特性的源头，如下表格的初始化脚本/etc/init.d。用来控制系统的启动和关闭。

（B）BSD（Berkeley Software Distribution，伯克利软件套件）是Unix的衍生系统，1970年代由伯克利加州大学（Uni Versity of California, Berkeley）开创。BSD用来代表由此派生出的各种套件集合。
 

（2）关于System V和BSD风格以及他们与Linux的关系：

（A）System V 和BSD同出于AT＆T实验室的两个不同的部门，SystemV是一个Unix的商业化标准，BSD为Unix标准化的Berkeley风格。

（B）由于Linux是Linus Torvalds在以Unix为构架的系统上重新开发的，但仍沿用了两大Unix系统进程的风格，实事上应该确切的说Linus Torvalds只开发了kernel，而软件依然来自GNU和GPL两个组织。

目前只有Slackware是Linux发行版中唯一使用BSD风格的版本。其他的就是FreeBSD、NetBSD和OpenBSD三个著名的BSD发行版，并遵循「GPL规范」。在商业版的Unix及多数Linux发行版使用SystemV风格的init『可能有版权纠纷问题』。Linux代表的有：RedHat、Suse、MDV、MagicLinux、Debian等几乎大部分发行版。Unix代表的有AIX、IRIX、Solars、HP-UX。

 

2.Linux命令长选项"--"和短选项"-"和没有"-"选项的全部写法
（1）选项前有一横“-”，如“ls -a”（含义：list all,列出所有当前文件夹的文件）

（2）选项前有两横“--”，如“ls --all”（含义：list all,列出所有当前文件夹的文件）

（3）选项前有一横“-”，如“tar -xzvf”（tar命令用于对文件打包压缩或解压，格式为：“tar [选项] [文件]”，-xzvf是4个参数的组合体,tar命令最初的设计目的是将文件备份到磁带上(tape archive)，因而得名tar）

（4）选项前没有任何横，如“tar xzvf”

 

3.Linux命令长选项"--"和短选项"-"和没有"-"选项的详细解释
（1）短选项（short options）:顾名思义，就是短小参数。它们通常包含一个连字号‘-’和一个字母（大写或小写字母）。例如：-s，-h等

（2）长选项（long options）：长选项，包含了两个连字号"--"和一些大小写字母组成的单词。例如：--size，--help等

（3）参数前有横的是 System V风格

（4）参数前没有横的是 BSD风格

 

4.Linux命令长选项"--"和短选项"-"的意义及额外备注
（1）一个程序通常会提供包括short options和long options两种参数形式的参数，例如："ls -a"和“ls --all”等价

（2）因为短选项（short option）是可以合并的，如-sh,为了区分sh是一个选项还是两个选项s和h的组合，对于组合选项用单连字符'-',如果是单一选项sh则要用双连字符'--'。例如：-sh表示-s和-h的组合，如果要表示为一个选项需要用长选项--sh。

（3）但是对于一些命令，它们不遵循以上的规则，例如：“find -type d -mindepth 2”和“find -name -fstype”（它们是单连字符'-'连接一个完整单词，不符合3（1）和3（2））
————————————————
版权声明：本文为CSDN博主「快乐李同学(李俊德-大连理工大学)」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/wq6ylg08/article/details/88812451

>https://blog.csdn.net/wq6ylg08/article/details/88812451
>https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
