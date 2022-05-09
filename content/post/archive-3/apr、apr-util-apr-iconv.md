---
title: apr、apr-util, apr-iconv
author: "-"
date: 2019-05-30T01:51:38+00:00
url: /?p=14422
categories:
  - Inbox
tags:
  - reprint
---
## apr、apr-util, apr-iconv
https://my.oschina.net/shawnplaying/blog/1518144

安装Apache的时候，为什么要安装apr和apr-util呢

要测APR给tomcat带来的好处最好的方法是在慢速网络上 (模拟Internet) ，将Tomcat线程数开到300以上的水平，然后模拟一大堆并发请求。如果不配APR，基本上300个线程狠快就会用满，以后的请求就只好等待。但是配上APR之后，并发的线程数量明显下降，从原来的300可能会马上下降到只有几十，新的请求会毫无阻塞的进来。

APR对于Tomcat最大的作用就是socket调度。

你在局域网环境测，就算是400个并发，也是一瞬间就处理/传输完毕，但是在真实的Internet环境下，页面处理时间只占0.1%都不到，绝大部分时间都用来页面传输。如果不用APR，一个线程同一时间只能处理一个用户，势必会造成阻塞。所以生产环境下用apr是非常必要的。

注: APR(Apache portable Run-time libraries，Apache可移植运行库)的目的如其名称一样，主要为上层的应用程序提供一个可以跨越多操作系统平台使用的底层支持接口库。
  
在早期的Apache版本中，应用程序本身必须能够处理各种具体操作系统平台的细节，并针对不同的平台调用不同的处理函数。随着Apache的进一步开发，Apache组织决定将这些通用的函数独立出来并发展成为一个新的项目。这样，APR的开发就从Apache中独立出来，Apache仅仅是使用APR而已。
  
一般情况下，APR开发包很容易理解为仅仅是一个开发包，不过事实上并不是。目前，完整的APR实际上包含了三个开发包: apr、apr-util以及apr-iconv，每一个开发包分别独立开发，并拥有自己的版本。