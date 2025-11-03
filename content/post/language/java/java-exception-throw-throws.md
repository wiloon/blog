---
title: 'Java  exception throw throws'
author: "-"
date: 2015-05-14T00:28:57+00:00
url: /?p=7663
categories:
  - Inbox
tags:
  - Java

---
## 'Java  exception throw throws'
 
CheckException和RuntimeException
java文档中对RuntimeException的定义是: 

RuntimeException 是那些可能在 Java 虚拟机正常运行期间抛出的异常的超类。

可能在执行方法期间抛出但未被捕获的 RuntimeException 的任何子类都无需在 throws 子句中进行声明。

 

java中Exception分为两类,一类是CheckException一类是UncheckException。并且java的Error都属于UncheckedException。

一、CheckException和UnCheckException的区别: 

1. 在编译的时候,java编译器会强制你处理CheckException,处理的方式有两种: 一种是抛出异常；另一种是捕获异常 (常见的有ClassNotFoundException等) 。而对于UncheckException编译去则不需要你做任何处理,只是在运行时出现了该类异常,则会被抛出 (常见的有: NullPointException,ArrayIndexOutofBoundException等) 。

2. Checked exception用来指示一种调用方能够直接处理的异常情况。而Runtime exception则用来指示一种调用方本身无法处理或恢复的程序错误。


1. 区别
throws是用来声明一个方法可能抛出的所有异常信息,而throw则是指抛出的一个具体的异常类型。此外throws是将异常声明但是不处理,而是将异常往上传,谁调用我就交给谁处理。

2.分别介绍

throws: 用于声明异常,例如,如果一个方法里面不想有任何的异常处理,则在没有任何代码进行异常处理的时候,必须对这个方法进行声明有可能产生的所有异常 (其实就是,不想自己处理,那就交给别人吧,告诉别人我会出现什么异常,报自己的错,让别人处理去吧) 。

格式是: 方法名 (参数) throws 异常类1,异常类2,.....

Java代码
  
class Math{
  
public int div(int i,int j) throws Exception{
  
int t=i/j;
  
return t;
  
}
  
}

public class ThrowsDemo {
  
public static void main(String args[]) throws Exception{
  
Math m=new Math();
  
System.out.println("出发操作: "+m.div(10,2));
  
}
  
}
  
throw: 就是自己进行异常处理,处理的时候有两种方式,要么自己捕获异常 (也就是try catch进行捕捉) ,要么声明抛出一个异常 (就是throws 异常~~) 。注意: throw一旦进入被执行,程序立即会转入异常处理阶段,后面的语句就不再执行,而且所在的方法不再返回有意义的值！


Java代码
  
public class TestThrow
  
{
  
public static void main(String[] args)
  
{
  
try
  
{
  
//调用带throws声明的方法,必须显式捕获该异常
  
//否则,必须在main方法中再次声明抛出
  
throwChecked(-3);
  
}
  
catch (Exception e)
  
{
  
System.out.println(e.getMessage());
  
}
  
//调用抛出Runtime异常的方法既可以显式捕获该异常,
  
//也可不理会该异常
  
throwRuntime(3);
  
}
  
public static void throwChecked(int a)throws Exception
  
{
  
if (a > 0)
  
{
  
//自行抛出Exception异常
  
//该代码必须处于try块里,或处于带throws声明的方法中
  
throw new Exception("a的值大于0,不符合要求");
  
}
  
}
  
public static void throwRuntime(int a)
  
{
  
if (a > 0)
  
{
  
//自行抛出RuntimeException异常,既可以显式捕获该异常
  
//也可完全不理会该异常,把该异常交给该方法调用者处理
  
throw new RuntimeException("a的值大于0,不符合要求");
  
}
  
}
  
}
  
http://lcy0202.iteye.com/blog/1555907

http://lavasoft.blog.51cto.com/62575/18920/


https://www.cnblogs.com/fsh1542115262/p/3933712.html

