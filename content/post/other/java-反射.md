---
title: java 反射, reflect
author: "-"
date: 2011-09-09T03:34:28+00:00
url: /?p=736
categories:
  - Java
tags:
  - reprint
---
## java 反射, reflect

[http://www.iteye.com/topic/137944](http://www.iteye.com/topic/137944)
  
## 什么是反射

反射的概念是由 Smith 在 1982 年首次提出的，主要是指程序可以访问、检测和修改它本身状态或行为的一种能力。这一概念的提出很快引发了计算机科学领域关于应用反射性的研究。它首先被程序语言的设计领域所采用, 并在 Lisp 和面向对象方面取得了成绩。其中 LEAD/LEAD++ 、OpenC++ 、MetaXa 和 OpenJava 等就是基于反射机制的语言。最近，反射机制也被应用到了视窗系统、操作系统和文件系统中。

反射本身并不是一个新概念，尽管计算机科学赋予了反射概念新的含义。在计算机科学领域，反射是指一类应用，它们能够自描述和自控制。也就是说，这类应用通过采用某种机制来实现对自己行为的描述 (self-representation) 和监测 (examination) ，并能根据自身行为的状态和结果，调整或修改应用所描述行为的状态和相关的语义。

## 什么是Java中的类反射
  
Reflection 是 Java 程序开发语言的特征之一，它允许运行中的 Java 程序对自身进行检查，或者说"自审"，并能直接操作程序的内部属性和方法。Java 的这一能力在实际应用中用得不是很多，但是在其它的程序设计语言中根本就不存在这一特性。例如，Pascal、C 或者 C++ 中就没有办法在程序中获得函数定义相关的信息。
  
Reflection 是 Java 被视为动态 (或准动态) 语言的关键，允许程序于执行期 Reflection APIs 取得任何已知名称之 class 的內部信息，包括 package、type parameters、superclass、implemented interfaces、inner classes, outer class, fields、constructors、methods、modifiers，並可于执行期生成instances、变更 fields 內容或唤起 methods。

## Java类反射中所必须的类
  
Java的类反射所需要的类并不多，它们分别是: Field、Constructor、Method、Class、Object，下面我将对这些类做一个简单的说明。
  
Field类: 提供有关类或接口的属性的信息，以及对它的动态访问权限。反射的字段可能是一个类 (静态) 属性或实例属性，简单的理解可以把它看成一个封装反射类的属性的类。
  
Constructor类: 提供关于类的单个构造方法的信息以及对它的访问权限。这个类和Field类不同，Field类封装了反射类的属性，而Constructor类则封装了反射类的构造方法。
  
Method类: 提供关于类或接口上单独某个方法的信息。所反映的方法可能是类方法或实例方法 (包括抽象方法) 。 这个类不难理解，它是用来封装反射类方法的一个类。
  
Class类: 类的实例表示正在运行的 Java 应用程序中的类和接口。枚举是一种类，注释是一种接口。每个数组属于被映射为 Class 对象的一个类，所有具有相同元素类型和维数的数组都共享该 Class 对象。
  
Object类: 每个类都使用 Object 作为超类。所有对象 (包括数组) 都实现这个类的方法。

## Java的反射类能做什么
  
看完上面的这么多我想你已经不耐烦了，你以为我在浪费你的时间，那么好吧！下面我们就用一些简单的小例子来说明它。
  
首先我们来看一下通过Java的反射机制我们能得到些什么。

```java
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

class A extends Object implements ActionListener{
  private int a = 3;
  public Integer b = new Integer(4);
  public A(){}
  public A(int id,String name){}
  public int abc(int id,String name){return 0;}
  public void actionPerformed(ActionEvent e){}
}
```

你可能被我这个类弄糊涂了，你看不出我要做什么，那就不要看这个类了，这个类是用来测试的，你知道知道它继承了Object类，有一个接口是ActionListener，两个属性int和Integer,两个构造方法和两个方法，这就足够了。
  
下面我们把A这个类作为一个反射类，来过去A类中的一些信息，首先我们先来过去一下反射类中的属性和属性值。

import java.lang.reflect.*;

class B{

public static void main(String args[]){
  
A r = new A();
  
Class temp = r.getClass();
  
try{
  
System.out.println("反射类中所有公有的属性");
  
Field[] fb =temp.getFields();
  
for(int j=0;j<fb.length;j++){
  
Class cl = fb[j].getType();
  
System.out.println("fb:"+cl);
  
}

System.out.println("反射类中所有的属性");
  
Field[] fa = temp.getDeclaredFields();
  
for(int j=0;j<fa.length;j++){
  
Class cl = fa[j].getType();
  
System.out.println("fa:"+cl);
  
}
  
System.out.println("反射类中私有属性的值");
  
Field f = temp.getDeclaredField("a");
  
f.setAccessible(true);
  
Integer i = (Integer)f.get(r);
  
System.out.println(i);
  
}catch(Exception e){
  
e.printStackTrace();
  
}
  
}

}

这里用到了两个方法，getFields()、getDeclaredFields()，它们分别是用来获取反射类中所有公有属性和反射类中所有的属性的方法。另外还有getField(String)和getDeclaredField(String)方法都是用来过去反射类中指定的属性的方法，要注意的是getField方法只能取到反射类中公有的属性，而getDeclaredField方法都能取到。
  
这里还用到了Field 类的setAccessible方法，它是用来设置是否有权限访问反射类中的私有属性的，只有设置为true时才可以访问，默认为false。另外Field类还有set(Object AttributeName,Object value)方法，可以改变指定属性的值。

下面我们来看一下如何获取反射类中的构造方法
  
import java.lang.reflect.*;
  
public class SampleConstructor {
  
public static void main(String[] args) {
  
A r = new A();
  
printConstructors(r);
  
}

public static void printConstructors(A r) {
  
Class c = r.getClass();
  
//获取指定类的类名
  
String className = c.getName();
  
try {
  
//获取指定类的构造方法
  
Constructor[] theConstructors = c.getConstructors();
  
for(int i=0; i<theConstructors.length; i++) {
  
//获取指定构造方法的参数的集合
  
Class[] parameterTypes = theConstructors[i].getParameterTypes();

System.out.print(className + "(");

for(int j=0; j<parameterTypes.length; j++)
  
System.out.print(parameterTypes[j].getName() + " ");

System.out.println(")");

}
  
}catch(Exception e) {
  
e.printStackTrace();
  
}
  
}
  
}
  
这个例子很简单,只是用getConstructors()方法获取了反射类的构造方法的集合，并用Constructor类的getParameterTypes()获取该构造方法的参数。

下面我们再来获取一下反射类的父类 (超类) 和接口
  
import java.io.*;
  
import java.lang.reflect.*;

public class SampleInterface {
  
public static void main(String[] args) throws Exception {
  
A raf = new A();
  
printInterfaceNames(raf);
  
}

public static void printInterfaceNames(Object o) {
  
Class c = o.getClass();
  
//获取反射类的接口
  
Class[] theInterfaces = c.getInterfaces();
  
for(int i=0; i<theInterfaces.length; i++)
  
System.out.println(theInterfaces[i].getName());
  
//获取反射类的父类 (超类) 
  
Class theSuperclass = c.getSuperclass();
  
System.out.println(theSuperclass.getName());
  
}
  
}
  
这个例子也很简单，只是用Class类的getInterfaces()方法获取反射类的所有接口，由于接口可以有多个，所以它返回一个Class数组。用getSuperclass()方法来获取反射类的父类 (超类) ，由于一个类只能继承自一个类，所以它返回一个Class对象。

下面我们来获取一下反射类的方法
  
import java.lang.reflect.*;
  
public class SampleMethod {

public static void main(String[] args) {
  
A p = new A();
  
printMethods(p);
  
}

public static void printMethods(Object o) {
  
Class c = o.getClass();
  
String className = c.getName();
  
Method[] m = c.getMethods();
  
for(int i=0; i<m.length; i++) {
  
//输出方法的返回类型
  
System.out.print(m[i].getReturnType().getName());
  
//输出方法名
  
System.out.print(" "+m[i].getName()+"(");
  
//获取方法的参数
  
Class[] parameterTypes = m[i].getParameterTypes();
  
for(int j=0; j<parameterTypes.length; j++){ System.out.print(parameterTypes[j].getName()); if(parameterTypes.length>j+1){
  
System.out.print(",");
  
}
  
}

System.out.println(")");
  
}

}

}
  
这个例子并不难，它只是获得了反射类的所有方法，包括继承自它父类的方法。然后获取方法的返回类型、方法名和方法参数。

接下来让我们回过头来想一想，我们获取了反射类的属性、构造方法、父类、接口和方法，可这些东西能帮我们做些什么呢！！
  
下面我写一个比较完整的小例子，来说明Java的反射类能做些什么吧！！
  
import java.lang.reflect.Constructor;
  
import java.lang.reflect.Method;

public class LoadMethod {
  
public Object Load(String cName,String MethodName,String[] type,String[] param){
  
Object retobj = null;
  
try {
  
//加载指定的Java类
  
Class cls = Class.forName(cName);

//获取指定对象的实例
  
Constructor ct = cls.getConstructor(null);
  
Object obj = ct.newInstance(null);

//构建方法参数的数据类型
  
Class partypes[] = this.getMethodClass(type);

//在指定类中获取指定的方法
  
Method meth = cls.getMethod(MethodName, partypes);

//构建方法的参数值
  
Object arglist[] = this.getMethodObject(type,param);

//调用指定的方法并获取返回值为Object类型
  
retobj= meth.invoke(obj, arglist);

}
  
catch (Throwable e) {
  
System.err.println(e);
  
}
  
return retobj;
  
}

//获取参数类型Class[]的方法
  
public Class[] getMethodClass(String[] type){
  
Class[] cs = new Class[type.length];
  
for (int i = 0; i < cs.length; i++) {
  
if(!type[i].trim().equals("")||type[i]!=null){
  
if(type[i].equals("int")||type[i].equals("Integer")){
  
cs[i]=Integer.TYPE;
  
}else if(type[i].equals("float")||type[i].equals("Float")){
  
cs[i]=Float.TYPE;
  
}else if(type[i].equals("double")||type[i].equals("Double")){
  
cs[i]=Double.TYPE;
  
}else if(type[i].equals("boolean")||type[i].equals("Boolean")){
  
cs[i]=Boolean.TYPE;
  
}else{
  
cs[i]=String.class;
  
}
  
}
  
}
  
return cs;
  
}

//获取参数Object[]的方法
  
public Object[] getMethodObject(String[] type,String[] param){
  
Object[] obj = new Object[param.length];
  
for (int i = 0; i < obj.length; i++) {
  
if(!param[i].trim().equals("")||param[i]!=null){
  
if(type[i].equals("int")||type[i].equals("Integer")){
  
obj[i]= new Integer(param[i]);
  
}else if(type[i].equals("float")||type[i].equals("Float")){
  
obj[i]= new Float(param[i]);
  
}else if(type[i].equals("double")||type[i].equals("Double")){
  
obj[i]= new Double(param[i]);
  
}else if(type[i].equals("boolean")||type[i].equals("Boolean")){
  
obj[i]=new Boolean(param[i]);
  
}else{
  
obj[i] = param[i];
  
}
  
}
  
}
  
return obj;
  
}
  
}
  
这是我在工作中写的一个实现Java在运行时加载指定的类，并调用指定方法的一个小例子。这里没有main方法，你可以自己写一个。
  
Load方法接收的五个参数分别是，Java的类名，方法名，参数的类型和参数的值。

结束语: 
  
Java语言反射提供一种动态链接程序组件的多功能方法。它允许程序创建和控制任何类的对象，无需提前硬编码目标类。这些特性使得反射特别适用于创建以非常普通的方式与对象协作的库。Java reflection 非常有用，它使类和数据结构能按名称动态检索相关信息，并允许在运行着的程序中操作这些信息。Java 的这一特性非常强大，并且是其它一些常用语言，如 C、C++、Fortran 或者 Pascal 等都不具备的。

但反射有两个缺点。第一个是性能问题。用于字段和方法接入时反射要远慢于直接代码。性能问题的程度取决于程序中是如何使用反射的。如果它作为程序运行中相对很少涉及的部分，缓慢的性能将不会是一个问题。即使测试中最坏情况下的计时图显示的反射操作只耗用几微秒。仅反射在性能关键的应用的核心逻辑中使用时性能问题才变得至关重要。


JAVA语言中的反射机制: 
  
在Java 运行时 环境中，对于任意一个类，能否知道这个类有哪些属性和方法？
  
对于任意一个对象，能否调用他的方法？这些答案是肯定的，这种动态获取类的信息，以及动态调用类的方法的功能来源于JAVA的反射。从而使java具有动态语言的特性。
  
JAVA反射机制主要提供了以下功能: 
  
1.在运行时判断任意一个对象所属的类
  
2.在运行时构造任意一个类的对象
  
3.在运行时判断任意一个类所具有的成员变量和方法 (通过反射甚至可以调用private方法) 
  
4.在运行时调用任意一个对象的方法 (\*****注意: 前提都是在运行时，而不是在编译时) 
  
Java 反射相关的API简介: 
  
位于java.lang.reflect包中
  
-Class类: 代表一个类
  
-Filed类: 代表类的成员变量
  
-Method类: 代表类的方法
  
-Constructor类: 代表类的构造方法
  
-Array类: 提供了动态创建数组，以及访问数组的元素的静态方法。该类中的所有方法都是静态方法

--Class类
  
在 java 的Object类中的申明了数个应该在所有的java类中被改写的methods: 
  
hashCode(), equals(),clone(),toString(),getClass()等，其中的getClass()返回Class 类型的对象。
  
Class类十分的特殊，它和一般的类一样继承自Object，其实体用以表达java程序运行
  
时的 class和 interface，也用来表达 enum，array，primitive，Java Types 以及关键字void
  
，当加载一个类，或者当加载器(class loader)的defineClass() 被JVM调用，便产生一个Class
  
对象，
  
Class是Reflection起源，针对任何你想探勘的class (类) ，唯有现为他产生一个Class
  
的对象，接下来才能经由后者唤起为数十多个的反射API。

Java允许我们从多种途径为一个类class生成对应的Class对象。
  
-运用 getClass(): Object类中的方法，每个类都拥有此方法
  
String str="abc";
  
Class cl=str.getClass();

-用 Class.getSuperclass(): Class类中的方法，返回该Class的父类的Class
  
-用 Class.forName()静态方法: 
  
-用 ,Class: 类名.class
  
-用primitive wrapper classes的TYPE语法:  基本类型包装类的TYPE，如: Integer.TYPE
  
注意: TYPE的使用，只适合原生(基本)数据类型
  
--运行时生成instance
  
想生成对象的实体，在反射动态机制中有两种方法，一个针对无变量的构造方法，一个针对带参数的
  
构造方法,如果想调用带参数的构造方法，就比较的麻烦，不能直接调用Class类中的newInstance () 
  
，而是调用Constructor类中newInstance()方法，首先准备一个Class[]作为Constructor的参数类型。
  
然后调用该Class对象的getConstructor()方法获得一个专属的Constructor的对象，最后再准备一个
  
Object[]作为Constructor对象昂的newInstance () 方法的实参。
  
在这里需要说明的是 只有两个类拥有newInstance () 方法，分别是Class类和Constructor类
  
Class类中的newInstance () 方法是不带参数的，而Constructro类中的newInstance () 方法是带参数的
  
需要提供必要的参数。
  
例:
  
Class c=Class.forName("DynTest");
  
Class[] ptype=new Class[]{double.class,int.class}；
  
Constructor ctor=c.getConstructor(ptypr);
  
Object[] obj=new Object[]{new Double(3.1415),new Integer(123)};
  
Object object=ctor.newInstance(obj);
  
System.out.println(object);
  
--运行时调用Method
  
这个动作首先准备一个Class[]{}作为getMethod (String name，Class[]) 方法的参数类型，接下来准备一个
  
Obeject[]放置自变量，然后调用Method对象的invoke (Object obj，Object[]) 方法。
  
注意，在这里调用
  
--运行时调用Field内容
  
变更Field不需要参数和自变量，首先调用Class的getField () 并指定field名称，获得特定的Field对象后
  
便可以直接调用Field的 get (Object obj) 和set(Object obj,Object value)方法
  
java 代码
  
package cn.com.reflection;

import java.lang.reflect.Field;
  
import java.lang.reflect.InvocationTargetException;
  
import java.lang.reflect.Method;

public class ReflectTester {

/**
  
* 在这个类里面存在有copy () 方法，根据指定的方法的参数去 构造一个新的对象的拷贝
  
* 并将他返回
  
* @throws NoSuchMethodException
  
* @throws InvocationTargetException
  
* @throws IllegalAccessException
  
* @throws InstantiationException
  
* @throws SecurityException
  
* @throws IllegalArgumentException
  
*/
  
public Object copy(Object obj) throws IllegalArgumentException, SecurityException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{

//获得对象的类型
  
Class classType=obj.getClass();
  
System.out.println("该对象的类型是: "+classType.toString());

//通过默认构造方法去创建一个新的对象，getConstructor的视其参数决定调用哪个构造方法
  
Object objectCopy=classType.getConstructor(new Class[]{}).newInstance(new Object[]{});

//获得对象的所有属性
  
Field[] fields=classType.getDeclaredFields();

for(int i=0;i
  
//获取数组中对应的属性
  
Field field=fields[i];

String fieldName=field.getName();
  
String stringLetter=fieldName.substring(0, 1).toUpperCase();

//获得相应属性的getXXX和setXXX方法名称
  
String getName="get"+stringLetter+fieldName.substring(1);
  
String setName="set"+stringLetter+fieldName.substring(1);

//获取相应的方法
  
Method getMethod=classType.getMethod(getName, new Class[]{});
  
Method setMethod=classType.getMethod(setName, new Class[]{field.getType()});

//调用源对象的getXXX () 方法
  
Object value=getMethod.invoke(obj, new Object[]{});
  
System.out.println(fieldName+" :"+value);

//调用拷贝对象的setXXX () 方法
  
setMethod.invoke(objectCopy,new Object[]{value});

}

return objectCopy;

}

public static void main(String[] args) throws IllegalArgumentException, SecurityException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
  
Customer customer=new Customer();
  
customer.setName("hejianjie");
  
customer.setId(new Long(1234));
  
customer.setAge(19);

Customer customer2=null;
  
customer2=(Customer)new ReflectTester().copy(customer);
  
System.out.println(customer.getName()+" "+customer2.getAge()+" "+customer2.getId());

System.out.println(customer);
  
System.out.println(customer2);

}

}

class Customer{

private Long id;

private String name;

private int age;

public Customer(){

}

public int getAge() {
  
return age;
  
}

public void setAge(int age) {
  
this.age = age;
  
}

public Long getId() {
  
return id;
  
}

public void setId(Long id) {
  
this.id = id;
  
}

public String getName() {
  
return name;
  
}

public void setName(String name) {
  
this.name = name;
  
}

}

java 代码
  
package cn.com.reflection;

import java.lang.reflect.Array;

public class ArrayTester1 {

/**
  
* 此类根据反射来创建
  
* 一个动态的数组
  
*/
  
public static void main(String[] args) throws ClassNotFoundException {

Class classType=Class.forName("java.lang.String");

Object array= Array.newInstance(classType,10); //指定数组的类型和大小

//对索引为5的位置进行赋值
  
Array.set(array, 5, "hello");

String s=(String)Array.get(array, 5);

System.out.println(s);

//循环遍历这个动态数组
  
for(int i=0;i<((String[])array).length;i++){

String str=(String)Array.get(array, i);

System.out.println(str);
  
}

}

}

## Java 反射真的很慢吗？

反射带来的问题
到现在为止，我们已经把反射生成实例的所有流程都搞清楚了。回到文章开头的问题，我们现在反思下，反射性能低么？为什么？

反射调用过程中会产生大量的临时对象，这些对象会占用内存，可能会导致频繁 gc，从而影响性能。
反射调用方法时会从方法数组中遍历查找，并且会检查可见性等操作会耗时。
反射在达到一定次数时，会动态编写字节码并加载到内存中，这个字节码没有经过编译器优化，也不能享受JIT优化。
反射一般会涉及自动装箱/拆箱和类型转换，都会带来一定的资源开销。

在Android中，我们可以在某些情况下对反射进行优化。举个例子，EventBus 2.x 会在 register 方法运行时，遍历所有方法找到回调方法；而EventBus 3.x 则在编译期间，将所有回调方法的信息保存的自己定义的 SubscriberMethodInfo 中，这样可以减少对运行时的性能影响。
本文的结论如下：

不要在性能敏感的应用中，频繁调用反射。
如果反射执行的次数小于1000这个数量级，反射的耗时实际上与正常调用无太大差异。
反射对内存占用还有一定影响的，在内存敏感的场景下，谨慎使用反射。

作者：orzangleli
链接：https://juejin.cn/post/6844904098207105038
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
