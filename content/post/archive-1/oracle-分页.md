---
title: Oracle 分页
author: lcf
date: 2012-11-15T08:20:35+00:00
url: /?p=4693
categories:
  - DataBase

---
## Oracle 分页
  1. - Oracle 分页算法一
  2. select * from (
  3.        select page.\*,rownum rn from (select \* from help) page
  4.        - 20 = (currentPage-1) * pageSize + pageSize
  5.        where rownum <= 20
  6. )
  7. - 10 = (currentPage-1) * pageSize
  8. where rn > 10;