---
title: update join, delete join
author: "-"
date: 2013-07-22T04:25:34+00:00
url: /?p=5688
categories:
  - DataBase
tags:
  - reprint
---
## update join, delete join
```sql
   
UPDATE t1
    
SET t1.CalculatedColumn = t2.[Calculated Column]
    
FROM dbo.Table1 AS t1
    
INNER JOIN dbo.Table2 AS t2
    
ON t1.CommonField = t2.[Common Field]
    
WHERE t1.BatchNo = '110';
  
```

```sql
  
DELETE a
  
from t0 a
  
JOIN t1 b
  
ON a.c0=b.c0
  
WHERE b.c1='xxx'
  
```

http://stackoverflow.com/questions/1980738/sql-delete-with-join-another-table-for-where-condition

http://stackoverflow.com/questions/652770/delete-with-join-in-MySQL/29204958#29204958