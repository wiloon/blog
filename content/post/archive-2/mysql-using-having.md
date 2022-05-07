---
title: MySQL using having
author: "-"
date: 2017-11-22T06:17:25+00:00
url: /?p=11462
categories:
  - Inbox
tags:
  - reprint
---
## MySQL using having
http://wuzhangshu927.blog.163.com/blog/static/1142246872010113093426574/

  1. USING()

using可用在join语句相同字段连接,起到和ON相同作用,inner join 和left join中都可以使用

示例: 

LEFT JOIN 正常写法: 

     SELECT t1.id,t2.name FROM t1 LEFT JOIN t2 ON t1.id=t2.id WHERE ....
    

其实也可以这么写: 

     SELECT t1.id,t2.name FROM t1 LEFT JOIN t2 USING(id) WHERE ....
    

  1. HAVING

MySQL中的where和having子句都可以实现筛选记录的功能,having 可以认为是对where的补充,因为它可以对分组数据进行再次判断,一般跟在group by 后面,并可以使用聚集函数(sum,min,max,avg,count)

示例: 

    SELECT `uid`,SUM(`points`) num FROM table GROUP BY `uid` HAVING num>1000