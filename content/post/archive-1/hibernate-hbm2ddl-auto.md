---
title: hibernate.hbm2ddl.auto
author: "-"
date: 2015-05-21T01:58:01+00:00
url: /?p=7696
categories:
  - Uncategorized

---
## hibernate.hbm2ddl.auto
hibernate.cfg.xml 中hibernate.hbm2ddl.auto配置节点如下: 
  
<properties>
  
<property name="hibernate.show_sql" value="true" />
  
<property name="hibernate.hbm2ddl.auto" value="create" />
  
</properties>

Hibernate Reference Documentation 3.3.1解释如下: 
  
Automatically validate or export schema DDL to the database when the SessionFactory is created.
  
With create-drop, the database schema will be dropped when the SessionFactory is closed explicitly.
  
eg. validate | update | create | create-drop
  
其实这个hibernate.hbm2ddl.auto参数的作用主要用于: 自动创建|更新|验证数据库表结构。如果不是此方面的需求建议set value="none"。
  
create: 
  
每次加载hibernate时都会删除上一次的生成的表,然后根据你的model类再重新来生成新表,哪怕两次没有任何改变也要这样执行,这就是导致数据库表数据丢失的一个重要原因。
  
create-drop : 
  
每次加载hibernate时根据model类生成表,但是sessionFactory一关闭,表就自动删除。
  
update: 
  
最常用的属性,第一次加载hibernate时根据model类会自动建立起表的结构（前提是先建立好数据库) ,以后加载hibernate时根据 model类自动更新表结构,即使表结构改变了但表中的行仍然存在不会删除以前的行。要注意的是当部署到服务器后,表结构是不会被马上建立起来的,是要等 应用第一次运行起来后才会。
  
validate : 
  
每次加载hibernate时,验证创建数据库表结构,只会和数据库中的表进行比较,不会创建新表,但是会插入新值。

再说点"废话": 
  
当我们把hibernate.hbm2ddl.auto=create时hibernate先用hbm2ddl来生成数据库schema。
  
当我们把hibernate.cfg.xml文件中hbm2ddl属性注释掉,这样我们就取消了在启动时用hbm2ddl来生成数据库schema。通常 只有在不断重复进行单元测试的时候才需要打开它,但再次运行hbm2ddl会把你保存的一切都删除掉（drop) -- create配置的含义是: "在创建SessionFactory的时候,从scema中drop掉所以的表,再重新创建它们"。
  
注意,很多Hibernate新手在这一步会失败,我们不时看到关于Table not found错误信息的提问。但是,只要你根据上面描述的步骤来执行,就不会有这个问题,因为hbm2ddl会在第一次运行的时候创建数据库schema, 后续的应用程序重启后还能继续使用这个schema。假若你修改了映射,或者修改了数据库schema,你必须把hbm2ddl重新打开一次。

\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***\*****

这两天在整理Spring + JPA（Hibernate实现) ,从网上copy了一段Hibernate连接参数的配置。

<properties>
  
<property name="hibernate.show_sql" value="true" />
  
<property name="hibernate.hbm2ddl.auto" value="create" />
  
</properties>
  
结果在测试时,老是发现数据库表数据丢失。这个参数以前没怎么用,查了一圈其它的东西,最后才定位到这个上面。赶紧查了一下Hibernate的参数配置,解释如下: 

hibernate.hbm2ddl.auto Automatically validate or export schema DDL to the database when the SessionFactory is created. With create-drop, the database schema will be dropped when the SessionFactory is closed explicitly. eg. validate | update | create | create-drop

其实这个参数的作用主要用于: 自动创建|更新|验证数据库表结构。如果不是此方面的需求建议set value="none".

其它几个参数的意思,我解释一下: 

validate               加载hibernate时,验证创建数据库表结构
  
create                  每次加载hibernate,重新创建数据库表结构,这就是导致数据库表数据丢失的原因。
  
create-drop        加载hibernate时创建,退出是删除表结构
  
update                 加载hibernate自动更新数据库结构

以上4个属性对同一配置文件下所用有的映射表都起作用


总结: 

1.请慎重使用此参数,没必要就不要随便用。

2.如果发现数据库表丢失,请检查hibernate.hbm2ddl.auto的配置


本文来自CSDN博客,转载请标明出处: http://blog.csdn.net/lgq_0714/archive/2009/11/16/4814693.aspx