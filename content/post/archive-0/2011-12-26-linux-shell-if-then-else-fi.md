---
title: linux shell/bash scripting
author: wiloon
type: post
date: 2011-12-26T07:49:00+00:00
url: /?p=2015
categories:
  - Linux
tags:
  - Shell

---
### 判断指定文件中是否包含指定的字符串

```bashgrep "prod" /home/admin/gitrep/otp/otp-webapp-api/src/main/webapp/WEB-INF/web.xml &gt; /dev/null
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

1.并且
  
条件 c1并且条件c2

方式一： -a: and

if [ c1 -a c2 ]; then
  
…
  
fi
  
1
  
2
  
3
  
方式二：

if [ c1 && c2 ]; then
  
…
  
fi
  
1
  
2
  
3
  
2.或者
  
条件 c1或者 条件c2

方式一：-o: or

if [ c1 -o c2 ]; then
  
…
  
fi
  
1
  
2
  
3
  
方式二：

if [ c1 || c2 ]; then
  
…
  
fi

参考

## http://fyan.iteye.com/blog/1130034

作者：翔云翔云
  
来源：CSDN
  
原文：https://blog.csdn.net/lanyang123456/article/details/57416906
  
版权声明：本文为博主原创文章，转载请附上博文链接！

## grep

grep操作的返回值：
  
如果有匹配的字符串，返回值是0， 还会打印出匹配字符串的行。
  
如果没有匹配， 会返回1。

本文来自 wujiangguizhen 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/wujiangguizhen/article/details/26992353?utm_source=copy

https://www.shellscript.sh/functions.html

```bash
# check if directory is exist
if [ ! -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
fi

```

shell变量

```bash$var
${var}
${var:start_index}
${var:-newstring}

```

<http://www.cnblogs.com/barrychiao/archive/2012/10/22/2733210.html>{.wp-editor-md-post-content-link}

if/else
  
和C语言类似，在Shell中用if、then、elif、else、fi这几条命令实现分支控制。这种流程控制语句本质上也是由若干条Shell命令组成的，例如

<pre><code class="language-shell line-numbers">if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

其实是三条命令，if [ -f ~/.bashrc ]是第一条，then . ~/.bashrc是第二条，fi是第三条。如果两条命令写在同一行则需要用;号隔开，一行只写一条命令就不需要写;号了，另外，then后面有换行，但这条命令没写完，Shell会自动续行，把下一行接在then后面当作一条命令处理。和[命令一样，要注意命令和各参数之间必须用空格隔开。if命令的参数组成一条子命令，如果该子命令的Exit Status为0（表示真），则执行then后面的子命令，如果Exit Status非0（表示假），则执行elif、else或者fi后面的子命令。if后面的子命令通常是测试命令，但也可以是其它命令。Shell脚本没有{}括号，所以用fi表示if语句块的结束。见下例：

#! /bin/sh
  
if [ -f /bin/bash ]
  
then echo "/bin/bash is a file&#8221;
  
else echo "/bin/bash is NOT a file&#8221;
  
fi
  
if :; then echo "always true&#8221;; fi
  
:是一个特殊的命令，称为空命令，该命令不做任何事，但Exit Status总是真。此外，也可以执行/bin/true或/bin/false得到真或假的Exit Status。再看一个例子：

#! /bin/sh

echo "Is it morning? Please answer yes or no.&#8221;
  
read YES\_OR\_NO
  
if [ "$YES\_OR\_NO&#8221; = "yes&#8221; ]; then
    
echo "Good morning!&#8221;
  
elif [ "$YES\_OR\_NO&#8221; = "no&#8221; ]; then
    
echo "Good afternoon!&#8221;
  
else
    
echo "Sorry, $YES\_OR\_NO not recognized. Enter yes or no.&#8221;
    
exit 1
  
fi
  
exit 0
  
上例中的read命令的作用是等待用户输入一行字符串，将该字符串存到一个Shell变量中。

此外，Shell还提供了&&和||语法，和C语言类似，具有Short-circuit特性，很多Shell脚本喜欢写成这样：

test "$(whoami)&#8221; != &#8216;root&#8217; && (echo you are using a non-privileged account; exit 1)
  
&&相当于“if…then…”，而||相当于“if not…then…”。&&和||用于连接两个命令，而上面讲的-a和-o仅用于在测试表达式中连接两个测试条件，要注意它们的区别，例如，

test “$VAR” -gt 1 -a “$VAR” -lt 3
  
和以下写法是等价的

test “$VAR” -gt 1 && test “$VAR” -lt 3

—

把whoami的结果赋给A

eval A=`whoami`

获取当前目录

${PWD}

判断目录是否存在:

if [ ! -d /mnt/u ];
  
判断目录非空

#如果结果为0则目录为空
  
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
  
字符串比较运算符 （请注意引号的使用，这是防止空格扰乱代码的好方法）
  
-z string 如果 string 长度为零，则为真 [ -z "$myvar&#8221; ]
  
-n string 如果 string 长度非零，则为真 [ -n "$myvar&#8221; ]
  
string1 = string2 如果 string1 与 string2 相同，则为真 [ "$myvar&#8221; = "one two three&#8221; ]
  
string1 != string2 如果 string1 与 string2 不同，则为真 [ "$myvar&#8221; != "one two three&#8221; ]
  
算术比较运算符
  
num1 -eq num2 等于 [ 3 -eq $mynum ]
  
num1 -ne num2 不等于 [ 3 -ne $mynum ]
  
num1 -lt num2 小于 [ 3 -lt $mynum ]
  
num1 -le num2 小于或等于 [ 3 -le $mynum ]
  
num1 -gt num2 大于 [ 3 -gt $mynum ]
  
num1 -ge num2 大于或等于 [ 3 -ge $mynum ]

算术运算符
  
+ &#8211; * / % 表示加减乘除和取余运算
  
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

（1）数值测试：

　　-eq 等于则为真。

　　-ne 不等于则为真。

　　-gt 大于则为真。

　　-ge 大于等于则为真。

　　-lt 小于则为真。

　　-le 小于等于则为真。

（2）字串测试：

　　= 等于则为真。

　　!= 不相等则为真。

　　-z字串 字串长度伪则为真。

　　-n字串 字串长度不伪则为真。

（3）文件测试：

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

#!/bin/bash

var1=&#8221;1"
  
var2=&#8221;2"

下面是“与”运算符-a，另外注意，用一个test命令就可以了，还有if条件后面的分号

if test $var1 = "1&#8221;-a $var2 = "2&#8221; ; then
     
echo "equal&#8221;
  
fi

下面是“或”运算符 -o，有一个为真就可以

if test $var1 != "1&#8221; -o $var2 != "3&#8221; ; then
     
echo "not equal&#8221;
  
fi

下面是“非”运算符 ！
  
if条件是为真的时候执行，如果使用！运算符，那么原表达式必须为false

if ! test $var1 != "1&#8221;; then
     
echo "not 1"
  
fi

以上三个if都为真，所以三个echo都会打印

示例：

[javascript] view plain copy
  
#!/bin/sh

aa=&#8221;August 15, 2012&#8221;
  
bb=&#8221;August 15, 20122"
  
cc=&#8221;123"
  
dd=&#8221;123"

# -o

if [ "$aa&#8221; = "$bb&#8221; -o "$cc&#8221; = "$dd&#8221; ]; then
      
echo "yes&#8221;
  
else
      
echo "no&#8221;
  
fi

# -a and !

if [ "$aa&#8221; != "$bb&#8221; -a "$cc&#8221; = "$dd&#8221; ]; then
      
echo "yes&#8221;
  
else
      
echo "no&#8221;
  
fi
  
运行结果：
  
true

* * *

shell字符串比较、判断是否为数字

二元比较操作符,比较变量或者比较数字.注意数字与字符串的区别.

1 整数比较

-eq 等于,如:if [ "$a&#8221; -eq "$b&#8221; ]

-ne 不等于,如:if [ "$a&#8221; -ne "$b&#8221; ]

-gt 大于,如:if [ "$a&#8221; -gt "$b&#8221; ]

-ge 大于等于,如:if [ "$a&#8221; -ge "$b&#8221; ]

-lt 小于,如:if [ "$a&#8221; -lt "$b&#8221; ]

-le 小于等于,如:if [ "$a&#8221; -le "$b&#8221; ]

< 小于(需要双括号),如:(("$a&#8221; < "$b&#8221;))

<= 小于等于(需要双括号),如:(("$a&#8221; <= "$b&#8221;))

>       大于(需要双括号),如:(("$a" > "$b"))
>     
> 
> = 大于等于(需要双括号),如:(("$a&#8221; >= "$b&#8221;)) 

整数比较实例

[css] view plain copy
  
#!/bin/bash

file=&#8217;folder\_url\_top24/url\_usa\_top24_0&#8242;
  
fileSize=`ls -l folder_url_top24/url_usa_top24_0 | awk -F '[" "]' '{print $5}'`
  
FILESIZE=1000
  
#while [ ! -f $file -o "$fileSize&#8221; -lt "$FILESIZE&#8221; ]
  
#while [ ! -f $file -o "$fileSize&#8221; -lt 1000 ]
  
while (("$fileSize&#8221; < 1000))
  
do
      
echo "down again&#8230;&#8221;
  
done
  
其中，下面三种整数比较都成立：
  
1） while [ ! -f $file -o "$fileSize&#8221; -lt "$FILESIZE&#8221; ]

2） while [ ! -f $file -o "$fileSize&#8221; -lt 1000 ]

3） (("$fileSize&#8221; < 1000))

推荐使用第一种

2 字符串比较
  
= 等于,如:if [ "$a&#8221; = "$b&#8221; ]

== 等于,如:if [ "$a&#8221; == "$b&#8221; ],与=等价
         
注意:==的功能在[[]]和[]中的行为是不同的,如下:
         
1 [[ $a == z* ]] # 如果$a以&#8221;z&#8221;开头(模式匹配)那么将为true
         
2 [[ $a == "z_&#8221; ]] # 如果$a等于z_(字符匹配),那么结果为true
         
3
         
4 [ $a == z* ] # File globbing 和word splitting将会发生
         
5 [ "$a&#8221; == "z_&#8221; ] # 如果$a等于z_(字符匹配),那么结果为true
         
一点解释,关于File globbing是一种关于文件的速记法,比如&#8221;*.c&#8221;就是,再如~也是.
         
但是file globbing并不是严格的正则表达式,虽然绝大多数情况下结构比较像.

!= 不等于,如:if [ "$a&#8221; != "$b&#8221; ]
         
这个操作符将在[[]]结构中使用模式匹配.

< 小于,在ASCII字母顺序下.如:
         
if [[ "$a&#8221; < "$b&#8221; ]]
         
if [ "$a&#8221; \< "$b&#8221; ]
         
注意:在[]结构中&#8221;<"需要被转义.

>       大于,在ASCII字母顺序下.如:
>        if [[ "$a" > "$b" ]]
>        if [ "$a" \> "$b" ]
>        注意:在[]结构中">"需要被转义.
>        具体参考Example 26-11来查看这个操作符应用的例子.
>     

-z 字符串为&#8221;null&#8221;.就是长度为0

-n 字符串不为&#8221;null&#8221;

判断shell传入的参数个数是否为空：

[python] view plain copy
  
#!/bin/bash

port=6379 # 命令行没参数，默认指定端口号为 6379
  
if [ $# -ge 1 ]; then # 命令行参数个数大于等于1，则使用传入的参数port
      
port=$1 # 获取指定端口号
  
fi

echo "redis port: $port&#8221;
  
redis-cli -h 172.1628.10.114 -p $port

字符串比较实例：

if [ "$var1&#8221; = "$var2" ]

代码：

[css] view plain copy
  
#!/bin/sh

aa=&#8221;August 15, 2012&#8221;
  
bb=&#8221;August 15, 2012"

if [ "$aa&#8221; = "$bb&#8221; ]; then
      
echo "yes&#8221;
  
else
      
echo "no&#8221;
  
fi

判断子字符串包含关系： =~

代码：

[python] view plain copy
  
a1=&#8221;ithomer&#8221;
  
a2=&#8221;ithomer.net&#8221;
  
a3=&#8221;blog.ithomer.net&#8221;

if [[ "$a3&#8221; =~ "$a1&#8221; ]]; then
           
echo "$a1是$a3的子串！&#8221;
  
else
           
echo "$a1不是$a3的子串！&#8221;
  
fi

if [[ "$a3&#8221; =~ "$a2&#8221; ]];then
           
echo "$a2是$a3的子串！&#8221;
  
else
           
echo "$a2不是$a3的子串！&#8221;
  
fi

注意:
  
使用-n在[]结构中测试必须要用&#8221;&#8221;把变量引起来.使用一个未被&#8221;&#8221;的字符串来使用! -z或者就是未用&#8221;&#8221;引用的字符串本身,放到[]结构中。虽然一般情况下可以工作,但这是不安全的.习惯于使用&#8221;&#8221;来测试字符串是一种好习惯.

awk &#8216;{print $2}&#8217; class.txt | grep &#8216;^[0-9.]&#8217; > res
  
https://www.linuxquestions.org/questions/programming-9/bash-put-output-from-%60ls%60-into-an-array-346719/

————————————————
  
版权声明：本文为CSDN博主「DevMaster」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接：https://blog.csdn.net/wncnke/java/article/details/54847140