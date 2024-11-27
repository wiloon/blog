---
title: MVCC, Multiversion Concurrency Control, 多版本并发控制
author: "-"
date: 2017-05-09T01:39:18+00:00
url: mvcc
categories:
  - database
tags:
  - reprint
  - remix
---
## MVCC, Multiversion Concurrency Control, 多版本并发控制

[http://donghui.blog.51cto.com/2709336/692586](http://donghui.blog.51cto.com/2709336/692586)

多版本并发控制技术已经被广泛运用于各大数据库系统中,如 Oracle, MS SQL Server 2005+, Postgresql, Firebird, Maria 等等, 开源数据库 MySQL 中流行的 INNODB 引擎也采用了类似的并发控制技术.本文就将结合实例来解析不同事务隔离等级下 INNODB 的 MVCC 实现原理.

1.1 MVCC 简介

MVCC (Multiversion Concurrency Control), 即多版本并发控制技术, 它使得大部分支持行锁的事务引擎, 不再单纯的使用行锁来进行数据库的并发控制, 取而代之的是, 把数据库的行锁与行的多个版本结合起来, 只需要很小的开销, 就可以实现非锁定读, 从而大大提高数据库系统的并发性能.

1.2 实现原理

MVCC 可以提供基于某个时间点的快照, 使得对于事务看来, 总是可以提供与事务开始时刻相一致的数据, 而不管这个事务执行的时间有多长. 所以在不同的事务看来, 同一时刻看到的相同行的数据可能是不一样的, 即一个行可能有多个版本. 是否听起来不可思议呢?

原来, 为了实现 mvcc, innodb 对每一行都加上了两个隐含的列, 其中一列存储行被更新的"时间", 另外一列存储行被删除的"时间". 但是 innodb 存储的并不是绝对的时间, 而是与时间对应的数据库系统的版本号, 每当一个事务开始的时候, innodb 都会给这个事务分配一个递增的版本号, 所以版本号也可以被认为是事务号. 对于每一个"查询"语句, innodb 都会把这个查询语句的版本号同这个查询语句遇到的行的版本号进行对比, 然后结合不同的事务隔离等级, 来决定是否返回该行.

下面分别以 select、delete、 insert、 update 语句来说明:

1) SELECT
对于select语句,只有同时满足了下面两个条件的行,才能被返回:

- 行的被修改版本号小于或者等于该事务号
- 行的被删除版本号要么没有被定义, 要么大于事务的版本号: 行的删除版本号如果没有被定义, 说明该行没有被删除过; 如果删除版本号大于当前事务的事务号, 说明该行是被该事务后面启动的事务删除的, 由于是 repeatable read 隔离等级, 后开始的事务对数据的影响不应该被先开始的事务看见, 所以该行应该被返回.

2) INSERT
对新插入的行,行的更新版本被修改为该事务的事务号

3) DELETE

对于删除,innodb直接把该行的被删除版本号设置为当前的事务号,相当于标记为删除,而不是实际删除

4) UPDATE

在更新行的时候,innodb会把原来的行复制一份到回滚段中,并把当前的事务号作为该行的更新版本

1.3 MVCC 的优缺点

上述策略的结果就是,在读取数据的时候,innodb几乎不用获得任何锁, 每个查询都通过版本检查,只获得自己需要的数据版本,从而大大提高了系统的并发度.

这种策略的缺点是,为了实现多版本,innodb必须对每行增加相应的字段来存储版本信息,同时需要维护每一行的版本信息,而且在检索行的时候,需要进行版本的比较,因而降低了查询的效率;innodb还必须定期清理不再需要的行版本,及时回收空间,这也增加了一些开销

2 INNODB支持的事务隔离等级

INNODB支持并实现了ISO标准的4个事务隔离等级,即 READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, SERIALIZABLE.

1) READ UNCOMMITTED (可以读未提交的): 查询可以读取到其他事务正在修改的数据,即使其他事务的修改还没有提交.这种隔离等级无法避免脏读.

2) READ COMMITTED(只可以读已经提交的):其他事务对数据库的修改,只要已经提交,其修改的结果就是可见的,与这两个事务开始的先后顺序无关.这种隔离等级避免了脏读,但是无法实现可重复读,甚至有可能产生幻读.

3) REPEATABLE READ(可重复读):比read committed更进了一步,它只能读取在它开始之前已经提交的事务对数据库的修改,在它开始以后,所有其他事务对数据库的修改对它来说均不可见.从而实现了可重复读,但是仍有可能幻读

4) SERIALIZABLE(可串行化):这是事务隔离等级的最高级别.其实现原理就是对于所有的query,即使是查询,也会加上读锁,避免其他事务对数据的修改.所以它成功的避免了幻读.但是代价是,数据库系统的并发处理能力大大降低,所以它不会被用到生产系统中.

我们对MVCC和标准事务隔离等级有所了解以后,再结合实例来看看其具体表现吧.

3 不同事务隔离等级下的MVCC实现

MVCC由于其实现原理,只支持read committed和repeatable read隔离等级,下面分别举例详细说明:

每次开始之前,都先执行如下的语句:

create database if not exists mydb;

use mydb;

drop table if exists emp;

create table `emp` ( `empno` int(11) not null auto_increment, `ename` varchar(20) default null, Primary key (empno)) engine=innodb default charset=gbk;

insert into emp values(100, "yuxiangang") ;

insert into emp values(200,"2zhaoyinggang");

insert into emp values(300,"3yihongbin");

3.1 read committed隔离等级

说明:session 1和session 2表示访问同一个数据库的两个不同的会话.行号用来代表不同的语句执行的时间点.

行号

session 1

session 2

set transaction isolation level read committed;

2

start transaction;

3

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1yuxiangang |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

+---+---+

4

set transaction isolation level read committed;

5

start transaction;

6

update emp set ename=1 where empno=100;

delete from emp where empno=200;

说明: 修改一行,然后删除一行,但是事务不提交.

7

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1yuxiangang |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

+---+---+

说明:会话2的事务没有提交,所以会话1看不到会话2的事务对数据库数据的修改.但是实际上修改已经发生,会话1获取的被修改或者删除的数据,都来自于回滚段.这是通过MVCC来实现的.

8

commit;

说明: 会话2提交

9

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 300 | 3yihongbin |

+---+---+

说明:当事务2提交以后,由于会话1采用的是read committed隔离等级,所以会话2的提交马上会被会话1的事务看见.对于会话1来说,第一次执行select * from emp where empno>=100;与第二次执行该语句,两次看到的结果不一样,第一次读看到了3行,第二次只看到了2行,就像发生了幻觉,称之为幻读;第一次看到100对应的ename为1yuxiangang,第二次看到的100对应的是1,两次获取的数据内容不一样,称之为不可重复读.

3.2 repeatable read隔离等级

注意:先执行开头的所有sql语句.

行号

session 1

session 2

session 3

session 4

set transaction isolation level repeatable read;

2

start transaction;

3

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1yuxiangang |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

+---+---+

4

set @@session.autocommit=1;

说明: 这里让会话4可以自动提交,便于观察它对前面3个会话的影响

update emp set ename=1 where empno=100;

insert into emp values(400,"4chj");

说明: 会话4先更新一行数据,然后插入一行数据,并自动提交

5

select * from emp where empno>=100;

查询的结果为: +---+---+

| empno | ename |

+---+---+

| 100 | 1yuxiangang |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

+---+---+

说明: 会话1执行查询,两次查询得到的结果一样.它看不到会话4对数据库的修改,虽然会话4的事务已经提交.这是因为会话4的事务是在会话1的事务之后才开始.从这里也可以看出,repeatable read实现了可重复读

6

set transaction isolation level repeatable read;start transaction;

7

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

| 400 | 4chj |

+---+---+

说明: 会话2是在会话4之后开始的,所以它看到了会话4对数据库的修改.同时可以看到,相同的查询语句,不同的事务来执行的时候,得到的结果不一样.会话2与会话3执行相同的查询就得到不一样的结果.

8

update emp set ename=2 where empno=200;

9

set transaction isolation level repeatable read;start transaction;

10

select * from emp where empno>=100;查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4chj |

+---+---+

说明: 同样,这个会话查询到的结果与会话1和会话2的结果也不一样.而且会话3看到了会话4对数据库的修改.

11

update emp set ename=4 where empno=400;

12

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

说明: 事务总是可以看到自身对数据库数据的修改,尽管别的事务可能看不到这种修改

13

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1yuxiangang |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2zhaoyinggang |

| 300 | 3yihongbin |

| 400 | 4chj |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4chj |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

说明: 从上面的结果可以很清晰的看到:会话1,2,3,4执行相同的语句,即使是在同一时刻,他们看到的数据都可能不一样:对于empno为100的行,有 100 1yuxiangang 和 100 1两个版本;对于empno为200的行,有 200 2zhaoyinggang 和200 2两个版本…,而每一行数据都可能存在多个版本,那么这些行组合起来得到的结果集的版本就更是不计其数,这就是数据库多版本的由来.MVCC就是通过事务发生的不同的时间点,与数据行的版本来进行对比,从而取回与事务开始的时间点相一致的数据,来实现非阻塞的一致读.

14

commit;

commit;

commit;

commit;

15

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

select * from emp where empno>=100;

查询的结果为:

+---+---+

| empno | ename |

+---+---+

| 100 | 1 |

| 200 | 2 |

| 300 | 3yihongbin |

| 400 | 4 |

+---+---+

说明: 当所有事务都提交后,他们看到的结果都是一样的
