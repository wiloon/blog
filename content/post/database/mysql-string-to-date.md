---
title: MySQL string to date
author: "-"
date: 2011-04-16T09:44:29+00:00
url: /?p=61
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL string to date
MySQL中DATE_FORMAT(date, format)函数可根据format字符串格式化日期或日期和时间值date，返回结果串。
  
也可用DATE_FORMAT( ) 来格式化DATE 或DATETIME 值，以便得到所希望的格式。根据format字符串格式化date值:
  
下面是函数的参数说明:
  
%S, %s 两位数字形式的秒 ( 00,01, . . ., 59) 
  
%i 两位数字形式的分 ( 00,01, . . ., 59) 
  
%H 两位数字形式的小时，24 小时 (00,01, . . ., 23) 
  
%h, %I 两位数字形式的小时，12 小时 (01,02, . . ., 12) 
  
%k 数字形式的小时，24 小时 (0,1, . . ., 23) 
  
%l 数字形式的小时，12 小时 (1, 2, . . ., 12) 
  
%T 24 小时的时间形式 (hh : mm : s s) 
  
%r 12 小时的时间形式 (hh:mm:ss AM 或hh:mm:ss PM) 
  
%p AM 或P M
  
%W 一周中每一天的名称 ( Sunday, Monday, . . ., Saturday) 
  
%a 一周中每一天名称的缩写 ( Sun, Mon, . . ., Sat) 
  
%d 两位数字表示月中的天数 ( 00, 01, . . ., 31) 
  
%e 数字形式表示月中的天数 ( 1, 2， . . ., 31) 
  
%D 英文后缀表示月中的天数 ( 1st, 2nd, 3rd, . . .) 
  
%w 以数字形式表示周中的天数 ( 0 = Sunday, 1=Monday, . . ., 6=Saturday) 
  
%j 以三位数字表示年中的天数 ( 001, 002, . . ., 366) 
  
% U 周 (0, 1, 52) ，其中Sunday 为周中的第一天
  
%u 周 (0, 1, 52) ，其中Monday 为周中的第一天
  
%M 月名 (January, February, . . ., December) 
  
%b 缩写的月名 ( January, February, . . ., December) 
  
%m 两位数字表示的月份 ( 01, 02, . . ., 12) 
  
%c 数字表示的月份 ( 1, 2, . . ., 12) 
  
%Y 四位数字表示的年份
  
%y 两位数字表示的年份
  
%% 直接值"%"
  
示例:
  
select date_format(日期字段,'%Y-%m-%d') as '日期' from test
  
MySQL> SELECT DATE_FORMAT('1997-10-04 22:23:00', '%W %M %Y');
  
-> 'Saturday October 1997'
  
MySQL> SELECT DATE_FORMAT('1997-10-04 22:23:00', '%H:%i:%s');
  
-> '22:23:00'
  
MySQL> SELECT DATE_FORMAT('1997-10-04 22:23:00',
  
'%D %y %a %d %m %b %j');
  
-> '4th 97 Sat 04 10 Oct 277'
  
MySQL> SELECT DATE_FORMAT('1997-10-04 22:23:00',
  
'%H %k %I %r %T %S %w');
  
-> '22 22 10 10:23:00 PM 22:23:00 00 6'
  
MySQL> SELECT DATE_FORMAT('1999-01-01', '%X %V');
  
-> '1998 52'

在 MySQL 3.23 中，在格式修饰符前需要字符 \`%\`。在更早的 MySQL 版本中，\`%\` 是可选的。 月份与天修饰符的范围从零开始的原因是，在 MySQL 3.23 中，它允许存储不完善的日期值(例如 '2009-00-00')。