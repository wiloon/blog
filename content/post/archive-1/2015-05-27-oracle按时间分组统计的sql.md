---
title: Oracle按时间分组统计的sql
author: wiloon
type: post
date: 2015-05-27T02:50:59+00:00
url: /?p=7712
categories:
  - Uncategorized

---
http://www.programgo.com/article/72675408491/
  
标签: mysql 按周统计   oracle 按季度查询   oracle date 周
  
转自: http://blog.itpub.net/9907339/viewspace-1048055/
  
oracle 实现按周,月,季度,年查询统计数据

//按自然周统计
  
select to_char(date,&#8217;iw&#8217;),sum()
  
from
  
where
  
group by to_char(date,&#8217;iw&#8217;)

//按自然月统计
  
select to_char(date,&#8217;mm&#8217;),sum()
  
from
  
where
  
group by to_char(date,&#8217;mm&#8217;)

//按季统计
  
select to_char(date,&#8217;q&#8217;),sum()
  
from
  
where
  
group by to_char(date,&#8217;q&#8217;)

//按年统计
  
select to_char(date,&#8217;yyyy&#8217;),sum()
  
from
  
where
  
group by to_char(date,&#8217;yyyy&#8217;)

Oracle 中 IW和WW 有何差别

SQL> select day,
  
2 to_char(day, &#8216;d&#8217;),
  
3 to_char(day, &#8216;iw&#8217;),
  
4 to_char(day, &#8216;ww&#8217;)
  
5 from (select trunc(sysdate, &#8216;year&#8217;)+level-1 as day from dual connect by level <=8)
  
6 /

DAY TO\_CHAR(DAY,&#8217;D&#8217;) TO\_CHAR(DAY,&#8217;IW&#8217;) TO_CHAR(DAY,&#8217;WW&#8217;)
  
&#8212;&#8212;&#8212;&#8211; &#8212;&#8212;&#8212;&#8212;&#8212;- &#8212;&#8212;&#8212;&#8212;&#8212;&#8211; &#8212;&#8212;&#8212;&#8212;&#8212;&#8211;
  
2009-1-1 5 01 01
  
2009-1-2 6 01 01
  
2009-1-3 7 01 01
  
2009-1-4 1 01 01
  
2009-1-5 2 02 01
  
2009-1-6 3 02 01
  
2009-1-7 4 02 01
  
2009-1-8 5 02 02
  
IW：ISO标准周
  
WW：oracle标准周
  
举例：
  
SELECT to\_char(to\_date(&#8216;20051203&#8242;,&#8217;yyyymmdd&#8217;),&#8217;WW&#8217;) &#8220;WW03&#8221;,
  
to\_char(to\_date(&#8216;20051203&#8242;,&#8217;yyyymmdd&#8217;),&#8217;IW&#8217;) &#8220;IW03&#8221;,
  
to\_char(to\_date(&#8216;20051204&#8242;,&#8217;yyyymmdd&#8217;),&#8217;WW&#8217;) &#8220;WW04&#8221;,
  
to\_char(to\_date(&#8216;20051204&#8242;,&#8217;yyyymmdd&#8217;),&#8217;IW&#8217;) &#8220;WW04&#8221;,
  
to\_char(to\_date(&#8216;20051205&#8242;,&#8217;yyyymmdd&#8217;),&#8217;WW&#8217;) &#8220;WW05&#8221;,
  
to\_char(to\_date(&#8216;20051205&#8242;,&#8217;yyyymmdd&#8217;),&#8217;IW&#8217;) &#8220;WW05&#8221;
  
FROM dual;

Oracle中发现的WW和IW的规律
  
WW：
  
每年的1月1日作为当年的第一周的第一天（不管当年的1月1日是星期几）；
  
比如：2004/01/01 是周四， 在Oracle中被定义为2004年WW的第一周的第一天；
  
SELECT TO\_CHAR(TO\_DATE(&#8216;20040101&#8242;,&#8217;YYYYMMDD&#8217;),&#8217;YY:WW&#8217;),TO\_CHAR(TO\_DATE(&#8216;20040107&#8242;,&#8217;YYYYMMDD&#8217;),&#8217;YY:WW&#8217;),TO\_CHAR(TO\_DATE(&#8216;20040108&#8242;,&#8217;YYYYMMDD&#8217;),&#8217;YY:WW&#8217;) FROM DUAL;

IW ：
  
以周别为“主线” ，每年最多可以有53个周B别，但是每年至少要包含52个周别；
  
如果一年当中第52周别之后至当年的12月31日之间，还有大于或等于4天的话，则定为当年的第53周，否则剩余这些天数被归为下一年的第1周；如果在不 足52周别的话，则以下一年的时间来补；每周固定的从周一开始作为本周的第1天，到周日作为本周的第7天；比如：在Oracle中 2006/01/01 依然属于IW周别 05年的第52周的第7天

[@more@]