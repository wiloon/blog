---
title: CSS DIV居中
author: "-"
date: 2014-06-25T05:40:35+00:00
url: /?p=6771
categories:
  - Uncategorized
tags:
  - CSS

---
## CSS DIV居中
CSS 如何使DIV层水平居中
  
今天用CSS碰到个很棘手的问题,DIV本身没有定义自己居中的属性,
  
网上很多的方法都是介绍用上级的text-align: center然后嵌套一层DIV来解决问题.
  
可是事实上这样的方法科学吗?
  
经过网络搜索和亲自实验得出以下结论:
  
正确的也是对页面构造没有影响的设置如下:
  
对需要水平居中的DIV层添加以下属性:

margin-left: auto;
  
margin-right: auto;

经过这么一番设置问题似乎解决了,在FF中已经居中了,可是在IE中看竟然还是没有居中!
  
郁闷了一下午,就是找不出问题所在,还特地比较了网上的文章竟然一模一样.
  
问题到底出在哪里呢?
  
感谢网友乐天无用帮忙找出了这个邪门问题的原因.
  
原来是L-Blog默认没有在HTML前加上DTD,于是IE就以HTML而不是XHTML来解释文档.
  
问题并不在CSS而在XHTML网页本身.
  
需要加上这样的代码才能使得上述设置有效果:
  
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  
如果您希望更为严格的XHTML 1.0 Strict或者XHTML 1.1请查阅相关文档.
  
以上测试均基于Windows XP SP2版IE6和FireFox 1.0最终版.
  
如何使DIV居中
  
主要的样式定义如下: 
  
body {TEXT-ALIGN: center;}
  
#center { MARGIN-RIGHT: auto; MARGIN-LEFT: auto; }
  
说明: 
  
首先在父级元素定义TEXT-ALIGN: center;这个的意思就是在父级元素内的内容居中；对于IE这样设定就已经可以了。但在mozilla中不能居中。解决办法就是在子元素定义时候设定时再加上"MARGIN-RIGHT: auto;MARGIN-LEFT: auto; "
  
需要说明的是,如果你想用这个方法使整个页面要居中,建议不要套在一个DIV里,你可以依次拆出多个div,只
  
要在每个拆出的div里定义MARGIN-RIGHT: auto;MARGIN-LEFT: auto; 就可以了。

如何使图片在DIV 中垂直居中,用背景的方法。举例: 
  
body{BACKGROUND: url(http://www.w3cn.org/style/001/logo_w3cn_194x79.gif) #FFF no-repeat center;}
  
关键就是最后的center,这个参数定义图片的位置。还可以写成"top left"(左上角)或者"bottom right"等,也可以直接写数值"50 30"

如何使文本在DIV中垂直居中
  
如果是文字,便不能用背景方法,可以用增高行距的办法变通实现垂直居中,完整代码如下: 
  
<html>
  
<head>
  
<style>
  
body{TEXT-ALIGN: center;}
  
#center{ MARGIN-RIGHT: auto;
  
MARGIN-LEFT: auto;
  
height:200px;
  
background:#F00;
  
width:400px;
  
vertical-align:middle;
  
line-height:200px;
  
}
  
</style>
  
</head>
  
<body >
  
test content
  
</body>
  
</html>
  
说明: 
  
vertical-align:middle;表示行内垂直居中,我们将行距增加到和整个DIV一样高line-height:200px;然后插入文字,就垂直居中了。

CSS+DIV控制页面中元素垂直居中代码 全局和区域垂直居中
  
<style type="text/css" media=screen>
  
body
  
{
  
text-align: center;
  
}
  
#a
  
{
  
width: 200px;
  
height: 400px;
  
background: #000;
  
}
  
#b
  
{
  
margin-top: expression((a.clientHeight-50)/2);
  
width: 50px;
  
height: 50px;
  
background: #FFF;
  
}
  
#c
  
{
  
position: absolute;
  
left: expression((body.clientWidth-50)/2);
  
top: expression((body.clientHeight-50)/2);
  
width: 50px;
  
height: 50px;
  
background: #F00;
  
}
  
</style>
  

  

  
  

  
另一方法:
  
