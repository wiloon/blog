---
title: innodb_autoinc_lock_mode
author: "-"
date: 2014-01-20T09:34:59+00:00
url: /?p=6241
categories:
  - Uncategorized
tags:
  - MySQL

---
## innodb_autoinc_lock_mode
innodb_autoinc_lock_mode这个参数控制着在向有auto_increment 列的表插入数据时，相关锁的行为；

通过对它的设置可以达到性能与安全(主从的数据一致性)的平衡

【0】我们先对insert做一下分类

　　首先insert大致上可以分成三类：
　　　　1、simple insert 如insert into t(name) values('test')
　　　　2、bulk insert 如load data | insert into ... select .... from ....
　　　　3、mixed insert 如insert into t(id,name) values(1,'a'),(null,'b'),(5,'c');

 

【1】innodb_autoinc_lock_mode 的说明

　　innodb_auto_lockmode有三个取值：
　　　　1、0 这个表示tradition 传统
　　　　2、1 这个表示consecutive 连续
　　　　3、2 这个表示interleaved 交错

【1.1】tradition(innodb_autoinc_lock_mode=0) 模式:

　　1、它提供了一个向后兼容的能力
　　2、在这一模式下，所有的insert语句("insert like") 都要在语句开始的时候得到一个
　　　  表级的auto_inc锁，在语句结束的时候才释放这把锁，注意呀，这里说的是语句级而不是事务级的，
　　     一个事务可能包涵有一个或多个语句。
　　3、它能保证值分配的可预见性，与连续性，可重复性，这个也就保证了insert语句在复制到slave
          的时候还能生成和master那边一样的值(它保证了基于语句复制的安全)。
     4、由于在这种模式下auto_inc锁一直要保持到语句的结束，所以这个就影响到了并发的插入。

 

【1.2】consecutive(innodb_autoinc_lock_mode=1) 模式:

　　1、这一模式下去simple insert 做了优化，由于simple insert一次性插入值的个数可以立马得到
          确定，所以mysql可以一次生成几个连续的值，用于这个insert语句；总的来说这个对复制也是安全的
          (它保证了基于语句复制的安全)
　　2、这一模式也是mysql的默认模式，这个模式的好处是auto_inc锁不要一直保持到语句的结束，只要
          语句得到了相应的值后就可以提前释放锁

 

【1.3】interleaved(innodb_autoinc_lock_mode=2) 模式
　　1、由于这个模式下已经没有了auto_inc锁，所以这个模式下的性能是最好的；但是它也有一个问题，就是
          对于同一个语句来说它所得到的auto_incremant值可能不是连续的。

 

【2】如果你的二进制文件格式是mixed | row 那么这三个值中的任何一个对于你来说都是复制安全的。

　　由于现在mysql已经推荐把二进制的格式设置成row，所以在binlog_format不是statement的情况下最

　　好是innodb_autoinc_lock_mode=2 这样可能知道更好的性能。


>https://www.cnblogs.com/JiangLe/p/6362770.html
