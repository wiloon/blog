---
title: 左外连接，右外连接，全连接，内连接
author: "-"
date: 2013-03-20T14:39:45+00:00
url: /?p=5326
categories:
  - DataBase
tags:
  - reprint
---
## 左外连接，右外连接，全连接，内连接, left join, right join

外联接: 外联接可以是左向外联接、右向外联接或完整外部联接。
  
在 FROM 子句中指定外联接时，可以由下列几组关键字中的一组指定: 

LEFT JOIN 或 LEFT OUTER JOIN, SQL 标准允许省略 OUTER 关键字，因此 LEFT JOIN 已经足够明确。
  
左向外联接的结果集包括 LEFT OUTER 子句中指定的左表的所有行，而不仅仅是联接列所匹配的行。
如果左表的某行在右表中没有匹配行，则在相关联的结果集行中右表的所有选择列表列均为空值。

RIGHT JOIN 或 RIGHT OUTER JOIN。
  
右向外联接是左向外联接的反向联接。将返回右表的所有行。如果右表的某行在左表中没有匹配行，则将为左表返回空值。

FULL JOIN 或 FULL OUTER JOIN。
  
完整外部联接返回左表和右表中的所有行。当某行在另一个表中没有匹配行时，则另一个表的选择列表列包含空值。如果表之间有匹配行，则整个结果集行包含基表的数据值。

仅当至少有一个同属于两表的行符合联接条件时，内联接才返回行。内联接消除与另一个表中的任何行不匹配的行。而外联接会返回 FROM 子句中提到的至少一个表或视图的所有行，只要这些行符合任何 WHERE 或 HAVING 搜索条件。将检索通过左向外联接引用的左表的所有行，以及通过右向外联接引用的右表的所有行。完整外部联接中两个表的所有行都将返回。

Microsoft&reg; SQL Server  2000 对在 FROM 子句中指定的外联接使用以下 SQL-92 关键字: 

LEFT OUTER JOIN 或 LEFT JOIN

RIGHT OUTER JOIN 或 RIGHT JOIN

FULL OUTER JOIN 或 FULL JOIN
  
SQL Server 支持 SQL-92 外联接语法，以及在 WHERE 子句中使用 _= 和 =_ 运算符指定外联接的旧式语法。由于 SQL-92 语法不容易产生歧义，而旧式 Transact-SQL 外联接有时会产生歧义，因此建议使用 SQL-92 语法。

使用左向外联接
  
假设在 city 列上联接 authors 表和 publishers 表。结果只显示在出版商所在城市居住的作者 (本例中为 Abraham Bennet 和 Cheryl Carson) 。

若要在结果中包括所有的作者，而不管出版商是否住在同一个城市，请使用 SQL-92 左向外联接。下面是 Transact-SQL 左向外联接的查询和结果: 

USE pubs
  
SELECT a.au_fname, a.au_lname, p.pub_name
  
FROM authors a LEFT OUTER JOIN publishers p
  
ON a.city = p.city
  
ORDER BY p.pub_name ASC, a.au_lname ASC, a.au_fname ASC

下面是结果集: 

au_fname au_lname pub_name

* * *

Reginald Blotchet-Halls NULL
  
Michel DeFrance NULL
  
Innes del Castillo NULL
  
Ann Dull NULL
  
Marjorie Green NULL
  
Morningstar Greene NULL
  
Burt Gringlesby NULL
  
Sheryl Hunter NULL
  
Livia Karsen NULL
  
Charlene Locksley NULL
  
Stearns MacFeather NULL
  
Heather McBadden NULL
  
Michael O'Leary NULL
  
Sylvia Panteley NULL
  
Albert Ringer NULL
  
Anne Ringer NULL
  
Meander Smith NULL
  
Dean Straight NULL
  
Dirk Stringer NULL
  
Johnson White NULL
  
Akiko Yokomoto NULL
  
Abraham Bennet Algodata Infosystems
  
Cheryl Carson Algodata Infosystems

(23 row(s) affected)

不管是否与 publishers 表中的 city 列匹配，LEFT OUTER JOIN 均会在结果中包含 authors 表的所有行。注意: 结果中所列的大多数作者都没有相匹配的数据,因此，这些行的 pub_name 列包含空值。

使用右向外联接
  
假设在 city 列上联接 authors 表和 publishers 表。结果只显示在出版商所在城市居住的作者 (本例中为 Abraham Bennet 和 Cheryl Carson) 。SQL-92 右向外联接运算符 RIGHT OUTER JOIN 指明: 不管第一个表中是否有匹配的数据，结果将包含第二个表中的所有行。

若要在结果中包括所有的出版商，而不管城市中是否还有出版商居住，请使用 SQL-92 右向外联接。下面是 Transact-SQL 右向外联接的查询和结果: 

USE pubs
  
SELECT a.au_fname, a.au_lname, p.pub_name
  
FROM authors AS a RIGHT OUTER JOIN publishers AS p
  
ON a.city = p.city
  
ORDER BY p.pub_name ASC, a.au_lname ASC, a.au_fname ASC

下面是结果集: 

au_fname au_lname pub_name

* * *

Abraham Bennet Algodata Infosystems
  
Cheryl Carson Algodata Infosystems
  
NULL NULL Binnet & Hardley
  
NULL NULL Five Lakes Publishing
  
NULL NULL GGG&G
  
NULL NULL Lucerne Publishing
  
NULL NULL New Moon Books
  
NULL NULL Ramona Publishers
  
NULL NULL Scootney Books

(9 row(s) affected)

使用谓词 (如将联接与常量比较) 可以进一步限制外联接。下例包含相同的右向外联接，但消除销售量低于 50 本的书籍的书名: 

USE pubs
  
SELECT s.stor_id, s.qty, t.title
  
FROM sales s RIGHT OUTER JOIN titles t
  
ON s.title_id = t.title_id
  
AND s.qty > 50
  
ORDER BY s.stor_id ASC

下面是结果集: 

stor_id qty title

* * *

(null) (null) But Is It User Friendly?
  
(null) (null) Computer Phobic AND Non-Phobic Individuals: Behavior
  
Variations
  
(null) (null) Cooking with Computers: Surreptitious Balance Sheets
  
(null) (null) Emotional Security: A New Algorithm
  
(null) (null) Fifty Years in Buckingham Palace Kitchens
  
7066 75 Is Anger the Enemy?
  
(null) (null) Life Without Fear
  
(null) (null) Net Etiquette
  
(null) (null) Onions, Leeks, and Garlic: Cooking Secrets of the
  
Mediterranean
  
(null) (null) Prolonged Data Deprivation: Four Case Studies
  
(null) (null) Secrets of Silicon Valley
  
(null) (null) Silicon Valley Gastronomic Treats
  
(null) (null) Straight Talk About Computers
  
(null) (null) Sushi, Anyone?
  
(null) (null) The Busy Executive's Database Guide
  
(null) (null) The Gourmet Microwave
  
(null) (null) The Psychology of Computer Cooking
  
(null) (null) You Can Combat Computer Stress!

(18 row(s) affected)

有关谓词的更多信息，请参见 WHERE。

使用完整外部联接
  
若要通过在联接结果中包括不匹配的行保留不匹配信息，请使用完整外部联接。Microsoft&reg; SQL Server  2000 提供完整外部联接运算符 FULL OUTER JOIN，不管另一个表是否有匹配的值，此运算符都包括两个表中的所有行。

假设在 city 列上联接 authors 表和 publishers 表。结果只显示在出版商所在城市居住的作者 (本例中为 Abraham Bennet 和 Cheryl Carson) 。SQL-92 FULL OUTER JOIN 运算符指明: 不管表中是否有匹配的数据，结果将包括两个表中的所有行。

若要在结果中包括所有作者和出版商，而不管城市中是否有出版商或者出版商是否住在同一个城市，请使用完整外部联接。下面是 Transact-SQL 完整外部联接的查询和结果: 

USE pubs
  
SELECT a.au_fname, a.au_lname, p.pub_name
  
FROM authors a FULL OUTER JOIN publishers p
  
ON a.city = p.city
  
ORDER BY p.pub_name ASC, a.au_lname ASC, a.au_fname ASC

下面是结果集: 

au_fname au_lname pub_name

* * *

Reginald Blotchet-Halls NULL
  
Michel DeFrance NULL
  
Innes del Castillo NULL
  
Ann Dull NULL
  
Marjorie Green NULL
  
Morningstar Greene NULL
  
Burt Gringlesby NULL
  
Sheryl Hunter NULL
  
Livia Karsen NULL
  
Charlene Locksley NULL
  
Stearns MacFeather NULL
  
Heather McBadden NULL
  
Michael O'Leary NULL
  
Sylvia Panteley NULL
  
Albert Ringer NULL
  
Anne Ringer NULL
  
Meander Smith NULL
  
Dean Straight NULL
  
Dirk Stringer NULL
  
Johnson White NULL
  
Akiko Yokomoto NULL
  
Abraham Bennet Algodata Infosystems
  
Cheryl Carson Algodata Infosystems
  
NULL NULL Binnet & Hardley
  
NULL NULL Five Lakes Publishing
  
NULL NULL GGG&G
  
NULL NULL Lucerne Publishing
  
NULL NULL New Moon Books
  
NULL NULL Ramona Publishers
  
NULL NULL Scootney Books

(30 row(s) affected)