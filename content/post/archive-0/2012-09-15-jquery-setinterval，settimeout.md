---
title: 'jQuery  setInterval，setTimeout'
author: wiloon
type: post
date: 2012-09-15T15:14:37+00:00
url: /?p=4041
categories:
  - Uncategorized

---
<div>
  <p>
    <a href="http://hi.baidu.com/ruhaole/item/65ed5df334b3080985d278aa">http://hi.baidu.com/ruhaole/item/65ed5df334b3080985d278aa</a>
  </p>
  
  <p>
    <em>sliderIntervalID = setInterval(<strong>show</strong>,3000);</em>
  </p>
  
  <p>
    clearInterval(sliderIntervalID);
  </p>
</div>

<div id="content">
  <p>
    当遇到setInterval,setTimeout与jquery混用的问题 时，直接按JavaScript中的语法写并不起作用，有以下两种解决方法。
  </p>
  
  <p>
    <strong>方法1.</strong> 直接在ready中调用其他方法，会提示缺少对象的错误，应用jQuery的扩展可以解决这个问题。
  </p>
  
  <p>
    <em>$(document).ready(function(){</em>
  </p>
  
  <p>
    <em>$.extend({
 show:function(){
 alert("ready&#8221;);
 }
 });
 setInterval("$.show()&#8221;,3000);
 });</em>
  </p>
  
  <p>
    <strong>方法2.</strong> 指定定时执行的函数时不要使用引号和括号。
  </p>
  
  <p>
    <em>function show(){
 alert("ready&#8221;);
 }
 setInterval(<strong>show</strong>,3000);// 注意函数名没有引号和括弧！</em>
  </p>
  
  <p>
    <em>&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-</em>
  </p>
  
  <p>
    setTimeout(表达式,延迟时间); 单位:ms(毫秒)；1s=1000ms;
  </p>
  
  <p>
    setInterval(表达式,交 互时间);　 单位:ms(毫秒)；1s=1000ms;
  </p>
  
  <p>
    window.setTimeout()
  </p>
  
  <p>
    在执行时，它从载入后延迟指定的时间去执行一个表达式或者是函数;仅执行一次;和window.clearTimeout一起使用.
  </p>
  
  <p>
    window.setInterval()
  </p>
  
  <p>
    在执行时,它从载入页面后每隔指定的时间执行一个表达式或者是函数;(功能类似于递归函数)；和window.clearInterval一起使用.
  </p>
  
  <p>
    1，基本用法：
  </p>
  
  <p>
    执行一段代码：　 var i=0;
  </p>
  
  <p>
    setTimeout("i+=1;alert(i)&#8221;,1000);
  </p>
  
  <p>
    执行一个函数：
  </p>
  
  <p>
    var i=0;
  </p>
  
  <p>
    setTimeout(function(){i+=1;alert(i);},1000);
  </p>
  
  <p>
    //注意比较上面的两种方法的不同。
  </p>
  
  <p>
    下面再来一个执行函数的：
  </p>
  
  <p>
    <code>　 var i=0;&lt;br />
function test(){&lt;br />
i+=1;&lt;br />
alert(i);&lt;br />
}&lt;br />
setTimeout("test()",1000);&lt;br />
也可以这样：&lt;br />
setTimeout(test,1000);</code>
  </p>
  
  <p>
    总结：
  </p>
  
  <p>
    setTimeout的原型是这样的：
  </p>
  
  <p>
    iTimerID = window.setTimeout(vCode, iMilliSeconds [, sLanguage])
  </p>
  
  <p>
    setTimeout 有两种形式
  </p>
  
  <p>
    setTimeout(code,interval)
  </p>
  
  <p>
    setTimeout(func,interval,args)
  </p>
  
  <p>
    其中code是一个字符串
  </p>
  
  <p>
    func是一个函数.
  </p>
  
  <p>
    注意&#8221;函数&#8221;的意义,是一个表达式,而不是一个语句.
  </p>
  
  <p>
    比如你想周期性执行一个函数
  </p>
  
  <p>
    <code>　function a(){&lt;br />
//...&lt;br />
}</code>
  </p>
  
  <p>
    可写为
  </p>
  
  <p>
    setInterval("a()&#8221;,1000)
  </p>
  
  <p>
    或
  </p>
  
  <p>
    setInterval(a,1000)
  </p>
  
  <p>
    这里 注意第二种形式中,是a,不要写成a(),切记!!!
  </p>
  
  <p>
    展开来说,不管你这里写的是什么,如果是一个变量,一定是一个指向某函数的变量; 如果是个函数,那它的返回值就　要是个函数
  </p>
  
  <p>
    2,用setTimeout实现setInterval的功能
  </p>
  
  <p>
    思路很简 单，就是在一个函数中调用不停执行自己，有点像递归
  </p>
  
  <p>
    <code>　　var i=0;&lt;br />
function xilou(){&lt;br />
i+=1;&lt;br />
if(i&gt;10){alert(i);return;}&lt;br />
setTimeout("xilou()",1000);&lt;br />
//用这个也可以&lt;br />
//setTimeout(xilou,1000);&lt;br />
}</code>
  </p>
  
  <p>
    3,在类中使用setTimeout
  </p>
  
  <p>
    终于到正题了，其实在类中使用大家遇到的问题都是关于this的，只要解决了这个this的问题就万事无忧了。
  </p>
  
  <p>
    呵呵。让我们来分析一 下：
  </p>
  
  <p>
    <code>　　function xilou(){&lt;br />
//by 西楼冷月 www.chinacms.org&lt;br />
this.name="xilou";&lt;br />
this.sex="男";&lt;br />
this.num=0;&lt;br />
}&lt;br />
xilou.prototype.count=function(){&lt;br />
this.num+=1;&lt;br />
alert(this.num);&lt;br />
if(this.num&gt;10){return;}&lt;br />
//下面用四种方法测试,一 个一个轮流测试。&lt;br />
setTimeout("this.count()",1000);//A:当下面的x.count()调用时会发生错 误：对象不支持此属性或方法。&lt;br />
setTimeout("count()",1000);//B:错误显示：缺少对象&lt;br />
setTimeout(count,1000);//C:错误显示：'count'未定义&lt;br />
//下面是第四种 by 西楼冷月 www.chinacms.org&lt;br />
var self=this;&lt;br />
setTimeout(function() {self.count();},1000);//D:正确</code>
  </p>
  
  <p>
    }
  </p>
  
  <p>
    var x=new xilou();
 x.count();
  </p>
  
  <p>
    错误分析：
  </p>
  
  <p>
    A：中的this其实指是window 对象，并不是指当前实例对象
  </p>
  
  <p>
    B：和C：中的count()和count其实指的是单独的一个名为count()的函数,但也可以是 window.count(),因为window.count()可以省略为count()
  </p>
  
  <p>
    D：将变量self指向当前实例对象，这样 js解析引擎就不会混肴this指的是谁了。
  </p>
  
  <p>
    话说回来，虽然我们知道setTimeout("this.count()&#8221;,1000) 中的this指的是window对象，但还是不明白为什么会是
  </p>
  
  <p>
    window对象^_^(有点头晕&#8230;)
  </p>
  
  <p>
    那我们可以 想象一下这个setTimeout是怎样被定义的：
  </p>
  
  <p>
    setTimeout是window的一个方法，全称是这样 的：window.setTimeout()
  </p>
  
  <p>
    那应该是这样被定义的：
  </p>
  
  <p>
    <code>　　 window.setTimeout=function(vCode, iMilliSeconds [, sLanguage]){&lt;br />
//.....代码&lt;br />
return timer//返回一个标记符&lt;br />
}&lt;br />
</code>　　所以当向 setTimeout()传入this的时候，当然指的是它所属的当前对象window了。
  </p>
</div>