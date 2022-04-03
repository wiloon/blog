---
title: java basic
author: "-"
date: 2012-09-20T02:59:54+00:00
url: /?p=4117
categories:
  - Java
tags:
  - Java

---
## java basic
### JDK和JRE的区别
JRE：Java Runtime Environment 的简称，java 运行时环境，为 java 的运行提供了所需环境。
- Java 虚拟机
- jfr

JDK：Java Development Kit 的简称，java 开发工具包，提供了 java 的开发环境和运行环境。
- 包含了JRE
- 编译器: javac
- 其他的工具: JavaDoc，Java调试器(jdb), jcmd, jstat, jmap

JDK 其实包含了 JRE，同时还包含了编译 java 源码的编译器 javac，还包含了很多 java 程序调试和分析的工具。简单来说：如果你需要运行 java 程序，只需安装 JRE 就可以了，如果你需要编写 java 程序，需要安装 JDK。

>http://www.wiloon.com/jdk-jre

### == vs equals
#### ==
对于基本类型和引用类型 == 的作用效果是不同的  
基本类型：比较的是值是否相同； 
引用类型：比较的是引用是否相同； 

```java
String x = "string";
String y = "string";
String z = new String("string");
System.out.println(x==y); // true
System.out.println(x==z); // false
System.out.println(x.equals(y)); // true
System.out.println(x.equals(z)); // true
```


代码解读：因为 x 和 y 指向的是同一个引用，所以 == 也是 true，而 new String()方法则重写开辟了内存空间，所以 == 结果为 false，而 equals 比较的一直是值，所以结果都为 true。

#### equals
equals 本质上就是 ==，只不过 String 和 Integer 等重写了 equals 方法，把它变成了值比较。

### Math.round(-1.5)
等于 -1，因为在数轴上取值时，中间值 (0.5）向右取整，所以正 0.5 是向1取整，-0.5向0取整

```java
System.out.println(Math.round(1.4));
System.out.println(Math.round(1.5));
System.out.println(Math.round(1.6));

System.out.println(Math.round(-1.4));
System.out.println(Math.round(-1.5));
System.out.println(Math.round(-1.6));

1
2
2
-1
-1
-2
```

### String str="i"与 String str=new String("i")
不一样，因为内存的分配方式不一样。String str="i"的方式，java 虚拟机会将其分配到常量池中；而 String str=new String("i") 则会被分到堆内存中。

### 面向对象的三个基本特征: 封装、继承、多态。
#### 封装:
封装隐藏了类的内部实现机制，可以在不影响使用的情况下改变类的内部结构，同时也保护了数据。对外界而已它的内部细节是隐藏的，暴露给外界的只是它的访问方法。

封装 (Encapsulation) 是面向对象方法的重要原则，就是把对象的属性和操作 (或服务) 结合为一个独立的整体，并尽可能隐藏对象的内部实现细节。

封装是把过程和数据包围起来，对数据的访问只能通过已定义的接口。面向对象计算始于这个基本概念，即现实世界可以被描绘成一系列完全自治、封装的对象，这些对象通过一个受保护的接口访问其他对象。封装是一种信息隐藏技术，在java中通过关键字private实现封装。什么是封装？封装把对象的所有组成部分组合在一起，封装定义程序如何引用对象的数据，封装实际上使用方法将类的数据隐藏起来，控制用户对类的修改和访问数据的程度。

封装是面向对象的特征之一，是对象和类概念的主要特性。

封装，也就是把客观事物封装成抽象的类，并且类可以把自己的数据和方法只让可信的类或者对象操作，对不可信的进行信息隐藏。

即现实世界可以被描绘成一系列完全自治、封装的对象，这些对象通过一个受保护的接口访问其他对象。


#### 继承:

继承是为了重用父类代码。两个类若存在IS-A的关系就可以使用继承。，同时继承也为实现多态做了铺垫。

继承是一种联结类的层次模型，并且允许和鼓励类的重用，它提供了一种明确表述共性的方法。对象的一个新类可以从现有的类中派生，这个过程称为类继承。新类继承了原始类的特性，新类称为原始类的派生类 (子类) ，而原始类称为新类的基类 (父类) 。派生类可以从它的基类那里继承方法和实例变量，并且类可以修改或增加新的方法使之更适合特殊的需要。

继承是一种联结类的层次模型，并且允许和鼓励类的重用，它提供了一种明确表述共性的方法。对象的一个新类可以从现有的类中派生，这个过程称为类继承。新类继承了原始类的特性，新类称为原始类的派生类 (子类) ，而原始类称为新类的基类 (父类) 。派生类可以从它的基类那里继承方法和实例变量，并且类可以修改或增加新的方法使之更适合特殊的需要。


### 多态, polymorphism

多态性是指允许不同类的对象对同一消息作出响应。多态性包括参数化多态性和包含多态性。多态性语言具有灵活、抽象、行为共享、代码共享的优势，很好的解决了应用程序函数同名问题。

  http://wiloon.com/polymorphism


### 抽象: 

抽象就是忽略一个主题中与当前目标无关的那些方面，以便更充分地注意与当前目标有关的方面。抽象并不打算了解全部问题，而只是选择其中的一部分，暂时不用部分细节。抽象包括两个方面，一是过程抽象，二是数据抽象。


### 抽象和封装的不同点

抽象和封装是互补的概念。一方面，抽象关注对象的行为。另一方面，封装关注对象行为的细节。一般是通过隐藏对象内部状态信息做到封装，因此，封装可以看成是用来提供抽象的一种策略。


### 什么是Java虚拟机？为什么Java被称作是"平台无关的编程语言"？

Java虚拟机是一个可以执行Java字节码的虚拟机进程。Java源文件被编译成能被Java虚拟机执行的字节码文件。

Java被设计成允许应用程序可以运行在任意的平台，而不需要程序员为每一个平台单独重写或者是重新编译。Java虚拟机让这个变为可能，因为它知道底层硬件平台的指令长度和其他特性。




### static 关键字是什么意思？Java中是否可以覆盖(override)一个private或者是static的方法？

"static"关键字表明一个成员变量或者是成员方法可以在没有所属的类的实例变量的情况下被访问。
  
Java中static方法不能被覆盖，因为方法覆盖是基于运行时动态绑定的，而static方法是编译时静态绑定的。static方法跟类的任何实例都不相关，所以概念上不适用。

>wiloon.com/static

### Java 基本数据类型, String

String 不是基本数据类型，基本数据类型包括 byte, boolean, char, short, int, float, long, double。 
java.lang.String类是final类型的，因此不可以继承这个类、不能修改这个类。为了提高效率节省空间，我们应该用StringBuffer类.
>wiloon.com/java/primitive

### String、StringBuffer、StringBuilder。
String 声明的是不可变的对象，每次操作都会生成新的 String 对象
StringBuffer 是线程安全的，而 StringBuilder 是非线程安全的，但 StringBuilder 的性能却高于 StringBuffer，所以在单线程环境下推荐使用 StringBuilder，多线程环境下推荐使用 StringBuffer。

### 什么是自动拆装箱？

自动装箱是Java编译器在基本数据类型和对应的对象包装类型之间做的一个转化。比如: 把int转化成Integer，double转化成double，等等。反之就是自动拆箱。


  
    自动装箱 拆箱
  





### 什么是构造函数？什么是构造函数重载？什么是复制构造函数？

当新对象被创建的时候，构造函数会被调用。每一个类都有构造函数。在程序员没有给类提供构造函数的情况下，Java编译器会为这个类创建一个默认的构造函数。

Java中构造函数重载和方法重载很相似。可以为一个类创建多个构造函数。每一个构造函数必须有它自己唯一的参数列表。

Java不支持像C++中那样的复制构造函数，这个不同点是因为如果你不自己写构造函数的情况下，Java不会创建默认的复制构造函数。


### 什么是值传递和引用传递？

对象被值传递，意味着传递了对象的一个副本。因此，就算是改变了对象副本，也不会影响源对象的值。

对象被引用传递，意味着传递的并不是实际的对象，而是对象的引用。因此，外部对引用对象所做的改变会反映到所有的对象上。


### int 和 Integer 的区别

Java 提供两种不同的类型: 引用类型和原始类型 (或内置类型) 。int是java的原始数据类型，Integer是java为int提供的封装类。Java为每个原始类型提供了封装类。

原始类型boolean,char,byte,short,int,long,float,double;

封装类 Boolean,Character, Byte, Short, Integer, Long, Float, Double;

引用类型和原始类型的行为完全不同，并且它们具有不同的语义。引用类型和原始类型具有不同的特征和用法，它们包括: 大小和速度问题，这种类型以哪种类型的数据结构存储，当引用类型和原始类型用作某个类的实例数据时所指定的缺省值。对象引用实例变量的缺省值为 null，而原始类型实例变量的缺省值与它们的类型有关.

    引用类型 基本类型

http://www.wiloon.com/?p=4120&embed=true#?secret=3QUltjLSBh


### 异常
异常表示程序运行过程中可能出现的非正常状态，运行时异常表示虚拟机的通常操作中可能遇到的异常，是一种常见运行错误。java编译器要求方法必须声明抛出可能发生的非运行时异常，但是并不要求必须声明抛出未被捕获的运行时异常。

error 表示恢复不是不可能但很困难的情况下的一种严重问题。比如说内存溢出。不可能指望程序能处理这样的情况。 exception 表示一种设计或实现问题。也就是说，它表示如果程序运行正常，从不会发生的情况。

    运行时异常/一般异常

- ArrayList, Vector, LinkedList 区别
>wiloon.com/collection

### HashMap和Hashtable

HashMap是Hashtable的轻量级实现 (非线程安全的实现) ，他们都完成了Map接口，主要区别在于HashMap允许空 (null) 键值 (key) Hashtable不允许。HashMap由于非线程安全，效率上可能高于Hashtable。 而 HashMap把Hashtable的contains方法去掉了，改成containsvalue和containsKey。因为contains方法容易让人引起误解。 Hashtable继承自Dictionary类，而HashMap是Java1.2引进的Map interface的一个实现。 最大的不同是，Hashtable的方法是Synchronize的，而HashMap不是，在多个线程访问Hashtable时，不需要自己为它的方法实现同步，而HashMap 就必须为之提供外同步。 Hashtable和HashMap采用的hash/rehash算法都大概一样，所以性能不会有很大的差异。

http://www.wiloon.com/?p=4144&embed=true#?secret=Zea2iEVLs2


  
    HashSet、TreeSet、LinkedHashSet
  


http://www.wiloon.com/?p=6726&embed=true#?secret=PuZXM3VEiO

### Iterator和ListIterator的区别是什么？

下面列出了他们的区别: 

  * Iterator可用来遍历Set和List集合，但是ListIterator只能用来遍历List。
  * Iterator对集合只能是前向遍历，ListIterator既可以前向也可以后向。
  * ListIterator实现了Iterator接口，并包含其他的功能，比如: 增加元素，替换元素，获取前一个和后一个元素的索引，等等。


### Comparable 和 Comparator 接口是干什么的？列出它们的区别。

Java提供了只包含一个compareTo()方法的Comparable接口。这个方法可以个给两个对象排序。具体来说，它返回负数，0，正数来表明输入对象小于，等于，大于已经存在的对象。

Java提供了包含compare()和equals()两个方法的Comparator接口。compare()方法用来给两个输入参数排序，返回负数，0，正数表明第一个参数是小于，等于，大于第二个参数。equals()方法需要一个对象作为参数，它用来决定输入参数是否和comparator相等。只有当输入参数也是一个comparator并且输入参数和当前comparator的排序结果是相同的时候，这个方法才返回true。


### 什么是Java优先级队列(Priority Queue)？

PriorityQueue是一个基于优先级堆的无界队列，它的元素是按照自然顺序(natural order)排序的。在创建的时候，我们可以给它提供一个负责给元素排序的比较器。PriorityQueue不允许null值，因为他们没有自然顺序，或者说他们没有任何的相关联的比较器。最后，PriorityQueue不是线程安全的，入队和出队的时间复杂度是O(log(n))。


### &和&&

&是位运算符，表示按位与运算，&&是逻辑运算符，表示逻辑与 (and) 。


  
    移位运算符

### final, finally, finalize
#### final
final 修饰的类叫最终类，该类不能被继承。
final 修饰的方法不能被重写。
final 修饰的变量叫常量，常量必须初始化，初始化之后值就不能被修改。

#### finally
finally 是异常处理语句结构的一部分，表示总是执行。
#### finalize
finalize 是Object类的一个方法，在垃圾收集器执行的时候会调用被回收对象的此方法，可以覆盖此方法提供垃圾收集时的其他资源回收，例如关闭文件等。

>JVM内存管理-Java垃圾回收调优, http://www.wiloon.com/?p=4618

### 线程的几种可用状态。

线程在执行过程中，可以处于下面几种状态: 

  * 就绪(Runnable):线程准备运行，不一定立马就能开始执行。
  * 运行中(Running): 进程正在执行线程的代码。
  * 等待中(Waiting):线程处于阻塞的状态，等待外部的处理结束。
  * 睡眠中(Sleeping): 线程被强制睡眠。
  * I/O阻塞(Blocked on I/O): 等待I/O操作完成。
  * 同步阻塞(Blocked on Synchronization): 等待获取锁。
  * 死亡(Dead): 线程完成了执行。

### **sleep(), wait()   **

sleep是线程类 (Thread) 的方法，导致此线程暂停执行指定时间，给执行机会给其他线程，但是监控状态依然保持，到时后会自动恢复。调用sleep不会释放对象锁。

wait是Object类的方法，对此对象调用wait方法导致本线程放弃对象锁，进入等待此对象的等待锁定池，只有针对此对象发出notify方法 (或notifyAll) 后本线程才进入对象锁定池准备获得对象锁进入运行状态.


  
### java 线程 yield(), sleep(), wait(), join()
>http://www.wiloon.com/java/thread/sleep


### **Overload和Override的区别。Overloaded的方法是否可以改变返回值的类型?**

方法的重写Overriding和重载Overloading是Java多态性的不同表现。重写Overriding是父类与子类之间多态性的一种表现，重载Overloading是一个类中多态性的一种表现。如果在子类中定义某方法与其父类有相同的名称和参数，我们说该方法被重写 (Overriding)。子类的对象使用这个方法时，将调用子类中的定义，对它而言，父类中的定义如同被"屏蔽"了。如果在一个类中定义了多个同名的方法，它们或有不同的参数个数或有不同的参数类型，则称为方法的重载(Overloading)。Overloaded的方法是可以改变返回值的类型。


  
    Java Override Overload 重写、覆盖、重载、多态
  





### **同步,异步 在什么情况下使用**

如果数据将在线程间共享。例如正在写的数据以后可能被另一个线程读到，或者正在读的数据可能已经被另一个线程写过了，那么这些数据就是共享数据，必须进行同步存取。 当应用程序在对象上调用了一个需要花费很长时间来执行的方法，并且不希望让程序等待方法的返回时，就应该使用异步编程，在很多情况下采用异步途径往往更有效率。


### abstract class interface
声明方法的存在而不去实现它的类被叫做抽象类 (abstract class) ，它用于要创建一个体现某些基本行为的类，并为该类声明方法，但不能在该类中实现该类的情况。不能创建abstract 类的实例。然而可以创建一个变量，其类型是一个抽象类，并让它指向具体子类的一个实例。不能有抽象构造函数或抽象静态方法。Abstract 类的子类为它们父类中的所有抽象方法提供实现，否则它们也是抽象类为。取而代之，在子类中实现该方法。知道其行为的其它类可以在类中实现这些方法。 接口 (interface) 是抽象类的变体。在接口中，所有方法都是抽象的。多继承性可通过实现这样的接口而获得。接口中的所有方法都是抽象的，没有一个有程序体。接口只可以定义static final成员变量。接口的实现与子类相似，除了该实现类不能从接口定义中继承行为。当类实现特殊接口时，它定义 (即将程序体给予) 所有这种接口的方法。然后，它可以在实现了该接口的类的任何对象上调用接口的方法。由于有抽象类，它允许使用接口名作为引用变量的类型。通常的动态联编将生效。引用可以转换到接口类型或从接口类型转换，instanceof 运算符可以用来决定某对象的类是否实现了接口。

>http://www.wiloon.com/?p=3336&embed=true#?secret=MLUWtzeM61

### heap和stack的区别
栈是一种线性集合，栈按照后进先出的方式进行处理。
http://www.wiloon.com/?p=4151

http://www.wiloon.com/?p=4151&embed=true#?secret=20KcOkpGBn


### Static Nested Class 和 Inner Class的不同。
Static Nested Class是被声明为静态 (static) 的内部类，它可以不依赖于外部类实例被实例化。而通常的内部类需要在外部类实例化后才能实例化。

http://www.wiloon.com/?p=6474

 http://www.wiloon.com/?p=6474&embed=true#?secret=yj3jOD5DN0


**assert**

**assertion(断言)在软件开发中是一种常用的调试方式，很多开发语言中都支持这种机制。在实现中，assertion就是在程序中的一条语句，它对一个boolean表达式进行检查，一个正确程序必须保证这个boolean表达式的值为true；如果该值为false，说明程序已经处于不正确的状态下，系统将给出警告或退出。一般来说，assertion用于保证程序最基本、关键的正确性。assertion检查通常在开发和测试时开启。为了提高性能，在软件发布后，assertion检查通常是关闭的。 **


**GC是什么? 为什么要有GC?**

GC是垃圾收集的意思 (Gabage Collection) ,内存处理是编程人员容易出现问题的地方，忘记或者错误的内存回收会导致


  
    JVM内存管理和JVM垃圾回收机制
  


http://www.wiloon.com/?p=4620&embed=true#?secret=hz71dhuu22


### 你了解大O符号(big-O notation)么？你能给出不同数据结构的例子么？

大O符号描述了当数据结构里面的元素增加的时候，算法的规模或者是性能在最坏的场景下有多么好。
  
大O符号也可用来描述其他的行为，比如: 内存消耗。因为集合类实际上是数据结构，我们一般使用大O符号基于时间，内存和性能来选择最好的实现。大O符号可以对大量数据的性能给出一个很好的说明。


### JVM的永久代中会发生垃圾回收么？
如果永久代满了或者是超过了临界值，会触发完全垃圾回收 (Full GC)。如果你仔细查看垃圾收集器的输出信息，就会发现永久代也是被回收的。这就是为什么正确的永久代大小对避免 Full GC 是非常重要的原因。请参考下Java8: 从永久代到元数据区
  
(译者注: Java8中已经移除了永久代，新加了一个叫做元数据区的native内存区)

### 如何权衡是使用无序的数组还是有序的数组？
有序数组最大的好处在于查找的时间复杂度是O(log n)，而无序数组是O(n)。有序数组的缺点是插入操作的时间复杂度是O(n)，因为值大的元素需要往后移动来给新元素腾位置。相反，无序数组的插入时间复杂度是常量O(1)。


### Java集合类框架的最佳实践有哪些？
  * 根据应用的需要正确选择要使用的集合的类型对性能非常重要，比如: 假如元素的大小是固定的，而且能事先知道，我们就应该用Array而不是ArrayList。
  * 有些集合类允许指定初始容量。因此，如果我们能估计出存储的元素的数目，我们可以设置初始容量来避免重新计算hash值或者是扩容。
  * 为了类型安全，可读性和健壮性的原因总是要使用泛型。同时，使用泛型还可以避免运行时的ClassCastException。
  * 使用JDK提供的不变类(immutable class)作为Map的键可以避免为我们自己的类实现hashCode()和equals()方法。
  * 编程的时候接口优于实现。
  * 底层的集合实际上是空的情况下，返回长度是0的集合或者是数组，不要返回null。

### Enumeration接口和Iterator接口的区别有哪些？

Enumeration速度是Iterator的2倍，同时占用更少的内存。但是，Iterator远远比Enumeration安全，因为其他线程不能够修改正在被iterator遍历的集合里面的对象。同时，Iterator允许调用者删除底层集合里面的元素，这对Enumeration来说是不可能的。

## JavaEE


**25、JSP中动态INCLUDE与静态INCLUDE的区别？** 动态INCLUDE用jsp:include动作实现 它总是会检查所含文件中的变化，适合用于包含动态页面，并且可以带参数。 静态INCLUDE用include伪码实现,定不会检查所含文件的变化，适用于包含静态页面<%@ include file="included.htm" %>

### forward 和redirect的区别
forward是服务器请求资源，服务器直接访问目标地址的URL，把那个URL的响应内容读取过来，然后把这些内容再发给浏览器，浏览器根本不知道服务器发送的内容是从哪儿来的，所以它的地址栏中还是原来的地址。 redirect就是服务端根据逻辑,发送一个状态码,告诉浏览器重新去请求那个地址，一般来说浏览器会用刚才请求的所有参数重新请求，所以session,request参数都可以获取。

**23、EJB与**JAVA** BEAN的区别？** **Java** Bean 是可复用的组件，对Java Bean并没有严格的规范，理论上讲，任何一个Java类都可以是一个Bean。但通常情况下，由于Java Bean是被容器所创建 (如Tomcat) 的，所以Java Bean应具有一个无参的构造器，另外，通常Java Bean还要实现Serializable接口用于实现Bean的持久性。Java Bean实际上相当于微软COM模型中的本地进程内COM组件，它是不能被跨进程访问的。Enterprise Java Bean 相当于DCOM，即分布式组件。它是基于Java的远程方法调用 (RMI) 技术的，所以EJB可以被远程访问 (跨进程、跨计算机) 。但EJB必须被布署在诸如Webspere、WebLogic这样的容器中，EJB客户从不直接访问真正的EJB组件，而是通过其容器访问。EJB容器是EJB组件的代理， EJB组件由容器所创建和管理。客户通过容器来访问真正的EJB组件。

## Servlet的生命周期，Servlet和CGI的区别。

Servlet被服务器实例化后，容器运行其init方法，请求到达时运行其service方法，service方法自动派遣运行与请求对应的doXXX方法 (doGet，doPost) 等，当服务器决定将实例销毁的时候调用其destroy方法。 与cgi的区别在于servlet处于服务器进程中，它通过多线程方式运行其service方法，一个实例可以服务于多个请求，并且其实例一般不会销毁，而CGI对每个请求都产生新的进程，服务完成后就销毁，所以效率上低于servlet。

### 字符串反转
StringBuilder 或者 stringBuffer 的 reverse() 方法

### String 类的常用方法
- indexOf()：返回指定字符的索引。
- charAt()：返回指定索引处的字符。

replace()：字符串替换。

trim()：去除字符串两端空白。

split()：分割字符串，返回一个分割后的字符串数组。

getBytes()：返回字符串的 byte 类型数组。

length()：返回字符串长度。

toLowerCase()：将字符串转成小写字母。

toUpperCase()：将字符串转成大写字符。

substring()：截取字符串。

equals()：字符串比较。

### 抽象类必须要有抽象方法吗
不需要，抽象类不一定非要有抽象方法。
### 抽象类能使用 final 修饰吗
不能，定义抽象类就是让其他类继承的，如果定义为 final 该类就不能被继承，这样彼此就会产生矛盾，所以 final 不能修饰抽象类

### 接口和抽象类有什么区别？
实现：抽象类的子类使用 extends 来继承；接口必须使用 implements 来实现接口。

构造函数：抽象类可以有构造函数；接口不能有。

main 方法：抽象类可以有 main 方法，并且我们能运行它；接口不能有 main 方法。

实现数量：类可以实现很多个接口；但是只能继承一个抽象类。

访问修饰符：接口中的方法默认使用 public 修饰；抽象类中的方法可以是任意访问修饰符。
### java 中 IO 流分为几种？



按功能来分：输入流 (input）、输出流 (output）。



按类型来分：字节流和字符流。

字节流和字符流的区别是：字节流按 8 位传输以字节为单位输入输出数据，字符流按 16 位传输以字符为单位输入输出数据。

- BIO、NIO、AIO 有什么区别
>wiloon.com/nio

### Files的常用方法都有哪些

### Collection 和 Collections 区别
java.util.Collection 是一个集合接口 (集合类的一个顶级接口）。它提供了对集合对象进行基本操作的通用接口方法。Collection接口在Java 类库中有很多具体的实现。Collection接口的意义是为各种具体的集合提供了最大化的统一操作方式，其直接继承接口有List与Set。

Collections 则是集合类的一个工具类/帮助类，其中提供了一系列静态方法，用于对集合中元素进行排序、搜索以及线程安全等各种操作。

### List、Set、Map 之间的区别
wiloon.com/collection/list-set-map

### HashMap 和 Hashtable 区别
wiloon.com/hash/map-table

- HashMap 还是 TreeMap
wiloon.com/red–black-tree

- HashMap 的实现原理
  - 谈谈你理解的 HashMap，讲讲其中的 get put 过程。
  - 1.8 做了什么优化？
  - 是线程安全的嘛？
  - 不安全会导致哪些问题？
  - 如何解决？有没有线程安全的并发容器？
  - ConcurrentHashMap 是如何实现的？ 1.7、1.8 实现有何不同？为什么这么做？

>wiloon.com/hashmap

### HashSet 的实现原理
>wiloon.com/hashset

### ArrayList 和 LinkedList 的区别
>wiloon.com/collection


### Java 2021
>https://zhuanlan.zhihu.com/p/64147696
### Java Core Sprout
>https://github.com/crossoverJie/JCSprout

>http://zangweiren.blog.51cto.com/412366/94392
>http://www.cnblogs.com/chenssy/p/3372798.html
>http://blog.csdn.net/ericbaner/article/details/3857268
>http://www.importnew.com/10980.html#oop