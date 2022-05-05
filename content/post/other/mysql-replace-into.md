---
title: MySQL replace into
author: "-"
date: 2015-08-14T01:52:09+00:00
url: /?p=8114
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL replace into
http://my.oschina.net/junn/blog/110213

Replace into是Insert into的增强版。在向表中插入数据时，我们经常会遇到这样的情况: 1、首先判断数据是否存在；2、如果不存在，则插入；3、如果存在，则更新。

在SQL Server中可以这样处理: 

if not exists (select 1 from t where id = 1)
  
insert into t(id, update_time) values(1, getdate())
  
else
  
update t set update_time = getdate() where id = 1

那么 MySQL 中如何实现这样的逻辑呢？MySQL 中有更简单的方法:  replace into

replace into t(id, update_time) values(1, now());

或

replace into t(id, update_time) select 1, now();

replace into 跟 insert 功能类似，不同点在于: replace into 首先尝试插入数据到表中， 1. 如果发现表中已经有此行数据 (根据主键或者唯一索引判断) 则先删除此行数据，然后插入新的数据。 2. 否则，直接插入新数据。

要注意的是: 插入数据的表必须有主键或者是唯一索引！否则的话，replace into 会直接插入数据，这将导致表中出现重复的数据。

MySQL replace into 有三种形式: 

1. replace into tbl_name(col_name, ...) values(...)

2. replace into tbl_name(col_name, ...) select ...

3. replace into tbl_name set col_name=value, ...

第一种形式类似于insert into的用法，

第二种replace select的用法也类似于insert select，这种用法并不一定要求列名匹配，事实上，MySQL甚至不关心select返回的列名，它需要的是列的位置。例如，replace into tb1(  name, title, mood) select  rname, rtitle, rmood from tb2; 这个例子使用replace into从 tb2中将所有数据导入tb1中。

第三种replace set用法类似于update set用法，使用一个例如"SET col_name = col_name + 1"的赋值，则对位于右侧的列名称的引用会被作为DEFAULT(col_name)处理。因此，该赋值相当于SET col_name = DEFAULT(col_name) + 1。

前两种形式用的多些。其中 "into" 关键字可以省略，不过最好加上 "into"，这样意思更加直观。另外，对于那些没有给予值的列，MySQL 将自动为这些列赋上默认值。
  
转帖: 另外replace into的描述
  
REPLACE的运行与INSERT很相似。只有一点例外，假如表中的一个旧记录与一个用于PRIMARY KEY或一个UNIQUE索引的新记录具有相同的值，则在新记录被插入之前，旧记录被删除。注意，除非表有一个PRIMARY KEY或UNIQUE索引，否则，使用一个REPLACE语句没有意义。该语句会与INSERT相同，因为没有索引被用于确定是否新行复制了其它的行。

所有列的值均取自在REPLACE语句中被指定的值。所有缺失的列被设置为各自的默认值，这和INSERT一样。您不能从当前行中引用值，也不能在新行中使用值。如果您使用一个例如"SET col_name = col_name + 1"的赋值，则对位于右侧的列名称的引用会被作为DEFAULT(col_name)处理。因此，该赋值相当于SET col_name = DEFAULT(col_name) + 1。为了能够使用REPLACE，您必须同时拥有表的INSERT和DELETE权限。

REPLACE语句会返回一个数，来指示受影响的行的数目。该数是被删除和被插入的行数的和。如果对于一个单行REPLACE该数为1，则一行被插入，同时没有行被删除。如果该数大于1，则在新行被插入前，有一个或多个旧行被删除。如果表包含多个唯一索引，并且新行复制了在不同的唯一索引中的不同旧行的值，则有可能是一个单一行替换了多个旧行。

受影响的行数可以容易地确定是否REPLACE只添加了一行，或者是否REPLACE也替换了其它行: 检查该数是否为1 (添加) 或更大 (替换) 。
  
1. 尝试把新行插入到表中
  
2. 当因为对于主键或唯一关键字出现重复关键字错误而造成插入失败时: 
  
a. 从表中删除含有重复关键字值的冲突行
  
b. 再次尝试把新行插入到表中

REPLACE [LOW_PRIORITY | DELAYED]
  
[INTO] tbl_name [(col_name,...)]
  
VALUES ({expr | DEFAULT},…),(…),…
  
或: 

REPLACE [LOW_PRIORITY | DELAYED]
  
[INTO] tbl_name
  
SET col_name={expr | DEFAULT}, …
  
或: 

REPLACE [LOW_PRIORITY | DELAYED]
  
[INTO] tbl_name [(col_name,...)]
  
SELECT …

REPLACE INTO \`table\` (\`unique_column\`,\`num\`) VALUES ('$unique_value',$num);跟INSERT INTO \`table\` (\`unique_column\`,\`num\`) VALUES('$unique_value',$num) ON DUPLICATE UPDATE num=$num;还是有些区别的，区别就是replace into的时候会删除老记录。如果表中有一个自增的主键。那么就要出问题了。

首先，因为新纪录与老记录的主键值不同，所以其他表中所有与本表老数据主键id建立的关联全部会被破坏。
  
其次，就是，频繁的REPLACE INTO 会造成新纪录的主键的值迅速增大。总有一天。达到最大值后就会因为数据太大溢出了。就没法再插入新纪录了。数据表满了，不是因为空间不够了，而是因为主键的值没法再增加了。