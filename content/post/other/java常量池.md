---
title: Java 常量池
author: "-"
date: 2013-03-06T06:37:47+00:00
url: constantpool
categories:
  - Java
tags:$
  - reprint
---
## Java 常量池
### 什么是常量
  
用final修饰的成员变量表示常量，值一旦给定就无法改变！
  
final修饰的变量有三种: 静态变量、实例变量和局部变量，分别表示三种类型的常量。

### Class 文件中的常量池
  
在Class文件结构中，最头的4个字节用于存储魔数 Magic Number，用于确定一个文件是否能被JVM接受，再接着4个字节用于存储版本号，前2个字节存储次版本号，后2个存储主版本号，再接着是用于存放常量的常量池，由于常量的数量是不固定的，所以常量池的入口放置一个U2类型的数据(constant_pool_count)存储常量池容量计数值。
  
常量池主要用于存放两大类常量: 字面量(Literal)和符号引用量(Symbolic References)，字面量相当于Java语言层面常量的概念，如文本字符串，声明为final的常量值等，符号引用则属于编译原理方面的概念，包括了如下三种类型的常量: 

类和接口的全限定名
  
字段名称和描述符
  
方法名称和描述符
  
方法区中的运行时常量池
  
运行时常量池是方法区的一部分。

### Class文件常量池
CLass文件的字节码包含有类的版本、字段、方法、接口等描述信息，还有就是常量池
常量池里面主要存放编译器生成的各种字面量和符号引用，这部分内容将在类加载后进入方法区的运行时常量池中存放。
  
运行时常量池相对于CLass文件常量池的另外一个重要特征是具备动态性，Java语言并不要求常量一定只有编译期才能产生，也就是并非预置入CLass文件中常量池的内容才能进入方法区运行时常量池，运行期间也可能将新的常量放入池中，这种特性被开发人员利用比较多的就是String类的intern()方法。

常量池中主要存放两类常量。

字面量。
符号引用。
字面量

字面量，给基本类型变量赋值的方式就叫做字面量或者字面值。 比如：String a=“b” ，这里“b”就是字符串字面量，同样类推还有整数字面值、浮点类型字面量、字符字面量。

符号引用

符号引用主要设涉及编译原理方面的概念，包括下面三类常量:

类和接口的全限定名(Full Qualified Name)，也就是Ljava/lang/String;，主要用于在运行时解析得到类的直接引用。


字段的名称和描述符(Descriptor)，字段也就是类或者接口中声明的变量，包括类级别变量(static)和实例级的变量。

方法的名称和描述符,方法的描述类似于JNI动态注册时的“方法签名”，也就是参数类型+返回值类型，比如下面的这种字节码，表示main方法和String返回类型。
### 运行时常量池
运行时常量池是每一个类或者接口的常量池 (Constant Pool)的运行时的表现形式。

我们知道，一个类的加载过程，会经过：加载、连接 (验证、准备、解析）、初始化的过程，而在类加载这个阶段，需要做以下几件事情：

通过一个类的全类限定名获取此类的二进制字节流。
在堆内存生成一个java.lang.Class对象,代表加载这个类,做为这个类的入口。
将class字节流的静态存储结构转化成方法区(元空间）的运行时数据结构。
而其中第三点，将class字节流代表的静态储存结构转化为方法区的运行时数据结构这个过程，就包含了class文件常量池进入运行时常量池的过程。
所以，运行时常量池的作用是存储class文件常量池中的符号信息，在类的解析阶段会把这些符号引用转换成直接引用(实例对象的内存地址),翻译出来的直接引用也是存储在运行时常量池中。class文件常量池的大部分数据会被加载到运行时常量池。

### 字符串常量池
字符串常量池，简单来说就是专门针对String类型设计的常量池。

字符串常量池的常用创建方式有两种。

String a="Hello";
String b=new String("Mic");
a这个变量，是在编译期间就已经确定的，会进入到字符串常量池。
b这个变量，是通过new关键字实例化，new是创建一个对象实例并初始化该实例，因此这个字符串对象是在运行时才能确定的，创建的实例在堆空间上。
简单总结一下：JVM之所以单独设计字符串常量池，是JVM为了提高性能以及减少内存开销的一些优化：

String对象作为Java语言中重要的数据类型，是内存中占据空间最大的一个对象。高效地使用字符串，可以提升系统的整体性能。
创建字符串常量时，首先检查字符串常量池是否存在该字符串，如果有，则直接返回该引用实例，不存在，则实例化该字符串放入常量池中。
字符串常量池是JVM所维护的一个字符串实例的引用表，在HotSpot VM中，它是一个叫做StringTable的全局表。在字符串常量池中维护的是字符串实例的引用，底层C++实现就是一个Hashtable。这些被维护的引用所指的字符串实例，被称作”被驻留的字符串”或”interned string”或通常所说的”进入了字符串常量池的字符串”!
### 封装类常量池
除了字符串常量池，Java的基本类型的封装类大部分也都实现了常量池。包括Byte,Short,Integer,Long,Character,Boolean

注意，浮点数据类型Float,Double是没有常量池的。
封装类的常量池是在各自内部类中实现的，比如IntegerCache(Integer的内部类)。要注意的是，这些常量池是有范围的：

### 常量池的好处
  
常量池是为了避免频繁的创建和销毁对象而影响系统性能，其实现了对象的共享。
  
例如字符串常量池，在编译阶段就把所有的字符串文字放到一个常量池中。
  
 (1) 节省内存空间: 常量池中所有相同的字符串常量被合并，只占用一个空间。
  
 (2) 节省运行时间: 比较字符串时，==比equals()快。对于两个引用变量，只用==判断引用是否相等，也就可以判断实际值是否相等。

### 双等号==的含义
  
基本数据类型之间应用双等号，比较的是他们的数值。
  
复合数据类型(类)之间应用双等号，比较的是他们在内存中的存放地址。

二.8种基本类型的包装类和常量池

java中基本类型的包装类的大部分都实现了常量池技术，
  
即 Byte,Short,Integer,Long,Character,Boolean；

Integer i1 = 40;
  
Integer i2 = 40;
  
System.out.println(i1==i2); //输出TRUE
  
这5种包装类默认创建了数值[-128，127] 的相应类型的缓存数据，但是超出此范围仍然会去创建新的对象。

//Integer 缓存代码 : 
  
public static Integer valueOf(int i) {
       
assert IntegerCache.high >= 127;
       
if (i >= IntegerCache.low && i <= IntegerCache.high)
           
return IntegerCache.cache[i + (-IntegerCache.low)];
       
return new Integer(i);
   
}
  
Integer i1 = 400;
  
Integer i2 = 400;
  
System.out.println(i1==i2);//输出false
  
两种浮点数类型的包装类Float,Double并没有实现常量池技术。

Double i1=1.2;
  
Double i2=1.2;
  
System.out.println(i1==i2);//输出false
  
应用常量池的场景
  
(1)Integer i1=40；Java 在编译的时候会直接将代码封装成Integer i1=Integer.valueOf(40);，从而使用常量池中的对象。
  
(2)Integer i1 = new Integer(40);这种情况下会创建新的对象。

Integer i1 = 40;
  
Integer i2 = new Integer(40);
  
System.out.println(i1==i2);//输出false
  
Integer比较更丰富的一个例子

Integer i1 = 40;
  
Integer i2 = 40;
  
Integer i3 = 0;
  
Integer i4 = new Integer(40);
  
Integer i5 = new Integer(40);
  
Integer i6 = new Integer(0);

System.out.println("i1=i2 " + (i1 == i2));
  
System.out.println("i1=i2+i3 " + (i1 == i2 + i3));
  
System.out.println("i1=i4 " + (i1 == i4));
  
System.out.println("i4=i5 " + (i4 == i5));
  
System.out.println("i4=i5+i6 " + (i4 == i5 + i6));
  
System.out.println("40=i5+i6 " + (40 == i5 + i6));
  
i1=i2 true
  
i1=i2+i3 true
  
i1=i4 false
  
i4=i5 false
  
i4=i5+i6 true
  
40=i5+i6 true
  
解释: 语句i4 == i5 + i6，因为+这个操作符不适用于Integer对象，首先i5和i6进行自动拆箱操作，进行数值相加，即i4 == 40。然后Integer对象无法与数值进行直接比较，所以i4自动拆箱转为int值40，最终这条语句转为40 == 40进行数值比较。
  
Java中的自动装箱与拆箱

三. String类和常量池

String对象创建方式

String str1 = "abcd";
    
String str2 = new String("abcd");
    
System.out.println(str1==str2);//false
  
这两种不同的创建方法是有差别的，第一种方式是在常量池中拿对象，第二种方式是直接在堆内存空间创建一个新的对象。
  
只要使用new方法，便需要创建新的对象。

连接表达式 +
  
 (1) 只有使用引号包含文本的方式创建的String对象之间使用"+"连接产生的新对象才会被加入字符串池中。
  
 (2) 对于所有包含new方式新建对象 (包括null) 的"+"连接表达式，它所产生的新对象都不会被加入字符串池中。

String str1 = "str";
  
String str2 = "ing";

String str3 = "str" + "ing";
  
String str4 = str1 + str2;
  
System.out.println(str3 == str4);//false

String str5 = "string";
  
System.out.println(str3 == str5);//true
  
java基础: 字符串的拼接

特例1
  
public static final String A = "ab"; // 常量A
  
public static final String B = "cd"; // 常量B
  
public static void main(String[] args) {
  
String s = A + B; // 将两个常量用+连接对s进行初始化
  
String t = "abcd";
  
if (s == t) {
      
System.out.println("s等于t，它们是同一个对象");
  
} else {
      
System.out.println("s不等于t，它们不是同一个对象");
  
}
  
}
  
s等于t，它们是同一个对象
  
A和B都是常量，值是固定的，因此s的值也是固定的，它在类被编译时就已经确定了。也就是说: String s=A+B; 等同于: String s="ab"+"cd";
  
特例2
  
public static final String A; // 常量A
  
public static final String B; // 常量B
  
static {
  
A = "ab";
  
B = "cd";
  
}
  
public static void main(String[] args) {
  
// 将两个常量用+连接对s进行初始化
  
String s = A + B;
  
String t = "abcd";
  
if (s == t) {
      
System.out.println("s等于t，它们是同一个对象");
  
} else {
      
System.out.println("s不等于t，它们不是同一个对象");
  
}
  
}
  
s不等于t，它们不是同一个对象
  
A和B虽然被定义为常量，但是它们都没有马上被赋值。在运算出s的值之前，他们何时被赋值，以及被赋予什么样的值，都是个变数。因此A和B在被赋值之前，性质类似于一个变量。那么s就不能在编译期被确定，而只能在运行时被创建了。
  
String s1 = new String("xyz"); 创建了几个对象？
  
考虑类加载阶段和实际执行时。
  
 (1) 类加载对一个类只会进行一次。"xyz"在类加载时就已经创建并驻留了 (如果该类被加载之前已经有"xyz"字符串被驻留过则不需要重复创建用于驻留的"xyz"实例) 。驻留的字符串是放在全局共享的字符串常量池中的。
  
 (2) 在这段代码后续被运行的时候，"xyz"字面量对应的String实例已经固定了，不会再被重复创建。所以这段代码将常量池中的对象复制一份放到heap中，并且把heap中的这个对象的引用交给s1 持有。
  
这条语句创建了2个对象。

java.lang.String.intern()
  
运行时常量池相对于CLass文件常量池的另外一个重要特征是具备动态性，Java语言并不要求常量一定只有编译期才能产生，也就是并非预置入CLass文件中常量池的内容才能进入方法区运行时常量池，运行期间也可能将新的常量放入池中，这种特性被开发人员利用比较多的就是String类的intern()方法。
  
String的intern()方法会查找在常量池中是否存在一份equal相等的字符串,如果有则返回该字符串的引用,如果没有则添加自己的字符串进入常量池。

public static void main(String[] args) {
     
String s1 = new String("计算机");
     
String s2 = s1.intern();
     
String s3 = "计算机";
     
System.out.println("s1 == s2? " + (s1 == s2));
     
System.out.println("s3 == s2? " + (s3 == s2));
  
}
  
s1 == s2? false
  
s3 == s2? true
  
字符串比较更丰富的一个例子
  
public class Test {
  
public static void main(String[] args) {
     
String hello = "Hello", lo = "lo";
     
System.out.println((hello == "Hello") + " ");
     
System.out.println((Other.hello == hello) + " ");
     
System.out.println((other.Other.hello == hello) + " ");
     
System.out.println((hello == ("Hel"+"lo")) + " ");
     
System.out.println((hello == ("Hel"+lo)) + " ");
     
System.out.println(hello == ("Hel"+lo).intern());
  
}
  
}
  
class Other { static String hello = "Hello"; }
  
package other;
  
public class Other { public static String hello = "Hello"; }
  
true true true true false true
  
在同包同类下,引用自同一String对象.
  
在同包不同类下,引用自同一String对象.
  
在不同包不同类下,依然引用自同一String对象.
  
在编译成.class时能够识别为同一字符串的,自动优化成常量,引用自同一String对象.
  
在运行时创建的字符串具有独立的内存地址,所以不引用自同一String对象.

>https://segmentfault.com/a/1190000040922573#at?hmsr=toutiao.io&utm_campaign=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io
http://www.jianshu.com/p/c7f47de2ee80
  
https://tangxman.github.io/2015/07/27/the-difference-of-java-string-pool/

>https://cloud.tencent.com/developer/article/1450501
