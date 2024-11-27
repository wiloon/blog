---
title: 'java boolean的|=或&=或^=写法'
author: "-"
date: 2016-03-25T03:59:49+00:00
url: /?p=8828
categories:
  - Inbox
tags:
  - reprint
---
## 'java boolean的|=或&=或^=写法'
package jack.test;

/**
  
* 有时候看一看开源框架可以学到很多有用的东西,在看Simple Log的时候发现了一种写法
  
* 在对boolean操作时可以使用|=或者&=或者^=进行运算。
  
* 逻辑操作符
  
* 逻辑操作符的操作对象和结果均为boolean型,共六个: 
  
* ！ (逻辑非)  &&  (逻辑与)  || (逻辑或) 
  
* ^ (逻辑并或)  &  (逻辑与)  |  (逻辑或) 
  
* 按位与'&'也可作为逻辑与使用,但未作优化,而'&&'操作符是经过优化的。对'|'操作符也类似。
  
* @author Administrator
  
*
  
*/
  
public class Test {

public static void main(String[] args) {
  
boolean isTrue = false;
  
isTrue |= true;
  
System.out.println(isTrue);

isTrue = false;
  
isTrue |= false;
  
System.out.println(isTrue);

isTrue = true;
  
isTrue |= true;
  
System.out.println(isTrue);

isTrue = true;
  
isTrue |= false;
  
System.out.println(isTrue);
  
isTrue &= false;
  
System.out.println(isTrue);
  
isTrue = true;
  
isTrue ^= isTrue;
  
System.out.println(isTrue);
  
}
  
}

true &= true ==> true
  
true &= false ==> false
  
false &= true ==> false
  
false &= false ==> false
  
true |= true ==> true
  
true |= false ==> true
  
false |= true ==> true
  
false |= false ==> false
  
^= 相同为真,不同为假
  
true ^= true ==> false
  
true ^= false ==> true
  
false ^= true ==> true
  
false ^= false ==> false