---
title: MySQL 复制
author: "-"
date: 2011-04-16T00:55:15+00:00
url: /?p=19
tags:
  - MySQL

categories:
  - inbox
---
## MySQL 复制
1， MySQL的复制原理以及流程。
先问基本原理流程，3个线程以及之间的关联。


  答: MySQL复制的三个线程: 主库线程，从库I/O线程，从库sql线程；


  复制流程:  (1) I/O线程向主库发出请求


   (2) 主库线程响应请求，并推binlog日志到从库

 (3) I/O线程收到线程并记入中继日志

 (4) Sql线程从中继日志读取sql，并记入从库binlog日志，flush进硬盘；

 (2) 再问一致性延时性，数据恢复；

答:  (1) 主从复制一致性由binlog执行顺序保证 (timespan+pos) ；

日志越详细，主从一致性越容易保证；

 (2) 延时性: 延时表现为behind_master_pos后面的数字，其实并不准确；

5.5.30以前版本都属于异步复制，因此都有延时。因为是主库执行完成后从库才执行，一先一后就有了延迟；

主从延迟的准确计算方法是: 延迟时间=从库执行sql完成的时刻-主库开始执行sql的时间；

 (3) 数据恢复: 备份时记录的binlog位置点 (timespan+pos) ；

 (3) 再问各种工作遇到的复制bug的解决方法；

答: 这个问题感觉描述并不准确，不清楚是主从复制故障还是bug；

故障一般由于主键冲突，链接不上主库，找不到对应的binlog位置等引起；

解决方法是跳过冲突，检查主从链接，找正确的pos；

bug不常见，笔者碰到过一次，分享如下: 

环境: 主库从库都是虚机，每十分钟与宿主机同步一次时间，大约每次与主机相差2秒；

表现: 从库复制时重复执行两秒之内的日志；

从库show slave status\G，behind_master_pos在60000和0之间循环，每两秒一次；

**2， MySQL中myisam与innodb的区别，至少5点。**


   (1)  问5点不同


  答: 1、 存储成本不一样，存储限制不一样；


  2、CPU使用成本不一样，innodb缓存数据和索引；


  3、锁粒度不一样，支持MVCC；


  4、缓存机制不一样(buffer_pool和key_buffer)


  5、事务支持；


  6、索引支持: 全文索引(myisam),外键(innodb)，hash(innodb)


  7、读写速度；


  8、备份；


   (2) 、问各种不同MySQL版本的2者的改进；


  最近测5.1.38和5.5.35


  Innodb: (1) adeptive_innodb_index可控；


   (2) innodb变为默认引擎；


   (3) 更快的innodb插入；


   (4) 读写线程数目；


   (5) 半同步复制；


   (6) performance_schame


  Myisam (1) 


   (3) 2者的索引的实现方式；


    myisam将索引和数据分开存放，索引记录索引中键值的物理位置，根据物理位置去MYD的数据页中寻找对应的data page；数据排列是堆数据，没有物理顺序，索引只是在逻辑上将数据串起来，并不改变数据的物理位置；


   innodb采用主键将数据进行物理排序存放，新插入的数据根据主键的大小，会修改主键索引的序列；secondary index通过查找主键来查找数据；


  3，问MySQL中varchar与char的区别以及varchar(30)中的30代表的涵义。


   (1)  varchar与char的区别


  答: 变长和固定长度


         (2) varchar(50)中50的涵义


             答:  字符最大长度50，所代表的字节数与字符集有关，比如是utf8占3个字节，那么varchar(50)字段在表中最大取到150个字节


   (3)  int (20) 中20的涵义


  答: int是类型的数字，在2进制记录里，长度最大为20，数字范围是-2^19~(2^19-1)；


         (4) 为什么MySQL这样设计？


  答: 在varchar(M)中,varchar在一张表中最大的字节数目为65535，实际长度跟存放的内容有关；


  4，问了innodb的事务与日志的实现方式。
 


   (1) 有多少种日志


  答: 5种，binlog,查询日志，慢查询，错误日志，中继日志


   (2) 日志的存放形式


  答: Binlog,中继日志都是二进制；


  其他三种是文本形式；


   (3) 事务是如何通过日志来实现的，说得越深入越好。


  答: Innodb日志需要开启显式提交，默认是关闭的；


  首先了解日志过程。缓存进log_buffer,每秒或每十秒刷入redo_log，提交后刷入硬盘


  事务日志会在innodb_buffer_pool页中标记行是否更新，删除，commit后刷入硬盘，没有commit则不计入磁盘，属于脏数据；


  5，问了MySQL binlog的几种日志录入格式以及区别
 


   (1)     各种日志格式的涵义


  答: 三种日志格式 : statement,row,mixed


  每一条DML操作的sql都被计入statement日志；


  每条DML操作的sql被记录为对每条数据的操作，计入row日志；


  mixed日志是上面两种的混合，具体记录的方式由隔离级别+binlog_format共同决定


   (2)     适用场景


  答: 1、Statement，优点: 不需要记录每一行的变化，减少了binlog日志量，节约了IO，提高性能；


  缺点: 由于记录的只是执行语句，为了这些语句能在slave上正确运行，因此还必须记录每条语句在执行的时候的一些相关信息，以保证所有语句能在slave得到和在master端执行时候相同 的结果；


  某些特定函数功能会引起复制问题,比如sleep()函数， last_insert_id()；


  某些函数无法计入复制日志:  LOAD_FILE()


  2、Row模式，优点: 不记录执行的sql语句的上下文相关的信息，仅需要记录那一条记录被修改成什么了；


    缺点: 产生大量的日志，大量日志造成io开销大；


  3、mixed模式，一般的语句修改使用statment格式保存binlog，statement无法完成主从复制的操作，则采用row格式保存binlog，MySQL根据sql来选择日志记录格式，表结构变更的时候就会以statement模式来记录，update或者delete等修改数据的语句，还是会记录所有行的变更；


         (3) 结合第一个问题，每一种日志格式在复制中的优劣。


  6，问了下MySQL数据库cpu飙升到500%的话他怎么处理？


  答:  (1) 多实例的服务器，先top查看是那一个进程，哪个端口占用CPU多；


   (2) show processeslist查看是否由于大量并发，锁引起的负载问题；


   (3) 否则，查看慢查询，找出执行时间长的sql；explain分析sql是否走索引，sql优化；


   (4) 再查看是否缓存失效引起，需要查看buffer命中率；


  7， sql优化。
 


            (1) explain出来的各种item的意义


  答: Select_type: 所使用的查询类型，主要有以下这几种查询类型: 

DEPENDENT SUBQUERY: 子查询内层的第一个SELECT，依赖于外部查询的结果集。

DEPENDENT UNION: 子查询中的UNION，且为UNION中从第二个SELECT开始的后面所有SELECT，同样依赖于外部查询的结果集。

PRIMARY: 子查询中的最外层查询，注意并不是主键查询。

SIMPLE: 除子查询或UNION之外的其他查询。

SUBQUERY: 子查询内层查询的第一个SELECT，结果不依赖于外部查询结果集。

UNCACHEABLE SUBQUERY: 结果集无法缓存的子查询。

UNION: UNION语句中第二个SELECT开始后面的所有SELECT，第一个SELECT为PRIMARY。

UNION RESULT: UNION 中的合并结果。

Table: 显示这一步所访问的数据库中的表的名称。

Type: 告诉我们对表使用的访问方式，主要包含如下集中类型。

const: 读常量，最多只会有一条记录匹配，由于是常量，实际上只须要读一次。

eq_ref: 最多只会有一条匹配结果，一般是通过主键或唯一键索引来访问。

fulltext: 进行全文索引检索。

index: 全索引扫描。

index_merge: 查询中同时使用两个 (或更多) 索引，然后对索引结果进行合并 (merge) ，再读取表数据。

index_subquery: 子查询中的返回结果字段组合是一个索引 (或索引组合) ，但不是一个主键或唯一索引。

rang: 索引范围扫描。

Possible_keys: 该查询可以利用的索引。如果没有任何索引可以使用，就会显示成null，这项内容对优化索引时的调整非常重要。

Key: MySQL Query Optimizer 从 possible_keys 中所选择使用的索引。

Key_len: 被选中使用索引的索引键长度。

Ref: 列出是通过常量 (const) ，还是某个表的某个字段 (如果是join) 来过滤 (通过key) 的。

Rows: MySQL Query Optimizer 通过系统收集的统计信息估算出来的结果集记录条数。

Extra: 查询中每一步实现的额外细节信息，主要会是以下内容。

注: http://www.cnblogs.com/hustcat/articles/1579244.html


            (2) profile的意义以及使用场景。


  profile是为了锁定sql执行过程中，在每一步消耗的资源；然后有针对性的进行优化；


            (3) explain中的索引问题。


  8,  备份计划，MySQLdump以及xtranbackup的实现原理，
 


        答:  MySQLdump: 先锁所有表，然后把表中每条sql拼接为insert语句，一页为一小段，


                                     备份结构为: 表结构+insert


               Xtrabackup分对innodb和myisam引擎表的备份；


  myisam: 锁表进行copy；


  innodb:  Xtrabackup备份Innodb是利用了innodb的crach_recovery功能；


                                     Crash_recovery是对事务日志，commit的sql记入datafile，没有commit的则回滚，这点在innodb启动时被应用；


                                     Xtrabackup由三个线程进行: 


         线程1，copy innodb的页，每秒copy1M，64页，copy过程中页数据是rw的，利用Innodb的内置表进行copy；


   线程2，监控copy过程中页数据是否正常，正常则copy，不正常则再copy一次，最多重复10次；


                                     线程3，监控logfile，有变化则立刻copy走；


                                     Copy结束后，记录位置点；


               增量备份:检查与上次备份，哪些页有变化，比较上次备份页的lsn与当前页lsn大小，有变化则copy走，copy结束后，则记录最后的位置点；


   (1) 备份计划


  Dump，每天备份一次，每15分钟日志备份；


  Xtranbackup: 每三天备份一次，每天一次增量备份，每15分钟一次日志备份；


   (2) 备份恢复时间


   这个真心没看懂问的什么意思。


   (3)  备份恢复失败如何处理


  答: 检查表是否损坏，正常则再重新备份恢复；


  9，  500台db，在最快时间之内重启。

10**，****在当前的工作中，你碰到到的最大的****MySQL db****问题是？****
  
** 


  11，  innodb的读写参数优化


   (1)     读取参数，global buffer pool以及 local buffer


- Innodb_buffer_pool_size, 理论上越大越好，建议服务器50%~80%，实际为数据大小80%~90%即可；
buffer pool的大小，默认值128MB，建议为总内存的80%(InnoDB还要为buffer pool预留一些空间供control structures使用，因此实际大小为设定值的110%左右)

该参数定义了 InnoDB 存储引擎的表数据和索引数据的最大内存缓冲区大小。和 MyISAM 存储引擎不同，MyISAM 的 key_buffer_size只缓存索引键， 而 innodb_buffer_pool_size 却是同时为数据块和索引块做缓存，这个特性和 Oracle 是一样的。这个值设得越高，访问 表中数据需要的磁盘 I/O 就越少。在一个专用的数据库服务器上，可以设置这个参数达机器 物理内存大小的 80%。尽管如此，还是建议用户不要把它设置得太大，因为对物理内存的竞 争可能在操作系统上导致内存调度。  
https://zhuanlan.zhihu.com/p/60089484  


  Innodb_read_io_thread，根据处理器内核数决定；


  Read_buffer_size;


  Sort_buffer_size


   (2)     写入参数


  Insert_buffer_size；


  Innodb_double_write；


  Innodb_write_io_thread


  innodb_flush_method


   (3)     与IO相关的参数


  Innodb_log_buffer_size


  innodb_flush_log_at_trx_commit


  innodb_file_io_threads


  innodb_max_dirty_pages_pct


        (4) 缓存参数以及缓存的适用场景


  12 ，请简洁地描述下MySQL中InnoDB支持的四种事务隔离级别名称，以及逐级之间的区别？


         未提交读 (uncommited read) ，提交读 (commited read) ，重复读 (repeatable read) ，串行读 (serializable) 


         这四种隔离级别逐个提高，区别表现在脏读，非重复读，幻读这三点，还有对并发的影响，隔离级别越高，并发性越差；


         所谓脏读，就是同一事务中，会读取还未提交的事务修改的数据；


         非重复读，是指在同一事务中，在t1时刻，读取某行数据时为A，t2时刻读取同一行数据时，由于其他事务更新，这行数据已经发生改变；


         幻读，是指在同一事务中，同一查询多次进行时，由于其他事务的提交，插入新纪录，导致每次查询的结果都不同；


  区别在于: 


         未提交读: 会造成脏读，非重复读，幻读；


         提交读: 不会造成脏读，但是会有非重复读，幻读；


         重复读: 可能会造成幻读；


         串行读: 不会造成脏读，非重复读，幻读；


  13，表中有大字段X (例如: text类型) ，且字段X不会经常更新，以读为为主，请问


   (1)     您 是选择拆成子表，还是继续放一起？


  a)      放在子表中


   (2)     写出您这样选择的理由？


  a)       避免大数据被频繁的从buffer重换进换出，影响其他数据的缓存；


  14，MySQL中InnoDB引擎的行锁是通过加在什么上完成 (或称实现) 的？为什么是这样子的？ 


         Innodb的行锁是加在索引实现的；


   原因是:innodb是将primary key index和相关的行数据共同放在B+树的叶节点；innodb一定会有一个primary key，secondary index查找的时候，也是通过找到对应的primary，再找对应的数据行；


http://www.cnblogs.com/wyeat/p/job_interview2.html