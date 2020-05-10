---
title: jQuery序列化表单 serialize() serializeArray()
author: wiloon
type: post
date: 2015-05-11T01:38:18+00:00
url: /?p=7655
categories:
  - Uncategorized
tags:
  - JQuery

---
1、serialize()方法

描述：序列化表单内容为字符串,用于Ajax请求。

格式：var data = $(&#8220;form&#8221;).serialize();

2.serializeArray()方法

描述：序列化表单元素(类似&#8217;.serialize()&#8217;方法)返回JSON数据结构数据。

注意,此方法返回的是JSON对象而非JSON字符串。需要使用插件或者<a>第三方库</a>进行字符串化操作。

格式：var jsonData = $(&#8220;form&#8221;).serializeArray();

在使用ajax提交表单数据时,以上两种方法都可以将data参数设置为$(&#8220;form&#8221;).serialize()或$(&#8220;form&#8221;).serializeArray()。
  
Demo

\[html\]\[/html\]

view plaincopy
  
<form id=&#8221;myform&#8221;>
  
<table>
  
<tr>
  
<td>姓名:</td>
  
<td> <input type=&#8221;text&#8221; name=&#8221;name&#8221; /> </td>
  
</tr>
  
<tr>
  
<td>性别:</td>
  
<td>
  
<input type=&#8221;radio&#8221; name=&#8221;sex&#8221; value=&#8221;1&#8243;> 男
  
<input type=&#8221;radio&#8221; name=&#8221;sex&#8221; value=&#8221;0&#8243;> 女
  
</td>
  
</tr>
  
<tr>
  
<td>年龄:</td>
  
<td>
  
<select name=&#8221;age&#8221;>
  
<option value=&#8221;20&#8243;>20</option>
  
<option value=&#8221;21&#8243;>21</option>
  
<option value=&#8221;22&#8243;>22</option>
  
</select>
  
</td>
  
</tr>
  
<tr>
  
<td colspan=&#8221;2&#8243;>
  
<input type=&#8221;button&#8221; id=&#8221;ajaxBtn&#8221; value=&#8221;提交&#8221; />
  
</td>
  
</tr>
  
</table>
  
</form>

\[javascript\]\[/javascript\]

view plaincopy
  
$(function() {
  
$(&#8220;#ajaxBtn&#8221;).click(function() {
  
var params1 = $(&#8220;#myform&#8221;).serialize();
  
var params2 = $(&#8220;#myform&#8221;).serializeArray();
  
console.log(params1);  //name=zhangsan&sex=1&age=20
  
console.log(params2);  //[Object, Object, Object]
  
$.ajax( {
  
type : &#8220;POST&#8221;,
  
url : &#8220;RegisterAction.action&#8221;,
  
data : params1,
  
success : function(msg) {
  
alert(&#8220;success: &#8221; + msg);
  
}
  
});
  
})
  
})
  
从下图中可以看出两种方法的不同http://blog.csdn.net/itmyhome1990/article/details/41866265

&nbsp;