---
title: Sizzle
author: "-"
date: 2014-02-19T06:51:58+00:00
url: /?p=6262
categories:
  - Uncategorized
tags:
  - JQuery

---
## Sizzle
这是一篇关于介绍jQuery Sizzle选择器的文章，由我和obility共同完成。在文中，我们试图用自己的语言配以适量的代码向读者展现出Sizzle在处理选择符时的流程原理，以及末了以少许文字给你展示出如何借用Sizzle之手实现自定义选择器 (也许更标准的叫法叫做过滤符) 和它与YUI 选择器的大致比较。

### **前序**

jQuery相比1.2的版本，在内部代码的构造上已经出现了巨大的变化，其之一便是模块的分发.我记得09年在jquery 9月开的一次大会上 john放出的一张ppt上 也指出了当前的jquery下一步目标，不仅仅是除了sizzle选择器的分离，届时core，attribute，css以及manipulation，包括event也都会独立成单独的js文件. (1.4的文件结构，其实已经分成单独的[16][1]个模块的组成) 

随着jQuery被用来构建web app的场合愈来愈多，它的性能自然受到了大部分开发者的高度关注，它的内部实现机理又是如何，比如选择器的实现。

[Sizzle][2]，作为一个独立全新的选择器引擎，出现在jQuery 1.3版本之后，并被John Resig作为一个开源的项目，可以用于其他框架: Mool, Dojo，YUI等。

好了，现在来看为什么Sizzle选择器如此受欢迎，使它能够在[常用dom匹配][3]上都快于其他选择器而让这些框架们都垂青于它。


### **概要**

一般选择器的匹配模式 (包括jq1.2之前) ，都是一个顺序的思维方式，在需要递进式匹配时，比如$('div span') 这样的匹配时，执行的操作都是先匹配页面中div然后再匹配它的节点下的span标签，之后返回结果。

Sizzle则采取了相反Right To Left的实现方式，先搜寻页面中所有的span标签，再其后的操作中才去判断它的父节点 (包括父节点以上) 是否为div，是则压入数组，否则pass，进入下一判断，最后返回该操作序列。

另外，在很多细节上也进行了优化。

 [1]: http://github.com/jquery/jquery/tree/master/src
 [2]: http://sizzlejs.com/
 [3]: http://ejohn.org/blog/selectors-that-people-actually-use/