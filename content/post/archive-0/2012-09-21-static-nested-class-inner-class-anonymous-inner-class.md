---
title: Static Nested Class, Inner Class, Anonymous Inner Class
author: wiloon
type: post
date: 2012-09-21T07:12:51+00:00
url: /?p=4155
categories:
  - Java

---
<span style="font-size: medium;"><span style="font-family: 'Times New Roman';"> Inner Class</span>（内部类）定义在类中的类。</span>

<span style="font-size: medium;"><span style="font-family: 'Times New Roman';">Nested Class</span>（嵌套类）是静态（<span style="font-family: 'Times New Roman';">static</span>）内部类。<span style="font-family: 'Times New Roman';">1. </span>要创建嵌套类的对象，并不需要其外围类的对象。<span style="font-family: 'Times New Roman';">  2. </span>不能从嵌套类的对象中访问非静态的外围类对象。</span>

<span style="font-size: medium;"><span style="font-family: 'Times New Roman';">Anonymous Inner Class </span>（匿名内部类）匿名的内部类是没有名字的内部类。</span>

<span style="font-size: medium;">匿名的内部类不能<span style="font-family: 'Times New Roman';">extends</span>（继承）其它类，但一个内部类可以作为一个接口，由另一个内部类实现。</span>

<span style="font-size: medium;">嵌套类可以作为接口的内部类。正常情况下，你不能在接口内部放置任何代码，但嵌套类可以作为接口的一部分，因为它是<span style="font-family: 'Times New Roman';">static </span>的。只是将嵌套类置于接口的命名空间内，这并不违反接口的规则。</span>

<span style="font-size: medium;">内部类被继承<span style="font-family: 'Times New Roman';">,</span>由于内部类有一个指向外围类对象的秘密引用，所以在继承内部类的时候，该秘密引用必须被初始化。解决方法是<span style="font-family: 'Times New Roman';">enclosingClassReference.super();</span>语法，看一下代码：</span>

<p align="left">
  class Outer<br /> {<br /> class Inner<br /> {<br /> }<br /> }<br /> class AnoClass extends Outer.Inner<br /> {<br /> AnoClass (Outer wi)<br /> {<br /> wi.super();<br /> }<br /> }
</p>

<span style="font-size: medium;">匿名类（<span style="font-family: 'Times New Roman';">Anonymous Class</span>）</span>
  
<span style="font-size: medium;">　　当一个内部类的类声名只是在创建此类对象时用了一次，而且要产生的新类需继承于一个已有的父类或实现一个接口，才能考虑用匿名类，由于匿名类本身无名，因此它也就不存在构造方法，它需要显示地调用一个无参的父类的构造方法，并且重写父类的方法。</span>

<span style="font-size: medium;">。。。。。。。。。。。。</span>

<span style="font-size: medium;"><span style="font-family: 'Times New Roman';">f.addMouseMotionListener(new MouseMotionAdapter(){ //</span>匿名类开始</span>
  
<span style="font-size: medium;">　　　　　　　</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';">public void mouseDragged(MouseEvent e){<br /> </span>　　　　　　　　</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';">String s=&#8221;Mouse dragging: x=&#8221;+e.getX()+&#8221;Y=&#8221;+e.getY();<br /> </span>　　　　　　　　</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';">tf.setText(s); }<br /> </span>　　　　　　<span style="font-family: 'Times New Roman';">} ); //</span>匿名类结束</span>

<span style="font-size: medium;">　　存在它的原因是</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';">:<br /> </span>　　<span style="font-family: 'Times New Roman';">1.</span>一个内部类的对象能够访问创建它的对象的实现，包括私有数据。即内部类实例对包含它的哪个类的实例来说，是特权的。</span>
  
<span style="font-size: medium;">　　<span style="font-family: 'Times New Roman';">2.</span>对于同一个包中的其他类来说<span style="font-family: 'Times New Roman';">,</span>内部类能够隐藏起来<span style="font-family: 'Times New Roman';">,</span>换句话说，内部类不管方法的可见性如何，那怕是<span style="font-family: 'Times New Roman';">public</span>，除了包容类，其他类都无法使用它。</span>
  
<span style="font-size: medium;">　　<span style="font-family: 'Times New Roman';">3.</span>匿名内部类可以很方便的定义回调。</span>
  
<span style="font-size: medium;">　　<span style="font-family: 'Times New Roman';">4.</span>使用内部类可以非常方便的编写事件驱动程序。</span>
  
<span style="font-size: medium;">其实它真正的目的仅仅为了定义回调－－进一步就是事件驱动。</span>

<span style="font-size: medium;">　在使用匿名内部类时，要记住以下几个原则：</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> </span>　　<span style="font-family: 'Times New Roman';">·</span>匿名内部类不能有构造方法。</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> </span>　　<span style="font-family: 'Times New Roman';">·</span>匿名内部类不能定义任何静态成员、方法和类。</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> </span>　　<span style="font-family: 'Times New Roman';">·</span>匿名内部类不能是<span style="font-family: 'Times New Roman';">public,protected,private,static</span>。</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> </span>　　<span style="font-family: 'Times New Roman';">·</span>只能创建匿名内部类的一个实例。</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> ·</span>一个匿名内部类一定是在<span style="font-family: 'Times New Roman';">new</span>的后面，用其隐含实现一个接口或实现一个类。</span><span style="font-size: medium;"><span style="font-family: 'Times New Roman';"><br /> </span>　　<span style="font-family: 'Times New Roman';">·</span>因匿名内部类为局部内部类，所以局部内部类的所有限制都对其生效。<span style="font-family: 'Times New Roman';">  </span></span>

<span style="font-size: medium;">匿名类和内部类中的中的<span style="font-family: 'Times New Roman';">this :</span></span>
  
<span style="font-family: 'Times New Roman'; font-size: medium;"> </span><span style="font-size: medium;">有时候，我们会用到一些内部类和匿名类。当在匿名类中用<span style="font-family: 'Times New Roman';">this</span>时，这个<span style="font-family: 'Times New Roman';">this</span>则指的是匿名类或内部类本身。<span style="font-family: 'Times New Roman';"> </span>这时如果我们要使用外部类的方法和变量的话，则应该加上外部类的类名。</span>