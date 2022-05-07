---
title: MySQL collect
author: "-"
date: 2019-07-02T05:27:27+00:00
url: /?p=14604
categories:
  - Inbox
tags:
  - reprint
---
## MySQL collect
COLLATE是用来做什么的？
  
使用phpmyadmin的开发可能会非常眼熟，因为其中的中文表头已经给出了答案: 
  
phpmyadmin截图
  
所谓utf8_unicode_ci，其实是用来排序的规则。对于MySQL中那些字符类型的列，如VARCHAR，CHAR，TEXT类型的列，都需要有一个COLLATE类型来告知MySQL如何对该列进行排序和比较。简而言之，COLLATE会影响到ORDER BY语句的顺序，会影响到WHERE条件中大于小于号筛选出来的结果，会影响**DISTINCT**、**GROUP BY**、**HAVING**语句的查询结果。另外，MySQL建索引的时候，如果索引列是字符类型，也会影响索引创建，只不过这种影响我们感知不到。总之，凡是涉及到字符类型比较或排序的地方，都会和COLLATE有关。
  
各种COLLATE的区别
  
COLLATE通常是和数据编码 (CHARSET) 相关的，一般来说每种CHARSET都有多种它所支持的COLLATE，并且每种CHARSET都指定一种COLLATE为默认值。例如Latin1编码的默认COLLATE为latin1_swedish_ci，GBK编码的默认COLLATE为gbk_chinese_ci，utf8mb4编码的默认值为utf8mb4_general_ci。
  
这里顺便讲个题外话，MySQL中有utf8和utf8mb4两种编码，在MySQL中请大家忘记**utf8**，永远使用**utf8mb4**。这是MySQL的一个遗留问题，MySQL中的utf8最多只能支持3bytes长度的字符编码，对于一些需要占据4bytes的文字，MySQL的utf8就不支持了，要使用utf8mb4才行。
  
很多COLLATE都带有_ci字样，这是Case Insensitive的缩写，即大小写无关，也就是说"A"和"a"在排序和比较的时候是一视同仁的。selection * from table1 where field1="a"同样可以把field1为"A"的值选出来。与此同时，对于那些_cs后缀的COLLATE，则是Case Sensitive，即大小写敏感的。
  
在MySQL中使用show collation指令可以查看到MySQL所支持的所有COLLATE

作者: 腾讯云加社区
  
链接: https://juejin.im/post/5bfe5cc36fb9a04a082161c2
  
来源: 掘金
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
  
https://juejin.im/post/5bfe5cc36fb9a04a082161c2