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
select 'delete from ' || ut.table\_name || ';' from user\_tables ut;