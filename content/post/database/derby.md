---
title: Derby
author: "-"
date: 2011-09-22T09:27:58+00:00
url: /?p=858
categories:
  - DataBase
tags:
  - Database
  - Derby
  - Java

---
## Derby
Apache Derby, an Apache DB subproject, is an open source relational database implemented entirely in Java and available under the Apache License, Version 2.0. Some key advantages include:

Derby has a small footprint - about 2.6 megabytes for the base engine and embedded JDBC driver.
  
Derby is based on the Java, JDBC, and SQL standards.
  
Derby provides an embedded JDBC driver that lets you embed Derby in any Java-based solution.
  
Derby also supports the more familiar client/server mode with the Derby Network Client JDBC driver and Derby Network Server.
  
Derby is easy to install, deploy, and use.

Java DB is Oracle's supported distribution of the Apache Derby open source database. It supports standard ANSI/ISO SQL through the JDBC and Java EE APIs. Java DB is included in the JDK.

### At a Glance

  * Full-featured and easy-to-use
  * Transaction-protected and crash-recoverable
  * Embeddable in applications
  * Pure Java and portable and across CDC FP 1.1, Java 5, Java 6, and Java 7 (everywhere from tablets to mainframes)
  * Included in the JDK
  * Compact (2.6 MB)

新安装了 JDK 6 的程序员们也许会发现，除了传统的 bin、jre 等目录，JDK 6 新增了一个名为 db 的目录。这便是 Java 6 的新成员: Java DB。这是一个纯 Java 实现、开源的数据库管理系统 (DBMS) ，源于 Apache 软件基金会 (ASF) 名下的项目 Derby。它只有 2MB 大小，对比动辄上 G 的数据库来说可谓袖珍。但这并不妨碍 Derby 功能齐备，支持几乎大部分的数据库应用所需要的特性。更难能可贵的是，依托于 ASF 强大的社区力量，Derby 得到了包括 IBM 和 Sun 等大公司以及全世界优秀程序员们的支持。这也难怪 Sun 公司会选择其 10.2.2 版本纳入到 JDK 6 中，作为内嵌的数据库。这就好像为 JDK 注入了一股全新的活力: Java 程序员不再需要耗费大量精力安装和配置数据库，就能进行安全、易用、标准、并且免费的数据库编程。在这一章中，我们将初窥 Java DB 的世界，来探究如何使用它编写出功能丰富的程序。


**创建数据库、创建表、向表插入数据、查询表**

**数据库创建、连接
  
** **
  
** ij> connect 'jdbc:derby:myderby;create=true';
  
这句话的意思是连接到这个数据库，该数据库不存在就创建一个

ij> connect 'jdbc:derby:myderby';
  
这是连接到这个数据库

**创建表: **

create table firsttable(id int primary key, name varchar(20));

**插入数据: **

insert into firsttable values(1, 'wahaha');

**查询表: **

select * from firsttable;

**结果如下: **

ID         |NAME
  
——————————–
  
1          |wahaha

**其它命令**
  
断开连接: 
  
ij> disconnect;
  
退出ij: 
  
ij> exit;


<http://itmingong.iteye.com/blog/1338722>

<http://www.oracle.com/technetwork/java/javadb/overview/index.html>