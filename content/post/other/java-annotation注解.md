---
title: Annotation/注解
author: "-"
date: 2011-12-26T05:36:33+00:00
url: annotation
categories:
  - Java
tags:$
  - reprint
---
## Annotation/注解
# annotation
http://www.cnblogs.com/mandroid/archive/2011/07/18/2109829.html

annotation 是Java5开始引入的新特征。中文名称一般叫注解。它提供了一种安全的类似注释的机制，用来将任何的信息或元数据(metadata)与程序元素(类、方法、成员变量等)进行关联。

更通俗的意思是为程序的元素(类、方法、成员变量)加上更直观更明了的说明，这些说明信息是与程序的业务逻辑无关，并且是供指定的工具或框架使用的。

annotation 像一种修饰符一样，应用于包、类型、构造方法、方法、成员变量、参数及本地变量的声明语句中。

Annotation其实是一种接口。通过Java的反射机制相关的API来访问annotation信息。相关类(框架或工具中的类)根据这些信息来决定如何使用该程序元素或改变它们的行为。

annotation是不会影响程序代码的执行，无论annotation怎么变化，代码都始终如一地执行。

Java语言解释器在工作时会忽略这些annotation，因此在JVM 中这些annotation是"不起作用"的，只能通过配套的工具才能对这些 annotation 类型的信息进行访问和处理。

### Annotation 与interface的异同
1. Annotation类型使用关键字@interface而不是interface。
这个关键字声明隐含了一个信息: 它是继承了java.lang.annotation.Annotation接口，并非声明了一个interface。

2. Annotation类型、方法定义是独特的、受限制的。
Annotation 类型的方法必须声明为无参数、无异常抛出的。这些方法定义了annotation的成员: 方法名成为了成员名，而方法返回值成为了成员的类型。方法返回值类型必须为primitive类型、Class类型、枚举类型、annotation类型或者由前面类型之一作为元素的一维数组。方法的后面可以使用 default 和一个默认数值来声明成员的默认值，null 不能作为成员默认值，这与我们在非 annotation 类型中定义方法有很大不同。

Annotation 类型和它的方法不能使用 annotation 类型的参数、成员不能是 generic。只有返回值类型是Class的方法可以在annotation类型中使用generic，因为此方法能够用类转换将各种类型转换为Class。

3. Annotation类型又与接口有着近似之处。
它们可以定义常量、静态成员类型(比如枚举类型定义)。Annotation类型也可以如接口一般被实现或者继承。

### 应用场合
annotation一般作为一种辅助途径，应用在软件框架或工具中，在这些工具类中根据不同的 annotation 注解信息采取不同的处理过程或改变相应程序元素(类、方法及成员变量等)的行为。

例如: Junit、Struts、Spring等流行工具框架中均广泛使用了 annotation 。使代码的灵活性大提高。

### 常见标准的Annotation
从java5版本开始，自带了三种标准 annotation 类型: 

1. Override
java.lang.Override 是一个marker annotation类型，它被用作标注方法。它说明了被标注的方法重载了父类的方法，起到了断言的作用。如果我们使用了这种annotation在一个没有覆盖父类方法的方法时，java编译器将以一个编译错误来警示。

这个annotaton常常在我们试图覆盖父类方法而确又写错了方法名时加一个保障性的校验过程。

2. Deprecated
Deprecated也是一种marker annotation。当一个类型或者类型成员使用@Deprecated修饰的话，编译器将不鼓励使用这个被标注的程序元素。所以使用这种修饰具有一定的 "延续性": 如果我们在代码中通过继承或者覆盖的方式使用了这个过时的类型或者成员，虽然继承或者覆盖后的类型或者成员并不是被声明为 @Deprecated，但编译器仍然要报警。

注意: @Deprecated这个annotation类型和javadoc中的 @deprecated这个tag是有区别的: 前者是java编译器识别的，而后者是被javadoc工具所识别用来生成文档(包含程序成员为什么已经过时、它应当如何被禁止或者替代的描述)。
  
3. SuppressWarnings
此注解能告诉Java编译器关闭对类、方法及成员变量的警告。

有时编译时会提出一些警告，对于这些警告有的隐藏着Bug，有的是无法避免的，对于某些不想看到的警告信息，可以通过这个注解来屏蔽。

SuppressWarning不是一个marker annotation。它有一个类型为String[]的成员，这个成员的值为被禁止的警告名。对于javac编译器来讲，被-Xlint选项有效的警告名也同样对@SuppressWarings有效，同时编译器忽略掉无法识别的警告名。

annotation语法允许在annotation名后跟括号，括号中是使用逗号分割的name=value对用于为annotation的成员赋值: 

代码: 

@SuppressWarnings(value={"unchecked","fallthrough"})
  
public void lintTrap() { /* sloppy method body omitted */ }
  
在这个例子中SuppressWarnings annotation 类型只定义了一个单一的成员，所以只有一个简单的value={…}作为name=value对。又由于成员值是一个数组，故使用大括号来声明数组值。

注意: 我们可以在下面的情况中缩写annotation: 当annotation只有单一成员，并成员命名为"value="。这时可以省去"value="。比如将上面的SuppressWarnings annotation进行缩写: 
```java
@SuppressWarnings({"unchecked","fallthrough"})
```
如果SuppressWarnings所声明的被禁止警告个数为一个时，可以省去大括号: 
```java
@SuppressWarnings("unchecked")
```

### @Documented
@Documented 的目的就是让这一个Annotation类型的信息能够显示在 javaAPI说明文档上;没有添加的话，使用javadoc生成API文档的时候就会找不到这一个类型生成的信息.
### @Target
@Target里面的ElementType是用来指定Annotation类型可以用在哪一些元素上的.说明一下: TYPE(类型), FIELD(属性), METHOD(方法), PARAMETER(参数), CONSTRUCTOR(构造函数),LOCAL_VARIABLE(局部变量), ANNOTATION_TYPE,PACKAGE(包),其中的TYPE(类型)是指可以用在Class,Interface,Enum和Annotation类型上.

### @Retention
注解@Retention可以用来修饰注解，是注解的注解，称为元注解。
Retention注解有一个属性value，是RetentionPolicy类型的，Enum RetentionPolicy是一个枚举类型，
这个枚举决定了Retention注解应该如何去保持，也可理解为Rentention 搭配 RententionPolicy使用。RetentionPolicy有3个值: CLASS  RUNTIME   SOURCE
按生命周期来划分可分为3类: 
1. RetentionPolicy.SOURCE: 注解只保留在源文件，当Java文件编译成class文件的时候，注解被遗弃；
2. RetentionPolicy.CLASS: 注解被保留到class文件，但jvm加载class文件时候被遗弃，这是默认的生命周期；
3. RetentionPolicy.RUNTIME: 注解不仅被保存到class文件中，jvm加载class文件之后，仍然存在；
这3个生命周期分别对应于: Java源文件(.java文件) ---> .class文件 ---> 内存中的字节码。
那怎么来选择合适的注解生命周期呢？
首先要明确生命周期长度 SOURCE < CLASS < RUNTIME ，所以前者能作用的地方后者一定也能作用。
一般如果需要在运行时去动态获取注解信息，那只能用 RUNTIME 注解，比如@Deprecated使用RUNTIME注解
如果要在编译时进行一些预处理操作，比如生成一些辅助代码 (如 ButterKnife) ，就用 CLASS注解；
如果只是做一些检查性的操作，比如 @Override 和 @SuppressWarnings，使用SOURCE 注解。

注解@Override用在方法上，当我们想重写一个方法时，在方法上加@Override，当我们方法的名字出错时，编译器就会报错
注解@Deprecated，用来表示某个类或属性或方法已经过时，不想别人再用时，在属性和方法上用@Deprecated修饰
注解@SuppressWarnings用来压制程序中出来的警告，比如在没有用泛型或是方法已经过时的时候

### @Inherited
在Spring Boot中大量使用了@Inherited注解。我们来了解一下这个注解的用法，注解的源码: 

复制代码
package java.lang.annotation;

/**
 * Indicates that an annotation type is automatically inherited.  If
 * an Inherited meta-annotation is present on an annotation type
 * declaration, and the user queries the annotation type on a class
 * declaration, and the class declaration has no annotation for this type,
 * then the class's superclass will automatically be queried for the
 * annotation type.  This process will be repeated until an annotation for this
 * type is found, or the top of the class hierarchy (Object)
 * is reached.  If no superclass has an annotation for this type, then
 * the query will indicate that the class in question has no such annotation.
 *
 * <p>Note that this meta-annotation type has no effect if the annotated
 * type is used to annotate anything other than a class.  Note also
 * that this meta-annotation only causes annotations to be inherited
 * from superclasses; annotations on implemented interfaces have no
 * effect.
 *
 * @author  Joshua Bloch
 * @since 1.5
 * @jls 9.6.3.3 @Inherited
 */
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.ANNOTATION_TYPE)
public @interface Inherited {
}
复制代码
注解的作用: 

当某个注解类在它的类上定义了@Inherited注解，例如SpringBoot中的 @SpringBootApplication注解，@SpringBootApplication注解类就定义了@Inherited注解，看下源码中的红色部分: 

复制代码
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
        @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
        @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {

  // .....省略

}
复制代码
那么现在有一个我们自己开发的类使用了这个注解，例如: 

@SpringBootApplication
@Service
public class Person {

}
然后有个类Employee继承了Person

public class Employee extends Person{

}
那么现在在判断Employee类上有没有@SpringBootApplication时，通过代码验证: 

复制代码
@Test
    public void test1(){
        
        Class clazz = Employee.class ;
        if(clazz.isAnnotationPresent(SpringBootApplication.class)){
            System.out.println("true");     
        }
        
    }
复制代码
上面这个测试用例执行将输出true，也就是子类中能查找到@SpringBootApplication ，但同样，你用上述代码查找Employee类上是否有Spring的@Service注解时，会输出false，至此你应该明白@Inherited注解的用意了吧。

经过这样的分析，我们再来读一下JDK的文档，就会比较容易理解了，否则会觉的有些绕，下面列出 @interface注解的中文文档: 

指示注释类型被自动继承。如果在注释类型声明中存在 Inherited 元注释，并且用户在某一类声明中查询该注释类型，同时该类声明中没有此类型的注释，则将在该类的超类中自动查询该注释类型。此过程会重复进行，直到找到此类型的注释或到达了该类层次结构的顶层 (Object) 为止。如果没有超类具有该类型的注释，则查询将指示当前类没有这样的注释。

注意，如果使用注释类型注释类以外的任何事物，此元注释类型都是无效的。还要注意，此元注释仅促成从超类继承注释；对已实现接口的注释无效。



转自: 
http://blog.csdn.net/liuwenbo0920/article/details/7290586
http://blog.csdn.net/github_35180164/article/details/52118286

### 自定义 annotation 示例
示例共涉及四个类: 

#### Author.java
```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Documented
public @interface Author {
    String name();

    String group();
}
```
#### Description.java
```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
public @interface Description {
    String value();
}
```
#### Utility.java
```java
@Description(value = "这是一个有用的工具类")
public class Utility {
    @Author(name = "wiloon", group = "com.wiloon")
    public String work() {
        return "work over!";
    }
}
```
注: 这是个普通的Java类，运行了@Description和@Author注解。

### AnalysisAnnotation.java
```java
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
```
注: 这是个与自定义@Description和@Author配套的基础框架或工具类，通过此类来获得与普通Java类Utility.java关联的信息,即描述和作者。

运行AnalysisAnnotation,输出结果为: 

Utility's Description—>这是一个有用的工具类
  
Utility's Author—>haoran_202 from com.magc



  注解 (Annotation)  为我们在代码中添加信息提供了一种形式化的方法，是我们可以在稍后 某个时刻方便地使用这些数据 (通过 解析注解 来使用这些数据) 。

注解的语法比较简单，除了@符号的使用以外，它基本上与java的固有语法一致，java内置了三种

注解，定义在java.lang包中。

@Override 表示当前方法是覆盖父类的方法。

@Deprecated 表示当前元素是不赞成使用的。

@SuppressWarnings 表示关闭一些不当的编译器警告信息。

下面是一个定义注解的实例
  
```java
  
package com.wiloon.test.annotation;

import java.lang.annotation.Documented;
  
import java.lang.annotation.Inherited;
  
import java.lang.annotation.Retention;
  
import java.lang.annotation.Target;
  
import java.lang.annotation.ElementType;
  
import java.lang.annotation.RetentionPolicy;

/*
   
* 元注解@Target,@Retention,@Documented,@Inherited
   
*
   
* @Target 表示该注解用于什么地方，可能的 ElemenetType 参数包括: 
   
* ElemenetType.CONSTRUCTOR 构造器声明
   
* ElemenetType.FIELD 域声明 (包括 enum 实例) 
   
* ElemenetType.LOCAL_VARIABLE 局部变量声明
   
* ElemenetType.METHOD 方法声明
   
* ElemenetType.PACKAGE 包声明
   
* ElemenetType.PARAMETER 参数声明
   
* ElemenetType.TYPE 类，接口 (包括注解类型) 或enum声明
   
*
   
* @Retention 表示在什么级别保存该注解信息。可选的 RetentionPolicy 参数包括: 
   
* RetentionPolicy.SOURCE 注解将被编译器丢弃
   
* RetentionPolicy.CLASS 注解在class文件中可用，但会被VM丢弃
   
* RetentionPolicy.RUNTIME VM将在运行期也保留注释，因此可以通过反射机制读取注解的信息。
   
*
   
* @Documented 将此注解包含在 javadoc 中
   
*
   
* @Inherited 允许子类继承父类中的注解
   
*
   
*/
  
@Target(ElementType.METHOD)
  
@Retention(RetentionPolicy.RUNTIME)
  
@Documented
  
@Inherited
  
/*
   
* 定义注解 Test 注解中含有两个元素 id 和 description description 元素 有默认值 "no description"
   
*/
  
public @interface Test {
      
public int id();

public String description() default "no description";
  
}
  
```

下面是一个使用注解 和 解析注解的实例
  
```java
  
package com.wiloon.test.annotation;

import java.lang.reflect.Method;

public class Test_1 {
      
/*
       
* 被注解的三个方法
       
*/
      
@Test(id = 1, description = "hello method_1")
      
public void method_1() {
      
}

@Test(id = 2)
      
public void method_2() {
      
}

@Test(id = 3, description = "last method")
      
public void method_3() {
      
}

/*
       
* 解析注解，将Test_1类 所有被注解方法 的信息打印出来
       
*/
      
public static void main(String[] args) {
      
Method[] methods = Test_1.class.getDeclaredMethods();
      
for (Method method : methods) {
          
/*
           
* 判断方法中是否有指定注解类型的注解
           
*/
          
boolean hasAnnotation = method.isAnnotationPresent(Test.class);
          
if (hasAnnotation) {
          
/*
           
* 根据注解类型返回方法的指定类型注解
           
*/
          
Test annotation = method.getAnnotation(Test.class);
          
System.out.println("Test( method = " + method.getName() + " , id = "
              
+ annotation.id() + " , description = " + annotation.description() + " )");
          
}
      
}
      
}

}
  
```
  
输出结果如下: 

Test( method = method_1 , id = 1 , description = hello method_1 )
  
Test( method = method_2 , id = 2 , description = no description )
  
Test( method = method_3 , id = 3 , description = last method )

第一部分:了解一下java1.5起默认的三个annotation类型:
  
一个是@Override:只能用在方法之上的，用来告诉别人这一个方法是改写父类的。
  
一个是@Deprecated:建议别人不要使用旧的API的时候用的,编译的时候会用产生警告信息,可以设定在程序里的所有的元素上.
  
一个是@SuppressWarnings:这一个类型可以来暂时把一些警告信息消息关闭.
  
如果不清楚上面三个类型的具体用法，各位可以google一下的,很简单的。

第二部分:讲一下annotation的概念先，再来讲一下怎样设计自己的annotation.
  
首先在jdk自带的java.lang.annotation包里,打开如下几个源文件:

1. 源文件Target.java
  
```java
  
@Documented
  
@Retention(RetentionPolicy.RUNTIME)
  
@Target(ElementType.ANNOTATION_TYPE)
  
public @interface Target {
  
    ElementType[] value();
  
}
  
```

其中的@interface是一个关键字，在设计annotations的时候必须把一个类型定义为@interface，而不能用class或interface关键字(会不会觉得sun有点吝啬,偏偏搞得与interface这么像).

2. 源文件Retention.java
  
```java
  
@Documented
  
@Retention(RetentionPolicy.RUNTIME)
  
@Target(ElementType.ANNOTATION_TYPE)
  
public @interface Retention {
  
   RetentionPolicy value();
  
}
  
```

看到这里，大家可能都模糊了,都不知道在说什么，别急，往下看一下.
  
在上面的文件都用到了RetentionPolicy，ElementType这两个字段,你可能就会猜到这是两个java文件.的确，这两个文件的源代码如下: 

3. 源文件RetentionPolicy.java
  
```java
  
public enum RetentionPolicy {
  
SOURCE,
  
CLASS,
  
RUNTIME
  
}
  
```

这是一个enum类型,共有三个值，分别是SOURCE,CLASS 和 RUNTIME.
  
SOURCE代表的是这个Annotation类型的信息只会保留在程序源码里，源码如果经过了编译之后，Annotation的数据就会消失,并不会保留在编译好的.class文件里面。
  
ClASS的意思是这个Annotation类型的信息保留在程序源码里,同时也会保留在编译好的.class文件里面,在执行的时候，并不会把这一些信息加载到虚拟机(JVM)中去.注意一下，当你没有设定一个Annotation类型的Retention值时，系统默认值是CLASS.
  
第三个,是RUNTIME,表示在源码、编译好的.class文件中保留信息，在执行的时候会把这一些信息加载到JVM中去的．
  
举一个例子，如@Override里面的Retention设为SOURCE,编译成功了就不要这一些检查的信息;相反,@Deprecated里面的 Retention设为RUNTIME,表示除了在编译时会警告我们使用了哪个被Deprecated的方法,在执行的时候也可以查出该方法是否被 Deprecated.

4. 源文件ElementType.java
  
```java
  
public enum ElementType {
  
TYPE, FIELD, METHOD, PARAMETER, CONSTRUCTOR,
  
LOCAL_VARIABLE, ANNOTATION_TYPE,PACKAGE
  
}
  
```

＠Target里面的ElementType是用来指定Annotation类型可以用在哪一些元素上的.说明一下: TYPE(类型), FIELD(属性), METHOD(方法), PARAMETER(参数), CONSTRUCTOR(构造函数),LOCAL_VARIABLE(局部变量), ANNOTATION_TYPE,PACKAGE(包),其中的TYPE(类型)是指可以用在Class,Interface,Enum和 Annotation类型上.
  
另外,从1的源代码可以看出,@Target自己也用了自己来声明自己,只能用在ANNOTATION_TYPE之上.
  
如果一个Annotation类型没有指明@Target使用在哪些元素上,那么它可以使用在任何元素之上,这里的元素指的是上面的八种类型.
  
举几个正确的例子:
  
@Target(ElementType.METHOD)
  
@Target(value=ElementType.METHOD)
  
@Target(ElementType.METHOD,ElementType.CONSTRUCTOR)
  
具体参考一下javadoc文档

上面一下1和2的源文件，它们都使用了@Documented,
  
另外一点，如果需要把Annotation的数据继承给子类，那么就会用到@Inherited这一个Annotation类型.

第三部分:下面讲的设计一个最简单的Annotation例子,这一例子共用四个文件;
  
1. Description.java
  
```java
  
package lighter.javaeye.com;

import java.lang.annotation.Documented;
  
import java.lang.annotation.ElementType;
  
import java.lang.annotation.Retention;
  
import java.lang.annotation.RetentionPolicy;
  
import java.lang.annotation.Target;

@Target(ElementType.TYPE)
  
@Retention(RetentionPolicy.RUNTIME)
  
@Documented
  
public @interface Description {
  
String value();
  
}
  
```

说明:所有的Annotation会自动继承java.lang.annotation这一个接口,所以不能再去继承别的类或是接口.
  
最重要的一点,Annotation类型里面的参数该怎么设定:
  
第一,只能用public或默认(default)这两个访问权修饰.例如,String value();这里把方法设为defaul默认类型.
  
第二,参数成员只能用基本类型byte,short,char,int,long,float,double,boolean八种基本数据类型和 String,Enum,Class,annotations等数据类型,以及这一些类型的数组.例如,String value();这里的参数成员就为String.
  
第三,如果只有一个参数成员,最好把参数名称设为"value",后加小括号.例:上面的例子就只有一个参数成员.

2. Name.java
  
```java
  
package lighter.javaeye.com;

import java.lang.annotation.Documented;
  
import java.lang.annotation.ElementType;
  
import java.lang.annotation.Retention;
  
import java.lang.annotation.RetentionPolicy;
  
import java.lang.annotation.Target;

//注意这里的@Target与@Description里的不同,参数成员也不同
  
@Target(ElementType.METHOD)
  
@Retention(RetentionPolicy.RUNTIME)
  
@Documented
  
public @interface Name {
  
String originate();
  
String community();
  
}
  
```

3. JavaEyer.java
  
```java
  
package lighter.javaeye.com;

@Description("javaeye,做最棒的软件开发交流社区")
  
public class JavaEyer {
  
@Name(originate="创始人:robbin",community="javaEye")
  
public String getName()
  
{
  
return null;
  
}

@Name(originate="创始人:江南白衣",community="springside")
  
public String getName2()
  
{
  
return "借用两位的id一用,写这一个例子,请见谅!";
  
}
  
}
  
```

4. 最后，写一个可以运行提取JavaEyer信息的类TestAnnotation
  
```java
  
package lighter.javaeye.com;

import java.lang.reflect.Method;
  
import java.util.HashSet;
  
import java.util.Set;

public class TestAnnotation {
  
/**
  
* author lighter
  
* 说明:具体关天Annotation的API的用法请参见javaDoc文档
  
*/
  
public static void main(String[] args) throws Exception {
  
String  CLASS_NAME = "lighter.javaeye.com.JavaEyer";
  
Class  test = Class.forName(CLASS_NAME);
  
Method[] method = test.getMethods();
  
boolean flag = test.isAnnotationPresent(Description.class);
  
if(flag)
  
{
  
Description des = (Description)test.getAnnotation(Description.class);
  
System.out.println("描述:"+des.value());
  
System.out.println("------");
  
}

//把JavaEyer这一类有利用到@Name的全部方法保存到Set中去
  
Set<Method> set = new HashSet<Method>();
  
for(int i=0;i<method.length;i++)
  
{
  
boolean otherFlag = method[i].isAnnotationPresent(Name.class);
  
if(otherFlag) set.add(method[i]);
  
}
  
for(Method m: set)
  
{
  
Name name = m.getAnnotation(Name.class);
  
System.out.println(name.originate());
  
System.out.println("创建的社区:"+name.community());
  
}
  
}
  
}
  
```

5. 运行结果: 
  
描述:javaeye,做最棒的软件开发交流社区
  
------
  
创始人:robbin
  
创建的社区:javaEye
  
创始人:江南白衣
  
创建的社区:springside

Java注解(Annotation)
  
Annotation(注释)是JDK5.0及以后版本引入的。它可以用于创建文档，跟踪代码中的依赖性，甚至执行基本编译时检查。注释是以'@注释名'在代码中存在的，根据注释参数的个数，我们可以将注释分为: 标记注释、单值注释、完整注释三类。它们都不会直接影响到程序的语义，只是作为注释 (标识) 存在，我们可以通过反射机制编程实现对这些元数据的访问。另外，你可以在编译时选择代码里的注释是否只存在于源代码级，或者它也能在class文件中出现。
  
元数据的作用
  
如果要对于元数据的作用进行分类，目前还没有明确的定义，不过我们可以根据它所起的作用，大致可分为三类: 
  
编写文档: 通过代码里标识的元数据生成文档。
  
代码分析: 通过代码里标识的元数据对代码进行分析。
  
编译检查: 通过代码里标识的元数据让编译器能实现基本的编译检查。
  
1. 基本内置注释
  
@Override
  
```java
  
package com.iwtxokhtd.annotation;
  
/**
  
* 测试Override注解
  
* @author Administrator
  
*
  
*/
  
public class OverrideDemoTest {

//@Override
  
public String tostring(){
  
return "测试注释";
  
}
  
}
  
```
  
@Deprecated的作用是对不应该在使用的方法添加注释，当编程人员使用这些方法时，将会在编译时显示提示信息，它与javadoc里的@deprecated标记有相同的功能，准确的说，它还不如javadoc @deprecated，因为它不支持参数，使用@Deprecated的示例代码示例如下: 
  
```java
  
package com.iwtxokhtd.annotation;
  
/**
  
* 测试Deprecated注解
  
* @author Administrator
  
*
  
*/
  
public class DeprecatedDemoTest {
  
public static void main(String[] args) {
  
//使用DeprecatedClass里声明被过时的方法
  
DeprecatedClass.DeprecatedMethod();
  
}
  
}
  
class DeprecatedClass{
  
@Deprecated
  
public static void DeprecatedMethod() {
  
}
  
}
  
```
  
@SuppressWarnings,其参数有: 
  
deprecation，使用了过时的类或方法时的警告
  
unchecked，执行了未检查的转换时的警告
  
fallthrough，当 Switch 程序块直接通往下一种情况而没有 Break 时的警告
  
path，在类路径、源文件路径等中有不存在的路径时的警告
  
serial，当在可序列化的类上缺少 serialVersionUID 定义时的警告
  
finally ，任何 finally 子句不能正常完成时的警告
  
all，关于以上所有情况的警告
  
```java
  
package com.iwtxokhtd.annotation;
  
import java.util.ArrayList;
  
import java.util.List;
  
public class SuppressWarningsDemoTest {
  
public static List list=new ArrayList();
  
@SuppressWarnings("unchecked")
  
public void add(String data){
  
list.add(data);
  
}
  
}
  
```
  
2. 自定义注释
  
它类似于新创建一个接口类文件，但为了区分，我们需要将它声明为@interface,如下例: 
  
```java
  
package com.iwtxokhtd.annotation;
  
public @interface NewAnnotation {
  
}
  
```
  
使用自定义的注释类型
  
```java
  
package com.iwtxokhtd.annotation;
  
public class AnnotationTest {
  
@NewAnnotation
  
public static void main(String[] args) {
  
}
  
}
  
```
  
为自定义注释添加变量
  
```java
  
package com.iwtxokhtd.annotation;
  
public @interface NewAnnotation {
  
String value();
  
}
  
```
  
```java
  
public class AnnotationTest {
  
@NewAnnotation("main method")
  
public static void main(String[] args) {
  
saying();
  
}
  
@NewAnnotation(value = "say method")
  
public static void saying() {
  
}
  
}
  
```
  
定义一个枚举类型，然后将参数设置为该枚举类型，并赋予默认值
  
```java
  
public @interface Greeting {
  
public enum FontColor {
  
BLUE, RED, GREEN
  
};
  
String name();
  
FontColor fontColor() default FontColor.RED;
  
}
  
```
  
这里有两种选择，其实变数也就是在赋予默认值的参数上，我们可以选择使用该默认值，也可以重新设置一个值来替换默认值
  
```java
  
public class AnnotationTest {
  
@NewAnnotation("main method")
  
public static void main(String[] args) {
  
saying();
  
sayHelloWithDefaultFontColor();
  
sayHelloWithRedFontColor();
  
}

@NewAnnotation("say method")
  
public static void saying() {
  
}

// 此时的fontColor为默认的RED
  
@Greeting(name = "defaultfontcolor")
  
public static void sayHelloWithDefaultFontColor() {
  
}

// 现在将fontColor改为BLUE
  
@Greeting(name = "notdefault", fontColor = Greeting.FontColor.BLUE)
  
public static void sayHelloWithRedFontColor() {
  
}
  
}
  
```
  
3. 注释的高级应用
  
3.1. 限制注释的使用范围
  
用@Target指定ElementType属性
  
```java
  
package java.lang.annotation;
  
public enum ElementType {
  
TYPE,
  
// 用于类，接口，枚举但不能是注释
  
FIELD,
  
// 字段上，包括枚举值
  
METHOD,
  
// 方法，不包括构造方法
  
PARAMETER,
  
// 方法的参数
  
CONSTRUCTOR,
  
//构造方法
  
LOCAL_VARIABLE,
  
// 本地变量或catch语句
  
ANNOTATION_TYPE,
  
// 注释类型(无数据)
  
PACKAGE
  
// Java包
  
}
  
```
  
3.2. 注解保持性策略
  
```java
  
//限制注解使用范围
  
@Target({ElementType.METHOD,ElementType.CONSTRUCTOR})
  
public @interface Greeting {
  
//使用枚举类型
  
public enum FontColor{
  
BLUE,RED,GREEN
  
};
  
String name();
  
FontColor fontColor() default FontColor.RED;
  
}
  
```
  
在Java编译器编译时，它会识别在源代码里添加的注释是否还会保留，这就是RetentionPolicy。下面是Java定义的RetentionPolicy枚举: 
  
编译器的处理有三种策略: 
  
将注释保留在编译后的类文件中，并在第一次加载类时读取它
  
将注释保留在编译后的类文件中，但是在运行时忽略它
  
按照规定使用注释，但是并不将它保留到编译后的类文件中

```java
  
package java.lang.annotation;
  
public enum RetentionPolicy {
  
SOURCE,
  
// 此类型会被编译器丢弃
  
CLASS,
  
// 此类型注释会保留在class文件中，但JVM会忽略它
  
RUNTIME
  
// 此类型注释会保留在class文件中，JVM会读取它
  
}
  
Java代码
  
//让保持性策略为运行时态，即将注解编码到class文件中，让虚拟机读取
  
@Retention(RetentionPolicy.RUNTIME)
  
public @interface Greeting {
  
//使用枚举类型
  
public enum FontColor{
  
BLUE,RED,GREEN
  
};
  
String name();
  
FontColor fontColor() default FontColor.RED;
  
}
  
```

3.3. 文档化功能
  
Java提供的Documented元注释跟Javadoc的作用是差不多的，其实它存在的好处是开发人员可以定制Javadoc不支持的文档属性，并在开发中应用。它的使用跟前两个也是一样的，简单代码示例如下: 
  
```java
  
//让它定制文档化功能
  
//使用此注解时必须设置RetentionPolicy为RUNTIME
  
@Documented
  
public @interface Greeting {
  
//使用枚举类型
  
public enum FontColor{
  
BLUE,RED,GREEN
  
};
  
String name();
  
FontColor fontColor() default FontColor.RED;
  
}
  
```

3.4. 标注继承
  
```java
  
//让它允许继承，可作用到子类
  
@Inherited
  
public @interface Greeting {

//使用枚举类型
  
public enum FontColor{
  
BLUE,RED,GREEN
  
};
  
String name();
  
FontColor fontColor() default FontColor.RED;
  
}
  
```

4. 读取注解信息
  
属于重点，在系统中用到注解权限时非常有用，可以精确控制权限的粒度
  
注意:  要想使用反射去读取注解，必须将Retention的值选为Runtime
  
```java
  
package com.iwtxokhtd.annotation;
  
import java.lang.annotation.Annotation;
  
import java.lang.reflect.Method;
  
//读取注解信息
  
public class ReadAnnotationInfoTest {
  
public static void main(String[] args) throws Exception {
  
// 测试AnnotationTest类，得到此类的类对象
  
Class c = Class.forName("com.iwtxokhtd.annotation.AnnotationTest");
  
// 获取该类所有声明的方法
  
Method[] methods = c.getDeclaredMethods();
  
// 声明注解集合
  
Annotation[] annotations;
  
// 遍历所有的方法得到各方法上面的注解信息
  
for (Method method : methods) {
  
// 获取每个方法上面所声明的所有注解信息
  
annotations = method.getDeclaredAnnotations();
  
// 再遍历所有的注解，打印其基本信息
  
System.out.println(method.getName());
  
for (Annotation an : annotations) {
  
System.out.println("方法名为: " + method.getName() + " 其上面的注解为: "
  
+ an.annotationType().getSimpleName());
  
Method[] meths = an.annotationType().getDeclaredMethods();
  
// 遍历每个注解的所有变量
  
for (Method meth : meths) {
  
System.out.println("注解的变量名为: " + meth.getName());
  
}
  
}
  
}
  
}
  
}
  
```

---


https://www.cnblogs.com/hzhuxin/p/7799899.html

