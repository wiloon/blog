---
title: diff
author: "-"
date: 2019-02-22T11:50:08+00:00
url: diff
categories:
  - Linux
tags:
  - reprint
  - remix
---
## diff

- diff 的三种格式
  - 正常格式
  - 上下文格式
  - 合并格式
- git 格式

Git's diff is a variant of unified diff, so unified diff is preferred.

```bash
# unified diff
diff -u foo bar
```

diff 是 Unix 系统的一个很重要的工具程序。它用来比较两个文本文件的差异，是代码版本管理的基石之一。

## diff 的三种格式

- 正常格式（normal diff）
- 上下文格式（context diff）
- 合并格式（unified diff）

### 命令格式

```bash
diff [参数] [文件1或目录1] [文件2或目录2]
```

```bash
diff -B -b  -r --exclude="*.vscode" --exclude="*.svn"  /etc/nginx/ /etc/foo-nginx/

diff -r \
   --exclude="*~" \
   --exclude=".svn" \
   --exclude=".git" \
   --exclude="*.zip*" \
   --exclude="*.gz" \
   --exclude="*.tar" \

# -B 或--ignore-blank-lines 不检查空白行。
# -b 或--ignore-space-change 不检查空格字符的不同。
# -r 递归比较子目录中的文件
# -x 或--exclude 不比较选项中所指定的文件或目录。
# -w 或--ignore-all-space 忽略全部的空格字符。
# -q 或--brief 仅显示有无差异,不显示详细的信息。
# -a 将所有的比对文件都当作文本文件处理

```

### 比较两个文件

```bash
diff foo.log bar.log

3c3
< 2014-03
---
> 2013-03
8c8
< 2013-07
---
> 2013-08
11,12d10
< 2013-11
< 2013-12
```

## 说明

- 3c3 用来说明变动位置, 分为三个部分, 第一个数字表示 foo.log 的第 3 行有变化, 中间的 c 表示变动模式是内容改变 (change), 后面的 3 表示 变动后变成 bar.log 文件的第3行.
- < 2014-03, 分为两个部分, 前面的小于号表示 foo.log 比 bar.log 少了这一行, 2014-03 是该行的内容
- --- 分隔线, 用于分隔 foo.log bar.log
- > 2013-03, 大于号表示 bar.log 增加了这行

上面的"3c3"和"8c8"表示 log2014.log 和 log20143log 文件在 3 行和第 8 行内容有所不同；"11,12d10" 表示第一个文件比第二个文件多了第11和12行。
  
diff 的 normal 显示格式有三种提示:
  
- a, add
- c, change
- d, delete

diff 命令是 linux 上非常重要的工具, 用于比较文件的内容, 特别是比较两个版本不同的文件以找到改动的地方。 diff在命令行中打印每一个行的改动。 最新版本的 diff 还支持二进制文件。 diff 程序的输出被称为补丁 (patch), 因为 Linux 系统中还有一个 patch 程序, 可以根据 diff 的输出将 a.c 的文件内容更新为 b.c。diff是svn、cvs、git等版本控制工具不可或缺的一部分。

2．命令功能:
  
diff命令能比较单个文件或者目录内容。如果指定比较的是文件,则只有当输入为文本文件时才有效。以逐行的方式,比较文本文件的异同处。如果指定比较的是目录的的时候,diff 命令会比较两个目录下名字相同的文本文件。列出不同的二进制文件、公共子目录和只在一个目录出现的文件。

3．命令参数:

- 指定要显示多少行的文本。此参数必须与-c或-u参数一并使用。

-a或-text diff预设只会逐行比较文本文件。
  
-c 显示全部内文, 并标出不同之处。
  
-C或-context 与执行"-c-"指令相同。
  
-d或-minimal 使用不同的演算法,以较小的单位来做比较。
  
-D或ifdef 此参数的输出格式可用于前置处理器巨集。
  
-e或-ed 此参数的输出格式可用于ed的script文件。
  
-f或-forward-ed 输出的格式类似ed的script文件,但按照原来文件的顺序来显示不同处。
  
-H或-speed-large-files 比较大文件时,可加快速度。
  
-l或-ignore-matching-lines 若两个文件在某几行有所不同,而这几行同时都包含了选项中指定的字符或字符串,则不显示这两个文件的差异。
  
-i或-ignore-case 不检查大小写的不同。

-l或-paginate 将结果交由pr程序来分页。

-n或-rcs 将比较结果以RCS的格式来显示。

-N或-new-file 在比较目录时,若文件A仅出现在某个目录中,预设会显示: Only in目录: 文件A若使用-N参数,则diff会将文件A与一个空白的文件比较。

-p 若比较的文件为C语言的程序码文件时,显示差异所在的函数名称。

-P或-unidirectional-new-file 与-N类似,但只有当第二个目录包含了一个第一个目录所没有的文件时,才会将这个文件与空白的文件做比较。

-s或-report-identical-files 若没有发现任何差异,仍然显示信息。

-S或-starting-file 在比较目录时,从指定的文件开始比较。

-t或-expand-tabs 在输出时,将tab字符展开。

-T或-initial-tab 在每行前面加上tab字符以便对齐。

-u,-U或-unified= 以合并的方式来显示文件内容的不同。

-v或-version 显示版本信息。

-W或-width 在使用-y参数时,指定栏宽。

-X或-exclude-from 您可以将文件或目录类型存成文本文件,然后在=中指定此文本文件。

-y或-side-by-side 以并列的方式显示文件的异同之处。

-help 显示帮助。

-left-column 在使用-y参数时,若两个文件某一行内容相同,则仅在左侧的栏位显示该行内容。

-suppress-common-lines 在使用-y参数时,仅显示不同之处。
  
<http://www.ruanyifeng.com/blog/2012/08/how_to_read_diff.html>
  
<https://superuser.com/questions/644680/how-can-i-make-diff-x-ignore-specific-paths-and-not-file-names>
  
<https://www.cnblogs.com/peida/archive/2012/12/12/2814048.html>

## 上下文格式的 diff

上个世纪80年代初，加州大学伯克利分校推出BSD版本的Unix时，觉得diff的显示结果太简单，最好加入上下文，便于了解发生的变动。因此，推出了上下文格式的diff。

```bash
diff -c f1 f2
```

## 合并格式的 diff

如果两个文件相似度很高，那么上下文格式的 diff， 将显示大量重复的内容， 很浪费空间。 1990年，GNU diff 率先推出了 "合并格式" 的 diff，将 f1 和 f2 的上下文合并在一起显示。

它的使用方法是加入u参数（代表unified）。

```bash
diff -u f1 f2
```

显示结果如下：

```r
　　--- f1 2012-08-29 16:45:41.000000000 +0800
　　+++ f2 2012-08-29 16:45:51.000000000 +0800
　　@@ -1,7 +1,7 @@
　　 a
　　 a
　　 a
　　-a
　　+b
　　 a
　　 a
　　 a
```

它的第一部分，也是文件的基本信息。

```r
　　--- f1 2012-08-29 16:45:41.000000000 +0800
　　+++ f2 2012-08-29 16:45:51.000000000 +0800
```

"---"表示变动前的文件，"+++"表示变动后的文件。

第二部分，变动的位置用两个@作为起首和结束。

>@@ -1,7 +1,7 @@

前面的"-1,7"分成三个部分：减号表示第一个文件（即f1），"1"表示第1行，"7"表示连续7行。合在一起，就表示下面是第一个文件从第1行开始的连续7行。同样的，"+1,7" 表示变动后， 成为第二个文件从第1行开始的连续7行。

第三部分是变动的具体内容。

```r
 a
 a
 a
-a
+b
 a
 a
 a
```

除了有变动的那些行以外，也是上下文各显示3行。它将两个文件的上下文，合并显示在一起，所以叫做"合并格式"。每一行最前面的标志位，空表示无变动，减号表示第一个文件删除的行，加号表示第二个文件新增的行。

在彩色终端里有减号的行显示为红色(删除的行),  有加号的行显示为绿色(新增的行), 没有变动的行显示为白色.

## git 格式的 diff

版本管理系统 git, 使用的是合并格式 diff 的变体.

```bash
git diff f1 f2
```

显示结果如下：

```r
diff --git a/f1 b/f1
index 6f8a38c..449b072 100644
--- a/f1
+++ b/f1
@@ -1,7 +1,7 @@
 a
 a
 a
-a
+b
 a
 a
 a
```

第一行表示结果为 git 格式的 diff。

>diff --git a/f1 b/f1

进行比较的是，a 版本的 f1（即变动前）和 b 版本的 f1（即变动后）。

第二行表示两个版本的 git 哈希值（index 区域的 6f8a38c 对象，与工作目录区域的 449b072 对象进行比较），最后的六位数字是对象的模式（普通文件，644权限）。

>index 6f8a38c..449b072 100644

第三行表示进行比较的两个文件。

```r
　　--- a/f1
　　+++ b/f1
```

"---"表示变动前的版本，"+++"表示变动后的版本。

后面的行都与官方的合并格式 diff 相同。

```r
　　@@ -1,7 +1,7 @@
　　 a
　　 a
　　 a
　　-a
　　+b
　　 a
　　 a
　　 a
```

文档信息
版权声明：自由转载-非商用-非衍生-保持署名（创意共享3.0许可证）
发表日期： 2012年8月29日
作者： 阮一峰
<https://www.ruanyifeng.com/blog/2012/08/how_to_read_diff.html>
