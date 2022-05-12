---
title: 外观 Facade
author: "-"
date: 2012-10-16T06:49:57+00:00
url: /?p=4500
categories:
  - Java
tags:
  - reprint
---
## 外观 Facade
看到"门面"这个词，大家一定都觉得很熟悉。不错，这个词正是借用了我们日常生活中的"门面"的概念。日常生活中的"门面"，正是我们买东西的地方。因此可以这么说，"门面"就是这么一个地方，它们跟各种商品的生产商打交道，收集商品后，再卖给我们。换句话说，如果没有"门面"，我们将不得不直接跟各种各样的生产商买商品；而有了"门面"，我们要买东西，直接跟"门面"打交道就可以了。

Facade模式正是这样一个"门面": 我们本来需要与后台的多个类或者接口打交道，而Facade模式是客户端和后台之间插入一个中间层——门面，这个门面跟后台的多个类或接口打交道，而客户端只需要跟门面打交道即可。

使用Facade模式可以说是后台设计和编码人员的一个必备素质。我不止碰到过一个这样的后台开发人员，他们认为只要把后台功能完成了就万事大吉，而没有站在后台使用者的角度来看一看自己写出来的代码。其实，我们写出来的后台代码是要给别人使用的，所以我们提供给使用者的接口要越简单越好，这不单是对使用者好，同时对开发者也是好处多多的，至少你的接口简单了，你和使用者的交流就容易了。

而Facade模式中的Facade类正是这样一个用户接口，它和后台中的多个类产生依赖关系，而后台的客户类则只跟Facade类产生依赖关系。为什么要这么做？其中的原因十分简单: 后台的开发者熟悉他自己开发的各个类，也就容易解决和多个类的依赖关系，而后台的使用者则不太熟悉后台的各个类，不容易处理和它们之间的依赖；因此，后台的开发者自己在Facade类中解决了与后台多个类之间的依赖，后台的使用者只需要处理和Facade类的依赖即可。

好了，闲话少说。我们下面就以几个具体的例子来看一看Facade模式是怎么使用的。实际编程中，能使用到Facade模式的情况有很多，以下就分两种情况来具体说一说Facade模式的使用。可能还会有其他的情况，大家在实践中也可以加以补充。

第一种情况，客户类要使用的功能分布在多个类中，这些类可能相互之间没有什么关系；客户在使用后台的时候，必须先初始化要使用到的功能所在的类，然后才能使用。这时候，适合将这些功能集中在一个Facade类里，还可以替用户做一些初始化的工作，以减轻用户的负担。
  
例如，以商店为例。假如商店里出售三种商品: 衣服、电脑和手机。这三种商品都是由各自的生产厂商卖出的，如下: 
  
public class CoatFactory
  
{
  
public Coat saleCoat()
  
{
  
……
  
return coat;
  
}
  
……
  
}

然后是电脑的厂家类: 

public class ComputerFactory
  
{
  
public Computer saleComputer()
  
{
  
……
  
return computer;
  
}
  
……
  
}

最后是手机商类: 

public class MobileFactory
  
{
  
public Mobile saleMobile()
  
{
  
……
  
return mobile;
  
}
  
……
  
}
  
如果没有商店，我们就不得不分别跟各自的生产商打交道，如下: 

//买衣服
  
CoatFactory coatFactory = new CoatFactory();
  
coatFactory.saleCoat();
  
//买电脑
  
ComputerFactory computerFactory = new ComputerFactory();
  
computerFactory.saleComputer();
  
//买手机
  
MobileFactory mobileFactory = new MobileFactory();
  
mobileFactory.saleMobile();
  
对我们顾客来说，和这么多的厂家类打交道，这显然是够麻烦的。
  
这样，我们就需要创建一个商店类了，让商店类和这些厂家打交道，我们只和商店类打交道即可，如下: 

public class Store
  
{
  
public Coat saleCoat()
  
{
  
CoatFactory coatFactory = new CoatFactory();
  
return coatFactory.saleCoat();
  
}
  
public Computer saleComputer()
  
{
  
ComputerFactory computerFactory = new ComputerFactory();
  
return computerFactory.saleComputer();
  
}
  
public Mobile saleMobile()
  
{
  
MobileFactory mobileFactory = new MobileFactory();
  
return mobileFactory.saleMobile();
  
}
  
}
  
好了，现在我们要买东西，不用去跟那么多的厂家类打交道了。

Store store =new Store();
  
//买衣服
  
store.saleCoat();
  
//买电脑
  
store.saleComputer();
  
//买手机
  
store.saleMobile();
  
呵呵，这样对我们客户类来说，是不是简单多了。

第二种情况客户要完成的某个功能，可能需要调用后台的多个类才能实现，这时候特别要使用Facade模式。不然，会给客户的调用带来很大的麻烦。请看下面的例子。

我经常看到后台编码人员，强迫它们的使用者写出如下的代码: 

……
  
String xmlString = null;
  
int result = 0;
  
try
  
{
  
xmlString = gdSizeChart.buildDataXML(incBean);

String path = "D:/Eclipse3.0/workspace/PLMSuite/AppWeb/PM/productSpecification/gridfile.xml";
  
File f = new File(path);
  
PrintWriter out = new PrintWriter(new FileWriter(f));
  
out.print(xmlString);
  
out.close();
  
System.out.println("/r/n/r/n sumaryAction" + xmlString + "/r/n/r/n");
  
request.setAttribute("xmlString", xmlString);
  
}
  
catch(Exception ex)
  
{
  
ex.printStackTrace();
  
}
  
这段代码前面即省略号省略掉的一部分是客户类调用后台的一部分代码，是一个相对独立的功能。后面这一部分也是一个相对独立的功能，而后台代码设计人员却把这个功能留给客户类自己来实现。

我就很怀疑，让客户类做这么多事情，到底要你的后台做什么？你还不如直接把所有的事情都给客户类做了得了。因为，你后台做了一半，剩下的一部分给客户类做，客户类根本就不明白怎么回事，或者说他不清楚你的思路，这样做下去更加困难。可能这点逻辑对你来说，很简单。但使用者不明白你的思路啊，他不知道来龙去脉，怎么往下写？

如果在这里有一个Facade类，让它来做不该由客户类来做的事，是不是简单多了呢？如下是一个Facade类: 

public class Facade
  
{
  
public static void doAll(PE_MeasTableExdBean incBean, HttpServletRequest request)
  
{
  
……
  
request.setAttribute("xmlString",Facade.getFromOut(incBean));
  
}
  
private static String getFromOut(PE_MeasTableExdBean incBean)
  
{
  
try
  
{
  
xmlString = gdSizeChart.buildDataXML(incBean);

String path = "D:/Eclipse3.0/workspace/PLMSuite/AppWeb/PM/productSpecification/gridfile.xml";
  
File f = new File(path);
  
PrintWriter out = new PrintWriter(new FileWriter(f));
  
out.print(xmlString);
  
out.close();
  
System.out.println("/r/n/r/n sumaryAction" + xmlString + "/r/n/r/n");
  
return xmlString;
  
}
  
catch(Exception ex)
  
{
  
ex.printStackTrace();
  
return null;
  
}
  
}
  
}

那么客户类的调用就是下面的样子: 

Facade.doAll(incBean,request);
  
这样，客户是不是轻松多了？值得注意的是，Facade类中的getFromOut方法其实不应该在Facade类中，本文为了简单起见而放在了这个类中，对Facade类来说是不符合单一职责原则的。

最后总结一下第二种情况的模式。后台为实现某一个功能有如下类: 

public class ClassA
  
{
  
public void doA()
  
{
  
……
  
}
  
……
  
}
  
public class ClassB
  
{
  
public void doB()
  
{
  
……
  
}
  
……
  
}
  
public class ClassC
  
{
  
public void doC()
  
{
  
……
  
}
  
……
  
}

如果客户类需要这样调用: 

……
  
ClassA a = new ClassA();
  
a.doA();
  
ClassB b = new ClassB();
  
b.doB();
  
ClassC c = new ClassC();
  
c.doC();
  
……
  
那么就适合做一个Facade类，来替客户类来完成上述的功能，如下: 

public class Facade
  
{
  
public void doAll()
  
{
  
ClassA a = new ClassA();
  
a.doA();
  
ClassB b = new ClassB();
  
b.doB();
  
ClassC c = new ClassC();
  
c.doC();
  
}
  
}
  
则客户类的调用如下: 

……
  
Facade Facade = new Facade();
  
Facade.doAll();
  
……