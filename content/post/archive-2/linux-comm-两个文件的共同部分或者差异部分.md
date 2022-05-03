---
title: linux comm, 两个文件的共同部分或者差异部分
author: "-"
date: 2018-12-28T08:28:03+00:00
url: /?p=13228
categories:
  - Uncategorized

tags:
  - reprint
---
## linux comm, 两个文件的共同部分或者差异部分

两个文件的共同部分或者差异部分

1 comm 命令

在我们的开发和运营中,特别是对业务进行监控的时候,我们常常需要写一些监控shell脚本,而这些脚本需要求两个文件的共同的记录列表或者只出现在第一个文件但不出现在第二个文件的记录列表的场景,此时,comm命令则是您解决此类问题的利器和助手。

     随意man comm下,可以在linux下看到该命令的使用方法: 

NAME

comm - compare two sorted files line by line

SYNOPSIS

comm [OPTION]... FILE1 FILE2

DESCRIPTION

Compare sorted files FILE1 and FILE2 line by line.

       With  no  options,  produce  three-column  output.   Column one contains lines unique to FILE1, column two contains lines
       unique to FILE2, and column three contains lines common to both files.
    
       -1     suppress lines unique to FILE1
    
       -2     suppress lines unique to FILE2
    
       -3     suppress lines that appear in both files
    
       --help display this help and exit
    
       --version
              output version information and exit
    
     上面是英文说明,下面简单的说明如下: 
    
     一,利用comm命令进行处理的文件必须首先通过sort命令进行排序处理并且是unix格式而非dos格式的文本文件；
    
     二,中文说明如下: 

功能说明: 比较两个已排过序的文件。 (使用sort排序)
  
语法: comm [-123][-help][-version][第1个文件][第2个文件]
  
补充说明: 这项指令会一列列地比较两个已排序文件的差异,并将其结果显示出来,如果没有指定任何参数,则会把结果分成3栏显示: 第1栏仅是在第1个文件中出现过的记录,第2栏是仅在第2个文件中出现过的记录,第3栏则是在第1与第2个文件里都出现过的记录。若给予的文件名改为"-",则comm指令会从标准输入设备读取数据。
  
参数:

-1 不显示只在第1个文件里出现过的列。

-2 不显示只在第2个文件里出现过的列。

-3 不显示只在第1和第2个文件里出现过的列。

-help 在线帮助。

-version 显示版本信息。
  
例子
  
comm - 12 就只显示在两个文件中都存在的行；
  
comm - 23 只显示在第一个文件中出现而未在第二个文件中出现的行；
  
comm - 123 则什么也不显示。

例如: 找出a.txt文件有而b.txt文件中没有的放在c.txt文件中(注意: 一定要是先排序,即sort)

# !/bin/sh

# author by tianmo

# date 2011-11-21 20:33

# BEGIN
  
cat a.txt | sort | uniq | sort > a_u.txt
  
cat b.txt | sort | uniq | sort > b_u.txt
  
comm -23 a_u.txt b_u.txt > c.txt

# END

2 diff命令
  
功能说明: 比较文件的差异。

语法: diff [-abBcdefHilnNpPqrstTuvwy][-<行数>][-C <行数>][-D <巨集名称>][-I <字符或字符串>][-S <文件>][-W <宽度>][-x <文件或目录>][-X <文件>][-help][-left-column][-suppress-common-line][文件或目录1][文件或目录2]

补充说明: diff以逐行的方式,比较文本文件的异同处。所是指定要比较目录,则diff会比较目录中相同文件名的文件,但不会比较其中子目录。

参数:

-<行数> 指定要显示多少行的文本。此参数必须与-c或-u参数一并使用。

-a或-text diff预设只会逐行比较文本文件。

-b或-ignore-space-change 不检查空格字符的不同。

-B或-ignore-blank-lines 不检查空白行。

-c 显示全部内文,并标出不同之处。

-C<行数>或-context<行数> 与执行"-c-<行数>"指令相同。

-d或-minimal 使用不同的演算法,以较小的单位来做比较。

-D<巨集名称>或ifdef<巨集名称> 此参数的输出格式可用于前置处理器巨集。

-e或-ed 此参数的输出格式可用于ed的script文件。

-f或-forward-ed 输出的格式类似ed的script文件,但按照原来文件的顺序来显示不同处。

-H或-speed-large-files 比较大文件时,可加快速度。

-l<字符或字符串>或-ignore-matching-lines<字符或字符串> 若两个文件在某几行有所不同,而这几行同时都包含了选项中指定的字符或字符串,则不显示这两个文件的差异。

-i或-ignore-case 不检查大小写的不同。

-l或-paginate 将结果交由pr程序来分页。

-n或-rcs 将比较结果以RCS的格式来显示。

-N或-new-file 在比较目录时,若文件A仅出现在某个目录中,预设会显示:

Only in目录: 文件A若使用-N参数,则diff会将文件A与一个空白的文件比较。

-p 若比较的文件为C语言的程序码文件时,显示差异所在的函数名称。

-P或-unidirectional-new-file 与-N类似,但只有当第二个目录包含了一个第一个目录所没有的文件时,才会将这个文件与空白的文件做比较。

-q或-brief 仅显示有无差异,不显示详细的信息。

-r或-recursive 比较子目录中的文件。

-s或-report-identical-files 若没有发现任何差异,仍然显示信息。

-S<文件>或-starting-file<文件> 在比较目录时,从指定的文件开始比较。

-t或-expand-tabs 在输出时,将tab字符展开。

-T或-initial-tab 在每行前面加上tab字符以便对齐。

-u,-U<列数>或-unified=<列数> 以合并的方式来显示文件内容的不同。

-v或-version 显示版本信息。

-w或-ignore-all-space 忽略全部的空格字符。

-W<宽度>或-width<宽度> 在使用-y参数时,指定栏宽。

-x<文件名或目录>或-exclude<文件名或目录> 不比较选项中所指定的文件或目录。

-X<文件>或-exclude-from<文件> 您可以将文件或目录类型存成文本文件,然后在=<文件>中指定此文本文件。

-y或-side-by-side 以并列的方式显示文件的异同之处。

-help 显示帮助。

-left-column 在使用-y参数时,若两个文件某一行内容相同,则仅在左侧的栏位显示该行内容。

-suppress-common-lines 在使用-y参数时,仅显示不同之处。

例如:  找出a.txt文件有而b.txt文件中没有的放在c.txt文件中

# !/bin/sh

# author by tianmo

# date 2011-11-21 20:33

# BEGIN
  
cat a.txt | sort | uniq | sort > a_u.txt
  
cat b.txt | sort | uniq | sort > b_u.txt
  
diff a_u.txt b_u.txt | grep /< | awk ' $1 = " " ' > c.txt

# END

3 Linux系统下比较两个文件并删除相同部分

        方法一: 

comm -23 file1 file2

方法二:

grep -v -f file1 file2

/_注: : 此法在对比数字时候比较凑效果,文本对比不建议使用_/

方法三:

awk '{print NR,$0}' file1 file2 |sort -k2|uniq -u -f 1|sort -k1|awk '{print $2}'

或者:

awk '{print $0}' file1 file2 |sort|uniq -u

4 Linux Shell删除两个文件相同部分

因为在面试中遇到一个这样的问题,当时模模糊糊的,没有很确定的回答出来,后来上网查了一下结果,这里总结一下。首先描述一下这个问题: 比如两个文件file1和file2,删除两个文件中共同的部分,留下两个文件中独自有的部分。在网上找到一篇解决的答案,地址在这里<http://hi.baidu.com/robertoyuan/blog/item/559483c4946ed5a78226acac.html>。这里提到三种方法,但是没有给具体的解释。

方法一: 使用grep
  
grep -v -f file1 file2 && grep -v -f file2 file1
  
grep命令的详细使用方法,可以参考man,这里有一个简单实用的介绍: <http://linux.ccidnet.com/art/3067/20070313/1035613_1.html。在方法一中,用到了两个参数。参数-v,表示invert> match,即反向匹配,输出没有匹配上的项。参数-f,表示从文件中读取匹配模板(pattern)。方法一中的前一部分,在文件file1中匹配模板,来反向匹配文件file2中的内容,即输出文件file2中,在file1中没有的内容。后面的一部分同理可得,输出文件file1中,在file2中没有的内容。

方法二: 实用comm
  
comm -3 file1 file2
  
这个方法看起来最简单。命令comm的功能就是,逐行比较两个排好序的文件,默认输出有三列: 只在file1中有的行、只在file2中有的行、在file1和file2中共有的行。有参数-1 -2 -3,分别来抑制输出对应的列。例如在我们的方法二中,实用-3参数,不输出file1和file2中共有的部分。即能达到我们本文的目的。
  
但是注意到,comm比较排好序的两个文件,comm在处理文件的时候,首先要查看文件是否有序,例如file1和file2的内容如下:

$cat file1
  
line1
  
line2
  
line3
  
$cat file2
  
line0
  
line1
  
line3
  
line2
  
调用前面方法二的命令的时候,就会提示file2文件时无序的,输出的结果如下:

$ comm -3 file1 file2

line0
  
line2
  
comm: file 2 is not in sorted order

line2
  
如果使用-nocheck-order参数,不进行有序性检测,结果如下:

$ comm -3 -nocheck-order file1 file2

line0
  
line2

        line2

从这个结果中我们可以看到,这还是不是我们真正想要的结果。这里可体现comm的另一个特征,就是逐行比较。它是对file1和file2进行逐行往下的比较,检测是否相同。所以,在用comm的时候,要根据具体的情况进行分析了。

方法三: 使用awk
  
awk '{print NR, $0}' file1 file2 | sort -k2 | uniq -u -f 1 | sort -k1 | awk '{print $2}'
  
或者:
  
awk '{print $0}' file1 file2 | sort | uniq -u

awk命令的使用,听牛人说可谓博大精深,我也没有太搞清楚。这里只是使用了一些简单的功能。下面以我自己的理解来解释一下上面的shell代码。awk就是文本的解释器和过滤器。awk把每一行看成是一个记录(record),每个记录使用分隔符(默认是空格)把每条记录分成若干域。awk内置参数$0表示整行,$1、$2...分别表示各域,内置参数NR,表示记录的计数,awk '{print NR, $0}' file1 file2表示依次读取file1 file2,打印出每行,并且在前面添加行号。

     命令sort,就是对行进行排序,参数-k表示根据各行的第几个参数关键字开进行排序,这里的-k2表示根据第二个关键字开始进行排序。
    
     命令uniq,进行报告或者忽略重复的行,参数-u,表示只是打印出唯一的行(unique lines),-f表示忽略的每行的前n个域的比较。 

grep -xf file1 file2

补充的重要内容:

1. 统计两个文本文件的相同行

grep -Ff file1 file2

2. 统计file2中有,file1中没有的行

grep -vFf file2 file1

如何比较两个文件并去删除相同的内容

for i in $(<file1); do grep $i file2 || echo $i >>tmp1 ; done

输出相同行:

$grep -wf file1 file2

输出不同行

$grep -wvf file1 file2
