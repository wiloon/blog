---
title: 设计模式 — 工厂模式, Factory
author: "-"
date: 2026-04-16T12:12:48+08:00
url: design-pattern-factory
categories:
  - Java
tags:
  - Pattern
  - remix
  - AI-assisted
---
## 设计模式 — 工厂模式, Factory

一、引子
  
话说十年前，有一个老板，他家有三辆汽车 —— Benz奔驰、Bmw宝马、Audi奥迪，还雇了司机为他开车。不过，老板坐车时总是怪怪的: 上Benz车后跟司机说"开奔驰车！"，坐上Bmw后他说"开宝马车！"，坐上Audi说"开奥迪车！"。你一定说: 这人有病！直接说开车不就行了？！
  
而当把这个老板的行为放到我们程序设计中来时，会发现这是一个普遍存在的现象。幸运的是，这种有病的现象在 OO (面向对象) 语言中可以避免了。下面就以 Java 语言为基础来引入我们本文的主题: 工厂模式。

二、分类

工厂模式主要是为创建对象提供过渡接口，以便将创建对象的具体过程屏蔽隔离起来，达到提高灵活性的目的。

工厂模式在《Java与模式》中分为三类:

1) 简单工厂模式 (Simple Factory)

2) 工厂方法模式 (Factory Method)

3) 抽象工厂模式 (Abstract Factory)

这三种模式从上到下逐步抽象，并且更具一般性。
  
GOF在《设计模式》一书中将工厂模式分为两类: 工厂方法模式 (Factory Method) 与抽象工厂模式 (Abstract Factory) 。将简单工厂模式 (Simple Factory) 看为工厂方法模式的一种特例，两者归为一类。
  
两者皆可，在本文使用《Java与模式》的分类方法。下面来看看这些工厂模式是怎么来"治病"的。

## 简单工厂模式, 简单工厂 (Simple Factory)
  
简单工厂模式又称静态工厂方法模式。从命名上就可以看出这个模式一定很简单。它存在的目的很简单: 定义一个用于创建对象的接口。
  
先来看看它的组成:
  
1) 工厂类角色: 这是本模式的核心，含有一定的业务逻辑和判断逻辑。在 java 中它往往由一个具体类实现。
  
2) 抽象产品角色: 它一般是具体产品继承的父类或者实现的接口。在 java 中由接口或者抽象类来实现。
  
3) 具体产品角色: 工厂类所创建的对象就是此角色的实例。在 java 中由一个具体类实现。
  
来用类图来清晰的表示下的它们之间的关系 (如果对类图不太了解，请参考我关于类图的文章) :

那么简单工厂模式怎么来使用呢？我们就以简单工厂模式来改造老板坐车的方式——现在老板只需要坐在车里对司机说句: "开车"就可以了。

```java
// 抽象产品
interface Car {
    void drive();
}

// 具体产品
class Benze implements Car {
    public void drive() {
        System.out.println("Driving Benz");
    }
}

// 具体产品
class Bmw implements Car {
    public void drive() {
        System.out.println("Driving Bmw");
    }
}

// 工厂类
class Driver {
    // 工厂方法，注意返回类型为抽象产品
    public static Car createCar(String s) throws Exception {
        // 判断逻辑，返回具体的产品角色给 Client
        if (s.equalsIgnoreCase("Benz")) {
            return new Benze();
        } else if (s.equalsIgnoreCase("Bmw")) {
            return new Bmw();
        } else {
            throw new Exception();
        }
    }
}

// 客户端
public class Magnate {
    public static void main(String[] args) throws Exception {
        // 告诉司机我今天坐奔驰
        Car car = Driver.createCar("benz");
        // 下命令: 开车
        car.drive();

        car = Driver.createCar("bmw");
        car.drive();
    }
}
```

将本程序空缺的其他信息填充完整后即可运行。如果你将所有的类放在一个文件中，请不要忘记只能有一个类被声明为public。本程序在jdk1.4 下运行通过。
  
程序中各个类的关系表达如下:

这便是简单工厂模式了。怎么样，使用起来很简单吧？那么它带来了什么好处呢？
  
首先，使用了简单工厂模式后，我们的程序不在"有病"，更加符合现实中的情况；而且客户端免除了直接创建产品对象的责任，而仅仅负责"消费"产品 (正如老板所为) 。
  
下面我们从[开闭原则](/open-closed-principle) (对扩展开放；对修改封闭) 上来分析下简单工厂模式。

**产品部分符合开闭原则。** 当老板增加了一辆新车时，只要这辆车实现了 `Car` 接口（即符合接口这份"合同"），新车类本身就可以独立存在，不需要修改任何已有的产品类。

**但工厂部分违反了开闭原则。** 新车要能被客户端使用，还必须修改 `Driver.createCar()` 方法，在 `if/else` 判断链里追加一个分支，让工厂"认识"这辆新车：

```java
if (s.equalsIgnoreCase("Benz")) {
    return new Benze();
} else if (s.equalsIgnoreCase("Bmw")) {
    return new Bmw();
} else if (s.equalsIgnoreCase("Audi")) {  // 每新增一种车都要改这里
    return new Audi();
}
```

这就是"对修改不封闭"——每增加一种产品，都要打开工厂类修改代码。

随着车型不断增加，`Driver` 类需要了解所有车型的创建细节，承担了过多的职责，这样的类在设计模式中称为**上帝类（God Class）**——什么都管、什么都知道，最终变得难以维护。这也违反了[单一职责原则](/solid-principles)（一个类只应承担一个职责）。

工厂方法模式的解决思路是：把 `createCar()` 抽象成接口，每种车对应一个专属的工厂类（`BenzeDriver` 只负责创建 Benz，`BmwDriver` 只负责创建 Bmw）。新增车型时只需新增一个工厂类，无需修改任何已有代码。

我们举的例子是最简单的情况，而在实际应用中，产品往往是一个多层次的树状结构，工厂类需要处理的情况会更多，上帝的负担也就越来越重。
  
于是工厂方法模式作为救世主出现了。

## 工厂方法模式, 工厂方法 (Factory Method)

"Factory Method"中的 **method**，指的是抽象工厂接口里声明的那个创建方法——在本文的例子中就是 `Driver` 接口里的 `createCar()`。模式的核心思想是：把"创建哪种对象"这个决定，推迟到子类通过重写这个方法来实现。`BenzeDriver` 重写它返回 `Benz`，`BmwDriver` 重写它返回 `Bmw`——每个子类只负责自己那一种产品。

工厂方法模式去掉了简单工厂模式中工厂方法的静态属性，使得它可以被子类继承。这样在简单工厂模式里集中在工厂方法上的压力可以由工厂方法模式里不同的工厂子类来分担。
  
你应该大致猜出了工厂方法模式的结构，来看下它的组成:
  
1) 抽象工厂角色:  这是工厂方法模式的核心，它与应用程序无关。是具体工厂角色必须实现的接口或者必须继承的父类。在java中它由抽象类或者接口来实现。
  
2) 具体工厂角色: 它含有和具体业务逻辑有关的代码。由应用程序调用以创建对应的具体产品的对象。
  
3) 抽象产品角色: 它是具体产品继承的父类或者是实现的接口。在java中一般有抽象类或者接口来实现。
  
4) 具体产品角色: 具体工厂角色所创建的对象就是此角色的实例。在java中由具体的类来实现。
  
用类图来清晰的表示下的它们之间的关系:

工厂方法模式使用继承自抽象工厂角色的多个子类来代替简单工厂模式中的"上帝类"。正如上面所说，这样便分担了对象承受的压力；而且这样使得结构变得灵活起来——当有新的产品 (即老板的汽车) 产生时，只要按照抽象产品角色、抽象工厂角色提供的合同来生成，那么就可以被客户使用，而不必去修改任何已有的代码。可以看出工厂角色的结构也是符合开闭原则的！
  
我们还是老规矩，使用一个完整的例子来看看工厂模式各个角色之间是如何来协调的。话说老板生意越做越大，自己的爱车也越来越多。这可苦了那位司机师傅了，什么车它都要记得，维护，都要经过他来使用！于是老板同情他说: 看你跟我这么多年的份上，以后你不用这么辛苦了，我给你分配几个人手，你只管管好他们就行了！于是，工厂方法模式的管理出现了。代码如下:

```java
// 抽象产品
interface Car {
    void drive();
}

// 具体产品
class Benz implements Car {
    public void drive() {
        System.out.println("Driving Benz");
    }
}

// 具体产品
class Bmw implements Car {
    public void drive() {
        System.out.println("Driving Bmw");
    }
}

// 抽象工厂
interface Driver {
    Car createCar();
}

// 具体工厂
class BenzeDriver implements Driver {
    public Car createCar() {
        return new Benz();
    }
}

// 具体工厂
class BmwDriver implements Driver {
    public Car createCar() {
        return new Bmw();
    }
}

// 客户端
public class Magnate {
    public static void main(String[] args) {
        Driver driver = new BenzeDriver();
        Car car = driver.createCar();
        car.drive();

        driver = new BmwDriver();
        car = driver.createCar();
        car.drive();
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

## Effective Java: Item 1

> Consider static factory methods instead of constructors（用静态工厂方法代替构造函数）

《Effective Java》第一条建议：创建对象时，优先考虑静态工厂方法，而不是直接暴露构造函数。这与简单工厂模式的思路一脉相承——通过一个有语义的静态方法来封装对象的创建细节，例如 `Boolean.valueOf(true)` 比 `new Boolean(true)` 更清晰、更高效。

静态工厂方法的优点：

1. **有名字**，方法名可以描述返回对象的含义（构造函数名只能是类名）
1. **不必每次都创建新对象**，可以缓存或复用实例
1. **可以返回子类对象**，调用方只依赖接口，不感知具体实现类
1. **参数相同但含义不同时**，可以用不同方法名区分，而构造函数做不到

[http://www.wiloon.com/?p=4407](http://www.wiloon.com/?p=4407)

[http://blog.csdn.net/ai92/article/details/209198](http://blog.csdn.net/ai92/article/details/209198)

    持续改进，抽象工厂也反射
  
[http://www.wiloon.com/?p=4447&embed=true#?secret=K8dbXXCWWd](http://www.wiloon.com/?p=4447&embed=true#?secret=K8dbXXCWWd)

    抽象工厂模式解析例子
  
[http://www.wiloon.com/?p=4407&embed=true#?secret=dFCXQ3viP4](http://www.wiloon.com/?p=4407&embed=true#?secret=dFCXQ3viP4)
