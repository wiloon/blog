---
title: generate delete sql
author: wiloon
type: post
date: 2011-11-25T09:19:07+00:00
url: /?p=1598
bot_views:
  - 7
views:
  - 1
categories:
  - DataBase

---
select &#8216;delete from &#8216; || ut.table\_name || &#8216;;&#8217; from user\_tables ut;