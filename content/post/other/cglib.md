---
title: cglib
author: "-"
date: 2012-12-15T14:05:37+00:00
url: /?p=4901
categories:
  - Java

tags:
  - reprint
---
## cglib
cglib是一个强大的,高性能,高质量的Code生成类库,它可以在运行期扩展Java类与实现Java接口。Hibernate用它来实现PO字节码的动态生成。


CGLIB包的介绍


代理为控制要访问的目标对象提供了一种途径。当访问对象时,它引入了一个间接的层。JDK自从1.3版本开始,就引入了动态代理,并且经常被用来动态地创建代理。JDK的动态代理用起来非常简单,但它有一个限制,就是使用动态代理的对象必须实现一个或多个接口。如果想代理没有实现接口的继承的类,该怎么办？现在我们可以使用CGLIB包


CGLIB是一个强大的高性能的代码生成包。它广泛的被许多AOP的框架使用,例如Spring AOP和dynaop,为他们提供方法的interception (拦截) 。最流行的OR Mapping工具hibernate也使用CGLIB来代理单端single-ended(多对一和一对一)关联 (对集合的延迟抓取,是采用其他机制实现的) 。EasyMock和jMock是通过使用模仿 (moke) 对象来测试java代码的包。它们都通过使用CGLIB来为那些没有接口的类创建模仿 (moke) 对象。


CGLIB包的底层是通过使用一个小而快的字节码处理框架ASM,来转换字节码并生成新的类。除了CGLIB包,脚本语言例如Groovy和BeanShell,也是使用ASM来生成java的字节码。当不鼓励直接使用ASM,因为它要求你必须对JVM内部结构包括class文件的格式和指令集都很熟悉。

## CGLIB

代理为控制要访问的目标对象提供了一种途径。当访问对象时，它引入了一个间接的层。JDK自从1.3版本开始，就引入了动态代理，并且经常被用来动态地创建代理。JDK的动态代理用起来非常简单，但它有一个限制，就是使用动态代理的对象必须实现一个或多个接口。如果想代理没有实现接口的继承的类，该怎么办？现在我们可以使用CGLIB包
  
CGLIB是一个强大的高性能的代码生成包。它广泛的被许多AOP的框架使用，例如Spring AOP和dynaop，为他们提供方法的interception (拦截) 。最流行的OR Mapping工具hibernate也使用CGLIB来代理单端single-ended(多对一和一对一)关联 (对集合的延迟抓取，是采用其他机制实现的) 。EasyMock和jMock是通过使用模仿 (moke) 对象来测试java代码的包。它们都通过使用CGLIB来为那些没有接口的类创建模仿 (moke) 对象。
  
CGLIB包的底层是通过使用一个小而快的字节码处理框架ASM，来转换字节码并生成新的类。除了CGLIB包，脚本语言例如Groovy和BeanShell，也是使用ASM来生成java的字节码。当然不鼓励直接使用ASM，因为它要求你必须对JVM内部结构包括class文件的格式和指令集都很熟悉。Hibernate用它来实现PO(Persistent Object 持久化对象)字节码的动态生成。

http://baike.baidu.com/view/1254036.htm?fr=aladdin