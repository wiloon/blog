---
title: Oracle with as
author: w1100n
type: post
date: 2013-11-20T10:38:07+00:00
url: /?p=5985
categories:
  - Uncategorized

---
原文传送门: <http://blog.csdn.net/wh62592855/archive/2009/11/06/4776631.aspx>

记得以前在论坛里看到inthirties用到过WITH AS这个字眼，当时没特别在意。今天在一个帖子里又看到有人用这个，所以就去网上搜了搜相关内容，自己小试了一把，写下来，方便以后忘了的话学习。

===================================================================================

先举个例子吧: 

有两张表，分别为A、B，求得一个字段的值先在表A中寻找，如果A表中存在数据，则输出A表的值；如果A表中不存在，则在B表中寻找，若B表中有相应记录，则输出B表的值；如果B表中也不存在，则输出"no records"字符串。
  
    
http://blog.csdn.net/a9529lty/article/details/4923957#
      
      
      
  
  
  <ol start="1">
    <li>
      with
    </li>
    <li>
      sql1 as (select to_char(a) s_name from test_tempa),
    </li>
    <li>
      sql2 as (select to_char(b) s_name from test_tempb where not exists (select s_name from sql1 where rownum=1))
    </li>
    <li>
      select * from sql1
    </li>
    <li>
      union all
    </li>
    <li>
      select * from sql2
    </li>
    <li>
      union all
    </li>
    <li>
      select 'no records' from dual
    </li>
    <li>
             where not exists (select s_name from sql1 where rownum=1)
    </li>
    <li>
             and not exists (select s_name from sql2 where rownum=1);
    </li>
  </ol>

再举个简单的例子

with a as (select * from test)

select * from a;

其实就是把一大堆重复用到的SQL语句放在with as 里面，取一个别名，后面的查询就可以用它

这样对于大批量的SQL语句起到一个优化的作用，而且清楚明了

下面是搜索到的英文文档资料

About Oracle WITH clause
  
Starting in Oracle9i release 2 we see an incorporation of the SQL-99 "WITH clause", a tool for materializing subqueries to save Oracle from having to re-compute them multiple times.

The SQL "WITH clause" is very similar to the use of Global temporary tables (GTT), a technique that is often used to improve query speed for complex subqueries. Here are some important notes about the Oracle "WITH clause":

• The SQL "WITH clause" only works on Oracle 9i release 2 and beyond.
  
• Formally, the "WITH clause" is called subquery factoring
  
• The SQL "WITH clause" is used when a subquery is executed multiple times
  
• Also useful for recursive queries (SQL-99, but not Oracle SQL)

To keep it simple, the following example only references the aggregations once, where the SQL "WITH clause" is normally used when an aggregation is referenced multiple times in a query.
  
We can also use the SQL-99 "WITH clause" instead of temporary tables. The Oracle SQL "WITH clause" will compute the aggregation once, give it a name, and allow us to reference it (maybe multiple times), later in the query.

The SQL-99 "WITH clause" is very confusing at first because the SQL statement does not begin with the word SELECT. Instead, we use the "WITH clause" to start our SQL query, defining the aggregations, which can then be named in the main query as if they were "real" tables:

WITH
  
subquery_name
  
AS
  
(the aggregation SQL statement)
  
SELECT
  
(query naming subquery_name);

Retuning to our oversimplified example, let's replace the temporary tables with the SQL "WITH  clause":

WITH
  
sum_sales AS
  
select /*+ materialize */
  
sum(quantity) all_sales from stores
  
number_stores AS
  
select /*+ materialize */
  
count(*) nbr_stores from stores
  
sales_by_store AS
  
select /*+ materialize */
  
store_name, sum(quantity) store_sales from
  
store natural join sales
  
SELECT
  
store_name
  
FROM
  
store,
  
sum_sales,
  
number_stores,
  
sales_by_store
  
where
  
store_sales > (all_sales / nbr_stores)
  
;

Note the use of the Oracle undocumented "materialize" hint in the "WITH clause". The Oracle materialize hint is used to ensure that the Oracle cost-based optimizer materializes the temporary tables that are created inside the "WITH" clause. This is not necessary in Oracle10g, but it helps ensure that the tables are only created one time.

It should be noted that the "WITH clause" does not yet fully-functional within Oracle SQL and it does not yet support the use of "WITH clause" replacement for "CONNECT BY" when performing recursive queries.

To see how the "WITH clause" is used in ANSI SQL-99 syntax, here is an excerpt from Jonathan Gennick's great work "Understanding the WITH Clause" showing the use of the SQL-99 "WITH clause" to traverse a recursive bill-of-materials hierarchy
  
The SQL-99 "WITH clause" is very confusing at first because the SQL statement does not begin with the word SELECT. Instead, we use the "WITH clause" to start our SQL query, defining the aggregations, which can then be named in the main query as if they were "real" tables:

WITH
  
subquery_name
  
AS
  
(the aggregation SQL statement)
  
SELECT
  
(query naming subquery_name);
  
Retuning to our oversimplified example, let's replace the temporary tables with the SQL "WITH" clause":

=================================================================================

下面自己小试一把，当然，一点都不复杂，很简单很简单的例子，呵呵。
  
    
http://blog.csdn.net/a9529lty/article/details/4923957#
      
      
      
  
  
  <ol start="1">
    <li>
      SQL> create table t2(id int);
    </li>
    <li>
    </li>
    <li>
      Table created.
    </li>
    <li>
    </li>
    <li>
      SQL> create table t3(id int);
    </li>
    <li>
    </li>
    <li>
      Table created.
    </li>
    <li>
    </li>
    <li>
      SQL> insert into t2 values(1);
    </li>
    <li>
    </li>
    <li>
      1 row created.
    </li>
    <li>
    </li>
    <li>
      SQL> insert into t2 values(2);
    </li>
    <li>
    </li>
    <li>
      1 row created.
    </li>
    <li>
    </li>
    <li>
      SQL> insert into t3 values(3);
    </li>
    <li>
    </li>
    <li>
      1 row created.
    </li>
    <li>
    </li>
    <li>
      SQL> commit;
    </li>
    <li>
    </li>
    <li>
      Commit complete.
    </li>
    <li>
    </li>
    <li>
      SQL> select * from t2;
    </li>
    <li>
    </li>
    <li>
              ID
    </li>
    <li>
      ----
    </li>
    <li>
               1
    </li>
    <li>
               2
    </li>
    <li>
    </li>
    <li>
      SQL> select * from t3;
    </li>
    <li>
    </li>
    <li>
              ID
    </li>
    <li>
      ----
    </li>
    <li>
               3
    </li>
    <li>
      SQL> with
    </li>
    <li>
        2  sql1 as (select * from t2),
    </li>
    <li>
        3  sql2 as (select * from t3)
    </li>
    <li>
        4  select * from t2
    </li>
    <li>
        5  union
    </li>
    <li>
        6  select * from t3;
    </li>
    <li>
      sql2 as (select * from t3)
    </li>
    <li>
                             *
    </li>
    <li>
      ERROR at line 3:
    </li>
    <li>
      ORA-32035: unreferenced query name defined in WITH clause
    </li>
    <li>
    </li>
    <li>
      -从这里可以看到，你定义了sql1和sql2，就得用它们哦，不然会报错的。
    </li>
    <li>
    </li>
    <li>
      SQL> with
    </li>
    <li>
        2  sql1 as (select * from t2),
    </li>
    <li>
        3  sql2 as (select * from t3)
    </li>
    <li>
        4  select * from sql1
    </li>
    <li>
        5  union
    </li>
    <li>
        6  select * from sql2;
    </li>
    <li>
    </li>
    <li>
              ID
    </li>
    <li>
      ----
    </li>
    <li>
               1
    </li>
    <li>
               2
    </li>
    <li>
               3
    </li>
    <li>
    </li>
    <li>
      -下面加个WHERE条件试试
    </li>
    <li>
    </li>
    <li>
      SQL> with
    </li>
    <li>
        2  sql1 as (select * from t2),
    </li>
    <li>
        3  sql2 as (select * from t3)
    </li>
    <li>
        4  select * from sql1
    </li>
    <li>
        5  union
    </li>
    <li>
        6  select * from sql2
    </li>
    <li>
        7  where id in(2,3);
    </li>
    <li>
    </li>
    <li>
              ID
    </li>
    <li>
      ----
    </li>
    <li>
               1
    </li>
    <li>
               2
    </li>
    <li>
               3
    </li>
    <li>
    </li>
    <li>
      -奇怪？为什么加了WHERE条件还是输出ID=1的记录了，继续往下看: 
    </li>
    <li>
    </li>
    <li>
      SQL> with
    </li>
    <li>
        2  sql1 as (select * from t2),
    </li>
    <li>
        3  sql2 as (select * from t3)
    </li>
    <li>
        4  select * from sql1
    </li>
    <li>
        5  where id=3
    </li>
    <li>
        6  union
    </li>
    <li>
        7  select * from sql2
    </li>
    <li>
        8  where id=3;
    </li>
    <li>
    </li>
    <li>
              ID
    </li>
    <li>
      ----
    </li>
    <li>
               3
    </li>
    <li>
    </li>
    <li>
      -可以看到，每个条件是要针对每个SELECT语句的。
    </li>
  </ol>

好了就先记这些吧，以后看到了新的用法再补充。