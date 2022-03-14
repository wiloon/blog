---
title: oracle 导出sql脚本
author: "-"
date: 2015-04-22T04:30:33+00:00
url: /?p=7474
categories:
  - Uncategorized

tags:
  - reprint
---
## oracle 导出sql脚本
大体的分为三种方法: 

一、可以通过toad、plsql develop等第三方工具进行导出DLL操作，用这种办法的好处在于操作简单方便，但需要安装，下面简单介绍一下用这两个工具获得DLL语句的操作。

二、直接通过EXP/IMP工具

Oracle提供的最原始最实用的导入导出工具，我们大体上可以分为三种办法实现导出DDL。

a. 通过imp指定indexfile参数，但这种办法不爽在于有每行前会有REM

语法大体如下: 

exp userid=... tables=emp rows=n file=emp.dmp
  
imp userid=... file=emp.dmp indexfile=emp.sql

b. 通过imp指定show=y，同时指定log参数，格式上也不是很爽，在格式上很美观的还是通过工具导出的比较美观

语法大体如下: 

exp userid=... tables=emp rows=n file= emp.dmp
  
imp userid=... file= emp.dmp show=y log=emp.sql

c. 利用unix下有strings命令,语法大体如下，这种方法比较野蛮: 

exp userid=... tables=tab1 rows=n file=tab1.dmp
  
strings emp.dmp >emp.sql
  
emp.sql中就有DLL语句了

三、通过9i的DBMS_METADATA包得到DLL语句

基本上用到的语法如下: 

a. 获取单个的建表和建索引的语法
  
set heading off;
  
set echo off;
  
Set pages 999;
  
set long 90000;

spool DEPT.sql
  
select dbms_metadata.get_ddl('TABLE','DEPT','SCOTT') from dual;
  
select dbms_metadata.get_ddl('INDEX','DEPT_IDX','SCOTT') from dual;
  
spool off;

b.获取一个SCHEMA下的所有建表和建索引的语法，以scott为例: 

set pagesize 0
  
set long 90000
  
set feedback off

set echo off
  
spool scott_schema.sql
  
connect scott/tiger;
  
SELECT DBMS_METADATA.GET_DDL('TABLE',u.table_name) FROM USER_TABLES u;
  
SELECT DBMS_METADATA.GET_DDL('INDEX',u.index_name) FROM USER_INDEXES u;
  
spool off;

c. 获取某个SCHEMA的建全部存储过程的语法
  
connect brucelau /brucelau;
  
spool procedures.sql

select DBMS_METADATA.GET_DDL('PROCEDURE',u.object_name) from user_objects u where object_type = 'PROCEDURE';
  
spool off;

另: dbms_metadata.get_ddl('TABLE','TAB1','USER1')
  
三个参数中，第一个指定导出DDL定义的对象类型 (此例中为表类型) ，第二个是对象名 (此例中即表名) ，第三个是对象所在的用户名。

ORACLE获取DML(Insert into)的方法

from: 把Oracle表里的数据导成insert语句

有些时候我们需要把oracle里的数据导入其他数据库里。生成insert into 表名 .... 是一种很简单直接的方法。

今年六月份从www.arikaplan.com/oracle.html看到一个可以生成insert into 表名 ....语句的存储过程genins_output。按中文习惯的时间格式YYYY-MM-DD HH24:MI:SS改了改，并新写了一个存储过程genins_file.sql。

它可以把小于16383条记录表里的数据导成(insert into 表名 ....)OS下文件。

调用它之前，DBA要看看数据库的初始化参数 UTL_FILE_DIR 是否已经正确地设置:

SQL> show parameters utl_file_dir;
  
可以看到该参数的当前设置。

如果没有值，必须修改数据库的initsid.ora文件，将utl_file_dir 指向一个你想用PL/SQL file I/O 的路径。重新启动数据库。此参数才生效。

调用它，可以把表里的数据生成(insert into 表名 ....)OS下文件的过程genins_file方法:

SQL>exec genins_file('emp','/oracle/logs','insert_emp.sql');
  
| ||
  
表名，可变|生成OS下文件名,可变
  
|
  
utl_file_dir路径名,不变(我设置的是/oracle/logs)

可以在OS目录/oracle/logs下看到insert_emp.sql文件。
  
注意事项: 生成(insert into 表名 ....)OS下文件最多32767行。因为我一条insert分成两行,所以最多处理16383条记录的表。

附: genins_file.sql

code:
  
---------------------------
  
CREATE OR REPLACE PROCEDURE genins_file(
  
p_table     IN varchar2,
  
p_output_folder IN VARCHAR2,
  
p_output_file   IN VARCHAR2)
  
IS
  
-
  
l_column_list       VARCHAR2(32767);
  
l_value_list        VARCHAR2(32767);
  
l_query             VARCHAR2(32767);
  
l_cursor            NUMBER;
  
ignore         NUMBER;
  
l_insertline1          varchar2(32767);
  
l_insertline2          varchar2(32767);
  
cmn_file_handle       UTL_FILE.file_type;

-

FUNCTION get_cols(p_table VARCHAR2)
  
RETURN VARCHAR2
  
IS
  
l_cols VARCHAR2(32767);
  
CURSOR l_col_cur(c_table VARCHAR2) IS
  
SELECT column_name
  
FROM   user_tab_columns
  
WHERE  table_name = upper(c_table)
  
ORDER BY column_id;
  
BEGIN
  
l_cols := null;
  
FOR rec IN l_col_cur(p_table)
  
LOOP
  
l_cols := l_cols || rec.column_name || ',';
  
END LOOP;
  
RETURN substr(l_cols,1,length(l_cols)-1);
  
END;

-

FUNCTION get_query(p_table IN VARCHAR2)
  
RETURN VARCHAR2
  
IS
  
l_query VARCHAR2(32767);
  
CURSOR l_query_cur(c_table VARCHAR2) IS
  
SELECT 'decode('||column_name||',null,"null",'||
  
decode(data_type,'VARCHAR2',""""'||'||column_name ||'||""""'
  
,'DATE',""""'||to_char('||column_name||',"YYYY-MM-DD HH24:MI:SS")||""""'
  
,column_name
  
) || ')' column_query
  
FROM user_tab_columns
  
WHERE table_name = upper(c_table)
  
ORDER BY column_id;
  
BEGIN
  
l_query := 'SELECT ';
  
FOR rec IN l_query_cur(p_table)
  
LOOP
  
l_query := l_query || rec.column_query || '||","||';
  
END LOOP;
  
l_query := substr(l_query,1,length(l_query)-7);
  
RETURN l_query || ' FROM ' || p_table;
  
END;

-

BEGIN
  
l_column_list  := get_cols(p_table);
  
l_query        := get_query(p_table);
  
l_cursor := dbms_sql.open_cursor;
  
DBMS_SQL.PARSE(l_cursor, l_query, DBMS_SQL.native);
  
DBMS_SQL.DEFINE_COLUMN(l_cursor, 1, l_value_list, 32767);
  
ignore := DBMS_SQL.EXECUTE(l_cursor);

-

IF NOT UTL_FILE.IS_OPEN(cmn_file_handle) THEN
  
cmn_file_handle := UTL_FILE.FOPEN (p_output_folder, p_output_file, 'a',32767);
  
END IF;

LOOP
  
IF DBMS_SQL.FETCH_ROWS(l_cursor)>0 THEN
  
DBMS_SQL.COLUMN_VALUE(l_cursor, 1, l_value_list);
  
l_insertline1:='INSERT INTO '||p_table||' ('||l_column_list||')';
  
l_insertline2:=' VALUES ('||l_value_list||');';
  
UTL_FILE.put_line (cmn_file_handle, l_insertline1);
  
UTL_FILE.put_line (cmn_file_handle, l_insertline2);
  
ELSE
  
EXIT;
  
END IF;
  
END LOOP;
  
IF NOT UTL_FILE.IS_OPEN(cmn_file_handle) THEN
  
UTL_FILE.FCLOSE (cmn_file_handle);
  
END IF;
  
END;
  
/