---
title: 创建者模式 Builder
author: "-"
date: 2012-10-10T04:23:22+00:00
url: /?p=4421
categories:
  - pattern
tags:
  - DesignPattern

---
## 创建者模式 Builder

## 建造者模式

定义: 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示  

### 使用场景

1. 多个部件或零件，都可以装配到一个对象中，但产生的结果又不相同时。
2. 当初始化一个对象特别复杂的时候，比如参数多，而且很多参数都有默认值。

它分为抽象建造者 (Builder) 角色、具体建造者 (ConcreteBuilder) 角色、导演者 (Director) 角色、产品 (Product) 角色四个角色。

抽象建造者 (Builder) 角色: 给 出一个抽象接口，以规范产品对象的各个组成成分的建造。

具体建造者 (ConcreteBuilder) 角色: 要完成的任务包括: 1.实现抽象建造者Builder所声明的接口，给出一步一步地完成创建产品实例的操作。2.在建造过程完成后，提供产品的实例。

导演者 (Director) 角色: 担任这个角色的类调用具体建造者角色以创建产品对象。

产品 (Product) 角色: 产品便是建造中的复杂对象。

对于Builder模式很简单，但是一直想不明白为什么要这么设计，为什么要向builder要Product而不是向知道建造过程的Director要。刚才google到一篇文章，总算清楚了。在这里转贴一下这位richardluo的比喻。

简单地说，就好象我要一座房子住，可是我不知道怎么盖 (简单的砌墙，层次较低) ，也不知道怎么样设计 (建几个房间，几个门好看，层次较高) ，于是我需要找一帮民工，他们会砌墙，还得找个设计师，他知道怎么设计，我还要确保民工听设计师的领导，而设计师本身也不干活，光是下命令，这里砌一堵墙，这里砌一扇门，这样民工开始建设，最后，我可以向民工要房子了。在这个过程中，设计师是什么也没有，除了他在脑子里的设计和命令，所以要房子也是跟民工要，记住了！

以下是richardluo的代码，我根据他的思路加上了相应的注释。

1. 定义工人接口，就是能够完成建造房子任务的人的通用要求。

```java

// 工人接口，定义了各个工人所要进行的工所作。他们负责进行具体部件如窗户，地板的建造。

// 同时因为房子是民工建的，因此建设完成后由他把房子递交回房主

public interface Builder {

public void makeWindow();

public void makeFloor();

public Room getRoom();

}

2. 定义设计师，他的职责是指挥房主指派给他的工人按照自己的设计意图建造房子。

```java

// 设计师。他知道房子应该怎么设计，但他不会自己去建造，而是指挥民工去建造。

public class Designer {

// 指挥民工进行工作

public void order(Builder builder) {

builder.makeWindow();

builder.makeFloor();

}

}

```

3. 民工，他负责具体事物的实施。

```java
// 民工。负责进行具体部件如窗户，地板的建造。

//同时因为房子是民工建的，因此建设完成后由他把房子递交回房主

public class Mingong implements Builder {

private String window="";

private String floor="";

public void makeWindow() {

window=new String("window");

}

public void makeFloor(){

floor=new String("floor");

}

// 回交房子给房主

public Room getRoom() {

if((!window.equals(""))&&(!floor.equals(""))) {

System.out.println("room ready!");

return new Room();

}

else return null;

}

}

```

4. 房主，就是雇人，收房。

```java

// 房主。房主的任务就是聘请一个民工，一个设计师，同时把民工给设计师指挥，督促设计师开展工作。最后从民工手上收房。

public class Client {

public static void main(String[] args) {

Builder mingong = new Mingong();

Designer designer = new Designer();

designer.order(mingong);

mingong.getRoom();

}

}

```

好了，我觉得这样大概能说明白了。不知各位觉得如何呢？或者有更好的应用场景解释，敬请赐教。

[GOF95]中，Builder模式将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

Builder模式和AbstractFactory模式在功能上很相似，因为都是用来创建大的复杂的对象，它们的区别是: Builder模式强调的是一步步创建对象，并通过相同的创建过程可以获得不同的结果对象，一般来说Builder模式中对象不是直接返回的。而在AbstractFactory模式中对象是直接返回的，AbstractFactory模式强调的是为创建多个相互依赖的对象提供一个同一的接口。

```java

class Room {
}

abstract class Builder {
protected String window = "";
protected String floor = "";
public void prepareWater() {
}

public void prepareElectricity() {
   
}
   
public void prepareRoad() {
   
}
   
public void makeWindow() {
   
}
   
public void makeFloor() {
   
}
   
public abstract Room getRoom();
   
public void makeGarden() {
   
}
  
}

// Designer。他知道房子应该怎么设计，但他不会自己去建造，而是指挥民工去建造。
  
abstract class Designer {
   
Builder builder;

public Designer(Builder builder) {
   
this.builder = builder;
   
}

public void preparationWorks() {
   
builder.prepareWater();
   
builder.prepareElectricity();
   
builder.prepareRoad();
   
}
   
public abstract void construct();
  
}

class ApartmentDesigner extends Designer {

public ApartmentDesigner(Builder builder) {
   
super(builder);
   
}

// 指挥工人进行工作
   
public void construct() {
   
preparationWorks();
   
builder.makeWindow();

builder.makeFloor();

}

}

class HouseDesigner extends Designer {

public HouseDesigner(Builder builder) {
   
super(builder);
   
}

// 指挥工人进行工作
   
public void construct() {
   
preparationWorks();
   
builder.makeWindow();

builder.makeFloor();
   
builder.makeGarden();
   
}
  
}

// 建筑工人。负责进行具体部件如窗户，地板的建造.
  
//同时因为房子是工人建的，因此建设完成后由他把房子递交回房主.
  
class ApartmentBuilder extends Builder {
   
@Override
   
public void prepareWater() {
   
}

@Override
   
public void prepareElectricity() {
   
}

@Override
   
public void prepareRoad() {
   
}

public void makeWindow() {

window = new String("apartment window");

}

public void makeFloor() {

floor = new String("apartment floor");

}

// 回交房子给房主

public Room getRoom() {

if ((!window.equals("")) && (!floor.equals(""))) {

System.out.println("room ready!");

return new Room();

} else return null;

}
  
}

class HouseBuilder extends Builder {

@Override
   
public Room getRoom() {
   
return null;
   
}

public void makeWindow() {

window = new String("house window");

}

public void makeFloor() {

floor = new String("house floor");

}

@Override
   
public void makeGarden() {
   
//To change body of implemented methods use File | Settings | File Templates.
   
}
  
}

// 房主。房主的任务就是聘请一个工人，一个设计师，同时把工人给设计师指挥，督促设计师开展工作。最后从工人手上收房。
  
public class BuilderPatternClient {

public static void main(String[] args) {

Builder builder = new ApartmentBuilder();

Designer designer = new ApartmentDesigner(builder);

designer.construct();

builder.getRoom();

builder = new HouseBuilder();
   
designer = new HouseDesigner(builder);
   
designer.construct();
   
builder.getRoom();
   
}
  
}

```

工厂方法模式VS建造者模式
工厂方法模式注重的是整体对象的创建方法，而建造者模式注重的是部件构建的过程，旨在通过一步一步地精确构造创建出一个复杂的对象。
我们举个简单例子来说明两者的差异，如要制造一个超人，如果使用工厂方法模式，直接产生出来的就是一个力大无穷、能够飞翔、内裤外穿的超人；
而如果使用建造者模式，则需要组装手、头、脚、躯干等部分，然后再把内裤外穿，于是一个超人就诞生了。

工厂方法模式创建的产品一般都是单一性质产品，如成年超人，都是一个模样，而建造者模式创建的则是一个复合产品，它由各个部件复合而成，部件不同产品对象当然不同。
这不是说工厂方法模式创建的对象简单，而是指它们的粒度大小不同。一般来说，工厂方法模式的对象粒度比较粗，建造者模式的产品对象粒度比较细。

两者的区别有了，那在具体的应用中，我们该如何选择呢？
是用工厂方法模式来创建对象，还是用建造者模式来创建对象，这完全取决于我们在做系统设计时的意图，如果需要详细关注一个产品部件的生产、安装步骤，则选择建造者，否则选择工厂方法模式。

作者: ztzt123
链接: <https://www.jianshu.com/p/15b001f5b95f>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

<http://blog.csdn.net/surprisesdu/article/details/621046>

<http://smartfool.iteye.com/blog/71175>

作者: ztzt123
链接: <https://www.jianshu.com/p/15b001f5b95f>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
