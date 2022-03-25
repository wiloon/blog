---
title: Static Nested Class, Inner Class, Anonymous Inner Class
author: "-"
date: 2012-09-21T07:12:51+00:00
url: /?p=4155
categories:
  - Java

tags:
  - reprint
---
## Static Nested Class, Inner Class, Anonymous Inner Class
### Inner Class (内部类) 定义在类中的类。
Nested Class (嵌套类) 是静态 (static) 内部类。
1. 要创建嵌套类的对象，并不需要其外围类的对象。  
2. 不能从嵌套类的对象中访问非静态的外围类对象。

Anonymous Inner Class  (匿名内部类) 匿名的内部类是没有名字的内部类。

匿名的内部类不能extends (继承) 其它类，但一个内部类可以作为一个接口，由另一个内部类实现。

嵌套类可以作为接口的内部类。正常情况下，你不能在接口内部放置任何代码，但嵌套类可以作为接口的一部分，因为它是static 的。只是将嵌套类置于接口的命名空间内，这并不违反接口的规则。

内部类被继承,由于内部类有一个指向外围类对象的秘密引用，所以在继承内部类的时候，该秘密引用必须被初始化。解决方法是enclosingClassReference.super();语法，看一下代码: 


class Outer
{
 class Inner
 {
 }
 }
 class AnoClass extends Outer.Inner
 {
 AnoClass (Outer wi)
 {
 wi.super();
 }
}

### 匿名类 (Anonymous Class) 
当一个内部类的类声名只是在创建此类对象时用了一次，而且要产生的新类需继承于一个已有的父类或实现一个接口，才能考虑用匿名类，由于匿名类本身无名，因此它也就不存在构造方法，它需要显示地调用一个无参的父类的构造方法，并且重写父类的方法。

```java
f.addMouseMotionListener(new MouseMotionAdapter(){ //匿名类开始
public void mouseDragged(MouseEvent e){
 String s="Mouse dragging: x="+e.getX()+"Y="+e.getY();
 tf.setText(s); }
 } ); //匿名类结束
```

存在它的原因是:
1. 一个内部类的对象能够访问创建它的对象的实现，包括私有数据。即内部类实例对包含它的哪个类的实例来说，是特权的。
2. 对于同一个包中的其他类来说,内部类能够隐藏起来,换句话说，内部类不管方法的可见性如何，那怕是public，除了包容类，其他类都无法使用它。
3. 匿名内部类可以很方便的定义回调。
4. 使用内部类可以非常方便的编写事件驱动程序。
  
其实它真正的目的仅仅为了定义回调－－进一步就是事件驱动。

在使用匿名内部类时，要记住以下几个原则: 
- 匿名内部类不能有构造方法。
- 匿名内部类不能定义任何静态成员、方法和类。
- 匿名内部类不能是 public,protected,private,static。
- 只能创建匿名内部类的一个实例。
- 一个匿名内部类一定是在new的后面，用其隐含实现一个接口或实现一个类。
- 因匿名内部类为局部内部类，所以局部内部类的所有限制都对其生效。  

匿名类和内部类中的中的this :
有时候，我们会用到一些内部类和匿名类。当在匿名类中用this时，这个this则指的是匿名类或内部类本身。 这时如果我们要使用外部类的方法和变量的话，则应该加上外部类的类名。