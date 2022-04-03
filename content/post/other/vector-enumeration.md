---
title: java enum/枚举
author: "-"
date: 2012-09-22T08:10:05+00:00
url: /?p=4183
tags:
  - Java

categories:
  - inbox
---
## java enum/枚举
Java 5.0 引入了枚举类型,语法参见 JLS 8.9

### 枚举比较
```java
// 枚举可以用 "==" 和 equals 比较
GameEnum s1 = GameEnum.BIG;
GameEnum s2 = GameEnum.BIG;
GameEnum ss1 = GameEnum.SMALL;
System.out.println("s1 == s2: " + (s1 == s2)); //true
System.out.println("s1.equals(s2): " + (s1.equals(s2))); //true
System.out.println("s1 == ss1: " + (s1 == ss1)); //false
System.out.println("s1.equals(ss1): " + (s1.equals(ss1))); //false
```

```java
// 字符串 > 枚举
Blah val = Blah.valueOf("A")
package com.ljq.test;
```

### 普通枚举

定义一个功能简单的枚举类型，跟定义一个简单的类很相似，例如  
跟类定义一样，枚举类型可以单独放在一个文件里，当一个枚举类型用public修饰时，它对其他包可见，否则只对同一个包中的类可见，这和类定义是一样的。  
标识符 MONDAY, TUESDAY等就称为枚举常量 (enumeration constants)   
每一个枚举常量被隐式的声明成Day的一个public、static成员，而且其类型为Day，亦就是说这些常量是self-typed的

```java
public   enum  Day
{
MONDAY, TUESDAT, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

```java
public enum ColorEnum {
    red, green, yellow, blue;
}

/**
* 枚举像普通的类一样可以添加属性和方法，可以为它添加静态和非静态的属性或方法
*/
public enum SeasonEnum {
//注: 枚举写在最前面，否则编译出错
    spring, summer, autumn, winter;

private final static String position = "test";

public static SeasonEnum getSeason() {
if ("test".equals(position))
return spring;
else
return winter;
}
}
```

### 有构造器的枚举

```java
public enum Gender{
//通过括号赋值,而且必须带有一个参构造器和一个属性跟方法，否则编译出错
//赋值必须都赋值或都不赋值，不能一部分赋值一部分不赋值；如果不赋值则不能写构造器，赋值编译也出错
MAN("MAN"), WOMEN("WOMEN");

private final String value;

//构造器默认也只能是private, 从而保证构造函数只能在内部使用
Gender(String value) {
this.value = value;
}

public String getValue() {
return value;
}
}
```

### 有抽象方法的枚举

```java
public enum OrderState {
    /** 已取消 */
    CANCEL {public String getName(){return "已取消";}},
    /** 待审核 */
    WAITCONFIRM {public String getName(){return "待审核";}},
    /** 等待付款 */
    WAITPAYMENT {public String getName(){return "等待付款";}},
    /** 正在配货 */
    ADMEASUREPRODUCT {public String getName(){return "正在配货";}},
    /** 等待发货 */
    WAITDELIVER {public String getName(){return "等待发货";}},
    /** 已发货 */
    DELIVERED {public String getName(){return "已发货";}},
    /** 已收货 */
    RECEIVED {public String getName(){return "已收货";}};

    public abstract String getName();
}

public static void main(String[] args) {
//枚举是一种类型，用于定义变量，以限制变量的赋值；赋值时通过"枚举名.值"取得枚举中的值
ColorEnum colorEnum = ColorEnum.blue;
switch (colorEnum) {
case red:
System.out.println("color is red");
break;
case green:
System.out.println("color is green");
break;
case yellow:
System.out.println("color is yellow");
break;
case blue:
System.out.println("color is blue");
break;
}

//遍历枚举
System.out.println("遍历ColorEnum枚举中的值");
for(ColorEnum color : ColorEnum.values()){
System.out.println(color);
}

//获取枚举的个数
System.out.println("ColorEnum枚举中的值有"+ColorEnum.values().length+"个");

//获取枚举的索引位置，默认从0开始
System.out.println(ColorEnum.red.ordinal());//0
System.out.println(ColorEnum.green.ordinal());//1
System.out.println(ColorEnum.yellow.ordinal());//2
System.out.println(ColorEnum.blue.ordinal());//3

//枚举默认实现了java.lang.Comparable接口
System.out.println(ColorEnum.red.compareTo(ColorEnum.green));//-1

//————————–
System.out.println("===========");
System.err.println("季节为" + SeasonEnum.getSeason());

//————–
System.out.println("===========");
for(Gender gender : Gender.values()){
System.out.println(gender.value);
}

//————–
System.out.println("===========");
for(OrderState order : OrderState.values()){
System.out.println(order.getName());
}
}

}

```

2. 下面的定义也是合法的: 

```java
public enum Day
{
MONDAY, TUESDAT, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY,
}
//或
public enum Day
{
MONDAY, TUESDAT, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY,;
}
//或
public enum Day
{
MONDAY, TUESDAT, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;
}
```

但是当枚举类型有其他定义时，则分号;是必须的 3、声明、使用一个枚举类型:   (1) 在同一个包中: 

```java
public   class  BasicMainClass
{
public   static   void  main(String args[])
{
Day today  =  Day.SATURDAY;
System.out.println( " Today is  "   +  today.toString().toLowerCase());
}
}
```

 (2) 在不同包中: 

```java
import  basic.Day;
public   class  OtherMainClass
{
public   static   void  main(String [] args)
{
Day today  =  Day.SATURDAY;
System.out.println( " Today is  "   +  today.toString().toLowerCase());
}
}
```

4. 枚举类型的性质:  (摘自o'relly 出版的 Java in A Nutshell 5th)
  
Enumerated types have no public constructor. The only instances of an enumerated type are those declared by the enum.
  
Enums are not Cloneable, so copies of the existing instances cannot be created.
  
Enums implement java.io.Serializable so they can be serialized, but the Java serialization mechanism handles them specially to ensure that no new instances are ever created.
  
Instances of an enumerated type are immutable: each enum value retains its identity. (We'll see later in this chapter that you can add your own fields and methods to an enumerated type, which means that you can create enumerated values that have mutable portions. This is not recommended, but does not affect the basic identity of each value.)
  
Instances of an enumerated type are stored in public static final fields of the type itself. Because these fields are final, they cannot be overwritten with inappropriate values: you can't assign the DownloadStatus.ERROR value to the DownloadStatus.DONE field, for example.
  
By convention, the values of enumerated types are written using all capital letters, just as other static final fields are.
  
Because there is a strictly limited set of distinct enumerated values, it is always safe to compare enum values using the = = operator instead of calling the equals() method.
  
Enumerated types do have a working equals( ) method, however. The method uses = =finalso that it cannot be overridden. This working equals( ) method allows enumerated values to be used as members of collections such as Set, List, and Map. internally and is
  
Enumerated types have a working hashCode() method consistent with their equals( )equals(), hashCode( ) is final. It allows enumerated values to be used with classes like java.util.HashMap.method. Like
  
Enumerated types implement java.lang.Comparable, and the compareTo() method orders enumerated values in the order in which they appear in the enum declaration.
  
Enumerated types include a working toString( ) method that returns the name of the enumerated value. For example, DownloadStatus.DONE.toString( ) returns the string "DONE" by default. This method is not final, and enum types can provide a custom implementation if they choose.
  
Enumerated types provide a static valueOf( ) method that does the opposite of the default
  
toString( ) method. For example, DownloadStatus.valueOf("DONE") would return DownloadStatus.DONE.
  
Enumerated types define a final instance method namedordinal()that returns an integer for each enumerated value. The ordinal of an enumerated value represents its position (starting at zero) in the list of value names in the enum declaration. You do not typically need to use the ordinal( ) method, but it is used by a number of enum-related facilities, as described later in the chapter.
  
Each enumerated type defines a static method named values( ) that returns an array of enumerated values of that type. This array contains the complete set of values, in the order they were declared, and is useful for iterating through the complete set of possible values. Because arrays are mutable, the values( ) method always returns a newly created and initialized array.
  
Enumerated types are subclasses of java.lang.Enum, which is new in Java 5.0. (Enum is not itself an enumerated type.) You cannot produce an enumerated type by manually extending the Enum class, and it is a compilation error to attempt this. The only way to define an enumerated type is with the enum keyword.
  
It is not possible to extend an enumerated type. Enumerated types are effectively final, but the final keyword is neither required nor permitted in their declarations. Because enums are effectively final,they may not be abstract.
  
Like classes, enumerated types may implement one or more interfaces.

```java
public class VectorTest {
public static void main(String[] args) {
Vector vector = new Vector();
System.out.println("enter your number:");
int i = 0;
while (true) {
try {
i = System.in.read();
} catch (IOException e) {
}
if (i == 'n' || i == 'r')
break;
else {
int num = i – '0';
vector.addElement(new Integer(num));
}
}
Enumeration en = vector.elements();
int sum = 0;
int c = 0;
while (en.hasMoreElements()) {
Integer b = (Integer) en.nextElement();
c = b.intValue();
System.out.println(c);
sum = sum + c;
}
System.out.println("sum=" + sum);
}
}

```

Enumeration接口
  
Enumeration接口本身不是一个数据结构。但是，对其他数据结构非常重要。 Enumeration接口定义了从一个数据结构得到连续数据的手段。例如，Enumeration定义了一个名为nextElement的方法，可以用来从含有多个元素的数据结构中得到的下一个元素。
  
Enumeration接口提供了一套标准的方法，由于Enumeration是一个接口，它的角色局限于为数据结构提供方法协议。下面是一个使用的例子: 
  
//e is an object that implements the Enumeration interface
  
while (e.hasMoreElements()) {
  
Object o= e.nextElement();
  
System.out.println(o);
  
｝实现该接口的对象由一系列的元素组成，可以连续地调用nextElement()方法来得到 Enumeration枚举对象中的元素。Enumertion接口中仅定义了下面两个方法。
  
·boolean hasMoreElemerts()
  
测试Enumeration枚举对象中是否还含有元素，如果返回true，则表示还含有至少一个的元素。
  
·Object nextElement()
  
如果Bnumeration枚举对象还含有元素，该方法得到对象中的下一个元素。

```java
/*
* @(#)DemoEnumeration.java
* 演示Enumeration接口的使用
* /
import java.util.*;
class DemoEnumeration{
public static void main(String[] args){
//实例化MyDataStruct类型的对象
MyDataStruct mySataStruct=new myDataStruct();
//得到描述myDataStruct类型对象的enumeration对象
Enumeration myEnumeration =myDataStruct.getEnum();
//使用对象循环显示myDataStruct类型的对象中的每一个元素
while (myEnumeration.hasMoreElements())
System.out.println(myEnumeration.nextElement());
}
}

//MyEnumeration类实现Enumeration接口
class MyEnumerator implements Enumeration
{
int count; // 计数器
int length; //存储的数组的长度
object[] dataArray; // 存储数据数组的引用
//构造器
MyEnumeration(int count,int length,object[] dataArray){
this.count = count;
this.length= length;
this.dataArray＝dataArray;
}
public boolean hasMoreElements() {
return (count< length);
}
public Object nextElement() {
return dataArray[count++]；
}
}
//MyDataStruct类用于实例化一个简单的、可以提供enumeration对象
//给使用程序的数据结果对象
class MyDataSttuct
{
String[] data;
// 构造器
MyDataStruct(){
data＝new String[4]
data[0] ="zero"；
data[1]="one"；
data[2] ="two";
data[3]="three";
｝
// 返回一个enumeration对象给使用程序
Enumeration getEnum() {
return new MyEnumeration(0,data.length,data);
｝
```

程序的运行结果为:
  
zero
  
one
  
two
  
three

```java
public enum State {
CREATED(0),
UPDATED(1),
RESOLVED(2);

private final int value;

State(int val) {
this.value = val;
}

public int getValue() {
return value;
}

public static State fromValue(final int value) {

for (State state : State.values()) {
if (value == state.getValue()) {
return state;
}
}
return null;
}
}
```

DK1.5引入了新的类型——枚举。在 Java 中它虽然算个"小"功能，却给我的开发带来了"大"方便。
  
用法一: 常量
  
在JDK1.5 之前，我们定义常量都是:  public static fianl…. 。现在好了，有了枚举，可以把相关的常量分组到一个枚举类型里，而且枚举提供了比常量更多的方法。

```java
public enum Color {
RED, GREEN, BLANK, YELLOW
}

```

2.2 Equality

```java
public final boolean equals(Object other) {
return this==other;
}

public final int hashCode() {
return super.hashCode();
}
```

从以上代码中可以看出，对于枚举值的相等性判断，只需要判断引用是否相等即可。需要注意的是，这是在充分考虑了反射、对象克隆和序列化等诸多因素之后作出的决定。

用法二: switch
  
JDK1.6之前的switch语句只支持int,char,enum类型，使用枚举，能让我们的代码可读性更强。

```java
enum Signal {
GREEN, YELLOW, RED
}
public class TrafficLight {
Signal color = Signal.RED;
public void change() {
switch (color) {
case RED:
color = Signal.GREEN;
break;
case YELLOW:
color = Signal.RED;
break;
case GREEN:
color = Signal.YELLOW;
break;
}
}
}
```

用法三: 向枚举中添加新方法
  
如果打算自定义自己的方法，那么必须在enum实例序列的最后添加一个分号。而且 Java 要求必须先定义 enum 实例。

```java
java代码 收藏代码
public enum Color {
RED("红色", 1), GREEN("绿色", 2), BLANK("白色", 3), YELLO("黄色", 4);
// 成员变量
private String name;
private int index;
// 构造方法
private Color(String name, int index) {
this.name = name;
this.index = index;
}
// 普通方法
public static String getName(int index) {
for (Color c : Color.values()) {
if (c.getIndex() == index) {
return c.name;
}
}
return null;
}
// get set 方法
public String getName() {
return name;
}
public void setName(String name) {
this.name = name;
}
public int getIndex() {
return index;
}
public void setIndex(int index) {
this.index = index;
}
}
```

用法四: 覆盖枚举的方法
  
下面给出一个toString()方法覆盖的例子。

```java
public enum Color {
RED("红色", 1), GREEN("绿色", 2), BLANK("白色", 3), YELLO("黄色", 4);
// 成员变量
private String name;
private int index;
// 构造方法
private Color(String name, int index) {
this.name = name;
this.index = index;
}
//覆盖方法
@Override
public String toString() {
return this.index+"_"+this.name;
}
}
```

用法五: 实现接口
  
所有的枚举都继承自java.lang.Enum类。由于Java 不支持多继承，所以枚举对象不能再继承其他类。

```java
public interface Behaviour {
    void print();

    String getInfo();
}

public enum Color implements Behaviour {
    RED("红色", 1), GREEN("绿色", 2), BLANK("白色", 3), YELLO("黄色", 4);
    // 成员变量
    private String name;
    private int index;

    // 构造方法
    private Color(String name, int index) {
        this.name = name;
        this.index = index;
    }

    //接口方法
    @Override
    public String getInfo() {
        return this.name;
    }

    //接口方法
    @Override
    public void print() {
        System.out.println(this.index + ":" + this.name);
    }
}
```

用法六: 使用接口组织枚举

```java
public interface Food {
enum Coffee implements Food{
BLACK_COFFEE,DECAF_COFFEE,LATTE,CAPPUCCINO
}
enum Dessert implements Food{
FRUIT, CAKE, GELATO
}
}
```

用法七: 关于枚举集合的使用

java.util.EnumSet和java.util.EnumMap是两个枚举集合。EnumSet保证集合中的元素不重复；EnumMap中的key是enum类型，而value则可以是任意类型。关于这个两个集合的使用就不在这里赘述，可以参考JDK文档。
  
关于枚举的实现细节和原理请参考: 
  
参考资料: 《ThinkingInJava》第四版

http://softbeta.iteye.com/blog/1185573
  
http://whitesock.iteye.com/blog/728934
  
http://www.cnblogs.com/linjiqin/archive/2011/02/11/1951632.html https://www.ibm.com/developerworks/cn/java/j-lo-enum/ http://blog.jrwang.me/2016/java-enum/
  
http://outofmemory.cn/code-snippet/1964/java-jiang-string-switch-duiying-meiju-type
  
http://104660.blog.51cto.com/94660/20950
  
http://www.blogjava.net/JafeLee/archive/2007/09/08/143578.html
  
http://blog.csdn.net/ghost1392/article/details/3977106