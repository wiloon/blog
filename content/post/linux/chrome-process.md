---
author: "-"
date: "2021-06-09 12:30:27" 
title: "chrome 为什么多进程而不是多线程"
categories:
  - chrome
tags:
  - reprint
---
## chrome 为什么多进程而不是多线程

https://www.zhihu.com/question/368712837

多进程有四点好处。1，chromium项目创建初期，webkit不属于谷歌。他们对苹果的东西不信任，而且各种页面渲染时候的崩溃也很大。那时候webkit在chromium里的地位就是个小小第三方库。所以需要把渲染放到另外个进程防止崩溃了影响主进程。2，同样的，webkit那时候很多内存泄露。多进程能很大程度避免。一个进程关了，所有内存就回收了。当时谷歌还写文章鄙视了下那些说多进程占用内存多的人。3，多进程安全性更好。如果blink被发现什么提权漏洞，例如写一段js就能控制整个chromium进程做任何事情，显然多进程可以把损失限制在渲染线程。渲染线程拿不到主进程的各种私密信息，例如别的域名下的密码4，另外有个点大家没说的地方就是，webkit内部很多全局变量。如果要做到一个页面一个线程，理论上很难搞。谷歌其实考虑过想搞一个单进程多线程模式，后来发现不好搞就放弃了。。这个模式在移动平台还是有优势的。以前的手机性能和内存还很差。多进程很消耗内存。chromium刚移植到安卓上时，还是30几版本。性能和稳定性远不如webkit单进程。那时候安卓版chromium就是单进程模式。

作者: 龙泉寺扫地僧
链接: https://www.zhihu.com/question/368712837/answer/994040540
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



Chromium里有三种进程——浏览器、渲染器和插件。浏览器进程只有一个，管理窗口和tab，也处理所有的与磁盘，网络，用户输入和显示的工作。这就是我们看到的“Chrome界面”。渲染器开多个。每个渲染器负责处理HTML、CSS、js、图片等，将其转换成用户可见的数据。当时Chrome使用开源的webkit实现这个功能。顺便说一句，webkit是由Apple开发的，当时有很多坑，也被长期吐槽；现在Chrome已经转成使用自家的Blink引擎了。插件会开很多。每个类型的插件在第一次使用时会启动一个相应的进程。

作者: 大宽宽
链接: https://www.zhihu.com/question/368712837/answer/999401453
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。




Blink不再是WebKit: http://www.chromium.org/blink
BLINK内核就是谷歌公司，针对WEBKIT内核，做的修订和精简。
去掉了几十万行的没用的复杂代码，让效率更高。然后针对未来的网页格式，做了进一步优化，和效率提升的处理。
所以BLINK内核可以看成是WEBKIT的精简高效强化版。


---

https://blog.chromium.org/2008/09/multi-process-architecture.html