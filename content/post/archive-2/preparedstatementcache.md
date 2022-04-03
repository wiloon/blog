---
title: PreparedStatementCache
author: "-"
date: 2016-09-22T08:00:28+00:00
url: /?p=9213
categories:
  - Uncategorized

tags:
  - reprint
---
## PreparedStatementCache
http://www.cnblogs.com/alipayhutu/archive/2013/04/18/3029171.html


如何理解PreparedStatementCache,以及如何使用

为节约键盘敲击次数,记PreparedStatement为PS, PreparedStatementCache为PSCache,并且所有的SQL使用的绑定变量。

原理: 

http://www.dbafree.net/?p=287

http://agapple.iteye.com/blog/838286

http://singleant.iteye.com/blog/1298837


使用: 

1. 使用ps.

sql里用？占位,等待被替换。例如,select * from table1 where user_name = ? and age > ?


2. 启用pscache。

<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
  
....
  
<property name="poolPreparedStatements" value="true" />
  
<property name="maxOpenPreparedStatements" value="10" />
  
....
  
</bean>
  
3. 解析后的PS缓存,与重复利用。

sql语句,被发送到DB server端,经一系列处理 (语法解析、语义解析、结构优化) ,转化为一个树型结构 (sql, string -> tree) 。

3.1 sql解析后 (string -> tree) ,如何将ps放到pscache里？

首先,澄清个概念。执行树这个不是在应用客户端的,是在oracle服务器那边,server中也有pscache.
  
再者是说,只要客户端开启了PSCache,那么CS端都会缓存住这些个树 (尽管C端维护的结构可能简单一点) 。
  
底层会缓存 (LRU替换) ,用户不用关心。
  
3.2  假如pscache中,有一棵树是select * from table1 where user_name = ? and age > ? ,现在并发来了50个线程,都要用这棵树,如何复用？

执行树是一个具体的执行步骤了,是oracle服务器底层的具体执行步骤,所以再多的并发,直接拿过来用就是了,跟并发没有很多的关系。

可以理解为一个非状态的公共方法,就可以了,多个线程直接调用,复用这个方法,不存在瓶颈。

本质上来说,是oracle底层"包揽了"。底层逻辑: 

1) 根据sql (String及参数类型等各种信息) ,计算出一个key,看它在pscache里是否存在。
  
2) 如果存在,要看能否直接使用。能就用,不能就会临时创建出一个ps给我用 (这个新的ps不会被插到pscache中,因为cache里已经有啦) 
  
3) 如果不存在,那么就创建一个ps对象,并把它放到pscache中,根据LRU规则调整下pscache.