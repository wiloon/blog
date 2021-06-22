---
title: 'jQuery  setInterval，setTimeout'
author: "-"
type: post
date: 2012-09-15T15:14:37+00:00
url: /?p=4041
categories:
  - Uncategorized

---
  
    <a href="http://hi.baidu.com/ruhaole/item/65ed5df334b3080985d278aa">http://hi.baidu.com/ruhaole/item/65ed5df334b3080985d278aa</a>
  
  
    <em>sliderIntervalID = setInterval(show,3000);</em>
  
  
    clearInterval(sliderIntervalID);
  

<div id="content">
  
    当遇到setInterval,setTimeout与jquery混用的问题 时，直接按JavaScript中的语法写并不起作用，有以下两种解决方法。
  
  
    方法1. 直接在ready中调用其他方法，会提示缺少对象的错误，应用jQuery的扩展可以解决这个问题。
  
  
    <em>$(document).ready(function(){</em>
  
  
    <em>$.extend({
 show:function(){
 alert("ready");
 }
 });
 setInterval("$.show()",3000);
 });</em>
  
  
    方法2. 指定定时执行的函数时不要使用引号和括号。
  
  
    <em>function show(){
 alert("ready");
 }
 setInterval(show,3000);// 注意函数名没有引号和括弧！</em>
  
  
    <em>-------</em>
  
  
    setTimeout(表达式,延迟时间); 单位:ms(毫秒)；1s=1000ms;
  
  
    setInterval(表达式,交 互时间);　 单位:ms(毫秒)；1s=1000ms;
  
  
    window.setTimeout()
  
  
    在执行时，它从载入后延迟指定的时间去执行一个表达式或者是函数;仅执行一次;和window.clearTimeout一起使用.
  
  
    window.setInterval()
  
  
    在执行时,它从载入页面后每隔指定的时间执行一个表达式或者是函数;(功能类似于递归函数)；和window.clearInterval一起使用.
  
  
    1，基本用法：
  
  
    执行一段代码：　 var i=0;
  
  
    setTimeout("i+=1;alert(i)",1000);
  
  
    执行一个函数：
  
  
    var i=0;
  
  
    setTimeout(function(){i+=1;alert(i);},1000);
  
  
    //注意比较上面的两种方法的不同。
  
  
    下面再来一个执行函数的：
  
  
    <code>　 var i=0;

function test(){

i+=1;

alert(i);

}

setTimeout("test()",1000);

也可以这样：

setTimeout(test,1000);</code>
  
  
    总结：
  
  
    setTimeout的原型是这样的：
  
  
    iTimerID = window.setTimeout(vCode, iMilliSeconds [, sLanguage])
  
  
    setTimeout 有两种形式
  
  
    setTimeout(code,interval)
  
  
    setTimeout(func,interval,args)
  
  
    其中code是一个字符串
  
  
    func是一个函数.
  
  
    注意"函数"的意义,是一个表达式,而不是一个语句.
  
  
    比如你想周期性执行一个函数
  
  
    <code>　function a(){

//...

}</code>
  
  
    可写为
  
  
    setInterval("a()",1000)
  
  
    或
  
  
    setInterval(a,1000)
  
  
    这里 注意第二种形式中,是a,不要写成a(),切记!!!
  
  
    展开来说,不管你这里写的是什么,如果是一个变量,一定是一个指向某函数的变量; 如果是个函数,那它的返回值就　要是个函数
  
  
    2,用setTimeout实现setInterval的功能
  
  
    思路很简 单，就是在一个函数中调用不停执行自己，有点像递归
  
  
    <code>　　var i=0;

function xilou(){

i+=1;

if(i>10){alert(i);return;}

setTimeout("xilou()",1000);

//用这个也可以

//setTimeout(xilou,1000);

}</code>
  
  
    3,在类中使用setTimeout
  
  
    终于到正题了，其实在类中使用大家遇到的问题都是关于this的，只要解决了这个this的问题就万事无忧了。
  
  
    呵呵。让我们来分析一 下：
  
  
    <code>　　function xilou(){

//by 西楼冷月 www.chinacms.org

this.name="xilou";

this.sex="男";

this.num=0;

}

xilou.prototype.count=function(){

this.num+=1;

alert(this.num);

if(this.num>10){return;}

//下面用四种方法测试,一 个一个轮流测试。

setTimeout("this.count()",1000);//A:当下面的x.count()调用时会发生错 误：对象不支持此属性或方法。

setTimeout("count()",1000);//B:错误显示：缺少对象

setTimeout(count,1000);//C:错误显示：'count'未定义

//下面是第四种 by 西楼冷月 www.chinacms.org

var self=this;

setTimeout(function() {self.count();},1000);//D:正确</code>
  
  
    }
  
  
    var x=new xilou();
 x.count();
  
  
    错误分析：
  
  
    A：中的this其实指是window 对象，并不是指当前实例对象
  
  
    B：和C：中的count()和count其实指的是单独的一个名为count()的函数,但也可以是 window.count(),因为window.count()可以省略为count()
  
  
    D：将变量self指向当前实例对象，这样 js解析引擎就不会混肴this指的是谁了。
  
  
    话说回来，虽然我们知道setTimeout("this.count()",1000) 中的this指的是window对象，但还是不明白为什么会是
  
  
    window对象^_^(有点头晕...)
  
  
    那我们可以 想象一下这个setTimeout是怎样被定义的：
  
  
    setTimeout是window的一个方法，全称是这样 的：window.setTimeout()
  
  
    那应该是这样被定义的：
  
  
    <code>　　 window.setTimeout=function(vCode, iMilliSeconds [, sLanguage]){

//.....代码

return timer//返回一个标记符

}

</code>　　所以当向 setTimeout()传入this的时候，当然指的是它所属的当前对象window了。
  
