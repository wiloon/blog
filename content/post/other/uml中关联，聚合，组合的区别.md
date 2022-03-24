---
title: UML中关联，聚合，组合的区别
author: "-"
date: 2012-10-15T08:40:14+00:00
url: /?p=4463
categories:
  - UML
tags:
  - UML

---
## UML中关联，聚合，组合的区别
  
### 类间关系
在类图中，除了需要描述单独的类的名称、属性和操作外，我们还需要描述类之间的联系，因为没有类是单独存在的，它们通常需要和别的类协作，创造比单独工作更大的语义。在UML类图中，关系用类框之间的连线来表示，连线上和连线端头处的不同修饰符表示不同的关系。类之间的关系有继承 (泛化) 、关联、聚合和组合。

继承: 指的是一个类 (称为子类) 继承另外的一个类 (称为基类) 的功能，并增加它自己的新功能的能力，继承是类与类之间最常见的关系。类图中继承的表示方法是从子类拉出一条闭合的、单键头 (或三角形) 的实线指向基类。例如，图3.2给出了MFC中CObject类和菜单类CMenu的继承关系。
  
类的继承在C++中呈现为: 

class B { }
class A : public B{ }

关联: 指的是模型元素之间的一种语义联系，是类之间的一种很弱的联系。关联可以有方向，可以是单向关联，也可以是双向关联。可以给关联加上关联名来描述关联的作用。关联两端的类也可以以某种角色参与关联，角色可以具有多重性，表示可以有多少个对象参与关联。可以通过关联类进一步描述关联的属性、操作以及其他信息。关联类通过一条虚线与关联连接。对于关联可以加上一些约束，以加强关联的含义。
  
  
    关联在C++中呈现为: 
  
  
    class A{...}
  
  
    class B{ ...}
  
  
    A::Function1(B &b) //或A::Function1(B b) //或A::Function1(B *b)
  
  
    即一个类作为另一个类方法的参数。
  
  
    聚合: 指的是整体与部分的关系。通常在定义一个整体类后，再去分析这个整体类的组成结构。从而找出一些组成类，该整体类和组成类之间就形成了聚合关系。例如一个航母编队包括海空母舰、驱护舰艇、舰载飞机及核动力攻击潜艇等。需求描述中"包含"、"组成"、"分为…部分"等词常意味着聚合关系。
  
  
    组合: 也表示类之间整体和部分的关系，但是组合关系中部分和整体具有统一的生存期。一旦整体对象不存在，部分对象也将不存在。部分对象与整体对象之间具有共生死的关系。
  
  
    聚合和组合的区别在于: 聚合关系是"has-a"关系，组合关系是"contains-a"关系；聚合关系表示整体与部分的关系比较弱，而组合比较强；聚合关系中代表部分事物的对象与代表聚合事物的对象的生存期无关，一旦删除了聚合对象不一定就删除了代表部分事物的对象。组合中一旦删除了组合对象，同时也就删除了代表部分事物的对象。
  
  
    我们用浅显的例子来说明聚合和组合的区别。"国破家亡"，国灭了，家自然也没有了，"国"和"家"显然也是组合关系。而相反的，计算机和它的外设之间就是聚合关系，因为它们之间的关系相对松散，计算机没了，外设还可以独立存在，还可以接在别的计算机上。在聚合关系中，部分可以独立于聚合而存在，部分的所有权也可以由几个聚合来共享，比如打印机就可以在办公室内被广大同事共用。
  
  
    在C++语言中，从实现的角度讲，聚合可以表示为: 
  
  
    class A {...}
  
  
    class B { A* a; .....}
  
  
    即类B包含类A的指针；
  
  
    而组合可表示为: 
  
  
    class A{...}
  
  
    class B{ A a; ...}
  
  
    即类B包含类A的对象。
  
  
    准确的UML类图中用空心和实心菱形对聚合和组合进行了区分。
  
  
    关联和聚合的区别主要在语义上，关联的两个对象之间一般是平等的，例如你是我的朋友，聚合则一般不是平等的，例如一个公司包含了很多员工，其实现上是差不多的。聚合和组合的区别则在语义和实现上都有差别，组合的两个对象之间其生命期有很大的关联，被组合的对象是在组合对象创建的同时或者创建之后创建，在组合对象销毁之前销毁。一般来说被组合对象不能脱离组合对象独立存在，而且也只能属于一个组合对象，例如一个文档的版本，必须依赖于文档的存在，也只能属于一个文档。聚合则不一样，被聚合的对象可以属于多个聚合对象，例如一个员工可能可以属于多个公司。
  
  
    我想举个通俗的例子。
  
  
    你和你的心脏之间是composition关系 (心脏只属于你自己) 
  
  
    你和你买的书之间是aggregation关系 (书可能是别人的) 
  
  
    你和你的朋友之间是assoc
  
### UML中依赖 (Dependency) 和关联 (Association) 之间的区别
0. 一般情况下，使用关联 (association) 来表示像类中的字段等。这个关系是始终存在的，因此你可以随时针对关联项进行访问调用，例如可以始终从 Customer 对象获取 Order 对象。但事实上它并不需要是一个字段，如果从更偏向于接口建模的角度来看，它只是表示 Customer 中存在了一个可以返回 Order 的方法。

此处引用《UML Distilled》一书中的定义: 

a dependency exists between two elements if changes to the definition of one element (the supplier) may cause changes to the other (the client)

两个元素之间存在依赖关系，是指如果改变其中一个元素 (supplier) 的定义可能会导致另一个元素的变化 (client) 

这是一个模糊和普通的关系定义，这就是为什么对 UML 有许多不同形式的依赖 (dependency) 定义。而在代码术语中，诸如命名一个参数类型和创建一个临时变量对象等也暗示着依赖关系。

你可能不想在 UML 图中显示所有的依赖 - 因为有太多的依赖。你需要有选择性地显示那些对你的沟通表达非常重要的依赖。

我倾向于不频繁的使用多种依赖形式定义。我发现大部分情况下我要展现的关键点是依赖的存在，而使用哪种形式来表述已经不是那么重要。

关联 (association) 也意味着依赖 (dependency) ，如果两个类之间存在关联关系，则也存在依赖关系。但我无法想象你可能会用一条额外的线来表示这种情况。关联已经暗示了依赖，因此无需再泛化 (generalization) 了。

这种混淆的原因之一就是在 UML 1.0 中使用了瞬态链接 (transient links) ，这似乎是由于 UML 1.0 的元模型的定义问题，通过使用关联关系形式来体现它们自身的依赖，例如参数。我一直不喜欢这种表示方式，因为我觉得一个永久的关系和一个仅在当前方法中存在的上下文关系之间存在着重要的区别。因此我会以依赖的形式来表示而非关联。在 UML 2.0 中这个问题不会再出现，因为元模型中采用了不同的形式来表示方法上下文的关系，所以上述的表示形式在 UML 2.0 中不在有效。

 

翻译自 Martin Fowler 文章 《Dependency And Association》。


1. Dependency Relationship

Draw a dependency relationship between two classes, or between a class and an interface, to show that the client class depends on the supplier class/interface to provide certain services, such as:

?The client class accesses a value (constant or variable) defined in the supplier class/interface.

?Operations of the client class invoke operations of the supplier class/interface.

?Operations of the client class have signatures whose return class or arguments are instances of the supplier class/interface.

A dependency relationship is a dotted line with an arrowhead at one end:The arrowhead points to the supplier class.

Association Relationship

An association provides a pathway for communication. The communication can be between use cases and actors, between two classes or between a class and an interface. Associations are the most general of all relationships and consequentially the most semantically weak. If two objects are usually considered independently, the relationship is an association

2. Martin Fowler

If you have an association from Class A to Class B then that means every instance of class A has some kind of link to class B. Now exactly what people mean by "some kind of link" varies, it may be a conceptual link, a method of the form getA or a field inside class A. But the usual notion is that the link exists at all times (although if the lower bound is 0 it may be empty). This link can be used by any method of A and, if exposed, by other classes too.

With a parameter the connection between A and B only exists within the scope of the method that took the parameter. No other method can use the connection. As such that, for most people I come across, means that it is not an association.

The dependency means that if you change the interface of B then you may have to change A. An association usually implies a dependency, but not vice-versa, as the parameter example suggests.

3. Robert C. Martin However, association is not free of semantics. An association is a data relationship. i.e. the implementation must use some sort of data variable to implement it. Typically this is done with some kind of member variable or instance variable that refers to the associate. In C++ we might create a pointer variable, in Java a reference variable. Or we might use some kind of string that represents the associate in a dictionary somewhere.

In order for a message to be send between two objects, an association must exist between their two classes; and that association must be navigable in the direction that the message was sent.

4. quote:

What is the difference between Association and Dependency?

My understanding so far was:

If an object of class A has a reference to an object of class B in its attribute structure, it is association.

Robert C. Martin's answer:

Er, well, uh -- hmmm.

That's as good a definition as any I suppose. There are so many different colloquialisms and slangs for UML that I guess it hardly matters any more.

There was a time when an association was the channel between classes over which messages were sent. No message, no association. But that rule has been relaxed by so much conventional usage that I don't think it can hold any more.

Nowadays we seem to use association and aggregation interchangeably to represent a data field (except, of course, that everybody has their own private definition for what the white diamond means.) Dependency if very commonly used to represent an argument passed to a function. This was not the original intent of UML, but it's the way things have turned out.

There was a time when dependency meant that a class knew about another, but did not send messages. Data structures had dependencies on their members because they didn't send them messages, whereas classes had associations with their members because they did send them messages. But that nice separation has gotten so badly muddled that it has become useless.

Perhaps you can read from my tone that I'm pretty disillusioned with UML. Too bad. It could have been a standard. Now, I think its just going to be a confusing compendium of confounding conventions.

5. // From UML 2.0 Superstructure Final Adopted Specification: "An association describes a set of tuples whose values refer to typed instances." (p. 97) "A dependency is a relationship that signifies that a single or a set of model elements requires other model elements for their specification or implementation." (p. 124)

6. 依赖是比关联弱的关系，关联代表一种结构化的关系，体现在生成的代码中，以java为例： 若类A单向关联指向类B，则在类A中存在一个属性B b。 若类A依赖类B，则不会有这个属性，类B的实例可能存在于某个方法调用的参数中，或某个方法的局部变量中。

7. 关联有双向与单向之分，类A与类B双向关联可以是A与B相互可以作为对方的一个attribute，单向的话，就指其中一个类作为另一个类中的 attribute；依赖就只有单向的，不存在attribute的问题，例如类A依赖类B，表示在类A中有三种类B的使用方法：一是类B是全局的，二是类B在类A中实例化，三是类B作为参数被传递

8. 关联是一种结构关系，表现为一个对象能够获得另一个对象的实例引用并调用它的服务 (即使用它）；依赖是一种使用关系，表现为一个对象仅仅是调用了另一个对象的服务。

https://www.cnblogs.com/gaochundong/p/uml_difference_between_dependency_and_association.html
>https://leetschau.github.io/umlzhong-guan-lian-associationhe-yi-lai-dependencyde-qu-bie.html