---
title: 'MySQL 字符串连接  CONCAT()'
author: "-"
date: 2014-01-16T05:03:31+00:00
url: /?p=6221
categories:
  - Inbox
tags:
  - MySQL

---
## 'MySQL 字符串连接  CONCAT()'
```sql
  
MySQL> SELECT CONCAT('My', 'S', 'QL');
  
-> 'MySQL'
  
```

MySQL CONCAT () 函数用于将多个字符串连接成一个字符串

MySQL CONCAT(str1,str2,…)
  
返回结果为连接参数产生的字符串。如有任何一个参数为NULL ,则返回值为 NULL。或许有一个或多个参数。 如果所有参数均为非二进制字符串,则结果为非二进制字符串。 如果自变量中含有任一二进制字符串,则结果为一个二进制字符串。一个数字参数被转化为与之相等的二进制字符串格式；若要避免这种情况,可使用显式类型 cast, 例如:  SELECT CONCAT(CAST(int_col AS CHAR), char_col)

MySQL> SELECT CONCAT('My', 'S', 'QL');

-> 'MySQL'

MySQL> SELECT CONCAT('My', NULL, 'QL');

-> NULL

MySQL> SELECT CONCAT(14.3);

-> '14.3′

MySQL CONCAT_WS(separator,str1,str2,…)
  
CONCAT_WS() 代表 CONCAT With Separator ,是CONCAT()的特殊形式。 第一个参数是其它参数的分隔符。分隔符的位置放在要连接的两个字符串之间。分隔符可以是一个字符串,也可以是其它参数。如果分隔符为 NULL,则结果为 NULL。函数会忽略任何分隔符参数后的 NULL 值。

MySQL> SELECT CONCAT_WS(',','First name','Second name','Last Name');

-> 'First name,Second name,Last Name'

MySQL> SELECT CONCAT_WS(',','First name',NULL,'Last Name');

-> 'First name,Last Name'

MySQL CONCAT_WS()不会忽略任何空字符串。 (然而会忽略所有的 NULL) 。

http://database.51cto.com/art/201010/229188.htm