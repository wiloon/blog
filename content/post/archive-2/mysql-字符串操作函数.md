---
title: MySQL 字符串操作函数
author: "-"
date: 2016-04-11T11:15:05.000+00:00
url: "/?p=8876"
categories:
- Uncategorized
tags:$
  - reprint
---
## MySQL 字符串操作函数
### substring
substring('sqlstudy.com', 4, 2) 从字符串的第 4 个字符位置开始取,取 2 个字符。
```sql
        -- 下标从1开始
        MySQL> select substring('sqlstudy.com', 4, 2);
        +---------------------------------+
        | substring('sqlstudy.com', 4, 2) |
        +---------------------------------+
        | st                              |
        +---------------------------------+
```

http://www.cnblogs.com/xiangxiaodong/archive/2011/02/21/1959589.html

MySQL常用字符串操作函数大全,以及实例

今天在论坛中看到一个关于MySQL的问题,问题如下

good_id     cat_id

12654         665,569

12655         601,4722

goods_id是商品id

cat_id是分类id

当我,怎么根据这种分类ID查数据 (一个商品有多个分类,而且用逗号隔开了) 

我现在用的是like 这样的话,输入一个分类id是688,或者4722都能出来这个商品,但输入一个722也出来这个商品了。

如果用like做的话,肯定会有问题的,我的开始的想法是,把cat_id里面的字符串换成数组,这样可以利用MySQL里面的in操作,这样就不会出现查找722,而4722类别下的产品都跑出来了。我从网上找了半天,这方面的字符串操作函数,没找到,不过我发现了find_in_set这个函数虽然不能,将字符串转换成数组,但是也不会出现上面的情况。我发现自己有好多函数不知道,所以我从手册中,以及网上收集了半天,做了一些例子。

一,测试准备

查看复制打印?

测试表

CREATE TABLE `string_test` (

`id` int(11) NOT NULL auto_increment COMMENT '用户ID',

`name` varchar(50) NOT NULL default " COMMENT '名称',

`job` varchar(23) NOT NULL COMMENT '工作',

`sex` tinyint(1) NOT NULL default '1' COMMENT '性别',

`hobby` varchar(100) character set utf8 collate utf8_unicode_ci default NULL COMMENT '爱好',

PRIMARY KEY  (`id`)

) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

测试数据

INSERT INTO `string_test` (`id`, `name`, `job`, `sex`, `hobby`) VALUES

(1, 'tank', '农民工', 1, '军棋,游戏,fishing'),

(2, 'zhang', 'DUCK', 0, 'fly,make firend'),

(3, 'ying', 'no job', 1, 'flying,driving,testing'),

(4, 'tankzhang', 'love your love', 1, 'i love you');

测试表

CREATE TABLE `string_test` (

`id` int(11) NOT NULL auto_increment COMMENT '用户ID',

`name` varchar(50) NOT NULL default " COMMENT '名称',

`job` varchar(23) NOT NULL COMMENT '工作',

`sex` tinyint(1) NOT NULL default '1' COMMENT '性别',

`hobby` varchar(100) character set utf8 collate utf8_unicode_ci default NULL COMMENT '爱好',

PRIMARY KEY  (`id`)

) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

测试数据

INSERT INTO `string_test` (`id`, `name`, `job`, `sex`, `hobby`) VALUES

(1, 'tank', '农民工', 1, '军棋,游戏,fishing'),

(2, 'zhang', 'DUCK', 0, 'fly,make firend'),

(3, 'ying', 'no job', 1, 'flying,driving,testing'),

(4, 'tankzhang', 'love your love', 1, 'i love you');

id

name

job

sex

hobby


tank

农民工


军棋,游戏,fishing

2

zhang

DUCK

fly,make firend

3

ying

no job


flying,driving,testing

4

tankzhang

love your love


i love you

二,MySQL字符串操作函数

1,UPPER和UCASE

返回字符串str,根据当前字符集映射(缺省是ISO-8859-1 Latin1)把所有的字符改变成大写。该函数对多字节是可靠的。

MySQL> select name,UPPER(name) from string_test where name='tank';

\+——+————-+

| name | UPPER(name) |

\+——+————-+

| tank | TANK        |

\+——+————-+

1 row in set (0.00 sec)

2,LOWER和LCASE

返回字符串str,根据当前字符集映射(缺省是ISO-8859-1 Latin1)把所有的字符改变成小写。该函数对多字节是可靠的。

MySQL> select sex,LCASE(job) from string_test where job='DUCK';

\+——+————+

| sex  | LCASE(job) |

\+——+————+

|    1 | duck       |

\+——+————+

1 row in set (0.00 sec)

3,FIND_IN_SET(str,strlist)

如果字符串str在由N子串组成的表strlist之中,返回一个1到N的值。一个字符串表是被","分隔的子串组成的一个字符串。如果第一个参数是一个常数字符串并且第二个参数是一种类型为SET的列,FIND_IN_SET()函数被优化而使用位运算！如果str不是在strlist里面或如果 strlist是空字符串,返回0。如果任何一个参数是NULL,返回NULL。如果第一个参数包含一个",",该函数将工作不正常。看面是二种不同的效果,可以看一下

MySQL> SELECT id,name FROM string_test WHERE find_in_set('fly',hobby);

\+—-+——-+

| id | name  |

\+—-+——-+

|  2 | zhang |

\+—-+——-+

1 row in set (0.00 sec)

MySQL> SELECT id,name FROM string_test WHERE hobby like 'fly%';

\+—-+——-+

| id | name  |

\+—-+——-+

|  2 | zhang |

|  3 | ying  |

\+—-+——-+

2 rows in set (0.00 sec)

4,FIELD(str,str1,str2,str3,…)

返回str在str1, str2, str3, …清单的索引。如果str没找到,返回0。FIELD()是ELT()反运算。

MySQL> SELECT id, name, FIELD( id, name, sex, job, hobby )

\-> FROM string_test where id < 4;

\+—-+——-+————————————+

| id | name  | FIELD( id, name, sex, job, hobby ) |

\+—-+——-+————————————+

|  1 | tank  |                                  2 |

|  2 | zhang |                                  0 |

|  3 | ying  |                                  0 |

\+—-+——-+————————————+

3 rows in set (0.00 sec)

5\.ELT(N,str1,str2,str3,…)

如果N= 1,返回str1,如果N= 2,返回str2,等等。如果N小于1或大于参数个数,返回NULL。ELT()是FIELD()反运算。

MySQL> SELECT id, name, ELT(1, id, name, sex, job, hobby ) FROM string_test where id < 4;

\+—-+——-+————————————+

| id | name  | ELT(1, id, name, sex, job, hobby ) |

\+—-+——-+————————————+

|  1 | tank  | 1                                  |

|  2 | zhang | 2                                  |

|  3 | ying  | 3                                  |

\+—-+——-+————————————+

3 rows in set (0.00 sec)

MySQL> SELECT id, name, ELT(2, id, name, sex, job, hobby ) FROM string_test where id < 4;

\+—-+——-+————————————+

| id | name  | ELT(2, id, name, sex, job, hobby ) |

\+—-+——-+————————————+

|  1 | tank  | tank                               |

|  2 | zhang | zhang                              |

|  3 | ying  | ying                               |

\+—-+——-+————————————+

3 rows in set (0.00 sec)

6,REPLACE(str,from_str,to_str)

返回字符串str,其字符串from_str的所有出现由字符串to_str代替。

MySQL> SELECT id,REPLACE(hobby,"firend",'living') FROM string_test WHERE id = 2;

\+—-+———————————-+

| id | REPLACE(hobby,"firend",'living') |

\+—-+———————————-+

|  2 | fly,make living                  |

\+—-+———————————-+

1 row in set (0.00 sec)

7,REPEAT(str,count)

返回由重复countTimes次的字符串str组成的一个字符串。如果count <= 0,返回一个空字符串。如果str或count是NULL,返回NULL。

MySQL> SELECT id,REPEAT(name,2) FROM string_test WHERE id > 1 and id < 4;

\+—-+—————-+

| id | REPEAT(name,2) |

\+—-+—————-+

|  2 | zhangzhang     |

|  3 | yingying       |

\+—-+—————-+

2 rows in set (0.00 sec)

8,REVERSE(str)

返回颠倒字符顺序的字符串str。

MySQL> SELECT id,reverse(name) FROM string_test WHERE id > 1 and id < 4;

\+—-+—————+

| id | reverse(name) |

\+—-+—————+

|  2 | gnahz         |

|  3 | gniy          |

\+—-+—————+

2 rows in set (0.00 sec)

9,INSERT(str,pos,len,newstr)

返回字符串str,在位置pos起始的子串且len个字符长得子串由字符串newstr代替。

MySQL> select id,name,INSERT(hobby,10,6,'living') from string_test where id = 2;

\+—-+——-+—————————–+

| id | name  | INSERT(hobby,10,6,'living') |

\+—-+——-+—————————–+

|  2 | zhang | fly,make living             |

\+—-+——-+—————————–+

1 row in set (0.00 sec)

10,SUBSTRING(str FROM pos)

从字符串str的起始位置pos返回一个子串。下面的sub2没有值,因为MySQL数据库的下标是从1开始的。

MySQL> SELECT id, substring( hobby, 1, 6) AS sub1, substring( hobby from 0 for 8

) AS sub2,substring( hobby,2) AS sub3, substring( hobby from 4 ) AS sub4 FROM s

tring_test WHERE id =4;

\+—-+——–+——+———–+———+

| id | sub1   | sub2 | sub3      | sub4    |

\+—-+——–+——+———–+———+

|  4 | i love |      |  love you | ove you |

\+—-+——–+——+———–+———+

1 row in set (0.00 sec)

11,SUBSTRING_INDEX(str,delim,count)

返回从字符串str的第count个出现的分隔符delim之后的子串。如果count是正数,返回最后的分隔符到左边(从左边数) 的所有字符。如果count是负数,返回最后的分隔符到右边的所有字符(从右边数)。

MySQL> SELECT id,SUBSTRING_INDEX(hobby,',',2) as test1,SUBSTRING_INDEX(hobby,','

,-1) as test2 FROM string_test WHERE id = 3;

\+—-+—————-+———+

| id | test1          | test2   |

\+—-+—————-+———+

|  3 | flying,driving | testing |

\+—-+—————-+———+

1 row in set (0.01 sec)

12,LTRIM(str)

返回删除了其前置空格字符的字符串str。

MySQL> SELECT id,LTRIM(job) FROM string_test WHERE id = 4;

\+—-+—————-+

| id | LTRIM(job)     |

\+—-+—————-+

|  4 | love your love |

\+—-+—————-+

1 row in set (0.00 sec)

13,RTRIM(str)

返回删除了其拖后空格字符的字符串str。

MySQL> SELECT id,RTRIM(job) FROM string_test WHERE id = 4;

\+—-+—————-+

| id | RTRIM(job)     |

\+—-+—————-+

|  4 | love your love |

\+—-+—————-+

1 row in set (0.00 sec)

14,TRIM([[BOTH | LEADING | TRAILING] [remstr] FROM] str)

返回字符串str,其所有remstr前缀或后缀被删除了。如果没有修饰符BOTH、LEADING或TRAILING给出,BOTH被假定。如果remstr没被指定,空格被删除。

MySQL> select trim(' test  ');

\+—————–+

| trim(' test  ') |

\+—————–+

| test            |

\+—————–+

1 row in set (0.01 sec)

MySQL> SELECT id,TRIM(LEADING "love" from job) as test1,TRIM(BOTH "love" from jo

b) as test2,TRIM(TRAILING "love" from job) as test3 FROM string_test WHERE id =

4

\-> ;

\+—-+————+——–+————+

| id | test1      | test2  | test3      |

\+—-+————+——–+————+

|  4 |  your love |  your  | love your  |

\+—-+————+——–+————+

1 row in set (0.00 sec)

15,MID(str,pos,len)

从字符串str返回一个len个字符的子串,从位置pos开始。使用FROM的变种形式是ANSI SQL92语法。

MySQL>  SELECT id, mid( hobby, 1, 6 ) AS sub1, mid( hobby

\-> FROM 0

\-> FOR 8 ) AS sub2, mid( hobby, 2 ) AS sub3, mid( hobby

\-> FROM 4 ) AS sub4

\-> FROM string_test

\-> WHERE id =4 ;

\+—-+——–+——+———–+———+

| id | sub1   | sub2 | sub3      | sub4    |

\+—-+——–+——+———–+———+

|  4 | i love |      |  love you | ove you |

\+—-+——–+——+———–+———+

1 row in set (0.00 sec)

MySQL>

16,LPAD(str,len,padstr)

返回字符串str,左面用字符串padstr填补直到str是len个字符长。

MySQL> SELECT id,LPAD(name,11,"zhang ") FROM string_test WHERE id = 3;

\+—-+————————+

| id | LPAD(name,11,"zhang ") |

\+—-+————————+

|  3 | zhang zying            |

\+—-+————————+

1 row in set (0.00 sec)

17,RPAD(str,len,padstr)

返回字符串str,右面用字符串padstr填补直到str是len个字符长。

MySQL> SELECT id,RPAD(name,11," ying") FROM string_test WHERE id = 2;

\+—-+———————–+

| id | RPAD(name,11," ying") |

\+—-+———————–+

|  2 | zhang ying            |

\+—-+———————–+

1 row in set (0.00 sec)

18,LEFT(str,len)

返回字符串str的最左面len个字符。

MySQL> SELECT id,left(job,4) FROM string_test WHERE id = 4;

\+—-+————-+

| id | left(job,4) |

\+—-+————-+

|  4 | love        |

\+—-+————-+

1 row in set (0.00 sec)

19,RIGHT(str,len)

返回字符串str的最右面len个字符。

MySQL> SELECT id,right(job,4) FROM string_test WHERE id = 4;

\+—-+————–+

| id | right(job,4) |

\+—-+————–+

|  4 | love         |

\+—-+————–+

1 row in set (0.00 sec)

20,位置控制函数

POSITION(substr IN str)

返回子串substr在字符串str第一个出现的位置,如果substr不是在str里面,返回0.

LOCATE(substr,str,pos)

返回子串substr在字符串str第一个出现的位置,从位置pos开始。如果substr不是在str里面,返回0。

INSTR(str,substr)

返回子串substr在字符串str中的第一个出现的位置。这与有2个参数形式的LOCATE()相同,除了参数被颠倒。

MySQL> SELECT id,INSTR(job,"you") as instr,LOCATE('love',job,3) as locate,POSITI

ON('love' in job) as position FROM string_test WHERE id = 4;

\+—-+——-+——–+———-+

| id | instr | locate | position |

\+—-+——-+——–+———-+

|  4 |     6 |     11 |        1 |

\+—-+——-+——–+———-+

1 row in set (0.00 sec)

21,得到字符串长度的函数

LENGTH(str),OCTET_LENGTH(str),CHAR_LENGTH(str),CHARACTER_LENGTH(str)

MySQL> SELECT id,LENGTH(job) as one,OCTET_LENGTH(job) as two,CHAR_LENGTH(job) as

three,CHARACTER_LENGTH(job) as four FROM string_test WHERE id = 4;

\+—-+—–+—–+——-+——+

| id | one | two | three | four |

\+—-+—–+—–+——-+——+

|  4 |  14 |  14 |    14 |   14 |

\+—-+—–+—–+——-+——+

1 row in set (0.00 sec)

22,合并多个字符串,或者表中的多个字段

CONCAT(str1,str2,…)

返回来自于参数连结的字符串。如果任何参数是NULL,返回NULL。可以有超过2个的参数。一个数字参数被变换为等价的字符串形式。

MySQL> SELECT id,CONCAT(name,job,hobby) FROM string_test WHERE id = 4;

\+—-+———————————–+

| id | CONCAT(name,job,hobby)            |

\+—-+———————————–+

|  4 | tankzhanglove your lovei love you |

\+—-+———————————–+

1 row in set (0.00 sec)

23,进制转换

BIN(N)

返回二进制值N的一个字符串表示,在此N是一个长整数(BIGINT)数字,这等价于CONV(N,10,2)。如果N是NULL,返回NULL。

OCT(N)

返回八进制值N的一个字符串的表示,在此N是一个长整型数字,这等价于CONV(N,10,8)。如果N是NULL,返回NULL。

HEX(N)

返回十六进制值N一个字符串的表示,在此N是一个长整型(BIGINT)数字,这等价于CONV(N,10,16)。如果N是NULL,返回NULL。

ASCII(str)

返回字符串str的最左面字符的ASCII代码值。如果str是空字符串,返回0。如果str是NULL,返回NULL。

MySQL> select bin(20),oct(20),hex(20),ascii(20);

\+———+———+———+———–+

| bin(20) | oct(20) | hex(20) | ascii(20) |

\+———+———+———+———–+

| 10100   | 24      | 14      |        50 |

\+———+———+———+———–+

1 row in set (0.02 sec)

上面我只例举了一部分对字符串进行操作的函数,并且是我觉得我们平时会用的,有可能会用到的一些函数。