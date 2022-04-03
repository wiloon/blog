---
title: linux 运行级, runlevel
author: "-"
date: 2011-11-21T04:44:52+00:00
url: /?p=1566
categories:
  - Linux
tags:
  - RedHat

---
## linux 运行级, runlevel
作为默认，REDHAT Linux 9.0在启动时会自动启动X-Window进入图形化操作界面。而许多Linux铁杆玩家已经习惯了在Console字符界面工作，或是有些玩家嫌X-Window启动太慢，喜欢直观快速的Console操作。

1.进入字符界面

为了在Linux启动时直接进入Console界面，我们可以编辑/etc/inittab文件。找到

id:5:initdefault:

这一行，将它改为

id:3:initdefault:

后重新启动系统即可。我们看到，简简单单地将5改为3，就能实现启动时进入X-Window图形操作界面或Console字符界面的转换，这是因为Linux操作系统有六种不同的运行级 (run level) ，在不同的运行级下，系统有着不同的状态，这六种运行级分别为: 

0: 停机 (记住不要把initdefault 设置为0，因为这样会使Linux无法启动 ) 
  
1: 单用户模式，就像Win9X下的安全模式。
  
2: 多用户，但是没有 NFS 。
  
3: 完全多用户模式，标准的运行级。
  
4: 一般不用，在一些特殊情况下可以用它来做一些事情。
  
5: X11，即进到 X-Window 系统。
  
6: 重新启动  (记住不要把initdefault 设置为6，因为这样会使Linux不断地重新启动) 。

其中运行级3就是我们要进入的标准Console字符界面模式。

2.自由转换字符界面和X-Window图形界面

在了解了启动自动进入X-Window图形操作界面和Console字符操作界面的转换后，也许你会想，这两种操作界面各有各的好处，我能不能"贪心"一点，同时拥有这两种操作界面呢?在无所不能的Linux操作系统中，这个要求当然是可以得到满足的。

在X-Window图形操作界面中按"Alt+Ctrl+功能键Fnn=1~6"就可以进入Console字符操作界面。这就意味着你可以同时拥有X-Window加上6个Console字符操作界面，这是一件多么令人振奋的事情啊!

在Console字符操作界面里如何回到刚才的X-Window中呢?很简单，按"Alt+Ctrl+F7"即可。这时Linux默认打开7个屏幕，编号为tty1~tty7。X-Window启动后，占用的是tty7号屏幕，tty1~tty6仍为字符界面屏幕。也就是说，用"Alt+Ctrl+Fn"组合键即可实现字符界面与X Window界面的快速切换。

Linux的老用户们都知道，X-Window是一个非常方便地图形界面，它能使用户用鼠标最简单的进行操作，但是它也有不少缺点: 比如启动和运行速度慢、稳定性不够、兼容性差、容易崩溃等。但是一旦X-Window系统出了问题，并不会使整个Linux系统的崩溃而导致数据丢失或系统损坏，因为当X-Window由于自身或应用程序而失去响应或崩溃时，我们可以非常方便地退出X-Window进入Console进行故障处理，要做的只是按"Alt+Ctrl+Backspace"键，这意味着只要系统没有失去对键盘的响应，X-Window出了任何问题，都可以方便地退出。