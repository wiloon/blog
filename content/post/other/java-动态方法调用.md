---
title: Java 动态方法调用
author: "-"
date: 2012-09-19T08:29:05+00:00
url: /?p=4093
categories:
  - Java
tags:
  - reprint
---
## Java 动态方法调用


  原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://wujuxiang.blog.51cto.com/2250829/406802


  在Java中，如果方法重写只是一种名字空间的编写，那么它最多是让人感到有趣，但没有实际价值，但情况并非如此。方法重写构造成了Java最大的一个概念基础: 动态方法调度 (dynamic method dispatch) 。动态方法调度是一种机制，借助于这种机制，对一个已经重写的方法的调用将在运行时，而不是在编译时解析。动态方法调度非常重要，因为这关系到Java如何实现运行多态性的问题。我们知道，超类引用变量可以引用子类对象，Java使用这个事实来解决在运行时对重写方法的调用。下面是运行原理: 当一个超类引用调用一个重写方法时，Java根据在调用时被引用对象的类型执行哪个版本的方法。换句话说，是被引用对象的类型 (不是引用变量的类型) 决定将执行哪个版本的重写方法。因此，如果说超类包含一个被子类重写的方法，那么当通过超类引用变量来引用不同类型的对象时，就会执行那个方法的不同版本。演示如下:  
  
    public class ClassA {
 void callme(){
 System.out.println("Inside A's callme method");
 }
 }
  
  
    public class ClassB extends ClassA{
  
  
    void callme(){
 System.out.println("Inside B's callme method");
 }
 }
  
  
    public class ClassC extends ClassA{
  
  
    void callme(){
 System.out.println("Inside C's callme method");
 }
 }
  
  
    public class Dispatch {
  
  
    public static void main(String[] args) {
 ClassA classA = new ClassA();
 ClassB classB = new ClassB();
 ClassC classC = new ClassC();
  
  
    ClassA a = classA;
 a.callme();
 ClassB b = classB;
 b.callme();
 ClassC c = classC;
 c.callme();
 }
  
  
    }
  
  
    程序运行结果: 
  
  
    Inside A's callme method
 Inside B's callme method
 Inside C's callme method
  
  
    重写方法允许Java支持运行时多态性。多态是面向对象编程的本质，它允许通用类指定方法，这些方法对该类的所有派生类都是公用的，同时该方法还允许子类定义这些方法中的某些或全部的特定实现。重写方法是Java实现其多态性"一个接口，多个方法"的另一种方式。
 成功应用多态性的关键是要理解超类和子类形成了从简单到复杂的层次。为了正确应用多态性，超类提供了子类可以直接使用的所有元素。多态性也定义了派生类必须实现自己的方法，这允许子类在加强一致接口的同时，灵活地定义它们自己的方法。因此，通过同时使用继承和重写方法，超类能够定义供其所有子类使用的方法的通用形式。
 运行时多态性是面向对象设计方法实现代码重用和健壮性的最强大机制之一，代码库在维持抽象接口同时不重新编译的情况下即调用新类的实例。
 本文出自 "有思想的代码" 博客，请务必保留此出处http://wujuxiang.blog.51cto.com/2250829/406802
  
