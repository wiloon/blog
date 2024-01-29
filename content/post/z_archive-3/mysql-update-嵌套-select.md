---
title: MySQL update 嵌套 select
author: "-"
date: 2019-08-28T11:01:55+00:00
url: /?p=14860
categories:
  - Inbox
tags:
  - reprint
---
## MySQL update 嵌套 select
当你希望更新一批值，且值是通过select条件查询出来时，下面这个错误应该不陌生

You can't specify target table 'x' for update in FROM clause。

错误示范 1:  A B 有关联同一个key_id , 根据 B表符合条件 -> 更新A表val值。

UPDATE A a SET a.val = 2
  
WHERE a.id IN ( SELECT a.id FROM A
                  
LEFT JOIN B ON b.key_id = a.key_id
                  
WHERE b.satisfy = 1)
  
解决思路 1:  使用 INNER JOIN (最简洁)

UPDATE A a INNER JOIN B b ON b.key_id = a.key_id
  
SET a.val = 2 WHERE b.satisfy = 1
  
解决思路 2: 

UPDATE A a, (SELECT A.id from A
               
LEFT JOIN B ON B.key_id= A.key_id
               
WHERE B.satisfy = 1) b
  
SET a.val = 2
  
WHERE a.id = b.id
   
————————————————
  
版权声明: 本文为CSDN博主「InitJ」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/huanjia_h/article/details/78087994