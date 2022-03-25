---
title: 'MySQL 索引  失效'
author: "-"
date: 2017-11-24T02:03:41+00:00
url: /?p=11479
categories:
  - Uncategorized

tags:
  - reprint
---
## 'MySQL 索引  失效'
http://www.jianshu.com/p/932bcdf2c89f

索引并不会时时发生,有时就算是where查询字段中添加了索引,索引也会失效,下面我们来讲讲五种索引失效的场景。

1.查询条件包含or
  
查询条件包含or时,可能会导致索引失效: 

失效索引
  
当or左右查询字段只有一个是索引,该索引失效,explain执行计划key=null；只有当or左右查询字段均为索引时,才会生效；

有效索引
  
2.组合索引,不是使用第一列索引,索引失效
  
如果select from key1=1 and key2= 2;建立组合索引 (key1,key2) ;
  
select from key1 = 1;组合索引有效；
  
select from key1 = 1 and key2= 2;组合索引有效；
  
select from key2 = 2;组合索引失效；不符合最左前缀原则

3.like 以%开头
  
使用like模糊查询,当%在前缀时,索引失效；eg: 

索引失效
  
当前缀没有%,后缀有%时,索引有效；eg: 

索引有效
  
4.如何列类型是字符串,where时一定用引号括起来,否则索引失效
  
不用引号括起来

作者: 程序猿小屌丝
  
链接: http://www.jianshu.com/p/932bcdf2c89f
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。