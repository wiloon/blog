---
title: Console(控制台), Terminal(终端), tty, shell
author: "-"
date: 2018-12-24T04:52:41+00:00
url: console-terminal-tty-shell
categories:
  - shell
tags:
  - reprint
  - remix
---
## Console(控制台), Terminal(终端), tty, shell

[https://blog.csdn.net/on_1y/article/details/20203963](https://blog.csdn.net/on_1y/article/details/20203963)

使用 linux 已经有一段时间, 却一直弄不明白这几个概念之间的区别。虽然一直在用, 但是很多概念都感觉模糊不清, 这样不上不下的状态实在令人不爽。下面就澄清一下这些概念。

这些概念本身有着非常浓厚的历史气息, 随着时代的发展, 他们的含义也在发生改变, 它们有些已经失去了最初的含义, 但是它们的名字却被保留了下来。

控制台(Console)
  
控制台(Console)是物理设备,用于输入输出,它直接连接在计算机上,是计算机系统的一部分。计算机输出的信息会显示在控制台上,例如BIOS的输出,内核的输出。

终端(Terminal)
  
终端(Terminal)也是一台物理设备,只用于输入输出,本身没有强大的计算能力。一台计算机只有一个控制台,在计算资源紧张的时代,人们想共享一台计算机,可以通过终端连接到计算机上,将指令输入终端,终端传送给计算机,计算机完成指令后,将输出传送给终端,终端将结果显示给用户。

虚拟控制台(Virtual Console),虚拟终端(Virtual Terminal)
  
虚拟控制台(Virtual Console)和虚拟终端是一样的。我们只有一台终端 (物理设备) ,这是我们与计算机之间的用户接口。假如有一天,我们想拥有多个用户接口,那么,一方面我们可以增加终端数目 (物理设备) ,另一方面,还可以在同一台终端 (物理设备) 上虚拟出多个终端,它们之间互相不影响,至少看起来互相不影响。这些终端就是虚拟终端。

在Ubuntu中,我们按下Ctrl+Alt+Fx时,会进入第x个虚拟终端,一共有七个虚拟终端,其中第七个虚拟终端,就是我们默认使用的图形用户界面。

终端模拟器(Terminal Emulator)
  
我们知道,终端是一种物理设备,而终端模拟器(Terminal Emulator),是一个程序,这些程序用来模拟物理终端。图形用户界面中的终端模拟器一般称为终端窗口(Terminal Window),我们在Ubuntu下打开的gnome-terminal就属于此类。

## tty
  
tty 的全称是 TeleTYpewriter, 这就是早期的终端 (物理设备), 它们用于向计算机发送数据, 并将计算机的返回结果打印出来。显示器出现后, 终端不再将结果打印出来,而是显示在显示器上。但是tty的名字还是保留了下来。

在Ubuntu中,我们按下Ctrl+Alt+F1时,会进入第1个虚拟终端,你可以看到屏幕上方显示的tty1。

## shell
  
shell 和之前说的几个概念截然不同, 之前的几个概念都是与计算机的输入输出相关的, 而 shell 是和内核相关的。内核为上层的应用提供了很多服务, shell 在内核的上层, 在应用程序的下层。例如,你写了一个 hello world 程序,你并不用显式地创建一个进程来运行你的程序,你把写好的程序交给shell就行了,由shell负责为你的程序创建进程。

我们在终端模拟器中输入命令时, 终端模拟器本身并不解释执行这些命令, 它只负责输入输出, 真正解释执行这些命令的, 是 shell。

我们平时使用的sh, bash, csh 是 shell 的不同实现。

### sh 

Ubuntu 23.10 的 sh 是 /usr/bin/dash 的软链接

Archlinux 的 sh 是 /usr/bin/bash 的软链接

sh 这个概念本身就有岐义, 它可以指 shell 程序的名字, 也代表了 shell 的实现。

Thompson shell 是第一个 Unix shell, 由 Ken Thompson 于 1971 年在 Unix 第一版本中引入, shell 的程序名即为 sh。
Bourne shell 作为 Thompson shell 的替代, 由 Stephen Bourne 于 1977 年在 Unix 第七版中引入, 它的程序名也是 sh。
Bourne shell 不仅仅是一个命令解释器, 更作为一种编程语言, 提供了 Thompson shell 不具备的程序控制功能, 并随着 Brian W. Kernighan 
和 Rob Pike 的 The UNIX Programming Environment 的出版而名声大噪。

csh csh 全称为 C Shell, 由 Bill Joy 在 70 年代晚期完成, 那时候他还是加州伯克利大学的研究生。tcsh 是 csh 的升级版。
与 sh 不同, csh 的 shell 脚本, 语法接近于 C 语言。

bash 是由 Brian Fox 为 GNU 项目开发的自由软件, 作为 Bourne shell 的替代品, 于 1989 年发布。是 Linux 和 Mac OS X 的默认 shell。
bash 的命令语法是 Bourne shell 命令语法的超集,从 ksh 和 csh 借鉴了一些思想。

好了, 就写到这里, 上面的内容是我参考维基百科后写下的, 不保证完全正确, 下面还提供了一些资料, 如果有兴趣可以阅读一下

作者: on_1y  
来源: CSDN  
原文: [https://blog.csdn.net/on_1y/article/details/20203963](https://blog.csdn.net/on_1y/article/details/20203963)
版权声明: 本文为博主原创文章,转载请附上博文链接！  

### dash

http://gondor.apana.org.au/~herbert/dash/

```Bash
# doc
man dash

# 从一个字符串中读取命令而不是从 stdin
dash -c 
```

dash （Debian Almquist shell）一种 Unix shell。它比 Bash 小，只需要较少的磁盘空间，但是它的对话性功能也较少。
它由 NetBSD 版本的 Almquist shell (ash) 发展而来，于 1997 年由赫伯特·许（Herbert Xu）移植到 Linux 上，于 2002 年改名为 dash。

版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/lingeio/article/details/96135086
