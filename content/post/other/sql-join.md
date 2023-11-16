---
title: sql join
author: "-"
date: 2012-11-14T07:37:09+00:00
url: sql/join
categories:
  - DataBase
tags:
  - reprint
---
## sql join

## 多个条件

```sql
SELECT a.* FROM product a LEFT JOIN product_details b
ON a.id=b.id AND b.weight!=44 AND b.exist=0
WHERE b.id IS NULL;
```

### join

```sql
inner join(等值连接) 只返回两个表中联结字段相等的行
left join(左联接) 返回包括左表中的所有记录和右表中联结字段相等的记录
right join(右联接) 返回包括右表中的所有记录和左表中联结字段相等的记录
```

INNER JOIN 语法:

**INNER JOIN 连接两个数据表的用法:**
  
SELECT * FROM 表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号

**INNER JOIN 连接三个数据表的用法:**
  
SELECT * FROM (表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号

**INNER JOIN 连接四个数据表的用法:
  
** SELECT * FROM ((表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号) INNER JOIN 表4 ON Member.字段号=表4.字段号

**INNER JOIN 连接五个数据表的用法:**
  
SELECT * FROM (((表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号) INNER JOIN 表4 ON Member.字段号=表4.字段号) INNER JOIN 表5 ON Member.字段号=表5.字段号

连接六个数据表的用法: 略,与上述联接方法类似,大家举一反三吧: )

**注意事项:**

* 在输入字母过程中,一定要用英文半角标点符号,单词之间留一半角空格；
* 在建立数据表时,如果一个表与多个表联接,那么这一个表中的字段必须是"数字"数据类型,而多个表中的相同字段必须是主键,而且是"自动编号"数据类型。否则,很难联接成功。
* 代码嵌套快速方法: 如,想连接五个表,则只要在连接四个表的代码上加一个前后括号 (前括号加在FROM的后面,后括号加在代码的末尾即可) ,然后在后括号后面继续添加"INNER JOIN 表名X ON 表1.字段号=表X.字段号"代码即可,这样就可以无限联接数据表了: )

`join` `是 ``inner` `join``简写`

left join:是SQL语言中的查询类型,即连接查询。它的全称为左外连接 (left outer join),是外连接的一种。

连接通常可以在select语句的from子句或where子句中建立,其语法格式为:

from join_table join_type join_table

[on (join_condition)]

其中join_table指出参与连接操作的表名,连接可以对同一个表操作,也可以对多表操作,对同一个表操作的连接称为自连接, join_type 为连接类型,可以是left join 或者outer join 或者inner join 。

on (join_condition) 用来指连接条件,它由被连接表中的列和比较运算符、逻辑运算符等构成。

例1: SELECT bookinfo.bookname , authorinfo.hometown

FROM bookinfo LEFT JOIN authorinfo

ON bookinfo.authorname=authorinfo.authorname;

例2:  表A记录如下:

## aID aNum

1 a20050111

2 a20050112

3 a20050113

4 a20050114

5 a20050115

表B记录如下:

## bID bName

1 2006032401

2 2006032402

3 2006032403

4 2006032404

8 2006032408

**语句: select * from A left join B on A.aID = B.bID；**

结果如下:

aID aNum bID bName

1 a20050111 1 2006032401

2 a20050112 2 2006032402

3 a20050113 3 2006032403

4 a20050114 4 2006032404

5 a20050115 NULL NULL

 (所影响的行数为 5 行)

left join是以A表的记录为基础的,A可以看成左表,B可以看成右表,left join是以左表为准的。换句话说,左表(A)的记录将会全部表示出来,而右表(B)只会显示符合搜索条件的记录(例子中为: A.aID = B.bID)。B表记录不足的地方均为NULL。

```sql
  
SQL 几种JOIN用法实例

declare @ta table (id int,va varchar(10))

declare @tb table (id int,vb varchar(10))


insert into @ta select 1,'aa'

insert into @ta select 2,'bc'

insert into @ta select 3,'ccc'


insert into @tb select 1,'2'

insert into @tb select 3,'58'

insert into @tb select 4,'67'


-内连接简单写法


select a.id,a.va,b.id,b.vb from @ta a,@tb b

where a.id=b.id


-内连接


select a.id,a.va,b.id,b.vb from @ta a inner join @tb b

on a.id=b.id


select a.id,a.va,b.id,b.vb from @ta a join @tb b

on a.id=b.id


-左连接 (左外连接) 

-返回left join 子句中指定的左表的所有行,以及右表所匹配的行。


select a.id,a.va,b.id,b.vb from @ta a left join @tb b

on a.id=b.id


select a.id,a.va,b.id,b.vb from @ta a left outer join @tb b

on a.id=b.id


-右连接 (右外连接) 

-返回right join 子句中指定的右表的所有行,以及左表所匹配的行。


select a.id,a.va,b.id,b.vb from @ta a right join @tb b

on a.id=b.id


select a.id,a.va,b.id,b.vb from @ta a right outer join @tb b

on a.id=b.id


-完整外连接

-等同左连接+右连接


select a.id,a.va,b.id,b.vb from @ta a full join @tb b

on a.id=b.id


select a.id,a.va,b.id,b.vb from @ta a full outer join @tb b

on a.id=b.id

交叉连接

-没有两个表之间关系的交叉连接,将产生连接所涉及的表的笛卡尔积。


select a.id,a.va,b.id,b.vb from @ta a cross join @tb b


select a.id,a.va,b.id,b.vb from @ta a,@tb b


-自连接

-一个表和其本身连接。


select a.id,a.va,b.id,b.va from @ta a,@ta b where a.id=b.id+1
  
  
```

[http://baike.baidu.com/view/4828677.htm](http://baike.baidu.com/view/4828677.htm)

[http://www.lao8.org/html/8/2008-7-28/INNERJOIN/](http://www.lao8.org/html/8/2008-7-28/INNERJOIN/)
