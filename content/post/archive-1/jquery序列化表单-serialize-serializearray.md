---
title: jQuery序列化表单 serialize() serializeArray()
author: "-"
date: 2015-05-11T01:38:18+00:00
url: /?p=7655
categories:
  - Uncategorized
tags:
  - JQuery

---
## jQuery序列化表单 serialize() serializeArray()
1. serialize()方法

描述: 序列化表单内容为字符串,用于Ajax请求。

格式: var data = $("form").serialize();

2.serializeArray()方法

描述: 序列化表单元素(类似'.serialize()'方法)返回JSON数据结构数据。

注意,此方法返回的是JSON对象而非JSON字符串。需要使用插件或者第三方库进行字符串化操作。

格式: var jsonData = $("form").serializeArray();

在使用ajax提交表单数据时,以上两种方法都可以将data参数设置为$("form").serialize()或$("form").serializeArray()。
  
Demo

[html][/html]


  
<form id="myform">
  

  

  
姓名:
  
 <input type="text" name="name" /> 
  

  

  
性别:
  

  
<input type="radio" name="sex" value="1"> 男
  
<input type="radio" name="sex" value="0"> 女
  

  

  

  
年龄:
  

  
<select name="age">
  
<option value="20">20</option>
  
<option value="21">21</option>
  
<option value="22">22</option>
  
</select>
  

  

  

  

  
<input type="button" id="ajaxBtn" value="提交" />
  

  

  

  
</form>

[javascript][/javascript]


  
$(function() {
  
$("#ajaxBtn").click(function() {
  
var params1 = $("#myform").serialize();
  
var params2 = $("#myform").serializeArray();
  
console.log(params1);  //name=zhangsan&sex=1&age=20
  
console.log(params2);  //[Object, Object, Object]
  
$.ajax( {
  
type : "POST",
  
url : "RegisterAction.action",
  
data : params1,
  
success : function(msg) {
  
alert("success: " + msg);
  
}
  
});
  
})
  
})
  
从下图中可以看出两种方法的不同http://blog.csdn.net/itmyhome1990/article/details/41866265

