---
title: Provider 模式
author: "-"
date: 2011-08-20T18:43:35+00:00
url: provider
categories:
  - Linux

tags:
  - reprint
---
## Provider 模式

首先什么是Provider模式？Provider是由两个设计模式融合而来的: 策略模式+抽象工厂模式。这两个模式具体的介绍我在这里就不多说了，网上一搜一大把。provider模式的作用是为一个API进行定义和实现的分离。这样就通过核心功能的灵活性和易于修改的特点使得API具有灵活性。通俗一点来说就是实现了定义和实现的分离，最终效果就是不需要更改代码即可实现程序不同逻辑的改变。

在BlogEngine中，provider模式被应用于提供不同的数据的持久化。为了保证解压后就能使用默认采用的是xmlProvider。本文研究的重点就是了解这个Provider模式，并知道BlogEngine如何通过provider模式使得不同数据持久化方式之间的灵活切换。

>https://www.cnblogs.com/qianlifeng/archive/2010/12/07/1899343.html
