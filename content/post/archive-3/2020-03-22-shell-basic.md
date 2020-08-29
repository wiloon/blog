---
title: shell basic
author: wiloon
type: post
date: 2020-03-22T10:27:45+00:00
url: /?p=15803
categories:
  - Uncategorized

---
### 逻辑与，或表达式
    与&&：
    1）if [ $str=a -a $str=b ] 
    2）if [ $str=a ] && [  $str=b ]
    
    或||：
    1）if [ $str=a -o $str=b ] 
    2）if [ $str=a ] || [  $str=b ]


### 以-分隔取最后一段字符串
    a="foo-bar-foobar" && a="${a##*-}" && echo "${a}"
    # 输出
    foobar

### 以-分隔去掉第一段
    a="foo-bar-foobar" && a="${a#*-}" && echo "${a}"
    # 输出
    foo
### 去掉最后一段
    a="foo-bar-foobar" && a="${a%-*}" && echo "${a}"
    # 输出
    foo-bar
https://stackoverflow.com/questions/16153446/bash-last-index-of

### Shell中去除字符串前后空格
    echo ' A B C ' | awk '{gsub(/^\s+|\s+$/, "");print}'

### 判断字符串为空
    #!/bin/sh

    STRING=

    if [ -z "$STRING" ]; then
        echo "STRING is empty"
    fi

    if [ -n "$STRING" ]; then
        echo "STRING is not empty"
    fi

#将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法：

value=`pwd`

#将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法：

value=`pwd`

### 字符串连接
    strA="aaa"
    strB="bbb"
    strC=$strA$strB

### 判断指定文件中是否包含指定的字符串

```bash
grep "prod" /path/to/file/web.xml > /dev/null
if [ $? -eq 0 ]; then
    echo "Found!"
else
    echo "Not found!"
fi
```

### 判断字符串是否相等

```bash
#判断字符串是否相等
if [ "$A" = "$B" ];then
echo "[ = ]"
fi
```

### 检查目录是否存在
```bash
# check if directory is exist
if [ ! -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
fi

```

### shell变量

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
    ==       等于,如:if [ "$a" == "$b" ],与=等价 
        注意:==的功能在[[]]和[]中的行为是不同的,如下: 
        1 [[ $a == z* ]]    # 如果$a以"z"开头(模式匹配)那么将为true 
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

### 特殊变量：Shell $0, $#, $*, $@, $?, $$和命令行参数

    变量	含义
    $0	当前脚本的文件名
    $n	传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1，第二个参数是$2。
    $#	传递给脚本或函数的参数个数。
    $*	传递给脚本或函数的所有参数。
    $@	传递给脚本或函数的所有参数。被双引号(" ")包含时，与 $* 稍有不同，下面将会讲到。
    $?	上个命令的退出状态，或函数的返回值。
    $$	当前Shell进程ID。对于 Shell 脚本，就是这些脚本所在的进程ID。

### 参数 
    -p file] 如果file存在且是一个名字管道（F如果O）则为真 
    管道是linux里面进程间通信的一种方式，其他的还有像信号（signal）、信号量、消息队列、共享内存、套接字（socket）等。 
    [-r file] 如果file存在且是可读的则为真 
    [-s file] 如果file存在且大小不为0则为真 
    [-t FD] 如果文件描述符FD打开且指向一个终端则为真 
    [-u file] 如果file存在且设置了SUID（set userID）则为真 
    [-w file] 如果file存在且是可写的则为真 
    [-x file] 如果file存在且是可执行的则为真 
    [-O file] 如果file存在且属有效用户ID则为真 
    [-G file] 如果file存在且属有效用户组则为真 
    [-L file] 如果file存在且是一个符号连接则为真 
    [-N file] 如果file存在and has been mod如果ied since it was last read则为真 
    [-S file] 如果file存在且是一个套接字则为真 
    [file1 –nt file2] 如果file1 has been changed more recently than file2或者file1 exists and file2 does not则为真 
    [file1 –ot file2] 如果file1比file2要老，或者file2存在且file1不存在则为真 
    [file1 –ef file2] 如果file1和file2指向相同的设备和节点号则为真 
    [-o optionname] 如果shell选项“optionname”开启则为真 
    [-z string] “string”的长度为零则为真 
    [-n string] or [string] “string”的长度为非零non-zero则为真 
    [sting1==string2] 如果2个字符串相同。“=”may be used instead of “==”for strict posix compliance则为真 
    [string1!=string2] 如果字符串不相等则为真 
    [string1<string2] 如果“string1”sorts before“string2”lexicographically in the current locale则为真 
    [arg1 OP arg2] “OP”is one of –eq,-ne,-lt,-le,-gt or –ge.These arithmetic binary oprators return true if “arg1”is equal to,not equal to,less than,less than or equal to,greater than,or greater than or equal to“agr2”,respectively.“arg1”and “agr2”are integers. 

---
版权声明：本文为CSDN博主「无知的蜗牛」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_37998647/java/article/details/79718821
