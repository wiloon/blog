---
title: state和status的区别
author: "-"
date: 2019-11-08T01:49:28+00:00
url: /?p=15130
categories:
  - Inbox
tags:
  - reprint
---
## state和status的区别
state和status的区别

state: 比较常用，各种状态都可以用它，但是它更着重于一种心理状态或者物理状态。
  
Status: 用在人的身上一般是其身份和地位，作"状态，情形"讲时，多指政治和商业。

state倾向于condition，是一种延续性的状态。status常用于描述一个过程中的某阶段 (phase) ，类似于C语言中枚举型变量某一个固定的值，这个值属于一个已知的集合。
  
比如淘宝买家问卖家"我的网购现在是什么状况？"
  
这个问题的背景是讲话双方都清楚，交易状态有"买家选购""买家已付款""卖家已发货""买家已签收"或者有"买家已
  
投诉"等等状态。这些状态描述一件事情发展过程中的不同阶段。而且，这些阶段的先后顺序也是双方默许的。
  
所以在这里可以问"What's the status of my purchase?"，此处用state不太贴切，如果硬用上去从语感上可能听着别扭。

说物态变化用state再恰当不过。如果说一个物质的四种状态，可以说"solid state"，但如果你说"solid status"，第
  
一，这两个词的组合不像是描述物态，更像是在说"确定的状况 (solid产生歧义'确定的/确凿的') "；第二，这个说法即
  
使不被误解，也需要事先约定一组物态变化顺序，比如把这个物质从固态开始加热然后电离，可能先后经历固态、液态、气态、等离子态这四个阶段。类似先定义枚举，然后引用的方式。

扩展: 

ajax中readyState，statusText，onreadystatechange，window.status怎么一会state一会是status都晕乎了

state所指的状态，一般都是有限的、可列举的，status则是不可确定的。
  
比如
  
readyState - 就那么四五种值
  
statusText - 描述性的文字，可以任意
  
onreadystatechange - 那么四五种值之间发生变化
  
window.status - 描述性的文字，可以任意

来个形象的比方，你体重多少公斤，属于status，但说你体重属于偏瘦、正常还是偏胖，那就是state.

https://www.cnblogs.com/likebeta/archive/2012/07/03/2574595.html