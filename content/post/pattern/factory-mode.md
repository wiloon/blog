---
title: 工厂模式
author: "-"
date: 2011-10-29T06:02:20+00:00
url: /?p=1335
categories:
  - Java
tags:
  - DesignPattern

---
## 工厂模式
工厂模式是我们最常用的模式了,著名的Jive论坛 ,就大量使用了工厂模式，工厂模式在Java程序系统可以说是随处可见。
  
为什么工厂模式是如此常用？因为工厂模式就相当于创建实例对象的new，我们经常要根据类Class生成实例对象，如A a=new A() 工厂模式也是用来创建实例对象的，所以以后new时就要多个心眼，是否可以考虑使用工厂模式，虽然这样做，可能多做一些工作，但会给你系统带来更大的可扩展性和尽量少的修改量。
  
我们以类Sample为例， 如果我们要创建Sample的实例对象:

```java
  
Sample sample=new Sample();
  
```

可是，实际情况是，通常我们都要在创建sample实例时做点初始化的工作,比如赋值 查询数据库等。
  
首先，我们想到的是，可以使用Sample的构造函数，这样生成实例就写成:

```java
  
Sample sample=new Sample(参数);
  
```

但是，如果创建sample实例时所做的初始化工作不是象赋值这样简单的事，可能是很长一段代码，如果也写入构造函数中，那你的代码很难看了 (就需要Refactor重构) 。
  
为什么说代码很难看，初学者可能没有这种感觉，我们分析如下，初始化工作如果是很长一段代码，说明要做的工作很多，将很多工作装入一个方法中，相当于将很多鸡蛋放在一个篮子里，是很危险的，这也是有背于Java面向对象的原则，面向对象的封装(Encapsulation)和分派(Delegation)告诉我们，尽量将长的代码分派"切割"成每段，将每段再"封装"起来(减少段和段之间偶合联系性)，这样，就会将风险分散，以后如果需要修改，只要更改每段，不会再发生牵一动百的事情。
  
在本例中，首先，我们需要将创建实例的工作与使用实例的工作分开, 也就是说，让创建实例所需要的大量初始化工作从Sample的构造函数中分离出去。
  
这时我们就需要Factory工厂模式来生成对象了，不能再用上面简单new Sample(参数)。还有,如果Sample有个继承如MySample, 按照面向接口编程,我们需要将Sample抽象成一个接口.现在Sample是接口,有两个子类MySample 和HisSample .我们要实例化他们时,如下:

```java
  
Sample mysample=new MySample();
  
Sample hissample=new HisSample();
  
```

随着项目的深入,Sample可能还会"生出很多儿子出来", 那么我们要对这些儿子一个个实例化,更糟糕的是,可能还要对以前的代码进行修改:加入后来生出儿子的实例.这在传统程序中是无法避免的.
  
但如果你一开始就有意识使用了工厂模式,这些麻烦就没有了.
  
工厂方法
  
你会建立一个专门生产Sample实例的工厂:

```java
  
public class Factory{
  
public static Sample creator(int which){
  
//getClass 产生Sample 一般可使用动态类装载装入类。
  
if (which==1)
  
return new SampleA();
  
else if (which==2)
  
return new SampleB();
  
}
  
}
  
```

那么在你的程序中,如果要实例化Sample时.就使用
  
Sample sampleA=Factory.creator(1);
  
这样,在整个就不涉及到Sample的具体子类,达到封装效果,也就减少错误修改的机会,这个原理可以用很通俗的话来比喻:就是具体事情做得越多,越容易范错误.这每个做过具体工作的人都深有体会,相反,官做得越高,说出的话越抽象越笼统,犯错误可能性就越少.好象我们从编程序中也能悟出人生道理?呵呵.
  
使用工厂方法 要注意几个角色，首先你要定义产品接口，如上面的Sample,产品接口下有Sample接口的实现类,如SampleA,其次要有一个factory类，用来生成产品Sample。
  
抽象工厂
  
工厂模式中有: 工厂方法(Factory Method) 抽象工厂(Abstract Factory).
  
这两个模式区别在于需要创建对象的复杂程度上。如果我们创建对象的方法变得复杂了,如上面工厂方法中是创建一个对象Sample,如果我们还有新的产品接口Sample2.
  
这里假设: Sample有两个concrete类SampleA和SamleB，而Sample2也有两个concrete类Sample2A和Sample2B
  
那么，我们就将上例中Factory变成抽象类,将共同部分封装在抽象类中,不同部分使用子类实现，下面就是将上例中的Factory拓展成抽象工厂:

```java
  
public abstract class Factory{
  
public abstract Sample creator();
  
public abstract Sample2 creator(String name);
  
}
  
public class SimpleFactory extends Factory{
  
public Sample creator(){
  
.........
  
return new SampleA
  
}
  
public Sample2 creator(String name){
  
.........
  
return new Sample2A
  
}
  
}
  
public class BombFactory extends Factory{
  
public Sample creator(){
  
......
  
return new SampleB
  
}
  
public Sample2 creator(String name){
  
......
  
return new Sample2B
  
}
  
}
  
```

从上面看到两个工厂各自生产出一套Sample和Sample2,也许你会疑问，为什么我不可以使用两个工厂方法来分别生产Sample和Sample2?
  
抽象工厂还有另外一个关键要点，是因为 SimpleFactory内，生产Sample和生产Sample2的方法之间有一定联系，所以才要将这两个方法捆绑在一个类中，这个工厂类有其本身特征，也许制造过程是统一的，比如: 制造工艺比较简单，所以名称叫SimpleFactory。
  
在实际应用中，工厂方法用得比较多一些，而且是和动态类装入器组合在一起应用，
  
举例
  
我们以Jive的ForumFactory为例，这个例子在前面的Singleton模式中我们讨论过，现在再讨论其工厂模式:

```java
  
public abstract class ForumFactory {
  
private static Object initLock = new Object();
  
private static String className = "com.jivesoftware.forum.database.DbForumFactory";
  
private static ForumFactory factory = null;
  
public static ForumFactory getInstance(Authorization authorization) {
  
//If no valid authorization passed in, return null.
  
if (authorization == null) {
  
return null;
  
}
  
//以下使用了Singleton 单态模式
  
if (factory == null) {
  
synchronized(initLock) {
  
if (factory == null) {
  
......
  
try {
  
//动态转载类
Class c = Class.forName(className);
  
factory = (ForumFactory)c.newInstance();
  
}
  
catch (Exception e) {
  
return null;
  
}
  
}
  
}
  
}
  
//Now, 返回 proxy.用来限制授权对forum的访问
  
return new ForumFactoryProxy(authorization, factory,
  
factory.getPermissions(authorization));
  
}
  
//真正创建forum的方法由继承forumfactory的子类去完成.
  
public abstract Forum createForum(String name, String description)
  
throws UnauthorizedException, ForumAlreadyExistsException;
  
....
  
}
  
```

因为现在的Jive是通过数据库系统存放论坛帖子等内容数据,如果希望更改为通过文件系统实现,这个工厂方法ForumFactory就提供了提供动态接口:
  
private static String className = "com.jivesoftware.forum.database.DbForumFactory";
  
你可以使用自己开发的创建forum的方法代替com.jivesoftware.forum.database.DbForumFactory就可以.
  
在上面的一段代码中一共用了三种模式,除了工厂模式外,还有Singleton单态模式,以及proxy模式,proxy模式主要用来授权用户对forum的访问,因为访问forum有两种人:一个是注册用户 一个是游客guest,那么那么相应的权限就不一样,而且这个权限是贯穿整个系统的,因此建立一个proxy,类似网关的概念,可以很好的达到这个效果.
  
看看Java宠物店中的CatalogDAOFactory:

```java
  
public class CatalogDAOFactory {
  
/**
  
* 本方法制定一个特别的子类来实现DAO模式。
  
* 具体子类定义是在J2EE的部署描述器中。
  
*/
  
public static CatalogDAO getDAO() throws CatalogDAOSysException {
  
CatalogDAO catDao = null;
  
try {
  
InitialContext ic = new InitialContext();
  
//动态装入CATALOG_DAO_CLASS
  
//可以定义自己的CATALOG_DAO_CLASS，从而在无需变更太多代码
  
//的前提下，完成系统的巨大变更。
  
String className =(String) ic.lookup(JNDINames.CATALOG_DAO_CLASS);
  
catDao = (CatalogDAO) Class.forName(className).newInstance();
  
} catch (NamingException ne) {
  
throw new CatalogDAOSysException("
  
CatalogDAOFactory.getDAO: NamingException while
  
getting DAO type : n" + ne.getMessage());
  
} catch (Exception se) {
  
throw new CatalogDAOSysException("
  
CatalogDAOFactory.getDAO: Exception while getting
  
DAO type : n" + se.getMessage());
  
}
  
return catDao;
  
}
  
}
  
```

CatalogDAOFactory是典型的工厂方法，catDao是通过动态类装入器className获得CatalogDAOFactory具体实现子类，这个实现子类在Java宠物店是用来操作catalog数据库，用户可以根据数据库的类型不同，定制自己的具体实现子类，将自己的子类名给与CATALOG_DAO_CLASS变量就可以。
  
由此可见，工厂方法确实为系统结构提供了非常灵活强大的动态扩展机制，只要我们更换一下具体的工厂方法，系统其他地方无需一点变换，就有可能将系统功能进行改头换面的变化。

板桥里人 http://www.jdon.com 2002/10/07 (转载请保留) 