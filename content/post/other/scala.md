---
title: Scala
author: "-"
date: 2013-11-29T15:17:11+00:00
url: scala
categories:
  - Uncategorized
tags:
  - Java

---
## Scala

发音为/ˈskɑːlə, ˈskeɪlə/

Java VS Scala
从定义上来说，Java是面向对象的编程语言，而Scala是函数式编程语言，这两门语言之间，本身也有一定的关联。

Scala来源于Java，又“高于”Java，在Java之上增加了一层编码的“API”，让程序员可以通过函数式编程的方式来开发程序。

Scala程序最终被编译为.class文件运行在JVM虚拟机中，所以它是JVM下的语言一种，在实际的大数据开发任务当中，Java和Scala都运行于JVM之上，也能更好地集成。


Scala编程语言近来抓住了很多开发者的眼球。如果你粗略浏览Scala的网站，你会觉得Scala是一种纯粹的面向对象编程语言，而又无缝地结合了命令式和函数式的编程风格。Christopher Diggins认为: 


  不太久之前编程语言还可以毫无疑义地归类成"命令式"或者"函数式"。Scala代表了一个新的语言品种，它抹平了这些人为划分的界限。


  根据David Rupp在博客中的说法，Scala可能是下下一代Java。这么高的评价让人不禁想看看它到底是什么东西。


  Scala有几项关键特性表明了它的面向对象的本质。例如，Scala中的每个值都是一个对象，包括基本数据类型 (即布尔值、数字等) 在内，连函数也是对象。另外，类可以被子类化，而且Scala还提供了基于mixin的组合 (mixin-based composition) 。


  与只支持单继承的语言相比，Scala具有更广泛意义上的类重用。Scala允许定义新类的时候重用"一个类中新增的成员定义 (即相较于其父类的差异之处) "。Scala称之为mixin类组合。


  Scala还包含了若干函数式语言的关键概念，包括高阶函数 (Higher-Order Function) 、局部套用 (Currying) 、嵌套函数 (Nested Function) 、序列解读 (Sequence Comprehensions) 等等。


  Scala是静态类型的，这就允许它提供泛型类、内部类、甚至多态方法 (Polymorphic Method) 。另外值得一提的是，Scala被特意设计成能够与Java和.NET互操作。Scala当前版本还不能在.NET上运行 (虽然上一版可以-_-b) ，但按照计划将来可以在.NET上运行。


  Scala可以与Java互操作。它用scalac这个编译器把源文件编译成Java的class文件 (即在JVM上运行的字节码) 。你可以从Scala中调用所有的Java类库，也同样可以从Java应用程序中调用Scala的代码。用David Rupp的话来说，


  它也可以访问现存的数之不尽的Java类库，这让 (潜在地) 迁移到Scala更加容易。


  这让Scala得以使用为Java1.4、5.0或者6.0编写的巨量的Java类库和框架，Scala会经常性地针对这几个版本的Java进行测试。Scala可能也可以在更早版本的Java上运行，但没有经过正式的测试。Scala以BSD许可发布，并且数年前就已经被认为相当稳定了。


  说了这么多，我们还没有回答一个问题: "为什么我要使用Scala？"Scala的设计始终贯穿着一个理念: 


  创造一种更好地支持组件的语言。 (《The Scala Programming Language》，Donna Malayeri) 


  也就是说软件应该由可重用的部件构造而成。Scala旨在提供一种编程语言，能够统一和一般化分别来自面向对象和函数式两种不同风格的关键概念。

>https://cloud.tencent.com/developer/article/1758874