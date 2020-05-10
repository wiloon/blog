---
title: google firstitemmsec
author: wiloon
type: post
date: 2012-07-09T14:51:56+00:00
url: /?p=3838
categories:
  - Uncategorized

---
Get subscription list. Each subscription contains a &#8220;category&#8221; if the user had created folders. It also has a field called `firstitemmsec` that denotes in milliseconds the time from which entries for that feed should be picked up.

`firstitemmsec` initially stumped me until I added a new subscription. I noticed that Google Reader has entries for a feed spanning back to a month (probably -infinity). So the reader has to know to show you articles _only from the time you subscribed to a feed_.

`ot` is the parameter that takes `firstitemmsec / 1000` when you are fetching the reading list or a particular feed.

&nbsp;

{&#8220;subscriptions&#8221;:[{&#8220;id&#8221;:&#8221;feed/供稿地址&#8221;,&#8221;title&#8221;:&#8221;供稿名&#8221;,&#8221;categories&#8221;:[{&#8220;id&#8221;:&#8221;user/Google Reader用户ID/label/分类名&#8221;,&#8221;label&#8221;:&#8221;分类名&#8221;}],&#8221;sortid&#8221;:&#8221;不知道啥玩意&#8221;,&#8221;firstitemmsec&#8221;:&#8221;第一个条目的时间戳&#8221;,&#8221;htmlUrl&#8221;:&#8221;供稿的网站地址&#8221;},&#8230;(其他供稿的信息)]}

&nbsp;

获取预定列表。如果用户已创建了文件夹，每个预定包含一个“category”。它还有一个域，称为firstitemmsec ，以毫秒为单位，说明feed条目应该被提取的时间.

firstitemmsec 起初难倒了我, 直到我添加了一个新的预定。我注意到，GOOGLE阅读器的feed条目可回溯一个月之长（可能是无限期的）。因此，阅读器只能从你订阅的时间上判断，向你显示文章。

<http://anirudhsasikumar.net/blog/2009.11.04.html>

<http://www.keakon.net/2011/07/11/GoogleReaderAPI%E7%AE%80%E4%BB%8B>

<http://blog.csdn.net/lihe111/article/details/5437993>