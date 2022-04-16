---
title: Chrome 运行Android应用
author: "-"
date: 2014-11-19T03:49:12+00:00
url: /?p=7019
categories:
  - chrome
tags:
  - reprint
---
## Chrome 运行Android应用
说到Chrome运行android程序,不得不说一个东西,那就是"Android Runtime for Chrome (ARC) ",ARC是Google最新推出的 Chrome OS 运行Android程序的运行时。ARC基于Google的Native Client(NaCl)功能,其允许通过浏览器来运行原生代码(通常是C或C++),同时具备Chrome所提供的同等安全性。显然,NaCl扩展是可以做到跨平台的,这意味着它能够在PC、Mac、以及Linux等系统的桌面版Chrome浏览器上运行。

但遗憾的是,ARC已经被打上了"Chrome OS专属"的标记,只能运行在Chrome上,并且只能运行Google提供的四款Android App,不能运行其他的。所以一般人无法在桌面版Chrome浏览器上使用。值得庆幸的是,一名叫做 **Vladikoff** 的黑客,已经突破了这些限制。首先,他实现了如何让Chrome OS能加载任何Android App,而不仅仅局限于官方指定的四款App,而现在,他取得了更大的突破,让Android App工作在Windows,Mac和Linux操作系统当中。

Vladikoff做了一个定制版本的ARC,称之为"ARChon",可以在Windows,Mac和Linux操作系统当中Chrome37及以上版本的Chrome浏览器中可运行任何Android应用程序,但是,ARC不支持原始的Android应用程序包 (APK) ,它们需要被转换成一个Chrome扩展,好在Vladikoff提供了一个名为chromeos-apk 的转换工具,可以把Apk文件转换成Chrome扩展。

http://my.oschina.net/fants/blog/323672