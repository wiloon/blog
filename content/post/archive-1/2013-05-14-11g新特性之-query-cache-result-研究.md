---
title: 11g新特性之–Query Cache Result 研究
author: wiloon
type: post
date: 2013-05-14T04:23:29+00:00
url: /?p=5466
categories:
  - DataBase

---
**<http://www.killdb.com/2011/07/31/11g%E6%96%B0%E7%89%B9%E6%80%A7%E4%B9%8B-query-cache-result-%E7%A0%94%E7%A9%B6.html>**

**本站文章除注明转载外，均为本站原创：** 转载自[love wife & love life —Roger 提供oracle技术支持服务][1]

**本文链接地址:** [11g新特性之–Query Cache Result 研究][2]

该特性是11gR1引入的，关于query result cache特性，主要有2种：

1. PL/SQL Function Result Cache –针对plsql而言
  
2. Query Result Cache –顾名思义针对重复执行的sql

我们都知道oracle通常是通过参数来进行控制某个功能的，当然这个也不例外，
  
首先我们来介绍跟该特性有关的几个参数(包括隐含参数）：

  <table>
    <tr>
      <td>
        SQL> SELECT * FROM v$version WHERE rownum <2;

BANNER
--------------------------------------------------------------------------------
Oracle DATABASE 11g Enterprise Edition Release 11.2.0.1.0 - Production

SQL> SHOW parameter RESULT

NAME                                    TYPE        VALUE
------------------------------------    ----------- ------------------------------
_client_result_cache_bypass             BOOLEAN     FALSE
_result_cache_auto_execution_threshold  INTEGER     1
_result_cache_auto_size_threshold       INTEGER     100
_result_cache_auto_time_distance        INTEGER     300
_result_cache_auto_time_threshold       INTEGER     1000
_result_cache_block_size                INTEGER     1024
_result_cache_global                    BOOLEAN     TRUE
_result_cache_timeout                   INTEGER     10
_xsolapi_sql_result_set_cache_size      INTEGER     32
client_result_cache_lag                 big INTEGER 3000
client_result_cache_size                big INTEGER 0
result_cache_max_result                 INTEGER     5
result_cache_max_size                   big INTEGER 960K
result_cache_mode                       string      MANUAL
result_cache_remote_expiration          INTEGER     0
      </td>
    </tr>
  </table>

几个重要的参数：

**result\_cache\_mode**
  
该参数是最为重要的，其属性有manual和force 两种。
  
manual是默认属性，也就是说我们要启用该特性，那么必须通过hint来实现，不然oracle的优化器
  
是无法认知的，那么是什么hint呢？ 如下：

  <table>
    <tr>
      <td>
        SQL> SELECT name,version FROM v$sql_hint
  2  WHERE name LIKE '%RESULT%';
      </td>
    </tr>
  </table>


  <table>
    <tr>
      <td>
        NAME                                     VERSION
---------------------------------------- -------------------------
RESULT_CACHE                             11.1.0.6
NO_RESULT_CACHE                          11.1.0.6
      </td>
    </tr>
  </table>

当设置为force时，oracle 优化就能自动识别了，不需要使用hint，相反，如果当设置为force时，同时
  
你又不想某个sql或应用使用该特性，那么可以使用NO\_RESUIT\_CACHE  hint来进行避规。
  
至于说，当启动该特性时，oracle是如何来实现的？这个问题需要进一步研究。
  
**result\_cache\_max_size **
  
该参数控制着使用该特性的内存大小，当该参数设置为0，那么也就意味着关闭了该特性。
  
该部分内存是从SGA中分配的，至于分配的比例关系，metalink提供了如下的数据：
  
0.25% of MEMORY_TARGET or
  
0.5% of SGA_TARGET or
  
1% of SHARED\_POOL\_SIZE
  
上面的关系应该是一目了然了，如何解释？我暂且不说，给大家留个问题。
  
**result\_cache\_max_result**
  
该参数是控制单个result所能占据query cache的大小比例，注意是一个百分比。
  
该参数默认是是5%，取值范围当然是1% ~ 100% 了。
  
**result\_cache\_remote_expiration**
  
该参数的作用是根据远程数据库对象设置缓存过期的时间，默认值为0.
  
也就是说，默认情况下，远程数据库对象不会被进行cache的。

**\_result\_cache_global**
  
顾名思义，该参数肯定是针对Rac集群而设计的，这样可以大大的降低经典的gc等待。
  
下面通过相关的实验操作来进行详细的说明:

 [1]: http://www.killdb.com/
 [2]: http://www.killdb.com/2011/07/31/11g%e6%96%b0%e7%89%b9%e6%80%a7%e4%b9%8b-query-cache-result-%e7%a0%94%e7%a9%b6.html