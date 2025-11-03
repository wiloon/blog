---
title: Java转型(向上或向下转型)upcast)和向下转型(downcast)
author: "-"
date: 2014-05-30T01:48:04+00:00
url: /?p=6700
categories:
  - Inbox
tags:
  - Java

---
## Java转型(向上或向下转型)upcast)和向下转型(downcast)
在Java编程中经常碰到类型转换,对象类型转换主要包括向上转型和向下转型。

5.13.1 向上转型
  
我们在现实中常常这样说: 这个人会唱歌。在这里,我们并不关心这个人是黑人还是白人,是成人还是小孩,也就是说我们更倾向于使用抽象概念"人"。再例如,麻雀是鸟类的一种 (鸟类的子类) ,而鸟类则是动物中的一种 (动物的子类) 。我们现实中也经常这样说: 麻雀是鸟。这两种说法实际上就是所谓的向上转型,通俗地说就是子类转型成父类。这也符合Java提倡的面向抽象编程思想。来看下面的代码: 
  
package a.b;

public class A {

public void a1() {

System.out.println("Superclass");

}

}

A的子类B: 
  
package a.b;

public class B extends A {

public void a1() {

System.out.println("Childrenclass"); //覆盖父类方法

}

public void b1(){} //B类定义了自己的新方法

}

C类: 
  
package a.b;

public class C {

public static void main(String[] args) {

A a = new B(); //向上转型

a.a1();

}

}

如果运行C,输出的是Superclass 还是Childrenclass？不是你原来预期的Superclass,而是Childrenclass。这是因为a实际上指向的是一个子类对象。当然,你不用担心,Java虚拟机会自动准确地识别出究竟该调用哪个具体的方法。不过,由于向上转型,a对象会遗失和父类不同的方法,例如b1()。有人可能会提出疑问: 这不是多此一举吗？我们完全可以这样写: 
  
B a = new B();

a.a1();

确实如此！但这样就丧失了面向抽象的编程特色,降低了可扩展性。其实,不仅仅如此,向上转型还可以减轻编程工作量。来看下面的显示器类Monitor: 
  
package a.b;

public class Monitor{

public void displayText() {}

public void displayGraphics() {}

}

液晶显示器类LCDMonitor是Monitor的子类: 
  
package a.b;

public class LCDMonitor extends Monitor {

public void displayText() {

System.out.println("LCD display text");

}

public void displayGraphics() {

System.out.println("LCD display graphics");

}

}

阴极射线管显示器类CRTMonitor自然也是Monitor的子类: 
  
package a.b;

public class CRTMonitor extends Monitor {

public void displayText() {

System.out.println("CRT display text");

}

public void displayGraphics() {

System.out.println("CRT display graphics");

}

}

等离子显示器PlasmaMonitor也是Monitor的子类: 
  
package a.b;

public class PlasmaMonitor extends Monitor {

public void displayText() {

System.out.println("Plasma display text");

}

public void displayGraphics() {

System.out.println("Plasma display graphics");

}

}

现在有一个MyMonitor类。假设没有向上转型,MyMonitor类代码如下: 
  
package a.b;

public class MyMonitor {

public static void main(String[] args) {

run(new LCDMonitor());

run(new CRTMonitor());

run(new PlasmaMonitor());

}

public static void run(LCDMonitor monitor) {

monitor.displayText();

monitor.displayGraphics();

}

public static void run(CRTMonitor monitor) {

monitor.displayText();

monitor.displayGraphics();

}

public static void run(PlasmaMonitor monitor) {

monitor.displayText();

monitor.displayGraphics();

}

}

可能你已经意识到上述代码有很多重复代码,而且也不易维护。有了向上转型,代码可以更为简洁: 
  
package a.b;

public class MyMonitor {

public static void main(String[] args) {

run(new LCDMonitor()); //向上转型

run(new CRTMonitor()); //向上转型

run(new PlasmaMonitor()); //向上转型

}

public static void run(Monitor monitor) { //父类实例作为参数

monitor.displayText();

monitor.displayGraphics();

}

}

我们也可以采用接口的方式,例如: 
  
package a.b;

public interface Monitor {

abstract void displayText();

abstract void displayGraphics();

}

将液晶显示器类LCDMonitor稍作修改: 
  
package a.b;

public class LCDMonitor implements Monitor {

public void displayText() {

System.out.println("LCD display text");

}

public void displayGraphics() {

System.out.println("LCD display graphics");

}

}

CRTMonitor、PlasmaMonitor类的修改方法与LCDMonitor类似,而MyMonitor可以不不作任何修改。
  
可以看出,向上转型体现了类的多态性,增强了程序的简洁性。
  
5.13.2 向下转型
  
子类转型成父类是向上转型,反过来说,父类转型成子类就是向下转型。但是,向下转型可能会带来一些问题: 我们可以说麻雀是鸟,但不能说鸟就是麻雀。来看下面的例子: 
  
A类: 
  
package a.b;

public class A {

void aMthod() {

System.out.println("A method");

}

}

A的子类B: 
  
package a.b;

public class B extends A {

void bMethod1() {

System.out.println("B method 1");

}

void bMethod2() {

System.out.println("B method 2");

}

}

C类: 
  
package a.b;

public class C {

public static void main(String[] args) {

A a1 = new B(); // 向上转型

a1.aMthod(); // 调用父类aMthod(),a1遗失B类方法bMethod1()、bMethod2()

B b1 = (B) a1; // 向下转型,编译无错误,运行时无错误

b1.aMthod(); // 调用父类A方法

b1.bMethod1(); // 调用B类方法

b1.bMethod2(); // 调用B类方法

A a2 = new A();

B b2 = (B) a2; // 向下转型,编译无错误,运行时将出错

b2.aMthod();

b2.bMethod1();

b2.bMethod2();

}

}

从上面的代码我们可以得出这样一个结论: 向下转型需要使用强制转换。运行C程序,控制台将输出: 
  
Exception in thread "main" java.lang.ClassCastException: a.b.A cannot be cast to a.b.B at
  
a.b.C.main(C.java:14)

A method

A method

B method 1

B method 2

其实黑体部分的向下转型代码后的注释已经提示你将发生运行时错误。为什么前一句向下转型代码可以,而后一句代码却出错？这是因为a1指向一个子类B的对象,所以子类B的实例对象b1当然也可以指向a1。而a2是一个父类对象,子类对象b2不能指向父类对象a2。那么如何避免在执行向下转型时发生运行时ClassCastException异常？使用5.7.7节学过的instanceof就可以了。我们修改一下C类的代码: 
  
A a2 = new A();

if (a2 instanceof B) {

B b2 = (B) a2;

b2.aMthod();

b2.bMethod1();

b2.bMethod2();

}

这样处理后,就不用担心类型转换时发生ClassCastException异常了。

http://blog.csdn.net/shanghui815/article/details/6088588