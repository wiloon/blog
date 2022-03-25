---
title: Javascript 加载顺序
author: "-"
date: 2014-02-21T06:27:04+00:00
url: /?p=6271
categories:
  - Uncategorized
tags:
  - JavaScript

---
## Javascript 加载顺序
## Javascript加载顺序
http://www.benben.cc/blog/?p=9

最近经常看到别人提及Javascript脚本的加载顺序,看完之后虽略有所悟,但古人云"纸上得来终觉浅,绝知此事要躬行。"这句话云的好,所以我决定亲自测试一下,看看浏览器究竟是怎么加载脚本的。

先看html部分的代码: 

        <script>alert("我是html根节点之外的内部脚本");</script>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>js</title>
	<style type="text/css">body {margin:0;padding:0;}</style>
	<script>alert("我是头部header里的内部脚本");</script>
	<script src="header.js"></script>
	<script src="outer.js"></script>
</head>
<body>
	<script>alert("我是页面body里的内部脚本");</script>
	<script src="body.js"></script>
	<input type="button" value="绑定事件" onclick="javascript:alert('我是body中的按钮,这是我自己绑定的事件');"></input>
</body>
</html>
<script>alert("我是html根节点之外的内部脚本");</script>
      
    
  

再看header.js中的代码: 

  
    
      
        1
      
      
      
        alert("我是header中src外部引用的脚本");
      
    
  

接着是outer.js中的代码: 

  
    
      
              
      
      
        document.write('<script type="text/javascript">');
document.write('alert("我是header中通过外部通过document.write生成的脚本")');
//document.write('<script src="outerouter.js"></script>');
document.write('</script>');
      
    
  

最后是body.js中的代码

  
    
      
        1
      
      
      
        alert("我是body中src外部引用的脚本");
      
    
  

代码的输出顺序如下: 
  
    alert("我是html根节点之外的内部脚本");
alert("我是头部header里的内部脚本");
alert("我是header中src外部引用的脚本");
alert("我是header中通过外部通过document.write生成的脚本");
alert("我是页面body里的内部脚本");
alert("我是body中src外部引用的脚本");
alert("我是html根节点之外的内部脚本");
最后只有点击按钮才会触发alert('我是body中的按钮,这是我自己绑定的事件');
  

刚开始看完代码后你觉得加载顺序如何呢？其实很简单,浏览器加载的时候完全是按照自上而下顺序加载的,遇到外部引用就暂时跳出到外部js中执行,执行完毕后返回跳出的位置继续向下执行,而且经测试可以看到,按钮是在body.js执行完毕后才显示在页面中的,这也证实了浏览器是顺序加载的。

这里需要说明两点: 
  
1. 浏览器根节点之外是不允许有任何元素的,在这里我们只是为了判断加载顺序才写了不符合规矩的代码,这一点可以在chrome的调试中看到报错。
  
2. outer.js中通过document.write再次引用外部js的那一行我已经做了注释,虽然此方法有许多人证实可行,但是在我的环境下会报脚本错误,而且这样做会引起浏览器加载顺序的不兼容 (详情可见: [Javascript加载顺序的BUG][1]) ,因此在实际应用中若非迫不得已还是少用为妙。

 [1]: http://uicss.cn/javascript-load-order/