---
title: MySQL分区表, partition
author: "-"
date: 2017-04-07T02:27:33+00:00
url: /?p=10037
tags:
 - MySQL

categories:
  - inbox
---
## MySQL分区表, partition
### 没有分区的表创建分区
partition management on a not partitioned table is not possible

```sql
ALTER TABLE table0 PARTITION BY RANGE (to_days(field0)) (
PARTITION p201908 VALUES less THAN (737668),
PARTITION p201909 VALUES LESS THAN (737698),
PARTITION p201910 VALUES LESS THAN (737729),
PARTITION p201911 VALUES LESS THAN (737759),
PARTITION p201912 VALUES LESS THAN (737790)
)
```

```sql
ALTER TABLE table0 PARTITION BY RANGE (to_days(field0)) (
PARTITION p202007 VALUES less THAN (to_days('2020-08-01')),
PARTITION p202008 VALUES less THAN (to_days('2020-09-01')),
PARTITION p202009 VALUES less THAN (to_days('2020-10-01')),
PARTITION p202010 VALUES less THAN (to_days('2020-11-01')),
PARTITION p202011 VALUES less THAN (to_days('2020-12-01')),
PARTITION p202012 VALUES less THAN (to_days('2021-01-01')),
)
```

### 添加分区

```sql
alter TABLE  table0 add PARTITION ( PARTITION p201908 VALUES less THAN (737668));
alter table table0 add PARTITION ( PARTITION pmax VALUES less than MAXVALUE);
```

```sql
-- check partition size
USE information_schema;

SELECT PARTITION_NAME,TABLE_ROWS
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_NAME = 't0' and PARTITION_NAME='p0';

-- drop partition
ALTER TABLE `db0`.t0 DROP PARTITION p0;

```

### 查看分区的存储情况
```sql
SELECT partition_name, PARTITION_DESCRIPTION, PARTITION_EXPRESSION, table_rows
FROM information_schema.partitions
WHERE table_name = 'table0'
```

### 查询
查询的where条件要写完整的时间范围, 只写> 或者只写<, 会导致查询所有的分区.

    SELECT *  FROM table0 WHERE field0 > '2021-05-01 00:00:00' AND field0 < '2021-05-06 00:00:00' 
 
1. 什么是表分区？
MySQL 分区表 :逻辑上是一个表,底层却是由多个物理分区(子表)组合而成的一个表集合,每个子表相对独立,各自存储着自己的数据和索引。这种分区表又称局部分区表。MySQL暂时不支持全局分区表(各个分区存储数据,索引存在其他对象中)在以前的老版本(MySQL5.6之前)中有一个变量have_partitioning 开关控制着是否开启分区,默认为开启的,MySQL5.6将这个变量去掉了,默认自动开启。   

2. 表分区与分表的区别
分表: 指的是通过一定规则,将一张表分解成多张不同的表。比如将用户订单记录根据时间成多个表。 分表与分区的区别在于: 分区从逻辑上来讲只有一张表,而分表则是将一张表分解成多张表。

3. 表分区有什么好处？
数据管理方便。单独管理某些分区,例如: 删除历史数据,优化、检查、修复个别分区,备份,恢复个别分区对某些特定的查询起到极大的优化作用,通过跨多个磁盘来分散数据查询,来获得更大的查询吞吐量。

分区表的数据可以分布在不同的物理设备上,从而高效地利用多个硬件设备。和单个磁盘或者文件系统相比,可以存储更多数据优化查询, 在where语句中包含分区条件时,可以只扫描一个或多个分区表来提高查询效率；涉及到例如SUM() 和 COUNT()这样聚合函数的查询时,也可以在多个分区上并行处理,最后汇总结果。分区表更容易维护。例如: 想批量删除大量数据可以清除整个分区。

可以使用分区表来避免某些特殊的瓶颈,例如InnoDB的单个索引的互斥访问,ext3文件系统的inode锁竞争等。分散热点(hotpage)

4. 分区表的限制因素
  
一个表最多只能有1024个分区

MySQL5.1中,分区表达式必须是整数,或者返回整数的表达式。在MySQL5.5中提供了非整数表达式分区的支持。MySQL5.6开始可以直接对列进行分区。

所有的主键或者唯一索引必须被保函在分区表达式中。如果分区字段中有主键或者唯一索引的列,那么多有主键列和唯一索引列都必须包含进来。即: 分区字段要么不包含主键或者索引列,要么包含全部主键和索引列。

分区表中无法使用外键约束

MySQL的分区适用于一个表的所有数据和索引,不能只对表数据分区而不对索引分区,也不能只对索引分区而不对表分区,也不能只对表的一部分数据分区。

在分区表达式中,不允许子查询

  5. 如何判断当前MySQL是否支持分区？ (MySQL5.6之前,MySQL5.6将这个变量去掉了,默认自动开启。) 
  
    命令: show variables like '%partition%' 运行结果:
  
    MySQL> show variables like '%partition%';
  
    +-------+---+
  
    | Variable_name | Value |
  
    +-------+---+
  
    | have_partitioning | YES |
  
    +-------+---+
  
    1 row in set (0.00 sec)
  
    have_partintioning 的值为YES,表示支持分区。

  6. 分区类型
  
    range分区表: 根据一个列的值的区间范围分布存储数据。
  
    list分区表: 按照List中的值分区,和range分区表相似,但是list分区面向的是离散的值。range分区的区间范围值是连续的。
  
    hash分区表: 根据用户提供的分区表达式的返回值来进行分布存储数据。
  
    key分区表: 根据数据库提供的哈希函数来进行分区。说明 在MySQL5.1版本中,RANGE,LIST,HASH分区要求分区键必须是INT类型,或者通过表达式返回INT类型。但KEY分区的时候,可以使用其他类型的列 (BLOB,TEXT类型除外) 作为分区键。
  
    columns分区: 可以直接使用非整型的数据进行分区但只能在range和list上使用
  
    子分区: 又称符合分区,MySQL允许在range和list的分区上再进行hash或key的字分区。

  7. Range分区

利用取值范围进行分区,区间要连续并且不能互相重叠。 语法: 

partition by range(exp)( //exp可以为列名或者表达式,比如to_date(created_date)
      
partition p0 values less than(num)
  
)
  
例如: 

MySQL> create table emp(
      
-> id INT NOT null,
      
-> store_id int not null
      
-> )
      
-> partition by range(store_id)(
      
-> partition p0 values less than(10),
      
-> partition p1 values less than(20)
      
-> );
  
上面的语句创建了emp表,并根据store_id字段进行分区,小于10的值存在分区p0中,大于等于10,小于20的值存在分区p1中。 注意 每个分区都是按顺序定义的,从最低到最高。上面的语句,如果将less than(10) 和less than (20)的顺序颠倒过来,那么将报错,如下: 

ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition
  
RANGE分区存在的问题

range范围覆盖问题: 当插入的记录中对应的分区键的值不在分区定义的范围中的时候,插入语句会失败。 上面的例子,如果我插入一条store_id = 30的记录会怎么样呢？ 我们上面分区的时候,最大值是20,如果插入一条超过20的记录,会报错:
  
MySQL> insert into emp(id,store_id) values(2,30);
  
ERROR 1526 (HY000): Table has no partition for value 30
  
提示30这个值没有对应的分区。 解决办法 A. 预估分区键的值,及时新增分区。 B. 设置分区的时候,使用values less than maxvalue 子句,MAXVALUE表示最大的可能的整数值。 C. 尽量选择能够全部覆盖的字段作为分区键,比如一年的十二个月等。

Range分区中,分区键的值如果是NULL,将被作为一个最小值来处理。
  
8. LIST分区

List分区是建立离散的值列表告诉数据库特定的值属于哪个分区。 语法: 

    partition by list(exp)( //exp为列名或者表达式
        partition p0 values in (3,5)  //值为3和5的在p0分区
    )
    

与Range不同的是,list分区不必生命任何特定的顺序。例如: 

MySQL> create table emp1(
      
-> id int not null,
      
-> store_id int not null
      
-> )
      
-> partition by list(store_id)(
      
-> partition p0 values in (3,5),
      
-> partition p1 values in (2,6,7,9)
      
-> );
  
注意 如果插入的记录对应的分区键的值不在list分区指定的值中,将会插入失败。并且,list不能像range分区那样提供maxvalue。


  
    Columns分区
  


MySQL5.5中引入的分区类型,解决了5.5版本之前range分区和list分区只支持整数分区的问题。 Columns分区可以细分为 range columns分区和 list columns分区,他们都支持整数,日期时间,字符串三大数据类型。 (不支持text和blob类型作为分区键)  columns分区还支持多列分区 (这里不详细展开) 。

columns分区: MySQL5.6可以直接使用非整型的数据进行分区但只能在range和list上使用。

在MySQL5.6之前必须使用函数将列换成成整型才能对表进行分区,可以用来支持分区的常用函数有year(),to_days(),month()等。

MySQL5.6开始对整列进行分区,不需要函数进行转换,但是这个功能仅仅限于range和list分区

range columns 分区

drop table if EXISTS tt ;

create table tt(

tid int not null auto_increment ,

tname varchar(100) not null ,

tage TINYINT default 0 ,

tadd varchar(100) default " ,

tel varchar(20) default 0,

tmob varchar(20) DEFAULT " ,

tsfz varchar(100) default ",

tdeptId int default 0 ,

taddtime datetime DEFAULT now(),

PRIMARY key(tid,taddtime)

)

ENGINE=InnoDB DEFAULT CHARSET=utf8

PARTITION by range COLUMNS(taddtime)(

PARTITION p0 VALUES less than ('2009-01-01') ,

PARTITION p1 VALUES less than ('2010-01-01') ,

PARTITION p2 VALUES less than ('2011-01-01'),

PARTITION p3 VALUES less than ('2012-01-01'),

PARTITION p4 VALUES less than MAXVALUE

)

list columns 分区: 

drop table if EXISTS tt ;

create table tt(

tid int not null auto_increment ,

tname varchar(100) not null ,

tage TINYINT default 0 ,

tadd varchar(100) default " ,

tel varchar(20) default 0,

tmob varchar(20) DEFAULT " ,

tsfz varchar(100) default ",

tdeptId int default 0 ,

taddtime datetime DEFAULT now(),

PRIMARY key(tid,tname)

)

ENGINE=InnoDB DEFAULT CHARSET=utf8

PARTITION by list COLUMNS(tname)(

PARTITION p0 VALUES in ('张三疯','张无忌') ,

PARTITION p1 VALUES in ('郭靖','杨康') ,

PARTITION p2 VALUES in ('李四','张三'),

PARTITION p3 VALUES in ('甲鱼','乌龟')

)

Q1: list分区中,出现定义表达式以外的值

MySQL> insert into tt(tname,tage,tadd,tel,tmob,tsfz) VALUES('朱元璋',120,'武当山' ,18099001122,'012-46319976′,") ;

ERROR 1526 (HY000): Table has no partition for value from column_list

直接插入失败了,原因是MySQL不知道将这条数据存储在哪个分区中。


  
    Hash分区
  


Hash分区主要用来分散热点读,确保数据在预先确定个数的分区中尽可能平均分布。 MySQL支持两种Hash分区:常规Hash分区和线性Hash分区。 A. 常规Hash分区:使用取模算法 语法: 

partition by hash(store_id) partitions 4;
  
上面的语句,根据store_id对4取模,决定记录存储位置。 比如store_id = 234的记录,MOD(234,4)=2,所以会被存储在第二个分区。

常规Hash分区的优点和不足 优点: 能够使数据尽可能的均匀分布。 缺点: 不适合分区经常变动的需求。假如我要新增加两个分区,现在有6个分区,那么MOD(234,6)的结果与之前MOD(234,4)的结果就会出现不一致,这样大部分数据就需要重新计算分区。为解决此问题,MySQL提供了线性Hash分区。

B. 线性Hash分区: 分区函数是一个线性的2的幂的运算法则。 语法: 

partition by LINER hash(store_id) partitions 4;
  
与常规Hash的不同在于,"Liner"关键字。 算法介绍: 假设要保存记录的分区编号为N,num为一个非负整数,表示分割成的分区的数量,那么N可以通过以下步骤得到: 
  
Step 1. 找到一个大于等于num的2的幂,这个值为V,V可以通过下面公式得到: 
  
V = Power(2,Ceiling(Log(2,num)))
  
例如: 刚才设置了4个分区,num=4,Log(2,4)=2,Ceiling(2)=2,power(2,2)=4,即V=4
  
Step 2. 设置N=F(column_list)&(V-1)
  
例如: 刚才V=4,store_id=234对应的N值,N = 234& (4-1)  =2
  
Step 3. 当N>=num,设置V=Ceiling(V/2),N=N&(V-1)
  
例如: store_id=234,N=2<4,所以N就取值2,即可。
  
假设上面算出来的N=5,那么V=Ceiling(4/2)=2,N=5&(2-1)=1,即在第一个分区。

线性Hash的优点和不足 优点: 在分区维护 (增加,删除,合并,拆分分区) 时,MySQL能够处理得更加迅速。 缺点: 与常规Hash分区相比,线性Hash各个分区之间的数据分布不太均衡。


  
    Key分区
  


类似Hash分区,Hash分区允许使用用户自定义的表达式,但Key分区不允许使用用户自定义的表达式。Hash仅支持整数分区,而Key分区支持除了Blob和text的其他类型的列作为分区键。 语法:

partition by key(exp) partitions 4;//exp是零个或多个字段名的列表
  
key分区的时候,exp可以为空,如果为空,则默认使用主键作为分区键,没有主键的时候,会选择非空惟一键作为分区键。


  
    子分区
  


分区表中对每个分区再次分割,又成为复合分区。


  
    分区对于NULL值的处理
  


MySQ允许分区键值为NULL,分区键可能是一个字段或者一个用户定义的表达式。一般情况下,MySQL在分区的时候会把NULL值当作零值或者一个最小值进行处理。
  
注意
  
Range分区中: NULL值被当作最小值来处理
  
List分区中: NULL值必须出现在列表中,否则不被接受
  
Hash/Key分区中: NULL值会被当作零值来处理


  
    分区管理
  


分区管理包括对于分区的增加,删除,以及查询。

增加分区: 
  
对于Range分区和LIst分区来说: 
  
alter table table_name add partition (partition p0 values ...(exp))
  
values后面的内容根据分区的类型不同而不同。
  
对于Hash分区和Key分区来说: 

alter table table_name add partition partitions 8;
  
上面的语句,指的是新增8个分区 。

删除分区
  
对于Range分区和List分区: 
  
alter table table_name drop partition p0; //p0为要删除的分区名称
  
删除了分区,同时也将删除该分区中的所有数据。同时,如果删除了分区导致分区不能覆盖所有值,那么插入数据的时候会报错。
  
对于Hash和Key分区: 

alter table table_name coalesce partition 2; //将分区缩减到2个
  
coalesce [ˌkəʊəˈles] vi. 联合,合并

分区查询 1) 查询某张表一共有多少个分区
  
MySQL> select
   
-> partition_name,
   
-> partition_expression,
   
-> partition_description,
   
-> table_rows
   
-> from
   
-> INFORMATION_SCHEMA.partitions
   
-> where
   
-> table_schema='test'
   
-> and table_name = 'emp';
  
+------+--------+--------+----+
  
| partition_name | partition_expression | partition_description | table_rows |
  
+------+--------+--------+----+
  
| p0 | store_id | 10 | 0 |
  
| p1 | store_id | 20 | 1 |
  
+------+--------+--------+----+
  
即,可以从information_schema.partitions表中查询。
  
2) 查看执行计划,判断查询数据是否进行了分区过滤

MySQL> explain partitions select * from emp where store_id=10 \G;
  
\***\***\***\***\***\***\***\***\*\\*\* 1. row \*\*\***\***\***\***\***\***\***\****
          
id: 1
  
select_type: SIMPLE
       
table: emp
  
partitions: p1
        
type: system
  
possible_keys: NULL
         
key: NULL
     
key_len: NULL
         
ref: NULL
        
rows: 1
       
Extra:
  
1 row in set (0.00 sec)
  
上面的结果: partitions:p1 表示数据在p1分区进行检索。

[参考资料] 《深入MySQL数据库开发、优化与管理维护 (第2版) 》
  
《高性能MySQL》

http://www.cnblogs.com/zemliu/archive/2013/07/21/3203511.html
  
分区表是一种粗粒度,简易的索引策略,适用于大数据的过滤场景.最适合的场景是,没有合适的索引时,对其中几个分区表进行全表扫描.或者只有一个分区表和索引是热点,而且这个分区和索引能够全部存储在内存中.限制单表分区数不要超过150个,并且注意某些导致无法做分区过滤的细节,分区表对于单条记录的查询没有优势,需要注意这类查询的性能.

分区表语法

分区表分为RANGE,LIST,HASH,KEY四种类型,并且分区表的索引是可以局部针对分区表建立的

创建分区表
  
CREATE TABLE sales (
  
id INT AUTO_INCREMENT,
  
amount DOUBLE NOT NULL,
  
order_day DATETIME NOT NULL,
  
PRIMARY KEY(id, order_day)
  
) ENGINE=Innodb PARTITION BY RANGE(YEAR(order_day)) (
  
PARTITION p_2010 VALUES LESS THAN (2010),
  
PARTITION p_2011 VALUES LESS THAN (2011),
  
PARTITION p_2012 VALUES LESS THAN (2012),
  
PARTITION p_catchall VALUES LESS THAN MAXVALUE);

这段语句表示将表内数据按照order_dy的年份范围进行分区,2010年一个区,2011一个,2012一个,剩下的一个.

要注意如果这么做,则order_day必须包含在主键中,且会产生一个问题,就是当年份超过阈值,到了2013,2014时,需要手动创建这些分区

替代方法就是使用HASH

CREATE TABLE sales (
  
id INT PRIMARY KEY AUTO_INCREMENT,
  
amount DOUBLE NOT NULL,
  
order_day DATETIME NOT NULL
  
) ENGINE=Innodb PARTITION BY HASH(id DIV 1000000);
  
这种分区表示每100W条数据建立一个分区,且没有阈值范围的影响

对于大数据而言

对于大数据(如10TB)而言,索引起到的作用相对小,因为索引的空间与维护成本很高,另外如果不是索引覆盖查询,将导致回表,造成大量磁盘IO.那么对于这种情况的解决策略是:

1.全量扫描数据,不要任何索引

通过分区表表达式将数据定位在少量的分区表,然后正常访问这些分区表的数据

2.分离热点,索引数据

将热点数据分离出来在一个小的分区,并对分区建立索引,对热点数据的查询提高效率.

分区表的问题

1.NULL值使分区过滤无效

假设按照RANGE YEAR(order_date)分区,那么如果这个表达式计算出来的时NULL值,记录就会被存放到第一个分区.所以在查询时加入查询条件有可能出现NULL值,那么就会去检查第一个分区.解决的方法可以是将第一个分区建立为NULL分区 PARTITION p_nulls VALUES LESS THAN (0),或者在MySQL5.5以后,直接使用COLUMN建立分区 PARTITION BY RANGE COLUMNS(order_date)


  
    选择分区的成本
  


每插入一行数据都需要按照表达式筛选插入的分区地址


  
    分区列和索引列不匹配
  


如果索引列和分区列不匹配,且查询中没有包含过滤分区的条件,会导致无法进行分区过滤,那么将会导致查询所有分区.


  
    打开并锁住所有底层表
  


分区表的的查询策略是在分区过滤之前,打开并锁住所有底层表,这会造成额外的开销,解决问题的方法是尽量使用批量操作,例如LOAD DATA INFILE,或者一次删除多行数据.

过滤分区表的要点

过滤分区表的WHERE条件必须是切分分区表的列,而不能带有函数,例如只能是order_day,而不能是YEAR(order_day)

https://my.oschina.net/jasonultimate/blog/548745
  
http://dwchaoyue.blog.51cto.com/2826417/1553270