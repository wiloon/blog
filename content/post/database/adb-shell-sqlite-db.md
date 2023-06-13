---
title: adb shell sqlite DB
author: "-"
date: 2012-07-08T08:48:36+00:00
url: adb/sqlite
categories:
  - DataBase
tags:
  - Sqlite

---
## adb shell sqlite DB

在Android应用程序开发中，我们有时可能会用到系统中自带内嵌的数据库sqlite3，例如我们在某个应用程序中创建了数据库，如何查看该数据库或者如何查看该数据库中包含有哪些表或数据。下面是我在应用程序中创建了一个数据库以及表，如何采用命令行的方式去查看该数据库和表

cd /data/data/com.wiloon.android.rsslab/databases

sqlite3 RssLab

.tables

select * from tag;

com.wiloon.android.rsslab 是包名.

RssLab 是数据库名.

tag: 表名

.exit 退出.

查看字段名

.header on

查看sqlite3表结构的命令
  
在android下通过adb shell命令可以进入sqlite3的命令行client，见: 在android命令行下使用sqlite3。

如果想列出该数据库中的所有表，可:

.table
  
如果想查看这些表的结构:

select * from sqlite_master where type="table";
  
可以看到类似:

默认情况下，不会出现红框中的表头，需要之前设置，命令为:

.header on
  
如果只想查看具体一张表的表结构，比如查看emperors表，命令为:

select * from sqlite_master where type="table" and name="emperors";
  
另外，也可以这样:

sqlite> .schema emperors
  
CREATE TABLE emperors( id integer primary key autoincrement, name text,dynasty text,start_year text);

<http://marshal.easymorse.com/index.html%3Fp=2981.html>
