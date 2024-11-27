---
title: linux tc
author: "-"
date: 2016-06-10T03:09:16+00:00
url: /?p=9052
categories:
  - Inbox
tags:
  - reprint
---
## linux tc
http://blog.csdn.net/qinyushuang/article/details/46611709

TC
  
在Linux中,流量控制都是通过TC这个工具来完成的。通常,要对网卡进行流量控制的配置,需要进行如下的步骤: 

◆ 为网卡配置一个队列；

◆ 在该队列上建立分类；

◆ 根据需要建立子队列和子分类；

◆ 为每个分类建立过滤器。

在Linux中,可以配置很多类型的队列,比如CBQ、HTB等,其中CBQ 比较复杂,不容易理解。HTB(Hierarchical Token Bucket)是一个可分类的队列, 与其他复杂的队列类型相比,HTB具有功能强大、配置简单及容易上手等优点。在TC中,使用"major:minor"这样的句柄来标识队列和类别,其中major和minor都是数字。

对于队列来说,minor总是为0,即"major:0"这样的形式,也可以简写为"major: "比如,队列1:0可以简写为1:。需要注意的是,major在一个网卡的所有队列中必须是惟一的。对于类别来说,其major必须和它的父类别或父队列的major相同,而minor在一个队列内部则必须是惟一的(因为类别肯定是包含在某个队列中的)。举个例子,如果队列2:包含两个类别,则这两个类别的句柄必须是2:x这样的形式,并且它们的x不能相同,比如2:1和2:2。