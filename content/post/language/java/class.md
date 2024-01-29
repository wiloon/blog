---
title: Class 文件内容, 方法区, 常量池
author: "-"
date: 2012-04-15T13:05:03+00:00
url: class
categories:
  - Java
tags:
  - reprint
---
## Class 文件内容, 方法区, 常量池

当JVM运行Java程序的时候，它会加载对应的 class文件，并提取class文件中的信息存放在JVM开辟出来的方法区内存中。那么这个 class 文件里面到底有些什么内容呢？

一、class文件内容概述

class文件是由8bits的字节流组成，全部字节构成了15个有意义的项目。这些项目之间没有任何无意义的字节，因此class文件非常紧凑。占据多字节空间的项目按照高位在前的顺序存放。下面我们详细讨论这些项目:

### magic (魔数)

每个class文件的前4个字节称为魔数，值为 0xCAFEBABE。作用在于轻松的辨别class文件与非class文件。

### minor_version、major_version(次、主版本号)

各占2个字节。随着Java技术的发展，class文件的格式会发生变化。版本号的作用在于使得虚拟机能够认识当前加载class的文件格式。从而准确的提取class文件信息。

### constant_pool_count 、constance_pool  (常量池)

从这里开始的字节组成了常量池 。 存储了诸如符号常量、final常量值、基本数据类型的字面值等内容。JVM会将每一个常量构成一个常量表，每个常量表都有自己的入口地址。而实际上在JVM会将这些常量表存储在方法区中一块连续的内存空间中，因此class文件会根据常量表在常量池中的位置对其进行索引。比如常量池中的第一个常量表的索引值就是1，第二个就是2。有的时候常量表A需要常量表B的内容，则在常量表A中会存储常量表B的索引值x。而 constant_pool_count 就记录了有多少个常量表，或者所有多少个索引值。实际上，常量池中没有索引值为0的常量表，但这缺失的索引值也被记录在constant_pool_count中，因此 constant_pool_count等于常量表的数量加1。关于常量池的具体内容，我们会在下面详细讲述，并用一个例子来显示整个class文件的内容。

### access_flags(访问标志)

占用2个字节。用来表明该class文件中定义的是类还是接口，访问修饰符是public还是缺省。类或接口是否是抽象的。类是否是final的。

### this_class

占用2个字节。 它是一个对常量池的索引。指向的是常量池中存储类名符号引用的CONSTANT_Class_info常量表(见下面常量池具体结构)。比如this_class=0x0001。则表示指向常量池中的第一个常量表。通常这个表是指向当前class文件所定义的类名。

### super_class

占用2个字节 与this_class类似，指向存放当前class文件所定义类的超类名字的索引的CONSTANT_Class_info常量表。

### inteface_count、interfaces interface_count

是class文件所定义的类直接实现的接口或父类实现的接口的数量。占2个字节。intefaces包含了对每个接口的 CONSTANT_Class_info常量表的索引。

### fields_count、fields fields_count

表明了类中字段的数量 。fields是不同长度的field_info表的序列。这些field_info表中并不包含超类或父接口继承而来的字段。field_info表展示了一个字段的信息，包括字段的名字，描述符和修饰符。如果该字段是final的，那么还会展示其常量值。注意，这些信息有些存放在field_info里面，有些则存放在field_info所指向的常量池中。下面我们阐述一下这个field_info表的格式:

access_flags(2byte 访问修饰符)

name_index(2byte 存储字段名的常量表在常量池中的索引)

description_index(2byte 存储字段的所属类型的常量表在常量池中的索引)

attribute_count(2byte 属性表的数量)

attribute (属性)

其中attribute是由多个attribute_info组成。而JVM规范定义了字段的三种属性: ConstanceValue、Deprecated和Synthetic。

### method_count、methods

与字段类似，method_count表明类中方法的数量和每个方法的常量表的索引。methods表明了不同长度的method_info表的序列。该表格式如下:

access_flags(2byte 访问修饰符)

name_index(2byte 存储方法名的常量表在常量池中的索引)

description_index(2byte 存储方法的返回类型和参数类型的常量表在常量池中的索引)

attribute_count(2byte 属性表的数量)

attribute (属性)

其中方法的属性JVM规定了四种: Code，Deprecated，Exceptions，Synthetic。

### 常量池的具体结构

在Java程序中，有很多的东西是永恒的，不会在运行过程中变化。比如一个类的名字，一个类字段的名字/所属类型，一个类方法的名字/返回类型/参数名与所属类型，一个常量，还有在程序中出现的大量的字面值。比如下面小段源码红色显示的东西。

public class ClassTest {

private String itemS ="我们 ";

private final int itemI =100 ;

public void setItemS (String para ){…}

}

而这些在JVM解释执行程序的时候是非常重要的。那么编译器将源程序编译成class文件后，会用一部分字节分类存储这些永恒不变的红色东西。而这些字节我们就成为常量池。事实上，只有JVM加载class后，在方法区中为它们开辟了空间才更像一个"池"。

正如上面所示，一个程序中有很多永恒的红色东西。每一个都是常量池中的一个常量表(常量项)。而这些常量表之间又有不同，class文件共有11种常量表，如下所示:

常量表类型 标志值(占1 byte) 描述
  
CONSTANT_Utf8 1 UTF-8编码的Unicode字符串
  
CONSTANT_Integer 3 int类型的字面值
  
CONSTANT_Float 4 float类型的字面值
  
CONSTANT_Long 5 long类型的字面值
  
CONSTANT_Double 6 double类型的字面值
  
CONSTANT_Class 7 对一个类或接口的符号引用
  
CONSTANT_String 8 String类型字面值的引用
  
CONSTANT_Fieldref 9 对一个字段的符号引用
  
CONSTANT_Methodref 10 对一个类中方法的符号引用
  
CONSTANT_InterfaceMethodref 11 对一个接口中方法的符号引用
  
CONSTANT_NameAndType 12 对一个字段或方法的部分符号引用
  
(1) CONSTANT_Utf8 用UTF-8编码方式来表示程序中所有的重要常量字符串。这些字符串包括:  ①类或接口的全限定名， ②超类的全限定名，③父接口的全限定名， ④类字段名和所属类型名，⑤类方法名和返回类型名、以及参数名和所属类型名。⑥字符串字面值

表格式:  tag(标志1: 占1byte) length(字符串所占字节的长度，占2byte) bytes(字符串字节序列)

(2) CONSTANT_Integer、 CONSTANT_Float、 CONSTANT_Long、 CONSTANT_Double 所有基本数据类型的字面值。比如在程序中出现的1用CONSTANT_Integer表示。3.1415926F用 CONSTANT_Float表示。

表格式:  tag bytes(基本数据类型所需使用的字节序列)

(3) CONSTANT_Class 使用符号引用来表示类或接口。我们知道所有类名都以 CONSTANT_Utf8表的形式存储。但是我们并不知道 CONSTANT_Utf8表中哪些字符串是类名，那些是方法名。因此我们必须用一个指向类名字符串的符号引用常量来表明。

表格式:  tag name_index(给出表示类或接口名的CONSTANT_Utf8表的索引)

(4) CONSTANT_String 同 CONSTANT_Class，指向包含字符串字面值的 CONSTANT_Utf8表。

表格式:  tag string_index(给出表示字符串字面值的CONSTANT_Utf8表的索引)

(5) CONSTANT_Fieldref 、 CONSTANT_Methodref、 CONSTANT_InterfaceMethodref 指向包含该字段或方法所属类名的 CONSTANT_Utf8表，以及指向包含该字段或方法的名字和描述符的 CONSTANT_NameAndType表

表格式:  tag class _index(给出包含所属类名的CONSTANT_Utf8表的索引) name_and_type_index(包含字段名或方法名以及描述符的 CONSTANT_NameAndType表 的索引)

(6) CONSTANT_NameAndType 指向包含字段名或方法名以及描述符的 CONSTANT_Utf8表。

表格式:  tag name_index(给出表示字段名或方法名的CONSTANT_Utf8表的索引) type_index(给出表示描述符的CONSTANT_Utf8表的索引)

下面是我将一个源程序编译成class文件后，对文件中的每一个字节的分析，可以更好的理解class文件的内容以及常量池的组成。

三、TestClass.class 文件实例分析

Java代码 收藏代码
  
//源代码
  
package hr.test;
  
//ClassTest类
  
public class ClassTest {

private int itemI=0; //itemI类字段

private static String itemS="我们"; //itemS类字段

private final float PI=3.1415926F; //PI类字段

//构造器方法

public ClassTest(){

}

//getItemI方法

public int getItemI(){

return this.itemI;

}

//getItemS方法

public static String getItemS(){

return itemS;

}

//main主方法

public static void main(String[] args) {

ClassTest ct=new ClassTest();

}
  
}

TestClass.class 字节码分析(字节顺序从上到下，从左到右。每个字节用一个0-255的十进制整数表示)

202 254 186 190 — 魔数
  
0 0 — 次版本号
  
0 50 — 主版本号

0 43 — 常量池中常量表的数量有42个，下面红色括号中的数据表明该常量表所在常量池中的索引，从索引1开始

(1) 7 0 2 — 对类ClassTest的符号引用(7为标志 02指向了常量池的索引2的位置)

(2) 1 0 17 104 114 47 116 101 115 116 47 67 108 97 115 115 84 101 115 116 — 类全限定名hrtestClassTest
  
(3) 7 0 4 — 对类Object的符号引用

(4) 1 0 16 106 97 118 97 47 108 97 110 103 47 79 98 106 101 99 116 — 超类全限定名 java/lang/Object
  
(5) 1 0 5 105 116 101 109 73 — 第1个类字段名 itemI
  
(6) 1 0 1 73 — I 第1个类字段类型为整型
  
(7) 1 0 5 105 116 101 109 83 — 第2个类字段名 itemS
  
(8) 1 0 18 76 106 97 118 97 47 108 97 110 103 47 83 116 114 105 110 103 59 — 第2个类字段类型的全限定名 Ljava/lang/String
  
(9) 1 0 2 80 73 — 第3个类字段名PI
  
(10) 1 0 1 70 — 第3个类字段类型为float
  
(11) 1 0 13 67 111 110 115 116 97 110 116 86 97 108 117 101 — 第3个类字段为常量ConstantValue

(12) 4 64 73 15 218 — 第3个类字段float字面值,占4bytes(3.1415926)
  
(13) 1 0 8 60 99 108 105 110 105 116 62 — <clinit> 初始化方法名
  
(14) 1 0 3 40 41 86 — ()V 方法的返回类型为void

(15) 1 0 4 67 111 100 101 — Code
  
(16) 8 0 17 — String字符串字面值 (0 17表示索引1 7)
  
(17) 1 0 6 230 136 145 228 187 172 — "我们"
  
(18) 9 0 1 0 19 — 指向 第2个 字段的引用(0 1指向索引1，0 19指向索引19)
  
(19) 12 0 7 0 8 –指向 第2个 字段的名字和描述符的索引，
  
(20) 1 0 15 76 105 110 101 78 117 109 98 101 114 84 97 98 108 101 — LineNumberTable
  
(21) 0 18 76 111 99 97 108 86 97 114 105 97 98 108 101 84 97 98 108 101 — LocalVariableTable
  
(22) 1 0 6 60 105 110 105 116 62 — <init> 表示初始化方法名
  
(23) 10 0 3 0 24 — 指向父类Object的构造器方法，0 3表示父类名常量表的索引，0 24表示存放该方法名称和描述符的引用的常量表的索引
  
(24) 12 0 22 0 14 — 指向方法名和描述符的常量表的索引。0 22是方法名的常量表索引，0 14是描述符的常量表索引
  
(25) 9 0 1 0 26 — 指向第1个字段的引用， 0 1表示字段所属类型的索引，0 26表示字段名和描述符的索引
  
(26) 12 0 5 0 6 — 指向第1个字段的名字和描述符的索引
  
(27) 9 0 1 0 28 — 指向第3个字段的引用， 0 1表示字段所属类型的索引，0 28表示字段名和描述符的索引
  
(28) 12 0 9 0 10 — 指向第3个字段的名字和描述符的索引
  
(29) 1 0 4 116 104 105 115 — 隐含参数符号this
  
(30) 1 0 11 76 67 108 97 115 115 84 101 115 116 59 — LClassTest;
  
(31) 1 0 8 103 101 116 73 116 101 109 73 – – 方法名 getItemI
  
(32) 1 0 3 40 41 73 — ()I 方法描述符:返回类型int
  
(33) 1 0 8 103 101 116 73 116 101 109 83 — 方法名 getItemS
  
(34) 1 0 20 40 41 76 106 97 118 97 47 108 97 110 103 47 83 116 114 105 110 103 59 — 方法描述符()Ljava/lang/String;
  
(35) 1 0 4 109 97 105 110 — 主方法名main
  
(36) 1 0 22 40 91 76 106 97 118 97 47 108 97 110 103 47 83 116 114 105 110 103 59 41 86 — ()Ljava/lang/String;)V 主方法中的参数的字符串数组类型名
  
(37) 10 0 1 0 24 指向当前 ClassTest 类的构造器方法，0 1表示存放当前类名的常量表的索引。0 24是存放方法名和描述符的符号引用的常量表索引。
  
(38) 1 0 4 97 114 103 115 — 参数args
  
(39) 1 0 19 91 76 106 97 118 97 47 108 97 110 103 47 83 116 114 105 110 103 59 — 字符串数组 [Ljava/lang/String;
  
(40) 1 0 2 99 116 — 对象符号ct
  
(41) 1 0 10 83 111 117 114 99 101 70 105 108 101 — SourceFile
  
(42) 1 0 14 67 108 97 115 115 84 101 115 116 46 106 97 118 97 — ClassTest.java

       0 33 —- access_flag 访问标志  public
       0 1   —- this_class  指向当前类的符号引用在常量池中的索引
       0 3  —- super_class
       0 0 —- inteface_count接口的数量
    
       0 3   —  field_count字段的数量

// 字段 itemI

0 2 —- private 修饰符

0 5 —- 字段名在常量池中的索引，字段itemI

0 6 —- 字段的描述符(所属类型)在常量池中的索引

0 0 — 字段的属性信息表(attribute_info)的数量
  
// 字段 itemS

0 10 —- private static 修饰符

0 7 —字段名在常量池中的索引，字段itemS

0 8 —字段的描述符(所属类型)在常量池中的索引

0 0 — 字段的属性信息表(attribute_info)的数量
  
// 字段 PI

0 18 — private final 修饰符

0 9 —字段名在常量池中的索引，//字段PI

0 10 —字段的描述符(所属类型)在常量池中的索引

0 1 — 字段的属性信息表(attribute_info)的数量

0 11 — 属性名在常量池中的索引。即ConstantValue

0 0 0 2 — 属性所占的字节长度

0 12 — 属性值在常量池中的索引。即常量字面值

       0 5  — Method_count方法的数量
       //类的静态数据初始化方法<clinit>
       0 8 —- static 修饰符(所有的初始化方法都是static的)
       0 13 — 在常量池中的索引。初始化方法名<clinit>，该方法直接由JVM在特定的时候调用，并非由字节码生成。
       0 14 — 在常量池中的索引。返回类型为void。
    
       0 1 — 属性数量
       0 15 — 属性名 在常量池中的索引。即code
       0 0 0 42 —  属性所占的字节长度2
       0 1 0 0 0 0 0 6 18 16 179 0 18 177 0 0 0 2 0 20 0 0 0 10 0 2 0 0 0 5 0 5 0 2 0 21 0 0 0 2 0 0 —该方法的字节码指令序列和其他信息
       //类的普通实例数据的初始化方法，针对类构造器生成的<init>方法。
       0 1 — public 修饰符
       0 22 — 构初始化方法名<init>
       0 14 — 构造器的返回类型为void
       0 1  — 属性数量
       0 15 —  属性名在常量池中的索引。即Code
       0 0 0 70 — 属性所占的字节长度70
       0 2 0 1 0 0 0 16 42 183 0 23 42 3 181 0 25 42 18 12 181 0 27 177 0 0 0 2 0 200 0 0 18 0 4 0 0 0 8 0 4 0 4 0 9 0 6 0 15 0 9 0 21 0 0 0 12 0 10 0 0 16 0 29 0 30 0 0 —该方法的字节码指令序列和其他信息
       //getItemI方法
       0 1 — public 修饰符
       0 31 —  在常量池中的索引。方法名getItemI
       0 32 —  在常量池中的索引。方法返回类型为int
       0 1 — 属性数量
       0 15  — 属性名在常量池中的索引。即Code
       0 0 0 47 —  属性所占的字节长度70
       0 1 0 1 0 0 0 5 42 180 0 25 172 0 0 0 2 0 20 0 0 0 6 0 1 0 0 0 12 0 21 0 0 0 12 0 1 0 0 0 5 0 29 0 30 0 0  — 该方法的字节码指令序列和其他信息
       //getItemS方法
       0 9 — public static 修饰符
       0 33 —  在常量池中的索引。方法名getItemS
       0 34 – — 在常量池中的索引。方法返回类型为String
       0 1 — 属性数量
       0 15 — 属性名在常量池中的索引。即Code
       0 0 0 36 —  属性所占的字节长度36
       0 1 0 0 0 0 0 4 178 0 18 176 0 0 0 2 0 20 0 0 0 6 0 1 0 0 0 16 0 21 0 0 0 2 0 0 –该方法的字节码指令序列和其他信息
       //main方法
       0 9 — public static 修饰符
       0 35 —  在常量池中的索引。主方法名main
       0 36 — 在常量池中的索引。方法返回类型为String[]
       0 1 —  属性数量
       0 15  —  属性名在常量池中的索引。即Code
       0 0 0  65 —  属性所占的字节长度36
       0 2 0 2 0 0 0 9 187 0 1 89 183 0 37 76 177 0 0 0 2 0 20 0 0 0 10 0 2 0 0 0 20 0 8 0 21 0 21 0 0 0 22 0 2 0 0 0 9 0 38 0 39 0 0 0 8 0 1 0 40 0 30 0 1 0 1 0 41 0 0 0 2 0 42

我们分析上面的字节码例子，不难看出:

蓝色背景的常量池字节码区域:

(1) 所有的字面值都是存放在常量池中的。 特别注意的是"我们"这个字符串常量也是在常量池中的。如果一个程序出现多个"我们"，那么常量池中也只会有一个。另外，也正是因为"我们"存放在常量池中，使得一些字符串的==比较变的需要琢磨了。

(2)ClassTest并没有任何显示的父类。但在常量池中，我们发现有Object的符号常量存在。 这也证实了在Java中，任何类都直接或间接继承了Object的，而Object并不需要在代码中显示继承，JVM会帮我们做到这一点。

(3)常量池中有一个隐含参数this的符号常量。即使程序中不存在this，JVM也会悄悄的设置一个这样的对象。

绿色背景的类字段字节码区域:

(1)字段PI是浮点型常量，在编译期的字节码中就已经指定好了PI的字面值存储在常量池中的某个索引内 。这一点也证实了Java中的常量在编译期就已经得到了值，在运行过程中是无法改变的。

橙色背景的类方法字节码区域:

(1)主方法main是作为ClassTest的类方法存在的，在字节码中main和其他的类方法并没有什么区别。 实际上，我们也确实可以通过ClassTest.main(..)来调用ClassTest中的main方法。

(2)在class文件常量池字节码中有两个比较特别的方法名符号: <clinit>和<init>。其中<clinit>方法是编译器自己生成的，编译器会把类静态变量的直接初始化语句和静态初始化语句块的代码都放到了class文件的<clinit>方法中。而对所有非静态非常量数据域的初始化工作要靠<init>方法来完成。针对每一个类的构造方法，编译器都会产生一个<init>方法。即使是缺省构造器也不例外。
