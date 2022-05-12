---
title: sql 的四舍五入取整问题
author: "-"
date: 2013-08-20T07:44:44+00:00
url: /?p=5780
categories:
  - DataBase
tags:
  - reprint
---
## sql 的四舍五入取整问题
转自: <http://hi.baidu.com/yahuudang/blog/item/4c65ab77f758b01fb151b953.html>


经在sql server 2005测试，可以通过


SELECT CAST('123.456' as decimal) 将会得到 123 (小数点后面的将会被省略掉) 。
  
如果希望得到小数点后面的两位。
  
则需要把上面的改为
  
SELECT CAST('123.456' as decimal(38, 2)) ===>123.46
  
自动四舍五入了！


自己的例子: 
  
select CAST(AmountRmb as decimal(38)) as heji,CAST(NotFinFee as decimal(38)) as whx,* from Bill_Tab