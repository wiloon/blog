---
title: Oracle 分页
author: lcf
date: 2012-11-15T08:20:35+00:00
url: /?p=4693
categories:
  - DataBase

tags:
  - reprint
---
## Oracle 分页

```sql
select * from (
       select page.\*,rownum rn from (select \* from help) page
       - 20 = (currentPage-1) * pageSize + pageSize
       where rownum <= 20
)
- 10 = (currentPage-1) * pageSize
where rn > 10;
```