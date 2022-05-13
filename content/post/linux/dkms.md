---
author: "-"
date: "2020-05-30T06:52:05Z"
title: "DKMS"
categories:
  - inbox
tags:
  - reprint
---
## "DKMS"
## DKMS
我们都知道，如果要使用没有集成到内核之中的Linux驱动程序需要手动编译。当然，这并不是一件什么难事，即使是对于没有编程经验的Linux使用者，只要稍微有点hacker的意识，努力看看代码包里的Readme或者INSTALL文件，按部就班的执行几条命令还是很容易办到的。但这里还有一个问题，Linux模块和内核是有依赖关系的，如果遇到因为发行版更新造成的内核版本的变动，之前编译的模块是无法继续使用的，我们只能手动再编译一遍。这样重复的操作有些繁琐且是反生产力的，而对于没有内核编程经验的使用者来说可能会造成一些困扰，使用者搞不清楚为什么更新系统之后，原来用的好好的驱动程序突然就不能用了。这里，就是Dell创建的DKMS项目的意义所在。DKMS全称是Dynamic Kernel Module Support，它可以帮我们维护内核外的这些驱动程序，在内核版本变动之后可以自动重新生成新的模块。

[https://www.cnblogs.com/wwang/archive/2011/06/21/2085571.html](https://www.cnblogs.com/wwang/archive/2011/06/21/2085571.html "https://www.cnblogs.com/wwang/archive/2011/06/21/2085571.html")

>https://www.cnblogs.com/wwang/archive/2011/06/21/2085571.html