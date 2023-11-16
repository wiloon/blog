---
title: DelayQueue
author: "-"
date: 2013-02-25T13:46:31+00:00
url: DelayQueue
categories:
  - Java
tags:
  - reprint
---
## DelayQueue

DelayQueue 是什么
　　DelayQueue 是一个无界的 BlockingQueue，用于放置实现了Delayed接口的对象，其中的对象只能在其到期时才能从队列中取走。这种队列是有序的，即队头对象的延迟到期时间最长。注意：不能将null元素放置到这种队列中。

二、DelayQueue 能做什么
　1. 淘宝订单业务: 下单之后如果三十分钟之内没有付款就自动取消订单。
　2. 饿了吗订餐通知: 下单成功后60s之后给用户发送短信通知。

　3.关闭空闲连接。服务器中，有很多客户端的连接，空闲一段时间之后需要关闭之。

　4.缓存。缓存中的对象，超过了空闲时间，需要从缓存中移出。

　5.任务超时处理。在网络协议滑动窗口请求应答式交互时，处理超时未响应的请求等。

三、实例展示
　定义元素类，作为队列的元素

　DelayQueue只能添加(offer/put/add)实现了Delayed接口的对象，意思是说我们不能想往DelayQueue里添加什么就添加什么，不能添加int、也不能添加String进去，必须添加我们自己的实现了Delayed接口的类的对象，来代码

[https://www.cnblogs.com/myseries/p/10944211.html](https://www.cnblogs.com/myseries/p/10944211.html)

DelayQueue基本原理

DelayQueue是一个没有边界BlockingQueue实现，加入其中的元素必需实现Delayed接口。当生产者线程调用put之类的方法加入元素时，会触发Delayed接口中的compareTo方法进行排序，也就是说队列中元素的顺序是按到期时间排序的，而非它们进入队列的顺序。排在队列头部的元素是最早到期的，越往后到期时间赿晚。

消费者线程查看队列头部的元素，注意是查看不是取出。然后调用元素的getDelay方法，如果此方法返回的值小０或者等于０，则消费者线程会从队列中取出此元素，并进行处理。如果getDelay方法返回的值大于0，则消费者线程wait返回的时间值后，再从队列头部取出元素，此时元素应该已经到期。

DelayQueue是Leader-Followr模式的变种，消费者线程处于等待状态时，总是等待最先到期的元素，而不是长时间的等待。消费者线程尽量把时间花在处理任务上，最小化空等的时间，以提高线程的利用效率。

以下通过队列及消费者线程状态变化大致说明一下DelayQueue的运行过程。
————————————————
版权声明：本文为CSDN博主「五星上炕」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/dkfajsldfsdfsd/article/details/88966814](https://blog.csdn.net/dkfajsldfsdfsd/article/details/88966814)
