---
title: Intellij IDEA CE 自动生成 serialVersionUID
author: "-"
date: 2012-12-07T05:29:40+00:00
url: /?p=4832
categories:
  - Java
tags:
  - IDEA

---
## Intellij IDEA CE 自动生成 serialVersionUID

IDEA的Inspector对serialVersionUID检测默认是关闭的，因此如果你的class是Serialization，那么需要重新设置一下(IDEA 9.0):
  
Setting->Inspections->Serialization issues->Serializable class without 'serialVersionUID'
  
选上以后，在你的class中: Alt+Enter就会提示自动创建serialVersionUID了。

<http://blog.sina.com.cn/s/blog_728c25590100y33w.html>
