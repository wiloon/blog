---
title: jquery获取父元素、父节点–parents()与closest()
author: wiloon
type: post
date: 2013-11-11T04:49:30+00:00
url: /?p=5948
categories:
  - Uncategorized
tags:
  - JavaScript

---
先看个简单的例子，呵呵

&nbsp;

<ul class=&#8221;box&#8221; name=&#8221;a&#8221;>

<li name=&#8221;b&#8221; class=&#8221;li_moito&#8221;><p><a href=&#8221;#&#8221; class=&#8221;moto&#8221;>Hello Moto*</a></p></li>

<li><p><a href=&#8221;#&#8221; class=&#8221;kitty&#8221;>Hello Kitty*</a></p></li>

<li><p><a href=&#8221;#&#8221; class=&#8221;world&#8221;>Hello World*</a></p></li>

</ul>

&nbsp;

如果要获取class=&#8221;moto&#8221;的父级元素LI，或许我们最先想到的一种方法就是用

&nbsp;

$(&#8220;.moto&#8221;).parent().parent()。不错，这样写可以达到效果，却也显得有些烦琐了。其

&nbsp;

实想要获取父级标签还有另外两种方法的，即parents()与closest()。

&nbsp;

**parents()方法：**

parents()，我想这个大家再熟悉不过了，它是取得所有符合条件的祖先元素（不包括本

&nbsp;

身），这是一个集合，呵呵。后面可以通过一个可选元素来逐个筛选。

这里，我们可以：

$(&#8220;.moto&#8221;).parents(&#8220;li[name=&#8217;b&#8217;]&#8221;);

或者

$(&#8220;.moto&#8221;).parents(&#8220;.li_moito&#8221;);

&nbsp;

**closest()方法：**

closest()，这个方法呢就是向上检查元素并逐级匹配。首先，会从自身来匹配，匹配成

&nbsp;

功就返回本身；不成功则向上寻找，直到找到匹配的选择器为止。最后，如果神马也没

&nbsp;

找到，那就只好返回一个jquery的空对象喽……

可以这样写：

$(&#8220;.moto&#8221;).closest(&#8220;li[name=&#8217;b&#8217;]&#8221;);

或者

$(&#8220;.moto&#8221;).closest(&#8220;.li_moito&#8221;);

&nbsp;

乍看一眼，两者的用法还挺相似的，呵呵！下面我们比较一下他们的区别：

**区分parents()与closest()**

1、前者从父级开始匹配元素；而后者是从自身开始。

2、前者向上查找所有的父级元素，直至根元素，然后把这些查找的结果放到一个临时

的集合中，再通过额定的条件来进行筛选；后者是从自身元素开始向上查找，直到找到

&nbsp;

有效的匹配元素就停止。

3、前者返回元素值可以有0个、1个，或者是多个；后者只有0个或1个；

&nbsp;

本文参考资源：

<a href="http://www.cnblogs.com/weixing/archive/2012/03/20/2407618.html" target="_blank">http://www.cnblogs.com/weixing/archive/2012/03/20/2407618.html</a>

<http://hi.baidu.com/zhangqian04062/item/4f4656f5d3ef6743922af27a>