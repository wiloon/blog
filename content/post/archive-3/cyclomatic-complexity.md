---
title: 圈复杂度(Cyclomatic Complexity)
author: "-"
date: 2019-09-09T08:26:19+00:00
url: /?p=14915
categories:
  - Inbox
tags:
  - reprint
---
## 圈复杂度(Cyclomatic Complexity)

圈复杂度(Cyclomatic Complexity)是一种代码复杂度的衡量标准。它可以用来衡量一个模块判定结构的复杂程度，数量上表现为独立线性路径条数，也可理解为覆盖所有的可能情况最少使用的测试用例数。圈复杂度大说明程序代码的判断逻辑复杂，可能质量低且难于测试和维护。程序的可能错误和高的圈复杂度有着很大关系。

下面这个实例中，单元测试的覆盖率可以达到100%，但是很容易发现这其中已经漏掉了一个NPE的测试用例。case1方法的圈复杂度为2，因此至少需要2个用例才能完全覆盖到其所有的可能情况。

//程序原代码，圈复杂度为 2
  
public String case1(int num) {

String string = null;

if (num == 1) {

string = "String";

}

return string.substring(0);
  
}

//上面代码的单元测试代码
  
public void testCase1(){

String test1 = case1(1);
  
}

圈复杂度主要与分支语句 (if、else、，switch 等) 的个数成正相关。当一段代码中含有较多的分支语句，其逻辑复杂程度就会增加。

圈复杂度的计算方法，可以参考这篇文章: [http://blog.csdn.net/lg707415323/article/details/7790660](http://blog.csdn.net/lg707415323/article/details/7790660)

可以直接降低圈复杂度的9种重构技术 (针对结构化编程)

1.Composing Methods(重新组织你的函数)
  
<1>Extract Method(提炼函数)
  
<2>Substitute Algorithm(替换你的算法)

2.Simplifying Conditional Expressions(简化条件表达式)
  
<1>Decompose Conditional(分解表达式)
  
<2>Consolidate Conditional Expression(合并表达式)
  
<3>Consolidate Duplicate Conditional Fragments (合并重复的条件)
  
<4>Remove Control Flag(移除控制标记)

3.Making Method Calls Simpler(简化函数调用)
  
<1>Separate Query from Modifier(将查询函数和修改函数分离)
  
<2>PARAMETERIZE Method(令函数携带参数)
  
<3>Replace Parameter with Explicit Methods(以明确函数取代参数)

针对面向对象编程:
  
Replace Conditional with Polymorphism (以多态取代条件式)

[https://blog.csdn.net/rangqiwei/article/details/38400277](https://blog.csdn.net/rangqiwei/article/details/38400277)
