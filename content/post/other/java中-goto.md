---
title: Java中 goto
author: "-"
date: 2014-04-11T05:46:05+00:00
url: /?p=6513
categories:
  - Inbox
tags:
  - Java

---
## Java中 goto
http://lavasoft.blog.51cto.com/62575/178997/

Java语言中goto是保留关键字，没有goto语句，也没有任何使用goto关键字的地方。

Java中也可在特定情况下，通过特定的手段，来实现goto的功能。显然Java不愿意开发者随意跳转程序。下面解释两个特定: 

特定情况: 只有在循环体内，比如for、while语句 (含do...while语句) 中。

特定手段: 语句标签和循环控制关键字break、continue，语法格式是: break/continue 语句标签。

一、break、continue和语句标签

1. 语句标签

语句标签的语法是: 标签名:

语句标签可以定义在方法体内的最后一条语句之前即可。但是语句标签实际使用的机会是与break和continue结合使用的，而break和continue是和循环语句结合使用的，因此实际上语句标签的使用也是和循环紧密结合的。

语句标签在被使用的情况，只能定义在循环迭代语句之前，否则编译出错！

因此，有意义、可使用的标签含义是: 指定循环语句的标识！

2. break、continue语句单独使用

单独使用情况下: break语句作用是结束当前的循环迭代体，进而执行剩余的语句。

continue语句的作用是结束本次迭代过程，继续执行下一轮迭代。

3. break、continue语句结合语句标签的使用

为什么需要语句标签呢？

原因是因为程序可能有循环的嵌套，当多层循环嵌套时候，有时候需要一次跳出多级循环，这种情况下就需要结合语句标签才能实现此功能了。

带标签使用情况下: break中断并跳出标签所指定循环，continue跳转到标签指定的循环处，并继续执行该标签所指定的循环。

为了说明情况，看看下面的例子: 

import java.util.Random;

/**

* 语句标签测试

*

* @author leizhimin 2009-7-16 11:43:08

*/

public class TestLable {

public static void main(String[] args) {

outer:

for (int i = 0; i < 10; i++) {

System.out.println("\nouter_loop:" + i);

inner:

for (int k = 0; i < 10; k++) {

System.out.print(k + " ");

int x = new Random().nextInt(10);

if (x > 7) {

System.out.print(" >>x == " + x + "，结束inner循环，继续迭代执行outer循环了！");

continue outer;

}

if (x == 1) {

System.out.print(" >>x == 1，跳出并结束整个outer和inner循环！");

break outer;

}

}

}

System.out.println("-->>>所有循环执行完毕！");

}

}

执行结果: 

outer_loop:0

0 1 2 3 4 5 6 7 8 9 >>x == 8，结束inner循环，继续迭代执行outer循环了！

outer_loop:1

0 1 2 3 4 5 >>x == 9，结束inner循环，继续迭代执行outer循环了！

outer_loop:2

0 1 2 3 4 5 6 7 8 9 >>x == 8，结束inner循环，继续迭代执行outer循环了！

outer_loop:3

0 1 2 3 4 >>x == 9，结束inner循环，继续迭代执行outer循环了！

outer_loop:4

0 1 2 3 4 5 6 7 8 9 10 >>x == 8，结束inner循环，继续迭代执行outer循环了！

outer_loop:5

0 >>x == 1，跳出并结束整个outer和inner循环！-->>>所有循环执行完毕！

Process finished with exit code 0

这个执行结果是随机的。

下面给个图看看: 

二、switch语句

switch语句是一个条件选择语句，这个语句有"goto"的味道，但是限制也很多，因此，实际中使用较少。

switch语句的结构如下: 

switch(intvar){

case intval: 语句代码;break;

case intval: 语句代码;break;

case intval: 语句代码;break;

case intval: 语句代码;break;

default:

语句代码;

}

switch(intval){...}语句中，小括号中intvar是一个整数条件因子变量，这个变量只能为: byte、char、short、int和enum (枚举类型) 几种类型，本质上都是整形数字。intval是匹配的条件因子值，当匹配时，执行其下的语句。其中所有的break语句都是可选的。当执行了break语句后，就跳出整个switch语句，否则，还会继续往下匹配别的条件。当intvar不能匹配所有的给定条件值时候，就执行default语句，如果没有default语句，则跳出switch语句。

switch语句的条件因子变量只能作为整型数字或者字符型、枚举类型，这个限制太严格了，使得switch语句的实际用途不是很大。

下面是一个汉语金额数字转换程序: 

/**

* 汉语金额数字转换程序

*

* @author leizhimin 2009-7-16 13:28:05

*/

public class TestSwitch {

/**

* 数字转换为汉语金额数字

*

* @param num 数字

* @return 汉语金额数字

*/

public static String genCnNum(Long num) {

StringBuffer sb = new StringBuffer();

String snum = String.valueOf(num);

for (char c : snum.toCharArray()) {

sb.append(num2Cn(c));

}

return sb.toString();

}

/**

* 字符数字转换为汉语金额数字

*

* @param c 字符数字

* @return 汉语金额数字

*/

private static String num2Cn(char c) {

String res = null;

switch (c) {

case '0':

res = "零";

break;

case '1':

res = "壹";

break;

case '2':

res = "貮";

break;

case '3':

res = "叁";

break;

case '4':

res = "肆";

break;

case '5':

res = "伍";

break;

case '6':

res = "陆";

break;

case '7':

res = "柒";

break;

case '8':

res = "捌";

break;

case '9':

res = "玖";

break;

default:

System.out.println("您的输入有误，请重试！");

}

return res;

}

public static void main(String[] args) {

System.out.println(genCnNum(4523586022L));

}

}