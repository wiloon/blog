---
title: Java assertion
author: "-"
date: 2012-09-21T08:16:05+00:00
url: /?p=4159
categories:
  - Java
tags:
  - reprint
---
## Java assertion
as[http://www.ibm.com/developerworks/cn/java/l-javaassertion/index.html](http://www.ibm.com/developerworks/cn/java/l-javaassertion/index.html)

sertion的语法和语义

J2SE 1.4在语言上提供了一个新特性，就是assertion(断言)功能，它是该版本在Java语言方面最大的革新。在软件开发中，assertion是一种经典的调试、测试方式，本文将深入解析assertion功能的使用以及其设计理念，并给出相关的例子 。

assertion(断言)在软件开发中是一种常用的调试方式，很多开发语言中都支持这种机制，如C，C++和Eiffel等，但是支持的形式不尽相同，有的是通过语言本身、有的是通过库函数等。另外，从理论上来说，通过assertion方式可以证明程序的正确性，但是这是一项相当复杂的工作，目前还没有太多的实践意义。

在实现中，assertion就是在程序中的一条语句，它对一个boolean表达式进行检查，一个正确程序必须保证这个boolean表达式的值为true；如果该值为false，说明程序已经处于不正确的状态下，系统将给出警告或退出。一般来说，assertion用于保证程序最基本、关键的正确性。assertion检查通常在开发和测试时开启。为了提高性能，在软件发布后，assertion检查通常是关闭的。下面简单介绍一下Java中assertion的实现。

1．1) 语法表示

在语法上，为了支持assertion，Java增加了一个关键字assert。它包括两种表达式，分别如下: 

  1. assert expression1;
  2. assert expression1: expression2;

在两种表达式中，expression1表示一个boolean表达式，expression2表示一个基本类型或者是一个对象(Object) ，基本类型包括boolean,char,double,float,int和long。由于所有类都为Object的子类，因此这个参数可以用于所有对象。

1．2) 语义含义

在运行时，如果关闭了assertion功能，这些语句将不起任何作用。如果打开了assertion功能，那么expression1的值将被计算，如果它的值为false，该语句强抛出一个AssertionError对象。如果assertion语句包括expression2参数，程序将计算出expression2的结果，然后将这个结果作为AssertionError的构造函数的参数，来创建AssertionError对象，并抛出该对象；如果expression1值为true，expression2将不被计算。

一种特殊情况是，如果在计算表达式时，表达式本身抛出Exception，那么assert将停止运行，而抛出这个Exception。

1．3) 一些assertion例子

下面是一些Assert的例子。

  1. assert0 < value;
  2. assert0 < value:"value="+value;
  3. assertref != null:"ref doesn't equal null";
  4. assertisBalanced();

1．4) 编译

由于assert是一个新关键字，使用老版本的JDK是无法编译带有assert的源程序。因此，我们必须使用JDK1.4(或者更新)的Java编译器，在使用Javac命令时，我们必须加上-source 1.4作为参数。-source 1.4表示使用JDK 1.4版本的方式来编译源代码，否则编译就不能通过，因为缺省的Javac编译器使用JDK1.3的语法规则。

一个简单的例子如下: 

javac -source 1.4 test.java

1．5) 运行

由于带有assert语句的程序运行时，使用了新的ClassLoader和Class类，因此，这种程序必须在JDK1.4(或者更高版本)的JRE下运行，而不能在老版本的JRE下运行。

由于我们可以选择开启assertion功能，或者不开启，另外我们还可以开启一部分类或包的assertion功能，所以运行选项变得有些复杂。通过这些选项，我们可以过滤所有我们不关心的类，只选择我们关心的类或包来观察。下面介绍两类参数: 

  1. 参数 **-esa**和 **-dsa**: 
  
    它们含义为开启(关闭)系统类的assertion功能。由于新版本的Java的系统类中，也使了assertion语句，因此如果用户需要观察它们的运行情况，就需要打开系统类的assertion功能 ，我们可使用-esa参数打开，使用 -dsa参数关闭。 -esa和-dsa的全名为-enablesystemassertions和-disenablesystemassertions，全名和缩写名有同样的功能。
  2. 参数 **-ea**和 **-ea**: 
  
    它们含义为开启(关闭)用户类的assertion功能: 通过这个参数，用户可以打开某些类或包的assertion功能，同样用户也可以关闭某些类和包的assertion功能。打开assertion功能参数为-ea；如果不带任何参数，表示打开所有用户类；如果带有包名称或者类名称，表示打开这些类或包；如果包名称后面跟有三个点，代表这个包及其子包；如果只有三个点，代表无名包。关闭assertion功能参数为-da，使用方法与-ea类似。
  
    -ea和-da的全名为-enableassertions和-disenableassertions，全名和缩写名有同样的功能。
  
    下面表格表示了参数及其含义，并有例子说明如何使用。 
      
        
          参数
        
        
        
          例子
        
        
        
          说明
        
      
      
      
        
          -ea
        
        
        
          java -ea
        
        
        
          打开所有用户类的assertion
        
      
      
      
        
          -da
        
        
        
          java -da
        
        
        
          关闭所有用户类的assertion
        
      
      
      
        
          -ea:<classname>
        
        
        
          java -ea:MyClass1
        
        
        
          打开MyClass1的assertion
        
      
      
      
        
          -da:<classname>
        
        
        
          java -da: MyClass1
        
        
        
          关闭MyClass1的assertion
        
      
      
      
        
          -ea:<packagename>
        
        
        
          java -ea:pkg1
        
        
        
          打开pkg1包的assertion
        
      
      
      
        
          -da:<packagename>
        
        
        
          java -da:pkg1
        
        
        
          关闭pkg1包的assertion
        
      
      
      
        
          -ea:...
        
        
        
          java -ea:...
        
        
        
          打开缺省包(无名包)的assertion
        
      
      
      
        
          -da:...
        
        
        
          java -da:...
        
        
        
          关闭缺省包(无名包)的assertion
        
      
      
      
        
          -ea:<packagename>...
        
        
        
          java -ea:pkg1...
        
        
        
          打开pkg1包和其子包的assertion
        
      
      
      
        
          -da:<packagename>...
        
        
        
          java -da:pkg1...
        
        
        
          关闭pkg1包和其子包的assertion
        
      
      
      
        
          -esa
        
        
        
          java -esa
        
        
        
          打开系统类的assertion
        
      
      
      
        
          -dsa
        
        
        
          java -dsa
        
        
        
          关闭系统类的assertion
        
      
      
      
        
          综合使用
        
        
        
          java -dsa:MyClass1:pkg1
        
        
        
          关闭MyClass1和pkg1包的assertion
        
      
    
    
    其中...代表，此包和其子包的含义。例如我们有两个包为pkg1和pkg1.subpkg。那么pkg1...就代表pkg1和pkg1.subpkg两个包。
  
    另外，Java为了让程序也能够动态开启和关闭某些类和包的assertion功能，Java修该了Class和ClassLoader的实现，增加了几个用于操作assert的API。下面简单说明一下几个API的作用。
  
    ClassLoader类中的几个相关的API:
  
    setDefaultAssertionStatus:用于开启/关闭assertion功能
  
    setPackageAssertionStatus:用于开启/关闭某些包的assertion功能
  
    setClassAssertionStatus: 用于开启/关闭某些类的assertion功能
  
    clearAssertionStatus: 用于关闭assertion功能  
    
    
    
    
    [回页首][1]
    
    assertion的设计问题
    
    首先，我们认为assertion是必要的。因为，如果没有统一的assertion机制，Java程序通常使用if-then-else或者switch-case语句进行assertion检查，而且检查的数据类型也不完全相同。assertion机制让Java程序员用统一的方式处理assertion问题，而不是按自己的方式处理。另外，如果用户使用自己的方式进行检查，那么这些代码在发布以后仍然将起作用，这可能会影响程序的性能。而从语言言层次支持assertion功能，这将把assertion对性能带来的负面影响降到最小。
    
    Java是通过增强一个关键字assert实现支持assertion，而不是使用一个库函数支持，这说明Java认为assertion对于语言本身来说是非常重要的。实际上，在Java的早期的规范中，Java是能够支持assert的，但是由于一些实现的限制，这些特性从规范中除去了。因此，assert的再次引入应该是恢复了Java对assert的支持。C语言就是通过Assert.h函数库实现断言的支持。
    
    Java的assertion的开启也和C语言不太一样，我们都知道在C语言中，assertion的开启是在编译时候决定的。当我们使用debug方式编译程序时候，assertion被开启，而使用release方式编译时候，assertion自动被关闭。而Java的assertion却是在运行的时候进行决定的。其实，这两种方式是各有优缺点。如果采用编译时决定方式，开发人员将处理两种类型的目标码，debug版本和release版本，这加大了文档管理的难度，但是提高了代码的运行效率。Java采用运行时决定的方式，这样所有的assertion信息将置于目标代码中，同一目标代码可以选择不同方式运行，增强目标代码的灵活性，但是它将牺牲因为assertion而引起一部分性能损失。Java专家小组认为，所牺牲的性能相当小，因此java采用了运行时决定方式。
    
    另外，我们注意到AssertionError作为Error的一个子类，而不是RuntimeException。关于这一点，专家组也进行了长期的讨论。Error代表一些异常的错误，通常是不可以恢复的，而RuntimeException强调该错误在运行时才发生的特点。AssertionError通常为非常关键的错误，这些错误往往是不容易恢复的，而且assertion机制也不鼓励程序员对这种错误进行恢复。因此，为了强调assertion的含义，Java专家小组选择了让AssertError为Error的子类。
    
    
    
    
    [回页首][1]
    
    assertion与继承
    
    在本节，我们将考虑assertion与继承的关系，研究assert是如何定位的。如果开启一个子类的assertion，那么它的父类的assertion是否执行？
    
    下面的例子将显示如果一个assert语句在父类，而当它的子类调用它时，该assert为false。我们看看在不同的情况下，该assertion是否被处理。
    
    
      
        
          class Base
{
  public void baseMethod()
  {
    assert      false : "Assertion failed:This is base ";// 总是assertion失败
    System.out.println("Base Method");
  }
}
class Derived
  extends Base
{
  public void derivedMethod()
  {
    assert false: "Assertion failed:This is derive";// 总是assertion失败
    System.out.println( "Derived Method" );
  }
  public static void main( String[] args )
  {
    try
    {
      Derived derived = new Derived();
      derived.baseMethod(  );
      derived.derivedMethod();
    }
    catch( AssertionError ae )
    {
      System.out.println(ae);
    }
  }
}
        
      
    
    
    
    
    
      
        
          运行命令
        
        
        
          含义
        
        
        
          结果
        
      
      
      
        
          Java Derived
        
        
        
          不启用assertion
        
        
        
          Base MethodDerived Method
        
      
      
      
        
          Java -ea Derived
        
        
        
          开启所有assertion
        
        
        
          Java.lang.AssertionError:Assertion Failed:This is base
        
      
      
      
        
          Java -da Derived
        
        
        
          关闭所有assertion
        
        
        
          Base MethodDerived Method
        
      
      
      
        
          Java -ea:Base Derived
        
        
        
          仅打开Base的assertion
        
        
        
          Java.lang.AssertionError:Assertion Failed:This is base
        
      
      
      
        
          Java -ea:Derived Derived
        
        
        
          仅打开Derived的assertion
        
        
        
          Base MethodJava.lang.AssertionError:Assertion Failed:This is derived
        
      
    
    
    从这个例子我们可以看出，父类的assert语句将只有在父类的assert开启才起作用，如果仅仅开启子类的assert，父类的assert仍然不运行。例如，我们执行java -ea:Derived Derived的时候，Base类的assert语句并不执行。因此，我们可以认为，assert语句不具有继承功能。
    
    
    
    
    [回页首][1]
    
    assertion的使用
    
    assertion的使用是一个复杂的问题，因为这将涉及到程序的风格，assertion运用的目标，程序的性质等问题。通常来说，assertion用于检查一些关键的值，并且这些值对整个程序，或者局部功能的完成有很大的影响，并且这种错误不容易恢复的。assertion表达式应该短小、易懂，如果需要评估复杂的表达式，应该使用函数计算。以下是一些使用assertion的情况的例子，这些方式可以让java程序的可靠性更高。
    
      1. 检查控制流； 在if-then-else和swith-case语句中，我们可以在不应该发生的控制支流上加上assert false语句。如果这种情况发生了，assert能够检查出来。 例如: x取值只能使1,2,3，我们的程序可以如下表示
  
        
          
            
                  switch (x)
     { case 1: …;
          case 2: …;
          case 3: …
      default: assert false:"x value is invalid: "+x;
}
            
          
        
    
      2. 在私有函数计算前，检查输入参数是否有效；对于一私有些函数，要求输入满足一些特定的条件，那么我们可以在函数开始处使用assert进行参数检查。对于公共函数，我们通常不使用assertion检查，因为一般来说，公共函数必须对无效的参数进行检查和处理。而私有函数往往是直接使用的。
  
        例如: 某函数可能要求输入的参数必须不为null。那么我们可以在函数的一开始加上 `assert parameter1!=null : "paramerter is null in test method";`
      3. 在函数计算后，检查函数结果是否有效；对于一些计算函数，函数运行完成后，某些值需要保证一定的性质，因此我们可以通过assert检查该值。 例如，我们有一个计算绝对值的函数，那么我们就可以在函数的结果处，加上一个语句: 
  
        
          
            
              assert  value>=0:"Value should be bigger than 0:"+value;
            
          
        
        
        通过这种方式，我们可以对函数计算完的结果进行检查。 
        
          * 检查程序不变量；有些程序中，存在一些不变量，在程序的运行生命周期，这些不变量的值都是不变的。这些不变量可能是一个简单表达式，也可能是一个复杂的表达式。对于一些关键的不变量，我们可以通过assert进行检查。 例如，在一个财会系统中，公司的支出和收入必须保持一定的平衡关系，因此我们可以编写一个表达式检查这种平衡关系，如下表示。
  
            
              
                
                        private boolean isBalance() {
           ……
         }
                
              
            
            
            在这个系统中，在一些可能影响这种平衡关系的方法的前后，我们都可以加上assert验证:  `assert isBalance():"balance is destoried";`  
            
            
            
            
            [回页首][1]
            
            结论
            
            assertion为开发人员提供了一种灵活地调试和测试机制，它的使用也非常简单、方便。但是，如何规范、系统地使用assertion(特别是在Java语言中)仍然是一个亟待研究的问题。
            
            
            
            参考资料
            
              1. JSR 41 A Simple Assertion Facility [http://jcp.org/jsr/detail/41.jsp](http://jcp.org/jsr/detail/41.jsp)
              2. Wm. Paul Rogers, J2SE 1.4 premieres Java's assertion capabilities [http://www.javaworld.com/javaworld/jw-11-2001/jw-1109-assert.html?](http://www.javaworld.com/javaworld/jw-11-2001/jw-1109-assert.html?)
              3. J2SE 1.4 Documents, Programming With Assertions [http://java.sun.com/j2se/1.4/docs/guide/lang/assert.html](http://java.sun.com/j2se/1.4/docs/guide/lang/assert.html)
              4. John Zukowski, Mastering Java 2, J2SE 1.4
            
            作者简介
            
            
              
                
                  欧阳辰，北京大学计算机系硕士毕业，98年起开始研究基于java的软件开发、测试，参与开发、测试过多个基于Java的应用程序和Web服务项目。联系方式 yeekee@sina.com
                
              
              
              
                
                  周欣，北京大学计算机系在读博士生，主要研究方向: 程序理解、逆向工程及软件度量，联系方式 zhouxin@sei.pku.edu.cn。
                
              
            

 [1]: http://www.ibm.com/developerworks/cn/java/l-javaassertion/index.html#ibm-pcon