---
title: 设计模式 – Decorator
author: "-"
date: 2011-09-22T07:48:49+00:00
url: /?p=847
categories:
  - Java
tags:
  - DesignPattern

---
## 设计模式 – Decorator
Decorator设计模式是典型的结构型模式
  
装饰模式:Decorator常被翻译成"装饰",我觉得翻译成"油漆工"更形象点,油漆工(decorator)是用来刷油漆的,那么被刷油漆的对象我们称decoratee.这两种实体在Decorator模式中是必须的.

Decorator定义:
  
动态给一个对象添加一些额外的职责,就象在墙上刷油漆.使用Decorator模式相比用生成子类方式达到功能的扩充显得更为灵活.
  
下面是GOF的《Element of reusable Object-Oriented Software》中对Decorator用意的概述: 
  
Decorator Pattern――Attaches additional responsibilities to an object dynamically . Decorators provide a flexible alternative to subclassing for extending functionality .

1 何时需要使用装饰器模式

GOF的那本Bible中关于装饰器模式列举的是一个文本组件与边框的例子
  
下面举一个"三明治"的例子！

很多人都吃过三明治，都会知道三明治必不可少的是两块面包片，然后可以在夹层里加上蔬菜、沙拉、咸肉等等，外面可以涂上奶油之类的。假如现在你要为一个三明治小店构造一个程序，其中要设计各种三明治的对象。可能你已经创建了一个简单的Sandwich对象，现在要产生带蔬菜的就是继承原有的Sandwich添加一个蔬菜的成员变量，看起来很"正点"的做法，以后我还要带咸肉的、带奶油的、带蔬菜的又分为带青菜的、带芹菜的、生菜的……还是一个一个继承是吧！假如我们还需要即带蔬菜又带其它肉类，设置我们还要求这些添加成分的任意组合，那你就慢慢继承吧！
  
读过几年书的会下面这个算术，我们有n种成分，在做三明治的时候任意搭配，那么有多少种方案呢？！算算吧！你会有惊人的发现。N种成分，什么都不要是Cn0种方案吧！要1种是Cn1吧！…..要n种是Cnn吧！加起来不就是吗？Cn0+Cn1+……+Cnn-1+Cnn还不会啊！牛顿莱布尼兹公式记得吧！ (可惜Word的公式编辑器安装不了) 总共2的n次方案。有可能前面10天写了K个类，老板让你再加一种成分你就得再干10天，下一次再加一种你可得干20天哦！同时你可以发现你的类库急剧地膨胀！ (老板可能会说你: XXX前K天你加了n个成分，怎么现在这么不上进呢？后K天只加了1个成分啊？！！可能你会拿个比给老板算算，老板那么忙会睬你吗？！有可能你的老板会说: 不管怎么样我就要你加，K天你还给我加n个成分！！呵呵，怎么办啊！跳槽啊!跳槽了也没人要你！！人家一看就知道你没学设计模式) 。下面我们就使用装饰器模式来设计这个库吧！

下面是各个类的意义: 
  
1. Ingredient (成分) : 所有类的父类，包括它们共有的方法，一般为抽象类且方法都有默认的实现，也可以为接口。它有Bread和Decorator两个子类。这种实际不存在的，系统需要的抽象类仅仅表示一个概念，图中用红色表示。
  
2. Bread (面包) : 就是我们三明治中必须的两片面包。它是系统中最基本的元素，也是被装饰的元素，和IO中的媒质流 (原始流) 一个意义。在装饰器模式中属于一类角色，所以其颜色为紫色。
  
3. Decorator (装饰器) : 所有其它成分的父类，这些成分可以是猪肉、羊肉、青菜、芹菜。这也是一个实际不存在的类，仅仅表示一个概念，即具有装饰功能的所有对象的父类。图中用蓝色表示。
  
4. Pork (猪肉) : 具体的一个成分，不过它作为装饰成分和面包搭配。
  
5. Mutton (羊肉) : 同上。
  
6. Celery (芹菜) : 同上。
  
7. Greengrocery (青菜) : 同上。
  
总结一下装饰器模式中的四种角色: 
  
1.被装饰对象 (Bread) ；
  
2.装饰对象 (四种) ；
  
3.装饰器 (Decorator) ；
  
4.公共接口或抽象类 (Ingredient) 。
  
其中1和2是系统或者实际存在的，3和4是实现装饰功能需要的抽象类。
  
写段代码体会其威力吧！ (程序很简单，但是实现的方法中可以假如如何你需要的方法，意境慢慢体会吧！) 

```java
  
//Ingredient.java
  
public abstract class Ingredient {
      
public abstract String getDescription();

public abstract double getCost();

public void printDescription() {
          
System.out.println(" Name " + this.getDescription());
          
System.out.println(" Price RMB " + this.getCost());
      
}
  
}
  
//所有成分的父类，抽象类有一个描述自己的方法和一个得到价格的方法，以及一个打印自身描述和价格的方法 (该方法与上面两个方法构成模板方法哦！) 

//Bread.java
  
public class Bread extends Ingredient {
      
private String description;

public Bread(String desc) {
          
this.description = desc;
      
}

public String getDescription() {
          
return description;
      
}

public double getCost() {
          
return 2.48;
      
}
  
}
  
//面包类，因为它是一个具体的成分，因此实现父类的所有的抽象方法。描述可以通过构造器传入，也可以通过set方法传入。同样价格也是一样的，我就很简单地返回了。

//Decorator.java
  
public abstract class Decorator extends Ingredient {
      
Ingredient ingredient;

public Decorator(Ingredient igd) {
          
this.ingredient = igd;
      
}

public abstract String getDescription();

public abstract double getCost();
  
}
  
//装饰器对象，所有具体装饰器对象父类。它最经典的特征就是: 
  
//1.必须有一个它自己的父类为自己的成员变量；
  
//2.必须继承公共父类。这是因为装饰器也是一种成分，只不过是那些具体具有装饰功能的成分的公共抽象罢了。
  
//在我们的例子中就是有一个Ingredient作为其成员变量。Decorator继承了Ingredient类。

//Pork.java
  
public class Pork extends Decorator {
      
public Pork(Ingredient igd) {
          
super(igd);
      
}

public String getDescription() {
          
String base = ingredient.getDescription();
          
return base + "n" + "Decrocated with Pork !";
      
}

public double getCost() {
          
double basePrice = ingredient.getCost();
          
double porkPrice = 1.8;
          
return basePrice + porkPrice;
      
}
  
}
  
```

具体的猪肉成分，同时也是一个具体的装饰器，因此它继承了Decorator类。猪肉装饰器装饰可以所有的其他对象，因此通过构造器传入一个Ingredient的实例，程序中调用了父类的构造方法，主要父类实现了这样的逻辑关系。同样因为方法是具体的成分，所以getDescription得到了实现，不过由于它是具有装饰功能的成分，因此它的描述包含了被装饰成分的描述和自身的描述。价格也是一样的。价格放回的格式被装饰成分与猪肉成分的种价格哦！
  
从上面两个方法中我们可以看出，猪肉装饰器的功能得到了增强，它不仅仅有自己的描述和价格，还包含被装饰成分的描述和价格。主要是因为被装饰成分是它的成员变量，因此可以任意调用它们的方法，同时可以增加自己的额外的共同，这样就增强了原来成分的功能。

```java
  
//Mutton.java
  
public class Mutton extends Decorator {
      
public Mutton(Ingredient igd) {
          
super(igd);
      
}

public String getDescription() {
          
String base = ingredient.getDescription();
          
return base + "n" + "Decrocated with Mutton !";
      
}

public double getCost() {
          
double basePrice = ingredient.getCost();
          
double muttonPrice = 2.3;
          
return basePrice + muttonPrice;
      
}
  
}
  
//羊肉的包装器。

//Celery.java
  
public class Celery extends Decorator {
      
public Celery(Ingredient igd) {
          
super(igd);
      
}

public String getDescription() {
          
String base = ingredient.getDescription();
          
return base + "n" + "Decrocated with Celery !";
      
}

public double getCost() {
          
double basePrice = ingredient.getCost();
          
double celeryPrice = 0.6;
          
return basePrice + celeryPrice;
      
}
  
}
  
//芹菜的包装器。

//GreenGrocery.java
  
public class GreenGrocery extends Decorator {
      
public GreenGrocery(Ingredient igd) {
          
super(igd);
      
}

public String getDescription() {
          
String base = ingredient.getDescription();
          
return base + "n" + "Decrocated with GreenGrocery !";
      
}

public double getCost() {
          
double basePrice = ingredient.getCost();
          
double greenGroceryPrice = 0.4;
          
return basePrice + greenGroceryPrice;
      
}
  
}
  
//青菜的包装器。

//下面我们就领略装饰器模式的神奇了！我们有一个测试类，其中建立夹羊肉的三明治、全蔬菜的三明治、全荤的三明治。
  
public class DecoratorTest {
      
public static void main(String[] args) {
          
Ingredient compound = new Mutton(new Celery(new Bread("Master24's Bread")));
          
compound.printDescription();

compound = new Celery(new GreenGrocery(new Bread("Bread with milk")));
          
compound.printDescription();

compound = new Mutton(new Pork(new Bread("Bread with cheese")));
          
compound.printDescription();

}
  
}
  
//以上就是一个简单的装饰器类！
  
```

2 装饰器模式的结构
  
在谈及软件中的结构，一般会用UML图表示 (UML和ANT、JUnit等都是软件设计中基本的工具，会了没有啊！) 。下面是一个我们经常看到的关于Decorator模式的结构图。

1. Component就是装饰器模式中公共方法的类，在装饰器模式结构图的顶层。
2. ConcreateComponent是转换器模式中具体的被装饰的类，IO包中的媒体流就是此种对象。
3. Decorator装饰器模式中的核心对象，所有具体装饰器对象的父类，完成装饰器的部分职能。在上面的例子中Decorator类和这里的对应。该类可以只做一些简单的包裹被装饰的对象，也可以还包含对Component中方法的实现……他有一个鲜明的特点: 继承至Component，同时包含一个Component作为其成员变量。装饰器模式动机中的动态地增加功能是在这里实现的。
4. ConcreteDecoratorA和ConcreteDecoratorB是两个具体的装饰器对象，他们完成具体的装饰功能。装饰功能的实现是通过调用被装饰对象对应的方法，加上装饰对象自身的方法。这是装饰器模式动机中的添加额外功能的关键。

从上面图中你可能还会发现: ConcreteDecoratorA和ConcreteDecoratorB的方法不一样，这就是一般设计模式中谈及装饰器模式的"透明装饰器"和"不透明装饰器"。"透明装饰器"就是整个Decorator的结构中所有的类都保持同样的"接口" (这里是共同方法的意思) ，这是一种极其理想的状况，就像餐饮的例子一样。现实中绝大多数装饰器都是"不透明装饰器"，他们的"接口"在某些子类中得到增强，主要看这个类与顶层的抽象类或者接口是否有同样的公共方法。IO中的ByteArrayInputStream就比Inputstrem抽象类多一些方法，因此IO中的装饰器是一个"不通明装饰器"。下面是IO中输入字节流部分的装饰器的结构图。

1. InputStream是装饰器的顶层类，一个抽象类！包括一些共有的方法，如: 1.读方法――read (3个) ；2.关闭流的方法――close；3.mark相关的方法――mark、reset和markSupport；4.跳跃方法――skip；5.查询是否还有元素方法――available。图中红色的表示。
2. FileInputStream、PipedInputStream…五个紫色的，是具体的被装饰对象。从他们的"接口"中可以看出他们一般都有额外的方法。
3. FilterInputStream是装饰器中的核心，Decorator对象，图中蓝色的部分。
4. DataInputStream、BufferedInputStream…四个是具体的装饰器，他们保持了和InputStream同样的接口。
5. ObjectInputStream是IO字节输入流中特殊的装饰器，他不是FilterInputStream的子类 (不知道Sun处于何种意图不作为FileterInputStream的子类，其中流中也有不少的例子) 。他和其他FilterInputStream的子类功能相似都可以装饰其他对象。
  
    IO包中不仅输入字节流是采用装饰器模式、输出字节流、输入字符流和输出字符流都是采用装饰器模式。

为什么使用Decorator?
  
我们通常可以使用继承来实现功能的拓展,如果这些需要拓展的功能的种类很繁多,那么势必生成很多子类,增加系统的复杂性,同时,使用继承实现功能拓展,我们必须可预见这些拓展功能,这些功能是编译时就确定了,是静态的.

使用Decorator的理由是:这些功能需要由用户动态决定加入的方式和时机.Decorator提供了"即插即用"的方法,在运行期间决定何时增加何种功能.

如何使用?
  
举Adapter中的打桩示例,在Adapter中有两种类:方形桩 圆形桩,Adapter模式展示如何综合使用这两个类,在Decorator模式中,我们是要在打桩时增加一些额外功能,比如,挖坑 在桩上钉木板等,不关心如何使用两个不相关的类.

我们先建立一个接口:

public interface Work
  
{
  
public void insert();

}
  
接口Work有一个具体实现:插入方形桩或圆形桩,这两个区别对Decorator是无所谓.我们以插入方形桩为例:

public class SquarePeg implements Work{
  
public void insert(){
  
System.out.println("方形桩插入");
  
}
  
}
  
现在有一个应用:需要在桩打入前,挖坑,在打入后,在桩上钉木板,这些额外的功能是动态,可能随意增加调整修改,比如,可能又需要在打桩之后钉架子(只是比喻).

那么我们使用Decorator模式,这里方形桩SquarePeg是decoratee(被刷油漆者),我们需要在decoratee上刷些"油漆",这些油漆就是那些额外的功能.

public class Decorator implements Work{

private Work work;
  
//额外增加的功能被打包在这个List中
  
private ArrayList others = new ArrayList();

//在构造器中使用组合new方式,引入Work对象;
  
public Decorator(Work work)
  
{
  
this.work=work;

others.add("挖坑");

others.add("钉木板");
  
}

public void insert(){

newMethod();
  
}
  
//在新方法中,我们在insert之前增加其他方法,这里次序先后是用户灵活指定的
  
public void newMethod()
  
{
  
otherMethod();
  
work.insert();

}
  
public void otherMethod()
  
{
  
ListIterator listIterator = others.listIterator();
  
while (listIterator.hasNext())
  
{
  
System.out.println(((String)(listIterator.next())) + " 正在进行");
  
}

}
  
}
  
在上例中,我们把挖坑和钉木板都排在了打桩insert前面,这里只是举例说明额外功能次序可以任意安排.

好了,Decorator模式出来了,我们看如何调用:

Work squarePeg = new SquarePeg();
  
Work decorator = new Decorator(squarePeg);
  
decorator.insert();

Decorator模式至此完成.

如果你细心,会发现,上面调用类似我们读取文件时的调用:

FileReader fr = new FileReader(filename);
  
BufferedReader br = new BufferedReader(fr);

实际上Java 的I/O API就是使用Decorator实现的,I/O变种很多,如果都采取继承方法,将会产生很多子类,显然相当繁琐.

Jive中的Decorator实现
  
在论坛系统中,有些特别的字是不能出现在论坛中如"打倒XXX",我们需要过滤这些"反动"的字体.不让他们出现或者高亮度显示.

在IBM Java专栏中专门谈Jive的文章中,有谈及Jive中ForumMessageFilter.java使用了Decorator模式,其实,该程序并没有真正使用Decorator,而是提示说:针对特别论坛可以设计额外增加的过滤功能,那么就可以重组ForumMessageFilter作为Decorator模式了.

所以,我们在分辨是否真正是Decorator模式,以及会真正使用Decorator模式,一定要把握好Decorator模式的定义,以及其中参与的角色(Decoratee 和Decorator).

http://www.jdon.com 2002/04/28
  
http://miaoxiaodong78.blog.163.com/blog/static/18765136200701232434996/