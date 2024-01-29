---
title: MySQL update in
author: "-"
date: 2019-08-29T02:33:10+00:00
url: /?p=14866
categories:
  - inbox
tags:
  - reprint
---
## MySQL update in
```sql
EXPLAIN
UPDATE table0 w SET
 w.field0 ='foo'
WHERE 
 (w.key0,w.key1,w.) IN
 (
SELECT a.* FROM (
SELECT w1.key0,w1.key1,w1.key2
FROM table0 w1
WHERE w1.field0 IS NULL AND  w1.key2=0
LIMIT 10) AS a  );

```

```sql
EXPLAIN
UPDATE table0 w0
JOIN (SELECT *FROM table0 w1 WHERE w1.field0 IS NULL AND w1.key0=0 LIMIT 10) w2 
ON w0.key0=w2.key0 AND w0.key1=w2.key1 AND w0.key2=w2.key2 
SET w0.field0='foo'

```