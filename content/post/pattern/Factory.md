---
title: 设计模式 — 工厂模式, Factory
author: "-"
date: 2011-10-29T06:32:38+00:00
url: Factory
categories:
  - Java
tags:
  - DesignPattern
---
## 设计模式 — 工厂模式, Factory

一、引子
  
话说十年前，有一个暴发户，他家有三辆汽车——Benz奔驰、Bmw宝马、Audi奥迪，还雇了司机为他开车。不过，暴发户坐车时总是怪怪的: 上Benz车后跟司机说"开奔驰车！"，坐上Bmw后他说"开宝马车！"，坐上Audi说"开奥迪车！"。你一定说: 这人有病！直接说开车不就行了？！
  
而当把这个暴发户的行为放到我们程序设计中来时，会发现这是一个普遍存在的现象。幸运的是，这种有病的现象在OO (面向对象) 语言中可以避免了。下面就以Java语言为基础来引入我们本文的主题: 工厂模式。

二、分类
  
工厂模式主要是为创建对象提供过渡接口，以便将创建对象的具体过程屏蔽隔离起来，达到提高灵活性的目的。
  
工厂模式在《Java与模式》中分为三类:
  
1) 简单工厂模式 (Simple Factory)
  
2) 工厂方法模式 (Factory Method)
  
3) 抽象工厂模式 (Abstract Factory)
  
这三种模式从上到下逐步抽象，并且更具一般性。
  
GOF在《设计模式》一书中将工厂模式分为两类: 工厂方法模式 (Factory Method) 与抽象工厂模式 (Abstract Factory) 。将简单工厂模式 (Simple Factory) 看为工厂方法模式的一种特例，两者归为一类。
  
两者皆可，在本文使用《Java与模式》的分类方法。下面来看看这些工厂模式是怎么来"治病"的。

三、简单工厂模式
  
简单工厂模式又称静态工厂方法模式。从命名上就可以看出这个模式一定很简单。它存在的目的很简单: 定义一个用于创建对象的接口。
  
先来看看它的组成:
  
1) 工厂类角色: 这是本模式的核心，含有一定的业务逻辑和判断逻辑。在java中它往往由一个具体类实现。
  
2) 抽象产品角色: 它一般是具体产品继承的父类或者实现的接口。在java中由接口或者抽象类来实现。
  
3) 具体产品角色: 工厂类所创建的对象就是此角色的实例。在java中由一个具体类实现。
  
来用类图来清晰的表示下的它们之间的关系 (如果对类图不太了解，请参考我关于类图的文章) :

那么简单工厂模式怎么来使用呢？我们就以简单工厂模式来改造暴发户坐车的方式——现在暴发户只需要坐在车里对司机说句: "开车"就可以了。

```java
  
//抽象产品
  
interface Car {
   
public void drive();
  
}

//具体产品
  
class Benze implements Car {
   
public void drive() {
   
System.out.println("Driving Benz");
   
}
  
}

//具体产品
  
class Bmw implements Car {
   
public void drive() {
   
System.out.println("Driving Bmw");
   
}
  
}

//工厂类
  
class Driver {
   
//工厂方法.注意 返回类型为抽象产品
   
public static Car driverCar(String s) throws Exception {
   
//判断逻辑，返回具体的产品角色给Client
   
if (s.equalsIgnoreCase("Benz"))
   
return new Benze();
   
else if (s.equalsIgnoreCase("Bmw"))
   
return new Bmw();
   
else throw new Exception();
   
}
  
}

//欢迎暴发户出场......
  
public class Magnate {
   
public static void main(String[] args) throws Exception {
   
//告诉司机我今天坐奔驰
   
Car car = Driver.driverCar("benz");
   
//下命令: 开车
   
car.drive();
   
car = Driver.driverCar("bmw");
   
car.drive();
   
}
  
}
  
```

将本程序空缺的其他信息填充完整后即可运行。如果你将所有的类放在一个文件中，请不要忘记只能有一个类被声明为public。本程序在jdk1.4 下运行通过。
  
程序中各个类的关系表达如下:

这便是简单工厂模式了。怎么样，使用起来很简单吧？那么它带来了什么好处呢？
  
首先，使用了简单工厂模式后，我们的程序不在"有病"，更加符合现实中的情况；而且客户端免除了直接创建产品对象的责任，而仅仅负责"消费"产品 (正如暴发户所为) 。
  
下面我们从开闭原则 (对扩展开放；对修改封闭) 上来分析下简单工厂模式。当暴发户增加了一辆车的时候，只要符合抽象产品制定的合同，那么只要通知工厂类知道就可以被客户使用了。所以对产品部分来说，它是符合开闭原则的；但是工厂部分好像不太理想，因为每增加一辆车，都要在工厂类中增加相应的业务逻辑或者判断逻辑，这显然是违背开闭原则的。可想而知对于新产品的加入，工厂类是很被动的。对于这样的工厂类 (在我们的例子中是司机师傅) ，我们称它为全能类或者上帝类(God Class)。
  
我们举的例子是最简单的情况，而在实际应用中，很可能产品是一个多层次的树状结构。由于简单工厂模式中只有一个工厂类来对应这些产品，所以这可能会把我们的上帝累坏了，也累坏了我们这些程序员:(
  
于是工厂方法模式作为救世主出现了。

**四、工厂方法模式**
  
工厂方法模式去掉了简单工厂模式中工厂方法的静态属性，使得它可以被子类继承。这样在简单工厂模式里集中在工厂方法上的压力可以由工厂方法模式里不同的工厂子类来分担。
  
你应该大致猜出了工厂方法模式的结构，来看下它的组成:
  
1) 抽象工厂角色:  这是工厂方法模式的核心，它与应用程序无关。是具体工厂角色必须实现的接口或者必须继承的父类。在java中它由抽象类或者接口来实现。
  
2) 具体工厂角色: 它含有和具体业务逻辑有关的代码。由应用程序调用以创建对应的具体产品的对象。
  
3) 抽象产品角色: 它是具体产品继承的父类或者是实现的接口。在java中一般有抽象类或者接口来实现。
  
4) 具体产品角色: 具体工厂角色所创建的对象就是此角色的实例。在java中由具体的类来实现。
  
用类图来清晰的表示下的它们之间的关系:

工厂方法模式使用继承自抽象工厂角色的多个子类来代替简单工厂模式中的"上帝类"。正如上面所说，这样便分担了对象承受的压力；而且这样使得结构变得灵活起来——当有新的产品 (即暴发户的汽车) 产生时，只要按照抽象产品角色、抽象工厂角色提供的合同来生成，那么就可以被客户使用，而不必去修改任何已有的代码。可以看出工厂角色的结构也是符合开闭原则的！
  
我们还是老规矩，使用一个完整的例子来看看工厂模式各个角色之间是如何来协调的。话说暴发户生意越做越大，自己的爱车也越来越多。这可苦了那位司机师傅了，什么车它都要记得，维护，都要经过他来使用！于是暴发户同情他说: 看你跟我这么多年的份上，以后你不用这么辛苦了，我给你分配几个人手，你只管管好他们就行了！于是，工厂方法模式的管理出现了。代码如下:

```java
  
public class Magnate {
   
public static void main(String[] args) {
   
Driver driver = new BenzeDriver();
   
Car car = driver.driverCar();
   
car.drive();
   
driver = new BmwDriver();
   
car = driver.driverCar();
   
car.drive();
   
}
  
}

//抽象产品
  
interface Car {
   
public void drive();
  
}

//具体产品
  
class Benz implements Car {
   
public void drive() {
   
System.out.println("Driving Benz");
   
}
  
}

//具体产品
  
class Bmw implements Car {
   
public void drive() {
   
System.out.println("Driving Bmw");
   
}
  
}

//抽象工厂
  
interface Driver {
   
public Car driverCar();
  
}

//具体工厂
  
class BenzeDriver implements Driver {
   
public Car driverCar() {
   
return new Benz();
   
}
  
}

//具体工厂
  
class BmwDriver implements Driver {
   
public Car driverCar() {
   
return new Bmw();
   
}
  
}
  
```

可以看出工厂方法的加入，使得对象的数量成倍增长。当产品种类非常多时，会出现大量的与之对应的工厂对象，这不是我们所希望的。因为如果不能避免这种情况，可以考虑使用简单工厂模式与工厂方法模式相结合的方式来减少工厂类: 即对于产品树上类似的种类 (一般是树的叶子中互为兄弟的) 使用简单工厂模式来实现。

五、小结
  
工厂方法模式仿佛已经很完美的对对象的创建进行了包装，使得客户程序中仅仅处理抽象产品角色提供的接口。那我们是否一定要在代码中遍布工厂呢？大可不必。也许在下面情况下你可以考虑使用工厂方法模式:
  
1) 当客户程序不需要知道要使用对象的创建过程。
  
2) 客户程序使用的对象存在变动的可能，或者根本就不知道使用哪一个具体的对象。

简单工厂模式与工厂方法模式真正的避免了代码的改动了？没有。在简单工厂模式中，新产品的加入要修改工厂角色中的判断语句；而在工厂方法模式中，要么将判断逻辑留在抽象工厂角色中，要么在客户程序中将具体工厂角色写死 (就象上面的例子一样) 。而且产品对象创建条件的改变必然会引起工厂角色的修改。
  
面对这种情况，Java的反射机制与配置文件的巧妙结合突破了限制——这在Spring中完美的体现了出来。

**六、抽象工厂模式**
  
先来认识下什么是产品族:  位于不同产品等级结构中，功能相关联的产品组成的家族。还是让我们用一个例子来形象地说明一下吧。

图中的BmwCar和BenzCar就是两个产品树 (产品层次结构) ；而如图所示的BenzSportsCar和BmwSportsCar就是一个产品族。他们都可以放到跑车家族中，因此功能有所关联。同理BmwBussinessCar和BenzSportsCar也是一个产品族。
  
回到抽象工厂模式的话题上。
  
可以说，抽象工厂模式和工厂方法模式的区别就在于需要创建对象的复杂程度上。而且抽象工厂模式是三个里面最为抽象、最具一般性的。
  
抽象工厂模式的用意为: 给客户端提供一个接口，可以创建多个产品族中的产品对象
  
而且使用抽象工厂模式还要满足一下条件:
  
1) 系统中有多个产品族，而系统一次只可能消费其中一族产品。
  
2) 同属于同一个产品族的产品以其使用。
  
来看看抽象工厂模式的各个角色 (和工厂方法的如出一辙) :
  
1) 抽象工厂角色:  这是工厂方法模式的核心，它与应用程序无关。是具体工厂角色必须实现的接口或者必须继承的父类。在java中它由抽象类或者接口来实现。
  
2) 具体工厂角色: 它含有和具体业务逻辑有关的代码。由应用程序调用以创建对应的具体产品的对象。在java中它由具体的类来实现。
  
3) 抽象产品角色: 它是具体产品继承的父类或者是实现的接口。在java中一般有抽象类或者接口来实现。
  
4) 具体产品角色: 具体工厂角色所创建的对象就是此角色的实例。在java中由具体的类来实现。
  
类图如下:

看过了前两个模式，对这个模式各个角色之间的协调情况应该心里有个数了，我就不举具体的例子了。只是一定要注意满足使用抽象工厂模式的条件哦。

<http://www.wiloon.com/?p=4407>

<http://blog.csdn.net/ai92/article/details/209198>

    持续改进，抽象工厂也反射
  
<http://www.wiloon.com/?p=4447&embed=true#?secret=K8dbXXCWWd>

    抽象工厂模式解析例子
  
<http://www.wiloon.com/?p=4407&embed=true#?secret=dFCXQ3viP4>