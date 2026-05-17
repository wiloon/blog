---
title: generate delete sql
author: "-"
date: 2011-11-25T09:19:07+00:00
url: generate-delete-sql
categories:
  - Database
tags:
  - reprint
aliases:
  - /p1598/
---
## generate delete sql
select 'delete from ' || ut.table_name || ';' from user_tables ut;