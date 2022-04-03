---
title: Row_number () over (partition by col1 order by col2)的用法
author: "-"
date: 2013-05-08T03:13:29+00:00
url: /?p=5430
categories:
  - DataBase
tags:
  - oracle

---
## Row_number () over (partition by col1 order by col2)的用法

### oracle row_number 函数
```sql
ROW_NUMBER() OVER (PARTITION BY COL1 ORDER BY COL2) --其中，COL1，COL2可以为多列
select xt.id, xt.item, xt.attribute1, xt.attribute2, 
ROW_NUMBER() OVER(PARTITION BY xt.id,xt.item order by xt.id,xt.item) test
from xxuts_test xt
```


表示根据COL1分组，在分组内部根据 COL2排序
  
而这个值就表示每组内部排序后的顺序编号 (组内连续的唯一的) 

RANK() 类似，不过RANK 排序的时候跟派名次一样，可以并列2个第一名之后 是第3名

LAG 表示 分组排序后 ，组内后面一条记录减前面一条记录的差，第一条可返回 NULL

BTW: EXPERT ONE ON ONE 上讲的最详细,还有很多相关特性，文档看起来比较费劲

row_number()和rownum差不多，功能更强一点 (可以在各个分组内从1开时排序) 
  
rank()是跳跃排序，有两个第二名时接下来就是第四名 (同样是在各个分组内) 
  
dense_rank()l是连续排序，有两个第二名时仍然跟着第三名。
  
相比之下row_number是没有重复值的
  
lag (arg1,arg2,arg3):
  
arg1是从其他行返回的表达式
  
arg2是希望检索的当前行分区的偏移量。是一个正的偏移量，时一个往回检索以前的行的数目。
  
arg3是在arg2表示的数目超出了分组的范围时返回的值。



### 按照名字分组查询时间最早的一条记录
 
给出2种解决方案

rownumber

SELECT *
FROM
(
SELECT IdentityID, OpenID, ROW_NUMBER() OVER(PARTITION BY OpenID ORDER BY CreateTime DESC
) AS rownumber FROM dbo.T_Account
) AS tmp
WHERE tmp.rownumber = 1
相关子查询

SELECT DISTINCT OpenID, test1.IdentityID FROM dbo.T_Account
AS test1
WHERE test1.IdentityID
IN
(
SELECT TOP 1 IdentityID FROM dbo.T_Account
WHERE dbo.T_Account.OpenID =  test1.OpenID
ORDER BY CreateTime DESC
 
)

>https://www.shuzhiduo.com/A/8Bz8kWENdx/