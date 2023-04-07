---
title: 'shell, bash, csh, sh, ksh, dash, zsh'
author: "-"
date: 2011-12-04T01:55:39+00:00
url: shell
categories:
  - shell
tags:
  - reprint
---
## 'shell, bash, csh, sh, ksh, dash, zsh'

<https://blog.csdn.net/lina_acm/article/details/51815080>

Linux中的shell有多种类型，其中最常用的几种是Bourne shell (sh) 、C shell (csh) 和Korn shell (ksh) 。三种shell各有优缺点。Bourne shell是UNIX最初使用的shell，并且在每种UNIX上都可以使用。Bourne shell在shell编程方面相当优秀，但在处理与用户的交互方面做得不如其他几种shell。Linux操作系统缺省的shell是Bourne Again shell，它是Bourne shell的扩展，简称Bash，与Bourne shell完全向后兼容，并且在Bourne shell的基础上增加、增强了很多特性。Bash放在/bin/bash中，它有许多特色，可以提供如命令补全、命令编辑和命令历史表等功能，它还包含了很多C shell和Korn shell中的优点，有灵活和强大的编程接口，同时又有很友好的用户界面。

shell 脚本第一行以

# !/bin/bash
  
开头, 表示由/bin/bash负责解释.

# !/bin/sh
  
# !/bin/csh
  
# !/usr/bin/perl
  
# !/bin/php
  
# !/bin/expect
  
都是脚本常用的开头。
  
# ! 用来指定解释脚本的程序，可以是 Shell，也可以是其他程序
  
有一个非常奇怪的名字，叫shbang line
  
# !叫做Magic number

按照下面的方式来解释执行shell脚本
  
1) 如果shell脚本的第一个非空白字符不是"#"，则它会使用Bourne shell。
  
2) 如果shell脚本的第一个非空白字符是"#"，但不以"#!"开头时，则它会使用C shell。
  
3) 如果外壳脚本以"#!"开头，则" #!"后面所跟的字符串就是所使用的shell的绝对路径
  
名。Bourne shell的路径名称为/bin/sh ，而C shell则为/bin/csh。

sh (Bourne Shell) : 由Steve Bourne开发，各种UNIX系统都配有sh。
  
csh (C Shell) : 由Bill Joy开发，随BSD UNIX发布，它的流程控制语句很像C语言，支持很多Bourne Shell所不支持的功能: 作业控制，命令历史，命令行编辑。
  
ksh (Korn Shell) : 由David Korn开发，向后兼容sh的功能，并且添加了csh引入的新功能，是目前很多UNIX系统标准配置的Shell，在这些系统上/bin/sh往往是指向/bin/ksh的符号链接。
  
tcsh (TENEX C Shell) : 是csh的增强版本，引入了命令补全等功能，在FreeBSD、Mac OS X等系统上替代了csh。
  
bash (Bourne Again Shell) : 由GNU开发的Shell，主要目标是与POSIX标准保持一致，同时兼顾对sh的兼容，bash从csh和ksh借鉴了很多功能，是各种Linux发行版标准配置的Shell，在Linux系统上/bin/sh往往是指向/bin/bash的符号链接[38]。虽然如此，bash和sh还是有很多不同的，一方面，bash扩展了一些命令和参数，另一方面，bash并不完全和sh兼容，有些行为并不一致，所以bash需要模拟sh的行为: 当我们通过sh这个程序名启动bash时，bash可以假装自己是sh，不认扩展的命令，并且行为与sh保持一致。

在Linux系统上，通常有好几种shell可用，比较常见的有bash、dash和zsh shell。不同shell各有千秋: 有些更易于创建脚本，有些更易于管理进程。

bash shell是几乎所有Linux发行版的默认shell。作为标准Unix shell——Bourne shell (沿用创建者的名字) 的替代，bash shell由GNU工程开发。bash shell的名称就是针对这个Bourne shell的文字游戏，全称为"Bourne again shell"。 bash有很灵活和强大的编程接口，同时又有很友好的用户界面。功能包括命令补齐、通配符、命令历史记录、别名等。

dash shell是作为Debian Linux发行版的一部分开发的，主要出现在Ubuntu Linux发行版中。它是Bourne shell的精简版，支持的功能不像bash shell支持的那样多，这可能会给脚本编程带来一些问题。

dash shell的历史很有趣。它是ash shell的直系后代，而ash shell是Unix系统上原来的Bourne shell的简化版本。令人不解的是，实际上dash shell在许多基于Debian的Linux发行版中并不是默认的shell。由于bash shell在Linux中的流行，大多数基于Debian的Linux发行版将bash shell用作普通登录shell，只将dash shell用作安装脚本的快速启动shell来安装发行版文件。而流行的Ubuntu发行版是一个例外。Ubuntu Linux发行版将bash shell用作默认的交互shell，但将dash shell用作默认的/bin/sh shell。这通常会让shell脚本程序员很困惑，并给在Linux环境中运行shell脚本带来了很多问题。

zsh (Z shell) 是另一个流行的shell，是由Paul Falstad开发的开源Unix shell。它集成了所有现有shell的思想并增加了许多独到的功能，为程序员创建了一个全功能的高级shell。zsh shell具有三大功能: 改进的shell选项处理、shell兼容性模式以及可加载模块。其中，可加载模块是shell设计中最先进的功能。
