---
title: vi basic, vim basic command
author: "-"
date: 2022-12-15 12:44:54
url: vim
categories:
  - Editor
tags:
  - reprint
  - remix
  - VIM
---

## vi/vim basic, command

## 基本插入

```r
i:          在光标前插入；一个小技巧：按8，再按i，进入插入模式，输入=， 按esc进入命令模式，就会出现8个=。 这在插入分割线时非常有用，如`30i+<esc>`就插入了36个+组成的分割线。
I:          在当前行第一个非空字符前插入；
gI:         在当前行第一列插入；
a:          在光标后插入；
A:          在当前行最后插入；
o:          在当前行的下边插入新行, 在当前行的下边插入一行
O:          在当前行的上边插入新行
:r          filename在当前位置插入另一个文件的内容。
:[n]r       filename在第n行插入另一个文件的内容。
:r !date    在光标处插入当前日期与时间。同理，:r !command可以将其它shell命令的输出插入当前文档。
escape      回到命令模式
^v char     插入时忽略char的指定意义，这是为了插入特殊字符
```

### vim 编辑二进制文件

```bash
# 注意用-b，否则后面会有0a
vim -b test.bin
# 以16进制格式查看
:%!xxd
# 编辑完成后转换为二进制文件
:$!xxd -r
:wq

# force write
:w!
```

```bash
### vim utf8 乱码
#### 查看文件编码
:set fileencoding
# 显示行号
:set number
# 不自动换行
:set nowrap
# 自动换行
:set wrap
```

如果你只是想查看其它编码格式的文件或者想解决用 Vim 查看文件乱码的问题，那么你可以在 ~/.vimrc 文件中添加以下内容:

```bash
vim ~/.vimrc

# content
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8
```

这样，就可以让vim自动识别文件编码 (可以自动识别UTF-8或者GBK编码的文件) ，其实就是依照 fileencodings提供的编码列表尝试，如果没有找到合适的编码，就用latin-1(ASCII)编码打开。

### 上移一行

```vi
ddkP
```

### install

#### debian install nvim

<https://vra.github.io/2019/03/13/ubuntu-install-neovim/>

```bash
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt update
sudo apt install -y neovim
sudo add-apt-repository ppa:neovim-ppa/unstable
sudo apt update
sudo apt install -y neovim
# after install, type 'nvim' to open neovim 
```

### vim g 和 % 区别

#### g 全局的

替换行中出现的每一个pattern

```v
    s/pattern/replacement/
```

开始处的 g 是全局命令，意味着对所有与地址匹配的行进行改变。结尾处的g是一个标志，意味着改变一行上的每个。

```v
    g/pattern/s/pattern/replacement/g
```

linux中的grep = g/rep/p

#### %: 代表这文件本身每一行, 本文件的所有的行

```v
    % == g/.*/
```

g要与模式/pattern/一起使用 表示在某个范围内 (一行或者整个文本) 中所有与该模式匹配的部分  

对所有与地址匹配的行，/pattern/ 意味着与这个地址匹配的第一行

```v
    g/pattern/
```

s...只替换行中匹配到的第一个，s/pattern/replacement/g 意味着替换行中匹配到的所有

```v
    s/pattern/replacement/ 
```

%s/pattern/replacement == g/.*/s/pattern/replacement

对所有有任意数量的任意字符的行

```v
    g/.*/ : 
```

### 全选

```v
    按esc后，然后ggvG或者ggVG
```

### 替换换行符

```bash
windows 中将空格符替换为换行符的方法: 
:%s/xx/\r/g(因为windows的CTRL+V是粘贴的功能，所以不能输入^M)

linux中方法: 
:%s/xx/\r/g
:%s/xx/^M/g(^M的输入方法是: 先按CTRL+V，松开然后按回车键) 
```

### 复制

全部复制: 按esc键后，先按gg，然后ggyG
单行复制: 按esc键后，然后yy

### 执行上一次的命令

```v
    # 点
    .
```

### visual

visual模式
 (1) 在普通模式 (normal) 下，直接按键 v  就可以进入默认visual模式，可以使用v+j/k/h/l 进行文本选择

#### 复制，剪切，粘贴

用v选中文本
对于选中的文本进行如下按键
 (1.1) d   ------ 剪切操作
 (1.2) y   -------复制操作
 (1.3) p   -------粘贴操作
 (1.4) ^  --------选中当前行，光标位置到行首 (或者使用键盘的HOME键)
 (1.5) $  --------选中当前行，光标位置到行尾 (或者使用键盘的END键)

 (2) Visual Line模式  按键V可以进入

按键V之后，进入Visual Line模式，使用 j/k键可以选中一行或者多行

(3) Visual Block模式，按键Ctrl + V可以进入

按键Ctrl+V之后，进入Visual Block模式，使用 j/k/h/l键可以选中一块
在块模式下，可以进行多列的同时修改，修改方法是:

首先进入块模式 Ctrl+ v

使用按键j/k/h/l进行选中多列

按键Shift + i 进行 块模式下的插入

输入字符之后，按键ESC，完成多行的插入
//todo, visual move to separate post.

### 查找，替换

[http://blog.wiloon.com/?p=13147](http://blog.wiloon.com/?p=13147)

## vim 删除

- dw 从光标当前的位置开始删除, 删至下一个字的开头
- daw 删除光标所在的一个单词, delete a word
- bdw，这也是一个复合命令。b 可以让光标回退到单词开头的位置，而dw则是第1个描述过的命令。

| Command | Comments                                          |
| ------- | ------------------------------------------------- |
| X       | 删除光标前的字符，可以在X前加上需要删除的字符数目 |
| nX      | 从当前光标处往前删除n个字符                       |
| db      | 删除到前一个单词|
|dB|           删除到前一个单词包括标点在内|
|de|删除到本单词末尾|
|dE|删除到本单词末尾包括标点在内|
| d1G     | 删至文档首部                                      |
| dG      | 删除行，直到文件结束                              |
| d^      | 删除至行首                                        |
| d$      | 从光标处删除到行尾                                |
| dd      | 删除整行                                          |

## 光标移动

| Command | Comments                                         |
| ------- | ------------------------------------------------ |
| 0       | 移动到行首                                       |
| $       | 移动到行尾                                       |
| w       | 移到下一个字的开头                               |
| W       | 移到下一个字的开头，忽略标点符号                 |
| b       | 移到前一个字的开头                               |
| B       | 移到前一个字的开头，忽略标点符号                 |
| :n      | 输入:n，代表跳转到第n行，如:79，就跳转到第79行。 |
| n\|     | 移到到第n列                                      |

### Others

| Command | Comments                                      |
| ------- | --------------------------------------------- |
| :f      | 文件名 改变编辑中的文件名。(file)             |
| :35 r   | 文件名 将文件插入至 35 行之后。               |
| :r !xxx | 执行xxx并将结果插入                           |
| yy      | 复制一行,到缓冲区                             |
| p       | 粘贴                                          |

***

ndw 从当前光标处往后删除n个字

ndd 从当前行开始往后删除

db 删除光标前面的字

ndb 从当前行开始往前删除n字

:n,md 从第m行开始往前删除n行

dcursor_command 删除至光标命令处，如dG将从当产胆行删除至文件的末尾

^h或backspace 插入时，删除前面的字符

^w 插入时，删除前面的字

输入:n，代表跳转到第n行，如:79，就跳转到第79行。

```bash
:s/vivian/sky/g
:s/oldtext/newtext       #用newtext替换oldtext

dG  #删除直到工作缓存区结尾的内容
d1G #删除直到工作缓存区开始的内容
查询当前行:nu
多行删除
多行删除，删除1到10行:1,10d
从某行开始至文本末尾全部删除，删除第8行至末尾:8,$d
#正则. str后两位数字
/str\\d\\d

#vim统计某个匹配出现的次数
:%s/hello world/&/gn
:%s/objStr//gn
http://www.2cto.com/os/201209/153515.html
```

上句统计hello world 在全文出现的次数。

如果要统计从50行到100行，出现的次数，则使用

:50,100s/hello world//gn

gg 首行

G 未行

/pattern: 从光标开始处向文件尾搜索pattern

?pattern: 从光标开始处向文件首搜索pattern

n: 在同一方向重复上一次搜索命令

N: 在反方向上重复上一次搜索命令

vi统计某个匹配出现的次数

:%s/hello world/&/gn

命令 光标移动

h或^h 向左移一个字符

j或^j或^n 向下移一行

k或^p 向上移一行

l或空格 向右移一个字符

G 移到文件的最后一行

nG 移到文件的第n行

L 移到屏幕的最后一行

M 移到屏幕的中间一行

H 移到屏幕的第一行

e 移到下一个字的结尾

E 移到下一个字的结尾，忽略标点符号

( 移到句子的开头

) 移到句子的结尾

{ 移到段落的开头

} 移到下一个段落的开头

0或| 移到当前行的第一列

n| 移到当前行的第n列

^ 移到当前行的第一个非空字符

$ 移到当前行的最后一个字符

\+或return 移到下一行的第一个字符

– 移到前一行的第一个非空字符

修改vi文本

每个命令前面的数字表示该命令重复的次数

命令 替换操作

rchar 用char替换当前字符

R text escape 用text替换当前字符直到换下Esc键

stext escape 用text代替当前字符

S或cctext escape 用text代替整行

cwtext escape 将当前字改为text

Ctext escape 将当前行余下的改为text

cG escape 修改至文件的末尾

ccursor_cmd text escape 从当前位置处到光标命令位置处都改为text

在vi中查找与替换

命令 查找与替换操作

/text 在文件中向前查找text

?text 在文件中向后查找text

n 在同一方向重复查找

N 在相反方向重复查找

ftext 在当前行向前查找text

Ftext 在当前行向后查找text

ttext 在当前行向前查找text，并将光标定位在text的第一个字符

Ttext 在当前行向后查找text，并将光标定位在text的第一个字符

:set ic 查找时忽略大小写

:set noic 查找时对大小写敏感

:m,ns/oldtext/newtext 在m行通过n，用newtext替换oldtext

& 重复最后的:s命令

:g/text1/s/text2/text3 查找包含text1的行，用text3替换text2

:g/text/command 在所有包含text的行运行command所表示的命令

:v/text/command 在所有不包含text的行运行command所表示的命令

在vi中复制文本

命令 复制操作

yy 将当前行的内容放入临时缓冲区

nyy 将n行的内容放入临时缓冲区

p 将临时缓冲区中的文本放入光标后

P 将临时缓冲区中的文本放入光标前

dsfsd "(a-z)nyy 复制n行放入名字为圆括号内的可命名缓冲区，省略n表示当前行

"(a-z)ndd 删除n行放入名字为圆括号内的可命名缓冲区，省略n表示当前行

"(a-z)p 将名字为圆括号的可命名缓冲区的内容放入当前行后

"(a-z)P 将名字为圆括号的可命名缓冲区的内容放入当前行前

在vi中撤消与重复

命令 撤消操作

u 撤消最后一次修改

U 撤消当前行的所有修改

. 重复最后一次修改

, 以相反的方向重复前面的f、F、t或T查找命令

; 重复前面的f、F、t或T查找命令

"np 取回最后第n次的删除(缓冲区中存有一定次数的删除内容，一般为9)

n 重复前面的/或?查找命令

N 以相反方向重复前面的/或?命令

保存文本和退出vi

命令 保存和/或退出操作

:w 保存文件但不退出vi,  可以指定目录，相当于另存，:w /path/to/file/foo

:w file 将修改保存在file中但不退出vi

:wq或ZZ或:x 保存文件并退出vi

:q! 不保存文件，退出vi

:e! 放弃所有修改，从上次保存文件开始再编辑

vi中的选项

选项 作用

:set all 打印所有选项

:set nooption 关闭option选项

:set nu 每行前打印行号

:set showmode 显示是输入模式还是替换模式

:set noic 查找时忽略大小写

:set list 显示制表符(^I)和行尾符号

:set ts=8 为文本输入设置tab stops

:set window=n 设置文本窗口显示n行

vi的状态

选项 作用

:.= 打印当前行的行号

:= 打印文件中的行数

^g 显示文件名、当前的行号、文件的总行数和文件位置的百分比

:l 使用字母"l"来显示许多的特殊字符，如制表符和换行符

在文本中定位段落和放置标记

选项 作用

{ 在第一列插入{来定义一个段落

[[ 回到段落的开头处

]] 向前移到下一个段落的开头处

m(a-z) 用一个字母来标记当前位置，如用mz表示标记z

'(a-z) 将光标移动到指定的标记，如用'z表示移动到z

在vi中连接行

选项 作用

J 将下一行连接到当前行的末尾

nJ 连接后面n行

光标放置与屏幕调整

选项 作用

H 将光标移动到屏幕的顶行

nH 将光标移动到屏幕顶行下的第n行

M 将光标移动到屏幕的中间

L 将光标移动到屏幕的底行

nL 将光标移动到屏幕底行上的第n行

^e(ctrl+e) 将屏幕上滚一行

^y 将屏幕下滚一行

^u 将屏幕上滚半页

^d 将屏幕下滚半页

^b 将屏幕上滚一页

^f 将屏幕下滚一页

^l 重绘屏幕

z-return 将当前行置为屏幕的顶行

nz-return 将当前行下的第n行置为屏幕的顶行

z. 将当前行置为屏幕的中央

nz. 将当前行上的第n行置为屏幕的中央

z- 将当前行置为屏幕的底行

nz- 将当前行上的第n行置为屏幕的底行

### vi中的 shell 转义命令

选项 作用

:!command 执行shell的command命令，如:!ls

:!! 执行前一个shell命令

:r!command 读取command命令的输入并插入，如:r!ls会先执行ls，然后读入内容

:w!command 将当前已编辑文件作为command命令的标准输入并执行command命令，如:w!grep all

:cd directory 将当前工作目录更改为directory所表示的目录

:sh 将启动一个子shell，使用^d(ctrl+d)返回vi

:so file 在shell程序file中读入和执行命令

vi中的宏与缩写

(避免使用控制键和符号，不要使用字符K、V、g、q、v、*、=和功能键)

选项 作用

:map key command_seq 定义一个键来运行command_seq，如:map e ea，无论什么时候都可以e移到一个字的末尾来追加文本

:map 在状态行显示所有已定义的宏

:umap key 删除该键的宏

:ab string1 string2 定义一个缩写，使得当插入string1时，用string2替换string1。当要插入文本时，键入string1然后按Esc键，系统就插入了string2

:ab 显示所有缩写

:una string 取消string的缩写

在vi中缩进文本

选项 作用

^i(ctrl+i)或tab 插入文本时，插入移动的宽度，移动宽度是事先定义好的

:set ai 打开自动缩进

:set sw=n 将移动宽度设置为n个字符

n<< 使n行都向左移动一个宽度

n>> 使n行都向右移动一个宽度，例如3>>就将接下来的三行每行都向右移动一个移动宽度

一、查找

查找命令

`/pattern<Enter>` : 向下查找pattern匹配字符串

`?pattern<Enter>`: 向上查找pattern匹配字符串

使用了查找命令之后，使用如下两个键快速查找:

n: 按照同一方向继续查找

N: 按照反方向查找

字符串匹配

pattern是需要匹配的字符串，例如:

1: `/abc<Enter>` #查找abc

2: `/ abc <Enter>` #查找abc单词 (注意前后的空格)

除此之外，pattern还可以使用一些特殊字符，包括 (/、^、$、*、.) ，其中前三个这两个是vi与vim通用的，"/"为转义字符。

1: `/^abc<Enter>` #查找以abc开始的行

2: `/test$<Enter>` #查找以abc结束的行

3: `//^test<Enter>` #查找^tabc字符串

二、替换

基本替换

1: :s/vivian/sky/ #替换当前行第一个 vivian 为 sky

2: :s/vivian/sky/g #替换当前行所有 vivian 为 sky

3: :n,$s/vivian/sky/ #替换第 n 行开始到最后一行中每一行的第一个 vivian 为 sky

4: :n,$s/vivian/sky/g #替换第 n 行开始到最后一行中每一行所有 vivian 为 sky

5:  (n 为数字，若 n 为 .，表示从当前行开始到最后一行)

6:

7: :%s/vivian/sky/ # (等同于 :g/vivian/s//sky/)  替换每一行的第一个 vivian 为 sky

8: :%s/vivian/sky/g # (等同于 :g/vivian/s//sky/g)  替换每一行中所有 vivian 为 sky

可以使用 #或+ 作为分隔符，此时中间出现的 / 不会作为分隔符

1: :s#vivian/#sky/# 替换当前行第一个 vivian/ 为 sky/

2: :%s+/oradata/apras/+/user01/apras1+  (

3: 使用+ 来 替换 / ) :  /oradata/apras/替换成/user01/apras1/

删除文本中的^M

问题描述: 对于换行，window下用回车换行 (0A0D) 来表示，linux下是回车 (0A) 来表示。这样，将window上的文件拷到unix上用时，总会有个^M，请写个用在unix下的过滤windows文件的换行符 (0D) 的shell或c程序。

使用命令: cat filename1 | tr -d "^V^M" > newfile;

使用命令: sed -e "s/^V^M//" filename > outputfilename

需要注意的是在1、2两种方法中，^V和^M指的是Ctrl+V和Ctrl+M。你必须要手工进行输入，而不是粘贴。

在vi中处理: 首先使用vi打开文件，然后按ESC键，接着输入命令:

1: :%s/^V^M//

2: :%s/^M$//g

如果上述方法无用，则正确的解决办法是:

1: tr -d "/r" < src >dest

2: tr -d "/015″ dest

3:

4: strings A>B

其它用法

1: :s/str1/str2/ #用字符串 str2 替换行中首次出现的字符串 str1

2: :s/str1/str2/g #用字符串 str2 替换行中所有出现的字符串 str1

3: :.,$ s/str1/str2/g #用字符串 str2 替换正文当前行到末尾所有出现的字符串 str1

4: :1,$ s/str1/str2/g #用字符串 str2 替换正文中所有出现的字符串 str1

5: :g/str1/s//str2/g #功能同上

从上述替换命令可以看到:

g 放在命令末尾，表示对指定行的搜索字符串的每次出现进行替换；不加 g，表示只对指定行的搜索字符串的首次出现进行替换；

g 放在命令开头，表示对正文中所有包含搜索字符串的行进行替换操作。

也就是说命令的开始可以添加影响的行，如果为g表示对所有行；命令的结尾可以使用g来表示是否对每一行的所有字符串都有影响。

三、简单的vim正则表达式规则

在vim中有四种表达式规则:

magic(/m): 除了$.*^之外其他元字符都要加反斜杠

nomagic(/M): 除了$^之外其他元字符都要加反斜杠

/v (即 very magic 之意) : 任何元字符都不用加反斜杠

/V (即 very nomagic 之意) : 任何元字符都必须加反斜杠

vim默认使用magic设置，这个设置也可以在正则表达式中通过 /m /M /v /V开关临时切换。例如:

1: //m.* # 查找任意字符串

2: //M.*# 查找字符串 .*  (点号后面跟个星号)

3:

4: //v(a.c){3}$ # 查找行尾的abcaccadc

5: //m(a.c){3}$ # 查找行尾的(abc){3}

6: //M(a.c){3}$ # 查找行尾的(a.c){3}

7: //V(a.c){3}$ # 查找任意位置的(a.c){3}$

推荐使用默认的magic设置，在这种情况下，常用的匹配有:

1: // #查找以test结束的字符串

3:

4: $ 匹配一行的结束

5: ^ 匹配一行的开始

6: /< 匹配一个单词的开始，例如//:查找以abc开始的字符串

7: /> 匹配一个单词的结束，例如`/abc/><Enter>`:查找以abc结束的字符串

8:

9: * 匹配0或多次

10: /+ 匹配1或多次

11: /= 匹配0或1次

12:

13: . 匹配除换行符以外任意字符

14: /a 匹配一个字符

15: /d 匹配任一数字

16: /u 匹配任一大写字母

17:

18: [] 匹配范围，如t[abcd]s 匹配tas tbs tcs tds

19: /{} 重复次数，如a/{3,5} 匹配3\~5个a

20: /( /) 定义重复组，如a/(xy/)b 匹配ab axyb axyxyb axyxyxyb …

21: /| 或，如: for/|bar 表示匹配for或者bar

22:

23: /%20c 匹配第20列

24: /%20l 匹配第20行

关于正则表达式的详细信息，请参见参考文献。

### config

><https://www.ruanyifeng.com/blog/2018/09/vimrc.html>

<http://www.cnblogs.com/88999660/articles/1581524.html>

<http://www.cnblogs.com/taizi1985/archive/2007/08/13/853190.html>
<https://www.cnblogs.com/luosongchao/p/3193153.html>
