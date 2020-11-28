---
title: Oracle实例和Oracle数据库
author: w1100n
type: post
date: 2015-07-01T01:41:30+00:00
url: /?p=8002
categories:
  - Uncategorized

---
http://blog.csdn.net/leshami/article/details/5529239


Oracle实例和Oracle数据库(Oracle体系结构)
  
分类： Oracle 体系结构2010-04-26 11:47 26118人阅读 评论(13) 收藏 举报
  
oracle数据库sql server服务器server系统监控
  
-==========================================

-Oracle实例和Oracle数据库(Oracle体系结构)

-==========================================

/*

对于初接触Oracle 数据库的人来讲，很容易混淆的两个概念即是Oracle 实例和Oracle 数据库。这两

概念不同于SQL sever下的实例与数据库，当然也有些相似之处。只是在SQL server我们根本不需要花费太

多的精力去搞清SQL实例和数据库，因为它简单易于理解。下面简要说明一下SQL实例、数据库，更多的是讲

述Oracle下的实例及数据库。


一、SQL server中的实例与数据库

1.SQL中的实例指的是一个SQL server服务器上仅有一个缺省实例。缺省实例名即为机器名ServerName

(或IP)，如果在同一台机器上再安装SQL server，我们可以对实例命名如ServerName/InstanceName。

即一台SQL server服务器上可以存在多个不同的实例。一个实例下可以存在多个不同的数据库。

对于不同实例下的数据库的访问，使用ServerName/InstanceName：PortNo即可实现访问，缺省实例

为ServerName：PortNo。

2.对不同的实例配置IP地址，相关的访问协议，端口等等。

3.实例的可访问性需要启动该实例对应的相关服务。此处需要注意的是实例名和实例的服务名并不是相

同的。缺省的实例的服务名为MSSQLSERVER，而命名实例的服务名为MSSQL$INSTANCE_NAME。

4.实例的相关功能性的设置可以通过外围应用配置来实现。

5.上述完成后，即可实现对数据库的访问。

二、Oracle 实例

一个Oracle Server由一个Oracle实例和一个Oracle数据库组成。

即：Oracle Server = Oracle Instance + Oracle Database

Oracle实例

包括了内存结构(SGA)和一系列后台进程(Background Process),两者合起来称为一个Oracle实例

即：Oracle Instance = SGA + Background Process

Oracle内存结构

包含系统全局区(SGA)和程序全局区(PGA)

即Oracle Memory Structures = SGA + PGA

SGA由服务器和后台进程共享

PGA包含单个服务器进程或单个后台进程的数据和控制信息,与几个进程共享的SGA 正相反，PGA是

只被一个进程使用的区域，PGA 在创建进程时分配在终止进程时回收。即由服务器进程产生。


1.SGA

系统全局区SGA，SGA = 数据缓冲区+ 重做日志缓冲区+ 共享池+ 大池+ Java 池+ 流池

系统全局区是动态的，由参数SGA＿MAX＿SIZE决定。

查看当前系统的SGA大小：show parameter sga\_max\_size;

要修改：alter system set sga\_max\_size=1200m scope=spfile;

因为实例内存的分配是在数据库启动时进行的，所以要让修改生效，要重启数据库。


ORACLE 10G 引入了ASMM（自动共享内存管理），DBA只需设置SGA＿TARGET，ORACLE就会

自动的对共享池、JAVA池、大池、数据缓冲区、流池进行自动调配。取消自动调配就是

sga_target设为。


数据缓冲区(Database buffer cache):存储从数据文件中获得的数据块的镜像

大小由db\_cache\_size 决定

查看：show parameter db\_cache\_size;

设置：alter system set db\_cache\_size=800M;


重做日志缓冲区(Redo log buffer):对数据库的任何修改都按顺序被记录在该缓冲，然后由LGWR进程将

它写入磁盘,大小由LOG＿BUFFER决定


共享池(Shared pool):是SGA中最关键的内存片段,共享池主要由库缓存(共享SQL区和PL/SQL区)和数据

字典缓存组成，它的作用是存放频繁使用的sql，在有限的容量下，数据库系统根据一定的算法决

定何时释放共享池中的sql。

库缓存大小由shared\_pool\_size 决定

查看：show parameter shared\_pool\_size

修改：alter system set shared\_pool\_size=120m;


数据字典缓存：

存储数据库中数据文件、表、索引、列、用户和其它数据对象的定义和权限信息

大小由shared\_pool\_size 决定，不能单独指定


大池(Large pool):是一个可选的区域，用于一些大型的进程如Oracle的备份恢复操作、IO服务器进程等


Java 池：该程序缓冲区就是为Java 程序保留的。如果不用Java程序没有必要改变该缓冲区的默认大小


流池(Stream pool)：被Oracle流所使用


2.PGA

是为每个用户进程连接ORACLE数据库保留的内存

进程创建时分配，进程结束时释放，只能被一个进程使用

PGA包括了以下几个结构：

（）排序区

（）游标状态区

（）会话信息区

（）堆栈区

由参数：pga\_aggregate\_target 决定


3.几类进程：用户进程，服务器进程，后台进程，其它可选进程

用户进程

在用户连接数据库产生，请求oracle服务器连接，必须要先建立一个连接，不会直接和oracle服务器连接

服务器进程

当连接实例并建立用户会话时产生，独立服务器或者提供共享服务器都能产生

后台进程

维持物理和内存之间的联系，用来管理数据库的读写，恢复和监视等工作。

Server Process主要是通过他和user process进行联系和沟通，并由他和user process进行数据的交换。

在Unix机器上，Oracle后台进程相对于操作系统进程，也就是说，一个Oracle后台进程将启动一个操作

系统进程。

在Windows机器上，Oracle后台进程相对于操作系统线程，打开任务管理器，我们只能看到一个

ORACLE.EXE的进程，但是通过另外的工具，就可以看到包含在这里进程中的线程。


必须要有的后台进程

DBWn       ->数据库写进程

PMON       ->程序监控进程

SMON       ->系统监控进程

LGWr       ->日志写进程

CKPT       ->检查点进程


可选进程：

ARCN       归档进程

RECO

Snnn

pnnn


DBWn(数据库写进程)

负责将修改过的数据块从数据库缓冲区高速缓存写入磁盘上的数据文件中

写入条件：

发生检查点

脏缓存达到限制

没有自由的缓存

超时发生

表空间离线

表空间只读

表被删除或者截断

开始备份表空间

可以修改数据写进程的数量

alter system set db\_writer\_processes=3 scope=spfile;

PMON(程序监控进程)

清除失效的用户进程，释放用户进程所用的资源。

如PMON将回滚未提交的工作，释放锁，释放分配给失败进程的SGA资源。

清除失败的进程

回滚事务

释放锁

释放其他资源


SMON(系统监控进程)

检查数据库的一致性,当启动失败时完成灾难恢复等

实列恢复时，前滚所有重做日志中的文件，打开数据库为了用户能访问，回滚未提交的事务，释放临时表空间

清除临时空间，聚结空闲空间，从不可用的文件中恢复事务的活动，OPS中失败节点的实例恢复

清除OBJ$表

缩减回滚段

使回滚段脱机


LGWr(日志写进程)

将重做日志缓冲区中的更改写入在线重做日志文件

条件：

提交的时候（commit)

redo log buffer达到1／3满

每隔3秒

有大于1MB 重做日志缓冲区未被写入磁盘

DBWR需要写入的数据的SCN号大于LGWR 记录的SCN号，DBWR 触发LGWR写入

超时

在dbwr进程些之前写日志


CKPT(检查点进程)

DBWR/LGWR的工作原理，造成了数据文件，日志文件，控制文件的不一致，CKPT进程负责同步数据文件，

日志文件和控制文件

CKPT会更新数据文件/控制文件的头信息

条件：

在日志切换的时候

数据库用immediate ，transaction ，normal选项shutdown数据库的时候

根据初始话文件LOG\_CHECKPOINT\_INTERVAL、LOG\_CHECKPOINT\_TIMEOUT、FAST\_START\_IO_TARGET 的设置的数值来确定

用户触发


ARCN(归档进程)

在每次日志切换时把已满的日志组进行备份或归档

条件：

数据库以归档方式运行的时候


RECO

负责解决分布事物中的故障。Oracle可以连接远程的多个数据库，当由于网络问题，有些事物处于悬而未决的状态。

RECO进程试图建立与远程服务器的通信，当故障消除后，RECO进程自动解决所有悬而未决的会话。


Server Process(服务进程)

分为专用服务进程(Dedicated Server Process)和共享服务进程(MultiTreaded Server Process)

专用服务进程：一个服务进程对应多个用户进程，轮流为用户进程服务。


用户进程(User Process)、服务进程(Server Process)、后台进程(Background Processes)的启动

用户进程: 数据库用户请求Oralce server会话时被启动

服务进程：当用户会话启动后，连接到Oracle实例时该进程被启动

后台进程：当Oracle实例被启动时，启动相关的后台进程


三、Oracle 数据库

一系列物理文件的集合

包括控制文件、数据文件、联机日志文件、参数文件、密码文件等

即：Oracle Database = Controlfile + datafile + logfiel + spfile +..

1.控制文件(controlfile)

数据库的名字，检查点信息，数据库创建的时间戳

所有的数据文件，联机日志文件，归档日志文件信息

备份信息等


2.数据文件(datafile)

包含了用户和应用程序的所有数据

-查看数据文件信息

3.联机日志文件

记录了用户对数据库的所有操作，一个数据库中至少要有两个日志组文件，每个日志组中至少有一个日志成员

日志组中的多个日志成员是互为镜相关系


4.归档日志文件

Oracle可以运行在两种模式之中，归档模式和非归档模式。在归档模式中，为了保存用户的所有修改，

在联机日志文件切换后和被覆盖之间系统将他们另外保存成一组连续的文件系列，该文件系列就是归档日志文件。

用户恢复意外情况出现的数据丢失、异常等。


5.参数文件(pfile和spfile)

initSID.ora或init.ora文件,通常位于：$ORACLE_BASE/admin/<SID>/pfile

初始化文件记载了许多数据库的启动参数，如内存，控制文件，进程数等，在数据库启动的时候加载(Nomount时加载)


6.其他文件

密码文件：用于Oracle 的具有sysdba权限用户的认证.

告警日志文件：报警日志文件(alert.log或alrt.ora），记录数据库启动，关闭和一些重要的出错信息

查看路径：select value from v$PARAMETER where name ='background\_dump\_dest';


7.数据库逻辑组织结构

表空间、段、区、块

一个数据库由一个或多个表空间组成，一个表空间只能属于一个数据库

一个表空间由一个或多个多个数据文件组成，一个数据文件只能属于一个表空间

一个数据文件由一个或多个操作系统块组成，每一个操作系统块只能数以一个数据文件

一个表空间可以包含一个或多个段，一个段只能属于一个表空间

一个段由一个或多个区组成，每一个区只能属于一个段

一个区由一个或多个Oracle 块组成，每一个Oracle块只能属于一个区

一个区只能属于一个数据文件，数据文件的空间可以分配到一个或多个区

一个Oracle 块由一个或多个操作系统块组成，一个操作系统块是一个Oracle块的一部分

四、Oracle实例和Oracle数据库的关系

1.一个实例能够装载及打开仅仅一个数据库

2.一个数据库能够被多个实例装载并打开

3.实例与数据库的对应关系是一对一或多对一的关系


五、更多   */


SQL/PLSQL 基础


Oralce 10g 使用DBCA创建数据库


使用Uniread实现SQLplus翻页功能


Linux (RHEL 5.4)下安装Oracle 10g R2


VmWare6.5.2下安装RHEL 5.4（配置Oracle安装环境）


Oracle相关