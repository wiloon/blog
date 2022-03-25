---
title: sed
author: "-"
date: 2012-04-07T12:01:31+00:00
url: sed
categories:
  - Linux

tags:
  - reprint
---
## sed 
发音： [sed]  

sed全名叫 stream editor，流编辑器，sed 可以按照脚本的指令来处理文本文件。 简化对文件的反复操作、编写转换程序等
这里的脚本指的是sed脚本，如: 4anewline, 's/hello/world/' ...

### 语法
```bash
sed SCRIPT INPUTFILE
sed [-hnV][-e<script>][-f<script文件>][文本文件]
```

### 选项与参数
    -i : 直接修改读取的文件内容，而不是输出到终端。不加 -i 参数的话默认输出到 STDOUT
    -f : 直接将 sed 的动作写在一个文件内， -f filename 则可以运行 filename 内的 sed 动作；
    -r : sed 的动作支持的是延伸型正规表示法的语法。(默认是基础正规表示法语法)
    -n : 使用安静(silent)模式。在一般 sed 的用法中，所有来自 STDIN 的数据一般都会被列出到终端上。但如果加上 -n 参数后，则只有经过sed 特殊处理的那一行(或者动作)才会被列出来。
    -e script, --expression=script: -e 参数不常用，因为sed 默认把第一个非选项的字符串作为脚本, -e 参数用来显示的指定脚本位置， -e 和 -f 可以同时出现，也可以多次出现, 使用了-e之后，其它非选项字符串都 被认为是输入。
    

### 删除包含指定字符的行
```bash
# 删除包含指定字符的行
sed -i '/localhost/d' /etc/hosts
```

### 截取文本段
<https://blog.wiloon.com/?p=13845>

```bash
# 批量替换目录下所有文件
sed -i 's/old_string/new_string/g'  `grep old_string -rl ./`

# 删除匹配行和匹配行后的2行
sed '/muahao/,+2d' file

# 在匹配行前插入
sed -i '/foo/i\bar' foo.txt

# 在匹配行后追加
sed -i '/foo/a\bar' foo.txt

# 在写脚本的时候方便区分， 可以在i或a后面加一个反斜杠
sed -i '/foo/i\bar' foo.txt
sed -i '/foo/a\bar' foo.txt

# 用sed编辑某一目录下的所有文件
sed -i '/foo/i\bar' `grep foo -rl /path`

# 替换行
# 找出包含xxx的行，并将其中的aaa替换为fff
sed -i '/xxx/s/aaa/fff/g' file

sed  -i 's/properties/property/g'  build.xml

#可以在文件的末尾添加'eof'
sed '$a\eof' test.txt
```

动作说明:  [n1[,n2]]function
  
n1, n2 : 不见得会存在，一般代表『选择进行动作的行数』，举例来说，如果我的动作是需要在 10 到 20 行之间进行的，则『 10,20[动作行为] 』

function: 
  
a : 新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～
  
c : 取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！
  
d : 删除，因为是删除啊，所以 d 后面通常不接任何咚咚；
  
i : 插入， i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)；
  
p : 打印，亦即将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行～
  
s : 取代，可以直接进行取代的工作哩！通常这个 s 的动作可以搭配正规表示法！例如 1,20s/old/new/g 就是啦！

sed: 一个非交互性文本编辑器，它编辑文件或标准输入导出的文件，一次只能处理一行内容。

参数: -n 读取下一个输入行，用下一个命令处理新的行而不是用第一个命令。

Linux 操作系统最大的一个好处是它带有各种各样的实用工具。存在如此之多不同的实用工具，几乎不可能知道并了解所有这些工具。可以简化关键情况下操作的一个实用 工具是 sed。它是任何管理员的工具包中最强大的工具之一，并且可以证明它自己在关键情况下非常有价值。

sed 实用工具是一个"编辑器"，但它与其它大多数编辑器不同。除了不面向屏幕之外，它还是非交互式的。这意味着您必须将要对数据执行的命令插入到命令行或要处 理的脚本中。当显示它时，请忘记您在使用 Microsoft Word 或其它大多数编辑器时拥有的交互式编辑文件功能。sed 在一个文件 (或文件集) 中非交互式、并且不加询问地接收一系列的命令并执行它们。因而，它流经文本就如同水流经溪流一样，因而 sed 恰当地代表了流编辑器。它可以用来将所有出现的 "Mr. Smyth" 修改为 "Mr. Smith"，或将 "tiger cub" 修改为 "wolf cub"。流编辑器非常适合于执行重复的编辑，这种重复编辑如果由人工完成将花费大量的时间。其参数可能和一次性使用一个简单的操作所需的参数一样有限， 或者和一个具有成千上万行要进行编辑修改的脚本文件一样复杂。sed 是 Linux 和 UNIX 工具箱中最有用的工具之一，且使用的参数非常少。

sed 的工作方式

sed 实用工具按顺序逐行将文件读入到内存中。然后，它执行为该行指定的所有操作，并在完成请求的修改之后将该行放回到内存中，以将其转储至终端。完成了这一行 上的所有操作之后，它读取文件的下一行，然后重复该过程直到它完成该文件。如同前面所提到的，默认输出是将每一行的内容输出到屏幕上。在这里，开始涉及到 两个重要的因素—首先，输出可以被重定向到另一文件中，以保存变化；第二，源文件 (默认地) 保持不被修改。sed 默认读取整个文件并对其中的每一行进行修改。不过，可以按需要将操作限制在指定的行上。
  动作说明:  [n1[,n2]]function n1, n2 : 不见得会存在，一般代表『选择进行动作的行数』，举例来说，如果我的动作是需要在 10 到 20 行之间进行的，则『 10,20[动作行为] 』 function:  a : 新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～ c : 取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！ d : 删除，因为是删除啊，所以 d 后面通常不接任何命令 i : 插入， i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)； p : 列印，亦即将某个选择的数据印出。通常 p 会与参数 sed -n 一起运行～ s : 取代，可以直接进行取代的工作哩！通常这个 s 的动作可以搭配正规表示法！例如 1,20s/old/new/g

以行为单位的新增/删除

nl /etc/passwd | sed '2,5d'

http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2856901.html
  
http://wiki.jikexueyuan.com/project/shell-learning/sed-search-and-replace.html

```bash
cat *.csv >out
sed -e 's/^M//g' out > foo
cat foo | python -c "import sys; print sys.stdin.read().replace('.\n','.')" > bar
cat bar|sort >s

```

http://www.gnu.org/software/sed/manual/sed.html


  
### sed 简明教程
>https://coolshell.cn/articles/9104.html/embed#?secret=6JIFuxVo3p
  
https://www.gnu.org/software/sed/manual/sed.html
### linux下在某行的前一行或后一行添加内容
>http://www.361way.com/sed-process-lines/2263.html/embed#?secret=0mIvKAwlT1
  
https://www.cnblogs.com/muahao/p/6290813.html

  
a: 新增，例如: nl /etc/passwd | sed '2a Hello World'，在/etc/passwd第2行下面新增一行，写入"Hello World"。
  
i: 插入，例如: nl /etc/passwd | sed '2i Hello World'，在/etc/passwd第2行上面新增一行，写入"Hello World"
  
c: 替换，例如: nl /etc/passwd | sed '2,5c Hello World'，将/etc/passwd第2至5行的内容替换为"Hello Wolrd"。
  
d: 删除，例如: nl /etc/passwd | sed '2,5d'，删除/etc/passwd中的第2至5行。
  
p: 打印，例如: nl -n /etc/passwd | sed '2,5p'，仅显示2到5行，注意，如果不加-n，2到5行将重复输出。
  
s: 搜索，例如: nl /etc/passwd | sed '1,20s/old/new/g'，将第1~20行中出现的所有字符串old替换为new。


>https://www.gnu.org/software/sed/manual/sed.html