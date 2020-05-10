---
title: JAVA String, StringBuffer, StringBuilder
author: wiloon
type: post
date: 2012-09-20T03:27:09+00:00
url: /?p=4123
categories:
  - Java
tags:
  - Java

---
在java中与字符串操作相关的类

Character 是进行单个字符操作的，

**String 字符串常量** 对一串字符进行操作。不可变类。

StringBuffer 也是对一串字符进行操作，但是可变类。**字符串变量（线程安全）**

**StringBuilder 字符串变量（非线程安全）**

&nbsp;

String:
  
是对象不是原始类型.
  
为不可变对象,一旦被创建,就不能修改它的值.
  
对于已经存在的String对象的修改都是重新创建一个新的对象,然后把新的值保存进去.
  
String 是final类,即不能被继承.

&nbsp;

<div>
  <span style="font-size: large;">简要的说， String 类型和 StringBuffer 类型的主要性能区别其实在于 String 是不可变的对象, 因此在每次对 String 类型进行改变的时候其实都等同于生成了一个新的 String 对象，然后将指针指向新的 String 对象，所以经常改变内容的字符串最好不要用 String ，因为每次生成对象都会对系统性能产生影响，特别当内存中无引用对象多了以后， JVM 的 GC 就会开始工作，那速度是一定会相当慢的。<br /> 而如果是使用 StringBuffer 类则结果就不一样了，每次结果都会对 StringBuffer 对象本身进行操作，而不是生成新的对象，再改变对象引用。所以在一般情况下我们推荐使用 StringBuffer ，特别是字符串对象经常改变的情况下。而在某些特别情况下， String 对象的字符串拼接其实是被 JVM 解释成了 StringBuffer 对象的拼接，所以这些时候 String 对象的速度并不会比 StringBuffer 对象慢，而特别是以下的字符串对象生成中， String 效率是远要比 StringBuffer 快的：<br /> String S1 = “This is only a” + “ simple” + “ test”;<br /> StringBuffer Sb = new StringBuilder(“This is only a”).append(“ simple”).append(“ test”);<br /> 你会很惊讶的发现，生成 String S1 对象的速度简直太快了，而这个时候 StringBuffer 居然速度上根本一点都不占优势。其实这是 JVM 的一个把戏，在 JVM 眼里，这个<br /> String S1 = “This is only a” + “ simple” + “test”; 其实就是：<br /> String S1 = “This is only a simple test”; 所以当然不需要太多的时间了。但大家这里要注意的是，如果你的字符串是来自另外的 String 对象的话，速度就没那么快了，譬如：<br /> String S2 = “This is only a”;<br /> String S3 = “ simple”;<br /> String S4 = “ test”;<br /> String S1 = S2 +S3 + S4;<br /> 这时候 JVM 会规规矩矩的按照原来的方式去做</span>
</div>

<div>
  <span style="font-size: large;"><span style="color: #ff0000;">在大部分情况下 StringBuffer > String</span><br /> <strong>StringBuffer</strong><br /> Java.lang.StringBuffer线程安全的可变字符序列。一个类似于 String 的字符串缓冲区，但不能修改。虽然在任意时间点上它都包含某种特定的字符序列，但通过某些方法调用可以改变该序列的长度和内容。<br /> 可将字符串缓冲区安全地用于多个线程。可以在必要时对这些方法进行同步，因此任意特定实例上的所有操作就好像是以串行顺序发生的，该顺序与所涉及的每个线程进行的方法调用顺序一致。<br /> StringBuffer 上的主要操作是 append 和 insert 方法，可重载这些方法，以接受任意类型的数据。每个方法都能有效地将给定的数据转换成字符串，然后将该字符串的字符追加或插入到字符串缓冲区中。append 方法始终将这些字符添加到缓冲区的末端；而 insert 方法则在指定的点添加字符。<br /> 例如，如果 z 引用一个当前内容是“start”的字符串缓冲区对象，则此方法调用 z.append(&#8220;le&#8221;) 会使字符串缓冲区包含“startle”，而 z.insert(4, &#8220;le&#8221;) 将更改字符串缓冲区，使之包含“starlet”。<br /> <span style="color: #ff0000;">在大部分情况下 StringBuilder > StringBuffer</span></span>
</div>

<div>
  <span style="font-size: large;"><strong>java.lang.StringBuilde</strong><br /> java.lang.StringBuilder一个可变的字符序列是5.0新增的。此类提供一个与 StringBuffer 兼容的 API，但不保证同步。该类被设计用作 StringBuffer 的一个简易替换，用在字符串缓冲区被单个线程使用的时候（这种情况很普遍）。如果可能，建议优先采用该类，因为在大多数实现中，它比 StringBuffer 要快。两者的方法基本相同。</span>
</div>

<div>
</div>

<div id="article_content">
  <p>
    &nbsp;
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    StringBuffer:<br /> 是一个可变对象,当对他进行修改的时候不会像String那样重新建立对象它只能通过构造函数来建立,<br /> StringBuffer sb = new StringBuffer();<br /> note:不能通过赋值符号对他进行赋值.<br /> sb = &#8220;welcome to here!&#8221;;//error<br /> 对象被建立以后,在内存中就会分配内存空间,并初始保存一个null.向StringBuffer中付值的时候可以通过它的append方法.<br /> sb.append(&#8220;hello&#8221;);
  </p>
  
  <p>
    字符串连接操作中StringBuffer的效率要比String高:
  </p>
  
  <p>
    String str = new String(&#8220;welcome to &#8220;);<br /> str += &#8220;here&#8221;;<br /> 的处理步骤实际上是通过建立一个StringBuffer,然后调用append(),最后再将StringBuffer toSting();<br /> 这样的话String的连接操作就比StringBuffer多出了一些附加操作,当然效率上要打折扣.
  </p>
  
  <p>
    并且由于String 对象是不可变对象,每次操作Sting 都会重新建立新的对象来保存新的值.<br /> 这样原来的对象就没用了,就要被垃圾回收.这也是要影响性能的.
  </p>
  
  <p>
    看看以下代码：<br /> 将26个英文字母重复加了5000次，
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    [java]<br /> String tempstr = "abcdefghijklmnopqrstuvwxyz";<br /> int times = 5000;<br /> long lstart1 = System.currentTimeMillis();<br /> String str = "";<br /> for (int i = 0; i < times; i++) {<br /> str += tempstr;<br /> }<br /> long lend1 = System.currentTimeMillis();<br /> long time = (lend1 &#8211; lstart1);<br /> System.out.println("time="+time);
  </p>
  
  <p>
    [/java]
  </p>
  
  <p>
    可惜我的计算机不是超级计算机，得到的结果每次不一定一样一般为 46687左右。<br /> 也就是46秒。<br /> 我们再看看以下代码
  </p>
  
  <p>
    [java]
  </p>
  
  <p>
    String tempstr = "abcdefghijklmnopqrstuvwxyz";<br /> int times = 5000;<br /> long lstart2 = System.currentTimeMillis();<br /> StringBuffer sb = new StringBuffer();<br /> for (int i = 0; i < times; i++) {<br /> sb.append(tempstr);<br /> }<br /> long lend2 = System.currentTimeMillis();<br /> long time2 = (lend2 &#8211; lstart2);<br /> System.out.println("time=" + time2);
  </p>
  
  <p>
    [/java]
  </p>
  
  <p>
    得到的结果为 16 有时还是 0<br /> 所以结论很明显，StringBuffer 的速度几乎是String 上万倍。当然这个数据不是很准确。因为循环的次数在100000次的时候，差异更大。不信你试试。
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    根据上面所说：
  </p>
  
  <p>
    str += &#8220;here&#8221;;<br /> 的处理步骤实际上是通过建立一个StringBuffer,让侯调用append(),最后<br /> 再将StringBuffer toSting();
  </p>
  
  <p>
    所以str += &#8220;here&#8221;;可以等同于
  </p>
  
  <p>
    StringBuffer sb = new StringBuffer(str);
  </p>
  
  <p>
    sb.append(&#8220;here&#8221;);
  </p>
  
  <p>
    str = sb.toString();
  </p>
  
  <p>
    所以上面直接利用&#8221;+&#8221;来连接String的代码可以基本等同于以下代码
  </p>
  
  <p>
    [java]<br /> <pre>String tempstr = "abcdefghijklmnopqrstuvwxyz";<br /> int times = 5000;<br /> long lstart2 = System.currentTimeMillis();<br /> String str = "";<br /> for (int i = 0; i < times; i++) {<br /> StringBuffer sb = new StringBuffer(str);<br /> sb.append(tempstr);<br /> str = sb.toString();<br /> }<br /> long lend2 = System.currentTimeMillis();<br /> long time2 = (lend2 &#8211; lstart2);<br /> System.out.println("time=" + time2);</pre><br /> [/java]
  </p>
  
  <p>
    平均执行时间为46922左右，也就是46秒。
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    总结: 如果在程序中需要对字符串进行频繁的修改连接操作的话.使用StringBuffer性能会更高
  </p>
  
  <p>
    &nbsp;
  </p>
  
  <p>
    http://blog.csdn.net/yirentianran/article/details/2871417
  </p>
  
  <p>
    http://blog.csdn.net/rmn190/article/details/1492013
  </p>
</div>