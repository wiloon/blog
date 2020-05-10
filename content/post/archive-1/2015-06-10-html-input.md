---
title: html input
author: wiloon
type: post
date: 2015-06-10T03:56:12+00:00
url: /?p=7785
categories:
  - Uncategorized

---
<pre data-language=HTML><code class="language-markup line-numbers">&lt;input type="value0"&gt;
</code></pre> 

hidden 定义隐藏的输入字段。
  
Hidden 对象代表一个 HTML 表单中的某个隐藏输入域。

这种类型的输入元素实际上是隐藏的。这个不可见的表单元素的 value 属性保存了一个要提交给 Web 服务器的任意字符串。如果想要提交并非用户直接输入的数据的话，就是用这种类型的元素。

在 HTML 表单中 <input type=”hidden”> 标签每出现一次，一个 Hidden 对象就会被创建。

您可通过遍历表单的 elements[] 数组来访问某个隐藏输入域，或者通过使用document.getElementById()。

http://www.w3school.com.cn/jsref/dom\_obj\_hidden.asp

http://www.wiloon.com/wordpress/?p=6529