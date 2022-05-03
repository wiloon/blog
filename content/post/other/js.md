---
title: inline script 和外链script
author: "-"
date: ""
draft: true
url: /?p=4997

categories:
  - inbox
tags:
  - reprint
---
## inline script 和外链script

  1. 性能

从性能角度来说,inline script 和外链script  (`<script src="xxx" />`)  各有优势。
  
假设你的script只有很少的几行,写在html内确实省去了一个请求。
  
不过用外链方式,最好的情况下可以让浏览器从本地缓存中进行一次IO读取——这只会花2ms。如果谁有兴趣的话我可以解释一下什么情况下会完全读本地缓存,什么情况下是HTTP 304,什么情况下会是全新的HTTP 200. 这些不是重点,结论是 js比较少的时候,在页面上写会有性能优势。

但是随着js代码的增加,这个优势越来越小。你需要衡量的东西也会越来越多:
  
* 外链js对页面加载速度的影响
  
* 内联js对页面加载速度的影响
  
* 外链js被缓存后,用户访问多个页面时能节约的加载时间
  
* 不同页面,新访问用户的比例
  
随着js代码的增加,直接在页面上嵌入script的做法获得的收益越来越小

  1. 维护性

维护性在我看来是优先于性能要考虑的,放在后面说是因为这方面外链script完胜。如果你在页面上写js,分散的js碎片要么迅速膨胀,要么被遗忘而成为隐患。

所以建议js还是写到单独的js文件里面。

再回到楼主的问题, 是否可以或者应该合并到一处？
  
* 是完全可以的,`$(function(){})` 里面的`function`会在`DOMReady`之后才运行,所以放在哪里都可以 (甚至在你要操作的DOM HTML前面)
  
* 是否应该？如果模板是有很多个小模块构成,对应的js文件也尽量和模板放在一起,做模块化的管理。

  <!-- module A -->

a模块的HTML...</div>
<script src="module-a.js"></script>

<!-- module B -->
b模块的HTML</div>
<script src="module-b.js"></script>

(sinatra + haml 用惯了,不习惯rails的静态资源管理方式)

实际上上面这个模板,更好的方式是拆分成a、b两个partial模板了
