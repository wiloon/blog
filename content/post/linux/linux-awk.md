---
title: awk command
author: "-"
date: 2012-07-05T04:54:22+00:00
url: awk
categories:
  - Linux
tags:
  - reprint
  - remix
---
## awk command

## awk `[ɔk]`

### commands

```bash
# 单独使用 awk, 不需要 cat
awk  '{print $1}' /tmp/foo.txt
cat dep-clean|awk -F '@' '{if(NF>2){print "\"""@"$2"\""":"$3} else {pint $1":"$2}}'
cat dep-clean|awk -F '@' '{if(NF<3){print "\""$1"\""":"$2}}'
cat dep-clean|awk -F '@' '{if(NF>2){print "\"""@"$2"\""":"$3} else if (NF<3) {print $1":"$2}}'
# kill all java process
ps -ef |grep java|awk '{print $2}'|xargs -t -n 1 kill -9
# 取本机ip >https://www.cnblogs.com/poloyy/p/12212868.html
ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}'
```

### 变量

除了$ + 数字表示某个字段，awk还提供其他一些变量。

变量NF表示当前行有多少个字段，因此$NF就代表最后一个字段。

### AWK

AWK是贝尔实验室1977年搞出来的文本处理神器
  
之所以叫AWK是因为其取了三位创始人 Alfred Aho，Peter Weinberger, 和 Brian Kernighan 的Family Name的首字符

```bash
cat foo.log| awk -F 'data:' '{print $2}'
```

### 字段非空

```bash
awk '{if(NR>3 && $2 != "") {print $2}}'|sort -u
```

### awk输出单引号，双引号

双引号:

```bash
awk '{print "\""}'
```

使用""双引号把一个双引号括起来，然后用转义字符\对双引号进行转义，输出双引号。

单引号:

```bash
awk '{print "'\''"}'
```

使用一个双引号""，然后在双引号里面加入两个单引号''，接着在两个单引号里面加入一个转义的单引号\'，输出单引号。

### 多个分隔符

关于多个分割符号:
  
1. awk -F ',' 表示使用逗号多分隔符
2. awk -F 'AB' 表示使用符号AB做分隔符 echo ABCDABDDCADAFB | awk -F 'AB' '{for(i=1;i<=NF;i++)printf $i" "}'输出 CD DDCADAFB
3. awk -F '[AB]' 表示使用A或者B做分隔符，就是遇到字符A或者B都分割 echo ABCDABDDCADAFB | awk -F '[AB]' '{for(i=1;i<=NF;i++)printf $i" "}' 输出 CD DDC D F
4. awk -F '[&#92;|]' 表示使用符号'|'做分隔符，这里有两层转义，先转义\,然后转义|。
5. echo "ABC|DAB|DD CA DAFB" | awk -F '[ &#92;|]' '{for(i=1;i<=NF;i++)printf $i" "}' 输出 ABC DAB DD CA DAFB
6. print打印会换行，printf打印不换行

```bash
echo "i have two apples and one banana" | awk -F'one|two' '{for(i=1;i<=NF;i++)print i,"="$i}'
# 1 =i have
# 2 = apples and
# 3 = banana
```

### substr

```bash
substr($4,20)    --->  表示是从第4个字段里的第20个字符开始，一直到设定的分隔符","结束.
substr($3,12,8)  --->  表示是从第3个字段里的第12个字符开始，截取8个字符结束.
substr($3,6)     --->  表示是从第3个字段里的第6个字符开始，一直到设定的分隔.
```

```bash
tail -n 10000 info.log | grep 'xxx.*Unknown.*LF'|awk -F 'Unk|:L' '{print substr($2,14,7),substr($3,0,16)}'
```

### 统计

```bash
# 求和
cat data|awk '{sum+=$1} END {print "Sum = ", sum}'
cat foo.txt |awk '{sum+=$1} END {print "sum = ", sum}'

# 平均
grep '1-min rate' *.log  |awk -F ' ' '{sum+=$7} END {print "Average = ", sum/NR}'
#最大值
grep '1-min rate' *.log  |awk -F ' '  'BEGIN {max = 0} {if ($7>max) max=$7 fi} END {print "Max=", max}'
#最小值
grep '1-min rate' *.log  |awk -F ' '  'BEGIN {min = 1999999} {if ($7<min) min=$7 fi} END {print "Min=", min}'
```

awk: 一种编程语言，用于在 linux/unix 下对文本和数据进行处理。数据可以来自标准输入、一个或多个文件，或其它命令的输出。它支持用户自定义函数和动态正则表达式等先进功能，是 linux/unix 下的一个强大编程工具。它在命令行中使用，但更多是作为脚本来使用。awk 的处理文本和数据的方式: 它逐行扫描文件，从第一行到最后一行，寻找匹配的特定模式的行，并在这些行上进行你想要的操作。如果没有指定处理动作，则把匹配的行显示到标准输出 ( 屏幕 )，如果没有指定模式，则所有被操作所指定的行都被处理。
  
参数: -F fs or -field-separator fs : 指定输入文件折分隔符，fs 是一个字符串或者是一个正则表达式，如 -F:。

awk是一个强大的文本分析工具，相对于grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。简单来说awk就是把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。

awk有3个不同版本: awk、nawk和gawk，未作特别说明，一般指gawk，gawk 是 AWK 的 GNU 版本。

awk其名称得自于它的创始人 Alfred Aho 、Peter Weinberger 和 Brian Kernighan 姓氏的首个字母。实际上 AWK 的确拥有自己的语言:  AWK 程序设计语言 ， 三位创建者已将它正式定义为"样式扫描和处理语言"。它允许您创建简短的程序，这些程序读取输入文件、为数据排序、处理数据、对输入执行计算以及生成报表，还有无数其他的功能。

使用方法
  
awk '{pattern + action}' {filenames}
  
尽管操作可能会很复杂，但语法总是这样，其中 pattern 表示 AWK 在数据中查找的内容，而 action 是在找到匹配内容时所执行的一系列命令。花括号 ({}) 不需要在程序中始终出现，但它们用于根据特定的模式对一系列指令进行分组。 pattern就是要表示的正则表达式，用斜杠括起来。

awk语言的最基本功能是在文件或者字符串中基于指定规则浏览和抽取信息，awk抽取信息后，才能进行其他文本操作。完整的awk脚本通常用来格式化文本文件中的信息。

通常，awk是以文件的一行为处理单位的。awk每接收文件的一行，然后执行相应的命令，来处理文本。

调用awk
  
有三种方式调用awk
  
1.命令行方式
  
awk [-F field-separator] 'commands' input-file(s)
  
其中，commands 是真正awk命令，[-F域分隔符]是可选的。 input-file(s) 是待处理的文件。
  
在awk中，文件的每一行中，由域分隔符分开的每一项称为一个域。通常，在不指名-F域分隔符的情况下，默认的域分隔符是空格。

2.shell脚本方式
  
将所有的awk命令插入一个文件，并使awk程序可执行，然后awk命令解释器作为脚本的首行，一遍通过键入脚本名称来调用。
  
相当于shell脚本首行的: #!/bin/sh
  
可以换成: #!/bin/awk

3.将所有的awk命令插入一个单独文件，然后调用:
  
awk -f awk-script-file input-file(s)
  
其中，-f选项加载awk-script-file中的awk脚本，input-file(s)跟上面的是一样的。

本章重点介绍命令行方式。

入门实例
  
假设last -n 5的输出如下

[root@www ~]# last -n 5 <==仅取出前五行
  
root pts/1 192.168.1.100 Tue Feb 10 11:21 still logged in
  
root pts/1 192.168.1.100 Tue Feb 10 00:46 - 02:28 (01:41)
  
root pts/1 192.168.1.100 Mon Feb 9 11:41 - 18:30 (06:48)
  
dmtsai pts/1 192.168.1.100 Mon Feb 9 11:41 - 11:41 (00:00)
  
root tty1 Fri Sep 5 14:09 - 14:10 (00:01)
  
如果只是显示最近登录的5个帐号

# last -n 5 | awk '{print $1}'
  
root
  
root
  
root
  
dmtsai
  
root
  
awk工作流程是这样的: 读入有'\n'换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0则表示所有域,$1表示第一个域,$n表示第n个域。默认域分隔符是"空白键" 或 "[tab]键",所以$1表示登录用户，$3表示登录用户ip,以此类推。

如果只是显示/etc/passwd的账户

# cat /etc/passwd |awk -F ':' '{print $1}'
  
root
  
daemon
  
bin
  
sys
  
这种是awk+action的示例，每行都会执行action{print $1}。

-F指定域分隔符为':'。

如果只是显示/etc/passwd的账户和账户对应的shell,而账户与shell之间以tab键分割

# cat /etc/passwd |awk -F ':' '{print $1"\t"$7}'
  
root /bin/bash
  
daemon /bin/sh
  
bin /bin/sh
  
sys /bin/sh
  
如果只是显示/etc/passwd的账户和账户对应的shell,而账户与shell之间以逗号分割,而且在所有行添加列名name,shell,在最后一行添加"blue,/bin/nosh"。
  
cat /etc/passwd |awk -F ':' 'BEGIN {print "name,shell"} {print $1","$7} END {print "blue,/bin/nosh"}'
  
name,shell
  
root,/bin/bash
  
daemon,/bin/sh
  
bin,/bin/sh
  
sys,/bin/sh
  
....
  
blue,/bin/nosh

awk工作流程是这样的: 先执行BEGING，然后读取文件，读入有/n换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0则表示所有域,$1表示第一个域,$n表示第n个域,随后开始执行模式所对应的动作action。接着开始读入第二条记录······直到所有的记录都读完，最后执行END操作。

搜索/etc/passwd有root关键字的所有行

# awk -F: '/root/' /etc/passwd
  
root:x:0:0:root:/root:/bin/bash
  
这种是pattern的使用示例，匹配了pattern(这里是root)的行才会执行action(没有指定action，默认输出每行的内容)。

搜索支持正则，例如找root开头的: awk -F: '/^root/' /etc/passwd

搜索/etc/passwd有root关键字的所有行，并显示对应的shell

# awk -F: '/root/{print $7}' /etc/passwd

/bin/bash
  
这里指定了action{print $7}

awk内置变量
  
awk有许多内置变量用来设置环境信息，这些变量可以被改变，下面给出了最常用的一些变量。
  
ARGC 命令行参数个数
  
ARGV 命令行参数排列
  
ENVIRON 支持队列中系统环境变量的使用
  
FILENAME awk浏览的文件名
  
FNR 浏览文件的记录数
  
FS 设置输入域分隔符，等价于命令行 -F选项
  
NF 浏览记录的域的个数
  
NR 已读的记录数
  
OFS 输出域分隔符
  
ORS 输出记录分隔符
  
RS 控制记录分隔符

此外,$0变量是指整条记录。$1表示当前行的第一个域,$2表示当前行的第二个域,......以此类推。

统计/etc/passwd:文件名，每行的行号，每行的列数，对应的完整行内容:

# awk -F ':' '{print "filename:" FILENAME ",linenumber:" NR ",columns:" NF ",linecontent:"$0}' /etc/passwd
  
filename:/etc/passwd,linenumber:1,columns:7,linecontent:root:x:0:0:root:/root:/bin/bash
  
filename:/etc/passwd,linenumber:2,columns:7,linecontent:daemon:x:1:1:daemon:/usr/sbin:/bin/sh
  
filename:/etc/passwd,linenumber:3,columns:7,linecontent:bin:x:2:2:bin:/bin:/bin/sh
  
filename:/etc/passwd,linenumber:4,columns:7,linecontent:sys:x:3:3:sys:/dev:/bin/sh
  
使用printf替代print,可以让代码更加简洁，易读

awk -F ':' '{printf("filename:%10s,linenumber:%s,columns:%s,linecontent:%s\n",FILENAME,NR,NF,$0)}' /etc/passwd
  
print和printf
  
awk中同时提供了print和printf两种打印输出的函数。

其中print函数的参数可以是变量、数值或者字符串。字符串必须用双引号引用，参数用逗号分隔。如果没有逗号，参数就串联在一起而无法区分。这里，逗号的作用与输出文件的分隔符的作用是一样的，只是后者是空格而已。

printf函数，其用法和c语言中printf基本相似,可以格式化字符串,输出复杂时，printf更加好用，代码更易懂。

awk编程
  
变量和赋值

除了awk的内置变量，awk还可以自定义变量。

下面统计/etc/passwd的账户人数

awk '{count++;print $0;} END{print "user count is ", count}' /etc/passwd
  
root:x:0:0:root:/root:/bin/bash
  
......
  
user count is  40

count是自定义变量。之前的action{}里都是只有一个print,其实print只是一个语句，而action{}可以有多个语句，以;号隔开。

这里没有初始化count，虽然默认是0，但是妥当的做法还是初始化为0:

awk 'BEGIN {count=0;print "[start]user count is ", count} {count=count+1;print $0;} END{print "[end]user count is ", count}' /etc/passwd
  
[start]user count is 0
  
root:x:0:0:root:/root:/bin/bash
  
...
  
[end]user count is 40
  
统计某个文件夹下的文件占用的字节数

ls -l |awk 'BEGIN {size=0;} {size=size+$5;} END{print "[end]size is ", size}'
  
[end]size is  8657198

如果以M为单位显示:

ls -l |awk 'BEGIN {size=0;} {size=size+$5;} END{print "[end]size is ", size/1024/1024,"M"}'
  
[end]size is  8.25889 M
  
注意，统计不包括文件夹的子目录。

条件语句

awk中的条件语句是从C语言中借鉴来的，见如下声明方式:
  
if (expression) {
  
statement;
  
statement;
  
... ...
  
}

if (expression) {
  
statement;
  
} else {
  
statement2;
  
}

if (expression) {
  
statement1;
  
} else if (expression1) {
  
statement2;
  
} else {
  
statement3;
  
}

统计某个文件夹下的文件占用的字节数,过滤4096大小的文件(一般都是文件夹):

ls -l |awk 'BEGIN {size=0;print "[start]size is ", size} {if($5!=4096){size=size+$5;}} END{print "[end]size is ", size/1024/1024,"M"}'
  
[end]size is  8.22339 M
  
循环语句

awk中的循环语句同样借鉴于C语言，支持while、do/while、for、break、continue，这些关键字的语义和C语言中的语义完全相同。

数组

因为awk中数组的下标可以是数字和字母，数组的下标通常被称为关键字(key)。值和关键字都存储在内部的一张针对key/value应用hash的表格里。由于hash不是顺序存储，因此在显示数组内容时会发现，它们并不是按照你预料的顺序显示出来的。数组和变量一样，都是在使用时自动创建的，awk也同样会自动判断其存储的是数字还是字符串。一般而言，awk中的数组用来从记录中收集信息，可以用于计算总和、统计单词以及跟踪模板被匹配的次数等等。

显示/etc/passwd的账户
  
awk -F ':' 'BEGIN {count=0;} {name[count] = $1;count++;}; END{for (i = 0; i < NR; i++) print i, name[i]}' /etc/passwd
  
0 root
  
1 daemon
  
2 bin
  
3 sys
  
4 sync
  
5 games
  
......

这里使用for循环遍历数组

## awk的流程控制BEGIN和END

BEGIN模块后紧跟着动作块，这个动作块在awk处理任何输入文件之前执行。所以它可以在没有任何输入的情况下进行测试。它通常用来改变内建变量的值，如OFS,RS和FS等，以及打印标题。如: $ awk'BEGIN{FS=":"; OFS="\t"; ORS="\n\n"}{print $1,$2,$3} test。上式表示，在处理输入文件以前，域分隔符(FS)被设为冒号，输出文件分隔符(OFS)被设置为制表符，输出记录分隔符(ORS)被设置为两个换行符。$ awk 'BEGIN{print "TITLE TEST"}只打印标题.

END不匹配任何的输入文件，但是执行动作块中的所有动作，它在整个输入文件处理完成后被执行。如$ awk 'END{print "The number of records is" NR}' test，上式将打印所有被处理的记录数。

如何把一行竖排的数据转换成横排？

awk '{printf("%s,",$1)}' filename

awk 'BEGIN {FS=":";OFS=":"} gsub(/root/,"hwl",$1) {print $0}' passwd 作用于域t
  
awk 'BEGIN {FS=":";OFS=":"} gsub(/root/,"hwl") {print $0}' passwd 作用于全部域

# awk 'BEGIN {FS=":";OFS=":"} sub(/root/,"hwl",$6) {print $0}' passwd 将t中第一次出现的r替换为s

在Unix awk中两个特别的表达式，BEGIN和END，这两者都可用于pattern中 (参考前面的awk语法) ，提供BEGIN和END的作用是给程序赋予初始状态和在程序结束之后执行一些扫尾的工作。

任何在BEGIN之后列出的操作 (在{}内) 将在Unix awk开始扫描输入之前执行，而END之后列出的操作将在扫描完全部的输入之后执行。因此，通常使用BEGIN来显示变量和预置 (初始化) 变量，使用END来输出最终结果。

# !/bin/awk -f

# 运行前

BEGIN {
    printf "begin0\n"
    FS="Unk|:L"
}

# 运行中

{
    {printf "%s L%s\n", substr($2,14,4),substr($3,0,16)}
}

# 运行后

END {
    printf "---------------------------------------------\n"
}

```

https://blog.51cto.com/151wqooo/1309851
  
http://www.gnu.org/software/gawk/manual/gawk.html


  
    AWK 简明教程
  


https://coolshell.cn/articles/9070.html/embed#?secret=7pUo5sdZvt
  
http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2858470.html
  
https://blog.51cto.com/jschu/1770467
  
https://my.oschina.net/xiangtao/blog/751625
