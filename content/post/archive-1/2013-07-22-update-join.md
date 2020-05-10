---
title: update join, delete join
author: wiloon
type: post
date: 2013-07-22T04:25:34+00:00
url: /?p=5688
categories:
  - DataBase

---
[sql]
   
UPDATE t1
    
SET t1.CalculatedColumn = t2.[Calculated Column]
    
FROM dbo.Table1 AS t1
    
INNER JOIN dbo.Table2 AS t2
    
ON t1.CommonField = t2.[Common Field]
    
WHERE t1.BatchNo = &#8216;110&#8217;;
  
[/sql]

[sql]
  
DELETE a
  
from t0 a
  
JOIN t1 b
  
ON a.c0=b.c0
  
WHERE b.c1=&#8217;xxx&#8217;
  
[/sql]

http://stackoverflow.com/questions/1980738/sql-delete-with-join-another-table-for-where-condition

http://stackoverflow.com/questions/652770/delete-with-join-in-mysql/29204958#29204958