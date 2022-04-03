---
title: MySQL 横表和纵表转换
author: "-"
date: 2014-01-17T12:43:57.000+00:00
url: "/?p=6232"
categories:
- Uncategorized
tags:
- MySQL

---
## MySQL 横表和纵表转换
 (1) 表tb1有如下数据: 

 姓名                     语文                        数学                    物理

 张三                       68                           89                        99

 李四                      90                            66                         78 

现在要求写出查询语句得到如下查询结果  name                    subject                       score

 张三                       语文                           68

 张三                       数学                           89

 张三                       物理                            99

 李四                       语文                            90

李四                      数学                            66

李四                       物理                            78 

sql语句如下: 

select 姓名 as name,'语文' as subject,语文 as score from tb1

union select 姓名 as name,'数学' as subject,数学 as score from tb1

union  select 姓名 as name,'物理' as subject,物理 as score from tb1

 order by name 
或者: 


select * from(
 select 姓名 as name,'语文' as subject,语文 as score from tb1
 union
 select 姓名 as name,'数学' as subject,数学 as score from tb1
 union
 select 姓名 as name,'物理' as subject,物理 as score from tb1
 )tb
 order by name


 (2) tb2表有如下数据: 


name              subject                  score


张三               语文                       74
 张三                英语                      88
 张三                物理                       90
 李四                语文                      88
 李四                英语                      67
 李四                物理                        95


 


通过查询得到如下数据: 


姓名         语文                  英语                     物理


张三          74                   88                        90
 李四           88                    67                        95


 


sql语句如下: 


select name as '姓名',
 max(case subject when '语文' then score else 0 end) 语文,
 max(case subject when '英语' then score else 0 end) 英语,
 max(case subject when '物理' then score else 0 end)物理
 from tb2
 group by name


现在要求写出查询语句得到如下结果: 


姓名         语文                  英语                     物理            总分                平均分


张三          74                    88                        90               252                    84
 李四           88                    67                        95                250                    83.33


 


sql:


select name '姓名',
 max(case subject when '语文' then result else 0 end) 语文,
 max(case subject when '物理' then result else 0 end) 物理,
 max(case subject when '英语' then result else 0 end)英语,
 sum(result) as 总分,
 avg(result) as 平均分
 from tb
 group by name

