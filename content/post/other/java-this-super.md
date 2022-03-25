---
title: java this super
author: "-"
date: 2012-01-02T09:20:30+00:00
url: /?p=730
categories:
  - Java

tags:
  - reprint
---
## java this super
在Java中，this通常指当前对象，super则指父类的。当你想要引用当前对象的某种东西，比如当前对象的某个方法，或当前对象的某个成员，你便 可以利用this来实现这个目的，当然，this的另一个用途是调用当前对象的另一个构造函数，这些马上就要讨论。如果你想引用父类的某种东西，则非 super莫属。由于this与super有如此相似的一些特性和与生俱来的某种关系，所以我们在这一块儿来讨论，希望能帮助你区分和掌握它们两个。
  
在一般方法中
  
最普遍的情况就是，在你的方法中的某个形参名与当前对象的某个成员有相同的名字，这时为了不至于混淆，你便需要明确使用this关键字来指明你要使用某 个成员，使用方法是"this.成员名"，而不带this的那个便是形参。另外，还可以用"this.方法名"来引用当前对象的某个方法，但这时this 就不是必须的了，你可以直接用方法名来访问那个方法，编译器会知道你要调用的是那一个。下面的代码演示了上面的用法: 
  
public class DemoThis{
  
private String name;
  
private int age;
  
DemoThis(String name,int age){
  
setName(name); //你可以加上this来调用方法，像这样: this.setName(name);但这并不是必须的
  
setAge(age);
  
this.print();
  
}
  
public void setName(String name){
  
this.name=name;//此处必须指明你要引用成员变量
  
}
  
public void setAge(int age){
  
this.age=age;
  
}
  
public void print(){
  
System.out.println("Name="+name+" Age="+age);//在此行中并不需要用this，因为没有会导致混淆的东西
  
}
  
public static void main(String[] args){
  
DemoThis dt=new DemoThis("Kevin","22");
  
}
  
}
  
这段代码很简单，不用解释你也应该能看明白。在构造函数中你看到用this.print(),你完全可以用print()来代替它，两者效果一样。下面我们修改这个程序，来演示super的用法。
  
class Person{
  
public int c;
  
private String name;
  
private int age;
  
protected void setName(String name){
  
this.name=name;
  
}
  
protected void setAge(int age){
  
this.age=age;
  
}
  
protected void print(){
  
System.out.println("Name="+name+" Age="+age);
  
}
  
}
  
public class DemoSuper extends Person{
  
public void print(){
  
System.out.println("DemoSuper:");
  
super.print();
  
}
  
public static void main(String[] args){
  
DemoSuper ds=new DemoSuper();
  
ds.setName("kevin");
  
ds.setAge(22);
  
ds.print();
  
}
  
}
  
在DemoSuper中，重新定义的print方法覆写了父类的print方法，它首先做一些自己的事情，然后调用父类的那个被覆写了的方法。输出结果说明了这一点: 
  
DemoSuper:
  
Name=kevin Age=22
  
这样的使用方法是比较常用的。另外如果父类的成员可以被子类访问，那你可以像使用this一样使用它，用"super.父类中的成员名"的方式，但常常你并不是这样来访问父类中的成员名的。
  
在构造函数中
  
构造函数是一种特殊的方法，在对象初始化的时候自动调用。在构造函数中，this和super也有上面说的种种使用方式，并且它还有特殊的地方，请看下面的例子: 
  
class Person{
  
public static void prt(String s){
  
System.out.println(s);
  
}
  
Person(){
  
prt("A Person.");
  
}
  
Person(String name){
  
prt("A person name is:"+name);
  
}
  
}
  
public class Chinese extends Person{
  
Chinese(){
  
super(); //调用父类构造函数 (1) 
  
prt("A chinese.");//(4)
  
}
  
Chinese(String name){
  
super(name);//调用父类具有相同形参的构造函数 (2) 
  
prt("his name is:"+name);
  
}
  
Chinese(String name,int age){
  
this(name);//调用当前具有相同形参的构造函数 (3) 
  
prt("his age is:"+age);
  
}
  
public static void main(String[] args){
  
Chinese cn=new Chinese();
  
cn=new Chinese("kevin");
  
cn=new Chinese("kevin",22);
  
}
  
}
  
在这段程序中，this和super不再是像以前那样用"."连接一个方法或成员，而是直接在其后跟上适当的参数，因此它的意义也就有了变化。 super后加参数的是用来调用父类中具有相同形式的构造函数，如1和2处。this后加参数则调用的是当前具有相同参数的构造函数，如3处。当然，在 Chinese的各个重载构造函数中，this和super在一般方法中的各种用法也仍可使用，比如4处，你可以将它替换为"this.prt"(因为它 继承了父类中的那个方法) 或者是"super.prt" (因为它是父类中的方法且可被子类访问) ，它照样可以正确运行。但这样似乎就有点画蛇添足的味道 了。
  
最后，写了这么多，如果你能对"this通常指代当前对象，super通常指代父类"这句话牢记在心，那么本篇便达到了目的，其它的你自会在以后的编程实践当中慢慢体会、掌握。另外关于本篇中提到的继承，请参阅相关Java教程。