---
title: shell basic, shell script
author: "-"
date: 2019-05-06T04:27:52+00:00
url: shell
categories:
  - shell
tags:
  - reprint
---

## shell basic, shell script

## doc for bash

```bash
man bash
man zsh
```

## 自动输入密码/Y

```bash
echo "y" | sudo podman image prune
```

```bash
#!/bin/bash
sudo -S apt-get update << EOF 
你的密码
EOF
```

## 目录

### 检查目录是否存在

```bash
# check if directory is exist
if [ ! -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
fi

```

## read, 读取标准输入， 接收标准输入

read命令接收标准输入（键盘）的输入，或者其他文件描述符的输入。在得到输入之后，read命令把输入数据放入一个标准变量中。下面是read命令的基本形式:

```bash
# !/bin/bash                                 # 指定shell类型

echo -n "Enter your name:"                   # 参数 -n 的作用是不换行，echo 默认换行
read  name                                   # 把键盘输入保存到变量 name
echo "hello $name,welcome to my program"     # 显示输入信息
exit 0                                       # 返回一个零退出状态，退出shell程序
```

## 字符串

## 字符串截取, substring

```bash
url="c.biancheng.net"
echo ${url: 2: 9}
# 结果为biancheng

url="c.biancheng.net"
echo ${url: 2}  #省略 length，截取到字符串末尾
# 结果为biancheng.net。
```

<http://c.biancheng.net/view/1120.html>

### shell字符串大小写转换

#### typeset

typeset用于设置变量属性,如大小写,宽度,左右对齐等都可以用typeset来控制, 当用typeset改变一个变量的属性时,这种改变是永久的

有两个选项 -l 代表小写 -u 代表大写。
用法：
typeset -u name
name='asdasdas'
echo $name

typeset -l ame
ame='asdasdas'
echo $ame

利用表达式

echo 'hello' | tr '[:lower:]' '[:upper:]'
echo 'HELLO' | tr '[:upper:]' '[:lower:]'

————————————————
版权声明：本文为CSDN博主「LLZK_」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/LLZK_/article/details/66972407>

### 判断字符串是否相等

```bash
A="$1"
B="$2"

#判断字符串是否相等
if [ "$A" = "$B" ];then
echo "[ = ]"
fi

#判断字符串是否相等，与上面的=等价
if [ "$A" == "$B" ];then
echo "[ == ]"
fi
```

## 退出 shell 脚本

exit 命令可以接受一个整数值作为参数，代表退出状态。如果不指定，默认状态值是 0。

```bash
#!/bin/bash
echo "befor exit"
exit 8
echo "after exit"

```

## 特殊变量: Shell $0, $#, $*, $@, $?, $$和命令行参数

```bash
#变量       含义
$0        当前脚本的文件名
$n        传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1，第二个参数是$2/.
$#        传递给脚本或函数的参数个数。
$*        传递给脚本或函数的所有参数。
$@        传递给脚本或函数的所有参数。被双引号(" ")包含时，与 $* 稍有不同，下面将会讲到。
$?        上个命令的退出状态，或函数的返回值。
$$        Shell本身的进程ID(PID, Process ID)。对于 Shell 脚本，就是这些脚本所在的进程ID。
$!      上一个后台进程的进程号 (PID)
```

### $(), $( Dollar Single Parentheses )

Usage of the $ like ${HOME} gives the value of HOME. Usage of the $ like $(echo foo) means run whatever is inside the parentheses in a subshell and return that as the value.

#### Command Substitution

<https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html>

## 括号

## shell 括号

### 小括号，圆括号 `()`

单小括号 `()`
命令组。括号中的命令将会新开一个子 shell 顺序执行，所以括号中的变量不能够被脚本余下的部分使用。括号中多个命令之间用分号隔开，最后一个命令可以没有分号，各命令和括号之间不必有空格。
命令替换。等同于`cmd`，shell扫描一遍命令行，发现了`$(cmd)`结构，便将`$(cmd)`中的 cmd 执行一次，得到其标准输出，再将此输出放到原来命令。有些 shell 不支持，如 tcsh。
用于初始化数组。如：`array=(a b c d)`

#### 双小括号 `(())`

整数扩展。这种扩展计算是整数型的计算，不支持浮点型。((exp))结构扩展并计算一个算术表达式的值，如果表达式的结果为0，那么返回的退出状态码为1，或者 是"假"，而一个非零值的表达式所返回的退出状态码将为0，或者是"true"。若是逻辑判断，表达式exp为真则为1,假则为0。
只要括号中的运算符、表达式符合C语言运算规则，都可用在$((exp))中，甚至是三目运算符。作不同进位(如二进制、八进制、十六进制)运算时，输出结果全都自动转化成了十进制。如：echo $((16#5f)) 结果为95 (16进位转十进制)
单纯用 (( )) 也可重定义变量值，比如 a=5; ((a++)) 可将 $a 重定义为6
常用于算术运算比较，双括号中的变量可以不使用$符号前缀。括号内支持多个表达式用逗号分开。 只要括号中的表达式符合C语言运算规则,比如可以直接使用for((i=0;i<5;i++)), 如果不使用双括号, 则为for i in `seq 0 4`或者for i in {0..4}。再如可以直接使用if (($i<5)), 如果不使用双括号, 则为if [ $i -lt 5 ]。

#### 单中括号 `[]`, [ Single Square Brackets ]

中括号 `[]` 是 bash 的内部命令，[ 和 test 是等同的。如果我们不用绝对路径指明，通常我们用的都是bash自带的命令。if/test 结构中的左中括号是调用test的命令标识，右中括号是关闭条件判断的。  
这个命令把它的参数作为比较表达式或者作为文件测试，并且根据比较的结果来返回一个退出状态码。  

Test 和 [] 中可用的比较运算符只有 == 和 !=，两者都是用于字符串比较的，不可用于整数比较，整数比较只能使用 -eq，-gt 这种形式。无论是字符串比较还是整数比较都不支持大于号小于号。如果实在想用，对于字符串比较可以使用转义形式，如果比较 "ab" 和 "bc"[ ab \< bc ]，结果为真，也就是返回状态为0。
[] 中的逻辑与和逻辑或使用 -a 和 -o 表示。

#### 双中括号 `[[]]`

[[ 是 bash 程序语言的关键字。并不是一个命令，[[ ]] 结构比 [ ] 结构更加通用。在 [[ 和 ]]之间所有的字符都不会发生文件名扩展或者单词分割，但是会发生参数扩展和命令替换。
支持字符串的模式匹配，使用 =~ 操作符时甚至支持 shell 的正则表达式。字符串比较时可以把右边的作为一个模式，而不仅仅是一个字符串，比如 [[ hello == hell? ]]，结果为真。[[ ]] 中匹配字符串或通配符，不需要引号。
使用 [[ ... ]] 条件判断结构，而不是 [ ... ]，能够防止脚本中的许多逻辑错误。&&、||、< > 操作符能够正常存在于 [[ ]] 条件判断结构中，但是如果出现在 [ ] 结构中的话，会报错。可以直接使用 if [[ $a != 1 && $a != 2 ]], 如果不使用双括号, 则为 if [ $a -ne 1] && [ $a != 2 ] 或者 if [ $a -ne 1 -a $a != 2 ]。
双圆括号 (( ))
整数扩展。这种扩展计算是整数型的计算，不支持浮点型。
只要括号中的运算符、表达式符合 C 语言运算规则，都可用在 $((exp)) 中，甚至是三目运算符。作不同进位 (如二进制、八进制、十六进制) 运算时，输出结果全都自动转化成了十进制。如：echo $((16#5f)) 结果为 95 (16进位转十进制)
单纯用 (( )) 也可重定义变量值，比如 a=5; ((a++)) 可将 $a 重定义为6 。
常用于算术运算比较，双括号中的变量可以不使用 $ 符号前缀。括号内支持多个表达式用逗号分开。只要括号中的表达式符合 C 语言运算规则。可以使用 for((i=0;i<5;i++))，如果不使用双括号, 则为 for i in `seq 0 4` 或者 for i in {0..4}；直接使用 if (($i<5))，如果不使用双括号, 则为 if [ $i -lt 5 ]。

#### $[], dollar single square brackets

the $[ syntax was an early syntax that was deprecated in favor of $((, since the latter was already used by the Korn shell.

><https://unix.stackexchange.com/questions/209833/what-does-a-dollar-sign-followed-by-a-square-bracket-mean-in-bash>

#### { Single Curly Braces }

#### <( Angle Parentheses )

#### <<Double Angle Heredocs

><https://zhuanlan.zhihu.com/p/75145247>
><https://www.runoob.com/w3cnote/linux-shell-brackets-features.html>
><https://dev.to/rpalo/bash-brackets-quick-reference-4eh6>

## 循环, shell loop

```bash
#!/bin/sh

for i in 1 2 3 4 5
do
  echo "$i"
  date
  sleep 10
done

```

```bash
#!/bin/bash  

for i in {1..10}  
do  
echo $(expr $i \* 3 + 1);  
done
```

### 字符串分割

```bash
#!/bin/bash
string="hello,shell,haha"  
array=(${string//,/ })  
for var in ${array[@]}
do
   echo $var
done
```

### 布尔值变量

```bash
the_world_is_flat=true
# ...do something interesting...
if [ "$the_world_is_flat" = true ] ; then
    echo 'Be careful not to fall off!'
fi
```

<https://stackoverflow.com/questions/2953646/how-can-i-declare-and-use-boolean-variables-in-a-shell-script?rq=1>

### 字符串包含

```bash
# grep
strA="long string"
strB="string"
result=$(echo $strA | grep "${strB}")
if [[ "$result" != "" ]]
then
    echo "包含"
else
    echo "不包含"
fi
# 字符串运算符
strA="helloworld"
strB="low"
if [[ $strA =~ $strB ]]
then
    echo "包含"
else
    echo "不包含"
fi
# 通配符
A="helloworld"
B="low"
if [[ $A == *$B* ]]
then
    echo "包含"
else
    echo "不包含"
fi
```

### 把命令返回值赋值给变量, shell执行结果赋值给变量

```bash
tmp=$(pacman -Q go)
# 这种已经不推荐使用了
tmp=`pacman -Q go`

echo $tmp
```

### -f

检查文件是否存在

```bash
if [ -f filename ]
```

### 转义字符

在双引号中即可变普通字符的特殊字符

    空格 '\ `
    星号 '\*`
    井号 `#`
    换行符

即便在引号中也依然被 Shell 解释的特殊字符

    双引号 '\"'
    反引号 `` ` ``
    美元符 `\$`
    反斜杠 `\`

### Shell 变量
  
shell的使用比较简单，就像这样，并且没有数据类型的概念，所有的变量都可以当成字符串来处理:

```bash
#!/bin/bash
foo="tom"
bar="cat"
```

#### 使用变量

```bash
ABC="tom"
echo $ABC #使用变量前面加$美元符号
echo "ABC=$ABC" #可以直接在字符串里面引用
echo "ABC=${ABC}" #但是建议把变量名字用{}包起来
```

#### 只读变量

```bash
ABC="tom"
echo "ABC=${ABC}"
readOnly ABC #设置只读
ABC="CAT" #会报错，因为设置了只读，不能修改
```

#### 删除变量

```bash
ABC="tom"
echo "ABC=${ABC}"
unset ABC #删除
echo "ABC=$ABC"
echo "ABC=${ABC}"
```

### Shell 的字符串

### 判断字符串为空

```bash
#!/bin/sh

STRING=

if [ -z "$STRING" ]; then
    echo "STRING is empty"
fi

if [ -n "$STRING" ]; then
    echo "STRING is not empty"
fi
```

```bash
使用字符串

NAME="tom"
  
A=my #你甚至可以不用引号，但是字符串当中不能有空格，这种方式也不推荐
  
B='my name is ${NAME}' #变量不会被解析
  
C="my name is ${NAME}" #变量会解析
  
echo $A
  
echo $B
  
echo $C
```
<https://my.oschina.net/u/2428064/blog/3045121>

## string

### Replace

用法

```bash
${parameter/pattern/string}
```

使用

```bash
$ a=/data/wxnacy/data/log/log.txt
$ echo ${a/data/User}                # 将第一个 data 替换为 User
/User/wxnacy/data/log/log.txt

$ echo ${a//data/User}               # 将全部 data 替换为 User
/User/wxnacy/User/log/log.txt

$ echo ${a/#\/data/\/User}           # 匹配开头 /data 替换为 /User (/ 需要转义) 
/User/wxnacy/data/log/log.txt

$ echo ${a/%log.txt/User}            # 匹配结尾 log.txt 替换为 User
/data/wxnacy/data/log/User
其他方法

还有一种方法是利用 sed 来实现
 
$ echo $a | sed -e "s/data/User/g"
/User/wxnacy/User/log/log.txt
```

### 16进制转换成10进制

    printf %d 0x45b9

### 10进制转换成16进制

    printf "%x\n" tid

### 文件,目录

```bash
#如果文件夹不存在，创建文件夹
if [ ! -d "/myfolder" ]; then
  mkdir /myfolder
fi
```

### 判断单双周

```bash
if [ $(expr $(date +%W) \% 2) -eq 0 ] ; then
    echo "foo"
else
    echo "bar"
fi
```

### shell脚本中echo显示内容带颜色

shell脚本中echo显示内容带颜色显示,echo显示带颜色，需要使用参数-e
格式如下:  

    echo -e "\033[字背景颜色；文字颜色m字符串\033[0m" 
例如:  

    echo -e "\033[41;36m something here \033[0m" 
其中41的位置代表底色， 36的位置是代表字的颜色
注:  

1. 字背景颜色和文字颜色之间是英文的""
2. 文字颜色后面有个m
3. 字符串前后可以没有空格，如果有的话，输出也是同样有空格
下面是相应的字和背景颜色，可以自己来尝试找出不同颜色搭配

例

        echo -e "\033[31m 红色字 \033[0m" 
        echo -e "\033[34m 黄色字 \033[0m" 
        echo -e "\033[41;33m 红底黄字 \033[0m" 
        echo -e "\033[41;37m 红底白字 \033[0m" 
        字颜色: 30—–37 

echo -e "\033[30m 黑色字 \033[0m"
echo -e "\033[31m 红色字 \033[0m"
echo -e "\033[32m 绿色字 \033[0m"
echo -e "\033[33m 黄色字 \033[0m"
echo -e "\033[34m 蓝色字 \033[0m"
echo -e "\033[35m 紫色字 \033[0m"
echo -e "\033[36m 天蓝字 \033[0m"

字背景颜色范围: 40—–47

复制代码
echo -e "\033[40;37m 黑底白字 \033[0m"
echo -e "\033[41;37m 红底白字 \033[0m"
echo -e "\033[42;37m 绿底白字 \033[0m"
echo -e "\033[43;37m 黄底白字 \033[0m"
echo -e "\033[44;37m 蓝底白字 \033[0m"
echo -e "\033[45;37m 紫底白字 \033[0m"
echo -e "\033[46;37m 天蓝底白字 \033[0m"
echo -e "\033[47;30m 白底黑字 \033[0m"
复制代码
最后面控制选项说明

复制代码
\33[0m 关闭所有属性
\33[1m 设置高亮度
\33[4m 下划线
\33[5m 闪烁
\33[7m 反显
\33[8m 消隐
\33[30m — \33[37m 设置前景色
\33[40m — \33[47m 设置背景色
\33[nA 光标上移n行
\33[nB 光标下移n行
\33[nC 光标右移n行
\33[nD 光标左移n行
\33[y;xH设置光标位置
\33[2J 清屏
\33[K 清除从光标到行尾的内容
\33[s 保存光标位置
\33[u 恢复光标位置
\33[?25l 隐藏光标
\33[?25h 显示光标

### sleep

休眠5分钟,  s 为秒，m 为 分钟，h 为小时，d 为日数
sleep 5m

### 数组

```bash
my_array=(A B "C" D)

for element in ${my_array[@]}
#也可以写成for element in ${my_array[*]}
do
echo $element
done

echo "第一个元素为: ${my_array[0]}"
```

### 单引号内引入变量

```bash
#!/bin/bash

i=10
echo $i
echo '$i'
echo '$i is : '$i''

#执行结果
# ./test.sh 
10
$i
$i is : 10
单引号内嵌套单引号即可使用变量。
```

### 查看当前使用的shell

```bash
echo $SHELL
ps |  grep $$  |  awk '{print $4}'
```

命令行式shell (Command Line Interface shell ，即CLI shell)
  
也就是通过命令行和计算机交互的shell。 Windows NT 系统下有 cmd.exe (命令提示字符) 和近年来微软大力推广的 Windows PowerShell。 Linux下有bash / sh / ksh / csh/zsh等 一般情况下，习惯把命令行shell (CLI shell) 直接称做shell，以后，如果没有特别说明，shell就是指 CLI shell，后文也是主要讲Linux下的 CLI shell。

### 查看系统里有几种shell

```bash
cat /etc/shells
```

3.1、bash
  
Bourne Again Shell 用来替代Bourne shell，也是目前大多数Linux系统默认的shell。

3.2、sh
  
Bourne Shell 是一个比较老的shell，目前已经被/bin/bash所取代，在很多linux系统上，sh已经是一个指向bash的链接了。 下面是CentOS release 6.5 的系统

sh_to_bash

3.3、csh/tcsh
  
C shell 使用的是"类C"语法,csh是具有C语言风格的一种shell，tcsh是增强版本的csh，目前csh已经很少使用了。

3.4、ksh
  
最早，bash交互体验很好，csh作为非交互式使用很爽，ksh就吸取了2者的优点。

## zsh
  
zsh 本身是不兼容bash的，但是他可以使用仿真模式 (emulation mode) 来模拟 bash等，基本可以实现兼容。 zsh拥有很强大的提示和插件功能，推荐在终端的交互式使用中使用zsh，再安利一个插件Oh My Zsh 其实我个人的理解是，在终端中使用 shell，基本上只是调用各种命令，比如: curl cat ls等等，基本不会使用到 zsh的编程，所以终端中使用zsh是可以的。但是在写shell脚本的时候，需要考虑兼容性， 最主流的还是 bash shell，所以，后文我们介绍的shell脚本也是bash shell的。

执行并获取返回结果，有点类似 JavaScript 的eval函数。

```bash
# !/bin/bash
  
dt=`date` #反引号内的字符串会当作shell执行 ，并且返回结果。
  
echo "dt=${dt}"
```

## 逻辑与，或表达式

```bash
#与&&: 
if [ $str=a -a $str=b ] 
if [ $str=a ] && [  $str=b ]

#或||: 
if [ $str=a -o $str=b ] 
if [ $str=a ] || [  $str=b ]
```

### 字符串长度

```bash
${\#}
```

### 模式匹配截断

<https://blog.csdn.net/K346K346/article/details/51819236>

### 以-分隔取最后一段字符串

模式匹配截断，用法${variable##pattern} 这种模式时，shell在variable中查找给定的模式pattern，如果是存在，就从命令行把variable中的内容去掉左边最长的匹配模式。不改变原变量。

```bash
    a="foo-bar-foobar" && a="${a##*-}" && echo "${a}"
    # 输出
    foobar
```

### 以-分隔去掉第一段

模式匹配截断，用法${variable#pattern} 这种模式时，shell在variable中查找给定的模式pattern，如果找到，就从命令行把variable中的内容去掉左边最短的匹配模式。不改变原变量。

```bash
    a="foo-bar-foobar" && a="${a#*-}" && echo "${a}"
    # 输出
    foo
```

### 去掉最后一段

    a="foo-bar-foobar" && a="${a%-*}" && echo "${a}"
    # 输出
    foo-bar

<https://stackoverflow.com/questions/16153446/bash-last-index-of>

### Shell中去除字符串前后空格

    echo ' A B C ' | awk '{gsub(/^\s+|\s+$/, "");print}'

# 将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法:

value=`pwd`

# 将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法:

value=`pwd`

### 字符串连接

    strA="aaa"
    strB="bbb"
    strC=$strA$strB

### shell变量

定义变量时，变量名不加美元符号

    key0="value0"

注意，变量名和等号之间不能有空格，这可能和你熟悉的所有编程语言都不一样。同时，变量名的命名须遵循如下规则:

命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
中间不能有空格，可以使用下划线 (_) 。
不能使用标点符号。
不能使用bash里的关键字 (可用help命令查看保留关键字) 。

#### 可以用语句给变量赋值

    for file in `ls /etc`
    或
    for file in $(ls /etc)

```bash
$var
${var}
${var:start_index}
${var:-newstring}

```

### 整数比较

    -eq       等于,如:if [ "$a" -eq "$b" ] 
    -ne       不等于,如:if [ "$a" -ne "$b" ] 
    -gt       大于,如:if [ "$a" -gt "$b" ] 
    -ge       大于等于,如:if [ "$a" -ge "$b" ] 
    -lt       小于,如:if [ "$a" -lt "$b" ] 
    -le       小于等于,如:if [ "$a" -le "$b" ] 
    <       小于(需要双括号),如:(("$a" < "$b")) 
    <=       小于等于(需要双括号),如:(("$a" <= "$b")) 
    >       大于(需要双括号),如:(("$a" > "$b")) 
    >=       大于等于(需要双括号),如:(("$a" >= "$b")) 

### 字符串比较

    =       等于,如:if [ "$a" = "$b" ] 
    ==      等于,如:if [ "$a" == "$b" ],与=等价 
        注意:==的功能在[[]]和[]中的行为是不同的,如下: 
        1 [[ $a == z* ]]    # 如果$a以"z"开头(模式匹配)那么将为 true 
        2 [[ $a == "z*" ]] # 如果$a等于z*(字符匹配),那么结果为true 
        3 
        4 [ $a == z* ]      # File globbing 和word splitting将会发生 
        5 [ "$a" == "z*" ] # 如果$a等于z*(字符匹配),那么结果为true 
        一点解释,关于File globbing是一种关于文件的速记法,比如"*.c"就是,再如~也是. 
        但是file globbing并不是严格的正则表达式,虽然绝大多数情况下结构比较像. 
    !=       不等于,如:if [ "$a" != "$b" ] 
        这个操作符将在[[]]结构中使用模式匹配. 
    <       小于,在ASCII字母顺序下.如: 
        if [[ "$a" < "$b" ]] 
        if [ "$a" \< "$b" ] 
        注意:在[]结构中"<"需要被转义. 
    >       大于,在ASCII字母顺序下.如: 
        if [[ "$a" > "$b" ]] 
        if [ "$a" \> "$b" ] 
        注意:在[]结构中">"需要被转义. 
        具体参考Example 26-11来查看这个操作符应用的例子. 
    -z       字符串为"null".就是长度为0. 
    -n       字符串不为"null" 
        注意: 
        使用-n在[]结构中测试必须要用""把变量引起来.使用一个未被""的字符串来使用! -z 
        或者就是未用""引用的字符串本身,放到[]结构中。虽然一般情况下可 
        以工作,但这是不安全的.习惯于使用""来测试字符串是一种好习惯.

### 参数

    [-p file] 如果 file 存在且是一个名字管道 (F如果O) 则为真 
    [-r file] 如果file存在且是可读的则为真 
    [-s file] 如果file存在且大小不为0则为真 
    [-t FD] 如果文件描述符FD打开且指向一个终端则为真 
    [-u file] 如果file存在且设置了SUID (set userID) 则为真 
    [-w file] 如果file存在且是可写的则为真 
    [-x file] 如果file存在且是可执行的则为真 
    [-O file] 如果file存在且属有效用户ID则为真 
    [-G file] 如果file存在且属有效用户组则为真 
    [-L file] 如果file存在且是一个符号连接则为真 
    [-N file] 如果file存在and has been mod如果ied since it was last read 则为真 
    [-S file] 如果file存在且是一个 socket 则为真 
    [file1 –nt file2] 如果file1 has been changed more recently than file2或者file1 exists and file2 does not则为真 
    [file1 –ot file2] 如果file1比file2要老，或者file2存在且file1不存在则为真 
    [file1 –ef file2] 如果file1和file2指向相同的设备和节点号则为真 
    [-o optionname] 如果shell选项"optionname"开启则为真 
    [-z string] "string"的长度为零则为真 
    [-n string] or [string] "string"的长度为非零non-zero则为真 
    [sting1==string2] 如果2个字符串相同。"="may be used instead of "=="for strict posix compliance则为真 
    [string1!=string2] 如果字符串不相等则为真 
    [string1<string2] 如果"string1"sorts before"string2"lexicographically in the current locale则为真 
    [arg1 OP arg2] "OP"is one of –eq,-ne,-lt,-le,-gt or –ge.These arithmetic binary oprators return true if "arg1"is equal to,not equal to,less than,less than or equal to,greater than,or greater than or equal to"agr2",respectively."arg1"and "agr2"are integers. 

---
版权声明: 本文为CSDN博主「无知的蜗牛」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/weixin_37998647/java/article/details/79718821>

## grep 操作的返回值

如果有匹配的字符串，返回值是 0， 还会打印出匹配字符串的行。
  
如果没有匹配， 会返回1。

## shell, if/else
  
和C语言类似，在Shell中用if、then、elif、else、fi这几条命令实现分支控制。这种流程控制语句本质上也是由若干条Shell命令组成的，例如

### if

```bash
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

### if else if else

```bash
    if ... fi 语句；
    if ... else ... fi 语句；
    if ... elif ... else ... fi 语句
```

其实是三条命令，if [ -f ~/.bashrc ]是第一条，then . ~/.bashrc是第二条，fi是第三条。如果两条命令写在同一行则需要用;号隔开，一行只写一条命令就不需要写;号了，另外，then后面有换行，但这条命令没写完，Shell会自动续行，把下一行接在then后面当作一条命令处理。和[命令一样，要注意命令和各参数之间必须用空格隔开。if命令的参数组成一条子命令，如果该子命令的Exit Status为0 (表示真) ，则执行then后面的子命令，如果Exit Status非0 (表示假) ，则执行elif、else或者fi后面的子命令。if后面的子命令通常是测试命令，但也可以是其它命令。Shell脚本没有{}括号，所以用fi表示if语句块的结束。见下例:

# ! /bin/sh
  
if [ -f /bin/bash ]
  
then echo "/bin/bash is a file"
  
else echo "/bin/bash is NOT a file"
  
fi
  
if :; then echo "always true"; fi
  
:是一个特殊的命令，称为空命令，该命令不做任何事，但Exit Status总是真。此外，也可以执行/bin/true或/bin/false得到真或假的Exit Status。再看一个例子:

# ! /bin/sh

echo "Is it morning? Please answer yes or no."
  
read YES_OR_NO
  
if [ "$YES_OR_NO" = "yes" ]; then

echo "Good morning!"
  
elif [ "$YES_OR_NO" = "no" ]; then

echo "Good afternoon!"
  
else

echo "Sorry, $YES_OR_NO not recognized. Enter yes or no."

exit 1
  
fi
  
exit 0
  
上例中的read命令的作用是等待用户输入一行字符串，将该字符串存到一个Shell变量中。

此外，Shell还提供了&&和||语法，和C语言类似，具有Short-circuit特性，很多Shell脚本喜欢写成这样:

test "$(whoami)" != 'root' && (echo you are using a non-privileged account; exit 1)
  
&&相当于"if…then…"，而||相当于"if not…then…"。&&和||用于连接两个命令，而上面讲的-a和-o仅用于在测试表达式中连接两个测试条件，要注意它们的区别，例如，

test "$VAR" -gt 1 -a "$VAR" -lt 3
  
和以下写法是等价的

test "$VAR" -gt 1 && test "$VAR" -lt 3

—

把whoami的结果赋给A

eval A=`whoami`

获取当前目录

${PWD}

判断目录是否存在:

if [ ! -d /mnt/u ];
  
判断目录非空

# 如果结果为0则目录为空
  
ls dirname|wc -l

文件比较运算符
  
-e filename 如果 filename 存在，则为真 [ -e /var/log/syslog ]
  
-d filename 如果 filename 为目录，则为真 [ -d /tmp/mydir ]
  
-f filename 如果 filename 为常规文件，则为真 [ -f /usr/bin/grep ]
  
-L filename 如果 filename 为符号链接，则为真 [ -L /usr/bin/grep ]
  
-r filename 如果 filename 可读，则为真 [ -r /var/log/syslog ]
  
-w filename 如果 filename 可写，则为真 [ -w /var/mytmp.txt ]
  
-x filename 如果 filename 可执行，则为真 [ -L /usr/bin/grep ]
  
filename1 -nt filename2 如果 filename1 比 filename2 新，则为真 [ /tmp/install/etc/services -nt /etc/services ]
  
filename1 -ot filename2 如果 filename1 比 filename2 旧，则为真 [ /boot/bzImage -ot arch/i386/boot/bzImage ]
  
字符串比较运算符  (请注意引号的使用，这是防止空格扰乱代码的好方法)
  
-z string 如果 string 长度为零，则为真 [ -z "$myvar" ]
  
-n string 如果 string 长度非零，则为真 [ -n "$myvar" ]
  
string1 = string2 如果 string1 与 string2 相同，则为真 [ "$myvar" = "one two three" ]
  
string1 != string2 如果 string1 与 string2 不同，则为真 [ "$myvar" != "one two three" ]
  
算术比较运算符
  
num1 -eq num2 等于 [ 3 -eq $mynum ]
  
num1 -ne num2 不等于 [ 3 -ne $mynum ]
  
num1 -lt num2 小于 [ 3 -lt $mynum ]
  
num1 -le num2 小于或等于 [ 3 -le $mynum ]
  
num1 -gt num2 大于 [ 3 -gt $mynum ]
  
num1 -ge num2 大于或等于 [ 3 -ge $mynum ]

算术运算符
  
    + - * / % 表示加减乘除和取余运算
  
+= -= *= /= 同 C 语言中的含义

位操作符

        > > > = 表示位左右移一位操作
            
        > > > & &= | |= 表示按位与、位或操作
            
        > > > ~ ! 表示非操作
            
        > > > ^ ^= 表示异或操作 

关系运算符

= == != 表示大于、小于、大于等于、小于等于、等于、不等于操作
  
&& || 逻辑与、逻辑或操作

测试命令

test命令用于检查某个条件是否成立，它可以进行数值、字符和文件3个方面的测试，其测试符和相应的功能分别如下。

 (1) 数值测试:

-eq 等于则为真。

-ne 不等于则为真。

-gt 大于则为真。

-ge 大于等于则为真。

-lt 小于则为真。

-le 小于等于则为真。

 (2) 字串测试:

= 等于则为真。

!= 不相等则为真。

-z字串 字串长度伪则为真。

-n字串 字串长度不伪则为真。

### 文件测试

-e文件名 如果文件存在则为真。

-r文件名 如果文件存在且可读则为真。

-w文件名 如果文件存在且可写则为真。

-x文件名 如果文件存在且可执行则为真。

-s文件名 如果文件存在且至少有一个字符则为真。

-d文件名 如果文件存在且为目录则为真。

-f文件名 如果文件存在且为普通文件则为真。

-c文件名 如果文件存在且为字符型特殊文件则为真。

-b文件名 如果文件存在且为块特殊文件则为真

条件变量替换:

Bash Shell可以进行变量的条件替换,既只有某种条件发生时才进行替换,替换
  
条件放在{}中.
  
(1) ${value:-word}

当变量未定义或者值为空时,返回值为word的内容,否则返回变量的值.

(2) ${value:=word}

       与前者类似,只是若变量未定义或者值为空时,在返回word的值的同时将 word赋值给value 

(3) ${value:?message}

       若变量已赋值的话,正常替换.否则将消息message送到标准错误输出(若此替换出现在Shell程序中,那么该程序将终止运行) 

(4) ${value:+word}

       若变量已赋值的话,其值才用word替换,否则不进行任何替换 

(5) ${value:offset}

       ${value:offset:length} 从变量中提取子串,这里offset和length可以是算术表达式. 

(6) ${#value}

       变量的字符个数 

(7) ${value#pattern}

       ${value##pattern} 
       去掉value中与pattern相匹配的部分,条件是value的开头与pattern相匹配 
       #与##的区别在于一个是最短匹配模式,一个是最长匹配模式. 

(8) ${value%pattern}

       ${value%%pattern} 
       于(7)类似,只是是从value的尾部于pattern相匹配,%与%%的区别与#与##一样 

(9) ${value/pattern/string}

       ${value//pattern/string} 
       进行变量内容的替换,把与pattern匹配的部分替换为string的内容,/与//的区别与上同 

注意: 上述条件变量替换中,除(2)外,其余均不影响变量本身的值

# !/bin/bash

var1="1"
  
var2="2"

下面是"与"运算符-a，另外注意，用一个test命令就可以了，还有if条件后面的分号

if test $var1 = "1"-a $var2 = "2" ; then

echo "equal"
  
fi

下面是"或"运算符 -o，有一个为真就可以

if test $var1 != "1" -o $var2 != "3" ; then

echo "not equal"
  
fi

下面是"非"运算符 ！
  
if条件是为真的时候执行，如果使用！运算符，那么原表达式必须为false

if ! test $var1 != "1"; then

echo "not 1"
  
fi

以上三个if都为真，所以三个echo都会打印

示例:

```bash
 
  
#!/bin/sh

aa="August 15, 2012"
  
bb="August 15, 20122"
  
cc="123"
  
dd="123"

# -o

if [ "$aa" = "$bb" -o "$cc" = "$dd" ]; then
      
echo "yes"
  
else
      
echo "no"
  
fi

# -a and !

if [ "$aa" != "$bb" -a "$cc" = "$dd" ]; then
      
echo "yes"
  
else
      
echo "no"
  
fi
  
运行结果: 
  
true

* * *
```

### shell字符串比较、判断是否为数字

二元比较操作符,比较变量或者比较数字.注意数字与字符串的区别.

1 整数比较

-eq 等于,如:if [ "$a" -eq "$b" ]

-ne 不等于,如:if [ "$a" -ne "$b" ]

-gt 大于,如:if [ "$a" -gt "$b" ]

-ge 大于等于,如:if [ "$a" -ge "$b" ]

-lt 小于,如:if [ "$a" -lt "$b" ]

-le 小于等于,如:if [ "$a" -le "$b" ]

< 小于(需要双括号),如:(("$a" < "$b"))

<= 小于等于(需要双括号),如:(("$a" <= "$b"))

- > 大于(需要双括号),如:(("$a" > "$b"))

> = 大于等于(需要双括号),如:(("$a" >= "$b"))

整数比较实例

[css] 
  
# !/bin/bash

file='folder_url_top24/url_usa_top24_0'
  
fileSize=`ls -l folder_url_top24/url_usa_top24_0 | awk -F '[" "]' '{print $5}'`
  
FILESIZE=1000
  
# while [ ! -f $file -o "$fileSize" -lt "$FILESIZE" ]
  
# while [ ! -f $file -o "$fileSize" -lt 1000 ]
  
while (("$fileSize" < 1000))
  
do

echo "down again..."
  
done
  
其中，下面三种整数比较都成立:
  
1) while [ ! -f $file -o "$fileSize" -lt "$FILESIZE" ]

2) while [ ! -f $file -o "$fileSize" -lt 1000 ]

3) (("$fileSize" < 1000))

推荐使用第一种

2 字符串比较
  
= 等于,如:if [ "$a" = "$b" ]

== 等于,如:if [ "$a" == "$b" ],与=等价

注意:==的功能在[[]]和[]中的行为是不同的,如下:

1 [[ $a == z* ]] # 如果$a以"z"开头(模式匹配)那么将为true

2 [[ $a == "z_" ]] # 如果$a等于z_(字符匹配),那么结果为true

3

4 [ $a == z* ] # File globbing 和word splitting将会发生

5 [ "$a" == "z_" ] # 如果$a等于z_(字符匹配),那么结果为true

一点解释,关于File globbing是一种关于文件的速记法,比如"*.c"就是,再如~也是.

但是file globbing并不是严格的正则表达式,虽然绝大多数情况下结构比较像.

!= 不等于,如:if [ "$a" != "$b" ]

这个操作符将在[[]]结构中使用模式匹配.

< 小于,在ASCII字母顺序下.如:

if [[ "$a" < "$b" ]]

if [ "$a" \< "$b" ]

注意:在[]结构中"<"需要被转义.

大于,在ASCII字母顺序下.如:
if [[ "$a" > "$b" ]]
if [ "$a" \> "$b" ]
注意:在[]结构中">"需要被转义.
具体参考Example 26-11来查看这个操作符应用的例子.

-z 字符串为"null".就是长度为0

-n 字符串不为"null"

判断shell传入的参数个数是否为空:

[python] 
  
# !/bin/bash

port=6379 # 命令行没参数，默认指定端口号为 6379
  
if [ $# -ge 1 ]; then # 命令行参数个数大于等于1，则使用传入的参数port

port=$1 # 获取指定端口号
  
fi

echo "redis port: $port"
  
redis-cli -h 172.1628.10.114 -p $port

字符串比较实例:

if [ "$var1" = "$var2" ]

```bash  
# !/bin/sh

aa="August 15, 2012"
  
bb="August 15, 2012"

if [ "$aa" = "$bb" ]; then

echo "yes"
  
else

echo "no"
  
fi

判断子字符串包含关系:  =~

代码:

[python] 
  
a1="ithomer"
  
a2="ithomer.net"
  
a3="blog.ithomer.net"

if [[ "$a3" =~ "$a1" ]]; then

echo "$a1是$a3的子串！"
  
else

echo "$a1不是$a3的子串！"
  
fi

if [[ "$a3" =~ "$a2" ]];then

echo "$a2是$a3的子串！"
  
else

echo "$a2不是$a3的子串！"
  
fi
```

注意:
  
使用-n在[]结构中测试必须要用""把变量引起来.使用一个未被""的字符串来使用! -z或者就是未用""引用的字符串本身,放到[]结构中。虽然一般情况下可以工作,但这是不安全的.习惯于使用""来测试字符串是一种好习惯.

awk '{print $2}' class.txt | grep '^[0-9.]' > res
  
<https://www.linuxquestions.org/questions/programming-9/bash-put-output-from-%60ls%60-into-an-array-346719/>
  
版权声明: 本文为CSDN博主「DevMaster」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: <https://blog.csdn.net/wncnke/java/article/details/54847140>

参考

<http://fyan.iteye.com/blog/1130034>
作者: 翔云翔云  
来源: CSDN
原文: <https://blog.csdn.net/lanyang123456/article/details/57416906>
版权声明: 本文为博主原创文章，转载请附上博文链接！
本文来自 wujiangguizhen 的CSDN 博客 ，全文地址请点击: <https://blog.csdn.net/wujiangguizhen/article/details/26992353?utm_source=copy>

---

<https://www.shellscript.sh/functions.html>
<http://www.cnblogs.com/barrychiao/archive/2012/10/22/2733210.html>
<https://www.cnblogs.com/lr-ting/archive/2013/02/28/2936792.html>

<https://wxnacy.com/2018/06/20/shell-replace/>

## 'linux #!/bin/sh'

`#!/bin/sh` 是指此脚本使用/bin/sh来解释执行，#!是特殊的表示符，其后面根的是此解释此脚本的shell的路径。 $bash $表示系统提示符，$ 表示此用户为普通用户，超级用户的提示符是＃，bash是shell的一种，是linux下最常用的一种shell，$bash的意思是执行一个子shell，此子shell为bash.

## case, esac

```bash
printf "1. Goland\n2. WebStorm\nSelect IDEs (leave blank for Goland):"

read -r ides

code=""
case $ides in
    1) code=GO
    ;;
    2) code=WS
    ;;
esac

```

## declare

`man bash`, line:2995

声明变量，设置或显示变量的值和属性。

-A 创建关联数组(associative array)（如果支持）

## Shell 函数, function

```template
[ function ] funname [()]
{
    action;
    [return int;]
}
```

```bash
# 定义函数 fun0
fun0(){
    echo "run fun0 "
}
# 调用函数 fun0
fun0

```

```bash
# 定义带参数的函数 fun0
# 在Shell中，调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...
fun0(){
    echo "run fun0 $1 "
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
}
# 调用带参数的函数 fun0
fun0 foo

```

<https://www.runoob.com/linux/linux-shell-func.html>
  
<https://wiki.jikexueyuan.com/project/shell-tutorial/shell-function-parameter.html>

## shell 把命令输出结果存入变量

```bash
  
var=$(ls -lR|grep "^d"|wc -l)
  
或者另外一种 不建议的方式
  
var=\`ls -lR|grep "^d"|wc -l\`
  
```

<https://blog.csdn.net/baidu_35757025/article/details/64440047>
