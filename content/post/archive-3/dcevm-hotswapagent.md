---
title: DCEVM, HotSwapAgent
author: "-"
date: 2019-12-17T04:29:09+00:00
url: /?p=15208
categories:
  - Uncategorized

tags:
  - reprint
---
## DCEVM, HotSwapAgent
https://blog.csdn.net/u013613428/article/details/51499911

要高效的开发Java代码，那就必须要让java像js一样，修改过的代码可以实时的反应出来。要了解如何做到这一点，我们先要知道JVM是如何工作的: 

我们知道，JAVA程序都是运行在java虚拟机上面 (当然JVM有两种类型，JDK和单纯的JRE，这里我们主要是指的JDK，因为只有JDK包含了debug功能，而我们只有在debug端口打开的情况下才能实现run time class load) ，我们的写的每一个Java文件，会被编译器编译成为class文件，然后根据选择不同的打包选择，比如说 (jar, war, ear) ，被打包存放到系统的classpath中。在运行一个java程序的时候，会有几个步骤, 包括装载，链接，初始化，翻译 (在翻译成机器码的时候同时会对代码进行优化，inline) ，运行，就如下图

这里的关键，就是这个classloader。所有的类都会在jvm中生成为class对象，存放在内存当中， (这里，主要分成两部分，常量池和方法字节码) 当我们的程序生成一个类的实例或instance时候，就会根据这个类对象，分配和初始化内存用于存储对象的field，然后在调用对象方法的时候，则从class对象中获取方法字节码，如下图: 

因此，如果我们能够在JVM里面途欢这个class对象，那么我们创建的所有object或instance，在调用函数的时候，就可以动态获得你修改之后的代码。如下图: 

hotswap的原理，就是替换jvm里面的class对象. Sun 在2002年把这项技术引入到java 1.4的JVM中，Hotswap需要和debuggerAPI一起协同工作，我们可以通过debugger来更新jvm里面同名的class bytecode

因此，这也就限制了，我们在使用hotswap的时候，必须使用debug mode.因此也就限制了java app必须是运行在jdk上，而不是jre上，JAVA_HOME必须指向JDK。

说了这么多理论，回到我们最初的话题，如何做到hotswap呢，步骤很简单: 

用debug模式attach我们的app
  
修改你的java文件，并且编译
  
这时，神奇的事情发生了，如下图

我们的class被reload了，我们可以不用重新把app部署到服务器上就可以直接看修改代码之后的结果。

等等，天底下有这么容易的事情吗？！这个solution是有缺陷的，那就是我们只能简单修改class method的内容，如果我们新添加了Method,field，或者在method里面引用了新的lib，增加了Import语句，那么对不起，你会看到: 

hot swap失败了。

那么有没有什么解决方案呢？有！收费的JRebel，或者免费的HotSwapAgent+DCEVM

让我们来看看什么是DCEVM:

https://dcevm.github.io/
  
The Dynamic Code Evolution VirtualMachine (DCEVM)is a modification of the Java HotSpot(TM) VM that allows unlimited redefinitionof loaded classes at runtime. The current hotswapping mechanism of the HotSpot(TM) VM allows only changing methodbodies. Our enhanced VMallows adding and removing fields and methods as well as changes to the supertypes of a class.
  
什么是hotswapAgent:
  
uhttp://www.hotswapagent.org/
  
uHotswap agent does the work of reloadingresources and framework configuration (Spring, Hibernate, ...)
  
uHotswapagentis a plugin container with plugin manager, plugin registry, and several agentservices (e.g. to watch for class/resource change). It helps with common tasksand classloading issues. It scans classpath for class annotated with @Pluginannotation, injects agent services and registers reloading hooks. Runtimebytecode modification is provided by javaasist library.

具体怎么用？

照着我上头给的两个地址安装他们，具体怎么搞，我比较懒，就不写了 (注意，在安装DCEVM的时候，请用临时替换) "InstallDCEVM as altjvm" 

配置你的运行脚本 (假设你的APP是运行在各种服务器上，比如tomcat, jboss等) ，上头两个网站也有，别告诉我你看不懂英文，我还是懒，不想写
  
运行的程序，检查hotswapAgent有没有起来，有没有使用DCEVM(注意下图的 -XXaltjvm=dcevm)

然后，随意修改的java代码，享受编译之后直接替换的乐趣吧
  
————————————————
  
版权声明: 本文为CSDN博主「点火三周」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/u013613428/article/details/51499911