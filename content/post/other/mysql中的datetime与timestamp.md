---
title: MySQL中的datetime与timestamp
author: "-"
date: 2014-05-07T01:46:29+00:00
url: /?p=6592
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL中的datetime与timestamp
相同

显示

TIMESTAMP列的显示格式与DATETIME列相同。换句话说,显示宽度固定在19字符,并且格式为YYYY-MM-DD HH:MM:SS。

不同

范围

datetime 以'YYYY-MM-DD HH:MM:SS'格式检索和显示DATETIME值。支持的范围为'1000-01-01 00:00:00'到'9999-12-31 23:59:59'TIMESTAMP值不能早于1970或晚于2037

储存

TIMESTAMP

1.4个字节储存 (Time stamp value is stored in 4 bytes) 

2.值以UTC格式保存 ( it stores the number of milliseconds) 

3.时区转化 ,存储时对当前的时区进行转换,检索时再转换回当前的时区。

datetime

1.8个字节储存 (8 bytes storage) 

2.实际格式储存 (Just stores what you have stored and retrieves the same thing which you have stored.) 

3.与时区无关 (It has nothing to deal with the TIMEZONE and Conversion.) 

实例对比

现在我来做个时区对他们的影响。

1.先插入一个数据insert into \`t8\` values(now(), now());

2.改变客户端时区 (东9区,日本时区) 。

3.再次显示插入的数据,变化了,timestamp类型的数据 增加了 1个小时
  
接下来 讨论一些timestamp 的其他的属性

1.null 是否为空

timestamp 默认允许为 "非空" (not null by default) , 如果你在定义"ts TIMESTAMP DEFAULT NULL" 是非法的。 可以指定为空 null ,"ts TIMESTAMP NULL" ,这时可以在添加语句改变默认值。

ts2 TIMESTAMP NULL DEFAULT 0,
  
ts3 TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
  
default (一个表中只能有一个列选择下面其中一种)

default CURRENT_TIMESTAMP
  
default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

ON UPDATE CURRENT_TIMESTAMP

ON UPDATE 见上2

http://database.51cto.com/art/200905/124240.htm

