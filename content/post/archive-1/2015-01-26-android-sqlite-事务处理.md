---
title: Android SQLite 事务处理
author: "-"
type: post
date: 2015-01-26T02:39:02+00:00
url: /?p=7291
categories:
  - Uncategorized
tags:
  - Sqlite

---
## Android SQLite 事务处理
http://www.cnblogs.com/brainy/archive/2012/08/29/2662295.html

【转】Android SQLite 事务处理

应用程序初始化时需要批量的向sqlite中插入大量数据，单独的使用for+Insert方法导致应用响应缓慢,因为 sqlite插入数据的时候默认一条语句就是一个事务，有多少条数据就有多少次磁盘操作。我的应用初始5000条记录也就是要5000次读写磁盘操作。

而且不能保证所有数据都能同时插入。（有可能部分插入成功，另外一部分失败，后续还得删除。太麻烦) 

解决方法: 

添加事务处理，把5000条插入作为一个事务


我们使用SQLite的事务进行控制: 

db.beginTransaction();  //手动设置开始事务

try{

//批量处理操作

for(Collection c:colls){

insert(db, c);

}

db.setTransactionSuccessful(); //设置事务处理成功，不设置会自动回滚不提交。

//在setTransactionSuccessful和endTransaction之间不进行任何数据库操作

}catch(Exception e){

MyLog.printStackTraceString(e);

}finally{

db.endTransaction(); //处理完成

}

1.使用SQLiteDatabase的beginTransaction()方法可以开启一个事务，程序执行到endTransaction() 方法时会检查事务的标志是否为成功，如果程序执行到endTransaction()之前调用了setTransactionSuccessful() 方法设置事务的标志为成功，则所有从beginTransaction（) 开始的操作都会被提交，如果没有调用setTransactionSuccessful() 方法则回滚事务。

2.使用例子如下: 下面两条SQL语句在同一个事务中执行。

Java代码

//银行账户事务测试
  
public void payment()
  
{
  
SQLiteDatabase db = dbOpenHelper.getWritableDatabase();
  
//开启事务
  
db.beginTransaction();
  
try
  
{
  
db.execSQL("update person set amount=amount-10 where personid=?", new Object[]{1});
  
db.execSQL("update person set amount=amount+10 where personid=?", new Object[]{2});
  
//设置事务标志为成功，当结束事务时就会提交事务
  
db.setTransactionSuccessful();
  
}
  
catch（Exception e) {
  
throw(e);
  
}
  
finally
  
{
  
//结束事务
  
db.endTransaction();
  
}
  
}