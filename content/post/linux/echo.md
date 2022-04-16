---
title: echo, printf
author: "-"
date: 2012-06-21T01:21:27+00:00
url: echo
categories:
  - shell
tags:
  - reprint
---
## echo, printf
echo aaa > test.txt

echo bbb >> test.txt

### 参数 
    -n 不输出结尾的换行
    -e：打开反斜杠字符 backslash-escaped 的解析，即对 /n，/t 等字符进行解析，而不视之为两个字符
    -E：关闭反斜杠字符的解析，/n 作为两个字符，这是系统缺省模式

#### 反斜杠字符

    /a ： 发出警告铃音（ALERT or CTRL-G (bell)） 
    /b ： 退格（BACKSPACE or CTRL-H ） 
    /c ： 删除最后的字符及最后的换行（Omit final NEWLINE ） 
    /e ： 删除后面的一个字符（Escape character (same as /E) ） 
    /E ： 同上（Escape character） 
    /f ： 换页符，在某些现实中会清屏，有些会换行（FORMFEED or CTRL-L ） 
    /n ： 换行（NEWLINE (not at end of command) or CTRL-J ） 
    /r ： 从行头开始，和换行不一样，仍在本行（RETURN (ENTER) or CTRL-M ） 
    /t ： tab键（TAB or CTRL-I ） 
    /v ： 竖直tab，和/f一样，显示不同机器有所不一样，通常会引起换行VERTICAL TAB or CTRL-K 
    /n ： 在cygwin中使用/65，无法正确显示'A’但是下面两种方法否可以显示。ASCII character with octal (base-8) value n, where n is 1 to 3 digits 
    /0nnn ： 用8进制的值表示一个字符，例如/0101，即65，表示字符’A’(The eight-bit character whose value is the octal (base-8) value nnn where nnn is 1 to 3 digits ) 
    /xHH ： 用16进制的值表示一个字符，例如/x41，即65，表示字符’A’The eight-bit character whose value is the hexadecimal (base-16) value HH (one or two digits) 



linux的echo命令, 在shell编程中极为常用, 在终端下打印变量value的时候也是常常用到的, 因此有必要了解下echo的用法

echo命令的功能是在显示器上显示一段文字，一般起到一个提示的作用。
  
该命令的一般格式为:  echo [ -n ] 字符串
  
其中选项n表示输出文字后不换行；字符串能加引号，也能不加引号。用echo命令输出加引号的字符串时，将字符串原样输出；用echo命令输出不加引号的字符串时，将字符串中的各个单词作为字符串输出，各字符串之间用一个空格分割。

功能说明: 显示文字。
  
语  法: echo [-ne][字符串]或 echo [-help][-version]
  
补充说明: echo会将输入的字符串送往标准输出。输出的字符串间以空白字符隔开, 并在最后加上换行号。
 
  
–help 显示帮助
  
–version 显示版本信息
 
Linux的echo命令, 在shell编程中极为常用, 在终端下打印变量value的时候也是常常用到。

比如: echo可用作显示注释，用于一些批命令中需要注释给用户看的地方，比如前一条命令执行会花很长时间，常会用echo显示一条信息让用户知道这个时候比较慢，稍微等待一会。

在Linux中echo命令用来在标准输出上显示一段字符，比如: 
  
echo "the echo command test!"

这个就会输出"the echo command test!"这一行文字！

echo "the echo command test!">a.sh
  
这个就会在a.sh文件中输出"the echo command test!"这一行文字！ 该命令的一般格式为:  echo [ -n ] 字符串其中选项n表示输出文字后不换行；字符串能加引号，也能不加引号。用echo命令输出加引号的字符串时，将字符串原样输出；用echo命令输出不加引号的字符串时，将字符串中的各个单词作为字符串输出，各字符串之间用一个空格分割。

## shell printf

printf和C语言的使用方式类似。和echo不一样，它不会在最后自动加上换行，需要写入命令中。例如printf "Hello, world/n"。printf的命令格式如下： 

printf format-string [arguments]

    %c：ASCII字符，如果参数给出字符串，则打印第一个字符 
    %d：10进制整数 
    %i：同%d 
    %e：浮点格式（[-]d.精度[+-]dd） 
    %E：浮点格式（[-]d.精度E[+-]dd） 
    %f：浮点格式（[-]ddd.precision） 
    %g：%e或者%f的转换，如果后尾为0，则删除它们 
    %G：%E或者%f的转换，如果后尾为0，则删除它们 
    %o：8进制 
    %s：字符串 
    %u：非零正整数 
    %x：十六进制 
    %X：非零正数，16进制，使用A-F表示10-15 
    %%：表示字符"%"

>https://blog.csdn.net/shixin_0125/article/details/78723322

