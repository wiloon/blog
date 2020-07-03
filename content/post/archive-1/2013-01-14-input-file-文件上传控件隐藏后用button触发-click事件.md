---
title: input file 文件上传控件隐藏后用button触发 click事件
author: wiloon
type: post
date: 2013-01-14T04:47:29+00:00
url: /?p=5010
categories:
  - Web

---
http://bbs.csdn.net/topics/320156312

[html]

<HTML>

 <BODY>

 <div id="tt" style="position:relative;">

 <input type="button" value="添加附件" onmouseover="floatFile()">

 

 <div id="div1">

 <div id="file1text" ><input id="file1" name="myfile" type="file" onchange="showText(this)" style="position:absolute;filter:alpha(opacity=50);width:30px;opacity: 0.5;" hidefocus>

 

 

 

 <input type="button" onclick="alert($('tt').innerHTML)" value="showHTML">

 </BODY>

</HTML>

<SCRIPT LANGUAGE="JavaScript">

 function $(id)

 {

 return document.getElementById(id);

 }

 //全局变量，记录文件数；

 var fileNum=1;

 //mouseover时，把input file移到按扭上，保证点击的是file，

 function floatFile()

 {

 $("file"+fileNum).style.posTop=event.srcElement.offsetTop;

 $("file"+fileNum).style.posLeft=event.x-$("file"+fileNum).offsetWidth/2;

 }

 //选择完一个文件之后，自动创建一个新的div 和 file表单，用于下回使用，hidden刚用过的file

 function showText(obj)

 {

 $(obj.id+"text").innerHTML=obj.value+" <a href='javascript:del("+fileNum+")'>删除</a>";

 $("file"+fileNum).style.display='none';

 fileNum=fileNum+1;

 //直接追加innerHTML(innerHTML+=)会清空原来file中的内容

 $("div"+(fileNum-1)).insertAdjacentHTML('AfterEnd','<div id="div'+fileNum+'"><div id="file'+fileNum+'text" ><input id="file'+fileNum+'" name="myfile" type="file" onchange="showText(this)" style="position:absolute;filter:alpha(opacity=0);width:30px;"hidefocus>');

 }

 function del(id)

 {

 $("div"+id).innerHTML="";

 $("div"+id).style.display="none";

 }


  </SCRIPT>


  [/html]


  IE 使用 'filter:alpha(opacity=50);' 通过 Filter 的 alpha 通道滤镜使元素半透明，但元素必须触发 hasLayout 特性。

  非 IE 浏览器使用 'opacity:0.5;' 这个 CSS3 草案中的 'opacity' 特性使元素半透明。


  所以同时使用 'filter:alpha(opacity=50);' opacity:0.5; 即可保证在所有浏览器中呈现出半透明效果。


  


  http://www.w3help.org/zh-cn/causes/BT9011
