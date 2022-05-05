---
title: 设计模式 – 策略/Strategy
author: "-"
date: 2017-01-30T08:43:37+00:00
url: Strategy
categories:
  - pattern
tags:
  - reprint
---
## 设计模式 – 策略/Strategy

设计模式之Strategy(策略)
  
板桥里人 <http://www.jdon.com> 2002/03/30
  
Strategy策略模式是属于设计模式中 对象行为型模式,主要是定义一系列的算法,把这些算法一个个封装成单独的类.

Stratrgy应用比较广泛,比如, 公司经营业务变化图, 可能有两种实现方式,一个是线条曲线,一个是框图(bar),这是两种算法,可以使用Strategy实现.

这里以字符串替代为例, 有一个文件,我们需要读取后,希望替代其中相应的变量,然后输出.关于替代其中变量的方法可能有多种方法,这取决于用户的要求,所以我们要准备几套变量字符替代方案.

首先,我们建立一个抽象类RepTempRule 定义一些公用变量和方法:

public abstract class RepTempRule{

protected String oldString="";
  
public void setOldString(String oldString){
  
this.oldString=oldString;
  
}

protected String newString="";
  
public String getNewString(){
  
return newString;
  
}

public abstract void replace() throws Exception;
  
}
  
在RepTempRule中 有一个抽象方法abstract需要继承明确,这个replace里其实是替代的具体方法.
  
我们现在有两个字符替代方案,
  
1.将文本中aaa替代成bbb;
  
2.将文本中aaa替代成ccc;

对应的类分别是RepTempRuleOne RepTempRuleTwo

public class RepTempRuleOne extends RepTempRule{
  
public void replace() throws Exception{

//replaceFirst是jdk1.4新特性
  
newString=oldString.replaceFirst("aaa", "bbbb")
  
System.out.println("this is replace one");

}
  
}
  
public class RepTempRuleTwo extends RepTempRule{
  
public void replace() throws Exception{

newString=oldString.replaceFirst("aaa", "ccc")
  
System.out.println("this is replace Two");

}
  
}
  
第二步: 我们要建立一个算法解决类,用来提供客户端可以自由选择算法。

public class RepTempRuleSolve {private RepTempRule strategy;

public RepTempRuleSolve(RepTempRule rule){
  
this.strategy=rule;
  
}

public String getNewContext(Site site,String oldString) {
  
return strategy.replace(site,oldString);
  
}

public void changeAlgorithm(RepTempRule newAlgorithm) {
  
strategy = newAlgorithm;
  
}

}
  
调用如下:

public class test{

......

public void testReplace(){

//使用第一套替代方案
  
RepTempRuleSolve solver=new RepTempRuleSolve(new RepTempRuleOne());
  
solver.getNewContext(site,context);

//使用第二套

solver=new RepTempRuleSolve(new RepTempRuleTwo());
  
solver.getNewContext(site,context);

}

.....

}
  
我们达到了在运行期间,可以自由切换算法的目的。

实际整个Strategy的核心部分就是抽象类的使用,使用Strategy模式可以在用户需要变化时,修改量很少,而且快速.

Strategy和Factory有一定的类似,Strategy相对简单容易理解,并且可以在运行时刻自由切换。Factory重点是用来创建对象。

Strategy适合下列场合:

1.以不同的格式保存文件;

2.以不同的算法压缩文件;

3.以不同的算法截获图象;

4.以不同的格式输出同样数据的图形,比如曲线 或框图bar等
