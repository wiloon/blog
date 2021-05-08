---
title: sql server存储过程中SELECT 与 SET 对变量赋值的区别
author: w1100n
type: post
date: 2013-07-19T07:32:23+00:00
url: /?p=5678
categories:
  - DataBase

---
SQL Server 中对已经定义的变量赋值的方式用两种，分别是 SET 和 SELECT。
  
对于这两种方式的区别，SQL Server 联机丛书中已经有详细的说明，但很多时候我们
  
并没有注意，其实这两种方式还是有很多差别的。

SQL Server推荐使用 SET 而不是 SELECT 对变量进行赋值。
  
当表达式返回一个值并对一个变量进行赋值时，推荐使用 SET 方法。

下表列出 SET 与 SELECT 的区别。请特别注意红色部分。

<table width="509" border="2">
  <tr>
    <td>
    </td>
    
    <td>
      set
    </td>
    
    <td>
      select
    </td>
  </tr>
  
  <tr>
    <td>
      同时对多个变量同时赋值
    </td>
    
    <td>
      不支持
    </td>
    
    <td>
      支持
    </td>
  </tr>
  
  <tr>
    <td>
      表达式返回多个值时
    </td>
    
    <td>
      出错
    </td>
    
    <td>
      <span style="color: #ff0000;">将返回的最后一个值赋给变量
    </td>
  </tr>
  
  <tr>
    <td>
      表达式未返回值
    </td>
    
    <td>
      变量被赋null值
    </td>
    
    <td>
      <span style="color: #ff0000;">变量保持原值
    </td>
  </tr>
</table>

下面以具体示例来说明问题: 

create table chinadba1(
  
userid int ,
  
addr varchar(128)
  
)
  
go
  
insert into chinadba1(userid,addr) values(1,'addr1')
  
insert into chinadba1(userid,addr) values(2,'addr2')
  
insert into chinadba1(userid,addr) values(3,'addr3')
  
go

表达式返回多个值时，使用 SET 赋值
  
declare @addr varchar(128)
  
set @addr = (select addr from chinadba1)
  
/*
  
-出错信息为
  
服务器: 消息 512，级别 16，状态 1，行 2
  
子查询返回的值多于一个。当子查询跟随在 =、!=、<、<=、>、>= 之后，或子查询用作表达式时，这种情况是不允许的。
  
*/
  
go

表达式返回多个值时，使用 SELECT 赋值

declare @addr varchar(128)
  
select @addr = addr from chinadba1
  
print @addr -结果集中最后一个 addr 列的值
  
-结果: addr3
  
go

表达式未返回值时，使用 SET 赋值

declare @addr varchar(128)
  
set @addr = '初始值'
  
set @addr = (select addr from chinadba1 where userid = 4 )
  
print @addr -null值
  
go

表达式未返回值时，使用 SELECT 赋值

declare @addr varchar(128)
  
set @addr = '初始值'
  
select @addr = addr from chinadba1 where userid = 4
  
print @addr -保持原值
  
go

需要注意的是，SELECT 也可以将标量子查询的值赋给变量，如果标量子查询不返回值，则变量被置为 null 值。
  
此时与 使用 SET 赋值是完全相同的
  
对标量子查询的概念大家应该都觉得陌生，举个例子就能说明

declare @addr varchar(128)
  
set @addr = '初始值'
  
-select addr from chinadba1 where userid = 4 为标量子查询语句
  
select @addr = (select addr from chinadba1 where userid = 4)
  
print @addr -null值
  
go