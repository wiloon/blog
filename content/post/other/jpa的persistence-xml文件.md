---
title: JPA的persistence.xml文件
author: "-"
date: 2014-05-29T05:47:15+00:00
url: /?p=6688
categories:
  - Uncategorized
tags:
  - JPA

---
## JPA的persistence.xml文件
Posted on 2012-05-24 12:27 CN.programmer.Luxh 阅读(7217) 评论(0) 编辑 收藏
  
persistence.xml文件必须定义在classpath路径下的META-INF文件夹中。


我们看看基于Hibernate提供的一个比较完整的JPA2.0的persistence.xml文件。

persistence.xml:

复制代码
  
1 <?xml version="1.0" encoding="UTF-8"?>
  
2 <persistence version="2.0" xmlns="http://java.sun.com/xml/ns/persistence"
  
3 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
4 xsi:schemaLocation="http://java.sun.com/xml/ns/persistence
  
5 http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd">
  
7 <!-必须要有name属性，不能为空 ->
  
8 <persistence-unit name="jpaPU" transaction-type="RESOURCE_LOCAL">
  
9 <!-可选 ->
  
10 <provider>org.hibernate.ejb.HibernatePersistence</provider>
  
11 <!-可选 ->
  
12 <jta-data-source>java:/DefaultDS</jta-data-source>
  
13 <!-可选 ->
  
14 <mapping-file>ormap.xml</mapping-file>
  
15 <!-可选 ->
  
16 <jar-file>MyApp.jar</jar-file>
  
17 <!-可选 ->
  
18 <class>org.acme.Employee</class>
  
19 <!-可选 ->
  
20 <shared-cache-mode>ENABLE_SELECTOVE</shared-cache-mode>
  
21 <!-可选 ->
  
22 <validation-mode>CALLBACK</validation-mode>
  
24 <!-厂商的特定属性 ->
  
25 <properties>
  
26 <!-配置Hibernate方言 ->
  
27 <property name="hibernate.dialect" value="org.hibernate.dialect.MySQL5Dialect" />
  
28 <!-配置数据库驱动 ->
  
29 <property name="hibernate.connection.driver_class" value="com.MySQL.jdbc.Driver" />
  
30 <!-配置数据库用户名 ->
  
31 <property name="hibernate.connection.username" value="root" />
  
32 <!-配置数据库密码 ->
  
33 <property name="hibernate.connection.password" value="root" />
  
34 <!-配置数据库url ->
  
35 <property name="hibernate.connection.url" value="jdbc:MySQL://localhost:3306/jpa?useUnicode=true&characterEncoding=UTF-8" />
  
36 <!-设置外连接抓取树的最大深度 ->
  
37 <property name="hibernate.max_fetch_depth" value="3" />
  
38 <!-自动输出schema创建DDL语句 ->
  
39 <property name="hibernate.hbm2ddl.auto" value="update" />
  
40 </properties>
  
41 </persistence-unit>
  
43 </persistence>
  
复制代码

xsi:schemaLocation="http://java.sun.com/xml/ns/persistence http://java.sun.com/xml/ns/persistence/persistence_2_0.xsd"

要注意使用的是2.0规范

name

JPA2.0规范要求每一个持久化单元必须有一个名字，不能为空。即persistence-unit name="manager1"的name不能为空。

transaction-type

使用的事务类型。有JTA和RESOURCE_LOCAL两种类型可以选择。在JavaEE环境中默认为JTA,在JavaSE环境中默认为RESOURCE_LOCAL。当在persistent.xml文件使用<jta-data-source>,默认就是JTA事务，使用<non-jta-data-source>，默认就是使用RESOURCE_LOCAL事务。这两种事务的区别不在这里讨论。

provider

EJB Persistence provider的一个实现类。如果不是使用多个厂商的 EJB Persistence实现，是不需要定义的。

mapping-file

指定映射文件的位置

jar-file

指定要解析的jar。jar中所有注解的类、包和所有的hbm.xml都会被添加到persistent-unit的配置中。主要用在JavaEE环境中。

exclude-unlisted-classes

不检查jar中加了@Entity注解的类。

class

明确指定要映射的类

shared-cache-mode

缓存模式。加了@Cacheable注解的默认为二级缓存。有四种模式: ALL-缓存所有实体；NONE-禁止缓存；ENABLE_SELECTIVE-如果加了缓存的标识，是默认的选选项；DISABLE_SELECTIVE- enable caching unless explicitly marked as @Cacheable(false) (not recommended)

validation-mode

实体的验证模式，默认是激活的。当一个实体在创建、更新，在实体发送到数据库前会被进行验证。CALLBACK: entities are validated on creation, update and deletion. If no Bean Validation provider is present, an exception is raised at initialization time.

properties

配置厂商的一些特定属性。

http://www.cnblogs.com/luxh/archive/2012/05/24/2516282.html