---
title: javascript unit test
author: wiloon
type: post
date: 2014-08-25T01:30:34+00:00
url: /?p=6959
categories:
  - Uncategorized
tags:
  - JavaScript

---
http://blog.sina.com.cn/s/blog_6768f2290100ubw5.html

最近由于工作和个人兴趣的关系，有幸研究了一下javascript的unit test，市面上常见且比较易用的javascript的unit test的framework有三个：jsunit, qunit和yuitest，虽然出处不同，但是本质上，使用方法都大同小异。

jsunit：http://www.jsunit.net/ 最早开发自2001年，是第一个实用的javascript的unit test framework（那时候TDD还远未流行），其完全遵循junit的xunit pattern, 有setup, teardown, 有testsuit概念，还有若干种assert方法，不过因为其诞生早，对非同步的ajax测试支持不够，因而有市场占有率渐低的趋势。

qunit: http://docs.jquery.com/Qunit 个人极其欣赏的一个framework，隶属于大名鼎鼎的jquery，但是又无需依赖于jquery的库可单独运行, 方法轻量易学，且具有异步测试的功能。可惜在公司没有被官方支持，只能自己玩。

yui test: http://developer.yahoo.com/yui/yuitest/ 著名的yahoo web js toolkit library中的ut子项目，使用方法和qunit极其相似，也具有异步测试功能，在本人公司被官方支持，最大的缺点是使用时要调用其他诸多的yui模块用来显示结果，不够独立。

以下以qunit为例子，介绍这些unit test framework的使用方法：
  
1 ) 下载qunit的测试驱动程序js文件和对应显示结果用的css文件（分别为qunit.js 和qunit.css )
  
2 ) 将这两个文件保存在某个目录，并在同一目录建立一个简单的html文件，包含该两个文件以及jquery.js
  
3 ) 将我们需要测试的js代码的文件也包含入该简单html中(该例中为mycode.js)。
  
4 ) 将我们要测试的js代码的依赖库也加入该html中(如ExtJS或者其他库)
  
5 ) 在html中添加script的测试代码 (test suit和assert部分）
  
6 ) 在浏览器中载入该html文件，页面会自动显示运行结果。

值得一提的是，网上有qunit-CLI的项目，其用rhino解释器来代替浏览器做unit test js的运行环境，提高了测试的效率，有兴趣的朋友可以去google搜索看看。

代码如下：
  
mycode.js

function (a, b) {
  
return a + b;
  
}

test.html

<html>
  
<head>
  
<link rel=&#8221;stylesheet&#8221; href=&#8221;qunit.css&#8221; type=&#8221;text/css&#8221; media=&#8221;screen&#8221; />
  
<script src=&#8221;http://code.jquery.com/jquery-latest.js&#8221;></script>
  
<script type=&#8221;text/javascript&#8221; src=&#8221;qunit.js&#8221;></script>

<!&#8211; js to be tested &#8211;>
  
<script type=&#8221;text/javascript&#8221; src=&#8221;mycode.js&#8221;></script>

<!&#8211; unit test part &#8211;>
  
<script>
  
$(document).ready(function(){
  
test(&#8220;a basic test example&#8221;, function() {
  
var sum = add (1 + 1);
  
equal( sum, &#8220;2&#8221;, &#8220;We expect value to be 2&#8243; );
  
});
  
});
  
</script>
  
</head>
  
<body>
  
<h1 id=&#8221;qunit-header&#8221;>QUnit example</h1>
  
<h2 id=&#8221;qunit-banner&#8221;></h2>
  
<div id=&#8221;qunit-testrunner-toolbar&#8221;></div>
  
<h2 id=&#8221;qunit-userAgent&#8221;></h2>
  
<ol id=&#8221;qunit-tests&#8221;></ol>
  
<div id=&#8221;qunit-fixture&#8221;>test markup, will be hidden</div>
  
</