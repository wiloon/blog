---
title: oracle 导出sql脚本
author: w1100n
type: post
date: 2015-04-22T04:30:33+00:00
url: /?p=7474
categories:
  - Uncategorized

---
大体的分为三种方法：

一、可以通过toad、plsql develop等第三方工具进行导出DLL操作，用这种办法的好处在于操作简单方便，但需要安装，下面简单介绍一下用这两个工具获得DLL语句的操作。

二、直接通过EXP/IMP工具

Oracle提供的最原始最实用的导入导出工具，我们大体上可以分为三种办法实现导出DDL。

a. 通过imp指定indexfile参数，但这种办法不爽在于有每行前会有REM

语法大体如下：

exp userid=... tables=emp rows=n file=emp.dmp
  
imp userid=... file=emp.dmp indexfile=emp.sql

b. 通过imp指定show=y，同时指定log参数，格式上也不是很爽，在格式上很美观的还是通过工具导出的比较美观

语法大体如下：

exp userid=... tables=emp rows=n file= emp.dmp
  
imp userid=... file= emp.dmp show=y log=emp.sql

c. 利用unix下有strings命令,语法大体如下，这种方法比较野蛮：

exp userid=... tables=tab1 rows=n file=tab1.dmp
  
strings emp.dmp >emp.sql
  
emp.sql中就有DLL语句了

三、通过9i的DBMS_METADATA包得到DLL语句

基本上用到的语法如下：

a. 获取单个的建表和建索引的语法
  
set heading off;
  
set echo off;
  
Set pages 999;
  
set long 90000;

spool DEPT.sql
  
select dbms\_metadata.get\_ddl('TABLE','DEPT','SCOTT') from dual;
  
select dbms\_metadata.get\_ddl('INDEX','DEPT_IDX','SCOTT') from dual;
  
spool off;

b.获取一个SCHEMA下的所有建表和建索引的语法，以scott为例：

set pagesize 0
  
set long 90000
  
set feedback off

set echo off
  
spool scott_schema.sql
  
connect scott/tiger;
  
SELECT DBMS\_METADATA.GET\_DDL('TABLE',u.table\_name) FROM USER\_TABLES u;
  
SELECT DBMS\_METADATA.GET\_DDL('INDEX',u.index\_name) FROM USER\_INDEXES u;
  
spool off;

c. 获取某个SCHEMA的建全部存储过程的语法
  
connect brucelau /brucelau;
  
spool procedures.sql

select DBMS\_METADATA.GET\_DDL('PROCEDURE',u.object\_name) from user\_objects u where object_type = 'PROCEDURE';
  
spool off;

另：dbms\_metadata.get\_ddl('TABLE','TAB1','USER1')
  
三个参数中，第一个指定导出DDL定义的对象类型（此例中为表类型），第二个是对象名（此例中即表名），第三个是对象所在的用户名。

ORACLE获取DML(Insert into)的方法

from: 把Oracle表里的数据导成insert语句

有些时候我们需要把oracle里的数据导入其他数据库里。生成insert into 表名 .... 是一种很简单直接的方法。

今年六月份从www.arikaplan.com/oracle.html看到一个可以生成insert into 表名 ....语句的存储过程genins\_output。按中文习惯的时间格式YYYY-MM-DD HH24:MI:SS改了改，并新写了一个存储过程genins\_file.sql。

它可以把小于16383条记录表里的数据导成(insert into 表名 ....)OS下文件。

调用它之前，DBA要看看数据库的初始化参数 UTL\_FILE\_DIR 是否已经正确地设置:

SQL> show parameters utl\_file\_dir;
  
可以看到该参数的当前设置。

如果没有值，必须修改数据库的initsid.ora文件，将utl\_file\_dir 指向一个你想用PL/SQL file I/O 的路径。重新启动数据库。此参数才生效。

调用它，可以把表里的数据生成(insert into 表名 ....)OS下文件的过程genins_file方法:

SQL>exec genins\_file('emp','/oracle/logs','insert\_emp.sql');
  
|　　　 |　　　　　　|
  
表名，可变　|　　　生成OS下文件名,可变
  
|
  
utl\_file\_dir路径名,不变(我设置的是/oracle/logs)

可以在OS目录/oracle/logs下看到insert_emp.sql文件。
  
注意事项: 生成(insert into 表名 ....)OS下文件最多32767行。因为我一条insert分成两行,所以最多处理16383条记录的表。

附：genins_file.sql

code:
  
---------------------------
  
CREATE OR REPLACE PROCEDURE genins_file(
  
p_table     IN varchar2,
  
p\_output\_folder IN VARCHAR2,
  
p\_output\_file   IN VARCHAR2)
  
IS
  
-
  
l\_column\_list       VARCHAR2(32767);
  
l\_value\_list        VARCHAR2(32767);
  
l_query             VARCHAR2(32767);
  
l_cursor            NUMBER;
  
ignore         NUMBER;
  
l_insertline1          varchar2(32767);
  
l_insertline2          varchar2(32767);
  
cmn\_file\_handle       UTL\_FILE.file\_type;

-

FUNCTION get\_cols(p\_table VARCHAR2)
  
RETURN VARCHAR2
  
IS
  
l_cols VARCHAR2(32767);
  
CURSOR l\_col\_cur(c_table VARCHAR2) IS
  
SELECT column_name
  
FROM   user\_tab\_columns
  
WHERE  table\_name = upper(c\_table)
  
ORDER BY column_id;
  
BEGIN
  
l_cols := null;
  
FOR rec IN l\_col\_cur(p_table)
  
LOOP
  
l\_cols := l\_cols || rec.column_name || ',';
  
END LOOP;
  
RETURN substr(l\_cols,1,length(l\_cols)-1);
  
END;

-

FUNCTION get\_query(p\_table IN VARCHAR2)
  
RETURN VARCHAR2
  
IS
  
l_query VARCHAR2(32767);
  
CURSOR l\_query\_cur(c_table VARCHAR2) IS
  
SELECT 'decode('||column_name||',null,"null",'||
  
decode(data\_type,'VARCHAR2',""""'||'||column\_name ||'||""""'
  
,'DATE',""""'||to\_char('||column\_name||',"YYYY-MM-DD HH24:MI:SS")||""""'
  
,column_name
  
) || ')' column_query
  
FROM user\_tab\_columns
  
WHERE table\_name = upper(c\_table)
  
ORDER BY column_id;
  
BEGIN
  
l_query := 'SELECT ';
  
FOR rec IN l\_query\_cur(p_table)
  
LOOP
  
l\_query := l\_query || rec.column_query || '||","||';
  
END LOOP;
  
l\_query := substr(l\_query,1,length(l_query)-7);
  
RETURN l\_query || ' FROM ' || p\_table;
  
END;

-

BEGIN
  
l\_column\_list  := get\_cols(p\_table);
  
l\_query        := get\_query(p_table);
  
l\_cursor := dbms\_sql.open_cursor;
  
DBMS\_SQL.PARSE(l\_cursor, l\_query, DBMS\_SQL.native);
  
DBMS\_SQL.DEFINE\_COLUMN(l\_cursor, 1, l\_value_list, 32767);
  
ignore := DBMS\_SQL.EXECUTE(l\_cursor);

-

IF NOT UTL\_FILE.IS\_OPEN(cmn\_file\_handle) THEN
  
cmn\_file\_handle := UTL\_FILE.FOPEN (p\_output\_folder, p\_output_file, 'a',32767);
  
END IF;

LOOP
  
IF DBMS\_SQL.FETCH\_ROWS(l_cursor)>0 THEN
  
DBMS\_SQL.COLUMN\_VALUE(l\_cursor, 1, l\_value_list);
  
l\_insertline1:='INSERT INTO '||p\_table||' ('||l\_column\_list||')';
  
l\_insertline2:=' VALUES ('||l\_value_list||');';
  
UTL\_FILE.put\_line (cmn\_file\_handle, l_insertline1);
  
UTL\_FILE.put\_line (cmn\_file\_handle, l_insertline2);
  
ELSE
  
EXIT;
  
END IF;
  
END LOOP;
  
IF NOT UTL\_FILE.IS\_OPEN(cmn\_file\_handle) THEN
  
UTL\_FILE.FCLOSE (cmn\_file_handle);
  
END IF;
  
END;
  
/