---
title: sql server 临时表
author: "-"
type: post
date: 2013-07-08T07:40:14+00:00
url: /?p=5619
categories:
  - Uncategorized

---
## sql server 临时表
SQL Server 支持临时表。临时表就是那些名称以井号 (#) 开头的表。如果当用户断开连接时没有除去临时表，SQL Server 将自动除去临时表。临时表不存储在当前数据库内，而是存储在系统数据库 tempdb 内。

临时表有两种类型: 

本地临时表
  
以一个井号 (#) 开头的那些表名。只有在创建本地临时表的连接上才能看到这些表。

全局临时表
  
以两个井号 (##) 开头的那些表名。在所有连接上都能看到全局临时表。如果在创建全局临时表的连接断开前没有显式地除去这些表，那么只要所有其它任务停止引用它们，这些表即被除去。当创建全局临时表的连接断开后，新的任务不能再引用它们。当前的语句一执行完，任务与表之间的关联即被除去；因此通常情况下，只要创建全局临时表的连接断开，全局临时表即被除去。

**创建临时表**
  
方法一: 
  
create table #临时表名(字段1 约束条件,
  
字段2 约束条件,
  
.....)
  
create table ##临时表名(字段1 约束条件,
  
字段2 约束条件,
  
.....)
  
方法二: 
  
select * into #临时表名 from 你的表;
  
select * into ##临时表名 from 你的表;
  
注: 以上的#代表局部临时表，##代表全局临时表

**查询临时表**
  
select * from #临时表名;
  
select * from ##临时表名;

**删除临时表**
  
drop table #临时表名;
  
drop table ##临时表名;

<http://www.cnblogs.com/Hdsome/archive/2008/12/10/1351504.html>

<http://blog.csdn.net/hank5658/article/details/5543622>