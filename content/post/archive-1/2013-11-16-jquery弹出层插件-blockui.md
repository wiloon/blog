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

[javascript]

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js" type="text/javascript"></script>
  
<script src="images/jquery.blockUI.js" type="text/javascript"></script>



$(function(){
  
$(&#8216;#box\_btn&#8217;).click(function(){ //给box\_btn绑定一个鼠标点击的事件
   
$.blockUI({ //当点击事件发生时调用弹出层
   
message: $(&#8216;#box&#8217;), //要弹出的元素box
   
css: { //弹出元素的CSS属性
   
top: &#8216;50%&#8217;,
   
left: &#8216;50%&#8217;,
   
textAlign: &#8216;left&#8217;,
   
marginLeft: &#8216;-320px&#8217;,
   
marginTop: &#8216;-145px&#8217;,
   
width: &#8216;600px&#8217;,
   
background: &#8216;none&#8217;
   
}
   
}); <a href="http://zwitserlandcasino.ch/">casino spiele online</a>
   
$(&#8216;.blockOverlay&#8217;).attr(&#8216;title&#8217;,&#8217;单击关闭&#8217;).click($.unblockUI); //遮罩层属性的设置以及当鼠标单击遮罩层可以关闭弹出层
   
$(&#8216;.close&#8217;).click($.unblockUI); //也可以自定义一个关闭按钮来关闭弹出层
  
});
  
});

[/javascript]