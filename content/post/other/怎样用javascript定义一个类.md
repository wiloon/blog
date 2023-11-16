---
title: 怎样用Javascript定义一个类
author: "-"
date: 2014-02-25T05:40:45+00:00
url: /?p=6282
categories:
  - JavaScript
tags:
  - JavaScript

---
## 怎样用Javascript定义一个类
http://www.cnblogs.com/xcj26/archive/2013/04/08/3006023.html

其实Javascript中没有类这个定义,但是有类这个概念。很多人都写过这样的代码,对,没错,就是如下代码,清晰的不能再清晰了,就是一个关键字 function,然后定义一个方法名,方法名后紧跟一对括号。如果你在项目中写过这样的代码,那么祝贺你,你可以不费任何吹毛之力,就能一口气读完这篇博文了.

  function Print() {
     ……
 }

当我们在写c#代码,焦头烂额,无从下手的时候,至少我们还是可以厚着脸皮在老板的面前,敲出华丽的 class \***{},是的,没错,就这几个字符。殊不知这这几个字符体现出来的境界。说浅些,我会敲键盘写代码,说深些,我有可能理解了面向对象的编程,至少我会定义一个类。是这样的,c#中定义一个类是用class。

有一天,老板变态了,让我用Javascript来定义一个类,我无从下手呀,我平时都是用("."),("#")的人物呀,思考良久,我还模糊的记的document.getElementById("")这个东西,但是好像与Javascript的类扯不上关系呀。怎么办？问了google问百度啊,最后在一个角落,找到了定义Javascript类的E文。仔细一阅,难道这是一个坑吗？明明用function定义了一个方法,活生生的把它说成一个类,反复几次Google百度后,有点怀疑了,难道Javascript中定义一个类,真的是用function？其实没错,在Javascript中,定义一个类是用fucntion() \*\\*\*{}。不管是在学校的菜鸟,还是国外的顶级程序员,在这件事上是平等的,想定义一个Javascript的类,就必须得先敲下function \*\**(){}。

在定义Javascript类上,表现形势上大家虽然是平等的,都是用function \***(){}。但实质上,确是蕴含着大量的学问。也许有些朋友到目前为止,是不是感觉我说的太简单了,那我们就在这个function上玩点花样。

  function Dog(category, name, age) {
    this.Category = category;
    this.Name = name;
    this.Age = age;
}

一个Javascript类就这样定义完成了,现在就可以自豪的说,我会面向对象的手法编定Javascript代码了。

类定义好了,那我们怎么样来用这个类呢?其实用法和C#的用法很像。

  var dog01 = new Dog("狗类", "土狗", 2);
var dog02 = new Dog("狗类", "黄狗", 5);

有些朋友要拍砖了,这么简单的东西,都拿出来说,那我们不妨再来进阶一下。我上边的代码,实例化了两个对象,一个是dog01,dog01下边那个是dog02。因为dog01的Cateogry太口语化了,我要修改为dog01.Categry = '犬类',这样听起来是不是舒服多了,这是一个很简单的事,我们仅仅需要为dog01的Cateogry重赋值就可以了。我们修改了dog01的Cateory, dog02的Category会跟着变吗？答案是肯定的,不会变,如果有变,肯定有鬼。那我们有没有方法让dog01,dog02这些对象的Cateogry属性共用起来呢？也就是说当我修改了Category属性,不管是dog01,还是dog02都跟一样的变,我们不妨来这样写写。
  
    <img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" />
  
  function Dog(name,age) {
    this.Name = "";
    this.Age = "";
}
Dog.prototype.Category = "狗类";
var dog01 = new Dog("土狗",2);
var dog02 = new Dog("黄狗",5);
alert(dog01.Category);
alert(dog02.Category);
Dog.prototype.Category = "犬类";
alert(dog01.Category);
alert(dog02.Category);
  
    <img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" />
  

当我们修改Dog.prototype.Category的时候,dog01,dog02的属性都跟着神奇的变了。是不是有点类似于C#中的static。

当你已经耐心的看到这儿的时候,我相信对朝九晚五的写("."),("#")的朋友指明了一个方向。如果我写的这些你已经知道了,你可以去看看阮一峰写的 Javascript定义类的几种方法: [http://www.ruanyifeng.com/blog/2012/07/three_ways_to_define_a_javascript_class.html][1]

[http://www.cnblogs.com/v10258/archive/2013/05/20/3065247.html](http://www.cnblogs.com/v10258/archive/2013/05/20/3065247.html)


 [1]: http://www.ruanyifeng.com/blog/2012/07/three_ways_to_define_a_javascript_class.html