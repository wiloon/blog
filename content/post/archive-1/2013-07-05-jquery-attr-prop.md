---
title: jquery attr prop
author: wiloon
type: post
date: 2013-07-05T11:23:08+00:00
url: /?p=5615
categories:
  - Web

---

<http://www.candoudou.com/archives/161>

jquery1.6中新加了一个方法prop()，一直没用过它，官方解释只有一句话:获取在匹配的元素集中的第一个元素的属性值。

官方例举的例子感觉和attr()差不多，也不知道有什么区别，既然有了prop()这个新方法，不可能没用吧，那什么时候该用attr()，什么时候该用prop()呢？

大家都知道有的浏览器只要写disabled，checked就可以了，而有的要写成disabled = "disabled"，checked="checked"，比如用attr("checked")获取checkbox的checked属性时选中的时候可以取到值,值为"checked"但没选中获取值就是undefined。

jq提供新的方法“prop”来获取这些属性，就是来解决这个问题的，以前我们使用attr获取checked属性时返回"checked"和"",现在使用prop方法获取属性则统一返回true和false。

那么，什么时候使用attr()，什么时候使用prop()？
  
1.添加属性名称该属性就会生效应该使用prop();
  
2.是有true,false两个属性使用prop();
  
3.其他则使用attr();