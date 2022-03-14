---
title: java 静态变量/方法
author: "-"
date: 2012-06-28T14:15:30+00:00
url: /?p=3689
categories:
  - Java

tags:
  - reprint
---
## java 静态变量/方法
有时你希望定义一个类成员，使它的使用完全独立于该类的任何对象。通常情况下，类成员必须通过它的类的对象访问，但是可以创建这样一个成员，它能够被它自己使用，而不必引用特定的实例。在成员的声明前面加上关键字static(静态的)就能创建这样的成员。如果一个成员被声明为static，它就能够在它的类的任何对象创建之前被访问，而不必引用任何对象。你可以将方法和变量都声明为static。static 成员的最常见的例子是main( ) 。因为在程序开始执行时必须调用main() ，所以它被声明为static。

声明为static的变量实质上就是全局变量。当声明一个对象时，并不产生static变量的拷贝，而是该类所有的实例变量共用同一个static变量。声明为static的方法有以下几条限制: 

·

它们仅能调用其他的static 方法。

·

它们只能访问static数据。

·

它们不能以任何方式引用this 或super (关键字super 与继承有关，在下一章中描述) 。

如果你需要通过计算来初始化你的static变量，你可以声明一个static块，Static 块仅在该类被加载时执行一次。下面的例子显示的类有一个static方法，一些static变量，以及一个static 初始化块: 

// Demonstrate static variables，methods，and blocks.

class UseStatic {

static int a = 3;

static int b;

static void meth(int x) {

System.out.println("x = " + x);

System.out.println("a = " + a);

System.out.println("b = " + b);

}

static {

System.out.println("Static block initialized.");

b = a * 4;

}

public static void main(String args[]) {

meth(42);

}

}

一旦UseStatic 类被装载，所有的static语句被运行。首先，a被设置为3，接着static 块执行(打印一条消息)，最后，b被初始化为a*4 或12。然后调用main()，main() 调用meth() ，把值42传递给x。3个println ( ) 语句引用两个static变量a和b，以及局部变量x 。

注意: 在一个static 方法中引用任何实例变量都是非法的。

下面是该程序的输出: 

Static block initialized.

x = 42

a = 3

b = 12

在定义它们的类的外面，static 方法和变量能独立于任何对象而被使用。这样，你只要在类的名字后面加点号运算符即可。例如，如果你希望从类外面调用一个static方法，你可以使用下面通用的格式: 

classname.method( )

这里，classname 是类的名字，在该类中定义static方法。可以看到，这种格式与通过对象引用变量调用非static方法的格式类似。一个static变量可以以同样的格式来访问——类名加点号运算符。这就是Java 如何实现全局功能和全局变量的一个控制版本。

下面是一个例子。在main() 中，static方法callme() 和static 变量b在它们的类之外被访问。

class StaticDemo {

static int a = 42;

static int b = 99;

static void callme() {

System.out.println("a = " + a);

}

}

class StaticByName {

public static void main(String args[]) {

StaticDemo.callme();

System.out.println("b = " + StaticDemo.b);

}

}

下面是该程序的输出: 

a = 42

b = 99

### java 静态块、非静态块、静态函数、构造函数 执行顺序
  java中经常有一些静态块，这是用来在生成类之前进行的初始化，无论java还C++语言中的static，都是最先初始化好的。结构如下: 
 static {
 静态语句代码块
 } 
  
    {
 非静态语句代码块
 }
 异同点
 相同点: 都是在JVM加载类时且在构造方法执行之前执行，在类中都可以定义多个，一般在代码块中对一些static变量进行赋     值。
 不同点: 静态代码块在非静态代码块之前执行 (静态代码块-》非静态代码块-》构造方法) 。
 静态代码块只在第一次new执行一次，之后不在执行，而非静态代码块在每new一次就执行一次。非静态代码块可以     在普通方法中定义 (个人感觉作用不大) ;而静态代码块不行。
  
  
    Java代码
 package com.sample.client;
 public class Test {
 public int a;
  
  
    static {
 System.out.println("Test Static 静态语句块");
 }
 public Test() {
 System.out.println("Test 默认无参构造器");
 }
 {
 System.out.println("Test 非静态");
 }
 }
  
  
    Java代码
 package com.sample.client;
  
  
    public class Test1 extends Test {
 public int i;
 public double d;
  
  
    static {
 System.out.println("Test1 Static 静态语句块");
 }
  
  
    public Test1 () {
 System.out.println("Test1 默认无参构造器");
 }
  
  
    {
 System.out.println("Test1 非静态");
 }
  
  
    public static void main(String[] args) {
 Test1 t = new Test1();
  
  
    }
 }
  
  
    Java代码
 输出结果如下: 
  
  
    Test Static 静态语句块
 Test1 Static 静态语句块
 Test 非静态
 Test 默认无参构造器
 Test1 非静态
 Test1 默认无参构造器
  
  
    小结: 
 1、静态代码块是在类加载时自动执行的，非静态代码块在创建对象自动执行的代码，不创建对象不执行该类的非静态代码块。 顺序:  静态代码块-》非静态代码块-》类构造方法。
 2、在静态方法里面只能直接调用同类中其他的静态成员 (包括变量和方法) ，而不能直接访问类中的非静态成员。因为对于非静态的方法和变量，需要先创建类的实例对象后方可使用，而静态方法在使用前不用创建任何对象。
 3、如果某些代码必须要在项目启动时候就执行的时候，我们可以采用静态代码块，这种代码是主动执行的；需要在项目启动的时候就初始化，在不创建对象的情况下，其他程序来调用的时候，需要使用静态方法，此时代码是被动执行的。
 区别: 静态代码块是自动执行的；
 静态方法是被调用的时候才执行的；
 作用: 静态代码块可以用来初始化一些项目最常用的变量和对象；静态方法可以用作不创建对象也可以能需要执行的代码。
  





  http://liqita.iteye.com/blog/1472717

 [1]: http://liqita.iteye.com/blog/1472717