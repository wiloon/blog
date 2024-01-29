---
title: cd pushd
author: "-"
date: 2016-07-02T02:05:53+00:00
url: /?p=9105
categories:
  - Linux
tags:
  - reprint
  - remix
---
## cd pushd

http://os.51cto.com/art/200910/158752.htm

## cd -

```Bash
# list current dir
pwd
/foo

# cd to /bar
cd /bar
pwd
/bar

# 可以在 $OLDPWD 变量里查看旧目录
echo $OLDPWD

# cd - return to previous dir /foo
cd -
pwd
/foo

# cd -, return to previous dir /bar
cd -
pwd
/bar
```

## pushd、popd 和 dirs

pushd 和 popd 是对一个目录栈进行操作，而 dirs 是显示目录栈的内容。而目录栈就是一个保存目录的栈结构，该栈结构的顶端永远都存放着当前目录（这里点从下面可以进一步看到）。

dirs 的 参数：

- -p	每行显示一条记录
- -v	每行显示一条记录，同时展示该记录在栈中的 index
- -c	清空目录栈, 将目录栈中除当前目录之外的其它目录清除

每次 cd 之后, 新目录都会被记录到目录栈中

pushd
每次pushd命令执行完成之后，默认都会执行一个dirs命令来显示目录栈的内容。pushd的用法主要有如下几种：

pushd 目录

pushd 后面如果直接跟目录使用，会切换到该目录并且将该目录置于目录栈的栈顶。(时时刻刻都要记住，目录栈的栈顶永远存放的是当前目录。如果当前目录发生变化，那么目录栈的栈顶元素肯定也变了；反过来，如果栈顶元素发生变化，那么当前目录肯定也变了。)

pushd 不带任何参数。相当于 pushd -1

pushd 不带任何参数执行的效果就是，将目录栈最顶层的两个目录进行交换。前面说过，栈顶目录和当前目录一个发生变化，另一个也变。这样，实际上，就实现了cd -的功能。


## pushd -n

在 archlinux 上测试的 pushd 行为跟搜到的资料不一致, 可能是版本不同吧 2023.12.05

pushd -n cd 到 dirs -v 正序第 n 个目录
pushd +n cd 到 dirs -v 倒序第 n 个目录

```Bash
dirs -c
cd /home
cd /mnt
cd /tmp
cd /var

dirs -v

0       /var
1       /tmp
2       /mnt
3       /home
4       /

pushd -1
/tmp /mnt /home / /var

pushd +1
/ /var /tmp /mnt /home
```

## popd

次popd命令执行完成之后，默认都会执行一个dirs命令来显示目录栈的内容。popd的用法主要有如下几种：

popd不带参数

popd不带任何参数执行的效果，就是将目录栈中的栈顶元素出栈。这时，栈顶元素发生变化，自然当前目录也会发生相应的切换(接上文的执行现场)，

```Bash
dirs -v
0       /
1       /var
2       /tmp
3       /mnt
4       /home

popd

dirs -v
0       /var
1       /tmp
2       /mnt
3       /home

# 从栈中删除第二个元素 /mnt 但是栈顶元素不变, 目录不会发生切换.
popd -2

0       /var
1       /tmp
2       /home

pupd /mnt

0       /mnt
1       /var
2       /tmp
3       /home

# 从栈中删除倒数第一个元素 /tmp, 栈顶元素不变, 目录不切换
popd +1

0       /mnt
1       /var
2       /home

# 删除栈中倒数第二个元素 /mnt, 栈顶元素变化, 目录切换到了 /var
popd +2
/var /home
```

-n是指从左往右数，+n是指从右往左数，都是从0开始。

---

如何把目录从堆栈中删除?

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

作者：SpaceCat
链接：https://www.jianshu.com/p/53cccae3c443
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。