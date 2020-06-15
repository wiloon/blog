---
title: 'Java  exception throw throws'
author: wiloon
type: post
date: 2015-05-14T00:28:57+00:00
url: /?p=7663
categories:
  - Uncategorized
tags:
  - Java

---
1. 区别



throws是用来声明一个方法可能抛出的所有异常信息，而throw则是指抛出的一个具体的异常类型。此外throws是将异常声明但是不处理，而是将异常往上传，谁调用我就交给谁处理。

2.分别介绍

throws：用于声明异常，例如，如果一个方法里面不想有任何的异常处理，则在没有任何代码进行异常处理的时候，必须对这个方法进行声明有可能产生的所有异常（其实就是，不想自己处理，那就交给别人吧，告诉别人我会出现什么异常，报自己的错，让别人处理去吧）。

格式是：方法名（参数）throws 异常类1，异常类2，&#8230;..





Java代码
  
class Math{
  
public int div(int i,int j) throws Exception{
  
int t=i/j;
  
return t;
  
}
  
}

public class ThrowsDemo {
  
public static void main(String args[]) throws Exception{
  
Math m=new Math();
  
System.out.println("出发操作："+m.div(10,2));
  
}
  
}
  
throw：就是自己进行异常处理，处理的时候有两种方式，要么自己捕获异常（也就是try catch进行捕捉），要么声明抛出一个异常（就是throws 异常~~）。注意：throw一旦进入被执行，程序立即会转入异常处理阶段，后面的语句就不再执行，而且所在的方法不再返回有意义的值！



Java代码
  
public class TestThrow
  
{
  
public static void main(String[] args)
  
{
  
try
  
{
  
//调用带throws声明的方法，必须显式捕获该异常
  
//否则，必须在main方法中再次声明抛出
  
throwChecked(-3);
  
}
  
catch (Exception e)
  
{
  
System.out.println(e.getMessage());
  
}
  
//调用抛出Runtime异常的方法既可以显式捕获该异常，
  
//也可不理会该异常
  
throwRuntime(3);
  
}
  
public static void throwChecked(int a)throws Exception
  
{
  
if (a > 0)
  
{
  
//自行抛出Exception异常
  
//该代码必须处于try块里，或处于带throws声明的方法中
  
throw new Exception("a的值大于0，不符合要求");
  
}
  
}
  
public static void throwRuntime(int a)
  
{
  
if (a > 0)
  
{
  
//自行抛出RuntimeException异常，既可以显式捕获该异常
  
//也可完全不理会该异常，把该异常交给该方法调用者处理
  
throw new RuntimeException("a的值大于0，不符合要求");
  
}
  
}
  
}
  
http://lcy0202.iteye.com/blog/1555907

http://lavasoft.blog.51cto.com/62575/18920/