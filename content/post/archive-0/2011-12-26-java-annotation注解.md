---
title: Java Annotation/注解
author: w1100n
type: post
date: 2011-12-26T05:36:33+00:00
url: /?p=2003
categories:
  - Java

---
http://www.cnblogs.com/mandroid/archive/2011/07/18/2109829.html

Annontation是Java5开始引入的新特征。中文名称一般叫注解。它提供了一种安全的类似注释的机制，用来将任何的信息或元数据(metadata)与程序元素(类、方法、成员变量等)进行关联。

　　更通俗的意思是为程序的元素(类、方法、成员变量)加上更直观更明了的说明，这些说明信息是与程序的业务逻辑无关，并且是供指定的工具或框架使用的。

Annontation像一种修饰符一样，应用于包、类型、构造方法、方法、成员变量、参数及本地变量的声明语句中。

Annotation其实是一种接口。通过Java的反射机制相关的API来访问annotation信息。相关类(框架或工具中的类)根据这些信息来决定如何使用该程序元素或改变它们的行为。

annotation是不会影响程序代码的执行，无论annotation怎么变化，代码都始终如一地执行。

Java语言解释器在工作时会忽略这些annotation，因此在JVM 中这些annotation是"不起作用"的，只能通过配套的工具才能对这些annontaion类型的信息进行访问和处理。

Annotation与interface的异同：

1)、Annotation类型使用关键字@interface而不是interface。

这个关键字声明隐含了一个信息：它是继承了java.lang.annotation.Annotation接口，并非声明了一个interface。

2)、Annotation类型、方法定义是独特的、受限制的。

Annotation 类型的方法必须声明为无参数、无异常抛出的。这些方法定义了annotation的成员：方法名成为了成员名，而方法返回值成为了成员的类型。而方法返回值类型必须为primitive类型、Class类型、枚举类型、annotation类型或者由前面类型之一作为元素的一维数组。方法的后面可以使用 default和一个默认数值来声明成员的默认值，null不能作为成员默认值，这与我们在非annotation类型中定义方法有很大不同。

Annotation类型和它的方法不能使用annotation类型的参数、成员不能是generic。只有返回值类型是Class的方法可以在annotation类型中使用generic，因为此方法能够用类转换将各种类型转换为Class。

3)、Annotation类型又与接口有着近似之处。

它们可以定义常量、静态成员类型(比如枚举类型定义)。Annotation类型也可以如接口一般被实现或者继承。

　　二、应用场合

annotation一般作为一种辅助途径，应用在软件框架或工具中，在这些工具类中根据不同的 annontation注解信息采取不同的处理过程或改变相应程序元素(类、方法及成员变量等)的行为。

例如：Junit、Struts、Spring等流行工具框架中均广泛使用了annontion。使代码的灵活性大提高。

　　三、常见标准的Annotation

从java5版本开始，自带了三种标准annontation类型：

(1) Override

java.lang.Override 是一个marker annotation类型，它被用作标注方法。它说明了被标注的方法重载了父类的方法，起到了断言的作用。如果我们使用了这种annotation在一个没有覆盖父类方法的方法时，java编译器将以一个编译错误来警示。

这个annotaton常常在我们试图覆盖父类方法而确又写错了方法名时加一个保障性的校验过程。

(2) Deprecated

Deprecated也是一种marker annotation。当一个类型或者类型成员使用@Deprecated修饰的话，编译器将不鼓励使用这个被标注的程序元素。所以使用这种修饰具有一定的 "延续性"：如果我们在代码中通过继承或者覆盖的方式使用了这个过时的类型或者成员，虽然继承或者覆盖后的类型或者成员并不是被声明为 @Deprecated，但编译器仍然要报警。

注意：@Deprecated这个annotation类型和javadoc中的 @deprecated这个tag是有区别的：前者是java编译器识别的，而后者是被javadoc工具所识别用来生成文档(包含程序成员为什么已经过时、它应当如何被禁止或者替代的描述)。
  
(3) SuppressWarnings

此注解能告诉Java编译器关闭对类、方法及成员变量的警告。

有时编译时会提出一些警告，对于这些警告有的隐藏着Bug，有的是无法避免的，对于某些不想看到的警告信息，可以通过这个注解来屏蔽。

SuppressWarning不是一个marker annotation。它有一个类型为String[]的成员，这个成员的值为被禁止的警告名。对于javac编译器来讲，被-Xlint选项有效的警告名也同样对@SuppressWarings有效，同时编译器忽略掉无法识别的警告名。

annotation语法允许在annotation名后跟括号，括号中是使用逗号分割的name=value对用于为annotation的成员赋值：

代码：

@SuppressWarnings(value={"unchecked","fallthrough"})
  
public void lintTrap() { /\* sloppy method body omitted \*/ }
  
在这个例子中SuppressWarnings annotation类型只定义了一个单一的成员，所以只有一个简单的value={…}作为name=value对。又由于成员值是一个数组，故使用大括号来声明数组值。

注意：我们可以在下面的情况中缩写annotation：当annotation只有单一成员，并成员命名为"value="。这时可以省去"value="。比如将上面的SuppressWarnings annotation进行缩写：

代码：

@SuppressWarnings({"unchecked","fallthrough"})
  
如果SuppressWarnings所声明的被禁止警告个数为一个时，可以省去大括号：

@SuppressWarnings("unchecked")
  
　　四、自定义annontation示例

示例共涉及四个类：

清单1:Author.java

package com.magc.annotation;
  
import java.lang.annotation.Documented;
  
import java.lang.annotation.ElementType;
  
import java.lang.annotation.Retention;
  
import java.lang.annotation.RetentionPolicy;
  
import java.lang.annotation.Target;
  
/**
  
* 定义作者信息，name和group
  
* @author magc
  
*
  
*/
  
@Retention(RetentionPolicy.RUNTIME)
  
@Target(ElementType.METHOD)
  
@Documented
  
public @interface Author {
  
String name();
  
String group();
  
}
  
清单2:Description.java

/**
  
*
  
*/
  
package com.magc.annotation;
  
import java.lang.annotation.Documented;
  
import java.lang.annotation.ElementType;
  
import java.lang.annotation.Retention;
  
import java.lang.annotation.RetentionPolicy;
  
import java.lang.annotation.Target;
  
/**
  
* @author magc
  
*
  
* 定义描述信息 value
  
*/
  
@Retention(RetentionPolicy.RUNTIME)
  
@Target(ElementType.TYPE)
  
@Documented
  
public @interface Description {
  
String value();
  
}
  
清单3:Utility.java

package com.magc.annotation;
  
@Description(value = "这是一个有用的工具类")
  
public class Utility {
  
@Author(name = "haoran_202″,group="com.magc")
  
public String work()
  
{
  
return "work over!";
  
}
  
}
  
注：这是个普通的Java类，运行了@Description和@Author注解。

清单3:AnalysisAnnotation.java

package com.magc.annotation;
  
import java.lang.reflect.Method;
  
public class AnalysisAnnotation {
  
/**
  
* 在运行时分析处理annotation类型的信息
  
*
  
*
  
*/
  
public static void main(String[] args) {
  
try {
  
//通过运行时反射API获得annotation信息
  
Class rt_class = Class.forName("com.magc.annotation.Utility");
  
Method[] methods = rt_class.getMethods();
  
boolean flag = rt_class.isAnnotationPresent(Description.class);
  
if(flag)
  
{
  
Description description = (Description)rt_class.getAnnotation(Description.class);
  
System.out.println("Utility's Description—>"+description.value());
  
for (Method method : methods) {
  
if(method.isAnnotationPresent(Author.class)) {
  
Author author = (Author)method.getAnnotation(Author.class);
  
System.out.println("Utility's Author—>"+author.name()+" from "+author.group());
  
}
  
}
  
}
  
}
  
catch (ClassNotFoundException e) {
  
e.printStackTrace();
  
}
  
}
  
}
  
注：这是个与自定义@Description和@Author配套的基础框架或工具类，通过此类来获得与普通Java类Utility.java关联的信息,即描述和作者。

运行AnalysisAnnotation,输出结果为：

　　Utility's Description—>这是一个有用的工具类
  
Utility's Author—>haoran_202 from com.magc