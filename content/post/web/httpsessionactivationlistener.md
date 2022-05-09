---
title: HttpSessionActivationListener
author: "-"
date: 2012-06-22T08:24:12+00:00
url: /?p=3605
categories:
  - Inbox
tags:
  - reprint
---
## HttpSessionActivationListener
HttpSessionActivationListener
  
jsp/servlet 标准不要求一个web容器支持分布式应用，
  
但是他一定要支持HttpSessionActivationListener借口，以使代码可以支持分布式环境。
  
一般免费的web容器都不支持分布式，weblogic websphere是支持的。
  
为了负载均衡或者fail-over,web容器可以迁移一个session到其他的jvm.
  
session的passivation是指非活动的session被写入持久设备 (比如硬盘) 。
  
activate自然就是相反的过程。在分布式环境中切换的属性必须实现serializable接口。

一般情况下他和HttpSessionBindingListener一起使用。
  
比如一个属性类，