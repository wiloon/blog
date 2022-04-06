---
title: sqlite
author: "-"
date: 2022-01-21 15:35:49
url: sqlite
categories:
  - database

tags:
  - reprint
---
## sqlite
SQLite，是一款轻型的数据库，是遵守ACID的关联式数据库管理系统，它的设计目标是嵌入式的，而且目前已经在很多嵌入式产品中使用了它，它占用资源非常的低，在嵌入式设备中，可能只需要几百K的内存就够了。它能够支持Windows/Linux/Unix等等主流的操作系统，同时能够跟很多程序语言相结合，比如 Tcl、C#、PHP、Java等，还有ODBC接口，同样比起MySQL、PostgreSQL这两款开源世界著名的数据库管理系统来讲，它的处理速度比他们都快。SQLite第一个Alpha版本诞生于2000年5月。 至今已经有12个年头，SQLite也迎来了一个版本 SQLite 3已经发布。

```sql
sql-statement ::=    CREATE [UNIQUE] INDEX [IF NOT EXISTS] [database-name .] index-name
ON table-name ( column-name [, column-name]* )
```
### 建表
```sql
CREATE TABLE IF NOT EXISTS users (
  id char(36) PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  create_time timestamp NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS index_user_name on users (name);
CREATE INDEX IF NOT EXISTS index_user_email ON users (email);

CREATE TABLE IF NOT EXISTS comment(
  id INTEGER AUTO_INCREMENT NOT NULL,
  content VARCHAR(300) NOT NULL,
  user_id char(36)  NOT NULL,
  create_time timestamp NOT NULL,
  update_time timestamp NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tree_path(
  parent INTEGER NOT NULL,
  child INTEGER NOT NULL,
  PRIMARY KEY (parent, child)
);

INSERT INTO users VALUES ('c31f5e0e-0e0c-4731-97dc-9c6675a0068c','admin','admin@admin.com','$2a$10$AR7t1b/kgGS2oiTrlrW2C.JkVAOT3ZviKj.2zvWZIm0lBnsOrTuX2', now())
```

>https://www.runoob.com/sqlite/sqlite-create-table.html
>http://shows.poorren.com/Document/SQLite/39.Html



### 索引 B树
>https://blog.csdn.net/jinking01/article/details/115725022


### command
```bash
# query schema
.table


```
>https://www.sqlite.org/cli.html
