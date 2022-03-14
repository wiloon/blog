---
title: Oracle按时间分组统计的sql
author: "-"
date: 2015-05-27T02:50:59+00:00
url: /?p=7712
categories:
  - Uncategorized

tags:
  - reprint
---
## Oracle按时间分组统计的sql
http://www.programgo.com/article/72675408491/
  
标签: MySQL 按周统计   oracle 按季度查询   oracle date 周
  
转自: http://blog.itpub.net/9907339/viewspace-1048055/
  
oracle 实现按周,月,季度,年查询统计数据

//按自然周统计
  
select to_char(date,'iw'),sum()
  
from
  
where
  
group by to_char(date,'iw')

//按自然月统计
  
select to_char(date,'mm'),sum()
  
from
  
where
  
group by to_char(date,'mm')

//按季统计
  
select to_char(date,'q'),sum()
  
from
  
where
  
group by to_char(date,'q')

//按年统计
  
select to_char(date,'yyyy'),sum()
  
from
  
where
  
group by to_char(date,'yyyy')

Oracle 中 IW和WW 有何差别

SQL> select day,
  
2 to_char(day, 'd'),
  
3 to_char(day, 'iw'),
  
4 to_char(day, 'ww')
  
5 from (select trunc(sysdate, 'year')+level-1 as day from dual connect by level <=8)
  
6 /

DAY TO_CHAR(DAY,'D') TO_CHAR(DAY,'IW') TO_CHAR(DAY,'WW')
  
---- ------ ------ ------
  
2009-1-1 5 01 01
  
2009-1-2 6 01 01
  
2009-1-3 7 01 01
  
2009-1-4 1 01 01
  
2009-1-5 2 02 01
  
2009-1-6 3 02 01
  
2009-1-7 4 02 01
  
2009-1-8 5 02 02
  
IW: ISO标准周
  
WW: oracle标准周
  
举例: 
  
SELECT to_char(to_date('20051203','yyyymmdd'),'WW') "WW03",
  
to_char(to_date('20051203','yyyymmdd'),'IW') "IW03",
  
to_char(to_date('20051204','yyyymmdd'),'WW') "WW04",
  
to_char(to_date('20051204','yyyymmdd'),'IW') "WW04",
  
to_char(to_date('20051205','yyyymmdd'),'WW') "WW05",
  
to_char(to_date('20051205','yyyymmdd'),'IW') "WW05"
  
FROM dual;

Oracle中发现的WW和IW的规律
  
WW: 
  
每年的1月1日作为当年的第一周的第一天 (不管当年的1月1日是星期几) ；
  
比如: 2004/01/01 是周四, 在Oracle中被定义为2004年WW的第一周的第一天；
  
SELECT TO_CHAR(TO_DATE('20040101','YYYYMMDD'),'YY:WW'),TO_CHAR(TO_DATE('20040107','YYYYMMDD'),'YY:WW'),TO_CHAR(TO_DATE('20040108','YYYYMMDD'),'YY:WW') FROM DUAL;

IW : 
  
以周别为"主线" ,每年最多可以有53个周B别,但是每年至少要包含52个周别；
  
如果一年当中第52周别之后至当年的12月31日之间,还有大于或等于4天的话,则定为当年的第53周,否则剩余这些天数被归为下一年的第1周；如果在不 足52周别的话,则以下一年的时间来补；每周固定的从周一开始作为本周的第1天,到周日作为本周的第7天；比如: 在Oracle中 2006/01/01 依然属于IW周别 05年的第52周的第7天

[@more@]