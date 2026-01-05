---
title: SQLite
author: "-"
date: 2026-01-05T15:35:49+08:00
url: sqlite
categories:
  - database
tags:
  - reprint
  - remix
  - AI-assisted
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

## SQLite vs DuckDB 对比

### 核心定位差异

**SQLite**

- **定位**: OLTP (事务处理) 数据库
- **设计目标**: 嵌入式、高并发写入、数据持久化
- **典型场景**: 应用程序数据存储、移动应用、IoT 设备、浏览器存储

**DuckDB**

- **定位**: OLAP (分析处理) 数据库
- **设计目标**: 快速分析查询、列式存储、内存计算
- **典型场景**: 数据分析、数据科学、BI 报表、日志分析

### 性能特点对比

| 特性 | SQLite | DuckDB |
|------|--------|--------|
| **存储方式** | 行式存储 (Row-oriented) | 列式存储 (Column-oriented) |
| **查询类型** | 事务查询 (OLTP) | 分析查询 (OLAP) |
| **写入性能** | 优秀 (支持高并发写入) | 一般 (批量写入较好) |
| **读取性能** | 点查询快 | 聚合分析快 (扫描大量数据) |
| **并发模型** | 多读单写 | 主要为单用户设计 |
| **内存占用** | 极低 (KB 级别) | 较高 (优化内存计算) |

### 功能特性对比

**查询能力**

```sql
-- SQLite: 基础 SQL 支持
SELECT * FROM users WHERE age > 18;

-- DuckDB: 强大的分析函数
SELECT 
    date_trunc('month', create_time) as month,
    count(*) as user_count,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY age) as p95_age
FROM users
GROUP BY month
WINDOW w AS (ORDER BY month ROWS BETWEEN 3 PRECEDING AND CURRENT ROW);
```

**数据类型**

- **SQLite**: INTEGER, REAL, TEXT, BLOB, NULL (动态类型)
- **DuckDB**: 丰富类型支持 - ARRAY, STRUCT, MAP, JSON, UUID, TIMESTAMP WITH TIME ZONE

**数据导入导出**

```sql
-- SQLite: 有限的导入导出
.mode csv
.import file.csv table_name

-- DuckDB: 原生支持多种格式
COPY users TO 'output.parquet' (FORMAT PARQUET);
SELECT * FROM 'data.parquet';
SELECT * FROM 'data.json';
SELECT * FROM read_csv_auto('*.csv');
```

### 使用场景建议

**选择 SQLite 的场景**

1. 需要嵌入式数据库的应用程序
2. 移动应用 (iOS/Android)
3. 浏览器本地存储 (Web SQL)
4. 配置文件、缓存存储
5. 小型 Web 应用的持久化层
6. 频繁的增删改操作

**选择 DuckDB 的场景**

1. 数据分析和数据科学项目
2. 需要处理 CSV/Parquet/JSON 等文件
3. 复杂的聚合和统计查询
4. 替代 Pandas 进行大数据集分析
5. BI 工具的嵌入式分析引擎
6. 数据管道中的 ETL 转换

### 性能基准示例

**场景: 分析 1000 万行数据**

```sql
-- 查询: 按月统计用户数并计算平均值
SELECT 
    strftime('%Y-%m', create_time) as month,
    COUNT(*) as total,
    AVG(score) as avg_score
FROM users
GROUP BY month;
```

- **SQLite**: ~30-60 秒 (行式扫描，读取所有列)
- **DuckDB**: ~1-3 秒 (列式存储，只读需要的列)

**场景: 单条记录插入**

```sql
INSERT INTO users VALUES ('uuid', 'name', 'email', 'password', NOW());
```

- **SQLite**: ~0.1 毫秒 (优化的 OLTP 性能)
- **DuckDB**: ~0.5 毫秒 (非优化场景)

### 生态系统对比

**SQLite**

- 语言绑定: 几乎所有主流语言 (C, Python, Java, Go, Rust, JavaScript...)
- 工具支持: DB Browser for SQLite, Datasette, Litestream
- 社区: 成熟稳定，超过 20 年历史

**DuckDB**

- 语言绑定: Python, R, Java, Node.js, Go, Rust, C++
- 工具支持: DBeaver, 与 Pandas/Arrow 深度集成
- 社区: 快速增长，现代化设计

### 组合使用场景

在某些项目中，可以同时使用两者:

```python
import sqlite3
import duckdb

# SQLite 用于事务数据
sqlite_conn = sqlite3.connect('app.db')
sqlite_conn.execute("INSERT INTO orders VALUES (...)")

# DuckDB 用于分析
duck_conn = duckdb.connect()
duck_conn.execute("""
    SELECT date_trunc('day', order_time) as day,
           SUM(amount) as revenue
    FROM sqlite_scan('app.db', 'orders')
    GROUP BY day
""")
```

### 总结

- **SQLite**: 久经考验的嵌入式 OLTP 数据库，适合事务处理和应用数据存储
- **DuckDB**: 现代化的嵌入式 OLAP 数据库，适合数据分析和复杂查询
- **不是替代关系**: 两者解决不同问题，可以根据场景选择或组合使用

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