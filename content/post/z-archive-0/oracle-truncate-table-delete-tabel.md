---
title: Oracle truncate table, delete tabel
author: "-"
date: 2011-11-28T09:22:02+00:00
url: /?p=1653
categories:
  - DataBase

tags:
  - reprint
---
## Oracle truncate table, delete tabel
# 一、

  
    
      1.delete产生rollback，如果删除大数据量的表速度会很慢，同时会占用很多的rollback segments .truncate 是DDL操作，不产生rollback，速度快一些.
    
    
    
      Truncate table does not generate rollback information and redo records so it is much faster than delete.
    
    
    
      In default, it deallocates all space except the space allocated by MINEXTENTS unless you specify REUSE STORAGE clause.
    
    
    
      2.不从tablespace中腾出空间,需要
    
    
    
      ALTER TABLESPACE AAA COALESCE; 才有空间
    
    
    
      3.truncate 调整high water mark 而delete不.truncate之后，TABLE的HWM退回到 INITIAL和NEXT的位置 (默认) 
    
    
    
      delete 则不可以。
    
    
    
      4.truncate 只能对TABLE
    
    
    
      delete 可以是table,view,synonym
    
    
    
      5.TRUNCATE TABLE 的对象必须是本模式下的，或者有drop any table的权限 而 DELETE 则是对象必须是本模式下的，或被授予 DELETE ON SCHEMA.TABLE 或DELETE ANY TABLE的权限
    
    
    
      二、 truncate是DDL語言.
 delete是DML語言
    
    
    
      DDL語言是自動提交的.
 命令完成就不可回滾.
    
    
    
      truncate的速度也比delete要快得多.
    
    
    
      三、 truncate 会把 highwatermark 回归至 0 ... 当下一次再插入新资料时就会快一些啦。
    
    
    
      所以一般都是在 temp table 上使用的，不过要注意就是 truncate 不能在 pl/sql 上使用，要用 dynamic SQL 才可以。
    
    
    
      四、
    
    
    
      当你不再需要该表时， 用 drop;
 当你仍要保留该表，但要删除所有记录时， 用 truncate;
 当你要删除部分记录时 (always with a WHERE clause), 用 delete.
  
