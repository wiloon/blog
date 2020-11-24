---
title: jquery autocomplete
author: w1100n
type: post
date: 2013-03-21T08:42:55+00:00
url: /?p=5328
categories:
  - Web
tags:
  - JavaScript

---
主要的事件 jQuery UI Autocomplete有一些事件，可用于在一些阶段进行额外的控制：

create(event, ui)：Autocomplete创建时，可以在此事件中，对外观进行一些控制 search(event, ui)： 在开始请求之前，可以在此事件中返回false来取消请求 open(event, ui)：Autocomplete的结果列表弹出时 focus(event, ui)：Autocomplete的结果列表任意一项获得焦点时，ui.item为获得焦点的项 select(event, ui)：Autocomplete的结果列表任意一项选中时，ui.item为选中的项 close(event, ui)：Autocomplete的结果列表关闭时 change(event, ui)：当值改变时，ui.item为选中的项

http://www.cnblogs.com/lwme/archive/2012/02/12/jquery-ui-autocomplete.html