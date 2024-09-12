---
title: cat command
author: "-"
date: 2012-06-21T01:17:40+00:00
url: cat
categories:
  - Linux
tags:
  - reprint
---
## cat command
Red Hat Linux 有一个工具程序，它能够帮助你保留简短列表，将这些列表收集起来，甚至向你透漏一点你的系统信息。下面就是Linux Cat命令及使用详解

      Red Hat Linux 有一个工具程序，它能够帮助你保留简短列表，将这些列表收集起来，甚至向你透漏一点你的系统信息。下面就是Linux Cat命令及主要功能。
 

Linux Cat命令主要有三大功能: 
1.Linux Cat命令一次显示整个文件。$ 
    cat filename
 
2.Linux Cat命令从键盘创建一个文件。$ cat > filename
 只能创建新文件,不能编辑已有文件.

3.Linux Cat命令将几个文件合并为一个文件。
    cat file1 file2 > file_out
 参数: 
 -n 或 -number 由 1 开始对所有输出的行数编号
 -b 或 -number-nonblank 和 -n 相似，只不过对于空白行不编号
 -s 或 -squeeze-blank
 当遇到有连续两行以上的空白行，就代换为一行的空白行
 -v 或 -show-nonprinting
 范例: 
 cat -n textfile1 > textfile2 把 textfile1
 的档案内容加上行号后输入 textfile2 这个档案里
 cat -b textfile1 textfile2 >> textfile3 把 textfile1 和
 textfile2 的档案内容加上行号 (空白行不加) 之后将内容附加到
 textfile3 里。
 范例: 
 把 textfile1 的档案内容加上行号后输入 textfile2 这个档案里
 cat -n textfile1 > textfile2
 把 textfile1 和 textfile2
 的档案内容加上行号 (空白行不加) 之后将内容附加到 textfile3
 里。
 cat -b textfile1 textfile2 >> textfile3
 cat /dev/null > /etc/test.txt
 此为清空/etc/test.txt档案内容
 cat 也可以用来制作 image file。例如要制作软碟的 image
 file，将软碟放好后打
 cat /dev/fd0 > OUTFILE
 相反的，如果想把 image file 写到软碟，请打
 cat IMG_FILE > /dev/fd0
 注: 
 1. OUTFILE 指输出的 image 档名。
 2. IMG_FILE 指 image file。
 3. 若从 image file 写回 device 时，device 容量需与相当。
 4. 通常用在制作开机磁片。


## 用 cat 命令和 EOF 标识生成文件

[http://www.linuxfly.org/post/146/](http://www.linuxfly.org/post/146/)

在某些场合,可能我们需要在脚本中生成一个临时文件,然后把该文件作为最终文件放入目录中。 (可参考ntop.spec文件) 这样有几个好处,其中之一就是临时文件不是唯一的,可以通过变量赋值,也可根据不同的判断生成不同的最终文件等等。

一、cat 和 EOF

cat 命令是 linux 下的一个文本输出命令, 通常是用于观看某个文件的内容的；

EOF 是 "end of file", 表示文本结束符。

结合这两个标识, 即可避免使用多行echo命令的方式, 并实现多行输出的结果。

二、使用

看例子是最快的熟悉方法:

```bash
cat <<EOF >/etc/profile.d/goroot.sh
export GOROOT=$GOROOT
export GOPATH=$GOPATH
export PATH=\$PATH:$GOROOT/bin:$GOPATH/bin
EOF
```

结果:

引用

cat test.sh

!/bin/bash

you Shell script writes here

可以看到,test.sh的内容就是cat生成的内容。

三、其他写法

1. 追加文件

cat << EOF >> test.sh

2. 换一种写法

cat > test.sh << EOF

3. EOF只是标识,不是固定的

# cat << HHH > iii.txt

> sdlkfjksl

> sdkjflk

> asdlfj

> HHH

这里的"HHH"就代替了"EOF"的功能。结果是相同的。

引用

# cat iii.txt

sdlkfjksl

sdkjflk

asdlfj

4. 非脚本中

如果不是在脚本中,我们可以用Ctrl-D输出EOF的标识

# cat > iii.txt

skldjfklj

sdkfjkl

kljkljklj

kljlk

Ctrl-D

结果:

引用

# cat iii.txt

skldjfklj

sdkfjkl

kljkljklj

kljlk

※关于">"、">>"、"<"、"<<"等的意思,请自行查看bash的介绍。

