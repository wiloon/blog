---
title: MySQL "ON DUPLICATE KEY UPDATE"
author: "-"
date: 2014-05-21T01:33:15+00:00
url: /?p=6643
categories:
  - Inbox
tags:
  - MySQL

---
## MySQL "ON DUPLICATE KEY UPDATE"
如果在INSERT语句末尾指定了ON DUPLICATE KEY UPDATE,并且插入行后会导致在一个UNIQUE索引或PRIMARY KEY中出现重复值,则在出现重复值的行执行UPDATE；如果不会导致唯一值列重复的问题,则插入新行。
  
例如,如果列 a 为 主键 或 拥有UNIQUE索引,并且包含值1,则以下两个语句具有相同的效果: 
  
INSERT INTO TABLE (a,c) VALUES (1,3) ON DUPLICATE KEY UPDATE c=c+1;
  
UPDATE TABLE SET c=c+1 WHERE a=1;
  
如果行作为新记录被插入,则受影响行的值显示1；如果原有的记录被更新,则受影响行的值显示2。
  
这个语法还可以这样用:
  
如果INSERT多行记录(假设 a 为主键或 a 是一个 UNIQUE索引列):
  
1.INSERT INTO TABLE (a,c) VALUES (1,3),(1,7) ON DUPLICATE KEY UPDATE c=c+1;
  
执行后, c 的值会变为 4 (第二条与第一条重复, c 在原值上+1).
  
2.INSERT INTO TABLE (a,c) VALUES (1,3),(1,7) ON DUPLICATE KEY UPDATE c=VALUES(c);
  
执行后, c 的值会变为 7 (第二条与第一条重复, c 在直接取重复的值7).
  
注意: ON DUPLICATE KEY UPDATE只是MySQL的特有语法,并不是SQL标准语法！
  
这个语法和适合用在需要 判断记录是否存在,不存在则插入存在则更新的场景.
  
可以参考语法:
