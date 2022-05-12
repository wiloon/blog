---
title: generate delete sql
author: "-"
date: 2011-11-25T09:19:07+00:00
url: /?p=1598
categories:
  - DataBase
tags:
  - reprint
---
## generate delete sql
select 'delete from ' || ut.table_name || ';' from user_tables ut;