---
title: SQLite
author: "-"
date: 2022-01-21 15:35:49
url: sqlite
categories:
  - database
tags:
  - reprint
---
## SQLite

version: 3.44.0

- SQLite 通过文件来保存数据库，一个文件就是一个数据库

### commands

```bash
# archlinux install sqlite
sudo pacman -S sqlite

# ubuntu
sudo apt install sqlite3

# 打开一个已经存在的数据库
sqlite3 /var/lib/enx-api/enx.db

# 启动 sqlite
sqlite3

# 列出数据库文件和名字
.databases

# query schema, 列出所有的表
.table

# 查看表结构, 注意, 表名后面没有分号
.schema table0

# 创建数据库
sqlite3 /data/rssx/rssx.db


# insert data
insert into table_0 (name) values ('foo');

CREATE TABLE if not exists table_1 (name varchar(50) collate nocase PRIMARY KEY, create_time timestamp DEFAULT NULL);
insert into table_1 (name) values ('foo');
insert into table_1 (name) values ('Foo'); -- Runtime error: UNIQUE constraint failed: table_1.name (19)

# help 
.help

# show tables
.tables

# insert

# alter table, rename
alter table feed
    rename to feeds;
```

```sql
-- query that returns the size of a table in a SQLite database
-- 空表的 size 是 4096
select sum("pgsize") from "dbstat" where name='table0';

-- drop table
drop table table0;
```

SQLite，是一种轻型的数据库，是遵守 ACID 的关联式数据库管理系统，它的设计目标是嵌入式的，而且目前已经在很多嵌入式产品中使用了它，
它占用资源非常地低，在嵌入式设备中，可能只需要几百K的内存就够了。它能够支持 Windows/Linux/Unix 等等主流的操作系统，
同时能够跟很多程序语言相结合，比如 Tcl、C#、PHP、Java等，还有ODBC接口，同样比起 MySQL、PostgreSQL 这两款开源世界著名的数据库管理系统来讲，
它的处理速度比他们都快。SQLite 第一个Alpha 版本诞生于2000年5月。 至今已经有12个年头，SQLite 也迎来了一个版本 SQLite 3 已经发布。

```sql
sql-statement ::= CREATE [UNIQUE] INDEX [IF NOT EXISTS] [database-name .] index-name
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

-- 建表
CREATE TABLE if not exists table_0 (id char(36) PRIMARY KEY NOT NULL, name varchar(50) DEFAULT NULL, create_time timestamp DEFAULT NULL);
CREATE TABLE if not exists table_0 (name varchar(50) PRIMARY KEY, create_time timestamp DEFAULT NULL);

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

[https://www.runoob.com/sqlite/sqlite-create-table.html](https://www.runoob.com/sqlite/sqlite-create-table.html)
[http://shows.poorren.com/Document/SQLite/39.Html](http://shows.poorren.com/Document/SQLite/39.Html)

### 索引 B 树

[https://blog.csdn.net/jinking01/article/details/115725022](https://blog.csdn.net/jinking01/article/details/115725022)

[https://www.sqlite.org/cli.html](https://www.sqlite.org/cli.html)

## 在 windows 环境使用 sqlite

- install

[https://www.sqlite.org/download.html](https://www.sqlite.org/download.html)

需要下载两个包: sqlite-dll-win-x64-3440000.zip, sqlite-tools-win-x64-3440000.zip, 解压之后把所有文件都放到同一个目录, 比如: C:\workspace\apps, 把这个目录加到环境变量 PATH.