---
title: sqlite
author: "-"
date: 2012-07-08T06:30:12+00:00
url: sqlite
categories:
  - DataBase

---
## sqlite
SQLite，是一款轻型的数据库，是遵守ACID的关联式数据库管理系统，它的设计目标是嵌入式的，而且目前已经在很多嵌入式产品中使用了它，它占用资源非常的低，在嵌入式设备中，可能只需要几百K的内存就够了。它能够支持Windows/Linux/Unix等等主流的操作系统，同时能够跟很多程序语言相结合，比如 Tcl、C#、PHP、Java等，还有ODBC接口，同样比起MySQL、PostgreSQL这两款开源世界著名的数据库管理系统来讲，它的处理速度比他们都快。SQLite第一个Alpha版本诞生于2000年5月。 至今已经有12个年头，SQLite也迎来了一个版本 SQLite 3已经发布。
```sql
sql-statement ::=	CREATE [UNIQUE] INDEX [IF NOT EXISTS] [database-name .] index-name
ON table-name ( column-name [, column-name]* )
```
### 建表
```sql
CREATE TABLE IF NOT EXISTS p219.users(
  id char(36) PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS index_user_name on p219.users (name);
CREATE INDEX IF NOT EXISTS index_user_email ON p219.users (email);
```

>https://www.runoob.com/sqlite/sqlite-create-table.html
>http://shows.poorren.com/Document/SQLite/39.Html
