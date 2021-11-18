---
title: SQL SERVER 存储过程学习笔记
author: "-"
date: 2012-11-15T10:17:04+00:00
url: /?p=4700
categories:
  - DataBase
tags:
  - SQLServer

---
## SQL SERVER 存储过程学习笔记
## 


   将常用的或很复杂的工作,预先用SQL语句写好并用一个指定的名称存储起来, 那么以后要叫数据库提供与已定义好的存储过程的功能相同的服务时,只需调用execute,即可自动完成命令。                  存储过程的优点 
  
        1.存储过程只在创造时进行编译,以后每次执行存储过程都不需再重新编译,而一般SQL语句每执行一次就编译一次,所以使用存储过程可提高数据库执行速度。
 2.当对数据库进行复杂操作时(如对多个表进行Update,Insert,Query,Delete时) ,可将此复杂操作用存储过程封装起来与数据库提供的事务处理结合一起使用。
 3.存储过程可以重复使用,可减少数据库开发人员的工作量
 4.安全性高,可设定只有某此用户才具有对指定存储过程的使用权
  
  
     创建存储过程
 *************************************************
  
  
    语法
  
  
  
    CREATE PROC[ EDURE ] [ owner. ] procedure_name [ ; number ]
 [ { @parameter data_type }
 [ VARYING ] [ = default ] [ OUTPUT ] 
     ] [ ,...n ] 
    
    
      [ WITH
 { RECOMPILE | ENCRYPTION | RECOMPILE , ENCRYPTION } ]
    
    
    
      [ FOR REPLICATION ]
    
    
    
      AS sql_statement [ ...n ] 
      
      
        参数
      
      
      
        owner
      
      
      
            拥有存储过程的用户 ID 的名称。owner 必须是当前用户的名称或当前用户所属的角色的名称。
      
      
      
        procedure_name
      
      
      
            新存储过程的名称。过程名必须符合标识符规则,且对于数据库及其所有者必须唯一。
      
      
      
        ;number
      
      
      
            是可选的整数,用来对同名的过程分组,以便用一条 DROP PROCEDURE 语句即可将同组的过程一起除去。例如,名为 orders 的应用程序使用的过程可以命名为 orderproc;1、orderproc;2 等。DROP PROCEDURE orderproc 语句将除去整个组。如果名称中包含定界标识符,则数字不应包含在标识符中,只应在 procedure_name 前后使用适当的定界符。
      
      
      
        @parameter
      
      
      
            过程中的参数。在 CREATE PROCEDURE 语句中可以声明一个或多个参数。用户必须在执行过程时提供每个所声明参数的值（除非定义了该参数的默认值,或者该值设置为等于另一个参数) 。存储过程最多可以有 2.100 个参数。
      
      
      
        使用 @ 符号作为第一个字符来指定参数名称。参数名称必须符合标识符的规则。每个过程的参数仅用于该过程本身；相同的参数名称可以用在其它过程中。默认情况下,参数只能代替常量,而不能用于代替表名、列名或其它数据库对象的名称。
      
      
      
        data_type
      
      
      
            参数的数据类型。除 table 之外的其他所有数据类型均可以用作存储过程的参数。但是,cursor 数据类型只能用于 OUTPUT 参数。如果指定 cursor 数据类型,则还必须指定 VARYING 和 OUTPUT 关键字。对于可以是 cursor 数据类型的输出参数,没有最大数目的限制。
      
      
      
        VARYING
      
      
      
            指定作为输出参数支持的结果集（由存储过程动态构造,内容可以变化) 。仅适用于游标参数。
      
      
      
        default
      
      
      
            参数的默认值。如果定义了默认值,不必指定该参数的值即可执行过程。默认值必须是常量或 NULL。如果过程将对该参数使用 LIKE 关键字,那么默认值中可以包含通配符（%、_、[] 和 [^]) 。
      
      
      
        OUTPUT
      
      
      
            表明参数是返回参数。该选项的值可以返回给 EXEC[UTE]。使用 OUTPUT 参数可将信息返回给调用过程。Text、ntext 和image 参数可用作 OUTPUT 参数。使用 OUTPUT 关键字的输出参数可以是游标占位符。
      
      
      
        n
      
      
      
            表示最多可以指定 2.100 个参数的占位符。
      
      
      
        {RECOMPILE | ENCRYPTION | RECOMPILE, ENCRYPTION}
      
      
      
            RECOMPILE 表明 SQL Server 不会缓存该过程的计划,该过程将在运行时重新编译。在使用非典型值或临时值而不希望覆盖缓存在内存中的执行计划时,请使用 RECOMPILE 选项。
      
      
      
        ENCRYPTION 表示 SQL Server 加密 syscomments 表中包含 CREATE PROCEDURE 语句文本的条目。使用 ENCRYPTION 可防止将过程作为 SQL Server 复制的一部分发布。
      
      
      
        FOR REPLICATION
      
      
      
            指定不能在订阅服务器上执行为复制创建的存储过程。.使用 FOR REPLICATION 选项创建的存储过程可用作存储过程筛选,且只能在复制过程中执行。本选项不能和 WITH RECOMPILE 选项一起使用。
      
      
      
        AS
      
      
      
           指定过程要执行的操作。
      
      
      
        sql_statement
      
      
      
           过程中要包含的任意数目和类型的 Transact-SQL 语句。但有一些限制。
      
      
      
        n
      
      
      
           是表示此过程可以包含多条 Transact-SQL 语句的占位符。
      