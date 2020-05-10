---
title: input file 文件上传控件隐藏后用button触发 click事件
author: wiloon
type: post
date: 2013-01-14T04:47:29+00:00
url: /?p=5010
categories:
  - Web

---
<pre>http://bbs.csdn.net/topics/320156312<br />
[html]<br />
<HTML><br />
 <BODY><br />
 <div id="tt" style="position:relative;"><br />
 <input type="button" value="添加附件" onmouseover="floatFile()"><br />
 <br><br />
 <div id="div1"><br />
 <div id="file1text" ></div><input id="file1" name="myfile" type="file" onchange="showText(this)" style="position:absolute;filter:alpha(opacity=50);width:30px;opacity: 0.5;" hidefocus><br />
 </div><br />
 </div><br />
 </p><br />
 <input type="button" onclick="alert($('tt').innerHTML)" value="showHTML"><br />
 </BODY><br />
</HTML><br />
<SCRIPT LANGUAGE="JavaScript"><br />
 function $(id)<br />
 {<br />
 return document.getElementById(id);<br />
 }<br />
 //全局变量，记录文件数；<br />
 var fileNum=1;<br />
 //mouseover时，把input file移到按扭上，保证点击的是file，<br />
 function floatFile()<br />
 {<br />
 $("file"+fileNum).style.posTop=event.srcElement.offsetTop;<br />
 $("file"+fileNum).style.posLeft=event.x-$("file"+fileNum).offsetWidth/2;<br />
 }<br />
 //选择完一个文件之后，自动创建一个新的div 和 file表单，用于下回使用，hidden刚用过的file<br />
 function showText(obj)<br />
 {<br />
 $(obj.id+"text").innerHTML=obj.value+" <a href='javascript:del("+fileNum+")'>删除</a>";<br />
 $("file"+fileNum).style.display='none';<br />
 fileNum=fileNum+1;<br />
 //直接追加innerHTML(innerHTML+=)会清空原来file中的内容<br />
 $("div"+(fileNum-1)).insertAdjacentHTML('AfterEnd','<div id="div'+fileNum+'"><div id="file'+fileNum+'text" ></div><input id="file'+fileNum+'" name="myfile" type="file" onchange="showText(this)" style="position:absolute;filter:alpha(opacity=0);width:30px;"hidefocus></div>');<br />
 }<br />
 function del(id)<br />
 {<br />
 $("div"+id).innerHTML="";<br />
 $("div"+id).style.display="none";<br />
 }</p>


<p>
  </SCRIPT>
</p>


<p>
  [/html]
</p>


<p>
  IE 使用 'filter:alpha(opacity=50);' 通过 Filter 的 alpha 通道滤镜使元素半透明，但元素必须触发 hasLayout 特性。<br />
  非 IE 浏览器使用 'opacity:0.5;' 这个 CSS3 草案中的 'opacity' 特性使元素半透明。
</p>


<p>
  所以同时使用 'filter:alpha(opacity=50);' opacity:0.5; 即可保证在所有浏览器中呈现出半透明效果。
</p>


<p>
  &nbsp;
</p>


<p>
  http://www.w3help.org/zh-cn/causes/BT9011
</p>