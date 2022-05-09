---
title: google firstitemmsec
author: "-"
date: 2012-07-09T14:51:56+00:00
url: /?p=3838
categories:
  - Inbox
tags:
  - reprint
---
## google firstitemmsec
Get subscription list. Each subscription contains a "category" if the user had created folders. It also has a field called `firstitemmsec` that denotes in milliseconds the time from which entries for that feed should be picked up.

`firstitemmsec` initially stumped me until I added a new subscription. I noticed that Google Reader has entries for a feed spanning back to a month (probably -infinity). So the reader has to know to show you articles _only from the time you subscribed to a feed_.

`ot` is the parameter that takes `firstitemmsec / 1000` when you are fetching the reading list or a particular feed.


{"subscriptions":[{"id":"feed/供稿地址","title":"供稿名","categories":[{"id":"user/Google Reader用户ID/label/分类名","label":"分类名"}],"sortid":"不知道啥玩意","firstitemmsec":"第一个条目的时间戳","htmlUrl":"供稿的网站地址"},...(其他供稿的信息)]}


获取预定列表。如果用户已创建了文件夹，每个预定包含一个"category"。它还有一个域，称为firstitemmsec ，以毫秒为单位，说明feed条目应该被提取的时间.

firstitemmsec 起初难倒了我, 直到我添加了一个新的预定。我注意到，GOOGLE阅读器的feed条目可回溯一个月之长 (可能是无限期的) 。因此，阅读器只能从你订阅的时间上判断，向你显示文章。

<http://anirudhsasikumar.net/blog/2009.11.04.html>

<http://www.keakon.net/2011/07/11/GoogleReaderAPI%E7%AE%80%E4%BB%8B>

<http://blog.csdn.net/lihe111/article/details/5437993>