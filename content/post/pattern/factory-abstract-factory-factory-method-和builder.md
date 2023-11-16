---
title: Factory, Abstract Factory, Factory Method, 和Builder
author: "-"
date: 2012-10-11T06:53:48+00:00
url: /?p=4430
categories:
  - Java
tags:
  - DesignPattern

---
## Factory, Abstract Factory, Factory Method, 和Builder
选这4个模式在一起讨论首先是因为它们的功能比较类似，都是用来制造对象实例的，从归类来说，他们都属于制造类模式(creational patterns)，其次她们们在工作中比较常用，由于功能太过相似，往往导致在某个实际问题上让人举棋不定，似乎选哪个都可以解决问题，可是真的选择某个模式后，又会发现不是完全合适。今天我们就来讨论讨论在什么情况下选择什么模式来解决问题比较合适。

考虑到不是所有的朋友都对以上提到的4种模式都了如指掌，在开始讨论之前先简单的介绍一下这4个模式，对这4种模式熟悉的朋友也可以顺便回顾一下。请注意，这里我只会做简短的介绍，如果要比较深入地了解她们的话，还请去看模式相关的书籍，比较浅显易懂的我推荐 "Head First Design Patterns"。如果要在工作中反复参考的我推荐 "Applied Java Patterns"。那本经典的GOF Design Patterns由于写的时间比较早，举的例子不太适合现在的软件开发，我个人认为初学者或者是没有太多时间的朋友没有必要去读那本书，尽管她的确是经典。

**Factory Pattern**

中文叫工厂模式, 这个是我们在面向对象编程中最常用的模式之一了，她的主要功能就是制造对象，也正是这个原因才叫她为工厂模式，工厂干什么？生产产品。通常情况而言某个工厂所生产的产品总是一个系列的不同种类，大体上相同，细节上有差异。

图1 展示了一个非常简单的例子，通常CarFactory类会提供下列方法来生产车辆, 如代码片断1所示: 

public class CarFactory {

public Car createBusinessCar() {….}

public Car createSportCar() {…}

}

代码片断 1

http://www.wiloon.com/wp-content/uploads/2012/10/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBeu5PDT5UndtcNdt48rY80PV_fd8Ce5pLpHavAj520cgRoVa4EmOhjE5VNS7GnBHl126UUuSSCrcM8YMFLVb3mp_UsivKRLJ1HKESriM5FDQA-1.gif

图1 Factory Pattern

**Abstract Factory Pattern**

中文叫抽象工厂模式，顾名思义，就是把工厂模式在进一步抽象化，进一步细化。我们继续沿用上面的例子，不过这次增加产品的种类，如图2所示。由于我们增加了一层分类，当我们要生产某种车的时候就需要询问要哪种车, 商用还是跑车？不然的话就要增加create方法，如果分类多了，create方法就会成几何数量增长。

public class CarFactory {

public Car createBusinessBMWCar() {….}

public Car createBusinessBenzCar() {…}

public Car createSportBMWCar() {….}

public Car createSportBenzCar() {…}

}

代码片断 2

![][2]

图2 bad Factory Pattern

从面向对象的角度来讲，不是很好的解决方法，需要进一步抽象。结果就是把CarFactory进行抽象，然后针对不同品牌的车产生不同的工厂。 如图3

![][3]

图3 Abstract Factory Pattern

这个时候每个工厂类仍然只需要2个方法，如代码片断1所示，用户会在不同需要的情况下得到不同的工厂对象，进而生产出需要的Car。不论这里工厂类如何实现，客户端的代码可以始终不变，类似这样: getCarFactory().createBusinessCar()。

以上两个模式多用于: 

1 。 客户端需要依赖制造对象的细节。
  
1. 一系列类似的对象需要被制造出来。
  
3.      同种对象不同实体需要在不同的地点不同是时间被制造出来。

**Factory Method Pattern**

中文叫工厂方法模式， 通常是用于当某个类的功能主要是针对生产出来的对象提供一些相关服务，而且这些对象有共同的接口，至于对象具体是什么，留给她的子类来决定。这样解释起来比较晦涩难懂，我们还是沿用生产汽车的例子，不过不再用工厂，而是改用销售部门，因为销售部门主要为生产出来的车提供相关服务的，比方说，折扣，售后服务等等。代码如代码片断3 所示, 这里CarStore是个抽象类，如何生产需要的车将由子类来进一步实现， 比方说BMWStore就会生产出BMW。图4展示了相关的UML图, 总体看起来图4和图3非常相似， 但是从实现原理和实际应用上来说两者是完全不同的， 图3 Abstract Factory是针对Interface的多种不同的实现，具体使用的

时候是"组和"，用英语术语表达就是"composition"。 而图4 Factory Method是子类对抽象父类继承，进而实现父类的抽象方法， 具体使用的时候是"继承"， 用英语术语表达就是"inheritance"。 也就是很多OO书里说谈到的"is a? or has a?"的问题， composition指的就是has a, 而inheritance指的就是is a。

public abstract class CarStore {

// Factory method

protected abstract Car createBusinessCar();

protected abstract Car createSportCar();

public void sell() {

createBusinessCar();

discount(…);

....

}

public double discount(Customer customer) {….}

public void service() {…}

}

代码片断 3

这个模式多半会和另一个模式Template Method一起使用，事实上代码片断3中方法sell() 就是template Method。具体关于template method pattern的详细讲解已不属于本文的讨论主题 ，感兴趣的朋友请看相关书籍。

![][4]

图4 Factory Method

**Builder Pattern**

中文叫生成器模式，我觉得叫构造模式更贴切，通常用于提供尽可能简单的接口来生成比较复杂的对象，这个复杂的对象通常包含有很多其他的对象。有些人认为Builder和Factory Method很相似，有时候是可以互换的，这样理解是错误的。这两个模式的侧重点是不同的，Builder侧重的是构造复杂对象，而且经常是使用到composite模式; Factory Method侧重的是生产各种各样不同的对象，这些对象通常都是比较简单的，一般而言，Factory Method不会和composite联合使用。总的来说这两个模式是相辅相成的，决不能视为同类。具体原因我会在讨论中加以阐述。图5 展示了Builder概念图。

![][5]

图5 Builder Pattern

考虑到使用composite模式，我们使用另外一个例子，做饭，比较简单，常见，人人都做过，解释起来应该比较好懂。我们先定义好"食品"是对所有吃的物品的概括，做好的炸酱面是食品，煮好的面条是食品，做好的酱是食品，做酱用的料也是食品。当我们去餐馆叫吃炸酱面时，我们只希望要一碗做好的炸酱面， 我们可不会希望对小二说煮面，切黄瓜丝，打鸡蛋，剁肉末，熬酱，等等。我们只希望说: "小二，来碗炸酱面。" 这时候就需要用到builder,  builder会提供一个简单的方法createNoodleWithSource() — 做炸酱面，当顾客点吃炸酱面后，builder就会在内部制造一系列的食品，比方说，煮面，切黄瓜丝，打鸡蛋，剁肉末，熬酱，等等。而这些细节，作为顾客是不需要费心的。

**讨论**

4种模式都已经简要的介绍完了，到这里大家应该对她们有了大概地了解。从根本上来说，每一个模式都不难理解，真正困难的是选择，在什么情况下用哪个模式才是正确的？ 每一个初学者碰到了实际的问题都会产生疑问，好像用那个模式都可以解决问题。我对以上4种模式进行了一番对比，并结合工作中的实际问题进行了思考，并且和同事们展开了讨论 (这真是人生一大快事啊！) 。我的建议是"xxx教导我们要用发展的眼光来看待这个问题。

一般来说，在软件开发过程中，总是把大的问题进行细化，然后从小处入手，逐渐发展壮大。也就是说最开始的时候遇到的问题往往很小，一个类就可以解决了，对于只需要生成简单对象的情况，使用Factory模式；对于需要生成复杂对象的情况，用builder模式，只需要写一个类，接口拉，抽象类拉，完全不需要！目前不需要担心松紧耦合的问题。进一步优化的话，可以写两个类，builder负责生成复杂的对象，而将所有关于生成简单对象的工作转交给Factory，用英语术语来表达的话叫"delegate", 对应的模式叫Business Delegate (core J2EE Patterns) 。

当系统发展壮大后, 需要生成很多种类的复杂对象，导致了需要很多builder来负责生成她们，这个时候就需要做两件事，第一是使用Abstract Factory模式，负责生成相对应的builder类，进而对各种复杂的对象生成进行系统的管理。第二是为各种类别的builder和Factory编写接口，然后利用refactoring将使用类的地方尽可能的替换为使用借口，也就是面向对象编程基本原理之一的"尽量针对接口编程，而不是针对实现类"。如果希望优化系统，减少对象实体的生成，可以视情况而定，采用Singleton模式。

请注意到目前为止，我们没有用到继承，这也是符合面向对象编程的原理的—组合优先于继承 (composition， not inheritance) 。但是当系统再进一步发展长大后，她已经不能再称为模块，而是成长为框架 (framework) 时，我们就要考虑适当的使用Factory Method模式了。基本的功能将在父类中加以实现，而具体的对象生成交由子类来完成。如果结合其他模式来理解的话，就是子类中生成对象的工作将转交给其他3中模式类们来完成。如果希望在运行状态 (runtime) 时动态切换相关的Builder或Factory的话，可以采用Strategy模式。不过，就像很多介绍面向对象编程的书籍建议的那样，不到万不得已不要使用继承，也就是说，切忌在系统还非常简单的情况下就贸然使用Factory Method。

![][6]

图6 Big picture

到此为止所有4种模式都用上了，整个系统有如下优点: 

1. 健壮，易于扩展，易于维护。
  
2. 针对接口，系统内部松散，解耦合。
  
3. 基本上避免了代码重复。

这样构件的系统里，我们用到了下列模式: 

1.      Factory Pattern

2.      Abstract Factory Pattern

3.      Builder Pattern

4.      Singleton Pattern

5.      Template Method Pattern

6.      Composite Pattern

7.      Strategy Pattern

8.      Business Delegate Pattern

[http://www.iteye.com/topic/17112](http://www.iteye.com/topic/17112)

 [1]: http://www.wiloon.com/wp-content/uploads/2012/10/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBeu5PDT5UndtcNdt48rY80PV_fd8Ce5pLpHavAj520cgRoVa4EmOhjE5VNS7GnBHl126UUuSSCrcM8YMFLVb3mp_UsivKRLJ1HKESriM5FDQA-1.gif
 [2]: http://storage.msn.com/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBee-TnpMzZc_ZqwZC1doT-cIW-U3P8N2-bwjC3VP-_6SlTcY5iXrrcpDcnU4l-WG2ExsjQnc-bZyr1hx0TfiXjK3YQEsA8ZnsrSglQaBWXZQQ
 [3]: http://storage.msn.com/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBfvnLjsxFYObHTGR9CPTp9UBQ_GxnpRhEDmyikpUU9sqYJUmC-gy1fSl2JMcMWgb-txY8kEBN_QXG-d3HAtxoSpLo_Oz30QnQcLwQI2M5JChg
 [4]: http://storage.msn.com/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBcigtvc1JV34v6wh_gCCn9NXHLLHeWJlj76OiZDZRbf8X_zj_z_ah5oDKF02kC2D7bLcsLOYqw79e8FzS15halIoxPca7kCgYhxoeAXYgeCJQ
 [5]: http://storage.msn.com/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBcWaDI_WugqSxGiMT8HyNq__h6MGuk8G87qbOMESYySsMzqcW0zl9jbcYK7c0PW5s02Yh6HLodZujaDwlHF4Y63a8zJLfnkuNUMAJhEQeQ5ag
 [6]: http://storage.msn.com/x1pBG_wmiiVq4fKhMkEoTbjopPcKCE3u0uJjfqcYoYvgBcvTDF0Pg2ZR7U3ahhCcauR5u1FUf05edNjFJfXq8-HjrJ7oCeeQrI9BBvsA8Vg6id6vZCSSzXtf9IsQAWDFEUjk_N_hAMhZyfQ54VQ8-o5kw