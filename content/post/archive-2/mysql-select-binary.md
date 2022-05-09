---
title: MySQL select binary
author: "-"
date: 2016-01-27T04:54:31+00:00
url: /?p=8712
categories:
  - Inbox
tags:
  - reprint
---
## MySQL select binary
BINARY不是函数,是类型转换运算符,它用来强制它后面的字符串为一个二进制字符串,可以理解为在字符串比较的时候区分大小写
  
如下: 
  
MySQL> select binary 'ABCD'='abcd' COM1, 'ABCD'='abcd' COM2;
  
+---+----+
  
| COM1 | COM2 |
  
+---+----+
  
|          0        |          1       |
  
+---+----+
  
1 row in set (0.00 sec)

____________________________________________________________
  
(仅仅有些而已！4.*以前)
  
因为有的MySQL特别是4.*以前的对于中文检索会有不准确的问题,可以在检索的时候加上binary。

建表: 

create TABLE usertest (
  
id int(9) unsigned NOT NULL auto_increment,
  
username varchar(30) NOT NULL default ",
  
primary key (id)
  
)
  
插入数据: 
  
insert into usertest (username) VALUES('美文');
  
insert into usertest (username) VALUES('美国项目');
  
insert into usertest (username) VALUES('李文');
  
insert into usertest (username) VALUES('老唐');
  
insert into usertest (username) VALUES('梦漂');
  
insert into usertest (username) VALUES('龙武');
  
insert into usertest (username) VALUES('夏');

例如: select * from usertest where username like '%夏%' ,结果七条记录都出来了,比较郁闷。

如果使用=而不是like的时候,select * from usertest where username = '夏' ,只出现一个结果。因为MySQL 的LIKE操作是按照ASCII 操作的,所以LIKE的时候是可能有问题的。问题继续: 如果再加上: 

insert into usertest (username) VALUES('文');

insert into usertest (username) VALUES('唐');

还是使用select * from usertest where username = '夏' ,结果还是出现3条记录,又郁闷了。解决办法如下: 

1.在create的时候就使用binary,而不是在query的时候加。

username varchar(30) BINARY NOT NULL default ", 如果表已经建好了,使用: 

alter table usertest modify username varchar(32) binary; 来就该表的属性。

2.在query的时候加上binary,select * from usertest where username like binary   '%夏%' ,就可以准确的查询出一条记录来。