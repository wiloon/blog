---
title: ARC 与 GC 区别
author: "-"
date: 2015-02-05T02:50:20+00:00
url: /?p=7311
categories:
  - Uncategorized

tags:
  - reprint
---
## ARC 与 GC 区别
http://my.oschina.net/u/566401/blog/109020

the short and sweet answer is as follow:

**1.GC of java is Runtime, while ARC is compile time.**

**2.GC has reference to the objects at runtime and check for the dependencies of object runtime. While ARC appends the release, retain, autorelease calls at compiletime.**

**更多链接: **

**1.http://stackoverflow.com/questions/6385212/how-does-the-new-automatic-reference-counting-mechanism-work**

**2.http://stackoverflow.com/questions/7900167/objective-c-2-0-garbage-collector-vs-automatic-reference-counter-in-ios-5-sdk**

**3.http://longweekendmobile.com/2011/09/07/objc-automatic-reference-counting-in-xcode-explained/**