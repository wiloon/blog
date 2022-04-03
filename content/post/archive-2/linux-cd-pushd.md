---
title: linux cd Pushd
author: "-"
date: 2016-07-02T02:05:53+00:00
url: /?p=9105
categories:
  - Uncategorized

tags:
  - reprint
---
## linux cd Pushd
http://os.51cto.com/art/200910/158752.htm


3,如何在多个目录之间切换？

用 pushd +n即可
  
说明:
  
n是一个数字,有此参数时,是切换到堆栈中的第n个目录,并把此目录以堆栈循环的方式推到堆栈的顶部
  
需要注意: 堆栈从第0个开始数起

看例子:

[root@localhost grub]# dirs -v
  
0  /boot/grub
  
1  /usr/share/kde4/apps/kget
  
2  /usr/local/sbin
  
3  ~
  
[root@localhost grub]# pushd +2
  
/usr/local/sbin ~ /boot/grub /usr/share/kde4/apps/kget
  
[root@localhost sbin]# dirs -v
  
0  /usr/local/sbin
  
1  ~
  
2  /boot/grub
  
3  /usr/share/kde4/apps/kget

4,如何把目录从堆栈中删除?


在向大家详细介绍linux之前,首先让大家了解下linux cd命令,然后全面介绍巧用linux cd命令的方法。在Linux的多目录命令提示符中工作是一种痛苦的事情,但以下这些利用linux cd命令和pushd切换目录的技巧有助于你节省时间和精力。

在Linux命令提示中,用linux cd命令来改变当前目录。这是linux cd命令的一些基本用法: 
  
改变你的根路径,键入cd,按回车键。
  
进入一个子目录,键入cd,空格,然后是子路径名 (例如: cd Documents) ,再按回车键。
  
进入当前目录的上一级目录,键入cd,空格,两个点,然后按回车键。
  
进入一个特定的目录,键入cd,空格,路径名 (例如 cd /usr/local/lib) ,再按回车键。

为了确定你所在的目录,你可以键入pwd,按回车键,你将看到你所在的当前目录名称。
  
与linux cd命令相似,用pushd实现在不同目录间切换。
  
在命令行模式下,当你工作在不同目录中,你将发现你有很多时间都浪费在重复输入上。如果这些目录不在同一个根目录中,你不得不在转换时输入完整的路径名,这难免让人有些难以忍受。但你可以用以下的一个或两个步骤来避免所有多余的输入: 用命令行解释器中的历史记录,或者用命令行函数pushd。

用命令行解释器中的历史记录的好处是只需按很少的键。在命令行中用向上的箭头来查找你用过的命令,直到你找到,然后按回车键。如果你所切换的两个目录在整个驱动器的子目录结构中很接,那用解释器中的历史记录可能是你最好的选择。然而,如果你在两个截然不同的路径间转换的话,你可能很希望利用pushd这个函数,你可以用它创建一个目录堆栈 (在内存中的一个列表) 。

注释: 缺省情况下,pushd函数可能不包括在你的Linux中；但它包涵在Red Hat和用Red Hat驱动的系统中。如果你的系统中没有pushd函数,你可以在ibiblio.org网站上下载相关的函数工具。
  
这里说一下怎么用pushd。假设你现在工作在/usr/share/fonts目录下。你需要对/usr/share/fonts做一些改动,你将频繁的在两个目录间切换。开始在一个目录下,用pushd函数切换到另一个目录。在我们的例子中,开始在/usr/share/fonts下,你键入pushd /opt/wonderword/fonts,然后按回车键。现在,你将在下一行看到堆栈中的内容: /opt/wonderword/fonts /usr/share/fonts。
  
正如你所看到的,当你键入pushd和一个路径名时,将自动产生一个堆栈,内容是你键入的目录名和你当前工作的目录名。在我们的例子中,你所键入的路径 (/opt/wonderword/fonts) 在堆栈的顶部。
  
快速返回上一级目录,你可以直接键入pushd,如果不跟路径名,
  
你将返回到堆栈中前一个目录的上一层目录。
  
如果你需要从堆栈中删除一个目录,键入popd,然后是目录名称,再按回车键。想查看堆栈中目录列表,键入dirs,然后按回车键。popd和dirs命令也是常用函数中的一部分。
  
以上是巧用linux cd命令和Pushd切换目录的方法,希望对您能有所帮助。