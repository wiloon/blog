---
title: java switch
author: "-"
date: 2012-06-13T10:44:36+00:00
url: /?p=3525
categories:
  - Java
tags:
  - reprint
---
## java switch
关于java中switch使用的一些说明

switch(表达式)
{
case 常量表达式1:语句1;
....
case 常量表达式2:语句2;
default:语句;
}
default就是如果没有符合的case就执行它,default并不是必须的.
case后的语句可以不用大括号.
switch语句的判断条件可以接受int,byte,char,short,不能接受其他类型.
一旦case匹配,就会顺序执行后面的程序代码,而不管后面的case是否匹配,直到遇见break,利用这一特性可以让好几个case执行统一语句.

例如:

switch(x)

{

case 1:

case 2:

case3: System.out.println("haha");

break;

case4: System.out.println("hehe");

}