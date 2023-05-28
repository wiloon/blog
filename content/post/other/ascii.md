---
title: ASCII
author: "-"
date: 2014-03-05T05:09:49+00:00
url: ascii
categories:
  - cs
tags:
  - reprint
---
## ASCII

|Dec|Hex|Char|
|-|-|-|
|10|0A|LF|
|35|30|#|
|48|30|0|
|57|39|9|
|65|41|A|
|66|42|B|
|67|43|C|
|70|46|F|
|90|5A|Z|
|97|61|a|
|102|66|f|
|112|7A|z|
|124|7C|\||

---

ASCII字符集，最基本的包含了128个字符。其中前32个，0-31，即0×00-0x1F，都是不可见字符。这些字符，就叫做控制字符。

这些字符没法打印出来，但是每个字符，都对应着一个特殊的控制功能的字符，简称功能字符或功能码Function Code。

简言之: ASCII中前32个字符，统称为Function Code功能字符。

此外，由于ASCII中的127对应的是Delete，也是不可见的，所以，此处根据笔者的理解，也可以归为Function Code。

此类字符，对应不同的"功能"，起到一定的"控制作用"，所以，称为控制字符。

在XML规范中，不支持ASCII前31个字符中的相当多控制符号，所以在组装XML时需过滤这些特殊字符，以免引起解析问题。同时，'&'(实体引用的开始)和'<'(控制符的开始)作为XML的标准控制字符必须不能出现在正常内容中，如果出现的话，需要转义。XML提供CDATA结构段用来指示XML解析器不要对CDATA段中的数据做处理。但如果在CDATA段中包含CDATA段的关闭符']]>'的话，还是会出现解析问题。
  
<http://www.asciitable.com/>
  
<http://en.wikipedia.org/wiki/ASCII>

ASCII字符集中的功能/控制字符 Function/Control Code/Character in ASCII
  
><http://book.51cto.com/art/201202/318141.htm>
