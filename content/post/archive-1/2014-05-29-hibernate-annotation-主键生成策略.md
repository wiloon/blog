---
title: hibernate annotation 主键生成策略
author: "-"
date: 2014-05-29T06:24:31+00:00
url: /?p=6690
categories:
  - Uncategorized
tags:
  - JPA

---
## hibernate annotation 主键生成策略
hibernate annotation 之 主键生成策略
  
Posted on 2012-10-12 20:10 fancydeepin 阅读(2993) 评论(1) 编辑 收藏 所属分类: Hibernate Annotation

Hibernate 默认总共支持 13 种生成策略 :
  
1. increment 2. identity 3. sequence
  
4. hilo 5. seqhilo 6. uuid
  
7. uuid.hex 8. guid 9. native
  
10. assigned 11. select 12. foreign 13. sequence-identity


下面介绍几个较为常用的策略 :
  
① identity [ 自然递增 ]

支持 DB2,MySQL,SQL Server,Sybase 和HypersonicSQL 数据库, 用于为 long 或 short 或 int 类型生成唯一标识。它依赖于底层不同的数据库,
  
与 Hibernate 和 程序员无关。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "identity")

@GeneratedValue(generator = "idGenerator")


② sequence [ 序列 ]

支持 Oracle,DB2,PostgreSql,SAPDb 等数据库,用于为 long 或 short 或 int 类型生成唯一标识。它需要底层数据库的支持,
  
并由数据库来维护这个 sequence 序列。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "sequence",

parameters = {@Parameter(name = "sequence",value="seq_name")})

@GeneratedValue(generator = "idGenerator")

注意 : 该策略要求设定序列名,否则 hibernate 将无法找到,这将引致抛出异常 :

org.hibernate.exception.SQLGrammarException: could not get next sequence value


③ native

需底层数据库的支持,对于 MySQL,SQL Server 采用 identity 的生成策略,对于 Oracle,则采用 sequence 策略。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "native")

@GeneratedValue(generator = "idGenerator")


④ increment [ 自然递增 ]

与 identity 策略不同的是,该策略不依赖于底层数据库,而依赖于 hibernate 本身,用于为 long 或 short 或 int 类型生成唯一标识。
  
主键计数器是由 hibernate 的一个实例来维护,每次自增量为 1,但在集群下不能使用该策略,
  
否则将引起主键冲突的情况,该策略适用于所有关系型数据库使用。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "increment")

@GeneratedValue(generator = "idGenerator")


⑤ uuid [ 32位16进制数的字符串 ]

采用128位UUID算法生成主键,能够保证网络环境下的主键唯一性,也就能够保证在不同数据库及不同服务器下主键的唯一性。
  
uuid 最终被编码成一个32位16进制数的字符串,
  
占用的存储空间较大。用于为 String 类型生成唯一标识,适用于所有关系型数据库。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "uuid")

@GeneratedValue(generator = "idGenerator")


⑤ assigned [ 手工分配主键ID值 ]

该策略要求程序员必须自己维护和管理主键,当有数据需要存储时,程序员必须自己为该数据分配指定一个主键ID值,
  
如果该数据没有被分配主键ID值或分配的值存在重复,则该数据都将无法被持久化且会引起异常的抛出。

注解示例 :

@Id

@GenericGenerator(name = "idGenerator", strategy = "assigned")

@GeneratedValue(generator = "idGenerator")

[ 随笔均原创,转载请注明出处: http://www.blogjava.net/fancydeepin ]