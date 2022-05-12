---
title: 从HTTP GET和POST的区别说起
author: "-"
date: 2012-06-03T11:45:35+00:00
url: /?p=3385
categories:
  - Java
  - Web
tags:$
  - reprint
---
## 从HTTP GET和POST的区别说起

  Zhang Yining / CC BY-NC-SA 3.0

http://www.yining.org/2010/05/04/http-get-vs-post-and-thoughts/

在推特上[抱怨面试时问HTTP GETE和POST的区别得到回答都不满意][1]，有人不清楚，当时只回复了看 RFC2616。趁有空说说

面试时得到的回答大多是: POST是安全的，因为被提交的数据看不到，或者被加密的，其它的还有GET的时候中文出现乱码 (在地址栏里) ，数据最大长度限制等等。

说 POST 比 GET 安全肯定是错的，POST跟GET都是明文传输，用[httpfox][2]等插件，或者像[WireShark ][3]等类似工具就能观察到。

POST和GET的差别其实是很大的。语义上，GET是获取指定URL上的资源，是读操作，重要的一点是不论对某个资源GET多少次，它的状态是不会改变的，在这个意义上，我们说GET是安全的 (不是被密码学或者数据保护意义上的安全) 。因为GET是安全的，所以GET返回的内容可以被浏览器，Cache服务器缓存起来 (其中还有很多细节，但不影响这里的讨论) 。

而POST的语意是对指定资源"追加/添加"数据，所以是不安全的，每次提交的POST，参与的代码都会认为这个操作会修改操作对象资源的状态，于是，浏览器在你按下F5的时候会跳出确认框，缓存服务器不会缓存POST请求返回内容。

很遗憾到目前为止没有应聘者能够提到这一点。我猜测这背后的原因大概有两个，一是也许大多数人往往 (我也一样) 满足于只要完成任务就好，不管用哪个，表单提交了，数据处理了，内容显示或者重新定向到另外一个页面，就算完成了一个任务，从任务表里划掉，结束。而且对大部分项目(OA, CRM, MIS)的大部分情况下，用哪个似乎都可以。

同时，在被商业机构在媒体和书籍上宣传兜售的WS-*概念和使用集成开发环境提供的"方便"的代码生成工具后，"了解"到所有Web服务调用都是通过POST，更潜意识里确定了POST和GET是一样的，而且GET能做的，POST都能做，POST简直就是GET++嘛。自然，能用POST就用POST，不必在乎两者的差别了。

这又让我想起最近学到的一个概念: Radius Of Comprehension，理解的半径:

当学习概念A的时候，需要先了解概念B，而概念C又是理解B的前提。当B和C都是新的需要学习的概念时，可以说A的理解半径是2，如图:

A --> B --> C
|--1--|--2--|

在学习Web开发时，接触到GET和POST时，"理解的半径"可能包涵:

POST vs. GET
     |---> Conditional GET -> ETag -> Cache
     |         `--> Status Code
     `---> HTTP的方法 --> URL

往往因为仅仅满足于完成手上被要求的任务，或者懒于问一个为什么，我们就把自己的理解半径设置成零，那么就学不到更深入的东西，也因此仅仅知道POST和GET不同，而不再会了解不同在哪里，什么是Conditional GET和缓存header等概念。

从一个简单的面试问题谈到这，貌似小题大作了，写到哪算哪吧。

<UPDATE>
  
看到Fenng [Buzz 了这篇文字][4]，引起一些评论，因此在这再讨论两个概念: [安全的(Safe)和幂等的(Idempotent)][5]。

安全的是指没有明显的对用户有影响的副作用(包括修改该资源的状态)。HTTP方法里的GET和HEAD都是安全的。

幂等的是指一个方法不论多少次操作，结果都是一样。PUT(把内容放到指定URL)，DELETE(删除某个URL代表的资源)，虽然都修改了资源内容，但多次操作，结果是相同的，因此和HEAD，GET一样都是幂等的。

所以根据HTTP协议，GET是安全的，也是幂等的，而POST既不是安全的，也不是幂等的。
  
</UPDATE>

<http://www.yining.org/2010/05/04/http-get-vs-post-and-thoughts/>

 [1]: http://twitter.com/yining/status/12993863581
 [2]: http://code.google.com/p/httpfox/
 [3]: http://www.wireshark.org/
 [4]: http://www.google.com/buzz/dbanotes/BuxABaL5oam/%E4%BB%8EHTTP-GET%E5%92%8CPOST%E7%9A%84%E5%8C%BA%E5%88%AB%E8%AF%B4%E8%B5%B7-Yining
 [5]: http://tools.ietf.org/html/rfc2616#section-9.1