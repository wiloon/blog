---
title: jQuery弹出层插件–BlockUI
author: wiloon
type: post
date: 2013-11-16T04:32:40+00:00
url: /?p=5963
categories:
  - Uncategorized
tags:
  - JavaScript
  - JQuery

---
<http://stylechen.com/jquery-blockui.html>

```

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js" type="text/javascript"></script>
  
<script src="images/jquery.blockUI.js" type="text/javascript"></script>


$(function(){
  
$('#box\_btn').click(function(){ //给box\_btn绑定一个鼠标点击的事件
   
$.blockUI({ //当点击事件发生时调用弹出层
   
message: $('#box'), //要弹出的元素box
   
css: { //弹出元素的CSS属性
   
top: '50%',
   
left: '50%',
   
textAlign: 'left',
   
marginLeft: '-320px',
   
marginTop: '-145px',
   
width: '600px',
   
background: 'none'
   
}
   
}); <a href="http://zwitserlandcasino.ch/">casino spiele online</a>
   
$('.blockOverlay').attr('title','单击关闭').click($.unblockUI); //遮罩层属性的设置以及当鼠标单击遮罩层可以关闭弹出层
   
$('.close').click($.unblockUI); //也可以自定义一个关闭按钮来关闭弹出层
  
});
  
});

```