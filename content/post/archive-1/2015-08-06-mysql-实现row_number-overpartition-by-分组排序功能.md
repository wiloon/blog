---
title: MYSQL-实现row_number() over(partition by ) 分组排序功能
author: wiloon
type: post
date: 2015-08-06T11:25:24+00:00
url: /?p=8069
categories:
  - Uncategorized

---
http://mrcelite.blog.51cto.com/2977858/745913

&nbsp;

原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://mrcelite.blog.51cto.com/2977858/745913
  
由于MYSQL没有提供类似ORACLE中OVER()这样丰富的分析函数. 所以在MYSQL里需要实现这样的功能,我们只能用一些灵活的办法:

1.首先我们来创建实例数据:

drop table if exists heyf_t10;
  
create table heyf_t10 (empid int ,deptid int ,salary decimal(10,2) );

insert into heyf_t10 values
  
(1,10,5500.00),
  
(2,10,4500.00),
  
(3,20,1900.00),
  
(4,20,4800.00),
  
(5,40,6500.00),
  
(6,40,14500.00),
  
(7,40,44500.00),
  
(8,50,6500.00),
  
(9,50,7500.00);

2. 确定需求: 根据部门来分组,显示各员工在部门里按薪水排名名次.

显示结果预期如下:

+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+
  
| empid | deptid | salary | rank |
  
+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+
  
| 1 | 10 | 5500.00 | 1 |
  
| 2 | 10 | 4500.00 | 2 |
  
| 4 | 20 | 4800.00 | 1 |
  
| 3 | 20 | 1900.00 | 2 |
  
| 7 | 40 | 44500.00 | 1 |
  
| 6 | 40 | 14500.00 | 2 |
  
| 5 | 40 | 6500.00 | 3 |
  
| 9 | 50 | 7500.00 | 1 |
  
| 8 | 50 | 6500.00 | 2 |
  
+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+

3. SQL 实现

select empid,deptid,salary,rank from (
  
select heyf\_tmp.empid,heyf\_tmp.deptid,heyf_tmp.salary,@rownum:=@rownum+1 ,
  
if(@pdept=heyf_tmp.deptid,@rank:=@rank+1,@rank:=1) as rank,
  
@pdept:=heyf_tmp.deptid
  
from (
  
select empid,deptid,salary from heyf_t10 order by deptid asc ,salary desc
  
) heyf_tmp ,(select @rownum :=0 , @pdept := null ,@rank:=0) a ) result
  
;

4. 结果演示

mysql> select empid,deptid,salary,rank from (
  
-> select heyf\_tmp.empid,heyf\_tmp.deptid,heyf_tmp.salary,@rownum:=@rownum+1 ,
  
-> if(@pdept=heyf_tmp.deptid,@rank:=@rank+1,@rank:=1) as rank,
  
-> @pdept:=heyf_tmp.deptid
  
-> from (
  
-> select empid,deptid,salary from heyf_t10 order by deptid asc ,salary desc
  
-> ) heyf_tmp ,(select @rownum :=0 , @pdept := null ,@rank:=0) a ) result
  
-> ;
  
+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+
  
| empid | deptid | salary | rank |
  
+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+
  
| 1 | 10 | 5500.00 | 1 |
  
| 2 | 10 | 4500.00 | 2 |
  
| 4 | 20 | 4800.00 | 1 |
  
| 3 | 20 | 1900.00 | 2 |
  
| 7 | 40 | 44500.00 | 1 |
  
| 6 | 40 | 14500.00 | 2 |
  
| 5 | 40 | 6500.00 | 3 |
  
| 9 | 50 | 7500.00 | 1 |
  
| 8 | 50 | 6500.00 | 2 |
  
+&#8212;&#8212;-+&#8212;&#8212;&#8211;+&#8212;&#8212;&#8212;-+&#8212;&#8212;+
  
9 rows in set (0.00 sec)

MySql中取出每个分组中的前N条记录
  
select a1.* from article a1

inner join

(select a.type,a.date from article a left join article b

on a.type=b.type and a.date<=b.date

group by a.type,a.date

having count(b.date)<=2

)b1

on a1.type=b1.type and a1.date=b1.date

order by a1.type,a1.date desc