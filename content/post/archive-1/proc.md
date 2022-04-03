---
title: proc
author: "-"
date: 2013-04-17T06:01:25+00:00
url: /?p=5402
categories:
  - DataBase

tags:
  - reprint
---
## proc
SET ANSI_NULLS ON

SQL-92 标准要求在对空值进行等于 (=) 或不等于 (<>) 比较时取值为 FALSE。当 SET ANSI_NULLS 为 ON 时，即使 column_name 中包含空值，使用 WHERE column_name = NULL 的 SELECT 语句仍返回零行。
SET QUOTED_IDENTIFIER
使 Microsoft® SQL Server™ 遵从关于引号分隔标识符和文字字符串的 SQL-92 规则。由双引号分隔的标识符可以是 Transact-SQL 保留关键字，或者可以包含 Transact-SQL 标识符语法规则通常不允许的字符。

语法
SET QUOTED_IDENTIFIER { ON | OFF }

注释
当 SET QUOTED_IDENTIFIER 为 ON 时，标识符可以由双引号分隔，而文字必须由单引号分隔。当 SET QUOTED_IDENTIFIER 为 OFF 时，标识符不可加引号，且必须遵守所有 Transact-SQL 标识符规则。有关更多信息，请参见使用标识符。文字可以由单引号或双引号分隔。

当 SET QUOTED_IDENTIFIER 为 ON 时，由双引号分隔的所有字符串都被解释为对象标识符。因此，加引号的标识符不必遵守 Transact-SQL 标识符规则。它们可以是保留关键字，并且可以包含 Transact-SQL 标识符中通常不允许的字符。不能使用双引号分隔文字字符串表达式，而必须用单引号括住文字字符串。如果单引号 (') 是文字字符串的一部分，则可以由两个单引号 ('') 表示。当对数据库中的对象名使用保留关键字时，SET QUOTED_IDENTIFIER 必须为 ON。

当 SET QUOTED_IDENTIFIER 为 OFF (默认值) 时，表达式中的文字字符串可以由单引号或双引号分隔。如果文字字符串由双引号分隔，则可以在字符串中包含嵌入式单引号，如省略号。

当在计算列或索引视图上创建或操作索引时，SET QUOTED_IDENTIFIER 必须为 ON。如果 SET QUOTED_IDENTIFIER 为 OFF，则计算列或索引视图上带索引的表上的 CREATE、UPDATE、INSERT 和 DELETE 语句将失败。有关计算列上的索引视图和索引所必需的 SET 选项设置的更多信息，请参见 SET 中的"使用 SET 语句时的注意事项"。

在进行连接时，SQL Server ODBC 驱动程序和用于 SQL Server 的 Microsoft OLE DB 提供程序自动将 QUOTED_IDENTIFIER 设置为 ON。这可以在 ODBC 数据源、ODBC 连接特性或 OLE DB 连接属性中进行配置。对来自 DB-Library 应用程序的连接，SET QUOTED_IDENTIFIER 设置默认为 OFF。

当创建存储过程时，将捕获 SET QUOTED_IDENTIFIER 和 SET ANSI_NULLS 设置，用于该存储过程的后续调用。

当在存储过程内执行 SET QUOTED_IDENTIFIER 时，其设置不更改。

当 SET ANSI_DEFAULTS 为 ON时，将启用 SET QUOTED_IDENTIFIER。

SET QUOTED_IDENTIFIER 还与 sp_dboption 的 quoted identifier 设置相对应。如果 SET QUOTED_IDENTIFIER 为 OFF，则 SQL Server 使用 sp_dboption 的 quoted identifier 设置。有关数据库设置的更多信息，请参见 sp_dboption 和设置数据库选项。

SET QUOTED_IDENTIFIER 是在分析时进行设置的。在分析时进行设置意味着: SET 语句只要出现在批处理或存储过程中即生效，与代码执行实际上是否到达该点无关；并且 SET 语句在任何语句执行之前生效。

权限
SET QUOTED_IDENTIFIER 权限默认授予所有用户。

示例
A. 使用被引用的标识符设置和保留字对象名
下例显示 SET QUOTED_IDENTIFIER 设置必须为 ON，而且表名内的关键字必须在双引号内，才能创建和使用带保留关键字的对象名。

SET QUOTED_IDENTIFIER OFF
GO
-- Attempt to create a table with a reserved keyword as a name
-- should fail.
CREATE TABLE "select" ("identity" int IDENTITY, "order" int)
GO

SET QUOTED_IDENTIFIER ON
GO

-- Will succeed.
CREATE TABLE "select" ("identity" int IDENTITY, "order" int)
GO

SELECT "identity","order" 
FROM "select"
ORDER BY "order"
GO

DROP TABLE "SELECT"
GO

SET QUOTED_IDENTIFIER OFF
GO

B. 在被引用的标识符设置中使用单引号和双引号
下例显示将 SET QUOTED_IDENTIFIER 设置为 ON 和 OFF 时，在字符串表达式中使用单引号和双引号的方式。

SET QUOTED_IDENTIFIER OFF
GO
USE pubs
IF EXISTS(SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS
      WHERE TABLE_NAME = 'Test')
   DROP TABLE Test
GO
USE pubs
CREATE TABLE Test ( Id int, String varchar (30) ) 
GO

-- Literal strings can be in single or double quotation marks.
INSERT INTO Test VALUES (1,"'Text in single quotes'")
INSERT INTO Test VALUES (2,'''Text in single quotes''')
INSERT INTO Test VALUES (3,'Text with 2 '''' single quotes')
INSERT INTO Test VALUES (4,'"Text in double quotes"')
INSERT INTO Test VALUES (5,"""Text in double quotes""")
INSERT INTO Test VALUES (6,"Text with 2 """" double quotes")
GO

SET QUOTED_IDENTIFIER ON
GO

-- Strings inside double quotation marks are now treated 
-- as object names, so they cannot be used for literals.
INSERT INTO "Test" VALUES (7,'Text with a single '' quote')
GO

-- Object identifiers do not have to be in double quotation marks
-- if they are not reserved keywords.
SELECT * 
FROM Test
GO

DROP TABLE Test
GO

SET QUOTED_IDENTIFIER OFF
GO

下面是结果集: 

Id          String                         
----------- ------------------------------ 
1           'Text in single quotes'        
2           'Text in single quotes'        
3           Text with 2 '' single quotes   
4           "Text in double quotes"        
5           "Text in double quotes"        
6           Text with 2 "" double quotes   
7           Text with a single ' quote