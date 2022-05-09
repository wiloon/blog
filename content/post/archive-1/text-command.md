---
title: 文本处理命令， text command
author: "-"
date: 2015-09-17T01:22:10+00:00
url: command/text
categories:
  - Linux
tags:
  - reprint
---
## 文本处理命令， text command

1. 正则表达式 (regular expression)
  
元字符 (如下图) 是正则表达式中含有的字符,在正则表达式中可以在字符串中使用元字符以匹配字符串的各种可能的情况。

注意:

(1) 在"[ ]"中还可以使用"-"来表示某一范围。例如"[a-z0-9]"匹配任意的小写字母或者数字,"[^A-Z]"表示非大写字母,"[0-9]{8}"表示任意一个8位数字。

(2) 元字符还可以配合使用:
  
".\*"可以匹配任意个字符,如"r.\*d"会匹配"rd"、"red"、"read"。
  
".+"可以匹配任意的一个或者多个字符,如"r.+d"会匹配"red"、"read",但不会匹配"rd"。
  
".?"可以匹配任意的零个或一个字符,如"r.?d"会匹配"rd"、"red",但不会匹配"read"。
  
"^$"匹配空白行。

(3) 在[ ]中还可以使用一些特殊匹配模式,如下表:
  
以"\"开头得元字符

- grep

>wangyue.dev/grep
  
- find

3. cut命令
  
命令说明: 按行处理,将一行消息的某段切出来。
  
格式: cut -d '分割字符' -f fields
  
cut -c m-n
  
例如: echo $PATH | cut -d ':' -f 3,5,取出环境变量PATH中的第3个和第5个路径。
  
echo $PATH | cut -d ':' -f 3-5,取出环境变量PATH中的第3个到第5个路径。
  
export | cut -c 12-, 将export中的每行的前面11个字符删除留,保留从第12个字符开始的所有字符。
  
4. awk工具
  
命令说明:  将一行消息分成数个段来处理,适合处理小型的数据。
  
格式: awk '条件类型 {动作}' file
  
awk的内置变量:
  
$n: 该行的第n个字段；
  
NF: 每一行拥有的字段总数；
  
NR: 当前行的行号；
  
FS: 分隔符,默认为空格键；

例如: cat /etc/passwd | awk 'BEGIN {FS=":"} $S3<10 {print $1 "\t" $3}',打印passwd文件第三栏小于10的行的第1、3栏。
  
### sort

命令说明: 将文本文件的内容按行排序。
  
格式: sort [-fbMnrtuk] [file or stdin]
  
#### 参数  

    -f: 忽略大小写；
    -b: 忽略最前面的空格；
    -g, --general-numeric-sort  compare according to general numerical value, 按照常规数值排序
    -u: 即uniq,重复行仅出现一次；
    -M: 以月份的名字来排序；
    -n: 使用纯数字来排序；
    -r: 反向排序
    -t: 分隔符,默认为tab键；
    -k: 按指定字段排序；例如:  cat /etc/passwd | sort -t ':' -k 3,对文件/etc/passwd以第三栏排序。

对第一列排序
sort -n test
对第二列进行排序
sort -n -k 2 test
如果将test文件的内容改为：
8723,23423
321324,213432
23,234
123,231
234,1234
654,345234
如果要对第二列按照大小排序
sort -n -t "," -k 2 test
————————————————
版权声明：本文为CSDN博主「sunjiangangok」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/sunjiangangok/article/details/69943756>

### uniq

命令说明: 如果排序完成了, 将重复的行仅显示一次. 注意, 若文件未排序,该命令失效。
  
格式: uniq [-ic]
  
#### uniq 参数
  
- -i: 忽略大小写；
- -c: 统计每行重复的次数；
- -d: 查找重复行

### wc

wc(Word Count)命令用来统计文件内容信息,包括字数，行数、字符数等  

#### 统计输出信息的行数

    wc -l

格式: wc [-lwm] fine_name

若不接文件，则统计标准输入

参数说明:

```bash
#显示文件内容信息,输出信息依次是:行数,字数,字节数,文件名称
wc filename
 
#显示一个文件的行数
wc -l filename
 
#显示一个文件的字节数
wc -c filename
 
#显示一个文件的字符数
wc -m filename
 
#显示一个文件中的最长行的长度
wc -L filename
 
#注意: 每行结尾的换行符也算一个字符，空格也算一个字符
#采用UTF-8编码，所以一个汉字在这里被转换为3字节
#当使用-m选项时，一个汉字就作为一个字符计算

# 词数
-w: 仅显示字数 (英文单词个数) 

```

### tee命令

命令说明: 双向重导向,从标准输入读取数据,输出到屏幕上,同时保存成文件。
  
格式: tee [-a] file
  
参数说明:
  
-a: 以累加的方式,将数据加入到file中。
  
例如: ls -al /home | tee ~/myfile | more,将ls命令的数据存一份到myfile中,同时屏幕也有输出数据。
  
10. tr命令
  
命令说明: 单个字符的处理工具,可以用于删除字符、替换字符等基本功能。更复杂的字符串处理工具通常使用sed。
  
格式: tr [-ds] SET1....
  
参数说明:
  
-d: 删除,例如: cat file | tr -d '\r',相当于dos2unix命令所起的作用。
  
-s: 替换字符,例如: cat file | tr -s [0-9],如果某个数字连续出现,仅保留第一个。
  
cat file | tr [a-z] [A-Z],将file中的小写字符全部改为大写。
  
11. col命令
  
命令说明: 格式化显示列。
  
格式: col [-x]
  
参数说明:
  
-x: 将tab键转换成对等的空格键；
  
例如: cat -A /etc/man.config | col -x | cat -A,使用cat -A,tab键会以^I显示,经过col -x处理,tab替换为空格。
  
12. expand命令
  
命令说明: 将tab键转换成空格键。
  
格式: expand [-t] file

参数说明:
  
-t n: 后面可以接一个数字n,一个tab键替换为n个空格键,默认值为8。

13. join命令
  
命令说明: 处理两个文件中有相同数据的行,将它们加在一起。
  
格式: join [-ti12] file1 file2

参数说明:
  
-i: 忽略大小写；
  
-t: 分隔符,默认为空格符；
  
-1 m: 指定file1用来比较的字段m,默认值为1；
  
-2 n: 指定file2用来比较的字段n,默认值为1；

14. paste命令
  
命令说明: 比较两个文件的数据关联性,直接将"两行贴在一起",中间以tab键隔开。
  
格式: paste [-d] file1 file2
  
参数说明:
  
-d: 后面接分隔符,默认为tab键。
  
15. diff命令
  
命令说明: 以"行"为单位进行文件比较,一般用在ASCII纯文本文件。
  
格式: diff [-bBi] file1 file2
  
参数:
  
-b: 忽略一行中有多个空白的差异；
  
-B: 忽略空白行的不同；
  
-i: 忽略大小写；

16. cmp命令
  
命令说明: 以"位"为单位进行文件比较,可以比较二进制文件。
  
格式: cmp [-s] file1 file2
  
参数:
  
-s: 将所有不同点的位都列出来,默认仅输出第一个发现的不同点；
  
17. patch命令
  
命令说明: diff old new > patch_file命令可以找出new文件与old文件不同的地方,然后用patch命令给old文件打上补丁,即与new文件相同了。
  
格式: patch -pN < patch_file
  
参数: -pN表示取消N层目录。

18. split命令
  
命令说明: 将一个大文件拆分为几个小文件。
  
格式: split [-bl] fle
  
参数说明:
  
-b: 拆分的文件大小,可加单位,如b, k, m等；
  
-l: 按行数进行拆分；
  
例如: split -b 512k bigfile smallfile,将文件bigfile按512K拆分,拆分后的文件依次为: smallfileaa. smallfileab等。
  
split -l 10 bigfile smallfile,将文件bigfile中的每10行拆分成一个小文件。
  
19. xargs命令

### head

head 命令可用于查看文件的开头部分的内容,有一个常用的参数 -n 用于显示行数,默认为 10,即显示 10 行的内容。
    -q 隐藏文件名
    -v 显示文件名
    -c<数目> 显示的字节数。
    -n<行数> 显示的行数。

> <http://blog.csdn.net/forgotaboutgirl/article/details/6801525#t16>
