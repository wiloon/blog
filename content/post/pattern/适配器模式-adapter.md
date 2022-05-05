---
title: 适配器模式 Adapter
author: "-"
date: 2012-10-18T07:55:56+00:00
url: Adapter
categories:
  - Pattern
tags:
  - reprint
---
## 适配器模式 Adapter

通常，客户类 (clients of class) 通过类的接口访问它提供的服务。有时，现有的类 (existing class) 可以提供客户类的功能需要，但是它所提供的接口不一定是客户类所期望的。这是由于现有的接口太详细或者缺乏详细或接口的名称与客户类所查找的不同等诸多不同原因导致的。

在这种情况下，现有的接口需要转化 (convert) 为客户类期望的接口，这样保证了对现有类的重用。如果不进行这样的转化，客户类就不能利用现有类所提供的功能。适配器模式 (Adapter Pattern) 可以完成这样的转化。适配器模式建议定义一个包装类，包装有不兼容接口的对象。这个包装类指的就是适配器 (Adapter) ，它包装的对象就是适配者(Adaptee)。适配器提供客户类需要的接口，适配器接口的实现是把客户类的请求转化为对适配者的相应接口的调用。换句话说: 当客户类调用适配器的方法时，在适配器类的内部调用适配者类的方法，这个过程对客户类是透明的，客户类并不直接访问适配者类。因此，适配器可以使由于借口不兼容而不能交互的类可以一起工作 (work together) 。

在上面讨论的接口:

 (1)     不是指在JAVA编程语言中接口的概念，虽然类的接口可以通过JAVA借扩来定义。

 (2)     不是指由窗体和GUI控件所组成的GUI应用程序的用户接口。

 (3)     而是指类所报漏的，被其他类调用的编程接口，

类适配器 (Class Adapter) VS对象适配器(Object Adapter)

适配器总体上可以分为两类??类适配器 (Class Adapter) VS对象适配器(Object Adapter)

#### 类适配器

类适配器是通过继承类适配者类 (Adaptee Class) 实现的，另外类适配器实现客户类所需要的接口。当客户对象调用适配器类方法的时候，适配器内部调用它所继承的适配者的方法。

#### 对象适配器

对象适配器包含一个适配器者的引用 (reference) ，与类适配器相同，对象适配器也实现了客户类需要的接口。当客户对象调用对象适配器的方法的时候，对象适配器调它所包含的适配器者实例的适当方法。

下表是类适配器 (Class Adapter) 和对象适配器(Object Adapter)的详细不同:

  <img src="http://image.tianjimedia.com/imagelist/05/10/b6z1pomi30yn.bmp" alt="" />

补充:

类适配器 (Class Adapter)     对象适配器(Object Adapter)

基于继承概念    利用对象合成

只能应用在适配者是接口，不能利用它子类的接口，当类适配器建立时，它就静态地与适配者关联    可以应用在适配者是接口和它的所有子类，因为适配器是作为适配者的子类，所以适配器可能会重载适配者的一些行为。

注意: 在JAVA中，子类不能重载父类中声明为final的方法。    不能重载适配者的方法。

注意:字面上，不能重栽只是因为没有继承。但是适配器提供包装方法可以按需要改变行为。

客户类对适配者中声明为public的接口是可见的，    客户类和适配者是完全不关联的，只有适配器才能感知适配者接口。

在JAVA应用程序中:

适用于期待的接口是JAVA接口的形式，而不是抽象地或具体地类的形式。这是因为JAVA编程语言只允许单继承。因此，类适配器设计成适配者的子类。    在JAVA应用程序中:
  
适用于当客户对象期望的接口是抽象类的形式，同时也可以应用于期望接口是Java接口的形式。

```java
  
package com.designpatterns.adapter;


/**

* 目标角色, 相当于我们的应用程序, sampleOperation1是我们开放给客户的接口

* @author suki

*/

public interface Target {

public void sampleOperation1();

}


/**

* 源角色,相当于第三方库

* @author suki

*/

public class Adaptee {

public Adaptee() {

}


public void sampleOperation2()

{

System.out.println("Adaptee.sampleOperation2()");

}

}


/**

* 适配器角色

* 把第三方库的接口sampleOperation2转化为我们开放给客户的接口sampleOperation1

\* \* @author suki

*/

public class Adapter extends Adaptee implements Target {

public void sampleOperation1() {

this.sampleOperation2();

}

}


/**

* 客户端类

* @author suki

*/

public class Client {

public static void main(String[] args) {

Adaptee adaptee = new Adaptee();

Target target = new Adapter();

target.sampleOperation1();

}

}
  
  
```

对象的适配器模式

在类的适配器模式中Adapter采用继承的方式复用Adaptee的接口，而在对象的适配器模式中Adapter则采用组合的方式实现Adaptee的复用
  
```java
  
package com.designpatterns.adapterofobject;


/**

 * 目标角色, 相当于我们的应用程序, sampleOperation1是我们开放给客户的接口

* @author suki

*/

public interface Target {

public void sampleOperation1();

}

/**

 * 源角色,相当于第三方库

* @author suki

*/

public class Adaptee {

public Adaptee() {

}


public void sampleOperation2() {

System.out.println("Adaptee.sampleOperation2()");

}

}


/**

 * 适配器角色

 * 把第三方库的接口sampleOperation2转化为我们开放给客户的接口sampleOperation1

* @author suki

*/

public class Adapter implements Target {

private Adaptee adaptee;

public Adapter(Adaptee adaptee)

{

super();

this.adaptee = adaptee;

}

public void sampleOperation1() {

adaptee.sampleOperation2();

}

}


/**

 * 客户端类

* @author suki

*/

public class Client {

public static void main(String[] args) {

Adaptee adaptee = new Adaptee();

Target target = new Adapter(adaptee);

target.sampleOperation1();

}

}
  
 
  
```
