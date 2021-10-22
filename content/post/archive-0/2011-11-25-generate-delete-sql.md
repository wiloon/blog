---
title: generate delete sql
author: "-"
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
## generate delete sql
select 'delete from ' || ut.table_name || ';' from user_tables ut;