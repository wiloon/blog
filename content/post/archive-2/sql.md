---
title: sql basic
author: "-"
date: 2017-07-26T01:09:13+00:00
url: sql
categories:
  - Database
tags:
  - reprint
  - remix
---
# sql basic

## between and

BETWEEN 用以查询确定范围的值，这些值可以是数字，文本或日期 。  
BETWEEN 运算符是闭区间的：包括开始 和 结束值 。  
not between 则是不包含前后边界的  

## select

```SQL
select * from table0 where column0!='';
```

!='' 会过滤掉值为 null 的数据.

The reason is simple: nulls are neither equal, nor not equal, to anything. This makes sense when you consider that null means "unknown", and the truth of a comparison to an unknown value is also unknown.

The corollary is that:

null = null is not true
null = some_value is not true
null != some_value is not true
The two special comparisons IS NULL and IS NOT NULL exist to deal with testing if a column is, or is not, null. No other comparisons to null can be true.

[https://stackoverflow.com/questions/19974472/postgres-excludes-null-in-where-id-int-query](https://stackoverflow.com/questions/19974472/postgres-excludes-null-in-where-id-int-query)
