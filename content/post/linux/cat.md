---
title: cat
author: "-"
date: 2012-06-21T01:17:40+00:00
url: /?p=3553
categories:
  - Linux
tags:
  - reprint
---
## linux cat
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
