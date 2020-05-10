---
title: Javascript 重定向 window.location.href / replace / reload()
author: wiloon
type: post
date: 2014-03-03T02:41:06+00:00
url: /?p=6309
categories:
  - Uncategorized
tags:
  - JavaScript

---
<div class="line number1 index0 alt2">
  <pre>location.href，可以点击浏览器的后退按钮返回本页。

location.assign(URL)
assign() 方法可加载一个新的文档。效果与location.href相当。</pre>
  
  <pre>location.reload(force)</pre>
  
  <p>
    如果该方法没有规定参数，或者参数是 false，它就会用 HTTP 头 If-Modified-Since 来检测服务器上的文档是否已改变。如果文档已改变，reload() 会再次下载该文档。如果文档未改变，则该方法将从缓存中装载文档。这与用户单击浏览器的刷新按钮的效果是完全一样的。
  </p>
  
  <p>
    如果把该方法的参数设置为 true，那么无论文档的最后修改日期是什么，它都会绕过缓存，从服务器上重新下载该文档。这与用户在单击浏览器的刷新按钮时按住 Shift 健的效果是完全一样。
  </p>
  
  <pre>location.replace(newURL)
不能点击浏览区的后退按钮返回本页。</pre>
</div>

将地址替换成新url，该方法通过指定URL替换当前缓存在历史里（客户端）的项目，
  
因此当使用replace方法之后，你不能通过“前进”和“后 退”来访问已经被替换的URL，这个特点对于做一些过渡页面非常有用！

replace() 方法不会在 History 对象中生成一个新的记录。当使用该方法时，新的 URL 将覆盖 History 对象中的当前记录。

&nbsp;

&nbsp;

http://jun1986.iteye.com/blog/1176909

一、最外层top跳转页面，适合用于iframe框架集

top.window.location.href(&#8220;${pageContext.request.contextPath}/Login_goBack&#8221;);

============================================================================================

二、window.location.href和window.location.replace的区别

1.window.location.href=“url”：改变url地址；

2.

三、强制页面刷新

1.window.location.reload()：强制刷新页面，从服务器重新请求！

============================================================================================

四、window.location.reload();页面实现跳转和刷新

1 history.go(0)
  
2 location.reload()
  
3 location=location
  
4 location.assign(location)
  
5 document.execCommand(&#8216;Refresh&#8217;)
  
6 window.navigate(location)
  
7 location.replace(location)
  
8 document.URL=location.href
  
这几个都可以刷新
  
window.location.reload();刷新
  
window.location.href=window.location.href;刷新
  
window.close();关闭窗口，不弹出系统提示，直接关闭
  
window.close()相当于self属性是当前窗口
  
window.parent.close()是parent属性是当前窗口或框架的框架组
  
页面实现跳转的九种方法实例：
  
<html>
  
<head>
  
<meta http-equiv=&#8221;Content-Type&#8221; content=&#8221;text/html; charset=utf-8&#8243; />
  
<title>navigate</title>
  
<script language=&#8221;javascript&#8221;>
  
setTimeout(&#8216;window.navigate(&#8220;top.html&#8221;);&#8217;,2000);
  
setTimeout(&#8216;window.document.location.href=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;window.document.location=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;window.location.href=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;window.location=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;document.location.href=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;document.location=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;location.href=&#8221;top.html&#8221;;&#8217;,2000);
  
setTimeout(&#8216;location.replace(&#8220;top.html&#8221;)&#8217;,2000);
  
//window对象
  
//document对象
  
//location对象
  
//href属性
  
//1.window.document.location.href
  
//2.window.document.location
  
//3.window.location.href
  
//4.window.location

//5.document.location.href
  
//6.document.location
  
//7.location.href
  
//8.window.navigate
  
//9.location.replace
  
//只要使用location方法，和任意的window对象，location对象，href属性连用，都可以页面的跳转////
  
</script>
  
</head>

<body>
  
页面将在2秒后跳转
  
</body>
  
</html>

解释：
  
location是个对象，比如本页的document.location和window.location的属性有
  
location.hostname   =   community.csdn.net
  
location.href   =   http://community.csdn.net/Expert/topic/4033/4033372.xml?temp=2.695864E-02
  
location.host   =   community.csdn.net
  
location.hash   =
  
location.port   =
  
location.pathname   =   /Expert/topic/4033/4033372.xml
  
location.search   =   ?temp=2.695864E-02
  
location.protocol   =   http:
  
可见href是location的属性，类别是string。

&nbsp;

http://shawnfree.iteye.com/blog/390374