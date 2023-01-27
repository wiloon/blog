---
title: tr command
author: "-"
date: 2020-02-14T02:56:46+00:00
url: tr
categories:
  - Linux
tags:
  - reprint
---
## tr command

```bash
# 转大写
echo 'hello' | tr '[:lower:]' '[:upper:]'
# 转小写
echo 'HELLO' | tr '[:upper:]' '[:lower:]'

```

什么是 tr 命令？ tr, translate 的简写

```r
\NNN            character with octal value NNN (1 to 3 octal digits)
\\              backslash
\a              audible BEL
\b              backspace
\f              form feed
\n              new line
\r              return
\t              horizontal tab
\v              vertical tab
CHAR1-CHAR2     all characters from CHAR1 to CHAR2 in ascending order
[CHAR*]         in SET2, copies of CHAR until length of SET1
[CHAR*REPEAT]   REPEAT copies of CHAR, REPEAT octal if starting with 0
[:alnum:]       all letters and digits
[:alpha:]       all letters
[:blank:]       all horizontal whitespace
[:cntrl:]       all control characters
[:digit:]       all digits
[:graph:]       all printable characters, not including space
[:lower:]       all lower case letters
[:print:]       all printable characters, including space
[:punct:]       all punctuation characters
[:space:]       all horizontal or vertical whitespace
[:upper:]       all upper case letters
[:xdigit:]      all hexadecimal digits
[=CHAR=]        all characters which are equivalent to CHAR
```

<https://blog.csdn.net/jeffreyst_zb/article/details/8047065>

通过使用tr，您可以非常容易地实现 sed 的许多最基本功能。您可以将 tr 看作为 sed的 (极其) 简化的变体: 它可以用一个字符来替换另一个字符，或者可以完全除去一些字符。您也可以用它来除去重复字符。这就是所有 tr所能够做的。

tr用来从标准输入中通过替换或删除操作进行字符转换。tr主要用于删除文件中控制字符或进行字符转换。使用tr时要转换两个字符串: 字符串1用于查询，字符串2用于处理各种转换。tr刚执行时，字符串1中的字符被映射到字符串2中的字符，然后转换操作开始。

带有最常用选项的tr命令格式为:
  
tr -c -d -s ["string1_to_translate_from"]["string2_to_translate_to"] < input-file
  
这里:
  
-c 用字符串1中字符集的补集替换此字符集，要求字符集为ASCII。
  
-d 删除字符串1中所有输入字符。
  
-s 删除所有重复出现字符序列，只保留第一个；即将重复出现字符串压缩为一个字符串。
  
input-file是转换文件名。虽然可以使用其他格式输入，但这种格式最常用。

1. 字符范围
  
指定字符串1或字符串2的内容时，只能使用单字符或字符串范围或列表。
  
[a-z] a-z内的字符组成的字符串。
  
[A-Z] A-Z内的字符组成的字符串。
  
[0-9] 数字串。
  
\octal 一个三位的八进制数，对应有效的ASCII字符。
  
[O_n] 表示字符O重复出现指定次数n。因此[O_2]匹配OO的字符串。
  
tr中特定控制字符的不同表达方式
  
速记符含义八进制方式
  
\a Ctrl-G 铃声\007
  
\b Ctrl-H 退格符\010
  
\f Ctrl-L 走行换页\014
  
\n Ctrl-J 新行\012
  
\r Ctrl-M 回车\015
  
\t Ctrl-I tab键\011
  
\v Ctrl-X \030

实例:

、将文件file中出现的"abc"替换为"xyz"

# cat file | tr "abc" "xyz" > new_file

【注意】这里，凡是在file中出现的"a"字母，都替换成"x"字母，"b"字母替换为"y"字母，"c"字母替换为"z"字母。而不是将字符串"abc"替换为字符串"xyz"。

2. 使用tr命令"统一"字母大小写
  
 (小写 -> 大写)

# cat file | tr [a-z] [A-Z] > new_file

 (大写 -> 小写)

# cat file | tr [A-Z] [a-z] > new_file

3. 把文件中的数字0-9替换为a-j

# cat file | tr [0-9] [a-j] > new_file

4. 删除文件file中出现的"Snail"字符

# cat file | tr -d "Snail" > new_file

【注意】这里，凡是在file文件中出现的'S','n','a','i','l'字符都会被删除！而不是紧紧删除出现的"Snail"字符串。

5. 删除文件file中出现的换行'\n'、制表'\t'字符

# cat file | tr -d "\n\t" > new_file

不可见字符都得用转义字符来表示的，这个都是统一的。

6. 删除"连续着的"重复字母，只保留第一个

# cat file | tr -s [a-zA-Z] > new_file

7. 删除空行

# cat file | tr -s "\n" > new_file

8. 删除Windows文件"造成"的'^M'字符

# cat file | tr -d "\r" > new_file

或者

# cat file | tr -s "\r" "\n" > new_file

【注意】这里-s后面是两个参数"\r"和"\n"，用后者替换前者

9. 用空格符\040替换制表符\011

# cat file | tr -s "\011" "\040" >new_file

10. 把路径变量中的冒号":"，替换成换行符"\n"

# echo $PATH | tr -s ":" "\n"

* * *

1关于tr

通过使用 tr，您可以非常容易地实现 sed 的许多最基本功能您可以将 tr 看作为 sed 的 (极其) 简化的变体: 它可以用一个字符来替换另一个字符，或者可以完全除去一些字符您也可以用它来除去重复字符这就是所有 tr 所能够做的

tr用来从标准输入中通过替换或删除操作进行字符转换tr主要用于删除文件中控制字符或进行字符转换使用tr时要转换两个字符串: 字符串1用于查询，字符串2用于处理各种转换tr刚执行时，字符串1中的字符被映射到字符串2中的字符，然后转换操作开始
  
带有最常用选项的tr命令格式为:
  
tr -c -d -s ["string1_to_translate_from"] ["string2_to_translate_to"] < input-file
  
这里:
  
-c 用字符串1中字符集的补集替换此字符集，要求字符集为ASCII
  
-d 删除字符串1中所有输入字符
  
-s 删除所有重复出现字符序列，只保留第一个；即将重复出现字符串压缩为一个字符串
  
input-file是转换文件名虽然可以使用其他格式输入，但这种格式最常用
  
2字符范围
  
指定字符串1或字符串2的内容时，只能使用单字符或字符串范围或列表
  
[a-z] a-z内的字符组成的字符串
  
[A-Z] A-Z内的字符组成的字符串
  
[0-9] 数字串
  
\octal 一个三位的八进制数，对应有效的ASCII字符
  
[O_n] 表示字符O重复出现指定次数n因此[O_2]匹配OO的字符串
  
tr中特定控制字符的不同表达方式
  
速记符含义八进制方式
  
\a Ctrl-G 铃声\007
  
\b Ctrl-H 退格符\010
  
\f Ctrl-L 走行换页\014
  
\n Ctrl-J 新行\012
  
\r Ctrl-M 回车\015
  
\t Ctrl-I tab键\011
  
\v Ctrl-X \030
  
3应用例子
  
 (1) 去除oops.txt里面的重复的小写字符
  
tr -s "[a-z]"<oops.txt >result.txt
  
 (2) 删除空行
  
tr -s "[\012]" < plan.txt 或 tr -s ["\n"] < plan.txt
  
 (3) 有时需要删除文件中的^M，并代之以换行
  
tr -s "[\015]" "[\n]" < file 或 tr -s "[\r]" "[\n]" < file
  
 (4) 大写到小写
  
cat a.txt |tr "[a-z]" "[A-Z]" >b.txt
  
 (5) 删除指定字符

一个星期的日程表任务是从其中删除所有数字，只保留日期日期有大写，也有小写格式因此需指定两个字符范围[a-z]和[A-Z]，命令tr -cs "[a-z][A-Z]" "[\012_]" 将文件每行所有不包含在[a-z]或[A-Z] (所有希腊字母) 的字符串放在字符串1中并转换为一新行-s选项表明压缩所有新行， -c表明保留所有字母不动原文件如下，后跟tr命令:
  
tr -cs "[a-z][A-Z]" "[\012_]" <diary.txt
  
 (6) 转换控制字符

tr的第一个功能就是转换控制字符，特别是从dos向UNIX下载文件时，忘记设置ftp关于回车换行转换的选项时更是如此cat -v filename 显示控制字符

cat -v stat.txt

box aa^^^^^12^M

apple bbas^^^^23^M

^Z
  
猜想^ ^ ^ ^ ^ ^是tab键每一行以Ctrl-M结尾，文件结尾Ctrl-Z，以下是改动方法
  
使用-s选项，查看ASCII表^的八进制代码是136，^M是015，tab键是011，^Z是032 ,下面将按步骤完成最终功能
  
用tab键替换^ ^ ^ ^ ^ ^，命令为"\136" "[\011_]"将结果重定向到临时工作文件stat.tmp
  
tr -s "[\136]" "[\011_]" <stat.txt >stat.tmp
  
用新行替换每行末尾的^M，并用\n去除^Z，输入要来自于临时工作文件stat.tmp
  
tr -s "[\015][\032]" "\n" <stat.tmp
  
要删除所有的tab键，代之以空格，使用命令
  
tr -s "[\011]" "[\040*]" <input.file
  
 (7) 替换passwd文件中所有冒号，代之以tab键，可以增加可读性
  
tr -s "[:]" "[\011]" < /etc/passwd 或 tr -s "[:]" "[\t]" < /etc/passwd
  
 (8) 使路径具有可读性

如果用 echo $PATH 或者 echo $LD_LIBRARY_PATH 等类似的命令来显示路径信息的话，我们看到的将会是一大堆用冒号连接在一起的路径， tr命令可以把这些冒号转换为回车，这样，这些路径就具有很好的可读性了
  
echo $PATH | tr ":" "\n"
  
 (9) 可以在vi内使用所有这些命令！只要记住: 在tr命令前要加上您希望处理的行范围和感叹号  (！) ，如 1,$!tr -d '\t' (美元符号表示最后一行)
  
 (10) 另外，当有人给您发送了一个在 Mac OS 或 DOS/Windows 机器上创建的文本文件时，您会发现tr非常有用

如果没有将文件保存为使用 UNIX 换行符来表示行结束这种格式，则需要将这样的文件转换成本机 UNIX 格式，否则一些命令实用程序不会正确地处理这些文件Mac OS 的行尾以回车字符(\r)结束，许多文本处理工具将这样的文件作为一行来处理为了纠正这个问题，可以用下列技巧:
  
Mac -> UNIX: tr "\r" "\n"<macfile > unixfile
  
UNIX -> Mac: tr "\n" "\r"<unixfile > macfile
  
Microsoft DOS/Windows 约定，文本的每行以回车字符(\r)并后跟换行符(\n)结束为了纠正这个问题，可以使用下列命令:
  
DOS -> UNIX: tr -d "\r"<dosfile > unixfile
  
UNIX -> DOS: 在这种情况下，需要用awk，因为tr不能插入两个字符来替换一个字符要使用的 awk 命令为 awk '{ print $0"\r" }'<unixfile > dosfile

# 注: 都可以用sed 来完成

用途
  
转换字符。

语法
  
tr [ -c | -cds | -cs | -C | -Cds | -Cs | -ds | -s ] [ -A ] String1 String2

tr { -cd | -cs | -Cd | -Cs | -d | -s } [ -A ] String1

描述
  
tr 命令从标准输入删除或替换字符，并将结果写入标准输出。根据由 String1 和 String2 变量指定的字符串以及指定的标志，tr 命令可执行三种操作。

转换字符
  
如果 String1 和 String2 两者都已指定，但 -d 标志没有指定，那么 tr 命令就会从标准输入中将 String1 中所包含的每一个字符都替换成 String2 中相同位置上的字符。

使用 -d 标志删除字符
  
如果 -d 标志已经指定，那么 tr 命令就会从标准输入中删除 String1 中包含的每一个字符。

用 -s 标志除去序列
  
如果 -s 标志已经指定，那么 tr 命令就会除去包含在 String1 或 String2 中的任何字符串系列中的除第一个字符以外的所有字符。对于包含在 String1 中的每一个字符，tr 命令会从标准输出中除去除第一个出现的字符以外的所有字符。对于包含在 String2 中的每一个字符，tr 命令除去标准输出的字符序列中除第一个出现的字符以外的所有字符。

表达字符串的特殊序列
  
String1 和 String2 变量中所包含的字符串可以使用以下的约定来表示:

C1-C2 指定了 C1 所指定的字符和 C2 所指定的字符之间 (包括 C1 和 C2) 进行整理的字符串。C1 所指定的字符必须整理放在由 C2 所指定的字符之前。
  
注:
  
在使用本方法指定子范围时，当前语言环境对结果有重要影响。如果需要用命令来产生与语言环境无关的一致结果，那么应该避免使用子范围。
  
[C_Number] Number 是一个整数，它指定了由 C 所指定的字符的重复次数。除非其首位数字是 0，否则 Number 一律视为是十进制整数；如果首位数字是 0，那么视为八进制整数。
  
[C_] 用 C 指定的字符填写字符串。该选项只用于包含在 String2 中的字符串末尾，它强制 String2 中的字符串具有与由 String1 变量所指定的字符串一样的字符数。* (星号) 后面指定的任何字符都被忽略。
  
[ :ClassName: ] 指定由当前语言环境中的 ClassName 所命名的字符类中的所有字符。类名可以是下述名称中的任何一种:
  
alnum lower
  
alpha print
  
blank punct
  
cntrl space
  
digit upper
  
graph xdigit
  
除 `[:lower:]` 和 `[:upper:]` 转换字符类之外，其他字符类指定的字符都按未指定的顺序放入数组中。由于未定义字符类指定的字符的顺序，仅当目的为将多个字符映射为一个时才使用这些字符。转换字符类除外。

有关字符类的详细情况，请参阅 ctype 子例程。

[ =C= ] 指定所有的字符具有与 C 所指定的字符相同的等价类。
  
\Octal 指定字符，其编码由 Octal 所指定的八进制值表示。Octal 可以是 1 位、2 位 或 3 位八进制整数。空字符可以用 '\0' 表示，并可以像任何其他的字符那样进行处理。
  
\ControlCharacter 指定与 ControlCharacter 所指定的值相应的控制字符。可以表示以下值:
  
\a
  
警告
  
\b
  
退格键
  
\f
  
换页
  
\n
  
换行
  
\r
  
回车
  
\t
  
制表键
  
\v
  
垂直制表键
  
&#92; 规定 "\" (反斜杠) 就是作反斜杠使用，而无作为转义字符的任何特殊意义。
  
&#91; 指定"[" (左括号) 就作为左括号使用，而无作为特定字符串序列的开始字符的任何特殊意义。
  
&#45; 指定"-" (负号) 就作为负号使用，而无作为范围分隔符的任何特殊意义。
  
如果某个字符在 String1 中被指定过多次，那么该字符就被转换成 String2 中为与 String1 中最后出现的字符相对应的字符。

如果由 String1 和 String2 指定的字符串长度不相同，那么 tr 命令就会忽略较长一个字符串中的多余字符。

标志
  
-A 使用范围和字符类 ASCII 整理顺序、一个字节一个字节地执行所有操作，而不是使用当前语言环境整理顺序。
  
-C 指定 String1 值用 String1 所指定的字符串的补码替换。String1 的补码是当前语言环境的字符集中的所有字符，除了由 String1 指定的字符以外。如果指定了 -A 和 -c 标志都已指定，那么与所有 8 位字符代码集合有关的字符将被补足。如果指定了 -c 和 -s 标志，那么 -s 标志适用于 String1 的补码中的字符。
  
如果没有指定 -d 选项，那么由 String1 指定的字符的补码将放置到升序排列的数组中 (如 LC_COLLATE 的当前设置所定义) 。

-c 指定 String1 值用 String1 所指定的字符串的补码替换。String1 的补码是当前语言环境的字符集中的所有字符，除了由 String1 指定的字符以外。如果指定了 -A 和 -c 标志都已指定，那么与所有 8 位字符代码集合有关的字符将被补足。如果指定了 -c 和 -s 标志，那么 -s 标志适用于 String1 的补码中的字符。
  
如果没有指定 -d 选项，那么由 String1 指定的值的补码将放置到通过二进制值升序排列的数组中。

-d 从标准输入删除包含在由 String1 指定的字符串中的每个字符。
  
注:
  
当 -C 选项和 -d 选项一起指定时，将删除所有除 String1 指定的那些字符以外的字符。忽略 String2 的内容，除非也指定了 -s 选项。
  
当 -c 选项和 -d 选项一起指定时，将删除所有除 String1 指定的那些字符以外的字符。忽略 String2 的内容，除非也指定了 -s 选项。
  
-s 在重复字符序列中除去除第一个字符以外的所有字符。将 String1 所指定的字符序列在转换之前从标准输入中除去，并将 String2 所指定的字符序列从标准输出中除去。
  
String1 指定一个字符串。
  
String2 指定一个字符串。
  
退出状态
  
该命令返回以下退出值:

    所有输入处理成功。

> 0 发生错误。

> 示例

> 若要将大括号转换为小括号，请输入:

> tr '{}' '()' < textfile > newfile

> 这便将每个 { (左大括号) 转换成 ( (左小括号) ，并将每个 } (右大括号) 转换成 ) (右小括号) 。所有其他的字符都保持不变。

若要将大括号转换成方括号，请输入:
  
tr '{}' '&#91;]' < textfile > newfile
  
这便将每个 { (左大括号) 转换成 [ (左方括号) ，并将每个 } (右大括号) 转换成 ] (右方括号) 。左方括号必须与一个 "\" (反斜扛) 转义字符一起输入。

若要将小写字符转换成大写，请输入:
  
tr 'a-z' 'A-Z' < textfile > newfile
  
若要创建一个文件中的单词列表，请输入:
  
```bash
tr -cs '[:lower:][:upper:]' '[\n_]' < textfile > newfile
```
  
这便将每一序列的字符 (小、大写字母除外) 都转换成单个换行符。_ (星号) 可以使 tr 命令重复换行符足够多次以使第二个字符串与第一个字符串一样长。

若要从某个文件中删除所有空字符，请输入:
  
tr -d '\0' < textfile > newfile
  
若要用单独的换行替换每一序列的一个或多个换行，请输入:
  
tr -s '\n' < textfile > newfile
  
或

tr -s '\012' < textfile > newfile
  
若要以"？" (问号) 替换每个非显示字符 (有效控制字符除外) ，请输入:
  
tr -c '[:print:][:cntrl:]' '[?*]' < textfile > newfile
  
这便对不同语言环境中创建的文件进行扫描，以查找当前语言环境下不能显示的字符。

要以单个"#"字符替换 <space> 字符类中的每个字符序列，请输入:
  
tr -s '[:space:]' '[#*]'

><https://www.cnblogs.com/amosli/p/3488306.html>
