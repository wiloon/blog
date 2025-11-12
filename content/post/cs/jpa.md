---
title: JPA
author: "-"
date: 2014-05-22T03:12:14+00:00
url: /?p=6649
categories:
  - Inbox
tags:
  - JPA

---
## JPA

 (1) 、JPA介绍:

JPA全称为Java Persistence API ,Java持久化API是Sun公司在Java EE 5规范中提出的Java持久化接口。JPA吸取了目前Java持久化技术的优点,旨在规范、简化Java对象的持久化工作。使用JPA持久化对象,并不是依赖于某一个ORM框架。

为什么要使用JAP?
  
在说为什么要使用JPA之前,我们有必要了解为什么要使用ORM技术。

ORM 是Object-Relation-Mapping,即对象关系影射技术,是对象持久化的核心。ORM是对JDBC的封装,从而解决了JDBC的各种存在问题:

a) 繁琐的代码问题

用JDBC的API编程访问数据库,代码量较大,特别是访问字段较多的表的时候,代码显得繁琐、累赘,容易出错。例如: PreparedStatement pstmt=con.prepareStatment("insert into account value(?,?,?,?,?,?,?,?,?)");

ORM则建立了Java对象与数据库对象之间的影射关系,程序员不需要编写复杂的SQL语句,直接操作Java对象即可,从而大大降低了代码量,也使程序员更加专注于业务逻辑的实现。

b) 数据库对象连接问题

关系数据对象之间,存在各种关系,包括1对1、1对多、多对1、多对多、级联等。在数据库对象更新的时候,采用JDBC编程,必须十分小心处理这些关系,以保证维持这些关系不会出现错误,而这个过程是一个很费时费力的过程。

ORM建立Java对象与数据库对象关系影射的同时,也自动根据数据库对象之间的关系创建Java对象的关系,并且提供了维持这些关系完整、有效的机制。

c) 系统架构问题

JDBC属于数据访问层,但是使用JDBC编程时,必须知道后台是用什么数据库、有哪些表、各个表有有哪些字段、各个字段的类型是什么、表与表之间什么关系、创建了什么索引等等与后台数据库相关的详细信息。

使用ORM技术,可以将数据库层完全隐蔽,呈献给程序员的只有Java的对象,程序员只需要根据业务逻辑的需要调用Java对象的Getter和 Setter方法,即可实现对后台数据库的操作,程序员不必知道后台采用什么数据库、有哪些表、有什么字段、表与表之间有什么关系。

d) 性能问题

采用JDBC编程,在很多时候存在效率低下的问题。

pstmt =conn.prepareStatement("insert into user_info values(?,?)");
  
for (int i=0; i<1000; i++) {
  
pstmt.setInt(1,i);
  
pstmt.setString(2,"User"+i.toString());
  
pstmt.executeUpdate();
  
}

以上程序将向后台数据库发送1000次SQL语句执行请求,运行效率较低。

采用ORM技术,ORM框架将根据具体数据库操作需要,会自动延迟向后台数据库发送SQL请求,ORM也可以根据实际情况,将数据库访问操作合成,尽量减少不必要的数据库操作请求。

JPA是目前比较流行的一种ORM技术之一,所以他拥有ORM技术的各种特点,当然他还有自己的一些优势:

1 标准化
  
JPA 是 JCP 组织发布的 Java EE 标准之一,因此任何声称符合 JPA 标准的框架都遵循同样的架构,提供相同的访问 API,这保证了基于JPA开发的企业应用能够经过少量的修改就能够在不同的JPA框架下运行。
  
2 对容器级特性的支持
  
JPA 框架中支持大数据集、事务、并发等容器级事务,这使得 JPA 超越了简单持久化框架的局限,在企业应用发挥更大的作用。
  
3 简单易用,集成方便
  
JPA的主要目标之一就是提供更加简单的编程模型: 在JPA框架下创建实体和创建Java 类一样简单,没有任何的约束和限制,只需要使用 javax.persistence.Entity进行注释；JPA的框架和接口也都非常简单,没有太多特别的规则和设计模式的要求,开发者可以很容易的掌握。JPA基于非侵入式原则设计,因此可以很容易的和其它框架或者容器集成。
  
4 可媲美JDBC的查询能力
  
JPA的查询语言是面向对象而非面向数据库的,它以面向对象的自然语法构造查询语句,可以看成是Hibernate HQL的等价物。JPA定义了独特的JPQL (Java Persistence Query Language) ,JPQL是EJB QL的一种扩展,它是针对实体的一种查询语言,操作对象是实体,而不是关系数据库的表,而且能够支持批量更新和修改、JOIN、GROUP BY、HAVING 等通常只有 SQL 才能够提供的高级查询特性,甚至还能够支持子查询。
  
5 支持面向对象的高级特性
  
JPA 中能够支持面向对象的高级特性，如类之间的继承、多态和类之间的复杂关系，这样的支持能够让开发者最大限度的使用面向对象的模型设计企业应用，而不需要自行处理这些特性在关系数据库的持久化。

## JPA的merge和persist

原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。[http://pz0513.blog.51cto.com/443986/113098](http://pz0513.blog.51cto.com/443986/113098)
  
原来merge()也有persist()的作用！
  
persist会把传进去的实体放到持久化上下文中，此时如果持久化上下文中有了这个实体，就会抛出javax.persistence.EntityExistsException，没有的话事务提交的时候把那个对象加进数据库中，如果数据库中已经存在了那个对象 (那一行) ，就会抛出com.MySQL.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException；

而merge会在持久化上下文中生成传进去的实体的受管版本，如果已经有了受管版本，那也不会抛出异常，然后把那个受管的实体返回出来，事务提交的时候如果数据库中不存在那个对象 (那一行) ，就把把那个受管的加进去，存在的话就替换掉原来的数据。merge是如果持久化上下文中有了受管版本，那就更新，没有就复制一份，返回受管的。

再次总结persist (①，②-③，④-⑤) :
  
 (这里说的抛出的异常都是指对象 (或者数据库中的行) 重复的异常)
  
① 如果persist的是一个受管实体 (即已经在上下文中) ，就不会抛出异常。
  
②如果persist的是一个游离实体 (即上下文中没有它) ，而上下文中又没有它的受管版本，数据库中也没有，也不会抛出异常，而会把这个实体写进数据库中。
  
③如果persist的是一个游离实体 (即上下文中没有) ，而上下文中又没有它的受管版本，数据库却有这个实体，那么EntityManager在persist它的时候不会抛出异常，但是事务提交的时候就会抛出异常:
  
Caused by: com.MySQL.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '7' for key 1；
  
④如果persist的是一个游离实体 (即上下文中没有) ，而上下文中却有它的受管版本，数据库中又没有这个实体，那么还是不会抛出异常，而是把它的受管版本加进去 (不是那个游离的，是那个受管的！)  (即，这种情况persist和没persist是一样的！) 。
  
⑤如果persist的是一个游离实体 (即上下文中没有) ，而上下文中却有它的受管版本，数据库中也有了这个实体，那么EntityManager在persist它的时候就会抛出异常: javax.persistence.EntityExistsException
  
而merge就不会抛出什么对象重复的异常的了。。
  
本文出自 "辽源大火的奋斗历程" 博客，请务必保留此出处[http://pz0513.blog.51cto.com/443986/113098](http://pz0513.blog.51cto.com/443986/113098)
