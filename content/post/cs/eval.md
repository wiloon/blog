---
title: eval command
author: "-"
date: 2018-05-11T01:05:54+00:00
url: eval
categories:
  - Linux
tags:
  - reprint
---
## eval command

语法: eval cmdLine
  
eval 会对后面的 cmdLine 进行两遍扫描, 如果第一遍扫描后, cmdLine 是个普通命令, 则执行此命令；如果 cmdLine 中含有变量的间接引用, 则保证间接引用的语义。

举例如下:
  
set 11 22 33 44
  
如果要输出最近一个参数,即 44, 可以使用如下命令
  
    echo $4
  
但是如果我们不知道有几个参数的时候, 要输出最后一个参数, 大家可能会想到使用 `$#` 来输出最后一个参数
  
如果使用命令:
  
    echo "\$$#"

则得到的结果是 $4,而不是我们想要的44。这里涉及到一个变量间接引用的问题, 我们的本意是输出 $4, 默认情况下, 命令后忽略变量间接引用的情况。
  
这时候,就可以使用eval命令。
  
    eval echo "\$$#"
  
得到的结果为44

1. eval命令将会首先扫描命令行进行所有的替换, 然后再执行命令。该命令使用于那些一次扫描无法实现其功能的变量。该命令对变量进行两次扫描。这些需要进行两次扫描的变量有时候被称为复杂变量。
2. eval也可以用于回显简单变量, 不一定时复杂变量。

NAME=ZONE

eval echo $NAME 等价于 echo $NAME

3. 两次扫描

test.txt内容: hello shell world!

myfile="cat test.txt"

(1)echo $myfile#result:cat test.txt

(2)eval echo $myfile#result:hello shell world!

从 (2) 可以知道第一次扫描进行了变量替换,第二次扫描执行了该字符串中所包含的命令

4.获得最后一个参数

echo "Last argument is $(eval echo \$$#)"

echo "Last argument is $(eval echo $#)"

---

转自: [http://www.2cto.com/os/201311/255577.html](http://www.2cto.com/os/201311/255577.html)
转自: [http://www.cnblogs.com/xdzone/archive/2011/03/15/1984971.html](http://www.cnblogs.com/xdzone/archive/2011/03/15/1984971.html)
[https://blog.csdn.net/vizts/article/details/47043695](https://blog.csdn.net/vizts/article/details/47043695)
