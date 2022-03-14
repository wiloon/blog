---
title: Interview – Database
author: lcf
date: 2012-11-27T14:55:38+00:00
url: /?p=4781
categories:
  - DataBase

tags:
  - reprint
---
## Interview – Database
## SQL tuning 类
### 列举几种表连接方式
等连接 (内连接) 、非等连接、自连接、外连接 (左、右、全)  Or hash join/merge join/nest loop(cluster join)/index join ？？ ORACLE 8i，9i 表连接方法。   一般的相等连接: 
select * from a, b where a.id = b.id; 这个就属于内连接。   
对于外连接:  Oracle中可以使用"(+) "来表示，9i可以使用LEFT/RIGHT/FULL OUTER JOIN   LEFT OUTER JOIN: 左外关联 SELECT e.last_name, e.department_id, d.department_name FROM employees e LEFT OUTER JOIN departments d ON (e.department_id = d.department_id); 等价于 SELECT e.last_name, e.department_id, d.department_name FROM employees e, departments d WHERE e.department_id=d.department_id(+) 结果为: 所有员工及对应部门的记录，包括没有对应部门编号department_id的员工记录。   RIGHT OUTER JOIN: 右外关联 SELECT e.last_name, e.department_id, d.department_name FROM employees e RIGHT OUTER JOIN departments d ON (e.department_id = d.department_id); 等价于 SELECT e.last_name, e.department_id, d.department_name FROM employees e, departments d WHERE e.department_id(+)=d.department_id 结果为: 所有员工及对应部门的记录，包括没有任何员工的部门记录。   FULL OUTER JOIN: 全外关联 SELECT e.last_name, e.department_id, d.department_name FROM employees e FULL OUTER JOIN departments d ON (e.department_id = d.department_id); 结果为: 所有员工及对应部门的记录，包括没有对应部门编号department_id的员工记录和没有任何员工的部门记录。   ORACLE8i是不直接支持完全外连接的语法，也就是说不能在左右两个表上同时加上(+)，下面是在ORACLE8i可以参考的完全外连接语法 select t1.id,t2.id from table1 t1,table t2 where t1.id=t2.id(+) union select t1.id,t2.id from table1 t1,table t2 where t1.id(+)=t2.id
  
  
    
      
         
        
        
          连接类型
        
      
      
      
        
          定义
        
      
      
      
        
          图示
        
      
      
      
        
          例子
        
      
    
    
    
      
        
          内连接
        
      
      
      
        
          只连接匹配的行
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A join B on A.c3 = B.c3;
        
      
    
    
    
      
        
          左外连接
        
      
      
      
        
          包含左边表的全部行 (不管右边的表中是否存在与它们匹配的行) 以及右边表中全部匹配的行
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A left join B on A.c3 = B.c3;
        
      
    
    
    
      
        
          右外连接
        
      
      
      
        
          包含右边表的全部行 (不管左边的表中是否存在与它们匹配的行) 以及左边表中全部匹配的行
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A right join B on A.c3 = B.c3;
        
      
    
    
    
      
        
          全外连接
        
      
      
      
        
          包含左、右两个表的全部行，不管在另一边的表中是否存在与它们匹配的行
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A full join B on A.c3 = B.c3;
        
      
    
    
    
      
        
           (theta) 连接
        
      
      
      
        
          使用等值以外的条件来匹配左、右两个表中的行
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A join B on A.c3 != B.c3;
        
      
    
    
    
      
        
          交叉连接
        
      
      
      
        
          生成笛卡尔积——它不使用任何匹配或者选取条件，而是直接将一个数据源中的每个行与另一个数据源的每个行一一匹配
        
      
      
      
      
      
      
        
          select A.c1,B.c2 from A,B;
        
      
    
  
  
  
    2.      不借助第三方工具，怎样查看sql的执行计划
  
  
    I) 使用Explain Plan,查询PLAN_TABLE; EXPLAIN  PLAN SET STATEMENT_ID='QUERY1' FOR SELECT * FROM a WHERE aa=1; SELECT   operation, options, object_name, object_type, ID, parent_id FROM plan_table WHERE STATEMENT_ID = 'QUERY1' ORDER BY ID; II)SQLPLUS中的SET TRACE 即可看到Execution Plan Statistics SET AUTOTRACE ON;
  
  
    3.      如何使用CBO,CBO与RULE的区别
  
  
    IF 初始化参数 OPTIMIZER_MODE = CHOOSE THEN  -(8I DEFAULT) IF 做过表分析 THEN 优化器 Optimizer=CBO(COST);          /*高效*/ ELSE 优化器 Optimizer=RBO(RULE);               /*高效*/ END IF; END IF;   区别:  RBO根据规则选择最佳执行路径来运行查询。 CBO根据表统计找到最低成本的访问数据的方法确定执行计划。 使用CBO需要注意:  I)  需要经常对表进行ANALYZE命令进行分析统计; II) 需要稳定执行计划; III)需要使用提示(Hint); 使用RULE需要注意:  I)  选择最有效率的表名顺序 II) 优化SQL的写法;     在optimizer_mode=choose时,如果表有统计信息 (分区表外) ,优化器将选择CBO,否则选RBO。 RBO遵循简单的分级方法学,使用15种级别要点，当接收到查询，优化器将评估使用到的要点数目,然后选择最佳级别 (最少的数量) 的执行路径来运行查询。 CBO尝试找到最低成本的访问数据的方法,为了最大的吞吐量或最快的初始响应时间,计算使用不同的执行计划的成本，并选择成本最低的一个,关于表的数据内容的统计被用于确定执行计划。
  
  
    4.      如何定位重要(消耗资源多)的SQL
  
  
    使用CPU多的用户session SELECT a.SID, spid, status, SUBSTR (a.program, 1, 40) prog, a.terminal,a.SQL_TEXT, osuser, VALUE / 60 / 100 VALUE FROM v$session a, v$process b, v$sesstat c WHERE c.statistic# = 12 AND c.SID = a.SID AND a.paddr = b.addr ORDER BY VALUE DESC;   select sql_text from v$sql where disk_reads > 1000 or (executions > 0 and buffer_gets/executions > 30000);
  
  
    5.      如何跟踪某个session的SQL
  
  
    利用TRACE 跟踪 ALTER SESSION SET SQLTRACE ON; COLUMN SQL format a200; SELECT   machine, sql_text SQL FROM v$sqltext a, v$session b WHERE address = sql_address AND machine = '&A' ORDER BY hash_value, piece;   exec dbms_system.set_sql_trace_in_session(sid,serial#,&sql_trace); select sid,serial# from v$session where sid = (select sid from v$mystat where rownum = 1); exec dbms_system.set_ev(&sid,&serial#,&event_10046,&level_12,");
  
  
    6.      SQL调整最关注的是什么
  
  
    检查系统的I/O问题 sar－d能检查整个系统的iostat (IO statistics)    查看该SQL的response time(db block gets/consistent gets/physical reads/sorts (disk))
  
  
### 说说你对索引的认识 (索引的结构、对dml影响、对查询影响、为什么提高查询性能) 
  
索引有B-TREE、BIT、CLUSTER等类型。ORACLE使用了一个复杂的自平衡B-tree结构;通常来说，在表上建立恰当的索引，查询时会改进查询性能。但在进行插入、删除、修改时，同时会进行索引的修改，在性能上有一定的影响。有索引且查询条件能使用索引时，数据库会先度取索引，根据索引内容和查询条件，查询出ROWID，再根据ROWID取出需要的数据。由于索引内容通常比全表内容要少很多，因此通过先读索引，能减少I/O，提高查询性能。   b-tree index/bitmap index/function index/patitional index(local/global)索引通常能提高select/update/delete的性能,会降低insert的速度,
  
  
    8.      使用索引查询一定能提高查询的性能吗？为什么
  
  
    通常,通过索引查询数据比全表扫描要快.但是我们也必须注意到它的代价. 索引需要空间来存储,也需要定期维护, 每当有记录在表中增减或索引列被修改时,索引本身也会被修改. 这意味着每条记录的INSERT,DELETE,UPDATE将为此多付出4,5 次的磁盘I/O. 因为索引需要额外的存储空间和处理,那些不必要的索引反而会使查询反应时间变慢.使用索引查询不一定能提高查询性能,索引范围查询(INDEX RANGE SCAN)适用于两种情况: 基于一个范围的检索,一般查询返回结果集小于表中记录数的30%宜采用; 基于非唯一性索引的检索   索引就是为了提高查询性能而存在的,如果在查询中索引没有提高性能,只能说是用错了索引,或者讲是场合不同
  
  
    9.      绑定变量是什么？绑定变量有什么优缺点？
  
  
    绑定变量是指在SQL语句中使用变量，改变变量的值来改变SQL语句的执行结果。 优点: 使用绑定变量，可以减少SQL语句的解析，能减少数据库引擎消耗在SQL语句解析上的资源。提高了编程效率和可靠性。减少访问数据库的次数, 就能实际上减少ORACLE的工作量。 缺点: 经常需要使用动态SQL的写法，由于参数的不同，可能SQL的执行效率不同；   绑定变量是相对文本变量来讲的,所谓文本变量是指在SQL直接书写查询条件， 这样的SQL在不同条件下需要反复解析,绑定变量是指使用变量来代替直接书写条件，查询bind value在运行时传递，然后绑定执行。 优点是减少硬解析,降低CPU的争用,节省shared_pool 缺点是不能使用histogram,sql优化比较困难
  
  
    10.  如何稳定(固定)执行计划
  
  
    可以在SQL语句中指定执行计划。使用HINTS; query_rewrite_enabled = true star_transformation_enabled = true optimizer_features_enable = 9.2.0 创建并使用stored outline
  
  
    11.  和排序相关的内存在8i和9i分别怎样调整，临时表空间的作用是什么
  
  
    SORT_AREA_SIZE 在进行排序操作时，如果排序的内容太多，内存里不能全部放下，则需要进行外部排序， 此时需要利用临时表空间来存放排序的中间结果。   8i中sort_area_size/sort_area_retained_size决定了排序所需要的内存， 如果排序操作不能在sort_area_size中完成,就会用到temp表空间 9i中如果workarea_size_policy=auto时, 排序在pga内进行,通常pga_aggregate_target的1/20可以用来进行disk sort; 如果workarea_size_policy=manual时,排序需要的内存由sort_area_size决定， 在执行order by/group by/distinct/union/create index/index rebuild/minus等操作时,如果在pga或sort_area_size中不能完成,排序将在临时表空间进行 (disk sort) ,临时表空间主要作用就是完成系统中的disk sort.
  
  
    12.  存在表T(a,b,c,d),要根据字段c排序后取第21—30条记录显示，请给出sql
  
  
    SELECT   * FROM (SELECT ROWNUM AS row_num, tmp_tab.* FROM (SELECT   a, b, c, d FROM T ORDER BY c) tmp_tab WHERE ROWNUM <= 30) WHERE row_num >= 20 ORDER BY row_num;   create table t(a number(,b number(,c number(,d number(); / begin for i in 1 .. 300 loop insert into t values(mod(i,2),i/2,dbms_random.value(1,300),i/4); end loop; end; / select * from (select c.*,rownum as rn from (select * from t order by c desc) c) where rn between 21 and 30; / select * from (select * from test order by c desc) x where rownum < 30 minus select * from (select * from test order by c desc) y where rownum < 20 order by 3 desc 相比之 minus性能较差
  
  
    二: 数据库基本概念类
  
  
  
    1 Pctused and pctfree 表示什么含义有什么作用
  
  
    pctused与pctfree控制数据块是否出现在freelist中,  pctfree控制数据块中保留用于update的空间,当数据块中的free space小于pctfree设置的空间时,该数据块从freelist中去掉,当块由于dml操作free space大于pct_used设置的空间时,该数据库块将被添加在freelist链表中。
  
  
    2 简单描述tablespace / segment / extent / block之间的关系
  
  
    tablespace: 一个数据库划分为一个或多个逻辑单位，该逻辑单位成为表空间;每一个表空间可能包含一个或多个 Segment; Segments: Segment指在tablespace中为特定逻辑存储结构分配的空间。每一个段是由一个或多个extent组成。包括数据段、索引段、回滚段和临时段。 Extents: 一个 extent 由一系列连续的 Oracle blocks组成.ORACLE为通过extent 来给segment分配空间。 Data Blocks: Oracle 数据库最小的I/O存储单位，一个data block对应一个或多个分配给data file的操作系统块。 table创建时,默认创建了一个data segment,每个data segment含有min extents指定的extents数,每个extent据据表空间的存储参数分配一定数量的blocks
  
  
    3 描述tablespace和datafile之间的关系
  
  
    一个表空间可包含一个或多个数据文件。表空间利用增加或扩展数据文件扩大表空间，表空间的大小为组成该表空间的数据文件大小的和。一个datafile只能属于一个表空间; 一个tablespace可以有一个或多个datafile,每个datafile只能在一个tablespace内, table中的数据,通过hash算法分布在tablespace中的各个datafile中,tablespace是逻辑上的概念,datafile则在物理上储存了数据库的种种对象。
  
  
    4 本地管理表空间和字典管理表空间的特点，ASSM有什么特点
  
  
    本地管理表空间:  (9i默认) 空闲块列表存储在表空间的数据文件头。 特点: 减少数据字典表的竞争，当分配和收缩空间时会产生回滚，不需要合并。 字典管理表空间:  (8i默认) 空闲块列表存储在数据库中的字典表里. 特点: 片由数据字典管理，可能造成字典表的争用。存储在表空间的每一个段都会有不同的存储字句，需要合并相邻的块;   本地管理表空间 (Locally Managed Tablespace简称LMT)  8i以后出现的一种新的表空间的管理模式，通过位图来管理表空间的空间使用。字典管理表空间 (Dictionary-Managed Tablespace简称DMT)  8i以前包括以后都还可以使用的一种表空间管理模式，通过数据字典管理表空间的空间使用。动段空间管理 (ASSM) ，它首次出现在Oracle920里有了ASSM，链接列表freelist被位图所取代，它是一个二进制的数组， 能够迅速有效地管理存储扩展和剩余区块 (free block) ，因此能够改善分段存储本质，ASSM表空间上创建的段还有另外一个称呼叫Bitmap Managed Segments (BMB 段) 。
  
  
    5 回滚段的作用是什么
  
  
    回滚段用于保存数据修改前的映象，这些信息用于生成读一致性数据库信息、在数据库恢复和Rollback时使用。一个事务只能使用一个回滚段。   事务回滚: 当事务修改表中数据的时候，该数据修改前的值 (即前影像) 会存放在回滚段中，当用户回滚事务 (ROLLBACK) 时，ORACLE将会利用回滚段中的数据前影像来将修改的数据恢复到原来的值。 事务恢复: 当事务正在处理的时候，例程失败，回滚段的信息保存在undo表空间中，ORACLE将在下次打开数据库时利用回滚来恢复未提交的数据。 读一致性: 当一个会话正在修改数据时，其他的会话将看不到该会话未提交的修改。 当一个语句正在执行时，该语句将看不到从该语句开始执行后的未提交的修改 (语句级读一致性)  当ORACLE执行SELECT语句时，ORACLE依照当前的系统改变号 (SYSTEM CHANGE NUMBER-SCN)  来保证任何前于当前SCN的未提交的改变不被该语句处理。可以想象: 当一个长时间的查询正在执行时， 若其他会话改变了该查询要查询的某个数据块，ORACLE将利用回滚段的数据前影像来构造一个读一致性视图
  
  
    6 日志的作用是什么
  
  
    日志文件 (Log File) 记录所有对数据库数据的修改，主要是保护数据库以防止故障,以及恢复数据时使用。其特点如下:  a)每一个数据库至少包含两个日志文件组。每个日志文件组至少包含两个日志文件成员。 b)日志文件组以循环方式进行写操作。 c)每一个日志文件成员对应一个物理文件。   记录数据库事务,最大限度地保证数据的一致性与安全性 重做日志文件: 含对数据库所做的更改记录，这样万一出现故障可以启用数据恢复,一个数据库至少需要两个重做日志文件 归档日志文件: 是重做日志文件的脱机副本，这些副本可能对于从介质失败中进行恢复很必要。
  
  
### SGA主要有那些部分，主要作用是什么
  
系统全局区 (SGA) :是ORACLE为实例分配的一组共享缓冲存储区，用于存放数据库数据和控制信息，以实现对数据库数据的管理和操作。 SGA主要包括: a)共享池(shared pool) : 用来存储最近执行的SQL语句和最近使用的数据字典的数据。 b)数据缓冲区 (database buffer cache): 用来存储最近从数据文件中读写过的数据。 c)重作日志缓冲区 (redo log buffer) : 用来记录服务或后台进程对数据库的操作。 另外在SGA中还有两个可选的内存结构:  d)Java pool:  用来存储Java代码。 e)Large pool: 用来存储不与SQL直接相关的大型内存结构。备份、恢复使用。   GA: db_cache/shared_pool/large_pool/java_pool db_cache: 数据库缓存 (Block Buffer) 对于Oracle数据库的运转和性能起着非常关键的作用，它占据Oracle数据库SGA (系统共享内存区) 的主要部分。Oracle数据库通过使用LRU算法，将最近访问的数据块存放到缓存中，从而优化对磁盘数据的访问. shared_pool: 共享池的大小对于Oracle 性能来说都是很重要的。共享池中保存数据字典高速缓冲和完全解析或编译的的PL/SQL 块和SQL 语句及控制结构 large_pool: 使用MTS配置时，因为要在SGA中分配UGA来保持用户的会话，就是用Large_pool来保持这个会话内存使用RMAN做备份的时候，要使用Large_pool这个内存结构来做磁盘I/O缓存器 java_pool: 为java procedure预备的内存区域,如果没有使用java proc,java_pool不是必须的

### 备份恢复类

#### 逻辑备份: exp/imp
  
指定表的逻辑备份 物理备份:  热备份:alter tablespace begin/end backup; 冷备份:脱机备份(database shutdown) RMAN备份 full backup/incremental backup(累积/差异)   物理备份 物理备份是最主要的备份方式。用于保证数据库在最小的数据库丢失或没有数据丢失的情况下得到恢复。 冷物理 冷物理备份提供了最简单和最直接的方法保护数据库因物理损坏丢失。建议在以下几种情况中使用。 对一个已经存在大最数据量的数据库，在晚间数据库可以关闭，此时应用冷物理备份。 对需对数据库服务器进行升级， (如更换硬盘) ，此时需要备份数据库信息，并在新的硬盘中恢复这些数据信息，建议采用冷物理备份。 热物理 主要是指备份过程在数据库打开并且用户可以使用的情况下进行。需要执行热物理备份的情况有:  由于数据库性质要求不间断工作，因而此时只能采用热物理备份。 由于备份的要求的时间过长，而数据库只能短时间关闭时。 逻辑备份 (EXP/IMP) 逻辑备份用于实现数据库对象的恢复。但不是基于时间点可完全恢复的备份策略。只能作为联机备份和脱机备份的一种补充。 完全逻辑备份 完全逻辑备份是将整个数据库导出到一个数据库的格式文件中，该文件可以在不同的数据库版本、操作系统和硬件平台之间进行移植。 指定表的逻辑备份 通过备份工具，可以将指定的数据库表备份出来，这可以避免完全逻辑备份所带来的时间和财力上的浪费。
  
#### 归档是什么含义
  
关于归档日志: Oracle要将填满的在线日志文件组归档时,则要建立归档日志 (archived redo log) 。其对数据库备份和恢复有下列用处:  数据库后备以及在线和归档日志文件，在操作系统和磁盘故障中可保证全部提交的事物可被恢复。 在数据库打开和正常系统使用下，如果归档日志是永久保存，在线后备可以进行和使用。 数据库可运行在两种不同方式下: NOARCHIVELOG方式或ARCHIVELOG 方式 数据库在NOARCHIVELOG方式下使用时，不能进行在线日志的归档, 数据库在ARCHIVELOG方式下运行，可实施在线日志的归档   归档是归档当前的联机redo日志文件。 SVRMGR> alter system archive log current; 数据库只有运行在ARCHIVELOG模式下，并且能够进行自动归档，才可以进行联机备份。有了联机备份才有可能进行完全恢复。
  
  
    3 如果一个表在2004-08-04 10:30:00 被drop，在有完善的归档和备份的情况下，如何恢复
  
  
    9i 新增的FLASH BACK 应该可以; Logminer应该可以找出DML。 有完善的归档和备份，先归档当前数据，然后可以先恢复到删除的时间点之前，把DROP 的表导出来，然后再恢复到最后归档时间； 手工拷贝回所有备份的数据文件 Sql〉startup mount; sql〉alter database recover automatic until time '2004-08-04:10:30:00'; sql〉alter database open resetlogs;
  
  
    4 rman是什么，有何特点
  
  
    RMAN(Recovery Manager)是DBA的一个重要工具，用于备份、还原和恢复oracle数据库, RMAN 可以用来备份和恢复数据库文件、归档日志、控制文件、系统参数文件,也可以用来执行完全或不完全的数据库恢复。 RMAN有三种不同的用户接口: COMMAND LINE方式、GUI 方式 (集成在OEM 中的备份管理器) 、API 方式 (用于集成到第三方的备份软件中) 。 具有如下特点:  1) 功能类似物理备份，但比物理备份强大N倍； 2) 可以压缩空块； 3) 可以在块水平上实现增量； 4) 可以把备份的输出打包成备份集，也可以按固定大小分割备份集； 5) 备份与恢复的过程可以自动管理； 6) 可以使用脚本 (存在Recovery catalog 中)  7) 可以做坏块监测
  
  
    5 standby的特点
  
  
    备用数据库 (standby database) : ORACLE推出的一种高可用性(HIGH AVAILABLE)数据库方案，在主节点与备用节点间通过日志同步来保证数据的同步，备用节点作为主节点的备份，可以实现快速切换与灾难性恢复,从920开始，还开始支持物理与逻辑备用服务器。 9i中的三种数据保护模式分别是:  1)、MAXIMIZE PROTECTION : 最大数据保护与无数据分歧，LGWR将同时传送到备用节点，在主节点事务确认之前，备用节点也必须完全收到日志数据。如果网络不好，引起LGWR不能传送数据，将引起严重的性能问题，导致主节点DOWN机。 2)、MAXIMIZE AVAILABILITY : 无数据丢失模式，允许数据分歧，允许异步传送。 正常情况下运行在最大保护模式，在主节点与备用节点的网络断开或连接不正常时，自动切换到最大性能模式，主节点的操作还是可以继续的。在网络不好的情况下有较大的性能影响。 3)、MAXIMIZE PERFORMANCE: 这种模式应当可以说是从8i继承过来的备用服务器模式，异步传送，无数据同步检查，可能丢失数据，但是能获得主节点的最大性能。9i在配置DATA GUARD的时候默认就是MAXIMIZE PERFORMANCE
  
  
    6 对于一个要求恢复时间比较短的系统(数据库50G,每天归档5G)，你如何设计备份策略
  
  
    数据库比较大逻辑备份没什么必要，每天归档5G，每周三/周六自动归档10G，每月RMAN归档全库。应该有standby。 rman/每月一号 level 0 每周末/周三 level 1 其它每天level 2
  
  
    四: 系统管理类
  
  
  
    1.      对于一个存在系统性能的系统，说出你的诊断处理思路
  
  
    ü         做statspack收集系统相关信息  了解系统大致情况/确定是否存在参数设置不合适的地方/查看top 5 event/查看top sql等 ü         查v$system_event/v$session_event/v$session_wait 从v$system_event开始,确定需要什么资源(db file sequential read)等，深入研究v$session_event,确定等待事件涉及的会话，从v$session_wait确定详细的资源争用情况(p1-p3的值:file_id/block_id/blocks等) ü         通过v$sql/v$sqltext/v$sqlarea表确定disk_reads、(buffer_gets/executions)值较大的SQL
  

    1.      列举几种诊断IO、CPU、性能状况的方法

  
top  uptime  vmstat  iostat  statspack  sql_trace/tkprof 查 v$system_event/v$session_event/v$session_wait 查v$sqlarea(disk_reads或buffer_gets/executions较大的SQL) 或者第三方的监视工具，TOAD就不错。
  
  
    1.      对statspack有何认识
  
  
    认识不深。仅限了解。StapSpack是Oracle公司提供的一个收集数据库运行性能指标的软件包。可以做数据库健康检查报告。 StapSpack是Oracle公司提供的一个收集数据库运行性能指标的软件包，该软件包从8i起，在9i、10g都有显著的增强 该软件包的辅助表 (存储相关参数与收集的性能指标的表) 由最初的25个增长到43个 收集级别参数由原来的3个 (0、5、10) 增加到5个 (0、5、6、7、10)  通过分析收集的性能指标，数据库管理员可以详细地了解数据库目前的运行情况，对数据库实例、等待事件、SQL等进行优化调整 利用statspack收集的snapshot,可以统计制作数据库的各种性能指标的统计趋势图表。
  
  
    1.      如果系统现在需要在一个很大的表上创建一个索引，你会考虑那些因素，如何做以尽量减小对应用的影响
  
  
    可以先表分析一下，然后测试创建索引前后对应用的性能影响； 需要考虑的是该索引列不经常更新，不是有很多重复值的情况时, 在大表中使用索引特别有效. 创建的索引可以跟数据表分不同表空间存储。   在系统比较空闲时nologging选项 (如果有dataguard则不可以使用nologging)  大的sort_ared_size或pga_aggregate_target较大
  
### 对raid10 和raid5有何认识
  
    RAID 10(或称RAID 1+0)与RAID 0+1不同，它是用硬盘驱动器先组成RAID 1阵列，然后在RAID 1阵列之间再组成RAID 0阵列。 RAID 10模式同RAID 0+1模式一样具有良好的数据传输性能，但却比RAID 0+1具有更高的可靠性。RAID 10阵列的实际容量为M×n/2，磁盘利用率为50％。RAID 10也需要至少4个硬盘驱动器构成，因而价格昂贵。 RAID 10的可靠性同RAID 1一样，但由于RAID 10硬盘驱动器之间有数据分割，因而数据传输性能优良。 RAID 5与RAID 3很相似，不同之处在于RAID 5的奇偶校验信息也同数据一样被分割保存到所有的硬盘驱动器，而不是写入一个指定的硬盘驱动器，从而消除了单个奇偶校验硬盘驱动器的瓶颈问题。RAID 5磁盘阵列的性能比RAID 3有所提高，但仍然需要至少3块硬盘驱动器。其实际容量为M×(n-1)，磁盘利用率为(n-1)/n 。
  
  
    五: 综合随意类
  
  
  
    1.      你最擅长的是oracle哪部分?
  
  
    pl/sql及sql优化
  
  
    1.      喜欢oracle吗？喜欢上论坛吗？或者偏好oracle的哪一部分？
  
  
    喜欢。PL/SQL比较得心应手。
  
  
    1.      随意说说你觉得oracle最有意思的部分或者最困难的部分
  
  
    我对数据库的备份/恢复和性能调优经验明显不足，自然觉得有些困难。 基于ORACLE的研究应该是个宽广的领域，所以我觉得还是有意思的。
  
  
    1.      为何要选择做DBA呢?
  
  
    我对数据库的备份/恢复和性能调优经验明显不足，主要是缺乏环境和交流。 因此，算不上什么DBA。不过因此我更需要这样的机会。 不过就整个ORACLE 来说，一直从事与它相关的工作，感情还是颇深的。放弃可惜。而且就技术本身而言我觉得自己还是有学习和创新的能力，它的诸如数据仓库，数据挖掘之类的领域也很广。
  
  
    六: Databases Questions & Answers
  
  
  
    1.      What are two methods of retrieving SQL?
  
  
  
    2.      What cursor type do you use to retrieve multiple recordsets?
  
  
  
    3.      What action do you have to perform before retrieving data from the next result set of a stored procedure?
  
  
  
    Move the cursor down one row from its current position. A ResultSet cursor is initially positioned before the first row. Before you can get to the first row, you would need to Move the cursor down by one row ( For ex: in java the first call to next makes the first row the current row; the second call makes the second row the current row, and so on).
  
  
    1.      What is the basic form of a SQL statement to read data out of a table?
  
  
  
    SELECT * FROM table_name;
  
  
    1.      What structure can you have the database make to speed up table reads?
  
  
    The question is not correct. "What structure can you have the database make to speed up table reads?" It is not clear what exactly the term "structure" means in this case. Follow the rules of DB tuning we have to: 1) properly use indexes ( different types of indexes) 2) properly locate different DB objects across different tablespaces, files and so on. 3) Create a special space (tablespace) to locate some of the data with special datatypes( for example CLOB, LOB and ...)
  
  
    1.      What is a "join"?
  
  
    Joins merge the data of two related tables into a single result set, presenting a denormalized view of the data.
  
  
    1.      What is a "constraint"?
  
  
    A constraint allows you to apply simple referential integrity checks to a table. There are 5 primary types of constraints that are currently supported by SQL Server: PRIMARY/UNIQUE - enforces uniqueness of a particular table column. DEFAULT - specifies a default value for a column in case an insert operation does not provide one. FOREIGN KEY - validates that every value in a column exists in a column of another table. CHECK - checks that every value stored in a column is in some specified list NOT NULL - is a constraint which does not allow values in the specific column to be null. And also it is the only constraint which is not a table level constraint.
  
  
    1.      What is a "primary key"?
  
  
    Primary Key is a type of a constraint enforcing uniqueness and data integrity for each row of a table. All columns participating in a primary key constraint must possess the NOT NULL property.
  
  
    1.      What is a "functional dependency"? How does it relate to database table design?
  
  
    What functional dependence in the context of a database means is that: Assume that a table exists in the database called TABLE with a composite primary key (A, B) and other non-key attributes (C, D, E). Functional dependency in general, would mean that any non-key attribute - C D or E being dependent on the primary key (A and B) in our table here. Partial functional dependency, on the other hand, is another corollary of the above, which states that all non-key attributes - C D or E - if dependent on the subset of the primary key (A and B) and not on it as a whole. Example : ---- Fully Functional Dependent : C D E -> A B Partial Functional dependency : C -> A, D E -> B Hope that helps!
  
  
    1.   What is a "trigger"?
  
  
    A trigger is a database object directly associated with a particular table. It fires whenever a specific statement/type of statement is issued against that table. The types of statements are insert, update, delete and query statements. Basically, trigger is a set of SQL statements that execute in response to a data modification/retrieval event on a table. Other than table triggers there are also schema and database triggers. These can be made to fire when new objects are created, when a user logs in, when the database shutdown etc. Table level triggers can be classified into row and statement level triggers and those can be further broken down into before and after triggers. Before triggers can modify data.
  
  
    1.   What is "index covering" of a query?
  
  
    A nonclustered index that includes (or covers) all columns used in a query is called a covering index. When SQL server can use a nonclustered index to resolve the query, it will prefer to scan the index rather than the table, which typically takes fewer data pages. If your query uses only columns included in the index, then SQL server may scan this index to produce the desired output.
  
  
    1.   What is a SQL view?
  
  
    View is a precomplied SQL query which is used to select data from one or more tables. A view is like a table but it doesn't physically take any space. View is a good way to present data in a particular format if you use that query quite often. View can also be used to restrict users from accessing the tables directly. A view otherwise known as a virtual table is a mere window over the base tables in the database. This helps us gain a couple of advantages: 1) Inherent security exposing only the data that is needed to be shown to the end user 2) Views are updateable based on certain conditions. For example, updates can only be directed to one underlying table of the view. After modification if the rows or columns don't comply with the conditions that the view was created with, those rows disappear from the view. You could use the CHECK OPTION with the view definition, to make sure that any updates to make the rows invalid will not be permitted to run. 3) Views are not materialized (given a physical structure) in a database. Each time a view is queried the definition stored in the database is run against the base tables to retrieve the data. One exception to this is to create a clustered index on the view to make it persistent in the database. Once you create a clustered index on the view, you can create any number of non-clustered indexes on the view.
  
  
    1.   存储过程和函数的区别
  
  
    存储过程是用户定义的一系列sql语句的集合，涉及特定表或其它对象的任务，用户可以调用存储过程，而函数通常是数据库已定义的方法，它接收参数并返回某种类型的值并且不涉及特定用户表。
  
  
    1.   事务是什么?
  
  
    事务是作为一个逻辑单元执行的一系列操作，一个逻辑工作单元必须有四个属性，称为 ACID(原子性、一致性、隔离性和持久性)属性，只有这样才能成为一个事务: 原子性: 事务必须是原子工作单元;对于其数据修改，要么全都执行，要么全都不执行。 一致性: 事务在完成时，必须使所有的数据都保持一致状态。在相关数据库中，所有规则都必须应用于事务的修改，以保持所有数据的完整性。事务结束时，所有的内部数据结构(如 B 树索引或双向链表)都必须是正确的。 隔离性: 由并发事务所作的修改必须与任何其它并发事务所作的修改隔离。事务查看数据时数据所处的状态，要么是另一并发事务修改它之前的状态，要么是另一事务修改它之后的状态，事务不会查看中间状态的数据。这称为可串行性，因为它能够重新装载起始数据，并且重播一系列事务，以使数据结束时的状态与原始事务执行的状态相同。 持久性: 事务完成之后，它对于系统的影响是永久性的。该修改即使出现系统故障也将一直保持。
  
  
    1.   游标的作用?如何知道游标已经到了最后?
  
  
    游标用于定位结果集的行，通过判断全局变量@@FETCH_STATUS可以判断是否到了最后，通常此变量不等于0表示出错或到了最后。
  
  
    1.   触发器分为事前触发和事后触发，这两种触发有和区别。语句级触发和行级触发有何区别。
  
  
    事前触发器运行于触发事件发生之前，而事后触发器运行于触发事件发生之后。通常事前触发器可以获取事件之前和新的字段值。 语句级触发器可以在语句执行前或后执行，而行级触发在触发器所影响的每一行触发一次。
  
  
    1.   SQL Server常用测试题(1)
  
  
    问题描述: 为管理岗位业务培训信息，建立3个表: S (S#,SN,SD,SA) S#,SN,SD,SA 分别代表学号、学员姓名、所属单位、学员年龄 C (C#,CN ) C#,CN 分别代表课程编号、课程名称 SC ( S#,C#,G ) S#,C#,G 分别代表学号、所选修的课程编号、学习成绩   1. 使用标准SQL嵌套语句查询选修课程名称为'税收基础'的学员学号和姓名 -实现代码: SELECT SN,SD FROM S WHERE [S#] IN(SELECT [S#] FROM C,SC WHERE C.[C#]=SC.[C#] AND CN=N'税收基础')   2. 使用标准SQL嵌套语句查询选修课程编号为'C2'的学员姓名和所属单位 -实现代码: SELECT S.SN,S.SD FROM S,SC WHERE S.[S#]=SC.[S#] AND SC.[C#]='C2'   3. 使用标准SQL嵌套语句查询不选修课程编号为'C5'的学员姓名和所属单位 -实现代码: SELECT SN,SD FROM S WHERE [S#] NOT IN(SELECT [S#] FROM SC WHERE [C#]='C5')   4. 使用标准SQL嵌套语句查询选修全部课程的学员姓名和所属单位 -实现代码: SELECT SN,SD FROM S WHERE [S#] IN( SELECT [S#] FROM SC RIGHT JOIN C ON SC.[C#]=C.[C#] GROUP BY [S#] HAVING COUNT(*)=COUNT([S#])) 5. 查询选修了课程的学员人数 -实现代码: SELECT 学员人数=COUNT(DISTINCT [S#]) FROM SC 6. 查询选修课程超过5门的学员学号和所属单位 -实现代码: SELECT SN,SD FROM S WHERE [S#] IN( SELECT [S#] FROM SC GROUP BY [S#] HAVING COUNT(DISTINCT [C#])>5)
  
  
    1.   Question 1: Can you use a batch SQL or store procedure to calculating the Number of Days in a Month
  
  
    找出当月的天数 select datepart(dd,dateadd(dd,-1,dateadd(mm,1,cast(cast(year(getdate()) as varchar)+'-'+cast(month(getdate()) as varchar)+'-01' as datetime))))
  
  
    1.   Question2: Can you use a SQL statement to calculating it! How can I print "10 to 20" for books that sell for between $10 and $20，"unknown" for books whose price is null, and "other" for all other prices?
  
  
    select bookid,bookname,price=case when price is null then 'unknown' when  price between 10 and 20 then '10 to 20' else price end from books
  
  
    1.     Question3: Can you use a SQL statement to finding duplicate values! How can I find authors with the same last name? You can use the table authors in datatabase pubs. I want to get the result as below: Output: au_lname                                 number_dups -------------- ---- Ringer                                   2 (1 row(s) affected) Answer 3 select au_lname,number_dups=count(1) from authors group by au_lname
  
  
  
    2.   Question4: Can you create a cross-tab report in my SQL Server! How can I get the report about sale quality for each store and each quarter and the total sale quality for each quarter at year 1993? You can use the table sales and stores in datatabase pubs. Table Sales record all sale detail item for each store. Column store_id is the id of each store, ord_date is the order date of each sale item, and column qty is the sale qulity. Table stores record all store information. I want to get the result look like as below: Output:
  
  
  
    
      
        
          
            stor_name                                Total       Qtr1        Qtr2        Qtr3        Qtr4 -------------- ---- ---- ---- ---- ---- Barnum's                                 50          0           50          0           0 Bookbeat                                 55          25          30          0           0 Doc-U-Mat: Quality Laundry and Books     85          0           85          0           0 Fricative Bookshop                       60          35          0           0           25 Total                                    250         60          165         0           25
          
        
      
    
  
  
    Answer 4: 用动态SQL实现
  
  
    1.   Question5: The Fastest Way to Recompile All Stored Procedures I have a problem with a database running in SQL Server 6.5 (Service Pack 4). We moved the database (object transfer) from one machine to another last night, and an error (specific to a stored procedure) is cropping up. However, I can't tell which procedure is causing it. Permissions are granted in all of our stored procedures; is there a way from the isql utility to force all stored procedures to recompile?
  
  
  
    Tips: sp_recompile can recomplie a store procedure each time Answer 5: 在执行存储过程时,使用 with recompile 选项强制编译新的计划；使用sp_recompile系统存储过程强制在下次运行时进行重新编译
  

    1.   Question6: How can I add row numbers to my result set? In database pubs, have a table titles , now I want the result shown as below,each row have a row number, how can you do that? Result:

line-no     title_id ---- --- 1           BU1032 2           BU1111 3           BU2075 4           BU7832 5           MC2222 6           MC3021 7           MC3026 8           PC1035 9           PC8888 10          PC9999 11          PS1372 12          PS2091 13          PS2106 14          PS3333 15          PS7777 16          TC3218 17          TC4203 18          TC7777
          
Answer 6:  -SQL 2005的写法 select row_number() as line_no ,title_id from titles -SQL 2000的写法 select line_no identity(int,1,1),title_id into #t from titles select * from #t drop table #t

1.  Question 7: Can you tell me what the difference of two SQL statements at performance of execution?
Statement 1: if NOT EXISTS ( select * from publishers where state = 'NY') begin SELECT 'Sales force needs to penetrate New York market' end else begin SELECT 'We have publishers in New York' end Statement 2: if EXISTS ( select * from publishers where state = 'NY') begin SELECT 'We have publishers in New York' end else begin SELECT 'Sales force needs to penetrate New York market' end Answer 7: 不同点:执行时的事务数,处理时间,从客户端到服务器端传送的数据量大小
  
1.  Question8: How can I list all California authors regardless of whether they have written a book? In database pubs, have a table authors and titleauthor , table authors has a column state, and titleauhtor have books each author written. CA behalf of california in table authors. Answer 8:  select * from  authors where state='CA'


27. Question9: How can I get a list of the stores that have bought both 'bussiness' and 'mod_cook' type books? In database pubs, use three table stores,sales and titles to implement this requestment. Now I want to get the result as below:

stor_id stor_name --- -------------- ... 7896    Fricative Bookshop ... ... ... Answer 9:  select distinct a.stor_id, a.stor_name from stores a,sales b,titles c where a.stor_id=b.stor_id and b.title_id=c.title_id and c.type='business' and exists(select 1 from sales k,titles g where stor_id=b.stor_id and k.title_id=g.title_id and g.type='mod_cook')
          
28. Question10: How can I list non-contignous data? In database pubs, I create a table test using statement as below, and I insert several row as below
create table test ( id int primary key ) go
          
insert into test values (1 ) insert into test values (2 ) insert into test values (3 ) insert into test values (4 ) insert into test values (5 ) insert into test values (6 ) insert into test values (8 ) insert into test values (9 ) insert into test values (11) insert into test values (12) insert into test values (13) insert into test values (14) insert into test values (18) insert into test values (19) go

Now I want to list the result of the non-contignous row as below,how can I do it? Missing after Missing before ----- ----- 6             8 9             11 ...
          
Answer 10:  select id from test t where not exists(select 1 from test where id=t.id+1) or not exists(select 1 from test where id=t.id-1)
  
29. Question11: How can I list all book with prices greather than the average price of books of the same type? In database pubs, have a table named titles , its column named price mean the price of the book, and another named type mean the type of books. Now I want to get the result as below:


type         title                                                                            price ---- --------------------------- ------- business     The Busy Executive's Database Guide                                              19.9900 ... ... ... ...
          
Answer 11:  select a.type,a.title,a.price from titles a, (select type,price=avg(price) from titles group by type)b where a.type=b.type and a.price>b.price
  
试题点评: 通览整个试题，我们不难发现，这份试题是针对SQL Server数据库人员的。而从难度分析上来看，这份试题也属于同类试题中比较难的了。之所以说它难，首先是限定时间的全英文试题；其次，尽管这份试题主要是考核开发能力，但却涉及到了算法的选择和性能的调优；最后，这份试题还夹进了SQL Server数据库的升级问题。因此，综上所述，我们估计这是一家从事程序外包工作的外企招聘后台开发或与后台开发相关的SQL Server高级程序员的试题。
  
