---
title: java doc, doc root
author: wiloon
type: post
date: 2011-08-28T06:02:31+00:00
url: /?p=606
bot_views:
  - 5
categories:
  - Java

---
{@docroot} 代表产生文档的根路径，从JDK/SDK 1.3开始引入。用法举例如下
  
/**
  
*see the <a href={@docroot}/copyright.html>copyright</a>
  
"*/
  
假定生成文档的根目录是doc，上面注释所在的文件最后生成的文件是docutilityutl.html，那么"copyright"的链接会指向..copyright.html。