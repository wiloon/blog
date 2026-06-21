---
title: Java反射机制
author: "-"
date: 2012-01-02T09:21:07+00:00
lastmod: 2026-06-21T11:46:40+08:00
url: java反射机制
categories:
  - language
tags:
  - java
  - reflection
  - remix
  - AI-assisted
---
## Java反射机制

### 通过反射取对象的属性值

```java
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class ReflectTest {
    public static void main(String[] args) {
        Foo foo = new Foo();
        foo.setBar("xxx");
        Map map = new HashMap();
        map.put("foo", "bar");
        foo.setTags(map);

        Class fooClass = foo.getClass();
        System.out.println("name:" + fooClass.getName());
        try {
            Field[] fields = fooClass.getDeclaredFields();
            for (Field field : fields) {
                field.setAccessible(true);
                System.out.println("field: " + field.getName());
                Object obj = field.get(foo);
                System.out.println(obj);
            }
            Field field0 = fooClass.getDeclaredField("bar");
            System.out.println(field0);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class Foo {
    private String bar;
    private Map<String, String> tags;

    public void setBar(String bar) {
        this.bar = bar;
    }

    public void setTags(Map tags) {
        this.tags = tags;
    }
}

```

Reflection 是Java被视为动态 (或准动态) 语言的一个关键性质。这个机制允许程序在运行时透过Reflection APIs取得任何一个已知名称的class的内部信息，包括其modifiers (诸如public, static 等等) 、superclass (例如Object) 、实现之interfaces (例如Cloneable) ，也包括fields和methods的所有信息，并可于运行时改变fields内容或唤起methods。本文借由实例，大面积示范Reflection APIs。

有时候我们说某个语言具有很强的动态性，有时候我们会区分动态和静态的不同技术与作法。我们朗朗上口动态绑定 (dynamic binding) 、动态链接 (dynamic linking) 、动态加载 (dynamic loading) 等。然而"动态"一词其实没有绝对而普遍适用的严格定义，有时候甚至像对象导向当初被导入编程领域一样，一人一把号，各吹各的调。

一般而言，开发者社群说到动态语言，大致认同的一个定义是: "程序运行时，允许改变程序结构或变量类型，这种语言称为动态语言"。从这个观点看，Perl，Python，Ruby是动态语言，C++，Java，C#不是动态语言。

尽管在这样的定义与分类下Java不是动态语言，它却有着一个非常突出的动态相关机制: Reflection。这个字的意思是"反射、映象、倒影"，用在Java身上指的是我们可以于运行时加载、探知、使用编译期间完全未知的classes。换句话说，Java程序可以加载一个运行时才得知名称的class，获悉其完整构造 (但不包括methods定义) ，并生成其对象实体、或对其fields设值、或唤起其methods1。这种"看透class"的能力 (the ability of the program to examine itself) 被称为introspection (内省、内观、反省) 。Reflection和introspection是常被并提的两个术语。

Java如何能够做出上述的动态特性呢？这是一个深远话题，本文对此只简单介绍一些概念。整个篇幅最主要还是介绍Reflection APIs，也就是让读者知道如何探索class的结构、如何对某个"运行时才获知名称的class"生成一份实体、为其fields设值、调用其methods。本文将谈到 [`java.lang.Class`](./lang-class.md)，以及java.lang.reflect中的Method、Field、Constructor等等classes。

[`java.lang.Class`](./lang-class.md) 是反射的起点：JVM 为每种类型维护唯一的 `Class` 对象，通过 `.class`、`getClass()`、`Class.forName` 等方式获取。取得 `Class` 之后，才能调用 `getDeclaredFields`、`getMethod` 等 API。三种获取方式、与实例的区别、常用方法等见专文，下文不再重复。

Java classes 组成分析
  
首先容我以图3的java.util.LinkedList为例，将Java class的定义大卸八块，每一块分别对应图4所示的Reflection API。图5则是"获得class各区块信息"的程序示例及执行结果，它们都取自本文示例程序的对应片段。

package java.util; //(1)
  
import java.lang.*; //(2)
  
public class LinkedList //(3)(4)(5)
  
extends AbstractSequentialList //(6)
  
implements List, Queue,
  
Cloneable, java.io.Serializable //(7)
  
{
  
private static class Entry { … }//(8)
  
public LinkedList() { … } //(9)
  
public LinkedList(Collection c) { … }
  
public E getFirst() { … } //(10)
  
public E getLast() { … }
  
private transient Entry header = …; //(11)
  
private transient int size = 0;
  
}
  
图3: 将一个Java class 大卸八块，每块相应于一个或一组Reflection APIs (图4) 。

Java classes 各成份所对应的Reflection APIs
  
图3的各个Java class成份，分别对应于图4的Reflection API，其中出现的Package、Method、Constructor、Field等等classes，都定义于java.lang.reflect。
  
Java class 内部模块 (参见图3) 
  
Java class 内部模块说明
  
相应之Reflection API，多半为Class methods。
  
返回值类型(return type)
  
(1) package
  
class隶属哪个package
  
getPackage()
  
Package
  
(2) import
  
class导入哪些classes
  
无直接对应之API。
  
解决办法见图5-2。

(3) modifier
  
class (或methods, fields) 的属性

int getModifiers()
  
Modifier.toString(int)
  
Modifier.isInterface(int)
  
int
  
String
  
bool
  
(4) class name or interface name
  
class/interface
  
名称getName()
  
String
  
(5) type parameters
  
参数化类型的名称
  
getTypeParameters()
  
TypeVariable []
  
(6) base class
  
base class (只可能一个) 
  
getSuperClass()
  
Class
  
(7) implemented interfaces
  
实现有哪些interfaces
  
getInterfaces()
  
Class[]

(8) inner classes
  
内部classes
  
getDeclaredClasses()
  
Class[]
  
(8') outer class
  
如果我们观察的class 本身是inner classes，那么相对它就会有个outer class。
  
getDeclaringClass()
  
Class
  
(9) constructors
  
构造函数getDeclaredConstructors()
  
不论 public 或private 或其它access level，皆可获得。另有功能近似之取得函数。
  
Constructor[]
  
(10) methods
  
操作函数getDeclaredMethods()
  
不论 public 或private 或其它access level，皆可获得。另有功能近似之取得函数。
  
Method[]
  
(11) fields
  
字段 (成员变量) 
  
getDeclaredFields()不论 public 或private 或其它access level，皆可获得。另有功能近似之取得函数。
  
Field[]
  
图4: Java class大卸八块后 (如图3) ，每一块所对应的Reflection API。本表并非
  
Reflection APIs 的全部。

Java Reflection API 运用示例
  
图5示范图4提过的每一个Reflection API，及其执行结果。程序中出现的tName()是个辅助函数，可将其第一自变量所代表的"Java class完整路径字符串"剥除路径部分，留下class名称，储存到第二自变量所代表的一个hashtable去并返回 (如果第二自变量为null，就不储存而只是返回) 。

#001 Class c = null;
  
c = Class.forName(args[0]);
  
#003
  
#004 Package p;
  
#005 p = c.getPackage();
  
#006
  
#007 if (p != null)
  
#008 System.out.println("package "+p.getName()+";");

执行结果 (例) : 
  
package java.util;
  
图5-1: 找出class 隶属的package。其中的c将继续沿用于以下各程序片段。

#001 ff = c.getDeclaredFields();
  
#002 for (int i = 0; i < ff.length; i++)
  
#003 x = tName(ff[i].getType().getName(), classRef);
  
#004
  
#005 cn = c.getDeclaredConstructors();
  
#006 for (int i = 0; i < cn.length; i++) {
  
#007 Class cx[] = cn[i].getParameterTypes();
  
#008 for (int j = 0; j < cx.length; j++)
  
#009 x = tName(cx[j].getName(), classRef);
  
#010 }
  
#011
  
#012 mm = c.getDeclaredMethods();
  
#013 for (int i = 0; i < mm.length; i++) {
  
#014 x = tName(mm[i].getReturnType().getName(), classRef);
  
#015 Class cx[] = mm[i].getParameterTypes();
  
#016 for (int j = 0; j < cx.length; j++)
  
#017 x = tName(cx[j].getName(), classRef);
  
#018 }
  
#019 classRef.remove(c.getName()); //不必记录自己 (不需import 自己) 

执行结果 (例) : 
  
import java.util.ListIterator;
  
import java.lang.Object;
  
import java.util.LinkedList$Entry;
  
import java.util.Collection;
  
import java.io.ObjectOutputStream;
  
import java.io.ObjectInputStream;
  
图5-2: 找出导入的classes，动作细节详见内文说明。

#001 int mod = c.getModifiers();
  
#002 System.out.print(Modifier.toString(mod)); //整个modifier
  
#003
  
#004 if (Modifier.isInterface(mod))
  
#005 System.out.print(" "); //关键词 "interface" 已含于modifier
  
#006 else
  
#007 System.out.print(" class "); //关键词 "class"
  
#008 System.out.print(tName(c.getName(), null)); //class 名称

执行结果 (例) : 
  
public class LinkedList
  
图5-3: 找出class或interface 的名称，及其属性 (modifiers) 。

#001 TypeVariable[] tv;
  
#002 tv = c.getTypeParameters(); //warning: unchecked conversion
  
#003 for (int i = 0; i < tv.length; i++) {
  
#004 x = tName(tv[i].getName(), null); //例如 E,K,V...
  
#005 if (i == 0) //第一个
  
#006 System.out.print(" #007 else //非第一个
  
#008 System.out.print("," + x);
  
#009 if (i == tv.length-1) //最后一个
  
#010 System.out.println(">");
  
#011 }

执行结果 (例) : 
  
public abstract interface Map
  
或 public class LinkedList
  
图5-4: 找出parameterized types 的名称

#001 Class supClass;
  
#002 supClass = c.getSuperclass();
  
#003 if (supClass != null) //如果有super class
  
#004 System.out.print(" extends" +
  
#005 tName(supClass.getName(),classRef));

执行结果 (例) : 
  
public class LinkedList
  
extends AbstractSequentialList,
  
图5-5: 找出base class。执行结果多出一个不该有的逗号于尾端。此非本处重点，为简化计，不多做处理。

#001 Class cc[];
  
#002 Class ctmp;
  
#003 //找出所有被实现的interfaces
  
#004 cc = c.getInterfaces();
  
#005 if (cc.length != 0)
  
#006 System.out.print(", rn" + " implements "); //关键词
  
#007 for (Class cite : cc) //JDK1.5 新式循环写法
  
#008 System.out.print(tName(cite.getName(), null)+", ");

执行结果 (例) : 
  
public class LinkedList
  
extends AbstractSequentialList,
  
implements List, Queue, Cloneable, Serializable,
  
图5-6: 找出implemented interfaces。执行结果多出一个不该有的逗号于尾端。此非本处重点，为简化计，不多做处理。

#001 cc = c.getDeclaredClasses(); //找出inner classes
  
#002 for (Class cite : cc)
  
#003 System.out.println(tName(cite.getName(), null));
  
#004
  
#005 ctmp = c.getDeclaringClass(); //找出outer classes
  
#006 if (ctmp != null)
  
#007 System.out.println(ctmp.getName());

执行结果 (例) : 
  
LinkedList$Entry
  
LinkedList$ListItr
  
图5-7: 找出inner classes 和outer class

#001 Constructor cn[];
  
#002 cn = c.getDeclaredConstructors();
  
#003 for (int i = 0; i < cn.length; i++) {
  
#004 int md = cn[i].getModifiers();
  
#005 System.out.print(" " + Modifier.toString(md) + " " +
  
#006 cn[i].getName());
  
#007 Class cx[] = cn[i].getParameterTypes();
  
#008 System.out.print("(");
  
#009 for (int j = 0; j < cx.length; j++) {
  
#010 System.out.print(tName(cx[j].getName(), null));
  
#011 if (j < (cx.length - 1)) System.out.print(", ");
  
#012 }
  
#013 System.out.print(")");
  
#014 }

执行结果 (例) : 
  
public java.util.LinkedList(Collection)
  
public java.util.LinkedList()
  
图5-8a: 找出所有constructors

#004 System.out.println(cn[i].toGenericString());

执行结果 (例) : 
  
public java.util.LinkedList(java.util.Collection)
  
public java.util.LinkedList()
  
图5-8b: 找出所有constructors。本例在for 循环内使用toGenericString()，省事。

#001 Method mm[];
  
#002 mm = c.getDeclaredMethods();
  
#003 for (int i = 0; i < mm.length; i++) {
  
#004 int md = mm[i].getModifiers();
  
#005 System.out.print(" "+Modifier.toString(md)+" "+
  
#006 tName(mm[i].getReturnType().getName(), null)+" "+
  
#007 mm[i].getName());
  
#008 Class cx[] = mm[i].getParameterTypes();
  
#009 System.out.print("(");
  
#010 for (int j = 0; j < cx.length; j++) {
  
#011 System.out.print(tName(cx[j].getName(), null));
  
#012 if (j < (cx.length - 1)) System.out.print(", ");
  
#013 }
  
#014 System.out.print(")");
  
#015 }

执行结果 (例) : 
  
public Object get(int)
  
public int size()
  
图5-9a: 找出所有methods

#004 System.out.println(mm[i].toGenericString());

public E java.util.LinkedList.get(int)
  
public int java.util.LinkedList.size()
  
图5-9b: 找出所有methods。本例在for 循环内使用toGenericString()，省事。

#001 Field ff[];
  
#002 ff = c.getDeclaredFields();
  
#003 for (int i = 0; i < ff.length; i++) {
  
#004 int md = ff[i].getModifiers();
  
#005 System.out.println(" "+Modifier.toString(md)+" "+
  
#006 tName(ff[i].getType().getName(), null) +" "+
  
#007 ff[i].getName()+";");
  
#008 }

执行结果 (例) : 
  
private transient LinkedList$Entry header;
  
private transient int size;
  
图5-10a: 找出所有fields

#004 System.out.println("G: " + ff[i].toGenericString());

private transient java.util.LinkedList.java.util.LinkedList$Entry??
  
java.util.LinkedList.header
  
private transient int java.util.LinkedList.size
  
图5-10b: 找出所有fields。本例在for 循环内使用toGenericString()，省事。