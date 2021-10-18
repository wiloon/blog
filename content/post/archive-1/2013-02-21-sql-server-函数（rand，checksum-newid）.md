---
title: SQL Server 函数（RAND，CHECKSUM, NEWID) 
author: "-"
type: post
date: 2013-02-21T03:35:36+00:00
url: /?p=5216
categories:
  - DataBase
tags:
  - SQLServer

---
# SQL Server 函数（RAND，CHECKSUM, NEWID)
<http://www.cnblogs.com/chenxizhang/archive/2009/06/26/1511898.html>

    这一篇我们来捋捋在T-SQL中可能会用到的几个特殊的函数
  
  
    1. 随机数: RAND
  
  
    返回从 0 到 1 之间的随机 float 值。
  
  语法: RAND ( [ <i>seed </i>] )
  
  <dl>
    <dt>
      <i>seed</i>
    </dt>
    
    <dd>
      提供种子值的整数表达式（tinyint、smallint 或 int) 。如果未指定 <i>seed</i>，则 Microsoft SQL Server 数据库引擎 随机分配种子值。对于指定的种子值，返回的结果始终相同。
    </dd>
  </dl>
  
    随机数是我们经常会用到的，几乎所有的语言都支持产生随机数。而且函数都差不多。例如在VBA和VB中也是用RAND，在C#中用RANDOM等等
  
  
    【注意】我相信很多朋友都对于彩票那些数字很感兴趣.其实说白了,那是一个随机数(如果电脑开票的话). 那么，如果我们能猜到那个seed，就能模拟出来想要的号码。这不是天方夜谭，我曾经听说台湾就曾经有人这么做过，而且每期必中。后来据说被逮起来了，说是有内幕交易，其实人家冤枉啊。早期的彩票比较粗糙，确实可能才出来的。
  
  
  
  
    2. 校验和值: CHECKSUM
  
  
    返回按照表的某一行或一组表达式计算出来的校验和值。CHECKSUM 用于生成哈希索引。
  
  语法: CHECKSUM ( * | <i>expression </i>[ ,...<i>n</i> ] )
  
    *
 指定对表的所有列进行计算。如果有任一列是非可比数据类型，则 CHECKSUM 返回错误。非可比数据类型有 text、ntext、image、XML 和 cursor，还包括以上述任一类型作为基类型的 sql_variant。
  
  
    expression
 除非可比数据类型之外的任何类型的表达式。
  
  
    返回值是int
  
  
    CHECKSUM 对其参数列表计算一个称为校验和的哈希值。此哈希值用于生成哈希索引。如果 CHECKSUM 的参数为列，并且对计算的 CHECKSUM 值生成索引，则结果是一个哈希索引。它可用于对列进行等价搜索。
  
  
    CHECKSUM 满足哈希函数的下列属性: 在使用等于 (=) 运算符比较时，如果两个列表的相应元素具有相同类型且相等，则在任何两个表达式列表上应用的 CHECKSUM 将返回同一值。对于该定义，指定类型的 Null 值被作为相等进行比较。如果表达式列表中的某个值发生更改，则列表的校验和通常也会更改。但只在极少数情况下，校验和会保持不变。因此，我们不推荐使用 CHECKSUM 来检测值是否更改，除非应用程序可以容忍偶尔丢失更改。请考虑改用 HashBytes。指定 MD5 哈希算法时，HashBytes 为两个不同输入返回相同结果的可能性比 CHECKSUM 小得多。
  
  
    表达式的顺序影响 CHECKSUM 的结果值。用于 CHECKSUM(*) 的列顺序是表或视图定义中指定的列顺序。其中包括计算列。
  
  
    【注意】这个函数我用的不多。理解不深。但对于它可以把一个文本产生一串数字感觉很有意思。
  
  
  
  
    3.全局唯一编号: NEWID
  
  
    创建 uniqueidentifier 类型的唯一值。
  
  
    语法: 
  
  NEWID ( )
  
    这个函数总是能返回一个新的GUID号码，它永远不会重复，而且毫无规律
  
  
  
  
    最后说点更实际的,这三个函数在一个场合下可以结合起来用
  
  
    SELECT TOP 10 * FROM Customers
 ORDER BY RAND()*CHECKSUM(NEWID())
  
  
  
  
    猜猜看,这个查询是什么意思 ?
  
  
  
  
  
