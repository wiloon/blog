---
title: sqlite command
author: "-"
date: 2015-01-17T04:46:52+00:00
url: /?p=7250
categories:
  - Inbox
tags:
  - Sqlite

---
## sqlite command
```bash
# 安装
sudo pacman -S sqlite
# 创建数据库
sqlite3 /data/rssx/rssx.db
#建表
CREATE TABLE if not exists users (  id char(36) PRIMARY KEY NOT NULL,  name varchar(50) DEFAULT NULL,  create_time timestamp DEFAULT NULL);
# help 
.help
# show tables
.tables
# insert

# alter table, rename
alter table feed
    rename to feeds;


```

在列模式下，每条记录在一个单独的行中以数据列对齐的方式显示。列如: 

sqlite> .mode column

显示 列名.header on

查出所有的表: 
  
select name from sqlite_master where type='table' order by name;

通过以下语句可查询出某个表的所有字段信息
  
PRAGMA table_info([tablename])

cur.execute("PRAGMA table_info(table)")
  
print cur.fetchall()
  
http://duduhehe.iteye.com/blog/1344858
  
http://www.cnblogs.com/riskyer/p/3333809.html

## Go sqlite

```go
import (
    "database/sql"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "rssx/utils/logger"
)

func test() {
    db, err := sql.Open("sqlite3", "./foo.db")
    checkErr(err)
    createTable := `CREATE TABLE if not exists users (
  id char(36) PRIMARY KEY NOT NULL,
  name varchar(50) DEFAULT NULL,
  create_time timestamp DEFAULT NULL
);
`
    r, err := db.Exec(createTable)
    checkErr(err)
    logger.Infof("%+v", r)
    stmt, err := db.Prepare("INSERT INTO `users` VALUES (?,?,?);")
    checkErr(err)
    res, err := stmt.Exec(0, "wiloon", "2017-12-07 22:10:49")
    checkErr(err)
    id, err := res.LastInsertId()
    checkErr(err)
    fmt.Println(id)
    db.Close()
}

func checkErr(err error) {
    if err != nil {
        logger.Errorf("err: %v", err)
    }
}


```