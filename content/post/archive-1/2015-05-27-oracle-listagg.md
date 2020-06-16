---
title: oracle listagg
author: wiloon
type: post
date: 2015-05-27T05:42:18+00:00
url: /?p=7717
categories:
  - Uncategorized

---
[sql]

SELECT deptno,
  
LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP(ORDER BY hiredate) AS employees
  
FROM test
  
GROUP BY deptno;

[/sql]



http://xpchild.blog.163.com/blog/static/10180985920108485721969/

本文描述了在oracle 11g release 2 版本中新增的listagg函数，listagg是一个实现字符串聚合的oracle内建函数。作为一种普遍的技术，网络上也有多种实现字符串聚合的方法。本文会首先介绍listagg函数，最后会拿这些方法与listagg进行性能方面的对比。

样例数据





本文的例子将使用如下的样例数据：

DEPTNO ENAME      HIREDATE
  
&#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;-
  
10 CLARK       09/06/1981
  
10 KING        17/11/1981
  
10 MILLER      23/01/1982
  
20 ADAMS       12/01/1983
  
20 FORD        03/12/1981
  
20 JONES       02/04/1981
  
20 SCOTT       09/12/1982
  
20 SMITH       17/12/1980
  
30 ALLEN       20/02/1981
  
30 BLAKE       01/05/1981
  
30 JAMES       03/12/1981
  
30 MARTIN      28/09/1981
  
30 TURNER      08/09/1981
  
30 WARD        22/02/1981

字符串聚合





字符串聚合就是按照分组把多行数据串联成一行，以下面的结果集为例：

DEPTNO ENAME
  
&#8212;&#8212;&#8212; &#8212;&#8212;&#8212;-
  
10 CLARK
  
10 KING
  
10 MILLER
  
20 ADAMS
  
20 FORD
  
20 JONES

按照DEPTNO字段分组，对结果集进行字符串聚合，结果如下：

DEPTNO AGGREGATED_ENAMES
  
&#8212;&#8212;&#8212; &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-
  
10 CLARK,KING,MILLER
  
20 ADAMS,FORD,JONES

可以看到，employee names基于deptno分组实现了串联，如前所述，有很多种方法实现聚合功能（文章最后提供相关链接），但是listagg更为简单，易用。

listagg 语法概述

listagg函数的语法结构如下：
  
LISTAGG( [,]) WITHIN GROUP (ORDER BY ) [OVER (PARTITION BY )]

listagg虽然是聚合函数，但可以提供分析功能（比如可选的OVER()子句）。使用listagg中，下列中的元素是必须的：

需要聚合的列或者表达式
  
WITH GROUP 关键词
  
分组中的ORDER BY子句
  
下面将演示listagg函数使用的例子

listagg 作为聚合函数
  
下面以EMP表为例，按照部门分组聚合employee name，并以，为分隔符。

SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP (ORDER BY ename) AS employees 3 FROM emp 4 GROUP BY 5 deptno;
  
DEPTNO EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 10 CLARK,KING,MILLER 20 ADAMS,FORD,JONES,SCOTT,SMITH 30 ALLEN,BLAKE,JAMES,MARTIN,TURNER,WARD 3 rows selected.
  
注：在每个聚合元素中，本例选用empolyee name字段进行排序，不过需要说明的是，在其它实现字符串聚合方法中，排序可是重量级的任务。

下面的例子中，empolyee name的聚合将按照hire date来排序。

SQL> SELECT deptno
  
2  ,      LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP (ORDER BY hiredate) AS employees
  
3  FROM   emp
  
4  GROUP  BY
  
5         deptno;

DEPTNO EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 10 CLARK,KING,MILLER 20 SMITH,JONES,FORD,SCOTT,ADAMS 30 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 3 rows selected.
  
可以看到，每组中empolyee names的排序与前面的例子截然不同。
  
listagg作为分析函数

与许多的聚合函数类似，listagg通过加上over（）子句可以实现分析功能，下面的例子将展示分析功能：SQL> SELECT deptno 2 , ename 3 , hiredate 4 , LISTAGG(ename, &#8216;,&#8217;) 5 WITHIN GROUP (ORDER BY hiredate) 6 OVER (PARTITION BY deptno) AS employees 7 FROM emp;
  
DEPTNO ENAME HIREDATE EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 10 CLARK 09/06/1981 CLARK,KING,MILLER 10 KING 17/11/1981 CLARK,KING,MILLER 10 MILLER 23/01/1982 CLARK,KING,MILLER 20 SMITH 17/12/1980 SMITH,JONES,FORD,SCOTT,ADAMS 20 JONES 02/04/1981 SMITH,JONES,FORD,SCOTT,ADAMS 20 FORD 03/12/1981 SMITH,JONES,FORD,SCOTT,ADAMS 20 SCOTT 19/04/1987 SMITH,JONES,FORD,SCOTT,ADAMS 20 ADAMS 23/05/1987 SMITH,JONES,FORD,SCOTT,ADAMS 30 ALLEN 20/02/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 30 WARD 22/02/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 30 BLAKE 01/05/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 30 TURNER 08/09/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 30 MARTIN 28/09/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 30 JAMES 03/12/1981 ALLEN,WARD,BLAKE,TURNER,MARTIN,JAMES 14 rows selected. 切记：分析函数不会丢失结果集的每一行，而字符串的聚合却并非如此。
  
排序

如前所述，ORDER BY 子句是必选项，如下例所示：

SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP () AS employees 3 FROM emp 4 GROUP BY 5 deptno;
  
, LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP () AS employees * ERROR at line 2: ORA-30491: missing ORDER BY clause
  
如果所要聚合字段的排序无关紧要，那么可以可以使用NULL代替：

SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;,&#8217;) WITHIN GROUP (ORDER BY NULL) AS employees 3 FROM emp 4 GROUP BY 5 deptno;
  
DEPTNO EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 10 CLARK,KING,MILLER 20 ADAMS,FORD,JONES,SCOTT,SMITH 30 ALLEN,BLAKE,JAMES,MARTIN,TURNER,WARD 3 rows selected.
  
在这个例子当中，虽然使用的是NULL来进行排序，但结果集中聚合的元素还是按字母的顺序排序的，这是因为listagg的默认排序行为。

分隔符


  
在字符串的聚合中，可以使用静态变量或者表达式作为分隔符，事实上，分隔符是可选项，例如：

SQL> SELECT deptno 2 , LISTAGG(ename) WITHIN GROUP (ORDER BY ename) AS employees 3 FROM emp 4 GROUP BY 5 deptno;
  
DEPTNO EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 10 CLARKKINGMILLER 20 ADAMSFORDJONESSCOTTSMITH 30 ALLENBLAKEJAMESMARTINTURNERWARD 3 rows selected.
  
唯一的限制是，分隔符要么是静态变量（如字母），要么是建立在分组字段上的确定性表达式，比如，不能使用ROWNUM作为分隔符，如下所示：

SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;(&#8216; || ROWNUM || &#8216;)&#8217;) 3 WITHIN GROUP (ORDER BY hiredate) AS employees 4 FROM emp 5 GROUP BY 6 deptno;
  
, LISTAGG(ename, &#8216;(&#8216; || ROWNUM || &#8216;)&#8217;) * ERROR at line 2: ORA-30497: Argument should be a constant or a function of expressions in GROUP BY.
  
错误信息非常清楚：ROWNUM既不是静态变量，也不是建立在分组字段上的表达式，如果使用了分组字段，那就限制了表达式的类型，例如：
  
SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;(&#8216; || MAX(deptno) || &#8216;)&#8217;) 3 WITHIN GROUP (ORDER BY hiredate) AS employees 4 FROM emp 5 GROUP BY 6 deptno;
  
, LISTAGG(ename, &#8216;(&#8216; || MAX(deptno) || &#8216;)&#8217;) * ERROR at line 2: ORA-30496: Argument should be a constant.
  
这个例子当中，oracle分析到分隔符试图使用分组字段，但是是一个非法的表达式，下面的例子中，使用了oracle接受的确定性表达式：
  
SQL> SELECT deptno 2 , LISTAGG(ename, &#8216;(&#8216; || CHR(deptno+55) || &#8216;); &#8216;) 3 WITHIN GROUP (ORDER BY hiredate) AS employees 4 FROM emp 5 GROUP BY 6 deptno;
  
DEPTNO EMPLOYEES &#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 10 CLARK(A); KING(A); MILLER 20 SMITH(K); JONES(K); FORD(K); SCOTT(K); ADAMS 30 ALLEN(U); WARD(U); BLAKE(U); TURNER(U); MARTIN(U); JAMES 3 rows selected.
  
这里把DETPNO转化成ASCII字符作为分隔符，这个一个在分组列上的确定性表达式。
  
其它限制

listagg聚合的结果列大小限制在varchar2类型的最大值内（比如4000），例如：
  
SQL> SELECT LISTAGG(object\_name) WITHIN GROUP (ORDER BY NULL) 2 FROM all\_objects;
  
FROM all_objects * ERROR at line 2: ORA-01489: result of string concatenation is too long
  
这里没有clob或者更大的varchar2类型类代替，所以更大的字符串必须使用替代方案（比如COLLECTION或者用户自定义的PL/SQL函数）
  
性能方面





下面将比较几种常用的字符串聚合方法的性能，类比的有：

LISTAGG (11g Release 2);
  
COLLECT + PL/SQL function(10g);
  
Oracle Data Cartridge - user-defined aggregate function (9i)
  
MODEL SQL (10g).
  
这里最主要的不同是listagg是一个内建函数，所以其至少与其它方案有可比性。

建立环境
  
为了性能比较，下面将建立一张有2000个分组，100万行数据的表，具体如下：

SQL> CREATE TABLE t 2 AS 3 SELECT ROWNUM AS id 4 , MOD(ROWNUM,2000) AS grp 5 , DBMS\_RANDOM.STRING(&#8216;u&#8217;,5) AS val 6 , DBMS\_RANDOM.STRING(&#8216;u&#8217;,30) AS pad 7 FROM dual 8 CONNECT BY ROWNUM <= 1000000;
  
Table created.
  
SQL> SELECT COUNT(*) FROM t;
  
COUNT(*) &#8212;&#8212;&#8212;- 1000000 1 row selected.
  
SQL> exec DBMS\_STATS.GATHER\_TABLE_STATS(USER, &#8216;T&#8217;);
  
PL/SQL procedure successfully completed.
  
这里将使用wall-clock和autotrace进行性能方面的类比。注：样例的数据已被缓存，准备环境如下：

SQL> set autotrace traceonly statistics SQL> set timing on SQL> set arrays 500
  
listagg
  
第一个测试的是listagg，下面将对2000个分组进行聚合，并按照value排序：



SQL> SELECT grp 2 , LISTAGG(val, &#8216;,&#8217;) WITHIN GROUP (ORDER BY val) AS vals 3 FROM t 4 GROUP BY 5 grp;
  
2000 rows selected. Elapsed: 00:00:05.85 Statistics &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 1 recursive calls 0 db block gets 7092 consistent gets 0 physical reads 0 redo size 6039067 bytes sent via SQL\*Net to client 552 bytes received via SQL\*Net from client 5 SQL*Net roundtrips to/from client 1 sorts (memory) 0 sorts (disk) 2000 rows processed
  
测试机上，这条语句执行了不到6秒，没有磁盘物理I/O，所有的sorting都在内存当中。
  
stragg/wm_concat

下面将使用广为流传的字符串聚合，Tom Kyte的定义的聚合函数STRAGG。在 oracle的10g版本中，oracle在WMSYS的用户下实现了类似功能的函数，这里直接使用这个函数来测试。注：STRAGG函数不支持字符串的排序。

SQL> SELECT grp 2 , WMSYS.WM\_CONCAT(val) AS vals &#8211;<- WM\_CONCAT ~= STRAGG 3 FROM t 4 GROUP BY 5 grp;
  
2000 rows selected. Elapsed: 00:00:19.45 Statistics &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 1 recursive calls 0 db block gets 7206 consistent gets 0 physical reads 0 redo size 6039067 bytes sent via SQL\*Net to client 552 bytes received via SQL\*Net from client 5 SQL*Net roundtrips to/from client 1 sorts (memory) 0 sorts (disk) 2000 rows processed
  
这个方法花费了三倍于listagg的时间（没有排序），用户自定义的函数会比这个PL/SQL函数效率更低（比如：上下文切换）

collect（without ordering）
  
当10g发布的时候，我就立即使用collect函数和一个“collection-to-string”PL/SQL函数来替代STRAGG。不过10g版本中的collect没有排序功能。注；To_STRING的源码可以在相关文档中查到。

SQL> SELECT grp 2 , TO\_STRING( 3 CAST(COLLECT(val) AS varchar2\_ntt) 4 ) AS vals 5 FROM t 6 GROUP BY 7 grp;
  
2000 rows selected. Elapsed: 00:00:02.90 Statistics &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 10 recursive calls 0 db block gets 7197 consistent gets 0 physical reads 0 redo size 6039067 bytes sent via SQL\*Net to client 552 bytes received via SQL\*Net from client 5 SQL*Net roundtrips to/from client 1 sorts (memory) 0 sorts (disk) 2000 rows processed
  
没有排序的情况下，collect/TO_STRING方法比listagg快了两倍，但是listagg花费了大量的时间在排序上，如果说排序时无关紧要的，那么可以说collect技术是最快的。
  
collect (with ordering)

公平起见，在collect中引入排序（11g中的一个新特性），如下；SQL> SELECT grp 2 , TO\_STRING( 3 CAST(COLLECT(val ORDER BY val) AS varchar2\_ntt) 4 ) AS vals 5 FROM t 6 GROUP BY 7 grp;
  
2000 rows selected. Elapsed: 00:00:07.08 Statistics &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 10 recursive calls 0 db block gets 7197 consistent gets 0 physical reads 0 redo size 6039067 bytes sent via SQL\*Net to client 552 bytes received via SQL\*Net from client 5 SQL*Net roundtrips to/from client 1 sorts (memory) 0 sorts (disk) 2000 rows processed 这次，引入了排序后，collect方法确实比listagg慢多了。
  
model

最后一个性能比较是与使用了model子句的实现方法。下面的例子的源代码来自于Rob van Wijk&#8217;s About Oracle blog 并做了些修改以适应样例数据。

SQL> SELECT grp 2 , vals 3 FROM ( 4 SELECT grp 5 , RTRIM(vals, &#8216;,&#8217;) AS vals 6 , rn 7 FROM t 8 MODEL 9 PARTITION BY (grp) 10 DIMENSION BY (ROW_NUMBER() OVER (PARTITION BY grp ORDER BY val) AS rn) 11 MEASURES (CAST(val AS VARCHAR2(4000)) AS vals) 12 RULES 13 ( vals[ANY] ORDER BY rn DESC = vals[CV()] || &#8216;,&#8217; || vals[CV()+1] 14 ) 15 ) 16 WHERE rn = 1 17 ORDER BY 18 grp;
  
2000 rows selected. Elapsed: 00:03:28.15 Statistics &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;- 3991 recursive calls 0 db block gets 7092 consistent gets 494791 physical reads 0 redo size 6039067 bytes sent via SQL\*Net to client 553 bytes received via SQL\*Net from client 5 SQL*Net roundtrips to/from client 130 sorts (memory) 0 sorts (disk) 2000 rows processed
  
这个例子执行了三分钟，统计信息显示发生了大量的I/O读，递归调用和内存排序，事实上，这个糟糕的表现主要是由于在查询中，大量的对临时表空间的读和写（尽管统计信息并未显示磁盘排序）。

MODEL字符串聚合方法的执行计划如下：

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211; | Id | Operation | Name | Rows | Bytes |TempSpc| &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211; | 0 | SELECT STATEMENT | | | | | | 1 | SORT ORDER BY | | 1000K| 1934M| 1953M| |* 2 | VIEW | | 1000K| 1934M| | | 3 | SQL MODEL ORDERED | | 1000K| 9765K| | | 4 | WINDOW SORT | | 1000K| 9765K| 19M| | 5 | TABLE ACCESS FULL| T | 1000K| 9765K| | &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8211; Predicate Information (identified by operation id): &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212; 2 &#8211; filter("RN"=1) 通过SQL的监控报告（使用DBMS\_SQLTUNE.REPORT\_SQL_MONITOR）在SQL MODEL操作的第三步中，数据的排序使用4Gb的临时空间，在Gary Myers&#8217; Sydney Oracle Lab blog中也阐述了这个现象。
  
性能总结

从以上事例中可以看出，listagg函数是字符串聚合方法中效率最高的一个，并且还是一个内建的函数。如果不需要排序的情况下，collect会更快一些，但如果是需要排序的话，listagg绝对是最快的。
  
深度阅读

更多关于listagg的信息，详见online sql reference。
  
源代码

本文中的源码可以在here获得.