---
title: static factory method
author: "-"
date: 2012-03-26T03:37:05+00:00
url: /?p=2626
categories:
  - Development
tags:
  - Java

---
## static factory method
创建类的实例的最常见的方式是用new语句调用类的构造方法。在这种情况下，程序可以创建类的任意多个实例，每执行一条new语句，都会导致Java虚拟机的堆区中产生一个新的对象。假如类需要进一步封装创建自身实例的细节，并且控制自身实例的数目，那么可以提供静态工厂方法。

例如Class实例是Java虚拟机在加载一个类时自动创建的，程序无法用new语句创建java.lang.Class类的实例，因为Class类没有提供public类型的构造方法。为了使程序能获得代表某个类的Class实例，在Class类中提供了静态工厂方法forName(String name)，它的使用方式如下: 

Class c=Class.forName( "Sample "); //返回代表Sample类的实例

静态工厂方法与用new语句调用的构造方法相比，有以下区别。

 (1) 构造方法的名字必须与类名相同。这一特性的优点是符合Java语言的规范，缺点是类的所有重载的构造方法的名字都相同，不能从名字上区分每个重载方法，容易引起混淆。

静态工厂方法的方法名可以是任意的，这一特性的优点是可以提高程序代码的可读性，在方法名中能体现与实例有关的信息。例如例程11-5的Gender类有两个静态工厂方法: getFemale()和getMale()。

例程11-5 Gender.java

public class Gender{

private String description;

private static final Gender female=new Gender( "女 ");

private static final Gender male=new Gender( "男 ");

private Gender(String description){this.description=description;}

public static Gender getFemale(){

return female;

}

public static Gender getMale(){

return male;

}

public String getDescription(){return description;}

}

这一特性的缺点是与其他的静态方法没有明显的区别，使用户难以识别类中到底哪些静态方法专门负责返回类的实例。为了减少这一缺点带来的负面影响，可以在为静态工厂方法命名时尽量遵守约定俗成的规范，当然这不是必需的。目前比较流行的规范是把静态工厂方法命名为valueOf或者getInstance。

l valueOf: 该方法返回的实例与它的参数具有同样的值，例如: 

Integer a=Integer.valueOf(100); //返回取值为100的Integer对象

从上面代码可以看出，valueOf()方法能执行类型转换操作，在本例中，把int类型的基本数据转换为Integer对象。

l getInstance: 返回的实例与参数匹配，例如: 

//返回符合中国标准的日历

Calendar cal=Calendar.getInstance(Locale.CHINA);

 (2) 每次执行new语句时，都会创建一个新的对象。而静态工厂方法每次被调用的时候，是否会创建一个新的对象完全取决于方法的实现。

 (3) new语句只能创建当前类的实例，而静态工厂方法可以返回当前类的子类的实例，这一特性可以在创建松耦合的系统接口时发挥作用，参见本章11.3.5节 (松耦合的系统接口) 。

静态工厂方法最主要的特点是: 每次被调用的时候，不一定要创建一个新的对象。利用这一特点，静态工厂方法可用来创建以下类的实例。

l 单例类: 只有惟一的实例的类。

l 枚举类: 实例的数量有限的类。

l 具有实例缓存的类: 能把已经创建的实例暂且存放在缓存中的类。

l 具有实例缓存的不可变类: 不可变类的实例一旦创建，其属性值就不会被改变。

在下面几节，将结合具体的例子，介绍静态工厂方法的用途。

11.3.1 单例 (singleton) 类
  
单例类是指仅有一个实例的类。在系统中具有惟一性的组件可作为单例类，这种类的实例通常会占用较多的内存，或者实例的初始化过程比较冗长，因此随意创建这些类的实例会影响系统的性能。

Tips

熟悉Struts和Hibernate软件的读者会发现，Struts框架的ActionServlet类就是单例类，此外，Hibernate的SessionFactory和Configuration类也是单例类。

例程11-6的GlobalConfig类就是个单例类，它用来存放软件系统的配置信息。这些配置信息本来存放在配置文件中，在GlobalConfig类的构造方法中会从配置文件中读取配置信息，并把它存放在properties属性中。

例程11-6 GlobalConfig.java

import java.io.InputStream;

import java.io.FileInputStream;

import java.io.IOException;

import java.util.Properties;

public class GlobalConfig {

private static final GlobalConfig INSTANCE=new GlobalConfig();

private Properties properties = new Properies();

private GlobalConfig(){

try{

//加载配置信息

InputStream in=getClass().getResourceAsStream( "myapp.properties ");

properties.load(in);

in.close();

}catch(IOException e){throw new RuntimeException( "加载配置信息失败 ");}

}

public static GlobalConfig getInstance(){ //静态工厂方法

return INSTANCE;

}

public Properties getProperties() {

return properties;

}

}

实现单例类有两种方式: 

 (1) 把构造方法定义为private类型，提供public static final类型的静态变量，该变量引用类的惟一的实例，例如: 

public class GlobalConfig {

public static final GlobalConfig INSTANCE =new GlobalConfig();

private GlobalConfig() {…}

…

}

这种方式的优点是实现起来比较简捷，而且类的成员声明清楚地表明该类是单例类。

 (2) 把构造方法定义为private类型，提供public static类型的静态工厂方法，例如: 

public class GlobalConfig {

private static final GlobalConfig INSTANCE =new GlobalConfig();

private GlobalConfig() {…

}

public static GlobalConfig getInstance(){return INSTANCE;}

…

}

这种方式的优点是可以更灵活地决定如何创建类的实例，在不改变GlobalConfig类的接口的前提下，可以修改静态工厂方法getInstance()的实现方式，比如把单例类改为针对每个线程分配一个实例，参见例程11-7。

例程11-7 GlobalConfig.java

package uselocal;

public class GlobalConfig {

private static final ThreadLocal <globalConfig> threadConfig=

new ThreadLocal <globalConfig> ();

private Properties properties = null;

private GlobalConfig(){…}

public static GlobalConfig getInstance(){

GlobalConfig config=threadConfig.get();

if(config==null){

config=new GlobalConfig();

threadConfig.set(config);

}

return config;

}

public Properties getProperties() {return properties; }

}

以上程序用到了ThreadLocal类，关于它的用法参见第13章的13.14节 (ThreadLocal类) 。

-
  
静态工厂方法是一种将类的运用者和产生着隔离的设计模式，它是一种创造型模式，但是它不属于23种基本设计模式中的一种，它是理解抽象工厂的基础，当然它自身也有用途，这里不说了。
  
一般我们在运用到一个实例的时候就会用new关键字来实例化这个对象。
  
例如说我们写一个A类，当我们应用调用A的时候就会用A a=new A();来创建实例。当我们的应用这样实现的时候就会出现这个应用着不但承担了类应用的任务而且还承担了类构建的任务。这样从职责的分配上就重合了，违背面向对象的思想。所以我们需要写一个专门类B去构建A类，这个B类就是构建着。
  
当然由于静态工厂所用的都是静态方法，所以有其局限性，但是java有一种很好的机制去解决一些局限性，再经过一些改良和其它模式的融入可以达到非常好的构建效果，这种机制就是反射。