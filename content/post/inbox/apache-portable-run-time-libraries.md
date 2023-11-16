---
title: apache portable run time libraries
author: "-"
date: 2018-02-23T09:41:04+00:00
url: /?p=11915
categories:
  - Inbox
tags:
  - reprint
---
## apache portable run time libraries

[http://blog.csdn.net/swartz_lubel/article/details/79215764](http://blog.csdn.net/swartz_lubel/article/details/79215764)

随着Apache的进一步开 发,Apache组织决定将这些通用的函数独立出来并发展成为一个新的项目。这样,APR的开发就从Apache中独立出来,Apache仅仅是使用 APR而已。目前APR主要还是由Apache使用,不过由于APR的较好的移植性,因此一些需要进行移植的C程序也开始使用APR,开源项目比如 Flood loader([http://httpd.apache.org/test/flood/,该项目用于服务器压力测试,不仅仅适用于Apache)、FreeSwitch(www.freeswitch.org),JXTA-C(http://jxta-c.jxta.org,C版本的JXTA点对点平台实现)；商业的项目则包括Blogline(http://www.bloglines.com/,covalent(http://www.covalent.net](http://httpd.apache.org/test/flood/,该项目用于服务器压力测试,不仅仅适用于Apache)、FreeSwitch(www.freeswitch.org),JXTA-C(http://jxta-c.jxta.org,C版本的JXTA点对点平台实现)；商业的项目则包括Blogline(http://www.bloglines.com/,covalent(http://www.covalent.net))等等。

APR使得平台细节的处理进行下移。对于应用程序而言,它们根本就不需要考虑具体的平台,不管是Unix、Linux还是Window,应用程序执行的接口基本都是统一一致的。因此对于APR而言,可移植性和统一的上层接口是其考虑的一个重点。而APR最早的目的并不是如此,它最早只是希望将Apache中用到的所有代码合并为一个通用的代码库,然而这不是一个正确的策略,因此后来APR改变了其目标。有的时候使用公共代码并不是一件好事,比如如何将一个请求映射到线程或者进程是平台相关的,因此仅仅一个公共的代码库并不能完成这种区分。APR的目标则是希望安全合并所有的能够合并的代码而不需要牺牲性能。

APR的最早的一个目标就是为所有的平台(不是部分)提供一个公共的统一操作函数接口,这是一个非常了不起的目的,当然也是不现实的一个目标。我们不可能支持所有平台的所有特征,因此APR目前只能为大多数平台提供所有的APR特性支持,包括Win32、OS/2、BeOS、Darwin、Linux等等。为了能够实现这个目标,APR开发者必须为那些不能运行于所有平台的特性创建了一系列的特征宏(FEATURE MACROS)以在各个平台之间区分这些特征。这些特征宏定义非常简单,通常用APR_HAS_FEATURE参数设置:

如果某个平台具有这个特性,则该宏必须设置为true,比如Linux和window都具有内存映射文件,同时APR提供了内存映射文件的操作接口,因此在这两个平台上,APR_HAS_MMAP宏必须设置,同时ap_mmap__函数应该将磁盘文件映射为内存并返回适当的状态码。如果你的操作系统并不支持内存映射,那么APR_HAS_MMAP必须设置为0,而且所有的ap_mmap__函数也可以不需要定义。第二步就是对于那些在程序中使用了不支持的函数必须提出警告。
