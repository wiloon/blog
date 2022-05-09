---
title: Java assert
author: "-"
date: 2014-11-26T06:40:20+00:00
url: /?p=7038
categories:
  - Inbox
tags:
  - reprint
---
## Java assert
http://lavasoft.blog.51cto.com/62575/43735
  
一、概述

在C和C++语言中都有assert关键，表示断言。
  
在Java中，同样也有assert关键字，表示断言，用法和含义都差不多。

二、语法

在Java中，assert关键字是从JAVA SE 1.4 引入的，为了避免和老版本的Java代码中使用了assert关键字导致错误，Java在执行的时候默认是不启动断言检查的 (这个时候，所有的断言语句都将忽略！) ，如果要开启断言检查，则需要用开关-enableassertions或-ea来开启。

assert关键字语法很简单，有两种用法: 

1. assert <boolean表达式>
  
如果<boolean表达式>为true，则程序继续执行。
  
如果为false，则程序抛出AssertionError，并终止执行。

2. assert <boolean表达式> : <错误信息表达式>
  
如果<boolean表达式>为true，则程序继续执行。
  
如果为false，则程序抛出java.lang.AssertionError，并输入<错误信息表达式>。

三、应用实例

下面给出一个例子，通过例子说明其用法: 

public class AssertFoo {
      
public static void main(String args[]) {
          
//断言1结果为true，则继续往下执行
          
assert true;
          
System.out.println("断言1没有问题，Go！");

        System.out.println("\n-----------------\n");
    
        //断言2结果为false,程序终止
        assert false : "断言失败，此表达式的信息将会在抛出异常的时候输出！";
        System.out.println("断言2没有问题，Go！");
    }
    

}

保存代码到C:\AssertFoo.java，然后按照下面的方式执行，查看控制台输出结果: 

1. 编译程序: 
  
C:>javac AssertFoo.java

2. 默认执行程序，没有开启-ea开关: 
  
C:>java AssertFoo
  
断言1没有问题，Go！

* * *

断言2没有问题，Go！

3. 开启-ea开关，执行程序: 
  
C:>java -ea AssertFoo
  
断言1没有问题，Go！

* * *

Exception in thread "main" java.lang.AssertionError: 断言失败，此表达式的信息将
  
会在抛出异常的时候输出！
          
at AssertFoo.main(AssertFoo.java:10)

四、陷阱

assert关键字用法简单，但是使用assert往往会让你陷入越来越深的陷阱中。应避免使用。笔者经过研究，总结了以下原因: 

1. assert关键字需要在运行时候显式开启才能生效，否则你的断言就没有任何意义。而现在主流的Java IDE工具默认都没有开启-ea断言检查功能。这就意味着你如果使用IDE工具编码，调试运行时候会有一定的麻烦。并且，对于Java Web应用，程序代码都是部署在容器里面，你没法直接去控制程序的运行，如果一定要开启-ea的开关，则需要更改Web容器的运行配置参数。这对程序的移植和部署都带来很大的不便。

2. 用assert代替if是陷阱之二。assert的判断和if语句差不多，但两者的作用有着本质的区别: assert关键字本意上是为测试调试程序时使用的，但如果不小心用assert来控制了程序的业务流程，那在测试调试结束后去掉assert关键字就意味着修改了程序的正常的逻辑。

3. assert断言失败将面临程序的退出。这在一个生产环境下的应用是绝不能容忍的。一般都是通过异常处理来解决程序中潜在的错误。但是使用断言就很危险，一旦失败系统就挂了。

五、对assert的思考

assert既然是为了调试测试程序用，不在正式生产环境下用，那应该考虑更好的测试JUint来代替其作用，JUint相对assert关键的所提供的功能是有过之而无不及。当然完全可以通过IDE debug来进行调试测试。在此看来，assert的前途一片昏暗。

因此，应当避免在Java中使用assert关键字，除非哪一天Java默认支持开启-ea的开关，这时候可以考虑。对比一下，assert能给你带来多少好处，多少麻烦，这是我们选择是否使用的的原则。

以上仅仅代表我个人观点，欢迎大家留言讨论。