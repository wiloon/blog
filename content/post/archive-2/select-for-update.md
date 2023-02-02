---
title: Select For update
author: "-"
date: 2016-10-14T10:21:55+00:00
url: select/for/update
  - Inbox
tags:
  - reprint
  - remix
---
## Select For update

<http://blog.itpub.net/17203031/viewspace-694383/>
  
Select … for update 语句是我们经常使用手工加锁语句。通常情况下, select 语句是不会对数据加锁, 妨碍影响其他的 DML 和 DDL 操作。同时, 在多版本一致读机制的支持下, select 语句也不会被其他类型语句所阻碍。

借助 for update 子句, 我们可以在应用程序的层面手工实现数据加锁保护操作。本篇我们就来介绍一下这个子句的用法和功能。

下面是采自 Oracle 官方文档《SQL Language Reference》中关于for update子句的说明: (请双击点开图片查看)

从for update子句的语法状态图中,我们可以看出该子句分为两个部分: 加锁范围子句和加锁行为子句。下面我们分别针对两个方面的进行介绍。

加锁范围子句

在select…for update之后,可以使用of子句选择对select的特定数据表进行加锁操作。默认情况下,不使用of子句表示在select所有的数据表中加锁。

//采用默认格式for update

SQL> select * from emp where rownum<2 for update;

EMPNO ENAME      JOB         MGR HIREDATE          SAL      COMM DEPTNO

* * *

7369 SMITH      CLERK      7902 1980-12-17     800.00               20

此时,我们观察v$lock和v$locked_object视图,可以看到锁信息。

//事务信息视图

SQL> select addr,xidusn,xidslot,xidsqn from v$transaction;

ADDR         XIDUSN    XIDSLOT     XIDSQN

* * *

377DB5D0          7         19        808

//锁对象信息

SQL> select xidusn,xidslot,xidsqn,object_id,session_id, oracle_username from v$locked_object;

XIDUSN    XIDSLOT     XIDSQN  OBJECT_ID SESSION_ID ORACLE_USERNAME

* * *

7         19        808      73181         36 SCOTT

//

SQL> select owner,object_name from dba_objects where object_id=73181;

OWNER                          OBJECT_NAME

* * *

SCOTT                          EMP

//

SQL> select addr, sid, type, id1,id2,lmode, request, block from v$lock where sid=36;

ADDR      SID TYPE        ID1        ID2      LMODE    REQUEST  BLOCK

* * *

37E808F0    36 AE          100          0          4          0    0

B7DE8A44   36 TM        73181          0          3          0   0

377DB5D0   36 TX       458771        808          6          0    0

从上面的情况看,默认情况下的for update语句,效果相当于启动了一个会话级别的事务,在对应的数据表 (select所涉及的所有数据表) 上加入一个数据表级共享锁 (TM,lmode=3) 。同时,在对应的数据行中加入独占锁 (TX,lmode=6) 。

根据我们以前的知识,如果此时有另一个会话视图获取对应数据行的独占权限 (无论是用update/delete还是另一个for update) ,都会以block而告终。

SQL> select sid from v$mystat where rownum<2;

SID

* * *

37

SQL> select * from emp where empno=7369 for update;

//系统blocking

此时系统中状态,切换到另一个用户下进行观察:

SQL> select addr, sid, type, id1,id2,lmode, request, block from v$lock where sid in (36,37);

ADDR   SID TYPE        ID1        ID2      LMODE    REQUEST      BLOCK

* * *

37E808F0         36 AE          100          0          4          0   0

37E80ED4         37 AE          100          0          4          0   0

37E80F48         37 TX       458771        808          0          6   0

B7DE8A44         37 TM        73181          0          3          0  0

B7DE8A44         36 TM        73181          0          3          0  0

377DB5D0         36 TX       458771        808          6          0  1

6 rows selected

SQL> select * from dba_waiters;

WAITING_SESSION HOLDING_SESSION LOCK_TYPE                  MODE_HELD                                MODE_REQUESTED                             LOCK_ID1   LOCK_ID2

* * *

37              36 Transaction                Exclusive                                Exclusive                                    458771        808

由此,我们可以获取到结论: for update子句的默认行为就是自动启动一个事务,借助事务的锁机制将数据进行锁定。

Of子句是配合for update语句使用的一个范围说明标记。从官方的语法结构看,后面可以跟一个或者多个数据列列表。这种语法场景常常使用在进行连接查询的select中,对其中一张数据表数据进行锁定。

SQL> select empno,ename,job,mgr,sal from emp,dept where emp.deptno=dept.deptno and empno=7369 for update of emp.empno;

EMPNO ENAME      JOB         MGR       SAL

* * *

7369 SMITH      CLERK      7902    800.00

SQL>  select addr, sid, type, id1,id2,lmode, request, block from v$lock where sid=36;

ADDR       SID TYPE        ID1        ID2      LMODE    REQUEST BLOCK

* * *

37E808F0         36 AE          100          0          4          0    0

B7E1C2E8         36 TM        73181          0          3         0    0

377DBC0C         36 TX        65566        747          6       0   0

上面的语句中,我们看到使用for update of指定数据列之后,锁定的范围限制在了所在的数据表。也就是说,当我们使用连接查询配合of子句的时候,可以实现有针对性的锁定。

同样在连接查询的时候,如果没有of子句,同样采用默认的模式,会如何呢？

SQL> select empno,ename,job,mgr,sal from emp,dept where emp.deptno=dept.deptno and empno=7369 for update;

EMPNO ENAME      JOB         MGR       SAL

* * *

7369 SMITH      CLERK      7902    800.00

SQL>  select addr, sid, type, id1,id2,lmode, request, block from v$lock where sid=36;

ADDR     SID TYPE        ID1        ID2      LMODE    REQUEST  BLOCK

* * *

37E808F0         36 AE          100          0          4          0     0

B7E1C2E8         36 TM        73179          0          3          0   0

B7E1C2E8         36 TM        73181          0          3          0     0

377DBC0C         36 TX       458777        805          6          0    0

SQL> select owner,object_name from dba_objects where object_id=73179;

OWNER                          OBJECT_NAME

* * *

SCOTT                          DEPT

明显可以看到,当我们没有使用of子句的时候,默认就是对所有select的数据表进行lock操作。

加锁行为子句

加锁行为子句相对比较容易理解。这里分别介绍。

Nowait子句

当我们进行for update的操作时,与普通select存在很大不同。一般select是不需要考虑数据是否被锁定,最多根据多版本一致读的特性读取之前的版本。加入for update之后,Oracle就要求启动一个新事务,尝试对数据进行加锁。如果当前已经被加锁,默认的行为必然是block等待。

使用nowait子句的作用就是避免进行等待,当发现请求加锁资源被锁定未释放的时候,直接报错返回。

///session1中

SQL> select * from emp for update;

EMPNO ENAME      JOB         MGR HIREDATE          SAL      COMM DEPTNO

* * *

7369 SMITH      CLERK      7902 1980-12-17     800.00               20

7499 ALLEN      SALESMAN   7698 1981-2-20     1600.00    300.00     30

7521 WARD       SALESMAN   7698 1981-2-22     1250.00    500.00     30

7566 JONES      MANAGER    7839 1981-4-2      2975.00               20

//变换session,进行执行。

SQL> select * from emp for update nowait;

select * from emp for update nowait

ORA-00054: 资源正忙, 但指定以 NOWAIT 方式获取资源, 或者超时失效

对应的还有就是wait子句,也就是默认的for update行为。一旦发现对应资源被锁定,就等待blocking,直到资源被释放或者用户强制终止命令。

对wait子句还存在一个数据参数位,表示当出现blocking等待的时候最多等待多长时间。单位是秒级别。

//接上面的案例

SQL> select * from emp for update wait 3;

select * from emp for update wait 3

ORA-30006: 资源已被占用; 执行操作时出现 WAIT 超时

Skip locked参数

Skip locked参数是最新引入到for update语句中的一个参数。简单的说,就是在对数据行进行加锁操作时,如果发现数据行被锁定,就跳过处理。这样for update就只针对未加锁的数据行进行处理加锁。

//session1中,对一部分数据加锁；

SQL> select * from emp where rownum<4 for update;

EMPNO ENAME      JOB         MGR HIREDATE          SAL      COMM DEPTNO

* * *

7369 SMITH      CLERK      7902 1980-12-17     800.00               20

7499 ALLEN      SALESMAN   7698 1981-2-20     1600.00    300.00     30

7521 WARD       SALESMAN   7698 1981-2-22     1250.00    500.00     30

//在session2中；

SQL> select * from emp for update skip locked;

EMPNO ENAME      JOB         MGR HIREDATE          SAL      COMM DEPTNO

* * *

 (篇幅原因,省略)

7934 MILLER     CLERK      7782 1982-1-23     1300.00               10

11 rows selected

总数据一共14行。Session1中,先lock住了3行数据。之后的seesion2中,由于使用的skip locked子句参数,将剩下的11条数据进行读取到并且加锁。

对for update的使用

在日常中,我们对for update的使用还是比较普遍的,特别是在如pl/sql developer中手工修改数据。此时只是觉得方便,而对for update真正的含义缺乏理解。

For update是Oracle提供的手工提高锁级别和范围的特例语句。Oracle的锁机制是目前各类型数据库锁机制中比较优秀的。所以,Oracle认为一般不需要用户和应用直接进行锁的控制和提升。甚至认为死锁这类锁相关问题的出现场景,大都与手工提升锁有关。所以,Oracle并不推荐使用for update作为日常开发使用。而且,在平时开发和运维中,使用了for update却忘记提交,会引起很多锁表故障。

那么,什么时候需要使用for update？就是那些需要业务层面数据独占时,可以考虑使用for update。场景上,比如火车票订票,在屏幕上显示邮票,而真正进行出票时,需要重新确定一下这个数据没有被其他客户端修改。所以,在这个确认过程中,可以使用for update。这是统一的解决方案方案问题,需要前期有所准备。
