---
title: linux typeset
author: "-"
date: 2019-10-28T09:32:49+00:00
url: /?p=15069
categories:
  - Inbox
tags:
  - reprint
---
## linux typeset

[https://blog.csdn.net/blackmanren/article/details/9281201](https://blog.csdn.net/blackmanren/article/details/9281201)

typeset 用于设置变量属性, 如大小写,宽度,左右对齐等都可以用typeset来控制, 当用typeset改变一个变量的属性时,这种改变是永久的,下面以ksh为例,演示typeset的几种典型用法

typeset的-u选项可以将一个变量的字符变成大写
  
/home/lee#typeset -u var=abc
  
/home/lee#echo $var
  
ABC

3:typeset的-l选项将一个变量的字符变成小写
  
/home/lee#typeset -l var=ABC
  
/home/lee#echo $var
  
abc

typeset的-L选项把变量变成一个左对齐的4个字符串,有些像字符串截取
  
/home/lee#typeset -L4 var=abcdefg
  
/home/lee#echo $var
  
abcd

typeset的-R选项把变量变成一个右对齐的4个字符串
  
/home/lee#typeset -R4 var=abcdefg
  
/home/lee#echo $var
  
defg

typeset的-Z选项把串变成一个空填充,占15个字符位的串,冒号用来保护空白符
  
typeset -Z15 var="abc ddd"
  
/home/lee#echo "$var"
  
^^^^^^^^abc ddd #^为空白
  
/home/lee#typeset -LZ15 var="abc 123"
  
/home/lee#echo "$var$var"
  
abc 123 abc 123

7:变量n是一个被设置成一个整数的变量,typeset命令将整数n前面补齐0,共15个字符位
  
/home/lee#typeset -i n=24
  
/home/lee#typeset -Z15 n
  
/home/lee#echo $n
  
000000000000024

8:变量answer被给定一个值-Yes并变成一个小写,左对齐,一个字符的串
  
/home/lee#typeset -lL1 answer=Yes
  
/home/lee#echo $answer
  
y

typeset其他用法:
  
typeset -i num #强制num为一个整数,如:
  
/home/lee#typeset -i num=10
  
/home/lee#echo $num
  
/home/lee#typeset -i16 num=10
  
/home/lee#echo $num
  
16#a
  
/home/lee#typeset -i2 num=10
  
/home/lee#echo $num
  
2#1010
  
/home/lee#typeset -i8 num=10
  
/home/lee#echo $num
  
8#12

typeset -x #显示被导出的变量
  
typeset a b c #如果在一个函数里定义,则把a b c创建为局部变量
  
typeset -r x=var#设置一个只读变量
