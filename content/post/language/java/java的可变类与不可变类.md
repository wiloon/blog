---
title: JAVA的可变类与不可变类
author: "-"
date: 2015-06-26T02:26:25+00:00
url: /?p=7847
categories:
  - Inbox
tags:
  - Java

---
## JAVA的可变类与不可变类
可变类和不变类(Mutable and immutable class)的初步定义: 

可变类: 当你获得这个类的一个实例引用时，你可以改变这个实例的内容。
  
不变类: 当你获得这个类的一个实例引用时，你不可以改变这个实例的内容。不可变类的实例一但创建，其内在成员变量的值就不能被修改。
  
如何创建一个自己的不可变类: 
  
.所有成员都是private
  
.不提供对成员的改变方法，例如: setXXXX
  
.确保所有的方法不会被重载。手段有两种: 使用final Class(强不可变类)，或者将所有类方法加上final(弱不可变类)。
  
.如果某一个类成员不是原始变量(primitive)或者不可变类，必须通过在成员初始化(in)或者get方法(out)时通过深度clone方法，来确保类的不可变。
  
一个示例
  
import java.util.Date;
  
public final class BrokenPerson
  
{
  
private String firstName;
  
private String lastName;
  
private Date dob;

public BrokenPerson( String firstName,                   public BetterPerson( String firstName,
  
String lastName, Date dob)                                             String lastName, Date dob)
  
{                                                                                      {
  
this.firstName = firstName;                                             this.firstName = firstName;
  
this.lastName = lastName;                                             this.lastName = lastName;
  
this.dob = dob;     //error               this.dob = new Date( dob.getTime() ); //correct
  
}                                                                                       }

public String getFirstName()
  
{
  
return this.firstName;
  
}
  
public String getLastName()
  
{
  
return this.lastName;
  
}
  
public Date getDOB()                                               public Date getDOB()
  
{                                                                                    {
  
return this.dob;    //error                  return new Date( this.dob.getTime() );//correct
  
}                                                                                     }
  
}
  
4. jdk的可变类和不可变类

primitive变量: boolean,byte, char, double ,float, integer, long, short
  
jdk的不可变类: jdk的java.lang包中 Boolean, Byte, Character, Double, Float, Integer, Long, Short, String.

StringBuffer 可变类
  
java.util.Date 可变类


对于这个系列里的问题，每个学Java的人都应该搞懂。当然，如果只是学Java玩玩就无所谓了。如果你认为自己已经超越初学者了，却不很懂这些问题，请将你自己重归初学者行列。内容均来自于CSDN的经典老贴。

问题一: 我声明了什么！

String s = "Hello world!";

许多人都做过这样的事情，但是，我们到底声明了什么？回答通常是: 一个String，内容是"Hello world!"。这样模糊的回答通常是概念不清的根源。如果要准确的回答，一半的人大概会回答错误。
  
这个语句声明的是一个指向对象的引用，名为"s"，可以指向类型为String的任何对象，目前指向"Hello world!"这个String类型的对象。这就是真正发生的事情。我们并没有声明一个String对象，我们只是声明了一个只能指向String对象的引用变量。所以，如果在刚才那句语句后面，如果再运行一句: 

String string = s;

我们是声明了另外一个只能指向String对象的引用，名为string，并没有第二个对象产生，string还是指向原来那个对象，也就是，和s指向同一个对象。

问题二: "=="和equals方法究竟有什么区别？

==操作符专门用来比较变量的值是否相等。比较好理解的一点是: 
  
int a=10;
  
int b=10;
  
则a==b将是true。
  
但不好理解的地方是: 
  
String a=new String("foo");
  
String b=new String("foo");
  
则a==b将返回false。

根据前一帖说过，对象变量其实是一个引用，它们的值是指向对象所在的内存地址，而不是对象本身。a和b都使用了new操作符，意味着将在内存中产生两个内容为"foo"的字符串，既然是"两个"，它们自然位于不同的内存地址。a和b的值其实是两个不同的内存地址的值，所以使用"=="操作符，结果会是false。诚然，a和b所指的对象，它们的内容都是"foo"，应该是"相等"，但是==操作符并不涉及到对象内容的比较。
  
对象内容的比较，正是equals方法做的事。

看一下Object对象的equals方法是如何实现的: 
  
boolean equals(Object o){

return this==o;

}
  
Object对象默认使用了==操作符。所以如果你自创的类没有覆盖equals方法，那你的类使用equals和使用==会得到同样的结果。同样也可以看出，Object的equals方法没有达到equals方法应该达到的目标: 比较两个对象内容是否相等。因为答案应该由类的创建者决定，所以Object把这个任务留给了类的创建者。

看一下一个极端的类: 
  
Class Monster{
  
private String content;
  
...
  
boolean equals(Object another){ return true;}

}
  
我覆盖了equals方法。这个实现会导致无论Monster实例内容如何，它们之间的比较永远返回true。

所以当你是用equals方法判断对象的内容是否相等，请不要想当然。因为可能你认为相等，而这个类的作者不这样认为，而类的equals方法的实现是由他掌握的。如果你需要使用equals方法，或者使用任何基于散列码的集合 (HashSet,HashMap,HashTable) ，请察看一下java doc以确认这个类的equals逻辑是如何实现的。

问题三: String到底变了没有？

没有。因为String被设计成不可变(immutable)类，所以它的所有对象都是不可变对象。请看下列代码: 

String s = "Hello";
  
s = s + " world!";

s所指向的对象是否改变了呢？从本系列第一篇的结论很容易导出这个结论。我们来看看发生了什么事情。在这段代码中，s原先指向一个String对象，内容是"Hello"，然后我们对s进行了+操作，那么s所指向的那个对象是否发生了改变呢？答案是没有。这时，s不指向原来那个对象了，而指向了另一个String对象，内容为"Hello world!"，原来那个对象还存在于内存之中，只是s这个引用变量不再指向它了。
  
通过上面的说明，我们很容易导出另一个结论，如果经常对字符串进行各种各样的修改，或者说，不可预见的修改，那么使用String来代表字符串的话会引起很大的内存开销。因为String对象建立之后不能再改变，所以对于每一个不同的字符串，都需要一个String对象来表示。这时，应该考虑使用StringBuffer类，它允许修改，而不是每个不同的字符串都要生成一个新的对象。并且，这两种类的对象转换十分容易。
  
同时，我们还可以知道，如果要使用内容相同的字符串，不必每次都new一个String。例如我们要在构造器中对一个名叫s的String引用变量进行初始化，把它设置为初始值，应当这样做: 
  
public class Demo {
  
private String s;
  
...
  
public Demo {
  
s = "Initial Value";
  
}
  
...
  
}
  
而非
  
s = new String("Initial Value");
  
后者每次都会调用构造器，生成新对象，性能低下且内存开销大，并且没有意义，因为String对象不可改变，所以对于内容相同的字符串，只要一个String对象来表示就可以了。也就说，多次调用上面的构造器创建多个对象，他们的String类型属性s都指向同一个对象。
  
上面的结论还基于这样一个事实: 对于字符串常量，如果内容相同，Java认为它们代表同一个String对象。而用关键字new调用构造器，总是会创建一个新的对象，无论内容是否相同。
  
至于为什么要把String类设计成不可变类，是它的用途决定的。其实不只String，很多Java标准类库中的类都是不可变的。在开发一个系统的时候，我们有时候也需要设计不可变类，来传递一组相关的值，这也是面向对象思想的体现。不可变类有一些优点，比如因为它的对象是只读的，所以多线程并发访问也不会有任何问题。当然也有一些缺点，比如每个不同的状态都要一个对象来代表，可能会造成性能上的问题。所以Java标准类库还提供了一个可变版本，即StringBuffer。

问题四: final关键字到底修饰了什么？

final使得被修饰的变量"不变"，但是由于对象型变量的本质是"引用"，使得"不变"也有了两种含义: 引用本身的不变，和引用指向的对象不变。

引用本身的不变: 
  
final StringBuffer a=new StringBuffer("immutable");
  
final StringBuffer b=new StringBuffer("not immutable");
  
a=b;//编译期错误

引用指向的对象不变: 
  
final StringBuffer a=new StringBuffer("immutable");
  
a.append(" broken!"); //编译通过

可见，final只对引用的"值"(也即它所指向的那个对象的内存地址)有效，它迫使引用只能指向初始指向的那个对象，改变它的指向会导致编译期错误。至于它所指向的对象的变化，final是不负责的。这很类似==操作符: ==操作符只负责引用的"值"相等，至于这个地址所指向的对象内容是否相等，==操作符是不管的。

理解final问题有很重要的含义。许多程序漏洞都基于此--final只能保证引用永远指向固定对象，不能保证那个对象的状态不变。在多线程的操作中,一个对象会被多个线程共享或修改，一个线程对对象无意识的修改可能会导致另一个使用此对象的线程崩溃。一个错误的解决方法就是在此对象新建的时候把它声明为final，意图使得它"永远不变"。其实那是徒劳的。

问题五: 到底要怎么样初始化！

本问题讨论变量的初始化，所以先来看一下Java中有哪些种类的变量。
  
1. 类的属性，或者叫值域
  
2. 方法里的局部变量
  
3. 方法的参数

对于第一种变量，Java虚拟机会自动进行初始化。如果给出了初始值，则初始化为该初始值。如果没有给出，则把它初始化为该类型变量的默认初始值。

int类型变量默认初始值为0
  
float类型变量默认初始值为0.0f
  
double类型变量默认初始值为0.0
  
boolean类型变量默认初始值为false
  
char类型变量默认初始值为0(ASCII码)
  
long类型变量默认初始值为0
  
所有对象引用类型变量默认初始值为null，即不指向任何对象。注意数组本身也是对象，所以没有初始化的数组引用在自动初始化后其值也是null。

对于两种不同的类属性，static属性与instance属性，初始化的时机是不同的。instance属性在创建实例的时候初始化，static属性在类加载，也就是第一次用到这个类的时候初始化，对于后来的实例的创建，不再次进行初始化。这个问题会在以后的系列中进行详细讨论。

对于第二种变量，必须明确地进行初始化。如果再没有初始化之前就试图使用它，编译器会抗议。如果初始化的语句在try块中或if块中，也必须要让它在第一次使用前一定能够得到赋值。也就是说，把初始化语句放在只有if块的条件判断语句中编译器也会抗议，因为执行的时候可能不符合if后面的判断条件，如此一来初始化语句就不会被执行了，这就违反了局部变量使用前必须初始化的规定。但如果在else块中也有初始化语句，就可以通过编译，因为无论如何，总有至少一条初始化语句会被执行，不会发生使用前未被初始化的事情。对于try-catch也是一样，如果只有在try块里才有初始化语句，编译部通过。如果在catch或finally里也有，则可以通过编译。总之，要保证局部变量在使用之前一定被初始化了。所以，一个好的做法是在声明他们的时候就初始化他们，如果不知道要出事化成什么值好，就用上面的默认值吧！

其实第三种变量和第二种本质上是一样的，都是方法中的局部变量。只不过作为参数，肯定是被初始化过的，传入的值就是初始值，所以不需要初始化。

问题六: instanceof是什么东西？

instanceof是Java的一个二元操作符，和==，>，<是同一类东西。由于它是由字母组成的，所以也是Java的保留关键字。它的作用是测试它左边的对象是否是它右边的类的实例，返回boolean类型的数据。举个例子: 

String s = "I AM an Object!";
  
boolean isObject = s instanceof Object;

我们声明了一个String对象引用，指向一个String对象，然后用instancof来测试它所指向的对象是否是Object类的一个实例，显然，这是真的，所以返回true，也就是isObject的值为True。
  
instanceof有一些用处。比如我们写了一个处理账单的系统，其中有这样三个类: 

public class Bill {//省略细节}
  
public class PhoneBill extends Bill {//省略细节}
  
public class GasBill extends Bill {//省略细节}

在处理程序里有一个方法，接受一个Bill类型的对象，计算金额。假设两种账单计算方法不同，而传入的Bill对象可能是两种中的任何一种，所以要用instanceof来判断: 

public double calculate(Bill bill) {
  
if (bill instanceof PhoneBill) {
  
//计算电话账单
  
}
  
if (bill instanceof GasBill) {
  
//计算燃气账单
  
}
  
...
  
}
  
这样就可以用一个方法处理两种子类。

然而，这种做法通常被认为是没有好好利用面向对象中的多态性。其实上面的功能要求用方法重载完全可以实现，这是面向对象变成应有的做法，避免回到结构化编程模式。只要提供两个名字和返回值都相同，接受参数类型不同的方法就可以了: 

public double calculate(PhoneBill bill) {
  
//计算电话账单
  
}

public double calculate(GasBill bill) {
  
//计算燃气账单
  
}

所以，使用instanceof在绝大多数情况下并不是推荐的做法，应当好好利用多态


http://www.blogjava.net/hilor/articles/150610.html