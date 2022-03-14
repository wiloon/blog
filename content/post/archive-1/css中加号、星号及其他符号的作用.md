---
title: CSS中加号、星号及其他符号的作用
author: "-"
date: 2014-04-11T05:47:57+00:00
url: /?p=6516
categories:
  - Uncategorized
tags:
  - CSS

---
## CSS中加号、星号及其他符号的作用
http://blog.sina.com.cn/s/blog_6790717801011dx8.html

CSS中加号、星号及其他符号的作用 (2012-06-27 14:34:32)转载▼

标签:  科技 css 浏览器 版本 it

首先,什么是CSS hack?

针对不同的浏览器写不同的CSS code的过程,就叫CSS hack!


CSS hack由于不同的浏览器,比如Internet Explorer 6,Internet Explorer 7,Mozilla Firefox等,对CSS的解析认识不一样,因此会导致生成的页面效果不一样,得不到我们所需要的页面效果。

这个时候我们就需要针对不同的浏览器去写不同的CSS,让它能够同时兼容不同的浏览器,能在不同的浏览器中也能得到我们想要的页面效果。


CSS Hack的原理是什么

由于不同的浏览器对CSS的支持及解析结果不一样,还由于CSS中的优先级的关系。我们就可以根据这个来针对不同的浏览器来写不同的CSS。

CSS Hack大致有3种表现形式,CSS类内部Hack、选择器Hack以及HTML头部引用(if IE)Hack,CSS Hack主要针对IE浏览器。

类内部Hack: 比如 IE6能识别下划线"_"和星号" \* ",IE7能识别星号" \* ",但不能识别下划线"_",而firefox两个都不能认识。

选择器Hack: 比如 IE6能识别\*html .class{},IE7能识别\*+html .class{}或者*:first-child+html .class{}。

HTML头部引用(if IE)Hack: 针对所有IE: <!-[if IE]><!-您的代码-><![endif]->,针对IE6及以下版本: <!-[if lt IE 7]><!-您的代码-><![endif]->,这类Hack不仅对CSS生效,对写在判断语句里面的所有代码都会生效。

书写顺序,一般是将识别能力强的浏览器的CSS写在后面。下面如何写里面说得更详细些。


如何写CSS Hack

比如要分辨IE6和firefox两种浏览器,可以这样写: 

<style>

div{

background:green;

*background:red;

}

</style>


在IE6中看到是红色的,在firefox中看到是绿色的。

上面的css在firefox中,它是认识不了后面的那个带星号的东西是什么的,于是将它过滤掉,不予理睬,解析得到的结果是:div{background:green},于是理所当然这个div的背景是绿色的。

在IE6中呢,它两个background都能识别出来,它解析得到的结果是:div{background:green;background:red;},于是根据优先级别,处在后面的red的优先级高,于是当然这个div的背景颜色就是红色的了。


在理想世界里,正确的CSS应该在任何支持CSS的浏览器里工作良好。不幸的是,我们并不是生活在理想的世界里,浏览器们布满了BUG和不一致。创建一个跨浏览器并且显示一致的页面,CSS开发者必须想尽办法。通过使用BUG和未实现的CSS,开发者就能够为不同的浏览器应用不同的规则。HACK和FILTER是开发者强有力的武器。了解各种常用的HACKS以及它们如何工作,是件重要的事,但什么时候用和什么时候不用它们,也是件同等重要的事情。

CSS filter或者hack是一种代码,用来根据浏览器类型,版本号显示或隐藏CSS标签。浏览器们对CSS行为有不同的解释,对W3C标准的支持程度也不相同。CSS 过滤器经常用于在多个浏览器中实现一致的布局外观,因为某些浏览器无法渲染。HACK (黑客) 这样的称呼多少有点消极,实质上属于个人对CSS代码非官方的修改,误导人们以为还有更好的方法达到目的,但其实我们没有,有的人喜欢用patch (补丁) 来称呼它,这样人们就能知道这本是浏览器造成的错误。

反斜线符号

这种hack利用了一个在Mac平台上的IE的bug。以*/结束的注释在IE Mac上是不正确关闭的,所以那些需要被忽略的语句可以放在这种注释后面。

selector { ...styles... }

盒模型hack

(适用于IE6以下版本)

叫它"盒模型hack"是因为它经常被用于解决IE的盒模型错误,这个hack可以为IE和其它浏览器设置不同的属性。 (在版本6时,IE已经修正了这个盒模型错误。) 

#elem {

width: [IE 中的宽度];

voice-family: "\"}\"";

voice-family:inherit;

width: [其它浏览器中的宽度];

}

html>body #elem {

width:[其它浏览器中的宽度];

}

第一个,把voice-family设置为字符串"}",但是IE的解析bug会把它当作一个反斜线加右括号。选择 voice-family是因为它不会影响到页面样式。第二个规则,使用了html>body hack,是为Opera7.0以前浏览器,它也有这样的解析错误,但幸好它支持子选择器,所以有这样较简单的方法。

下划线hack

(适用于IE6及其以下版本)

IE 6 及以下的版本可以识别带有下划线前缀的属性,而其它的浏览器会忽略它。因此,一个属性前面加上下划线或者连字符,就成为了IE6及以下版本浏览器的专有属性。

#elem {

width: [W3C Model Width];

_width: [BorderBox Model];

}

这个hack使用了无效的CSS,利用了一个浏览器的bug,但是我们有有效的CSS语句可以完成这样的事情,所以这个HACK不推荐使用。

星号hack

(适用于IE7以下版本)

除了下划线和连字符,版本7及以下的IE可以识别以非字母字符为前缀的属性,而其它浏览器会忽略。

#elem {

width: [W3C Model Width];

*width: [BorderBox Model];

}

这个HACK不推荐使用,原因同上面的下划线HACK一样。

星号 HTML hack

(适用于IE4-6)

HTML元素是W3C标准DOM (Document Object Model)的根元素,但是IE 4至6的版本中还有一个神秘的父元素。完全兼容的浏览器会忽略这个* html选择器,但IE4-6却会对它正常处理。这样就可以为这些版本的浏览器指定特别的规则。比如,这个规则可以特别指定IE4-6中的文字大小,但对其它浏览器不起作用。

* html p {font-size: 5em; }

这个HACK使用了完全有效的CSS。

星号加号HACK

(适用于IE7)

虽然IE7不再识别以前的* html hack,但它使用了一个相似的新的hack。

*:first-child+html p { font-size: 5em; }

或者: 

*+html p { font-size: 5em; }

此代码只适用于IE7,不适用于其它任何浏览器。注意这个HACK只在IE7标准模型里工作正常,在怪异模式下不能用。这个hack也被IE8的兼容模式 (相当于IE7的标准模式) 所支持。和星号HTML hack一样,它也使用了有效的CSS。

子选择器hack

(适用于IE6及以下版本)

IE6和早期的版本不支持"子选择器"(>),利用这个我们可以为其它浏览器指定特别的规则。举例来说,这个规则可以让段落文字在firefox 变成蓝色,但在IE7之前的版本里却不能。

html > body p { color: blue; }

虽然IE7增加了对子选择器的支持,但人们发现了新的hack可以把IE7也排除。当一个空的注释紧跟在子选择器的后面重复的时候,IE7会不识别后面的规则,就和较早版本的浏览器一样。

html > body p { color: blue; }

否定伪类HACK

(可区分IE和非IE)

IE的所有版本都不支持CSS3 : not() 伪类。有一种变异的HACK使用 : root 伪类,此伪类也同样不被IE识别。

.yourSelector {

color: black;

}

html:not([dummy]) .yourSelector {

color: red;

}

这种否定选择器接受任何类型作为参数,属性,通用,类或ID选择器,或者伪类。然后它会把后面的属性应用于所有不匹配此语法的元素上。

Body:empty hack

(适用于Firefox 2.0及以下版本)

:empty 伪类,在CSS3中介绍过的,用于选择不含任何内容的元素。然而,Geck0 1.8.1 和之后版本 (应用在Firefox2.0.x 及之后的版本) 错误地选择了body:empty 即使body元素包含有内容 (一般情况都如此) 。这样我们可以向Firefox 2.0x及以下版本提供专用的CSS规则。

body:empty p {

display:none;

}

此HACK使用有效的CSS.

！Important 怪僻

(适用于IE8以下版本)

IE8及以下版本有一些和!imporant有关的怪僻,它允许一个赋值优先级更高。IE7及更早版本接受任意字符串替代important,并且会正常处理该值,而其它浏览器则会忽略。

body {

color: black;

color: blue !ie;

}

相似地,IE8及更早版本接受在!important声明后面的非字母符号,而其它浏览器会忽略它。

body {

color: black;

color: blue !important!;

}

IE6及以下版本有一个!important带来的问题,当在同一段代码块中同一元素的同一属性有了不同的值,本应结果是第二个值被第一个取代,但IE6及更低版本并不这么做。

body {

color: black !important;

color: blue;

}

所有这些HACK使用的是有效的CSS。

动态属性

在版本5至7,IE曾支持过一种语法适用于动态变化的CSS属性,有时被称为CSS表达式。动态属性通常混合其它HACK以补偿更早版IE中不支持的属性。

div {

min-height: 300px;

_height: expression_r(document.body.clientHeight < 300 ? "300px" : "auto");

}

有条件的注释

有条件的注释只在Windows平台的IE上被识别,并从IE5起开始支持,它甚至可以区分版本5.0,5.5和6.0。

代码: 

下面是一些"有条件的注释",可以显示你正在使用的IE版本。如果你看不到,那么你用的不是IE: 

<!-[if IE]>

According to the conditional comment this is Internet Explorer

<![endif]->

<!-[if IE 5]>

According to the conditional comment this is Internet Explorer 5

<![endif]->

<!-[if IE 5.0]>

According to the conditional comment this is Internet Explorer 5.0

<![endif]->

<!-[if IE 5.5]>

According to the conditional comment this is Internet Explorer 5.5

<![endif]->

<!-[if IE 6]>

According to the conditional comment this is Internet Explorer 6

<![endif]->

<!-[if IE 7]>

According to the conditional comment this is Internet Explorer 7

<![endif]->

<!-[if gte IE 5]>

According to the conditional comment this is Internet Explorer 5 and up

<![endif]->

<!-[if lt IE 6]>

According to the conditional comment this is Internet Explorer lower than 6

<![endif]->

<!-[if lte IE 5.5]>

According to the conditional comment this is Internet Explorer lower or equal to 5.5

<![endif]->

<!-[if gt IE 6]>

According to the conditional comment this is Internet Explorer greater than 6

<![endif]->


注意它的语法: 

- gt: 高于

- lte:低于或相当

说明: 

1.它们的基本结构和HTML注释一样(<!- ->)。因此其它所有浏览器会把它们当作正常的注释忽略掉。

2.Windows IE里的程序可以识别这个特殊的<!-[if IE]>语法,处理if并解析此注释中的内容,就当作是正常的网页内容一样。

3.既然"有条件的注释"使用了HTML注释的结构,它们就只能被包含在HTML文件里,而不是CSS文件里。你可以把整个标签放在"有条件的注释"里,指向一个指定的样式表。如下所示: 



<!-[if IE]>  <![endif]->

<!-[if lt IE 7]>  <![endif]->

<!-[if !lt IE 7]><![IGNORE[-><![IGNORE[]]>  <!-<![endif]->

<!-[if !IE]>->  <!-<![endif]->

IE8 hack

IE8不能识别"*"和"_"的css hack,所以我们可以使用"\9"来区分IE的各个版本。

color:#0000FF\9; ;

*color:#FFFF00;

_color:#FF0000;

小结

使用HACK隐藏代码在浏览器更新时经常会导致页面不正常显示。许多HACK曾用于在IE6及更低版本中隐藏CSS,但在版本7下不再工作,因为IE改进了对CSS 标准的支持。微软的IE开发小组曾要求人们使用有条件