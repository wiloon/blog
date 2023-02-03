---
title: MySQL 日志 log
author: "-"
date: 2014-05-07T08:22:15+00:00
url: /?p=6599
categories:
  - Inbox
tags:
  - MySQL

---
## MySQL 日志 log

<https://mariadb.com/kb/en/mariadb/general-query-log/>

查询日志:

编辑/etc/MySQL/my.cnf, 在[MySQLd]段下添加以下三行并重启MySQL(MySQL用户写权限)

general-log=1
  
general-log-file=/data/logs/MySQL/MySQL.log
  
log-output=file

查看配置:

```sql
SHOW GLOBAL VARIABLES LIKE '%log%';
```

MySQL日志:
  
主要包含: 错误日志、查询日志、慢查询日志、事务日志、二进制日志；
  
日志是MySQL数据库的重要组成部分。日志文件中记录着MySQL数据库运行期间发生的变化；也就是说用来记录MySQL数据库的客户端连接状况、SQL语句的执行情况和错误信息等。当数据库遭到意外的损坏时，可以通过日志查看文件出错的原因，并且可以通过日志文件进行数据恢复。
  
错误日志
  
在MySQL数据库中，错误日志功能是默认开启的。并且，错误日志无法被禁止。默认情况下，错误日志存储在MySQL数据库的数据文件中。错误日志文件通常的名称为hostname.err。其中，hostname表示服务器主机名。
  
错误日志信息可以自己进行配置的，错误日志所记录的信息是可以通过log-error和log-warnings来定义的，其中log-err是定义是否启用错误日志的功能和错误日志的存储位置，log-warnings是定义是否将警告信息也定义至错误日志中。默认情况下错误日志大概记录以下几个方面的信息: 服务器启动和关闭过程中的信息 (未必是错误信息，如MySQL如何启动InnoDB的表空间文件的、如何初始化自己的存储引擎的等等) 、服务器运行过程中的错误信息、事件调度器运行一个事件时产生的信息、在从服务器上启动服务器进程时产生的信息。
  
下面我们来定义MySQL错误日志的功能:
  
一般而言，日志级别的定义没有回话变量都只是在全局级别下进行定义。

MySQL> SHOW GLOBAL VARIABLES LIKE '%log%';
  
+--------------+------------+
  
| Variable_name | Value |
  
+--------------+------------+
  
| back_log | 50 |
  
| binlog_cache_size | 32768 |
  
| binlog_direct_non_transactional_updates | OFF |
  
| binlog_format | MIXED |
  
| binlog_stmt_cache_size | 32768 |
  
| expire_logs_days | 0 |
  
| general_log | OFF |
  
| general_log_file | /mydata/data/stu18.log |
  
| innodb_flush_log_at_trx_commit | 1 |
  
| innodb_locks_unsafe_for_binlog | OFF |
  
| innodb_log_buffer_size | 8388608 |
  
| innodb_log_file_size | 5242880 |
  
| innodb_log_files_in_group | 2 |
  
| innodb_log_group_home_dir | ./ |
  
| innodb_mirrored_log_groups | 1 |
  
| log | OFF |
  
| log_bin | ON |
  
| log_bin_trust_function_creators | OFF |
  
| log_error | /mydata/data/stu18.magedu.com.err |定义错误日志
  
| log_output | FILE |
  
| log_queries_not_using_indexes | OFF |
  
| log_slave_updates | OFF |
  
| log_slow_queries | OFF |
  
| log_warnings | 1 是否把警告信息写入错误日志中
  
| max_binlog_cache_size | 18446744073709547520 |
  
| max_binlog_size | 1073741824 |
  
| max_binlog_stmt_cache_size | 18446744073709547520 |
  
| max_relay_log_size | 0 |
  
| relay_log | |
  
| relay_log_index | |
  
| relay_log_info_file | relay-log.info |
  
| relay_log_purge | ON |
  
| relay_log_recovery | OFF |
  
| relay_log_space_limit | 0 |
  
| slow_query_log | OFF |
  
| slow_query_log_file | /mydata/data/stu18-slow.log |
  
| sql_log_bin | ON |
  
| sql_log_off | OFF |
  
| sync_binlog | 0 |
  
| sync_relay_log | 0 |
  
| sync_relay_log_info | 0 |
  
+--------------+------------+
  
其中，log_error可以直接定义为文件路径，也可以为ON|OFF；log_warings只能使用1|0来定义开关启动。
  
更改错误日志位置可以使用log_error来设置形式如下:
  
[root@stu18 data]# vim /etc/my.cnf
  
[MySQLd]
  
Log_error=DIR/[filename]
  
解析: 其中，DIR参数指定错误日志的路径filename参数是错误日志的名称，没有指定该参数时默认为主机名。重启MySQL服务器即可生效。
  
查看MySQL错误日志:
  
[root@stu18 data]# tail -20 stu18.magedu.com.err
  
130813 15:30:50 InnoDB: Starting shutdown...
  
130813 15:30:51 InnoDB: Shutdown completed; log sequence number 1630920
  
130813 15:30:51 [Note] /usr/local/MySQL/bin/MySQLd: Shutdown complete
  
130813 15:30:52 MySQLd_safe MySQLd from pid file /mydata/data/stu18.magedu.com.pid ended
  
130813 15:30:53 MySQLd_safe Starting MySQLd daemon with databases from /mydata/data
  
130813 15:30:54 InnoDB: The InnoDB memory heap is disabled #禁用了InnoDB memory的堆功能。
  
130813 15:30:54 InnoDB: Mutexes and rw_locks use GCC atomic builtins #Mutexes (互斥量) 和 rw_locks (行级锁) 是GCC编译的是InnoDB内置的。
  
130813 15:30:54 InnoDB: Compressed tables use zlib 1.2.3 #默认压缩工具是zlib
  
130813 15:30:55 InnoDB: Initializing buffer pool, size = 128.0M #InnoDB引擎的缓冲池 (buffer pool) 的值大小
  
130813 15:30:55 InnoDB: Completed initialization of buffer pool
  
130813 15:30:55 InnoDB: highest supported file format is Barracuda.
  
130813 15:30:57 InnoDB: Waiting for the background threads to start
  
130813 15:30:58 InnoDB: 5.5.33 started; log sequence number 1630920
  
130813 15:30:58 [Note] Server hostname (bind-address): '0.0.0.0'; port: 3306
  
130813 15:30:58 [Note] - '0.0.0.0' resolves to '0.0.0.0'; #0.0.0.0会反解主机名，这里反解失败
  
130813 15:30:58 [Note] Server socket created on IP: '0.0.0.0'.
  
130813 15:30:58 [Note] Event Scheduler: Loaded 0 events #事件调度器没有任何事件，因为没有装载。
  
130813 15:30:58 [Note] /usr/local/MySQL/bin/MySQLd: ready for connections. #MySQL启动完成等待客户端的请求。
  
Version: '5.5.33-log' socket: '/tmp/MySQL.sock' port: 3306 Source distribution #创建一个本地sock用于本地连接。
  
删除错误日志:
  
在MySQL5.5.7之前: 数据库管理员可以删除很长时间之前的错误日志，以保证MySQL服务器上的硬盘空间。MySQL数据库中，可以使用MySQLadmin命令开启新的错误日志。MySQLadmin命令的语法如下: MySQLadmin –u root –pflush-logs也可以使用登录MySQL数据库中使用FLUSHLOGS语句来开启新的错误日志。
  
在MySQL5.5.7之后: 服务器将关闭此项功能。只能使用重命名原来的错误日志文件，手动冲洗日志创建一个新的: 方式如下:
  
[root@stu18 data]# mv stu18.magedu.com.err stu18.magedu.com.err.old
  
[root@stu18 data]# MySQLadmin flush-logs
  
[root@stu18 data]# ls
  
hellodb myclass MySQL-bin.000003 MySQL-bin.index stu18.magedu.com.pid ibdata1 MySQL MySQL-bin.000004 performance_schema ib_logfile0 MySQL-bin.000001 stu18.magedu.com.err test ib_logfile1 MySQL-bin.000002 stu18.magedu.com.err.old
  
更多信息请查阅官方文档: <http://dev.MySQL.com/doc/refman/5.5/en/error-log.html>
  
查询日志:
  
默认情况下查询日志是关闭的。由于查询日志会记录用户的所有操作，其中还包含增删查改等信息，在并发操作大的环境下会产生大量的信息从而导致不必要的磁盘IO，会影响MySQL的性能的。如若不是为了调试数据库的目的建议不要开启查询日志。
  
查看查询日志是否开启:
  
MySQL> SHOW GLOBAL VARIABLES LIKE '%log%';
  
+--------------+------------+
  
| Variable_name | Value |
  
+--------------+------------+
  
| back_log | 50 |
  
| binlog_cache_size | 32768 |
  
| binlog_direct_non_transactional_updates | OFF |
  
| binlog_format | MIXED |
  
| binlog_stmt_cache_size | 32768 |
  
| expire_logs_days | 0 |
  
| general_log | OFF #定义查询日志是否开启 |
  
| general_log_file | /mydata/data/stu18.log #定义查询日志的文件地址名称 |
  
| innodb_flush_log_at_trx_commit | 1 |
  
| innodb_locks_unsafe_for_binlog | OFF |
  
| innodb_log_buffer_size | 8388608 |
  
| innodb_log_file_size | 5242880 |
  
| innodb_log_files_in_group | 2 |
  
| innodb_log_group_home_dir | ./ |
  
| innodb_mirrored_log_groups | 1 |
  
| log | OFF #是否开启日志  (若开启则表示开启所有的日志功能)  |
  
| log_bin | ON |
  
| log_bin_trust_function_creators | OFF |
  
| log_error | /mydata/data/stu18.magedu.com.err |
  
| log_output | FILE #日志的输出的位置 |
  
| log_queries_not_using_indexes | OFF |
  
| log_slave_updates | OFF |
  
| log_slow_queries | OFF |
  
| log_warnings | 1 |
  
| max_binlog_cache_size | 18446744073709547520 |
  
| max_binlog_size | 1073741824 |
  
| max_binlog_stmt_cache_size | 18446744073709547520 |
  
| max_relay_log_size | 0 |
  
| relay_log | |
  
| relay_log_index | |
  
| relay_log_info_file | relay-log.info |
  
| relay_log_purge | ON |
  
| relay_log_recovery | OFF |
  
| relay_log_space_limit | 0 |
  
| slow_query_log | OFF |
  
| slow_query_log_file | /mydata/data/stu18-slow.log |
  
| sql_log_bin | ON |
  
| sql_log_off | OFF |
  
| sync_binlog | 0 |
  
| sync_relay_log | 0 |
  
| sync_relay_log_info | 0 |
  
+--------------+------------+
  
41 rows in set (0.00 sec)
  
拓展解析: 日志的输出位置一般有三种方式: file(文件)，table(表)，none(不保存)；其中前两个输出位置可以同时定义，none表示是开启日志功能但是记录日志信息。file就是通过general_log_file |/mydata/data/stu18.log 等方式定义的，而输出位置定义为表时查看日志的内容方式为:
  
MySQL> use MySQL; #在此数据库中
  
Database changed
  
MySQL> show tables;
  
+---------+
  
| Tables_in_MySQL |
  
+---------+
  
| columns_priv |
  
| db |
  
| event |
  
| func |
  
| general_log | #这个就是查询日志的表输出位置
  
| help_category |
  
| help_keyword |
  
| help_relation |
  
| help_topic
  
……………… |
  
+---------+
  
慢查询日志:
  
慢查询日志是用来记录执行时间超过指定时间的查询语句。通过慢查询日志，可以查找出哪些查询语句的执行效率很低，以便进行优化。一般建议开启，它对服务器性能的影响微乎其微，但是可以记录MySQL服务器上执行了很长时间的查询语句。可以帮助我们定位性能问题的。
  
查看慢查询日志的定义:
  
MySQL> SHOW GLOBAL VARIABLES LIKE '%log%';
  
| slow_query_log | OFF #定义慢查询日志的
  
| slow_query_log_file |/mydata/data/stu18-slow.log #输出方式为file (文件) 时定义慢查询日志的位置
  
启动和设置慢查询日志:
  
1. 通过配置文件my.cnf中的log-slow-queries选项可以开启慢查询日志；形式如下:
  
[root@stu18 data]# vim /etc/my.cnf
  
[MySQLd]
  
slow_query_log=1
  
log-slow-queries [= DIR/[filename] ]
  
其中，DIR参数指定慢查询日志的存储路径；filename参数指定日志的文件名，生成日志文件的完成名称为filename-slow.log。如果不指定存储路径，慢查询日志默认存储到MySQL数据库的数据文件下，如果不指定文件名，默认文件名为hostname-slow.log。
  
2. 通过登录MySQL服务器直接定义，方式如下:
  
首先要有全局权限；然后执行MySQL>set global slow_query_log=1;
  
时间默认超过多少的称为慢查询日志？
  
一般都是通过long_query_time选项来设置这个时间值，时间以秒为单位，可以精确到微秒。如果查询时间超过了这个时间值 (默认为10秒) ，这个查询语句将被记录到慢查询日志中。查看服务器默认时间值方式如下:
  
MySQL> SHOW GLOBAL VARIABLES LIKE 'long%';
  
+------+----+
  
| Variable_name | Value |
  
+------+----+
  
| long_query_time | 10.000000 |
  
+------+----+
  
1 row in set (0.04 sec)
  
注释: 其中这个慢查询时间并不是只表示语句自身执行超过10秒还包含由于其他资源被征用造成阻塞的查询执行时间或其他原因等都被记录到慢查询中。所以这个慢查的时长表示从查询开始到查询结束中间包含可能的任何原因所经历的所有时间。
  
测试是否可以记录日志:
  
MySQL> set globalslow_query_log=1; #开启慢查询日志
  
Query OK, 0 rowsaffected (0.35 sec)
  
MySQL> setsession long_query_time=0.001; #更改时间 (当前session中，退出则重置)
  
Query OK, 0 rowsaffected (0.00 sec)
  
MySQL> set globallong_query_time=0.001; #更改时间 (全局中，重启服务则重置)
  
MySQL> SHOWVARIABLES LIKE 'long%'; #查询定义时间
  
+------+----+
  
| Variable_name | Value |
  
+------+----+
  
| long_query_time |0.001000 |
  
+------+----+
  
1 row in set (0.00sec)
  
MySQL> showglobal variables like "%slow%"; #查看慢查询日志开启状态
  
+-------+----------+
  
| Variable_name | Value |
  
+-------+----------+
  
|log_slow_queries | ON |
  
|slow_launch_time | 2 |
  
|slow_query_log | ON |
  
|slow_query_log_file | /mydata/data/stu18-slow.log |
  
+-------+----------+
  
4 rows in set (0.03sec)
  
查看慢查询日志:
  
MySQL> use MySQL
  
MySQL> selectuser,host,password from user where user="root";
  
+--+------+----+
  
| user | host | password |
  
+--+------+----+
  
| root |localhost | |
  
| root |stu18.magedu.com | |
  
| root |127.0.0.1 | |
  
| root | ::1 | |
  
+--+------+----+
  
4 rows in set (0.08sec) #查询时间为0.08
  
MySQL> systemmore /mydata/data/stu18_slow.log #查询慢查询日志记录信息
  
/usr/local/MySQL/bin/MySQLd,Version: 5.5.33-log (Source distribution). started
  
with:
  
Tcp port: 3306 Unix socket: /tmp/MySQL.sock
  
Time Id Command Argument
  
>>>>>>>>>>>>>>>>部分已省略>>>>>>>>>>>>>>
  
# Time: 13100723:46:33
  
# User@Host:root[root] @ localhost []
  
# Query_time:0.108459 Lock_time: 0.000216 Rows_sent:4 Rows_examined: 6
  
SETtimestamp=1381160793;
  
selectuser,host,password from user where user="root";
  
事务日志:
  
事务日志 (InnoDB特有的日志) 可以帮助提高事务的效率。使用事务日志，存储引擎在修改表的数据时只需要修改其内存拷贝，再把改修改行为记录到持久在硬盘上的事务日志中，而不用每次都将修改的数据本身持久到磁盘。事务日志采用追加的方式，因此写日志的操作是磁盘上一小块区域内的顺序I/O，而不像随机I/O需要在磁盘的多个地方移动磁头，所以采用事务日志的方式相对来说要快得多。事务日志持久以后，内存中被修改的数据在后台可以慢慢的刷回到磁盘。目前大多数的存储引擎都是这样实现的，我们通常称之为预写式日志，修改数据需要写两次磁盘。
  
如果数据的修改已经记录到事务日志并持久化，但数据本身还没有写回磁盘，此时系统崩溃，存储引擎在重启时能够自动恢复这部分修改的数据。具有的恢复方式则视存储引擎而定。
  
查看事务日志的定义:
  
MySQL> SHOWGLOBAL VARIABLES LIKE '%log%';
  
+--------------+------------+
  
| Variable_name | Value |
  
+--------------+------------+
  
| innodb_flush_log_at_trx_commit | 1 #在事务提交时innodb是否同步日志从缓冲到文件中1表示事务以提交就同步不提交每隔一秒同步一次，性能会很差造成大量的磁盘I/O；定义为2表示只有在事务提交时才会同步但是可能会丢失整个事务 |
  
|innodb_locks_unsafe_for_binlog |OFF |
  
| innodb_log_buffer_size | 8388608 |
  
|innodb_log_file_size |5242880 |
  
| innodb_log_files_in_group | 2 #至少有两个 |
  
|innodb_log_group_home_dir |./ #定义innodb事务日志组的位置 |
  
|innodb_mirrored_log_groups |1 #表示对日志组做镜像 |
  
每个事务日志都是大小为5兆的文件:
  
[root@stu18 data]#ls -lh
  
-rw-rw-- 1 MySQLMySQL 5.0M Oct 7 23:36 ib_logfile0
  
-rw-rw-- 1 MySQLMySQL 5.0M Aug 12 01:06 ib_logfile1
  
二进制日志:
  
二进制日志也叫作变更日志，主要用于记录修改数据或有可能引起数据改变的MySQL语句，并且记录了语句发生时间、执行时长、操作的数据等等。所以说通过二进制日志可以查询MySQL数据库中进行了哪些变化。一般大小体积上限为1G。
  
二进制开启状态:
  
MySQL> showglobal variables like "%log_bin%";
  
+-----------+---+
  
| Variable_name | Value |
  
+-----------+---+
  
| log_bin | ON | #已开启
  
|log_bin_trust_function_creators | OFF |
  
| sql_log_bin | ON |
  
+-----------+---+
  
二进制日志相关的参数:
  
MySQL> showglobal variables like "%log%";
  
sql_log_bin ={ON|OFF} #用于控制会话级别二进制日志功能的开启或关闭。默认为ON，表示启用记录功能。用户可以在会话级别修改此变量的值，但其必须具有SUPER权限。
  
binlog_cache_size =32768 #默认值32768 Binlog Cache用于在打开了二进制日志 (binlog) 记录功能的环境，是MySQL 用来提高binlog的记录效率而设计的一个用于短时间内临时缓存binlog数据的内存区域。一般来说，如果我们的数据库中没有什么大事务，写入也不是特别频繁，2MB～4MB是一个合适的选择。但是如果我们的数据库大事务较多，写入量比较大，可与适当调高binlog_cache_size。同时，我们可以通过binlog_cache_use 以及 binlog_cache_disk_use来分析设置的binlog_cache_size是否足够，是否有大量的binlog_cache由于内存大小不够而使用临时文件 (binlog_cache_disk_use) 来缓存了。
  
binlog_stmt_cache_size= 32768 #当非事务语句使用二进制日志缓存，但是超出binlog_stmt_cache_size时，使用一个临时文件来存放这些语句。
  
log_bin = MySQL-bin#指定binlog的位置，默认在数据目录下。
  
binlog-format= {ROW|STATEMENT|MIXED} #指定二进制日志的类型，默认为MIXED。如果设定了二进制日志的格式，却没有启用二进制日志，则MySQL启动时会产生警告日志信息并记录于错误日志中。
  
sync_binlog = 10#设定多久同步一次二进制日志至磁盘文件中，0表示不同步，任何正数值都表示对二进制每多少次写操作之后同步一次。当autocommit的值为1时，每条语句的执行都会引起二进制日志同步，否则，每个事务的提交会引起二进制日志同步
  
max_binlog_cache_size= {4096 .. 18446744073709547520} #二进定日志缓存空间大小，5.5.9及以后的版本仅应用于事务缓存，其上限由max_binlog_stmt_cache_size决定。
  
max_binlog_stmt_cache_size= {4096 .. 18446744073709547520} #二进定日志缓存空间大小，5.5.9及以后的版本仅应用于事务缓存
  
expire_log_days ={0..99} #设定二进制日志的过期天数，超出此天数的二进制日志文件将被自动删除。默认为0，表示不启用过期自动删除功能。如果启用此功能，自动删除工作通常发生在MySQL启动时或FLUSH日志时。
  
二进制日志定义方式:
  
其一、log_bin可以直接定义为文件路径，也可以为ON|OFF。
  
其二、通过编辑my.cnf中的log-bin选项可以开启二进制日志；形式如下:
  
[root@stu18 ~]#my.cnf
  
[MySQLd]
  
log-bin [=DIR \ [filename]]
  
其中，DIR参数指定二进制文件的存储路径；filename参数指定二级制文件的文件名，其形式为filename.number，number的形式为000001、000002等。每次重启MySQL服务或运行MySQL> flush logs;都会生成一个新的二进制日志文件，这些日志文件的number会不断地递增。除了生成上述的文件外还会生成一个名为filename.index的文件。这个文件中存储所有二进制日志文件的清单又称为二进制文件的索引。
  
[root@stu18 ~]# cd /mydata/data/
  
[root@stu18 data]#ls -lh
  
-rw-rw-- 1 MySQLMySQL 14K Aug 13 15:30 MySQL-bin.000001
  
-rw-rw-- 1 MySQLMySQL 150 Aug 13 17:05 MySQL-bin.000002
  
-rw-rw-- 1 MySQLMySQL 150 Aug 13 17:06 MySQL-bin.000003
  
-rw-rw-- 1 MySQLMySQL 150 Aug 13 17:07 MySQL-bin.000004
  
-rw-rw-- 1 MySQLMySQL 150 Aug 13 17:39 MySQL-bin.000005
  
-rw-rw-- 1 MySQLMySQL 126 Aug 13 19:03 MySQL-bin.000006
  
-rw-rw-- 1 MySQLMySQL 126 Aug 13 19:03 MySQL-bin.000007
  
-rw-rw-- 1 MySQLMySQL 126 Aug 13 19:05 MySQL-bin.000008
  
-rw-rw-- 1 MySQLMySQL 107 Aug 13 19:05 MySQL-bin.000009
  
-rw-rw-- 1 MySQLMySQL 353 Oct 7 23:40 MySQL-bin.000010
  
-rw-rw-- 1 MySQLMySQL 190 Oct 7 20:43 MySQL-bin.index
  
[root@stu18 data]#cat MySQL-bin.index
  
./MySQL-bin.000001
  
./MySQL-bin.000002
  
./MySQL-bin.000003
  
./MySQL-bin.000004
  
./MySQL-bin.000005
  
./MySQL-bin.000006
  
./MySQL-bin.000007
  
./MySQL-bin.000008
  
./MySQL-bin.000009
  
./MySQL-bin.000010
  
如果说我们向某个表的某个字段插入一个数据而这个数据为当前时间(日期时间型)；过段时间将此二进制文件应用到另一台服务器上数据就会变动从而导致数据的不一致性所以说对于这种非确定性的数据使用默认的语句定义并不是可靠的；
  
二进制日志中常用的定义格式:
  
1. 语句(statement): 默认的记录格式；
  
2. 行(row): 定义的并非数据本身而是这一行的数据是什么；
  
3. 混合模式(mixed): 交替使用行和语句、由MySQL服务器自行判断。
  
其中基于行的定义格式数据量会大一些但是可以保证数据的精确性。
  
查看二进制日志:
  
二进制日志的定义方式为二进制格式；使用此格式可以存储更多的信息，并且可以使写入二进制日志的效率更高。但是不能直接使用查看命令打开并查看二进制日志。
  
MySQL> showbinary logs; #显示当前服务器使用的二进制文件及大小
  
+------+----+
  
| Log_name | File_size |
  
+------+----+
  
| MySQL-bin.000001| 13814 |
  
| MySQL-bin.000002| 150 |
  
| MySQL-bin.000003| 150 |
  
| MySQL-bin.000004| 150 |
  
| MySQL-bin.000005| 150 |
  
| MySQL-bin.000006| 126 |
  
| MySQL-bin.000007| 126 |
  
| MySQL-bin.000008| 126 |
  
| MySQL-bin.000009| 107 |
  
| MySQL-bin.000010| 353 |
  
+------+----+
  
10 rows in set (0.07sec)
  
MySQL> showmaster logs; #显示主服务器使用的二进制文件及大小
  
+------+----+
  
| Log_name | File_size |
  
+------+----+
  
| MySQL-bin.000001| 13814 |
  
| MySQL-bin.000002| 150 |
  
| MySQL-bin.000003| 150 |
  
| MySQL-bin.000004| 150 |
  
| MySQL-bin.000005| 150 |
  
| MySQL-bin.000006| 126 |
  
| MySQL-bin.000007| 126 |
  
| MySQL-bin.000008| 126 |
  
| MySQL-bin.000009| 107 |
  
| MySQL-bin.000010| 353 |
  
+------+----+
  
10 rows in set (0.02sec)
  
MySQL> showmaster status; #当前使用的二进制文件及所处位置
  
+------+----+-----+------+
  
| File | Position | Binlog_Do_DB |Binlog_Ignore_DB |
  
+------+----+-----+------+
  
| MySQL-bin.000010| 353 | | |
  
+------+----+-----+------+
  
1 row in set (0.00sec)
  
小扩展: 二进制日志的记录位置: 通常为上一个事件执行结束时间的位置，每一个日志文件本身也有自己的元数据所以说对于当前版本的MySQL来说二进制的开始位置通常为107；
  
MySQL> flushlogs;
  
Query OK, 0 rowsaffected (0.23 sec)
  
注意: flush logs一般只会滚动中继日志和二进制日志。
  
MySQL> showmaster status;
  
+------+----+-----+------+
  
| File | Position | Binlog_Do_DB |Binlog_Ignore_DB |
  
+------+----+-----+------+
  
| MySQL-bin.000011| 107 | | |
  
+------+----+-----+------+
  
1 row in set (0.00sec)
  
查看当前二进制文件的信息:
  
MySQL> createdatabase yong;
  
Query OK, 1 rowaffected (0.12 sec)
  
MySQL> createtable yong.tb1 (id int,name char(20));
  
Query OK, 0 rowsaffected (0.44 sec)
  
MySQL> insertinto yong.tb1 values(1,'tom');
  
Query OK, 1 rowaffected (0.14 sec)
  
MySQL> showmaster status;
  
+------+----+-----+------+
  
| File | Position | Binlog_Do_DB |Binlog_Ignore_DB |
  
+------+----+-----+------+
  
| MySQL-bin.000011| 479 | | |
  
+------+----+-----+------+
  
1 row in set (0.00sec)
  
查看二进制日志信息的命令:
  
SHOW BINLOG EVENTS[IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
  
MySQL> showbinlog events\G #查看所有的二进制信息
  
\***\***\***\***\***\***\***\***\*\\*\*87. row \*\*\***\***\***\***\***\***\***\****
  
Log_name: MySQL-bin.000001
  
Pos: 13580
  
Event_type: Query
  
Server_id: 1
  
End_log_pos: 13688
  
Info: use \`hellodb\`; /*!40000 ALTERTABLE \`toc\` DISABLE KEYS*/
  
\***\***\***\***\***\***\***\***\*\\*\*88. row \*\*\***\***\***\***\***\***\***\****
  
Log_name: MySQL-bin.000001
  
Pos: 13688
  
Event_type: Query
  
Server_id: 1
  
End_log_pos: 13795
  
Info: use \`hellodb\`; /*!40000 ALTERTABLE \`toc\` ENABLE KEYS*/
  
\***\***\***\***\***\***\***\***\*\\*\*89. row \*\*\***\***\***\***\***\***\***\****
  
Log_name: MySQL-bin.000001
  
Pos: 13795
  
Event_type: Stop
  
Server_id: 1
  
End_log_pos: 13814
  
Info:
  
89 rows in set (0.00sec)
  
MySQL> showbinlog events in 'MySQL-bin.000011'; #查看指定日志的二进制信息
  
+------+--+-----+----+-----+----------------+
  
| Log_name | Pos | Event_type | Server_id | End_log_pos | Info |
  
+------+--+-----+----+-----+----------------+
  
| MySQL-bin.000011| 4 | Format_desc | 1 | 107 | Server ver: 5.5.33-log, Binlogver: 4 |
  
| MySQL-bin.000011 |107 | Query | 1 | 190 | create database yong |
  
| MySQL-bin.000011 |190 | Query | 1 | 293 | create table yong.tb1 (idint,name char(20)) |
  
| MySQL-bin.000011 |293 | Query | 1 | 357 | BEGIN |
  
| MySQL-bin.000011 |357 | Query | 1 | 452 | insert into yong.tb1values(1,'tom') |
  
| MySQL-bin.000011 |452 | Xid | 1 | 479 | COMMIT /*xid=103*/ |
  
+------+--+-----+----+-----+----------------+
  
6 rows in set (0.00sec)
  
MySQL> showbinlog events in 'MySQL-bin.000011' from 190; #从指定的事件位置开始
  
+------+--+----+----+-----+----------------+
  
| Log_name | Pos | Event_type | Server_id |End_log_pos | Info |
  
+------+--+----+----+-----+----------------+
  
| MySQL-bin.000011 |190 | Query | 1 | 293 | create table yong.tb1 (idint,name char(20)) |
  
| MySQL-bin.000011 |293 | Query | 1 | 357 | BEGIN |
  
| MySQL-bin.000011 |357 | Query | 1 | 452 | insert into yong.tb1values(1,'tom') |
  
| MySQL-bin.000011 |452 | Xid | 1 | 479 | COMMIT /*xid=103*/ |
  
+------+--+----+----+-----+----------------+
  
4 rows in set (0.00sec)
  
MySQL> showbinlog events in 'MySQL-bin.000011' from 190 limit 3; #指定偏移量(不是语句，是事件)
  
+------+--+----+----+-----+----------------+
  
| Log_name | Pos | Event_type | Server_id |End_log_pos | Info |
  
+------+--+----+----+-----+----------------+
  
| MySQL-bin.000011 |190 | Query | 1 | 293 | create table yong.tb1 (idint,name char(20)) |
  
| MySQL-bin.000011 |293 | Query | 1 | 357 | BEGIN |
  
| MySQL-bin.000011 |357 | Query | 1 | 452 | insert into yong.tb1values(1,'tom') |
  
+------+--+----+----+-----+----------------+
  
3 rows in set (0.00sec)
  
命令行下查看二进制日志:
  
由于无法使用cat等方式直接打开并查看二进制日志；所以必须使用MySQLbinlog命令。但是当正在执行MySQL读写操作时建议不要使用此打开正在使用的二进制日志文件；若非要打开可flush logs。MySQLbinlog命令的使用方式:
  
[root@stu18 data]#MySQLbinlog MySQL-bin.000017 #必须在数据目录下
  
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;
  
/*!40019 SET@@session.max_insert_delayed_threads=0*/;
  
/*!50003 SET@OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
  
DELIMITER /*!*/;
  
# at 4 #事件开始处
  
# 131009 0:25:59 server id 1 end_log_pos 107 Start: binlog v 4, server v 5.5.33-log created 131009 0:25:59
  
# Warning: thisbinlog is either in use or was not closed properly
  
BINLOG '
  
FzJUUg8BAAAAZwAAAGsAAAABAAQANS41LjMzLWxvZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  
AAAAAAAAAAAAAAAAAAAAAAAAEzgNAAgAEgAEBAQEEgAAVAAEGggAAAAICAgCAA==
  
'/*!*/;
  
# at 107
  
# 131009 0:26:36 server id 1 end_log_pos 192 Query thread_id=12 exec_time=0 error_code=0 #131009 0:26:36年月日的简写方式；end_log_pos事件结束处；thread_id=12 哪个会话线程创建的此语句；exec_time=0 执行时长单位为秒；error_code=0 错误代码0表示没有
  
SET TIMESTAMP=1381249596/*!*/; #预设信息(环境设定)
  
导出此数据库的信息:
  
[root@stu18 data]#MySQLbinlog MySQL-bin.000017 > /tmp/a.sql
  
导入此数据库的信息:
  
[root@stu18 data]#MySQL < a.sql
  
删除二进制日志信息:
  
二进制日志会记录大量的信息 (其中包含一些无用的信息) 。如果很长时间不清理二进制日志，将会浪费很多的磁盘空间。但是，删除之后可能导致数据库崩溃时无法进行恢复，所以若要删除二进制日志首先将其和数据库备份一份，其中也只能删除备份前的二进制日志，新产生的日志信息不可删(可以做即时点还原)。也不可在关闭MySQL服务器之后直接删除因为这样可能会给数据库带来错误的。若非要删除二进制日志需要做如下操作: 导出备份数据库和二进制日志文件进行压缩归档存储。删除二进制文件的方法如下:
  
1. 删除所有的二进制日志 (不可效仿) :
  
使用RESET MASTER语句可以删除所有的二进制日志。该语句的形式如下:
  
MySQL> resetmaster;
  
Query OK, 0 rowsaffected (0.17 sec)
  
MySQL> showbinary logs;
  
+------+----+
  
| Log_name | File_size |
  
+------+----+
  
| MySQL-bin.000001| 107 |
  
+------+----+
  
1 row in set (0.04sec)
  
解析: 首先不建议在生产环境下使用此操作；删除所有的二进制日志后，MySQL将会重新创建新的二进制日志。新二进制日志的编号从000001开始。
  
2. 根据文件或时间点来删除二进制日志:
  
语法形式:
  
MySQL> PURGE { BINARY | MASTER } LOGS {TO 'log_name' | BEFORE datetime_expr }
  
其中TO'log_name'表示把这个文件之前的其他文件都删除掉，也可使用BEFORE datetime_expr指定把哪个时间之前的二进制文件删除了。
  
MySQL> PURGEBINARY LOGS TO 'MySQL-bin.000007';
  
Query OK, 0 rowsaffected (0.11 sec)
  
MySQL> showbinary logs;
  
+------+----+
  
| Log_name | File_size |
  
+------+----+
  
| MySQL-bin.000007| 150 |
  
| MySQL-bin.000008| 150 |
  
| MySQL-bin.000009| 150 |
  
| MySQL-bin.000010| 150 |
  
| MySQL-bin.000011| 150 |
  
| MySQL-bin.000012| 150 |
  
| MySQL-bin.000013| 150 |
  
| MySQL-bin.000014| 150 |
  
| MySQL-bin.000015| 150 |
  
| MySQL-bin.000016| 150 |
  
| MySQL-bin.000017| 483 |
  
+------+----+
  
11 rows in set (0.04sec)
  
[root@stu18 data]#cat MySQL-bin.index
  
./MySQL-bin.000007
  
./MySQL-bin.000008
  
./MySQL-bin.000009
  
./MySQL-bin.000010
  
./MySQL-bin.000011
  
./MySQL-bin.000012
  
./MySQL-bin.000013
  
./MySQL-bin.000014
  
./MySQL-bin.000015
  
./MySQL-bin.000016
  
./MySQL-bin.000017
  
由此可以看出这种清理二进制日志文件的方式是非常合理的，不会导致数据库的错误发生。
  
MySQL> PURGEBINARY LOGS BEFORE '13-10-19 10:26:36'; #使用时间来删除二进制日志
  
Query OK, 0 rowsaffected (0.05 sec)

<http://pangge.blog.51cto.com/6013757/1319304>

<http://hone033.iteye.com/blog/451100>
