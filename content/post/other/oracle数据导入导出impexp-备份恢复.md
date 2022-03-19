---
title: Oracle 导入/导出  imp/exp 备份 恢复 dump
author: "-"
date: 2012-01-12T01:33:09+00:00
url: /?p=2136
categories:
  - DataBase

tags:
  - reprint
---
## Oracle 导入/导出  imp/exp 备份 恢复 dump
```bash

exp scott/123456@172.16.234.51/orcl file=d:export.dmp owner=(scott)

```

语法: 
  
imp/exp [username[/password[@service]]]

其中service是服务实例名,关于如何创建
  
服务实例名或者数据库SID在http://blog.sina.com.cn/s/blog_7ffb8dd501013e5v.html有记录

或者:  imp/exp [username[/password[@hostIp: 1521/DBsid]]]  DBsid是数据库sid
  
如: exp admin/123@192.168.3.186/orcl(这里没有写端口号，默认是1521)


exp scott/123456@192.168.xxx.144/orcl file=d:xxx.dmp


exp system/manager@orclA file=d:is.dmp owner=(wiloon)

imp system/manager@orclB file=d:test.dmp fromuser=wiloontouser=wiloontest

功能: Oracle数据导入导出imp/exp就相当与oracle数据还原与备份。大多情况都可以用Oracle数据导入导出完成数据的备份和还原 (不会造成数据的丢失) 。

Oracle有个好处，虽然你的电脑不是服务器，但是你装了oracle客户端，并建立了连接  (通过net8 assistant中本地——>服务命名 添加正确的服务命名

其实你可以想成是客户端与服务器端修了条路，然后数据就可以被拉过来了) 这样你可以把数据导出到本地，虽然可能服务器离你很远。你同样可以把dmp文件从本地导入到远处的数据库服务器中。

利用这个功能你可以构建俩个相同的数据库，一个用来测试，一个用来正式使用。

执行环境: 可以在SQLPLUS.EXE或者DOS (命令行) 中执行，DOS中可以执行时由于 在oracle 8i 中  安装目录ora81BIN被设置为全局路径，该目录下有EXP.EXE与IMP.EXE文件被用来执行导入导出。

oracle用java编写，我想SQLPLUS.EXE、EXP.EXE、IMP.EXE这俩个文件是被包装后的类文件。SQLPLUS.EXE调用EXP.EXE、IMP.EXE他们所包裹的类，完成导入导出功能。

下面介绍的是导入导出的实例，向导入导出看实例基本上就可以完成，因为导入导出很简单。

数据导出: 

1 将数据库TEST完全导出，用户名system 密码manager 导出到D: daochu.dmp中

exp system/manager@TEST file=d: daochu.dmp full=y

2 将数据库中system用户与sys用户的表导出

exp system/manager@TEST file=d: daochu.dmp owner= (system，sys) 

3 将数据库中的表table1 、table2导出

exp system/manager@TEST file=d: daochu.dmp tables= (table1，table2) 

4 将数据库中的表table1中的字段filed1以"00"打头的数据导出

exp system/manager@TEST file=d: daochu.dmp tables= (table1)  query=" where filed1 like '00%'"

上面是常用的导出，对于压缩我不太在意，用winzip把dmp文件可以很好的压缩。

不过在上面命令后面 加上 compress=y  就可以了

数据的导入1 将D: daochu.dmp 中的数据导入 TEST数据库中。

imp system/manager@TEST  file=d: daochu.dmp

上面可能有点问题，因为有的表已经存在，然后它就报错，对该表就不进行导入。

在后面加上 ignore=y 就可以了。

2 将d: daochu.dmp中的表table1 导入

imp system/manager@TEST  file=d: daochu.dmp  tables= (table1) 

基本上上面的导入导出够用了。不少情况我是将表彻底删除，然后导入。

注意: 

你要有足够的权限，权限不够它会提示你。

数据库时可以连上的。可以用tnsping TEST 来获得数据库TEST能否连上。


Oracle数据库有三种标准的备份方法，它们分别是导出/导入 (EXP/IMP) 、热备份和冷备份。导出备件是一种逻辑备份，冷备份和热备份是物理备份。一、 导出/导入 (Export/Import) 利用Export可将数据从数据库中提取出来，利用Import则可将提取出来的数据送回到Oracle数据库中去。１、 简单导出数据 (Export) 和导入数据 (Import) 

Oracle支持三种方式类型的输出: 

 (１) 、表方式 (T方式) ，将指定表的数据导出。

 (２) 、用户方式 (U方式) ，将指定用户的所有对象及数据导出。

 (３) 、全库方式 (Full方式) ，瘵数据库中的所有对象导出。

数据导入 (Import) 的过程是数据导出 (Export) 的逆过程，分别将数据文件导入数据库和将数据库数据导出到数据文件。

２、 增量导出/导入

增量导出是一种常用的数据备份方法，它只能对整个数据库来实施，并且必须作为SYSTEM来导出。在进行此种导出时，系统不要求回答任何问题。导出文件名缺省为export.dmp，如果不希望自己的输出文件定名为export.dmp，必须在命令行中指出要用的文件名。

增量导出包括三种类型: 

 (１) 、"完全"增量导出 (Complete) 

即备份三个数据库，比如: 


exp system/manager inctype=complete file=040731.dmp
  
 (２) 、"增量型"增量导出

备份上一次备份后改变的数据，比如: 


exp system/manager inctype=incremental file=040731.dmp
  
 (３) 、"累积型"增量导出

累计型导出方式是导出自上次"完全"导出之后数据库中变化了的信息。比如: 


exp system/manager inctype=cumulative file=040731.dmp
  
数据库管理员可以排定一个备份日程表，用数据导出的三个不同方式合理高效的完成。

比如数据库的被封任务可以做如下安排: 

星期一: 完全备份 (A) 

星期二: 增量导出 (B) 

星期三: 增量导出 (C) 

星期四: 增量导出 (D) 

星期五: 累计导出 (E) 

星期六: 增量导出 (F) 

星期日: 增量导出 (G) 

如果在星期日，数据库遭到意外破坏，数据库管理员可按一下步骤来回复数据库: 

第一步: 用命令CREATE DATABASE重新生成数据库结构；

第二步: 创建一个足够大的附加回滚。

第三步: 完全增量导入A: 


imp system/manager inctype=RESTORE FULL=y FILE=A
  
第四步: 累计增量导入E: 


imp system/manager inctype=RESTORE FULL=Y FILE=E
  
第五步: 最近增量导入F: 


imp system/manager inctype=RESTORE FULL=Y FILE=F
  


二、 冷备份

冷备份发生在数据库已经正常关闭的情况下，当正常关闭时会提供给我们一个完整的数据库。冷备份时将关键性文件拷贝到另外的位置的一种说法。对于备份Oracle信息而言，冷备份时最快和最安全的方法。冷备份的优点是: 

１、 是非常快速的备份方法 (只需拷文件) 

２、 容易归档 (简单拷贝即可) 

３、 容易恢复到某个时间点上 (只需将文件再拷贝回去) 

４、 能与归档方法相结合，做数据库"最佳状态"的恢复。

５、 低度维护，高度安全。

但冷备份也有如下不足: 

１、 单独使用时，只能提供到"某一时间点上"的恢复。

２、 再实施备份的全过程中，数据库必须要作备份而不能作其他工作。也就是说，在冷备份过程中，数据库必须是关闭状态。

３、 若磁盘空间有限，只能拷贝到磁带等其他外部存储设备上，速度会很慢。

４、 不能按表或按用户恢复。

如果可能的话 (主要看效率) ，应将信息备份到磁盘上，然后启动数据库 (使用户可以工作) 并将备份的信息拷贝到磁带上 (拷贝的同时，数据库也可以工作) 。冷备份中必须拷贝的文件包括: 

１、 所有数据文件

２、 所有控制文件

３、 所有联机REDO LOG文件

４、 Init.ora文件 (可选) 

值得注意的使冷备份必须在数据库关闭的情况下进行，当数据库处于打开状态时，执行数据库文件系统备份是无效的。

下面是作冷备份的完整例子。

 (1)  关闭数据库


sqlplus /nolog
  
sql>;connect /as sysdba
  
sql>;shutdown normal;
  
 (2)  用拷贝命令备份全部的时间文件、重做日志文件、控制文件、初始化参数文件


sql>;cp <file>; <backup directory>;
  
 (3)  重启Oracle数据库


sql>;startup
  
三、 热备份

热备份是在数据库运行的情况下，采用archivelog mode方式备份数据库的方法。所以，如果你有昨天夜里的一个冷备份而且又有今天的热备份文件，在发生问题时，就可以利用这些资料恢复更多的信息。热备份要求数据库在Archivelog方式下操作，并需要大量的档案空间。一旦数据库运行在archivelog状态下，就可以做备份了。热备份的命令文件由三部分组成: 

1． 数据文件一个表空间一个表空间的备份。

 (1)  设置表空间为备份状态

 (2)  备份表空间的数据文件

 (3)  回复表空间为正常状态

2． 备份归档log文件

 (1)  临时停止归档进程

 (2)  log下那些在archive rede log目标目录中的文件

 (3)  重新启动archive进程

 (4)  备份归档的redo log文件

3． 用alter database bachup controlfile命令来备份控制文件

热备份的优点是: 

1． 可在表空间或数据库文件级备份，备份的时间短。

2． 备份时数据库仍可使用。

3． 可达到秒级恢复 (恢复到某一时间点上) 。

4． 可对几乎所有数据库实体做恢复

5． 恢复是快速的，在大多数情况下爱数据库仍工作时恢复。

热备份的不足是: 

1． 不能出错，否则后果严重

2． 若热备份不成功，所得结果不可用于时间点的恢复

3． 因难于维护，所以要特别仔细小心，不允许"以失败告终"。


export 有四种备份方式: 完全，表空间，用户，表

exp [user]/[passwd]@[servername] file=文件路径 log=日志路径

例如: exp system/manager@10g file=d:\expdata.dmp log=d:\expdata.log full=y

如何查看oracle用户权限

1. oracle用户查看自己的权限和角色
  
select * from user_tab_privs;
  
select * from user_role_privs;

2. sys用户查看任一用户的权限和角色
  
select * from dba_tab_privs;
  
select * from dba_role_privs;


Oracle怎样进行远程备份


今天我找到了一个用doc命令的备份方法，简单记录如下: 
  
备份: 
  
exp 用户名/密码@要连接的远程计算机IP/要备份的远程数据库名称 file=文件路径
  
如: exp hom/hom@192.168.5.14/qa file=d:/aa1.dmp
  
还原: 
  
imp 用户名/密码@还原的数据库名称 file=文件路径+文件名称
  
事例:  imp hom1/hom1@192.168.5.14/qa full=y file=D:/aa1.dmp ignore=y


http://2342615.blog.51cto.com/2332615/803497
  
http://blog.sina.com.cn/s/blog_7ffb8dd501013mls.html

http://www.cnblogs.com/yingpp/archive/2009/01/07/1371040.html

http://2342615.blog.51cto.com/2332615/803497