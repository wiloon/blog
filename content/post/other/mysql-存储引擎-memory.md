---
title: MySQL 存储引擎 Memory
author: "-"
date: 2015-06-28T06:19:57+00:00
url: /?p=7947
categories:
  - Uncategorized
tags:
  - MySQL

---
## MySQL 存储引擎 Memory
http://samyubw.blog.51cto.com/978243/223769


Memory存储引擎使用存在内存中的内容来创建表，每个Memory表只实际对应一个磁盘文件，在磁盘中表现为.frm文件。Memory类型的表访问速度非常快，因为它的数据是放在内存中的，并且默认使用hash索引，但是一旦服务关闭，表中的数据就会丢失。

示例: create table memory_tab(id int)engine=memory;
  
因为memory在MySQLd重启后数据就会丢失，为了获得稳定的数据源，可以在启动MySQLd时加上—init-file选项，把insert into memory_tab select 或load data infile类似的语句放进去即可。
  
另外因为memory表是把数据放到内存中的，所以服务器需要有足够的内存来维持所有在同一时间使用的memory表，注意对连接MySQLd的所有用户连接 共享 内存表中的数据，根据应用如果不是在所有连接间共享数据，最好在内存表中加入标志各个连接的ID。当不再需要memory数据时，要记得去删除自己连接的数据。
  
对于内存表的官方说明: 
  
The MEMORY storage engine creates tables with contents that are stored in memory. Formerly, these were known as HEAP tables. MEMORY is the preferred term, although HEAP remains supported for backward compatibility.
  
Each MEMORY table is associated with one disk file. The filename begins with the table name and has an extension of .frm to indicate that it stores the table definition.
  
概括将就是: 内存表把表结构存放到磁盘上，而把数据放在内存中。
  
As indicated by the name, MEMORY tables are stored in memory. They use hash indexes by default, which makes them very fast, and very useful for creating temporary tables. However, when the server shuts down, all rows stored in MEMORY tables are lost. The tables themselves continue to exist because their definitions are stored in .frm files on disk, but they are empty when the server restarts.
  
内存表的存储引擎默认使用的是hash index，速度要比使用B型树索引的MyISAM引擎快。
  
其它特性: 
  
内存表是有大小限制的，这主要取决于两个参数，一个是max_rows，另一个是max_heap_table_size.max_rows在创建表时可以指定(也可以 ALTER TABLE tbl_name MAX_ROWS= MAX_ROWS)，这样在往表中写数据时，如果写入的数据超过了规定的数目，就会报The table is full的提示，这里需要注意的是，我测试发现如果用insert into table values(xx),(yy)..这种一次带多个插入值的形式，可以插入超过max_rows数量的记录。
  
其它特性: 
  
1. heap对所有用户的连接是可见的，这使得它非常适合做缓存。
  
2. 仅适合使用的场合。heap不允许使用xxxTEXT和xxxBLOB数据类型；只允许使用=和<=>操作符来搜索记录 (不允许<、>、<=或>=) ；不支持auto_increment；只允许对非空数据列进行索引 (not null) 。
  
注: 操作符 "<=>" 说明: NULL-safe equal.这个操作符和"="操作符执行相同的比较操作，不过在两个操作码均为NULL时，其所得值为1而不为NULL，而当一个操作码为NULL时，其所得值为0而不为NULL。
  
3.HEAP表使用一个固定的记录长度格式。默认情况下max_rows依赖于max_heap_table_size.
  
4.HEAP不支持BLOB/TEXT列。

如果用过oracle的，一般类似的应用我们是用临时表来实现的，但是MySQL的临时表与oracle比有一定的不同。
  
首先MySQL创建临时表: create temporary table temp_tab(id int);
  
这里临时表默认使用的存储引擎是服务器指定的存储引擎 (默认是myisam) 。MySQL临时表的定义和数据都是放在内存中，而未放到磁盘中，用show tables是找不到临时表的。

另外，因为memory的存取速度优于myisam，在用临时表做中间表的应用时，可以将其改为使用memory引擎的临时表。


http://www.cnblogs.com/wu-jian/archive/2011/11/29/2267795.html