---
title: Java 运算符
author: "-"
date: 2012-05-03T07:28:36+00:00
url: /?p=3083
categories:
  - Java
tags:
  - reprint
---
## Java 运算符
三目运算符(又称条件运算符)

三元运算符一般用的很少，因为它在程序段中的可读性很差，所以笔者建议不要经常使用三元运算符，但很少使用并不代表不使用，所以还是要掌握好它的用法，三元运算符的表达形式如下: 
  
布尔表达式?值 0 : 值 1
  
它的运算过程是: 如果布尔表达式的结果是 true，就返回值 0，如果布尔表达式的结果是 false，就返回值 1，例如下面的程序段。

public class data21{
  
public static void main(String[] args){
  
int a=10;
  
int b=20;
  
System.out.println("此三元运算式结果是: "+((a>b)?'A':'B'));
  
}
  
}
  
分析上面程序段: 因为"a"是小于"b"，所以"a>b"这个关系运算符的结果是"false"，既然是"false"，那么选择值 1，即这个三元运算符的结果是"B"。
  
总结: 
  
条件运算符也被称为三元运算符。该运算符有3个操作数，并且需要判断布尔表达式的值。该运算符的主要是决定哪个值应该赋值给变量。
  
variable x = (expression) ? value if true : value if false
  
实例

public class Test {
  
public static void main(String args[]){
  
int a , b;
  
a = 10;
  
b = (a == 1) ? 20: 30;
  
System.out.println( "Value of b is : " + b );
  
b = (a == 10) ? 20: 30;
  
System.out.println( "Value of b is : " + b );
  
}
  
}
  
以上实例编译运行结果如下: 
  
Value of b is : 30
  
Value of b is : 20

这种运算符比较罕见，因为它有三个运算对象。但它确实属于运算符的一种，因为它最终也会生成一个值。这与本章后一节要讲述的普通if-else语句是不同的。表达式采取下述形式: 

布尔表达式 ? 值0:值1

若"布尔表达式"的结果为true，就计算"值0"，而且它的结果成为最终由运算符产生的值。但若"布尔表达式"的结果为false，计算的就是"值1"，而且它的结果成为最终由运算符产生的值。

当然，也可以换用普通的if-else语句 (在后面介绍) ，但三元运算符更加简洁。尽管C引以为傲的就是它是一种简练的语言，而且三元运算符的引入多半就是为了体现这种高效率的编程，但假若您打算频繁用它，还是要先多作一些思量――它很容易就会产生可读性极差的代码。

可将条件运算符用于自己的"副作用"，或用于它生成的值。但通常都应将其用于值，因为那样做可将运算符与if-else明确区别开。下面便是一个例子: 

static int ternary(int i) {

return i < 10 ? i \* 100 : i \* 10;

}

可以看出，假设用普通的if-else结构写上述代码，代码量会比上面多出许多。如下所示: 

static int alternative(int i) {

if (i < 10)

return i * 100;

return i * 10;

}

逗号运算符

在 Java 程序设计中，逗号运算符一般是用来将几个条件彼此分开，例如数组中的每个元素都是使用逗号与其他元素分开的。
  
public class var{
  
public static void main(String[] args){
  
int a=1,b=2,c=3;
  
System.out.println(a+b+c);
  
}
  
}

http://www.52ij.com/jishu/java/98790.html