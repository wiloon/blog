---
title: MySQL 存储引擎
author: "-"
date: 2015-06-28T05:52:57+00:00
url: /?p=7943
categories:
  - db
tags:
  - MySQL

---
## MySQL 存储引擎
## 什么是存储引擎？
关系数据库表是用于存储和组织信息的数据结构，可以将表理解为由行和列组成的表格，类似于Excel的电子表格的形式。有的表简单，有的表复杂，有的表根本不用来存储任何长期的数据，有的表读取时非常快，但是插入数据时去很差；而我们在实际开发过程中，就可能需要各种各样的表，不同的表，就意味着存储不同类型的数据，数据的处理上也会存在着差异，那么。对于MySQL来说，它提供了很多种类型的存储引擎，我们可以根据对数据处理的需求，选择不同的存储引擎，从而最大限度的利用MySQL强大的功能。这篇博文将总结和分析各个引擎的特点，以及适用场合，并不会纠结于更深层次的东西。我的学习方法是先学会用，懂得怎么用，再去知道到底是如何能用的。下面就对MySQL支持的存储引擎进行简单的介绍。

### MyISAM

MyISAM 发音为 "my-z[ei]m";

在MySQL客户端中，使用以下命令可以查看MySQL支持的引擎:show engines;

MyISAM表是独立于操作系统的，这说明可以轻松地将其从Windows服务器移植到Linux服务器；每当我们建立一个MyISAM引擎的表时，就会在本地磁盘上建立三个文件，文件名就是表明。例如，我建立了一个MyISAM引擎的tb_Demo表，那么就会生成以下三个文件: 

  * tb_demo.frm，存储表定义；
  * tb_demo.MYD，存储数据；
  * tb_demo.MYI，存储索引。

MyISAM表无法处理事务，这就意味着有事务处理需求的表，不能使用MyISAM存储引擎。MyISAM存储引擎特别适合在以下几种情况下使用: 

  * 选择密集型的表。MyISAM存储引擎在筛选大量数据时非常迅速，这是它最突出的优点。
  * 插入密集型的表。MyISAM的并发插入特性允许同时选择和插入数据。例如: MyISAM存储引擎很适合管理邮件或Web服务器日志数据。

### InnoDB

InnoDB是一个健壮的事务型存储引擎，这种存储引擎已经被很多互联网公司使用，为用户操作非常大的数据存储提供了一个强大的解决方案。我的电脑上安装的MySQL 5.6.13版，InnoDB就是作为默认的存储引擎。InnoDB还引入了行级锁定和外键约束，在以下场合下，使用InnoDB是最理想的选择: 

  * 更新密集的表。InnoDB存储引擎特别适合处理多重并发的更新请求。
  * 事务。InnoDB存储引擎是支持事务的标准MySQL存储引擎。
  * 自动灾难恢复。与其它存储引擎不同，InnoDB表能够自动从灾难中恢复。
  * 外键约束。MySQL支持外键的存储引擎只有InnoDB。
  * 支持自动增加列AUTO_INCREMENT属性。

一般来说，如果需要事务支持，并且有较高的并发读取频率，InnoDB是不错的选择。

### MEMORY

使用MySQL Memory存储引擎的出发点是速度。为得到最快的响应时间，采用的逻辑存储介质是系统内存。虽然在内存中存储表数据确实会提供很高的性能，但当MySQLd守护进程崩溃时，所有的Memory数据都会丢失。获得速度的同时也带来了一些缺陷。它要求存储在Memory数据表里的数据使用的是长度不变的格式，这意味着不能使用BLOB和TEXT这样的长度可变的数据类型，VARCHAR是一种长度可变的类型，但因为它在MySQL内部当做长度固定不变的CHAR类型，所以可以使用。

一般在以下几种情况下使用Memory存储引擎: 

  * 目标数据较小，而且被非常频繁地访问。在内存中存放数据，所以会造成内存的使用，可以通过参数max_heap_table_size控制Memory表的大小，设置此参数，就可以限制Memory表的最大大小。
  * 如果数据是临时的，而且要求必须立即可用，那么就可以存放在内存表中。
  * 存储在Memory表中的数据如果突然丢失，不会对应用服务产生实质的负面影响。

Memory同时支持散列索引和B树索引。B树索引的优于散列索引的是，可以使用部分查询和通配查询，也可以使用<、>和>=等操作符方便数据挖掘。散列索引进行"相等比较"非常快，但是对"范围比较"的速度就慢多了，因此散列索引值适合使用在=和<>的操作符中，不适合在<或>操作符中，也同样不适合用在order by子句中。

可以在表创建时利用USING子句指定要使用的版本。例如: 

create table users
  
(
  
id smallint unsigned not null auto_increment,
  
username varchar(15) not null,
  
pwd varchar(15) not null,
  
index using hash (username),
  
primary key (id)
  
)engine=memory;

上述代码创建了一个表，在username字段上使用了HASH散列索引。下面的代码就创建一个表，使用BTREE索引。

create table users
  
(
  
id smallint unsigned not null auto_increment,
  
username varchar(15) not null,
  
pwd varchar(15) not null,
  
index using btree (username),
  
primary key (id)
  
)engine=memory;

### MERGE

MERGE存储引擎是一组MyISAM表的组合，这些MyISAM表结构必须完全相同，尽管其使用不如其它引擎突出，但是在某些情况下非常有用。说白了，Merge表就是几个相同MyISAM表的聚合器；Merge表中并没有数据，对Merge类型的表可以进行查询、更新、删除操作，这些操作实际上是对内部的MyISAM表进行操作。Merge存储引擎的使用场景。

对于服务器日志这种信息，一般常用的存储策略是将数据分成很多表，每个名称与特定的时间端相关。例如: 可以用12个相同的表来存储服务器日志数据，每个表用对应各个月份的名字来命名。当有必要基于所有12个日志表的数据来生成报表，这意味着需要编写并更新多表查询，以反映这些表中的信息。与其编写这些可能出现错误的查询，不如将这些表合并起来使用一条查询，之后再删除Merge表，而不影响原来的数据，删除Merge表只是删除Merge表的定义，对内部的表没有任何影响。

### ARCHIVE

Archive是归档的意思，在归档之后很多的高级功能就不再支持了，仅仅支持最基本的插入和查询两种功能。在MySQL 5.5版以前，Archive是不支持索引，但是在MySQL 5.5以后的版本中就开始支持索引了。Archive拥有很好的压缩机制，它使用zlib压缩库，在记录被请求时会实时压缩，所以它经常被用来当做仓库使用。

## 存储引擎的一些问题

### 如何查看服务器有哪些存储引擎可以使用

为确定你的MySQL服务器可以用哪些存储引擎，执行如下命令: show engines;
  
这个命令就能搞定了。

### 如何选择最适合你的存储引擎呢

选择标准可以分为: 是否需要支持事务；是否需要使用热备；崩溃恢复: 能否接受崩溃；是否需要外键支持；
  
然后按照标准，选择对应的存储引擎即可:

* MyISAM: 默认的MySQL插件式存储引擎，它是在Web、数据仓储和其他应用环境下最常使用的MySQL存储引擎之一。注意，通过更改STORAGE_ENGINE配置变量，能够方便地更改MySQL服务器的默认存储引擎。
* InnoDB: 用于事务处理应用程序，具有众多特性，包括ACID事务支持。
* BDB: 可替代InnoDB的事务引擎，支持COMMIT、ROLLBACK和其他事务特性。
* Memory: 将所有数据保存在RAM中，在需要快速查找引用和其他类似数据的环境下，可提供极快的访问。
* Merge: 允许MySQL DBA或开发人员将一系列等同的MyISAM表以逻辑方式组合在一起，并作为1个对象引用它们。对于诸如数据仓储等VLDB环境十分适合。
* Archive: 为大量很少引用的历史、归档、或安全审计信息的存储和检索提供了完美的解决方案。
* Federated: 能够将多个分离的MySQL服务器链接起来，从多个物理服务器创建一个逻辑数据库。十分适合于分布式环境或数据集市环境。
* Cluster/NDB: MySQL的簇式数据库引擎，尤其适合于具有高性能查找要求的应用程序，这类查找需求还要求具有最高的正常工作时间和可用性。
* Other: 其他存储引擎包括CSV (引用由逗号隔开的用作数据库表的文件) ，Blackhole (用于临时禁止对数据库的应用程序输入) ，以及Example引擎 (可为快速创建定制的插件式存储引擎提供帮助) 。

请记住，对于整个服务器或方案，你并不一定要使用相同的存储引擎，你可以为方案中的每个表使用不同的MySQL存储引擎，这点很重要。

### 各存储引擎之间的区别

为了做出选择哪一个存储引擎的决定，我们首先需要考虑每一个存储引擎提供了哪些不同的核心功能。这种功能使我们能够把不同的存储引擎区别开来。我们一般把这些核心功能分为四类:支持的字段和数据类型、锁定类型、索引和处理。一些引擎具有能过促使你做出决定的独特的功能，我们一会儿再仔细研究这些具体问题。

#### 字段和数据类型

虽然所有这些引擎都支持通用的数据类型，例如整型、实型和字符型等，但是，并不是所有的引擎都支持其它的字段类型，特别是BLOG(二进制大对象)或者TEXT文本类型。其它引擎也许仅支持有限的字符宽度和数据大小。

这些局限性可能直接影响到你可以存储的数据，同时也可能会对你实施的搜索的类型或者你对那些信息创建的索引产生间接的影响。这些区别能够影响你的应用程序的性能和功能，因为你必须要根据你要存储的数据类型选择对需要的存储引擎的功能做出决策。

#### 锁定

数据库引擎中的锁定功能决定了如何管理信息的访问和更新。当数据库中的一个对象为信息更新锁定了，在更新完成之前，其它处理不能修改这个数据(在某些情况下还不允许读这种数据)。

锁定不仅影响许多不同的应用程序如何更新数据库中的信息，而且还影响对那个数据的查询。这是因为查询可能要访问正在被修改或者更新的数据。总的来说，这种延迟是很小的。大多数锁定机制主要是为了防止多个处理更新同一个数据。由于向数据中插入信息和更新信息这两种情况都需要锁定，你可以想象，多个应用程序使用同一个数据库可能会有很大的影响。

不同的存储引擎在不同的对象级别支持锁定，而且这些级别将影响可以同时访问的信息。得到支持的级别有三种:表锁定、块锁定和行锁定。支持最多的是表锁定，这种锁定是在MyISAM中提供的。在数据更新时，它锁定了整个表。这就防止了许多应用程序同时更新一个具体的表。这对应用很多的多用户数据库有很大的影响，因为它延迟了更新的过程。

页级锁定使用Berkeley DB引擎，并且根据上载的信息页(8KB)锁定数据。当在数据库的很多地方进行更新的时候，这种锁定不会出现什么问题。但是，由于增加几行信息就要锁定数据结构的最后8KB，当需要增加大量的行，也别是大量的小型数据，就会带来问题。

行级锁定提供了最佳的并行访问功能，一个表中只有一行数据被锁定。这就意味着很多应用程序能够更新同一个表中的不同行的数据，而不会引起锁定的问题。只有InnoDB存储引擎支持行级锁定。

#### 建立索引

建立索引在搜索和恢复数据库中的数据的时候能够显著提高性能。不同的存储引擎提供不同的制作索引的技术。有些技术也许会更适合你存储的数据类型。
  
有些存储引擎根本就不支持索引，其原因可能是它们使用基本表索引(如MERGE引擎)或者是因为数据存储的方式不允许索引(例如FEDERATED或者BLACKHOLE引擎)。

#### 事务处理

事务处理功能通过提供在向表中更新和插入信息期间的可靠性。这种可靠性是通过如下方法实现的，它允许你更新表中的数据，但仅当应用的应用程序的所有相关操作完全完成后才接受你对表的更改。例如，在会计处理中每一笔会计分录处理将包括对借方科目和贷方科目数据的更改，你需要要使用事务处理功能保证对借方科目和贷方科目的数据更改都顺利完成，才接受所做的修改。如果任一项操作失败了，你都可以取消这个事务处理，这些修改就不存在了。如果这个事务处理过程完成了，我们可以通过允许这个修改来确认这个操作。

### MyISAM与InnoDB的区别

虽然MySQL里的存储引擎不只是MyISAM与InnoDB这两个，但常用的就是它俩了,下面我们分别来看两种存储引擎的区别:

  * InnoDB支持事务，MyISAM不支持，这一点是非常之重要。事务是一种高级的处理方式，如在一些列增删改中只要哪个出错还可以回滚还原，而MyISAM就不可以了。
  * MyISAM适合查询以及插入为主的应用，InnoDB适合频繁修改以及设计到安全性就高的应用
  * InnoDB支持外键，MyISAM不支持
  * MyISAM是默认引擎，InnoDB需要指定
  * InnoDB不支持FULLTEXT类型的索引
  * InnoDB中不保存表的行数，如select count(\*) from table时，InnoDB需要扫描一遍整个表来计算有多少行，但是MyISAM只要简单的读出保存好的行数即可。注意的是，当count(\*)语句包含where条件时MyISAM也需要扫描整个表
  * 对于自增长的字段，InnoDB中必须包含只有该字段的索引，但是在MyISAM表中可以和其他字段一起建立联合索引
  * 清空整个表时，InnoDB是一行一行的删除，效率非常慢。MyISAM则会重建表
  * InnoDB支持行锁 (某些情况下还是锁整表，如 update table set a=1 where user like '%lee%'

## 总结

这篇文章总结了几种比较常用的存储引擎，对于实际的工作，需要根据具体的情况而定，结合实际的项目实例进行应用，才是最好的学习方法。

## 几个常用存储引擎的特点

下面我们重点介绍几种常用的存储引擎并对比各个存储引擎之间的区别和推荐使用方式。


  
    <th>
      特点
    </th>
    
    <th>
      Myisam
    </th>
    
    <th>
      BDB
    </th>
    
    <th>
      Memory
    </th>
    
    <th>
      InnoDB
    </th>
    
    <th>
      Archive
    </th>
  
  
  
    
      存储限制
    
    
    
      没有
    
    
    
      没有
    
    
    
      有
    
    
    
      64TB
    
    
    
      没有
    
  
  
  
    
      事务安全
    
    
    
    
    
    
      支持
    
    
    
    
    
    
      支持
    
    
    
    
  
  
  
    
      锁机制
    
    
    
      表锁
    
    
    
      页锁
    
    
    
      表锁
    
    
    
      行锁
    
    
    
      行锁
    
  
  
  
    
      B树索引
    
    
    
      支持
    
    
    
      支持
    
    
    
      支持
    
    
    
      支持
    
    
    
    
  
  
  
    
      哈希索引
    
    
    
    
    
    
    
    
    
      支持
    
    
    
      支持
    
    
    
    
  
  
  
    
      全文索引
    
    
    
      支持
    
    
    
    
    
    
    
    
    
    
    
    
    
  
  
  
    
      集群索引
    
    
    
    
    
    
    
    
    
    
    
    
      支持
    
    
    
    
  
  
  
    
      数据缓存
    
    
    
    
    
    
    
    
    
      支持
    
    
    
      支持
    
    
    
    
  
  
  
    
      索引缓存
    
    
    
      支持
    
    
    
    
    
    
      支持
    
    
    
      支持
    
    
    
    
  
  
  
    
      数据可压缩
    
    
    
      支持
    
    
    
    
    
    
    
    
    
    
    
    
      支持
    
  
  
  
    
      空间使用
    
    
    
      低
    
    
    
      低
    
    
    
      N/A
    
    
    
      高
    
    
    
      非常低
    
  
  
  
    
      内存使用
    
    
    
      低
    
    
    
      低
    
    
    
      中等
    
    
    
      高
    
    
    
      低
    
  
  
  
    
      批量插入的速度
    
    
    
      高
    
    
    
      高
    
    
    
      高
    
    
    
      低
    
    
    
      非常高
    
  
  
  
    
      支持外键
    
    
    
    
    
    
    
    
    
    
    
    
      支持
    
    
    
    
  


**最常使用的2种存储引擎: **

  * Myisam是MySQL的默认存储引擎。当create创建新表时，未指定新表的存储引擎时，默认使用Myisam。每个MyISAM在磁盘上存储成三个文件。文件名都和表名相同，扩展名分别是.frm (存储表定义) 、.MYD (MYData，存储数据)、.MYI (MYIndex，存储索引)。数据文件和索引文件可以放置在不同的目录，平均分布io，获得更快的速度。
  * InnoDB存储引擎提供了具有提交、回滚和崩溃恢复能力的事务安全。但是对比Myisam的存储引擎，InnoDB写的处理效率差一些并且会占用更多的磁盘空间以保留数据和索引。

## 如何选择合适的存储引擎

选择标准: 根据应用特点选择合适的存储引擎，对于复杂的应用系统可以根据实际情况选择多种存储引擎进行组合。

下面是常用存储引擎的适用环境: 

  1. MyISAM: 默认的MySQL插件式存储引擎，它是在Web、数据仓储和其他应用环境下最常使用的存储引擎之一
  2. InnoDB: 用于事务处理应用程序，具有众多特性，包括ACID事务支持。
  3. Memory: 将所有数据保存在RAM中，在需要快速查找引用和其他类似数据的环境下，可提供极快的访问。
  4. Merge: 允许MySQL DBA或开发人员将一系列等同的MyISAM表以逻辑方式组合在一起，并作为1个对象引用它们。对于诸如数据仓储等VLDB环境十分适合。
  5. 


建表的时候会选择数据库引擎，常用的有MyISAM和InnoDB，到底选哪个呢？

**参考文献: **

  * http://drizzlewalk.blog.51cto.com/2203401/443266
  * http://www.rackspace.com/knowledge_center/article/MySQL-engines-myisam-vs-innodb
  * http://stackoverflow.com/questions/20148/myisam-versus-innodb
  * http://www.pureweber.com/article/myisam-vs-innodb/

**什么是MyISAM?**

MyISAM是MySQL关系数据库管理系统的默认储存引擎。这种MySQL表存储结构从旧的ISAM代码扩展出许多有用的功能。在新版本的MySQL中，InnoDB引擎由于其对事务，参照完整性，以及更高的并发性等优点开始广泛的取代MyISAM。

每一个MyISAM表都对应于硬盘上的三个文件。这三个文件有一样的文件名，但是有不同的扩展名以指示其类型用途: .frm文件保存表的定义，但是这个文件并不是MyISAM引擎的一部，而是服务器的一部分；.MYD保存表的数据；.MYI是表的索引文件。

**什么是InnoDB?**

InnoDB是MySQL的另一个存储引擎，正成为目前MySQL AB所发行新版的标准，被包含在所有二进制安装包里。较之于其它的存储引擎它的优点是它支持兼容ACID的事务 (类似于PostgreSQL),以及参数完整性 (即对外键的支持) 。

Oracle公司与2005年10月收购了Innobase。Innobase采用双认证授权。它使用GNU发行，也允许其它想将InnoDB结合到商业软件的团体获得授权。

## MyISAM vs Innodb 快速比较表:


  
    <th>
      MyISAM
    </th>
    
    <th>
      Innodb
    </th>
  
  
  
    
      Not *ACID compliant and non-transactional
    
    
    
      *ACID compliant and hence fully transactional with ROLLBACK and COMMIT and support for Foreign Keys
    
  
  
  
    
      MySQL 5.0 Default Engine
    
    
    
      Rackspace Cloud Default Engine
    
  
  
  
    
      Offers Compression
    
    
    
      Offers Compression
    
  
  
  
    
      Requires full repair/rebuild of indexes/tables
    
    
    
      Auto recovery from crash via replay of logs
    
  
  
  
    
      Changed Db pages written to disk instantly
    
    
    
      Dirty pages converted from random to sequential before commit and flush to disk
    
  
  
  
    
      No ordering in storage of data
    
    
    
      Row data stored in pages in PK order
    
  
  
  
    
      Table level locking
    
    
    
      Row level locking
ACID – Atomicity, Consistency, Isolation, Durability (read more on it here: http://en.wikipedia.org/wiki/ACID

在StackOverflow上的小总结: 
 
InnoDB的设计目标是处理大容量数据库系统，它的CPU利用率是其它基于磁盘的关系数据库引擎所不能比的。


http://boweihe.me/?p=1500

http://c.biancheng.net/cpp/html/1465.html

http://noalgo.info/1053.html