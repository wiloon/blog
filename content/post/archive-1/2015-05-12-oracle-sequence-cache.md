---
title: Oracle Sequence cache
author: "-"
type: post
date: 2015-05-12T06:49:08+00:00
url: /?p=7658
categories:
  - Uncategorized

---
http://blog.itpub.net/17203031/viewspace-717042/


在Oracle中，我们没有MySQL和SQL Server可以使用的自增数据类型。大部分场景下，如果我们需要生成业务无关的（Business-Independent）主键列，序列Sequence对象是我们最方便的选择。


定义Sequence是很简单的，如果最大程度利用默认值的话，我们只需要定义sequence对象的名字即可。在序列Sequence对象的定义中，Cache是一个可选择的参数。默认的Sequence对象是有cache选项的，默认取值为20。


那么，这个Cache参数对Sequence的使用带来什么好处？如果不设置，会有什么问题。本篇我们就一起来探讨这个问题。


1、Sequence Cache简析


简单的说，Cache就是Oracle每次向Sequence进行请求时，分配出的独立数字数量。例如，当我们使用<seq_name>.nextval获取一个独立值时，Oracle需要将sequence对象的数据字典信息更新。如果我们设置cache为10，那么第一次请求nextval的时候，就更新数据字典信息增加10，取出的10个号放在Oracle服务器的缓存中。


在以后每次请求nextval的时候，Oracle就从服务器缓存中去获取序列值。而不需要更新数据字典信息。只有在分配到缓存的10个数字都已经分配完，或者因为缓存刷新操作剩余数字被清理的情况下，才会再次调用sequence分配机制，再次分出cache个数字。


在cache问题上，我们经常会疑惑为什么我们sequence生成的数字序列会"跳号"。这种跳号现象实际上就是因为cache的数字在缓存中因为各种原因被flush出，这样才导致生成的数字序列不连续。


注意: 在有cache的情况下，sequence只能保证每次获取到的数字都是唯一、递增的，从来没有保证过数字的连续性。


如果我们不设置cache，也就是不启用序列数字缓存机制，有什么缺点呢？


2、过多的Redo Log生成


我们首先从Redo的统计情况入手，看看cache在这个过程中的影响。我们选择Oracle 10g作为实验环境。

SQL> select * from v$version;


BANNER

----------------------

Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Prod

PL/SQL Release 10.2.0.1.0 - Production

CORE    10.2.0.1.0    Production


TNS for 32-bit Windows: Version 10.2.0.1.0 - Production

NLSRTL Version 10.2.0.1.0 - Production

分别创建两个sequence实验对象。

SQL> create sequence seq_nocache nocache;

Sequence created


SQL> create sequence seq_cache cache 3;

Sequence created

我们先对nocache对象进行实验。我们选择autotrace工具，进行三次调用操作，来观察各种资源使用情况。

-第一次调用；

SQL> select seq_nocache.nextval from dual;


NEXTVAL

----

1


已用时间:  00: 00: 00.01


执行计划

--------------------

Plan hash value: 3078288422


------------------------

| Id  | Operation        | Name        | Rows  | Cost (%CPU)| Time     |

------------------------

|   0 | SELECT STATEMENT |             |     1 |     2   (0)| 00:00:01 |

|   1 |  SEQUENCE        | SEQ_NOCACHE |       |            |          |

|   2 |   FAST DUAL      |             |     1 |     2   (0)| 00:00:01 |

------------------------

统计信息

--------------------

30  recursive calls

3  db block gets

3  consistent gets

0  physical reads

640  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed


-第二次调用（篇幅原因，执行计划和部分统计量省略）

SQL> select seq_nocache.nextval from dual;


NEXTVAL

----

2


已用时间:  00: 00: 00.01


统计信息

--------------------

14  recursive calls

3  db block gets

1  consistent gets

0  physical reads

688  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed


-第三次调用

SQL> select seq_nocache.nextval from dual;


NEXTVAL

----

3


已用时间:  00: 00: 00.01


统计信息

--------------------

14  recursive calls

3  db block gets

1  consistent gets

0  physical reads

636  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed

篇幅原因，本文只表现部分结果。从结果统计量中，可以发现: 虽然我们对sequence对象是采用select操作。但是对nocache的序列对象而言，每次操作都会有600左右的redo log生成。


那么，对于开启了cache的sequence对象而言，有什么不同呢？

SQL> select seq_cache.nextval from dual;


NEXTVAL

----

1


已用时间:  00: 00: 00.03


执行计划

--------------------

Plan hash value: 2754437009


------------------------

| Id  | Operation        | Name      | Rows  | Cost (%CPU)| Time     |

------------------------

|   0 | SELECT STATEMENT |           |     1 |     2   (0)| 00:00:01 |

|   1 |  SEQUENCE        | SEQ_CACHE |       |            |          |

|   2 |   FAST DUAL      |           |     1 |     2   (0)| 00:00:01 |

------------------------

统计信息

--------------------

30  recursive calls

3  db block gets

3  consistent gets

0  physical reads

688  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed


SQL> select seq_cache.nextval from dual;


NEXTVAL

----

2


已用时间:  00: 00: 00.00


统计信息

--------------------

0  recursive calls

0  db block gets

0  consistent gets

0  physical reads

0  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed


SQL> select seq_cache.nextval from dual;


NEXTVAL

----

3


已用时间:  00: 00: 00.01


统计信息

--------------------

0  recursive calls

0  db block gets

0  consistent gets

0  physical reads

0  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed


-第四次调用，获取新的cache值。

SQL> select seq_cache.nextval from dual;


NEXTVAL

----

4


统计信息

--------------------

14  recursive calls

3  db block gets

1  consistent gets

0  physical reads

636  redo size

407  bytes sent via SQL*Net to client

400  bytes received via SQL*Net from client

2  SQL*Net roundtrips to/from client

0  sorts (memory)

0  sorts (disk)

1  rows processed

对cache的sequence对象而言，redo size生成的频率显然是低得多。从上面的四次调用中，只有第一次和第四次调用的时候，才生成了redo log记录。这个显然同我们设置的cache=3相对应。


设置cache之后，Oracle似乎不用为每次的nextval进行数据字典修改，生成redo log记录。只有cache在内存中使用结束之后，才会进行获取。


在实际的生产环境中，我们对redo size无必要的生成是要尽力避免的。首先，过多的redo log生成，容易造成online redo log的写入量增加，切换频繁。第二，redo size和nocache的使用，可能是伴随着频繁的commit动作，进而是频繁的log buffer写入online log file的过程。同时归档量增加。同时，在进行恢复的时候，也要消耗更多的时间。


所以，设置cache可以有效减少redo log的大小。


从redo size动作，我们猜测在nextval的时候存在数据字典的频繁更新风险。


3、潜在的行锁争用（row lock contention）


我们猜测在nextval的时候，Oracle做了些什么。于是，我们选择10046事件，跟踪设置cache和不设置cache的两种sequence，在底层递归调用的行为。


我们本次使用oradebug进行事件跟踪。

SQL> oradebug setmypid;

已处理的语句

SQL> oradebug unlimit;

已处理的语句

SQL> oradebug event 10046 trace name context forever, level 12

已处理的语句

SQL> select scott.seq_nocache.nextval from dual;

NEXTVAL

----

9


SQL> select scott.seq_nocache.nextval from dual;

NEXTVAL

----

10


SQL> select scott.seq_nocache.nextval from dual;

NEXTVAL

----

11


SQL> select scott.seq_cache.nextval from dual;

NEXTVAL

----

9


SQL> select scott.seq_cache.nextval from dual;

NEXTVAL

----

10


SQL> select scott.seq_cache.nextval from dual;

NEXTVAL

----

11


SQL> oradebug event 10046 trace name context off;

已处理的语句


SQL> oradebug tracefile_name

c:\tool\oracle\oracle\product\10.2.0\admin\ots\udump\ots_ora_5932.trc

打开跟踪文件，我们首先分析nocache的几次调用片段。


-篇幅原因，本部分有省略；

=====================

PARSING IN CURSOR #1 len=42 dep=0 uid=0 ct=3 lid=0 tim=16143418536 hv=311402377 ad='248b5c60'

select scott.seq_nocache.nextval from dual –第一次调用nocache

END OF STMT

PARSE #1:c=0,e=110,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16143418526

BINDS #1:

EXEC #1:c=0,e=13893,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16143450260

WAIT #1: nam='SQL*Net message to client' ela= 8 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16143453714

=====================

PARSING IN CURSOR #2 len=129 dep=1 uid=0 ct=6 lid=0 tim=16143457545 hv=2635489469 ad='2891ff84'

update seq$ set increment$=:2,minvalue=:3,maxvalue=:4,cycle#=:5,order$=:6,cache=:7,highwater=:8,audit$=:9,flags=:10 where obj#=:1 –第一次循环递归；

END OF STMT

PARSE #2:c=0,e=129,p=0,cr=0,cu=0,mis=0,r=0,dep=1,og=4,tim=16143457535

BINDS #2:

kkscoacd

Bind#0

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c69dc  bln=24  avl=02  flg=09

value=1

Bind#1

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c69ee  bln=24  avl=02  flg=09

value=1

Bind#2

oacdty=02 mxl=22(15) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c6a00  bln=24  avl=15  flg=09

value=999999999999999999999999999

Bind#3

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefb8  bln=24  avl=01  flg=05

value=0

Bind#4

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef94  bln=24  avl=01  flg=05

value=0

Bind#5

oacdty=02 mxl=22(01) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c6a12  bln=24  avl=01  flg=09

value=0

Bind#6

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c6a24  bln=24  avl=02  flg=09

value=10

Bind#7

oacdty=01 mxl=32(32) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=01 csi=852 siz=32 ff=0

kxsbbbfp=248c6a36  bln=32  avl=32  flg=09

value="-----------"

Bind#8

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef70  bln=24  avl=02  flg=05

value=8

Bind#9

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefdc  bln=22  avl=04  flg=05

value=113487

（有省略……）


=====================

PARSING IN CURSOR #2 len=42 dep=0 uid=0 ct=3 lid=0 tim=16145504123 hv=311402377 ad='248b5c60'

select scott.seq_nocache.nextval from dual –第二次调用

END OF STMT

PARSE #2:c=0,e=50,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16145504114

BINDS #2:

EXEC #2:c=15625,e=4237,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16145528418

WAIT #2: nam='SQL*Net message to client' ela= 8 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16145532367

=====================

PARSING IN CURSOR #1 len=129 dep=1 uid=0 ct=6 lid=0 tim=16145536517 hv=2635489469 ad='2891ff84'

update seq$ set increment$=:2,minvalue=:3,maxvalue=:4,cycle#=:5,order$=:6,cache=:7,highwater=:8,audit$=:9,flags=:10 where obj#=:1

END OF STMT

PARSE #1:c=0,e=49,p=0,cr=0,cu=0,mis=0,r=0,dep=1,og=4,tim=16145536507

BINDS #1:

kkscoacd

(……)

Bind#6

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c6a24  bln=24  avl=02  flg=09

value=11

Bind#7

oacdty=01 mxl=32(32) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=01 csi=852 siz=32 ff=0

kxsbbbfp=248c6a36  bln=32  avl=32  flg=09

value="-----------"

Bind#8

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef70  bln=24  avl=02  flg=05

value=8

Bind#9

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefdc  bln=22  avl=04  flg=05

value=113487


=====================

PARSING IN CURSOR #1 len=42 dep=0 uid=0 ct=3 lid=0 tim=16147403782 hv=311402377 ad='248b5c60'

select scott.seq_nocache.nextval from dual –第三次调用

END OF STMT

=====================

PARSING IN CURSOR #2 len=129 dep=1 uid=0 ct=6 lid=0 tim=16147424639 hv=2635489469 ad='2891ff84'

update seq$ set increment$=:2,minvalue=:3,maxvalue=:4,cycle#=:5,order$=:6,cache=:7,highwater=:8,audit$=:9,flags=:10 where obj#=:1

END OF STMT

PARSE #2:c=0,e=43,p=0,cr=0,cu=0,mis=0,r=0,dep=1,og=4,tim=16147424633

BINDS #2:

kkscoacd


Bind#6

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c6a24  bln=24  avl=02  flg=09

value=12

Bind#7

oacdty=01 mxl=32(32) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=01 csi=852 siz=32 ff=0

kxsbbbfp=248c6a36  bln=32  avl=32  flg=09

value="-----------"

Bind#8

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef70  bln=24  avl=02  flg=05

value=8

Bind#9

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefdc  bln=22  avl=04  flg=05

value=113487

注意三次调用过程中的几个标注红色的部分。三次调用nextval，之后都存在一个递归调用更新seq$基表的过程。Seq$基表显然是记录系统sequence的数据字典表。更新信息虽然包括了所有字段，但是bind#6和bind#9需要额外注意。


Bind#6在undate语句中对应字段highwater，显然是表示当前sequence对象达到的最大数值，也就是更新之后的修改值。Bind#9表示的obj#编号，应该对应的11387就是我们的nocache实验sequence编号。

SQL> select object_type, object_id from dba_objects where wner='SCOTT' and object_name='SEQ_NOCACHE';


OBJECT_TYPE          OBJECT_ID

------- ----

SEQUENCE                113487

说明，在没有cache的情况下，每次调用nextval都会促使Oracle去更新且commit数据字典seq$记录。


那么，对cache的sequence而言，又是如何呢？

PARSING IN CURSOR #2 len=40 dep=0 uid=0 ct=3 lid=0 tim=16156274459 hv=1095976807 ad='24882bec'

select scott.seq_cache.nextval from dual –第一次调用

END OF STMT

PARSE #2:c=0,e=67,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16156274454

BINDS #2:

EXEC #2:c=0,e=84,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16156274601

WAIT #2: nam='SQL*Net message to client' ela= 6 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16156274643

FETCH #2:c=0,e=46,p=0,cr=0,cu=0,mis=0,r=1,dep=0,og=1,tim=16156274725

WAIT #2: nam='SQL*Net message from client' ela= 568 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16156275360

FETCH #2:c=0,e=3,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=0,tim=16156275411

WAIT #2: nam='SQL*Net message to client' ela= 2 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16156275445

WAIT #2: nam='SQL*Net message from client' ela= 2197902 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16158473393

STAT #2 id=1 cnt=1 pid=0 pos=1 bj=113488 p='SEQUENCE  SEQ_CACHE (cr=0 pr=0 pw=0 time=57 us)'

STAT #2 id=2 cnt=1 pid=1 pos=1 bj=0 p='FAST DUAL  (cr=0 pr=0 pw=0 time=8 us)'

=====================

PARSING IN CURSOR #1 len=40 dep=0 uid=0 ct=3 lid=0 tim=16158473685 hv=1095976807 ad='24882bec'

select scott.seq_cache.nextval from dual –第二次调用；

END OF STMT

PARSE #1:c=0,e=36,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16158473680

BINDS #1:

EXEC #1:c=0,e=73,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16158473813

WAIT #1: nam='SQL*Net message to client' ela= 5 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16158473855

=====================

PARSING IN CURSOR #2 len=129 dep=1 uid=0 ct=6 lid=0 tim=16158474024 hv=2635489469 ad='2891ff84'

update seq$ set increment$=:2,minvalue=:3,maxvalue=:4,cycle#=:5,order$=:6,cache=:7,highwater=:8,audit$=:9,flags=:10 where obj#=:1

END OF STMT

PARSE #2:c=0,e=30,p=0,cr=0,cu=0,mis=0,r=0,dep=1,og=4,tim=16158474020

BINDS #2:

kkscoacd

Bind#0

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c58a0  bln=24  avl=02  flg=09

value=1

Bind#1

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c58b2  bln=24  avl=02  flg=09

value=1

Bind#2

oacdty=02 mxl=22(15) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c58c4  bln=24  avl=15  flg=09

value=999999999999999999999999999

Bind#3

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefb8  bln=24  avl=01  flg=05

value=0

Bind#4

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef94  bln=24  avl=01  flg=05

value=0

Bind#5

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c58d6  bln=24  avl=02  flg=09

value=3

Bind#6

oacdty=02 mxl=22(02) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=248c58e8  bln=24  avl=02  flg=09

value=13

Bind#7

oacdty=01 mxl=32(32) mxlc=00 mal=00 scl=00 pre=00

oacflg=18 fl2=0001 frm=01 csi=852 siz=32 ff=0

kxsbbbfp=248c58fa  bln=32  avl=32  flg=09

value="-----------"

Bind#8

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cef70  bln=24  avl=02  flg=05

value=8

Bind#9

oacdty=02 mxl=22(22) mxlc=00 mal=00 scl=00 pre=00

oacflg=08 fl2=0001 frm=00 csi=00 siz=24 ff=0

kxsbbbfp=088cefdc  bln=22  avl=04  flg=05

value=113488


=====================

PARSING IN CURSOR #2 len=40 dep=0 uid=0 ct=3 lid=0 tim=16160280316 hv=1095976807 ad='24882bec'

select scott.seq_cache.nextval from dual –第三次调用

END OF STMT

PARSE #2:c=0,e=38,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16160280311

BINDS #2:

EXEC #2:c=0,e=77,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=1,tim=16160280449

WAIT #2: nam='SQL*Net message to client' ela= 6 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16160280593

FETCH #2:c=0,e=51,p=0,cr=0,cu=0,mis=0,r=1,dep=0,og=1,tim=16160280682

WAIT #2: nam='SQL*Net message from client' ela= 643 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16160281398

FETCH #2:c=0,e=3,p=0,cr=0,cu=0,mis=0,r=0,dep=0,og=0,tim=16160281451

WAIT #2: nam='SQL*Net message to client' ela= 3 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16160281482

\*** 2012-02-23 13:30:07.421

WAIT #2: nam='SQL*Net message from client' ela= 14238981 driver id=1413697536 #bytes=1 p3=0 obj#=-1 tim=16174520496

STAT #2 id=1 cnt=1 pid=0 pos=1 bj=113488 p='SEQUENCE  SEQ_CACHE (cr=0 pr=0 pw=0 time=52 us)'

STAT #2 id=2 cnt=1 pid=1 pos=1 bj=0 p='FAST DUAL  (cr=0 pr=0 pw=0 time=10 us)'

在三次调用中，只更新了一次seq$数据字典表。而且，更新的bind#6为13，实际上就是一次更新，多取出三个取值。以后的几次调用中，就不需要在更新该数据记录了。


由此，我们可以得到结论，无论对于cache还是nocache序列对象，都是存在更新数据字典表seq$的动作的。区别就是在于更新bind#6 highwater的频度和一次更新步长。


进一步想，如果我们处在一个高并发的情况下，系统频繁的多会话请求sequence取值。如果我们的sequence没有设置cache，那么每次都要更新数据字典，都要进行commit操作。多个会话还会出现该sequence记录的争用，出现等待事件row lock contention。


所以，一般情况下，我们建议设置一个较大的cache值，用于进行性能的优化。


4、写在后面的话


本篇解析了在单实例环境下，cache对于sequence的重要性。在RAC环境下，cache和noorder选项的作用更大。在RAC中，多个实例争用情况会让sequence设计的不合理效果放大。所以，在没有特殊情况下，还是设置合理的cache值，减少系统潜在性能瓶颈。