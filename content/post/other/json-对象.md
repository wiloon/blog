---
title: JavaScript json 对象
author: "-"
date: 2015-05-10T07:27:59+00:00
url: /?p=7637
categories:
  - JavaScript
tags:
  - JSON

---
## JavaScript json 对象

<http://www.cnblogs.com/tomxu/archive/2012/01/11/2311956.html>

深入理解JavaScript系列 (9) : 根本没有"JSON对象"这回事！

前言
  
写这篇文章的目的是经常看到开发人员说: 把字符串转化为JSON对象，把JSON对象转化成字符串等类似的话题，所以把之前收藏的一篇老外的文章整理翻译了一下，供大家讨论，如有错误，请大家指出，多谢。

正文
  
本文的主题是基于ECMAScript262-3来写的，2011年的262-5新规范增加了JSON对象，和我们平时所说的JSON有关系，但是不是同一个东西，文章最后一节会讲到新增加的JSON对象。

英文原文: <http://benalman.com/news/2010/03/theres-no-such-thing-as-a-json/>
  
我想给大家澄清一下一个非常普遍的误解，我认为很多JavaScript开发人员都错误地把 JavaScript 对象字面量 (Object Literals) 称为JSON对象 (JSON Objects) ，因为他的语法和JSON规范里描述的一样，但是该规范里也明确地说了JSON只是一个数据交换语言，只有我们将之用在string上下文的时候它才叫JSON。

序列化与反序列化
  
2个程序 (或服务器、语言等) 需要交互通信的时候，他们倾向于使用string字符串因为string在很多语言里解析的方式都差不多。复杂的数据结构经常需要用到，并且通过各种各样的中括号{}，小括号()，叫括号<>和空格来组成，这个字符串仅仅是按照要求规范好的字符。

为此，我们为了描述这些复杂的数据结构作为一个string字符串，制定了标准的规则和语法。JSON只是其中一种语法，它可以在string上下文里描述对象，数组，字符串，数字，布尔型和null，然后通过程序间传输，并且反序列化成所需要的格式。YAML和XML (甚至request params) 也是流行的数据交换格式，但是，我们喜欢JSON，谁叫我们是JavaScript开发人员呢！

字面量
  
引用Mozilla Developer Center里的几句话，供大家参考:

他们是固定的值，不是变量，让你从"字面上"理解脚本。 (Literals)
  
字符串字面量是由双引号 (") 或单引号 (') 包围起来的零个或多个字符组成的。(Strings Literals)
  
对象字面量是由大括号 ({}) 括起来的零个或多个对象的属性名-值对。(Object Literals)
  
何时是JSON，何时不是JSON？
  
JSON是设计成描述数据交换格式的，他也有自己的语法，这个语法是JavaScript的一个子集。
  
{ "prop": "val" } 这样的声明有可能是JavaScript对象字面量也有可能是JSON字符串，取决于什么上下文使用它，如果是用在string上下文 (用单引号或双引号引住，或者从text文件读取) 的话，那它就是JSON字符串，如果是用在对象字面量上下文中，那它就是对象字面量。

// 这是JSON字符串
  
var foo = '{ "prop": "val" }';

// 这是对象字面量
  
var bar = { "prop": "val" };
  
而且要注意，JSON有非常严格的语法，在string上下文里{ "prop": "val" } 是个合法的JSON，但{ prop: "val" }和{ 'prop': 'val' }确实不合法的。所有属性名称和它的值都必须用双引号引住，不能使用单引号。另外，即便你用了转义以后的单引号也是不合法的，详细的语法规则可以到这里查看。

放到上下文里来看
  
大家伙可能嗤之以鼻: 难道JavaScript代码不是一个大的字符串？

当然是，所有的JavaScript代码和HTML (可能还有其他东西) 都是字符串，直到浏览器对他们进行解析。这时候.jf文件或者inline的JavaScript代码已经不是字符串了，而是被当成真正的JavaScript源代码了，就像页面里的innterHTML一样，这时候也不是字符串了，而是被解析成DOM结构了。

再次说一下，这取决于上下文，在string上下文里使用带有大括号的JavaScript对象，那它就是JSON字符串，而如果在对象字面量上下文里使用的话，那它就是对象字面量。

真正的JSON对象
  
开头已经提到，对象字面量不是JSON对象，但是有真正的JSON对象。但是两者完全不一样概念，在新版的浏览器里JSON对象已经被原生的内置对象了，目前有2个静态方法: JSON.parse用来将JSON字符串反序列化成对象，JSON.stringify用来将对象序列化成JSON字符串。老版本的浏览器不支持这个对象，但你可以通过json2.js来实现同样的功能。

如果还不理解，别担心，参考一下的例子就知道了:

// 这是JSON字符串，比如从AJAX获取字符串信息
  
var my_json_string = '{ "prop": "val" }';

// 将字符串反序列化成对象
  
var my_obj = JSON.parse( my_json_string );

alert( my_obj.prop == 'val' ); // 提示 true, 和想象的一样!

// 将对象序列化成JSON字符串
  
var my_other_json_string = JSON.stringify( my_obj );
  
另外，Paul Irish提到Douglas Crockford在JSON RFC里用到了"JSON object"，但是在那个上下文里，他的意思是"对象描述成JSON字符串"不是"对象字面量"。

更多资料
  
如果你想了解更多关于JSON的资料，下面的连接对你绝对有用:

JSON specification
  
JSON RFC
  
JSON on Wikipedia
  
JSONLint - The JSON Validator
  
JSON is not the same as JSON
  
同步与推荐
  
本文已同步至目录索引: 深入理解JavaScript系列

深入理解JavaScript系列文章，包括了原创，翻译，转载等各类型的文章，如果对你有用，请推荐支持一把，给大叔写作的动力。
