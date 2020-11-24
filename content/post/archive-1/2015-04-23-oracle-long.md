---
title: Oracle LONG
author: w1100n
type: post
date: 2015-04-23T01:46:24+00:00
url: /?p=7483
categories:
  - Uncategorized

---
http://www.360doc.com/content/14/1011/23/10042054_416198756.shtml


本文主要介绍的是Oracle数据库的类型LONG，我们都知道LONG 数据类型中的存储是可以改变长字符串的，其改变的最大的长度限制是2GB。以下的文章主要是对Oracle数据库的类型的相关内容的介绍望你会有所收获。

LONGxina对于超出一定长度的文本，基本只能用LONG类型来存储，数据字典中很多对象的定义就是用LONG来存储的。


1、LONG 数据类型中存储的是可变长字符串，最大长度限制是2GB。


2、对于超出一定长度的文本，基本只能用Oracle数据库里LONG类型来存储，数据字典中很多对象的定义就是用LONG来存储的。


3、LONG类型主要用于不需要作字符串搜索的长串数据，如果要进行字符搜索就要用varchar2类型。


4、很多工具，包括SQL*Plus，处理LONG 数据类型都是很困难的。


5、LONG 数据类型的使用中，要受限于磁盘的大小。


能够操作 LONG 的 SQL 语句：


1、Select语句


2、Update语句中的SET语句


3、Insert语句中的VALUES语句


限制：


1、一个表中只能包含一个 LONG 类型的列。


2、不能索引Oracle数据库里LONG类型列。


3、不能将含有LONG类型列的表作聚簇。


4、不能在SQL*Plus中将LONG类型列的数值插入到另一个表格中,如insert into …select。


5、不能在SQL*Plus中通过查询其他表的方式来创建LONG类型列,如create table as select。


6、不能对LONG类型列加约束条件（NULL、NOT NULL、DEFAULT除外），如：关键字列(PRIMARY KEY)不能是 LONG 数据类型。


7、LONG类型列不能用在Select的以下子句中：where、group by、order by，以及带有distinct的select语句中。


8、LONG类型列不能用于分布查询。


9、PL/SQL过程块的变量不能定义为LONG类型。


10、Oracle数据库里LONG类型列不能被SQL函数所改变，如：substr、instr。