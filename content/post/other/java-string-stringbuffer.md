---
title: JAVA String, StringBuffer, StringBuilder
author: "-"
date: 2012-09-20T03:27:09+00:00
url: java/string
categories:
  - Java
tags:
  - Java

---
## JAVA String, StringBuffer, StringBuilder

JAVA平台提供了两个类: String 和 StringBuffer，它们可以储存和操作字符串，即包含多个字符的字符数据。这个String类提供了数值不可改变的字符串。而StringBuffer类提供的字符串允许进行修改。当你知道字符数据要改变的时候你就可以使用 StringBuffer。典型地，你可以使用 StringBuffers 来动态构造字符数据。

在java中与字符串操作相关的类

Character 是进行单个字符操作的，

- String 字符串常量 对一串字符进行操作。不可变类。
- StringBuffer 也是对一串字符进行操作，但是可变类。字符串变量 (线程安全) 
- StringBuilder 字符串变量 (非线程安全) 

### String
  
String是对象不是原始类型, 为不可变对象,一旦被创建,就不能修改它的值,对于已经存在的String对象的修改都是重新创建一个新的对象,然后把新的值保存进去.

String 是final类,即不能被继承.

简要的说， String 类型和 StringBuffer 类型的主要性能区别其实在于 String 是不可变的对象, 因此在每次对 String 类型进行改变的时候其实都等同于生成了一个新的 String 对象，然后将指针指向新的 String 对象，所以经常改变内容的字符串最好不要用 String ，因为每次生成对象都会对系统性能产生影响，特别当内存中无引用对象多了以后， JVM 的 GC 就会开始工作，那速度是一定会相当慢的。

而如果是使用 StringBuffer 类则结果就不一样了，每次结果都会对 StringBuffer 对象本身进行操作，而不是生成新的对象，再改变对象引用。所以在一般情况下我们推荐使用 StringBuffer ，特别是字符串对象经常改变的情况下。而在某些特别情况下， String 对象的字符串拼接其实是被 JVM 解释成了 StringBuffer 对象的拼接，所以这些时候 String 对象的速度并不会比 StringBuffer 对象慢，而特别是以下的字符串对象生成中， String 效率是远要比 StringBuffer 快的: 
String S1 = "This is only a" + " simple" + " test";
StringBuffer Sb = new StringBuilder("This is only a").append(" simple").append(" test");
你会很惊讶的发现，生成 String S1 对象的速度简直太快了，而这个时候 StringBuffer 居然速度上根本一点都不占优势。其实这是 JVM 的一个把戏，在 JVM 眼里，这个
String S1 = "This is only a" + " simple" + "test"; 其实就是: 
String S1 = "This is only a simple test"; 所以当然不需要太多的时间了。但大家这里要注意的是，如果你的字符串是来自另外的 String 对象的话，速度就没那么快了，譬如: 
String S2 = "This is only a";
String S3 = " simple";
String S4 = " test";
String S1 = S2 +S3 + S4;
这时候 JVM 会规规矩矩的按照原来的方式去做


在大部分情况下 StringBuffer > String
### StringBuffer
SringBuffer的append方法，为了实现同步，很多方法使用lSynchronized修饰

Java.lang.StringBuffer线程安全的可变字符序列。一个类似于 String 的字符串缓冲区，但不能修改。虽然在任意时间点上它都包含某种特定的字符序列，但通过某些方法调用可以改变该序列的长度和内容。

可将字符串缓冲区安全地用于多个线程。可以在必要时对这些方法进行同步，因此任意特定实例上的所有操作就好像是以串行顺序发生的，该顺序与所涉及的每个线程进行的方法调用顺序一致。
StringBuffer 上的主要操作是 append 和 insert 方法，可重载这些方法，以接受任意类型的数据。每个方法都能有效地将给定的数据转换成字符串，然后将该字符串的字符追加或插入到字符串缓冲区中。append 方法始终将这些字符添加到缓冲区的末端；而 insert 方法则在指定的点添加字符。
例如，如果 z 引用一个当前内容是"start"的字符串缓冲区对象，则此方法调用 z.append("le") 会使字符串缓冲区包含"startle"，而 z.insert(4, "le") 将更改字符串缓冲区，使之包含"starlet"。
在大部分情况下 StringBuilder > StringBuffer


  java.lang.StringBuilde
 java.lang.StringBuilder一个可变的字符序列是5.0新增的。此类提供一个与 StringBuffer 兼容的 API，但不保证同步。该类被设计用作 StringBuffer 的一个简易替换，用在字符串缓冲区被单个线程使用的时候 (这种情况很普遍) 。如果可能，建议优先采用该类，因为在大多数实现中，它比 StringBuffer 要快。两者的方法基本相同。

    StringBuffer:
 是一个可变对象,当对他进行修改的时候不会像String那样重新建立对象它只能通过构造函数来建立,
 StringBuffer sb = new StringBuffer();
 note:不能通过赋值符号对他进行赋值.
 sb = "welcome to here!";//error
 对象被建立以后,在内存中就会分配内存空间,并初始保存一个null.向StringBuffer中付值的时候可以通过它的append方法.
 sb.append("hello");
  
  
    字符串连接操作中StringBuffer的效率要比String高:
  
  
    String str = new String("welcome to ");
 str += "here";
 的处理步骤实际上是通过建立一个StringBuffer,然后调用append(),最后再将StringBuffer toSting();
 这样的话String的连接操作就比StringBuffer多出了一些附加操作,当然效率上要打折扣.
  
  
    并且由于String 对象是不可变对象,每次操作Sting 都会重新建立新的对象来保存新的值.
 这样原来的对象就没用了,就要被垃圾回收.这也是要影响性能的.
  
  
    看看以下代码: 
 将26个英文字母重复加了5000次，
  
  
  
  
```java
 String tempstr = "abcdefghijklmnopqrstuvwxyz";
 int times = 5000;
 long lstart1 = System.currentTimeMillis();
 String str = "";
 for (int i = 0; i < times; i++) {
 str += tempstr;
 }
 long lend1 = System.currentTimeMillis();
 long time = (lend1 - lstart1);
 System.out.println("time="+time);
```
  
  
    可惜我的计算机不是超级计算机，得到的结果每次不一定一样一般为 46687左右。
 也就是46秒。
 我们再看看以下代码
  
  
    ```java
 String tempstr = "abcdefghijklmnopqrstuvwxyz";
 int times = 5000;
 long lstart2 = System.currentTimeMillis();
 StringBuffer sb = new StringBuffer();
 for (int i = 0; i < times; i++) {
 sb.append(tempstr);
 }
 long lend2 = System.currentTimeMillis();
 long time2 = (lend2 - lstart2);
 System.out.println("time=" + time2);
  
  
    ```
  
  
    得到的结果为 16 有时还是 0
 所以结论很明显，StringBuffer 的速度几乎是String 上万倍。当然这个数据不是很准确。因为循环的次数在100000次的时候，差异更大。不信你试试。
  
  
  
  
    根据上面所说: 
  
  
    str += "here";
 的处理步骤实际上是通过建立一个StringBuffer,让侯调用append(),最后
 再将StringBuffer toSting();
  
  
    所以str += "here";可以等同于
  
  
    StringBuffer sb = new StringBuffer(str);
  
  
    sb.append("here");
  
  
    str = sb.toString();
  
  
    所以上面直接利用"+"来连接String的代码可以基本等同于以下代码
  
  
    ```java
 String tempstr = "abcdefghijklmnopqrstuvwxyz";
 int times = 5000;
 long lstart2 = System.currentTimeMillis();
 String str = "";
 for (int i = 0; i < times; i++) {
 StringBuffer sb = new StringBuffer(str);
 sb.append(tempstr);
 str = sb.toString();
 }
 long lend2 = System.currentTimeMillis();
 long time2 = (lend2 - lstart2);
 System.out.println("time=" + time2);
 ```
  
  
    平均执行时间为46922左右，也就是46秒。
  
  
  
  
    总结: 如果在程序中需要对字符串进行频繁的修改连接操作的话.使用StringBuffer性能会更高
  
  
  
  
    http://blog.csdn.net/yirentianran/article/details/2871417
  
  
    http://blog.csdn.net/rmn190/article/details/1492013
  
