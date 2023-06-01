---
title: MySQLslap
author: "-"
date: 2016-01-21T00:12:50+00:00
url: /?p=8691
categories:
  - Inbox
tags:
  - reprint
---
## MySQLslap

MySQLslap -uuser0 -ppassword0 -concurrency=1 -iterations=1 -engine=innodb -number-of-queries=20000 -debug-info -query="INSERT INTO xxxxxx"

MySQL数据库基准压力测试工具之MySQLSlap使用实例 2013-05-20 19:04:09
  
分类:  MySQL/postgreSQL
  
<http://www.2cto.com/database/201303/195303.html>

MySQL数据库基准压力测试工具之MySQLSlap使用实例

一、MySQLslap介绍
  
MySQLslap是MySQL5.1之后自带的benchmark基准测试工具,类似Apache Bench负载产生工具,生成schema,装载数据,执行benckmark和查询数据,语法简单,灵活,容易使用。该工具可以模拟多个客户端同时并发的向服务器发出查询更新,给出了性能测试数据而且提供了多种引擎的性能比较。MySQLslap为MySQL性能优化前后提供了直观的验证依据,笔者建议系统运维人员应该掌握一些常见的压力测试工具,这样才能较为准确的掌握线上系统能够支撑的用户流量上限及其抗压性等问题。  <www.2cto.com>
  
二、使用方法介绍
  
可以使用MySQLslap -help来显示使用方法:
  
1) -concurrency代表并发数量,多个可以用逗号隔开,例如: concurrency=10,50,100, 并发连接线程数分别是10、50、100个并发。
  
2) -engines代表要测试的引擎,可以有多个,用分隔符隔开。
  
3) -iterations代表要运行这些测试多少次。
  
4) -auto-generate-sql 代表用系统自己生成的SQL脚本来测试。
  
5) -auto-generate-sql-load-type 代表要测试的是读还是写还是两者混合的 (read,write,update,mixed)
  
6) -number-of-queries 代表总共要运行多少次查询。每个客户端运行的查询数量可以用查询总数/并发数来计算。
  
7) -debug-info 代表要额外输出CPU以及内存的相关信息。
  
8) -number-int-cols : 创建测试表的 int 型字段数量
  
9) -auto-generate-sql-add-autoincrement : 代表对生成的表自动添加auto_increment列,从5.1.18版本开始
  
10) -number-char-cols 创建测试表的 char 型字段数量。
  
11) -create-schema 测试的schema,MySQL中schema也就是database。
  
12) -query  使用自定义脚本执行测试,例如可以调用自定义的一个存储过程或者sql语句来执行测试。
  
13) -only-print 如果只想打印看看SQL语句是什么,可以用这个选项。
  
三、Demo实例
  
下面我们使用几个demo实例来进行测试
  
1. Demo1:
  
[root@localhost ~]# MySQLslap -uroot -p123abc -concurrency=100 -iterations=1 -auto-generate-sql -auto-generate-sql-load-type=mixed -auto-generate-sql-add-autoincrement -engine=myisam -number-of-queries=10 -debug-info
  
备注本次测试以100个并发线程、测试1次,自动生成SQL测试脚本、读、写、更新混合测试、自增长字段、测试引擎为myisam、共运行10次查询,输出cpu资源信息
  
返回信息如下所示:
  
rement -engine=myisam -number-of-queries=10 -debug-info
  
Benchmark
  
Running for engine myisam
  
Average number of seconds to run all queries: 0.129 seconds
  
Minimum number of seconds to run all queries: 0.107 seconds
  
Maximum number of seconds to run all queries: 0.264 seconds
  
Number of clients running queries: 100
  
Average number of queries per client: 0
  
User time 0.16, System time 0.25
  
Maximum resident set size 4624, Integral resident set size 0
  
Non-physical pagefaults 7346, Physical pagefaults 0, Swaps 0
  
Blocks in 0 out 0, Messages in 0 out 0, Signals 0
  
Voluntary context switches 27221, Involuntary context switches 4241
  
Demo2: 指定数据库和sql语句
  
MySQLslap -h192.168.202.84 -P3309 -concurrency=100 -iterations=1 -create-schema='mms_sdmtv' -query='select * from role;' -number-of-queries=10 -debug-info -uroot -p123abc
  
备注使用MySQLslap指定sql语句进行测试
  
Demo3: 测试用例
  
[root@localhost /]# MySQLslap -concurrency=50,100,200 -iterations=20 -number-int-cols=4 -number-char-cols=35 -auto-generate-sql -auto-generate-sql-add-autoincrement -auto-generate-sql-load-type=read -engine=myisam,innodb -number-of-queries=200 -verbose -socket=/var/lib/MySQL/MySQL.sock -uroot -p123abc
  
系统脚本测试,增加int型 4列char 型35列,测试2种引擎myisam,innodb读的性能,分别用50,100,200个客户端对服务器进行测试总共200个查询语句 执行20次查询
  
Benchmark
  
Running for engine myisam
  
Average number of seconds to run all queries: 0.666 seconds
  
Minimum number of seconds to run all queries: 0.223 seconds
  
Maximum number of seconds to run all queries: 4.889 seconds
  
Number of clients running queries: 50
  
Average number of queries per client: 4
  
Benchmark
  
Running for engine myisam
  
Average number of seconds to run all queries: 0.620 seconds
  
Minimum number of seconds to run all queries: 0.231 seconds
  
Maximum number of seconds to run all queries: 4.898 seconds
  
Number of clients running queries: 100
  
Average number of queries per client: 2
  
Benchmark
  
Running for engine myisam
  
Average number of seconds to run all queries: 0.503 seconds
  
Minimum number of seconds to run all queries: 0.257 seconds
  
Maximum number of seconds to run all queries: 4.269 seconds
  
Number of clients running queries: 200
  
Average number of queries per client: 1
  
Benchmark
  
Running for engine innodb
  
Average number of seconds to run all queries: 1.049 seconds
  
Minimum number of seconds to run all queries: 0.244 seconds
  
Maximum number of seconds to run all queries: 5.292 seconds
  
Number of clients running queries: 50
  
Average number of queries per client: 4
  
Benchmark
  
Running for engine innodb
  
Average number of seconds to run all queries: 0.712 seconds
  
Minimum number of seconds to run all queries: 0.246 seconds
  
Maximum number of seconds to run all queries: 6.585 seconds
  
Number of clients running queries: 100
  
Average number of queries per client: 2
  
Benchmark
  
Running for engine innodb
  
Average number of seconds to run all queries: 0.269 seconds
  
Minimum number of seconds to run all queries: 0.175 seconds
  
Maximum number of seconds to run all queries: 0.328 seconds
  
Number of clients running queries: 200
  
Average number of queries per client: 1
  
自建SQL测试用例
  
MySQLslap -create=/yourpath/Test1.sql -query=/yourpath/Test2.sql -concurrency=50,100,200 -iterations=20 -engine=myisam,innodb  -u root -p123abc
  
在设定的yourpath目录下创建你的测试sql文Test1及Test2并进行50、100及200的模拟并发测试

<http://blog.chinaunix.net/uid-177564-id-3711520.html>
