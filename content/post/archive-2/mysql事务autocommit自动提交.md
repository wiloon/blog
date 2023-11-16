---
title: MySQL事务autocommit自动提交
author: "-"
date: 2016-10-26T00:53:24+00:00
url: /?p=9333
categories:
  - Inbox
tags:
  - reprint
---
## MySQL事务autocommit自动提交

[http://www.qttc.net/201208175.html](http://www.qttc.net/201208175.html)

MySQL默认操作模式就是autocommit自动提交模式。这就表示除非显式地开始一个事务,否则每个查询都被当做一个单独的事务自动执行。我们可以通过设置autocommit的值改变是否是自动提交autocommit模式。

通过以下命令可以查看当前autocommit模式
  
MySQL> show variables like 'autocommit';
  
+-----+---+
  
| Variable_name | Value |
  
+-----+---+
  
| autocommit    | ON    |
  
+-----+---+
  
1 row in set (0.04 sec)
  
从查询结果中,我们发现Value的值是ON,表示autocommit开启。我们可以通过以下SQL语句改变这个模式

MySQL> set autocommit = 0;
  
值0和OFF都是一样的,当然,1也就表示ON。通过以上设置autocommit=0,则用户将一直处于某个事务中,直到执行一条commit提交或rollback语句才会结束当前事务重新开始一个新的事务。

举个例子:

张三给李四转账500元。那么在数据库中应该是以下操作:

1,先查询张三的账户余额是否足够

2,张三的账户上减去500元

3,李四的账户上加上500元

以上三个步骤就可以放在一个事务中执行提交,要么全部执行要么全部不执行,如果一切都OK就commit提交永久性更改数据；如果出错则rollback回滚到更改前的状态。利用事务处理就不会出现张三的钱少了李四的账户却没有增加500元或者张三的钱没有减去李四的账户却加了500元。

MySQL默认的存储引擎是MyISAM,MyISAM存储引擎不支持事务处理,所以改变autocommit没有什么作用。但不会报错,所以要使用事务处理的童鞋一定要确定你所操作的表示支持事务处理的,如InnoDB。如果不知道表的存储引擎可以通过查看建表语句查看建表的时候有没有指定事务类型的存储引擎,如果没有指定存储引擎默认则是MyISAM不支持事务的存储引擎。

当然,事务处理是为了保障表数据原子性、一致性、隔离性、持久性。这些都是要消耗系统资源的,要谨慎选择。
