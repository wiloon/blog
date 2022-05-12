---
title: 计算器 bc, expr、dc、echo、awk)
author: "-"
date: 2012-03-18T04:41:13+00:00
url: calculator
categories:
  - Linux
tags:
  - reprint
---
## 计算器 bc, expr、dc、echo、awk)
## Linux下的计算器 bc, expr、dc、echo、awk)
### bc
```bash
# install bc
sudo pacman -S bc
# 将16进制的A7输出为10进制, 注意，英文只能大写
echo "ibase=16;A7" |bc

```
bc在默认的情况下是个交互式的指 令。在bc工作环境下，可以使用以下计算符号: 
  
```
+ 加法
– 减法
* 乘法
/ 除法
^ 指数
% 余数
```

示例: 
```bash
bc
#bc 1.07.1
#Copyright 1991-1994, 1997, 1998, 2000, 2004, 2006, 2008, 2012-2017 Free Software Foundation, Inc.
#This is free software with ABSOLUTELY NO WARRANTY.
#For details type `warranty'.

2.7*8
# 21.6

3+6 <=加法
  
4+2_3 <=加法、乘法
  
(4+2)_3 <=加法、乘法 (优先) 
  
4_6/8 <=乘法、除法
  
10^3 <=指数
  
1000
  
18%5 <=余数
  
3+4;5_2;5^2;18/4 <=一行输入多个计算，用;相隔。
  
quit <=退出

bc
scale=3 <=设小数位
  
1/3
  
.333
  
quit


```
  
以上是交互的计算，那到也可以不进行交互而直接计算出结果。
  
A. 用echo和|法，如: 

```bash
echo "(6+3)*2" |bc
#18
```

# echo 15/4 |bc

3

# echo "scale=2;15/4" |bc

3.75

# echo "3+4;5*2;5^2;18/4" |bc

另外，bc除了scale来设定小数位之外，还有ibase和obase来其它进制的运算。
  
如: 
  


//将2进制的11111111转成10进制

# echo "ibase=2;11111111" |bc

//输入为16进制，输出为2进制

# echo "ibase=16;obase=2;B5-A4" |bc

10001
  
对于bc还有补充，在bc –help中还可以发现: bc后可以接文件名。如: 

# more calc.txt

3+2
  
4+5
  
8*2
  
10/4

# bc calc.txt

2

3)dc
  
用dc来进行计算的人可以不多，因为dc与bc相比要复杂，但是在进行简单的计划时，是差不多的，不算难。dc为压栈操作，默认也是交互的，但 也可以用echo和|来配合打算。
  
如: 

# dc

2+
  
p
  
4*
  
p
  
quit

# echo 3 2+ 4* p |dc

4)echo
  
echo用来进行回显，是周知的事。上面也配合bc来进行计算。其实echo也可以单独进行简单的计算，如: 

# echo $((3+5))

8

# echo $(((3+5)*2))

echo还可以进行变量的计算，如: 

# a=10

# b=5

# echo $(($a+$b))

15

# echo $a+$b

10+5

# echo $a+$b |bc

//计算前天的日期

# echo `date +%Y%m%d`

20090813

# echo `date +%Y%m%d`-2

20090813-2

# echo `date +%Y%m%d`-2 |bc

20090811
  
5)AWK
  
awk在处理文件的时，可以进行运算，那当然也可以单单用来计算了，如: 

# awk 'BEGIN{a=3+2;print a}'

5

# awk 'BEGIN{a=(3+2)*2;print a}'

Awk 支持常见的运算符， 如 +  (加) ，-  (减) ， \*  (乘) ， /  (除) ， ^ 或 \**  (乘方) ， %  (取模)  等等。 此外， awk 也提供了一些常用的数学函数, 比如 sin(x), cos(x), exp(x), log(x), sqrt(x), rand()。 使用这些运算符和函数可以直接进行一些简单的运算: 

# echo | awk '{print 8+6}'

14

# echo | awk '{print 8/6}'

1.33333

# echo | awk '{print 9%5}'

4

```bash
# expr只适用于整数之间的运算！
# expr命令计算加减乘除
# 在计算加减乘除时，不要忘了使用空格和转义。下面直接用实例来介绍一下expr的运算，如: 
expr 6 + 3        (有空格) 
9

expr 2 * 3       (有转义符号) 
6

expr 14 % 9
5

a=3
expr $a+5           (无空格) 
3+5

# expr $a + 5          (变量，有空格) 
8
# a=`expr 4 + 2`
echo $a
6
# expr $a + 3

# 计算字串长度
expr length "this is a test"
14

# 截取字串
expr substr "this is a test" 3 5
is is

# 返回第一个字符数字串出现的位置
expr index "sarasara"  a
 2

9另外，expr对于字串的操作 (计算) 也是很方便的，如: 
//字串长度
# expr length "yangzhigang.cublog.cn"
21
//从位置处抓取字串
# expr substr "yangzhigang.cublog.cn" 1 11
yangzhigang
//字串开始处
# expr index "yangzhigang.cublog.cn" cu
```

```bash
#10进制转16进制:
echo "obase=16;PID" | bc
echo "obase=16;ibase=10;100" | bc

#16进制转10进制,注意，16进制数字的F要大写，如果小写结果是不对的，不信试试:
echo "obase=10;ibase=16;11F8B" | bc
```

介绍如何在Linux下用bc命令进行快速的数字进制转换。

我想Windows里，数字进制转换最方便的就是自带的calc计算器，但是它原没有我们可爱的Linux方便。Linux下，我们在term里敲 几下键盘就可以做数字进制转换了。当然，你如果自己转换更快，那我比较佩服。这里，我们用到bc命令。bc命令是一个很好用的term计算器。我们要用到 bc的ibase和obase方法。

ibase是输入数字的进制，而obase就是输出数字的进制了。很好记，i是input，o是output。

如果用一条命令来转数字，可以用echo命令和管道结合bc。如下: 

10进制转2进制: 

$ echo "obase=2;ibase=10;100" | bc

$ echo "ibase=16;obase=2;f1" | bc


还可以用bc的交互模式来转换，最后Ctrl-D，或者输入quit退出。

~$ bcbc 1.06.94Copyright 1991-1994, 1997, 1998, 2000, 2004, 2006 Free Software Foundation, Inc.This is free software with ABSOLUTELY NO WARRANTY.For details type \`warranty'. ibase=16obase=2FF;F11111111111110001quit

Linux下的计算器

在windows下，大家都知道直接运行calc，(c:windowssystem32calc.exe),请可以打开计算器。
  
注: 
  
calculate vt.&vi. 计算；calculator n. 计算器。calc就是这个计算的简写。
  
Ca在化学中是代表钙元素，calcium 钙(20号元素,符号Ca)。两者有什么联系呢？
  
calculate 来自calculus,原义是做算术运算的小石子，是calx(石灰石) 的小称。
  
那么在linux系统下，有无与windows下calc.exe类似的计算器呢？
  
下面总结linux下的三个命令，来介绍一下linux下的计算方法: 

http://297020555.blog.51cto.com/1396304/591988