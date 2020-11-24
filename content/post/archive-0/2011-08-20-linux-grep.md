---
title: grep
author: w1100n
type: post
date: 2011-08-20T20:00:03+00:00
url: /?p=468
categories:
  - Linux

---
grep, Global Regular Expression Print

```bash
grep xxx -A5
grep xxx -B1
grep -C 5 foo file 显示file文件里匹配foo字串那行以及上下5行

#regex
grep ".*A.*" foo.txt
grep "foo\|bar" foo.txt

# -r: 搜索子目录
# -l: 查询多文件时只输出包含匹配字符的文件名.

# 统计某个字符串出现的次数
grep -o objStr  filename|wc -l
```

  * -A, –after-context=NUM print NUM lines of trailing context
  * -B <显示行数> -before-context=<显示行数> #除了显示符合样式的那一行之外，并显示该行之前的内容。
  * -C 显示file文件里匹配foo字串那行以及上下5行
  * -r, -recursive
  * -l, -files-with-matches
  * -G, -basic-regexp BRE 模式，也是默认的模式
  * -E, -extended-regexp ERE 模式
  * -h, 查询多文件时不显示文件名。
  * -a, --text: 强制作为文本文件处理， 报错：Binary file [some_file] matches 的时候可以用。

BRE(basic regular expression)

ERE(extended regular expression)
  
与 BRE 相比 ERE 最大的优点是支持更多的元字符，也就是在使用这些字符时不需要 \ 了。比如上面 BRE 中使用的 \ 符可以全部去掉。

1.作用
  
Linux系统中grep命令是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹 配的行打印出来。grep全称是Global Regular Expression Print，表示全局正则表达式版本，它的使用权限是所有用户。

2.格式
  
grep [options]

3.主要参数
  
[options]主要参数：

－c：只输出匹配行的计数。

－v：显示不包含匹配文本的所有行。
  
－I：不区分大 小写(只适用于单字符)。

－l：查询多文件时只输出包含匹配字符的文件名。
  
－n：显示匹配行及 行号。
  
－s：不显示不存在或无匹配文本的错误信息。

pattern正则表达式主要参数：
  
\： 忽略正则表达式中特殊字符的原有含义。
  
^：匹配正则表达式的开始行。
  
$: 匹配正则表达式的结束行。
  
\<：从匹配正则表达 式的行开始。
  
>：到匹配正则表达式的行结束。
  
[ ]：单个字符，如[A]即A符合要求.
  
[ – ]：范围，如[A-Z]，即A、B、C一直到Z都符合要求 。
  
。：所有的单个字符。
  
* ：有字符，长度可以为0。

4.grep命令使用简单实例
  
$ grep 'test' d*
  
显示所有以d开头的文件中包含 test的行。
  
$ grep 'test' aa bb cc
  
显示在aa，bb，cc文件中匹配test的行。
  
$ grep '[a-z]{5}' aa
  
显示所有包含每个字符串至少有5个连续小写字符的字符串的行。
  
$ grep 'w(es)t._\1′ aa
  
如果west被匹配，则es就被存储到内存中，并标记为1，然后搜索任意个字符(._)，这些字符后面紧跟着 另外一个es(\1)，找到就显示该行。如果用egrep或grep -E，就不用"\"号进行转义，直接写成'w(es)t.*\1′就可以了。

5.grep命令使用复杂实例
  
假设您正在'/usr/src/Linux/Doc'目录下搜索带字符 串'magic'的文件：
  
$ grep magic /usr/src/Linux/Doc/*
  
sysrq.txt:* How do I enable the magic SysRQ key?
  
sysrq.txt:* How do I use the magic SysRQ key?
  
其中文件'sysrp.txt'包含该字符串，讨论的是 SysRQ 的功能。
  
默认情况下，'grep'只搜索当前目录。如果 此目录下有许多子目录，'grep'会以如下形式列出：
  
grep: sound: Is a directory
  
这可能会使'grep' 的输出难于阅读。这里有两种解决的办法：
  
明确要求搜索子目录：grep -r
  
或忽略子目录：grep -d skip
  
如果有很多 输出时，您可以通过管道将其转到'less'上阅读：
  
$ grep magic /usr/src/Linux/Documentation/* | less
  
这样，您就可以更方便地阅读。

有一点要注意，您必需提供一个文件过滤方式(搜索全部文件的话用 *)。如果您忘了，'grep'会一直等着，直到该程序被中断。如果您遇到了这样的情况，按 <CTRL c> ，然后再试。

下面还有一些有意思的命令行参数：
  
grep -i pattern files ：不区分大小写地搜索。默认情况区分大小写，
  
grep -l pattern files ：只列出匹配的文件名，
  
grep -L pattern files ：列出不匹配的文件名，
  
grep -w pattern files ：只匹配整个单词，而不是字符串的一部分(如匹配'magic'，而不是'magical')，
  
grep -C number pattern files ：匹配的上下文分别显示[number]行，
  
grep pattern1 | pattern2 files ：显示匹配 pattern1 或 pattern2 的行，
  
grep pattern1 files | grep pattern2 ：显示既匹配 pattern1 又匹配 pattern2 的行。

grep -n pattern files 即可显示行号信息

grep -c pattern files 即可查找总行数

这里还有些用于搜索的特殊符号：
  
\< 和 > 分别标注单词的开始与结尾。
  
例如：
  
grep man * 会匹配 'Batman'、'manic'、'man'等，
  
grep '\<man' * 匹配'manic'和'man'，但不是'Batman'，
  
grep '\<man>' 只匹配'man'，而不是'Batman'或'manic'等其他的字符串。
  
'^'：指匹配的字符串在行首，
  
'$'：指匹配的字符串在行 尾，

Grep 命令 用法大全

1、 参数：
  
-I ：忽略大小写
  
-c ：打印匹配的行数
  
-l ：从多个文件中查找包含匹配项
  
-v ：查找不包含匹配项的行
  
-n：打印包含匹配项的行和行标

2、RE（正则表达式）
  
\ 忽略正则表达式中特殊字符的原有含义
  
^ 匹配正则表达式的开始行
  
$ 匹配正则表达式的结束行
  
\< 从匹配正则表达式的行开始
  
> 到匹配正则表达式的行结束
  
[ ] 单个字符；如[A] 即A符合要求
  
[ – ] 范围 ；如[A-Z]即A，B，C一直到Z都符合要求
  
. 所有的单个字符
  
* 所有字符，长度可以为0

3、举例

# ps -ef | grep in.telnetd

root 19955 181 0 13:43:53 ? 0:00 in.telnetd

# more size.txt size文件的内容

b124230
  
b034325
  
a081016
  
m7187998
  
m7282064
  
a022021
  
a061048
  
m9324822
  
b103303
  
a013386
  
b044525
  
m8987131
  
B081016
  
M45678
  
B103303
  
BADc2345

# more size.txt | grep '[a-b]' 范围 ；如[A-Z]即A，B，C一直到Z都符合要求

b124230
  
b034325
  
a081016
  
a022021
  
a061048
  
b103303
  
a013386
  
b044525

# more size.txt | grep '[a-b]'*

b124230
  
b034325
  
a081016
  
m7187998
  
m7282064
  
a022021
  
a061048
  
m9324822
  
b103303
  
a013386
  
b044525
  
m8987131
  
B081016
  
M45678
  
B103303
  
BADc2345

# more size.txt | grep 'b' 单个字符；如[A] 即A符合要求

b124230
  
b034325
  
b103303
  
b044525

# more size.txt | grep '[bB]'

b124230
  
b034325
  
b103303
  
b044525
  
B081016
  
B103303
  
BADc2345

# grep 'root' /etc/group

root::0:root
  
bin::2:root,bin,daemon
  
sys::3:root,bin,sys,adm
  
adm::4:root,adm,daemon
  
uucp::5:root,uucp
  
mail::6:root
  
tty::7:root,tty,adm
  
lp::8:root,lp,adm
  
nuucp::9:root,nuucp
  
daemon::12:root,daemon

# grep '^root' /etc/group 匹配正则表达式的开始行

root::0:root

# grep 'uucp' /etc/group

uucp::5:root,uucp
  
nuucp::9:root,nuucp

# grep '\<uucp' /etc/group

uucp::5:root,uucp

# grep 'root$' /etc/group 匹配正则表达式的结束行

root::0:root
  
mail::6:root

# more size.txt | grep -i 'b1..*3' -i ：忽略大小写

b124230
  
b103303
  
B103303

# more size.txt | grep -iv 'b1..*3' -v ：查找不包含匹配项的行

b034325
  
a081016
  
m7187998
  
m7282064
  
a022021
  
a061048
  
m9324822
  
a013386
  
b044525
  
m8987131
  
B081016
  
M45678
  
BADc2345

# more size.txt | grep -in 'b1..*3'

1:b124230
  
9:b103303
  
15:B103303

# grep '$' /etc/init.d/nfs.server | wc -l

128

# grep '\$' /etc/init.d/nfs.server | wc –l 忽略正则表达式中特殊字符的原有含义

15

# grep '\$' /etc/init.d/nfs.server

case "$1" in

> /tmp/sharetab.$$
    
> [ "x$fstype" != xnfs ] &&
    
> echo "$path\t$res\t$fstype\t$opts\t$desc"
> 
> > /tmp/sharetab.$$
      
> > /usr/bin/touch -r /etc/dfs/sharetab /tmp/sharetab.$$
      
> > /usr/bin/mv -f /tmp/sharetab.$$ /etc/dfs/sharetab
      
> > if [ -f /etc/dfs/dfstab ] && /usr/bin/egrep -v '^[ ]*(#|$)'
      
> > if [ $startnfsd -eq 0 -a -f /etc/rmmount.conf ] &&
      
> > if [ $startnfsd -ne 0 ]; then
      
> > elif [ ! -n "$\_INIT\_RUN_LEVEL" ]; then
      
> > while [ $wtime -gt 0 ]; do
      
> > wtime=`expr $wtime – 1`
      
> > if [ $wtime -eq 0 ]; then
      
> > echo "Usage: $0 { start | stop }" 

# more size.txt

the test file
  
their are files
  
The end

# grep 'the' size.txt

the test file
  
their are files

# grep '\<the' size.txt

the test file
  
their are files

# grep 'the>' size.txt

the test file

# grep '\<the>' size.txt

the test file

# grep '\<[Tt]he>' size.txt

the test file

==================================================================

1,简介
  
使用正则表达式的一个多用途文本搜索工具.这个php?name=%C3%FC%C1%EE" onclick="tagshow(event)" class="t\_tag">命令本来是ed行编辑器中的一个php?name=%C3%FC%C1%EE" onclick="tagshow(event)" class="t\_tag">命令/过滤器:
  
g/re/p — global – regular expression – print.
  
基本格式
  
grep pattern [file…]
  
(1)grep 搜索字符串 [filename]
  
(2)grep 正则表达式 [filename]
  
在文件中搜索所有 pattern 出现的位置, pattern 既可以是要搜索的字符串,也可以是一个正则表达式.
  
注意：在输入要搜索的字符串时最好使用双引号/而在模式匹配使用正则表达式时，注意使用单引号

2,grep的选项
  
-c 只输出匹配行的计数
  
-i 不区分大小写（用于单字符）
  
-n 显示匹配的行号
  
-v 不显示不包含匹配文本的所以有行
  
-s 不显示错误信息
  
-E 使用扩展正则表达式
  
更多的选项请查看：man grep

3,常用grep实例

(1)多个文件查询
  
grep "sort" *.doc #见文件名的匹配

(2)行匹配:输出匹配行的计数
  
grep -c "48" data.doc #输出文档中含有48字符的行数

(3)显示匹配行和行数
  
grep -n "48" data.doc #显示所有匹配48的行和行号

(4)显示非匹配的行
  
grep -vn "48" data.doc #输出所有不包含48的行

(4)显示非匹配的行
  
grep -vn "48" data.doc #输出所有不包含48的行

(5)大小写敏感
  
grep -i "ab" data.doc #输出所有含有ab或Ab的字符串的行

4, 正则表达式的应用

(1)正则表达式的应用 (注意：最好把正则表达式用单引号括起来)
  
grep '[239].' data.doc #输出所有含有以2,3或9开头的，并且是两个数字的行

(2)不匹配测试
  
grep '^[^48]' data.doc #不匹配行首是48的行

(3)使用扩展模式匹配
  
grep -E '219|216' data.doc

(4) …
  
这需要在实践中不断应用和总结，熟练掌握正则表达式。

5, 使用类名
  
可以使用国际模式匹配的类名：
  
\[[:upper:]\] \[A-Z\]
  
\[[:lower:]\] \[a-z\]
  
\[[:digit:]\] \[0-9\]
  
\[[:alnum:]\] \[0-9a-zA-Z\]
  
[[:space:]] 空格或tab
  
\[[:alpha:]\] \[a-zA-Z\]

(1)使用
  
grep '5\[[:upper:]\]\[[:upper:\]]' data.doc #查询以5开头以两个大写字母结尾的行

<ol start="5">
  <li>
    Grep命令选项
 -?
 同时显示匹配行上下的？行，如：grep -2 pattern filename同时显示匹配行的上下2行。
 -b，–byte-offset
 打印匹配行前面打印该行所在的块号码。
 -c,–count
 只打印匹配的行数，不显示匹配的内容。
 -f File，–file=File
 从文件中提取模板。空文件中包含0个模板，所以什么都不匹配。
 -h，–no-filename
 当搜索多个文件时，不显示匹配文件名前缀。
 -i，–ignore-case
 忽略大小写差别。
 -q，–quiet
 取消显示，只返回退出状态。0则表示找到了匹配的行。
 -l，–files-with-matches
 打印匹配模板的文件清单。
 -L，–files-without-match
 打印不匹配模板的文件清单。
 -n，–line-number
 在匹配的行前面打印行号。
 -s，–silent
 不显示关于不存在或者无法读取文件的错误信息。
 -v，–revert-match
 反检索，只显示不匹配的行。
 -w，–word-regexp
 如果被引用，就把表达式做为一个单词搜索。
 -V，–version
 显示软件版本信息。
  </li>
  <li>
    
      grep简介
    
  </li>
</ol>

grep （global search regular expression(RE) and print out the line,全面搜索正则表达式并把行打印出来）是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹配的行打印出来。Unix的grep家族包括grep、egrep和fgrep。egrep和fgrep的命令只跟grep有很小不同。egrep是grep的扩展，支持更多的re元字符， fgrep就是fixed grep或fast grep，它们把所有的字母都看作单词，也就是说，正则表达式中的元字符表示回其自身的字面意义，不再特殊。Linux使用GNU版本的grep。它功能更强，可以通过-G、-E、-F命令行选项来使用egrep和fgrep的功能。

grep的工作方式是这样的，它在一个或多个文件中搜索字符串模板。如果模板包括空格，则必须被引用，模板后的所有字符串被看作文件名。搜索的结果被送到屏幕，不影响原文件内容。

grep可用于shell脚本，因为grep通过返回一个状态值来说明搜索的状态，如果模板搜索成功，则返回0，如果搜索不成功，则返回1，如果搜索的文件不存在，则返回2。我们利用这些返回值就可进行一些自动化的文本处理工作。

<ol start="2">
  <li>
    grep正则表达式元字符集（基本集）
 ^
 锚定行的开始 如：'^grep'匹配所有以grep开头的行。
 $
 锚定行的结束 如：'grep$'匹配所有以grep结尾的行。
 匹配一个非换行符的字符 如：'gr.p'匹配gr后接一个任意字符，然后是p。
 *
 匹配零个或多个先前字符 如：'<em>grep'匹配所有一个或多个空格后紧跟grep的行。 .</em>一起用代表任意字符。
 []
 匹配一个指定范围内的字符，如'[Gg]rep'匹配Grep和grep。
 [^]
 匹配一个不在指定范围内的字符，如：'[^A-FH-Z]rep'匹配不包含A-R和T-Z的一个字母开头，紧跟rep的行。
 (..)
 标记匹配字符，如'(love)'，love被标记为1。
 <
 锚定单词的开始，如:'>
 锚定单词的结束，如'grep>'匹配包含以grep结尾的单词的行。
 x
 重复字符x，m次，如：'0'匹配包含5个o的行。
 x
 重复字符x,至少m次，如：'o'匹配至少有5个o的行。
 x
 重复字符x，至少m次，不多于n次，如：'o'匹配5–10个o的行。
 w
 匹配文字和数字字符，也就是[A-Za-z0-9]，如：'Gw*p'匹配以G后跟零个或多个文字或数字字符，然后是p。
 W
 w的反置形式，匹配一个或多个非单词字符，如点号句号等。
 b
 单词锁定符，如: 'bgrepb'只匹配grep。
  </li>
  <li>
    用于egrep和 grep -E的元字符扩展集
 +
 匹配一个或多个先前的字符。如：'[a-z]+able'，匹配一个或多个小写字母后跟able的串，如loveable,enable,disable等。
 ?
 匹配零个或多个先前的字符。如：'gr?p'匹配gr后跟一个或没有字符，然后是p的行。
 a|b|c
 匹配a或b或c。如：grep|sed匹配grep或sed
 ()
 分组符号，如：love(able|rs)ov+匹配loveable或lovers，匹配一个或多个ov。
 x,x,x
 作用同x,x,x
  </li>
  <li>
    
      POSIX字符类
 为了在不同国家的字符编码中保持一至，POSIX(The Portable Operating System Interface)增加了特殊的字符类，如[:alnum:]是A-Za-z0-9的另一个写法。要把它们放到[]号内才能成为正则表达式，如[A- Za-z0-9]或[[:alnum:]]。在Linux下的grep除fgrep外，都支持POSIX的字符类。
 [:alnum:]
 文字数字字符
 [:alpha:]
 文字字符
 [:digit:]
 数字字符
 [:graph:]
 非空字符（非空格、控制字符）
 [:lower:]
 小写字符
 [:cntrl:]
 控制字符
 [:print:]
 非空字符（包括空格）
 [:punct:]
 标点符号
 [:space:]
 所有空白字符（新行，空格，制表符）
 [:upper:]
 大写字符
 [:xdigit:]
 十六进制数字（0-9，a-f，A-F）
    
  </li>
  
  <li>
    
      实例
 要用好grep这个工具，其实就是要写好正则表达式，所以这里不对grep的所有功能进行实例讲解，只列几个例子，讲解一个正则表达式的写法。
 $ ls -l | grep '^a'
 通过管道过滤ls -l输出的内容，只显示以a开头的行。
 $ grep 'test' d*
 显示所有以d开头的文件中包含test的行。
 $ grep 'test' aa bb cc
 显示在aa，bb，cc文件中匹配test的行。
 $ grep '[a-z]' aa
 显示所有包含每个字符串至少有5个连续小写字符的字符串的行。
 $ grep 'w(es)t.<em>' aa
 如果west被匹配，则es就被存储到内存中，并标记为1，然后搜索任意个字符（.</em>），这些字符后面紧跟着另外一个es（），找到就显示该行。如果用egrep或grep -E，就不用""号进行转义，直接写成'w(es)t.*'就可以了。
    
  </li>
</ol>

http://www.cnblogs.com/end/archive/2012/02/21/2360965.htm
  
https://www.cnblogs.com/sparkdev/p/11294517.html
  
https://www.cnblogs.com/ywl925/p/3947778.html