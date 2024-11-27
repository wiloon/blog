---
title: MySQL 聚集函数
author: "-"
date: 2016-01-28T05:30:38+00:00
url: /?p=8718
categories:
  - Inbox
tags:
  - reprint
---
## MySQL 聚集函数
1. 聚集函数
  
聚集函数是运行在行组上,计算和返回单个值的函数。

SQL聚集函数
  
函数
  
说明
  
AVG()
  
返回某列的平均值
  
COUNT()
  
返回某列的行数
  
MAX()
  
返回某列的最大值
  
MIN()
  
返回某列的最小值
  
SUM()
  
返回某个列之和
  
 (1) 、AVG()函数
  
可以返回所有列的平均值,也可以返回特定列的平均值。
  
```sql``` 
  
print?
  
SELECT AVG(prd_price) AS avg_price FROM products
  
Where vend_id=1003;

将过滤出vend_id=1003的产品,avg是这些产品的平均值.
  
 (2) 、COUNT()函数
  
COUNT(*)对表中行的数目进行计数,不管表列中包含的是空 (NULL) 还是非空值；
  
COUNT(column)对特定列中有值的行进行计算,忽略NULL值。

 (3) 、MAX()函数
  
MAX()返回指定列的最大值,要求指定列名,忽略NULL值。
  
在MySQL中,MAX()函数可以对非数据列使用,在用于文本数据时,如果数据按相应的列排序,MAX()返回最后一行。
  
 (4) 、MIN()函数
  
MIN()返回指定列的最小值,要求指定列名,忽略NULL值。

在MySQL中,MIN()函数可以对非数据列使用,在用于文本数据时,如果数据按相应的列排序,MIN()返回最前面的一行。

 (5) 、SUM()函数
  
用来返回指定列的和 (总计) ,忽略NULL值的行。
  
```sql``` 
  
print?
  
SELECT SUM(num) AS prod_sum-返回指定订单号中的商品数量
  
FROM products
  
Where order_id=123456;
  
SUM()也可以合计计算值。
  
```sql``` 
  
print?
  
SELECT SUM(item_price*num) AS totol_price FROM order_items-返回订单中所有商品价格和。
  
Where order_id=123456;
  
2. 聚集不同值
  
DISTINCT关键字
  
如下面的SQL将返回vend_id=1003的不同价格商品的平均值
  
```sql``` 
  
print?
  
SELECT AVG(DISTINCT prd_price) AS avg_price FROM products
  
Where vend_id=1003;

3. 组合聚集函数
  
聚集函数可以组合使用
  
```sql``` 
  
print?
  
SELECT count(*) AS num,
  
MIN(prod_price) AS price_min,
  
MAX(prod_price) AS price_max,
  
AVG(prod_price) AS price_avg
  
FROM products;