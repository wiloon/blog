---
title: "DataGrip"
author: "-"
date: "2022-07-03 21:19:05"
url: "DataGrip"
categories:
  - "Inbox"
tags:
  - "Inbox"
  - "reprint"
---
## DataGrip

## console 中使用变量

```sql
select *
from public.actor
where actor.actor_id < ${a}

```

## 导出建表语句

打开DataGrip、找到目标表
选中之后右键点击SQL Scripts→SQL Generator.
就可以看到建表语句了
