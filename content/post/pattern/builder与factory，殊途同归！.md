---
title: Builder, Factory
author: "-"
date: 2012-10-12T08:26:55+00:00
url: /?p=4449
categories:
  - Java
tags:
  - DesignPattern

---
## Builder, Factory
[http://www.cnblogs.com/shenfx318/archive/2007/01/28/632724.html](http://www.cnblogs.com/shenfx318/archive/2007/01/28/632724.html)

  
    
      在设计模式的学习过程中，Builder与Factory是创建模式中两个经典的教程，给与了我们很多值得汲取的宝贵设计思想，然而Builder与Factory模式也是初学者容易混淆的两个模式，经常看到有人问及两者的区别与适用的场景，我在近一段设计模式的学习过程中同样碰到了这个问题，在两种模式的区别与联系间我看到的更多是后者，在这里愿意与大家分享一些我对Builder与Factory模式的感悟，有说的不对的地方，还请各位多加提点、指教。
    
    
    
      写在前面
    
    
    
      本文旨在两种模式间的对比与探讨，因此还希望各位看官首先对两个模式有一定的了解为好，因为常常看到有人提问说，Builder模式与抽象工厂 (Abstract Factory) 之间的区别，其实在我看来这两者间并无太多联系，因此也就谈不上区别，至于原因在此不做细述，有兴趣的朋友可以看看我写的有关
      
      http://www.cnblogs.com/shenfx318/archive/2007/01/16/621237.html
      
      抽象工厂的文章。故本文中所提的Factory模式皆指的是工厂方法 (Factory Method) 。
    
    
    
      从Builder到Factory的演化
    
    
    
      先来看看Builder模式，Builder模式的一般设计及实现
 <img src="http://images.cnblogs.com/cnblogs_com/shenfx318/builder_1.gif" alt="" width="455" height="179" border="0" />
    
    
    
      ```java
 public interface IBuilder
 {
 void BuildPart1();
 void BuildPart2();
 Product GetResult();
 }
 //ConcreteBuilderA
 public class BuilderA : IBuilder
 {
 private Product product;
 public void BuildPart1()
 {
 product = new Product();
 product.Add("Part1 build by builderA");
 }
 public void BuildPart2()
 {
 product.Add("Part2 build by builderA");
 }
 public Product GetResult()
 {
 return product;
 }
 }
 }
 //ConcreteBuilderB
 public class BuilderB : IBuilder
 //Director
 public class Director
 {
 public void Construct(IBuilder builder)
 {
 builder.BuildPart1();
 builder.BuildPart2();
 }
 }
 ```
    
    
    
      客户端调用代码
    
    
    
      ```java
 public class Client
 {
 public void Run()
 {
 Director director = new Director();
 IBuilder builder = new BuilderB();
 director.Construct(builder);
 Product product = builder.GetResult();
 product.Show();
 }
 }
 ```
    
    
    
      从类关系图上来看，Builder模式与我们熟知的工厂模式还是具有一定的区别，最显著的莫过于这个指导者(Director)的角色，我们观察这个Director，发现他无非是以参数的形势接收了一个Builder，并按照一定的顺序调用其相应的方法构造各个部件，使得Builder可以完成最终的产品。这其实是对复杂对象构造顺序的封装，但我们可以看到仅仅为了做这一件事情是否有必要为它单独设计一个类？每次都要实例化这个类的对象呢？既然建造顺序是相对稳定的，而且对于客户来讲并不关心这个顺序，那么是否可以将它与Builder类结合？当然可以，实际中也确实常常进行这样的简化，比如StringBuilder类，我们看不到类似Director对象的存在及调用。好，那么经过我们一次的改造以后，变成了如下形式。
    
    
    
      <img src="http://images.cnblogs.com/cnblogs_com/shenfx318/builder_2.gif" alt="" width="358" height="192" border="0" />
    
    
    
    
    
      客户端调用代码
    
    
    
      ```java
 public class Client
 {
 public void Run()
 {
 IBuilder builder = new BuilderB();
 builder.Construct(); //Attention here!
    
    
    
      Product product = builder.GetResult();
 product.Show();
 }
 }
    
    
    
      ```
    
    
    
      再看看客户端中的这条Builder.Construct()语句，似乎也有些多余了，客户一般只有在需要产品的时候才会实例化一个Builder对象，因此对于客户来讲，他创建了Builder意味着他需要Builder能够为他生成一个产品(GetProduct)，而返回产品必然需要构造Construct，于是我们又可以对代码进一步简化，将Construct方法与GetProduct方法结合。
    
    
    
      ```java
 public class BuilderA : IBuilder
 {
 private Product product;
    
    
    
      private void BuildPart1()
 {
 product = new Product();
 product.Add("Part1 build by builderA");
 }
    
    
    
      private void BuildPart2()
 {
 product.Add("Part2 build by builderA");
 }
    
    
    
      public Product GetResult()
 {
 //Construct here!
 BuildPart1();
 BuildPart2();
    
    
    
      return product;
 }
 }
    
    
    
      ```
    
    
    
      对了，客户是不关心这个复杂对象的建造生成过程的，也就是说BuildPartN(),这些方法对于客户是没有意义的，是不可见的，那么我们就将其声明为private,而GetProduct只是方法的一个名称，叫什么都可以，你可以叫GetResult，ReturnProduct….把它称为Create亦可。OK，之后再来看看改造后的类图。
    
    
    
      <img src="http://images.cnblogs.com/cnblogs_com/shenfx318/builder_3.gif" alt="" width="317" height="160" border="0" />
    
    
    
      OMG! 从图上来看，除了名称叫做Builder外，其他根本和Factory模式没有什么区别，从代码来看，不过是工厂模式在返回具体的产品前对该产品进行了一些初始化的工作。
    
    
    
      ```java
 //Create method in Buider
 public Product Create()
 {
 BuildPart1(); // Initail part1 of product
 BuildPart2(); // Initail part2 of product
    
    
    
      return product;
 }
    
    
    
      ```
    
    
    
      就是这些代码，我们将其挪个地方改个名称又何尝不可呢?
    
    
    
      ```java
 //Create method in Buider
 public Product Create()
 {
 return product;
 }
 //Build job move to the product class
 public class Product
 {
 ArrayList parts = new ArrayList();
    
    
    
      public Product()
 {
 InitalPart1(); // Same as BuildPart1()
 InitalPart2(); // Same as BuildPart2()
 }
 }
    
    
    
      ```
  
  
    好了，通过对Builder模式向Factory的一步步演化，我们可以看到两者实质上并没有太多的区别，这也就是本文想要阐述的观点，也许很多朋友这时会反驳我了，说两者怎么会没有区别呢？
  
  
    
      
        Builder模式用于创建复杂的对象。
      
    
    
    
      
        对象内部构建间的建造顺序通常是稳定的。
      
    
    
    
      
        对象内部的构建通常面临着复杂的变化。
      
    
  
  
    对于持以上观点的朋友，我也有如下一些疑问。
  
  
    
      
        什么样的对象属于复杂的对象？关于对象复杂与否是如何划分的？
      
    
    
    
      
        站在客户的角度来讲，是否关心对象的复杂程度及建造顺序？
      
    
    
    
      
        既然客户不关心对象是否复杂以及生成的顺序，那么将这个复杂对象分布构建的意义就在于它有益于设计方了，对于设计人员，复杂对象分布构建的分布体现在哪里?是依次写几行代码还是依次调用几个方法？
      
    
    
    
      
        这种分布给你带来了哪些好处？可以帮助你应付哪些变化？
      
    
  
  
    既然我们不是为了学习设计模式而学习，而是为了学习OOD的精髓，能够编写出更加灵活，适用于需求变化的软件。那么对于需求变化，我们不妨再来看看两个模式是如何应对的。Builder模式适用场景中的第3条提到了"变化"二字: 对象内部的构建通常面临着复杂的变化。就拿PartA为例，现在这个对象发生了剧烈的变化，对于Builder来讲，修改BuildPartA()方法显然是违反OCP的，于是采取第二种方法，从抽象Builder派生一个新的NewBuilder类，为这个新的Builder添加变化后的BuildPartA()方法，其余BuildPart方法不变。代码如下。
  
  
    ```java
 public class NewBuilder : IBuilder
 {
 private Product product;
 #region IBuilder Members
  
  
    public void BuildPart1()
 {
 //With new part1.
 product = new Product();
 product.Add("NewPart1 build by builderA");
 }
  
  
    public void BuildPart2()
 {
 //Nothing changed.
 product.Add("Part2 build by builderA");
 }
  
  
    #endregion
  
  
    public Product GetResult()
 {
 return product;
 }
 }
 //恩，上面的场景对于Builder模式的使用，还算比较恰当。
 //如果我们要换成Factory呢？一样可以通过扩展来应对变化。
  
  
    public class NewFactory : Factory
 {
 Product product = null;
  
  
    public Product Create()
 {
 //With new part1.
 product = new Product();
 product.Add("NewPart1 build by builderA");
  
  
    //Nothing changed.
 product.Add("Part2 build by builderA");
 return product;
 }
 }
 ```
  

你可能会认为，我改造后的Factory就不叫Factory了，已经失去了Factory的本意，好吧，那我们暂且抛开它的名称，换个角度来看看Builder与Factory，Builder具有Factory应付不了的情况吗？没有！因为对象很复杂，所以使用Builder构建对象功能更强大，更具有灵活性吗？没有！客户对于取得产品的过程，以及最终产品的使用有区别吗？没有！因此Builder仅仅是在代码的结构上与Factory产生了一些异同，使得用户可以在取得产品前对产品进行一定的初始化工作。如果这也能够称为新模式的话，那么只能说个人对于设计间区别的理解不同。

还有最后要说的一点，关于建造者模式中第2条: 对象内部构建间的建造顺序通常是稳定的，这点在我看来也难以构成对于与Factory模式区别的理由，因为Factory模式从来就没有考虑对象的建造顺序！只有不稳定的东西才能带来变化的可能性，将稳定的不会变化的东西也作为设计模式的理由是否有些牵强了？

本文仅代表了作者当时的认知程度与观点，文中之所以主要强调了两个模式间的相同点还是因为本人的水平有限未能找到合适的例子来区分二者，还希望大家各抒己见，为在下答疑解惑。