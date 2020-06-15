---
title: JPA的persistence.xml文件
author: wiloon
type: post
date: 2014-05-29T05:47:15+00:00
url: /?p=6688
categories:
  - Uncategorized
tags:
  - JPA

---
Posted on 2012-05-24 12:27 CN.programmer.Luxh 阅读(7217) 评论(0) 编辑 收藏
  
persistence.xml文件必须定义在classpath路径下的META-INF文件夹中。



我们看看基于Hibernate提供的一个比较完整的JPA2.0的persistence.xml文件。

persistence.xml:

复制代码
  
1 <?xml version=&#8221;1.0" encoding=&#8221;UTF-8"?>
  
2 <persistence version=&#8221;2.0" xmlns=&#8221;http://java.sun.com/xml/ns/persistence&#8221;
  
3 xmlns:xsi=&#8221;http://www.w3.org/2001/XMLSchema-instance&#8221;
  
4 xsi:schemaLocation=&#8221;http://java.sun.com/xml/ns/persistence
  
5 http://java.sun.com/xml/ns/persistence/persistence\_2\_0.xsd&#8221;>
  
6
  
7 <!&#8211;必须要有name属性，不能为空 &#8211;>
  
8 <persistence-unit name=&#8221;jpaPU&#8221; transaction-type=&#8221;RESOURCE_LOCAL&#8221;>
  
9 <!&#8211;可选 &#8211;>
  
10 <provider>org.hibernate.ejb.HibernatePersistence</provider>
  
11 <!&#8211;可选 &#8211;>
  
12 <jta-data-source>java:/DefaultDS</jta-data-source>
  
13 <!&#8211;可选 &#8211;>
  
14 <mapping-file>ormap.xml</mapping-file>
  
15 <!&#8211;可选 &#8211;>
  
16 <jar-file>MyApp.jar</jar-file>
  
17 <!&#8211;可选 &#8211;>
  
18 <class>org.acme.Employee</class>
  
19 <!&#8211;可选 &#8211;>
  
20 <shared-cache-mode>ENABLE_SELECTOVE</shared-cache-mode>
  
21 <!&#8211;可选 &#8211;>
  
22 <validation-mode>CALLBACK</validation-mode>
  
23
  
24 <!&#8211;厂商的特定属性 &#8211;>
  
25 <properties>
  
26 <!&#8211;配置Hibernate方言 &#8211;>
  
27 <property name=&#8221;hibernate.dialect&#8221; value=&#8221;org.hibernate.dialect.MySQL5Dialect&#8221; />
  
28 <!&#8211;配置数据库驱动 &#8211;>
  
29 <property name=&#8221;hibernate.connection.driver_class&#8221; value=&#8221;com.mysql.jdbc.Driver&#8221; />
  
30 <!&#8211;配置数据库用户名 &#8211;>
  
31 <property name=&#8221;hibernate.connection.username&#8221; value=&#8221;root&#8221; />
  
32 <!&#8211;配置数据库密码 &#8211;>
  
33 <property name=&#8221;hibernate.connection.password&#8221; value=&#8221;root&#8221; />
  
34 <!&#8211;配置数据库url &#8211;>
  
35 <property name=&#8221;hibernate.connection.url&#8221; value=&#8221;jdbc:mysql://localhost:3306/jpa?useUnicode=true&characterEncoding=UTF-8" />
  
36 <!&#8211;设置外连接抓取树的最大深度 &#8211;>
  
37 <property name=&#8221;hibernate.max\_fetch\_depth&#8221; value=&#8221;3" />
  
38 <!&#8211;自动输出schema创建DDL语句 &#8211;>
  
39 <property name=&#8221;hibernate.hbm2ddl.auto&#8221; value=&#8221;update&#8221; />
  
40 </properties>
  
41 </persistence-unit>
  
42
  
43 </persistence>
  
复制代码

xsi:schemaLocation=&#8221;http://java.sun.com/xml/ns/persistence http://java.sun.com/xml/ns/persistence/persistence\_2\_0.xsd&#8221;

要注意使用的是2.0规范

name

JPA2.0规范要求每一个持久化单元必须有一个名字，不能为空。即persistence-unit name=&#8221;manager1"的name不能为空。

transaction-type

使用的事务类型。有JTA和RESOURCE\_LOCAL两种类型可以选择。在JavaEE环境中默认为JTA,在JavaSE环境中默认为RESOURCE\_LOCAL。当在persistent.xml文件使用<jta-data-source>,默认就是JTA事务，使用<non-jta-data-source>，默认就是使用RESOURCE_LOCAL事务。这两种事务的区别不在这里讨论。

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

缓存模式。加了@Cacheable注解的默认为二级缓存。有四种模式：ALL-缓存所有实体；NONE-禁止缓存；ENABLE\_SELECTIVE-如果加了缓存的标识，是默认的选选　　　　　　　　项；DISABLE\_SELECTIVE- enable caching unless explicitly marked as @Cacheable(false) (not recommended)

validation-mode

实体的验证模式，默认是激活的。当一个实体在创建、更新，在实体发送到数据库前会被进行验证。CALLBACK: entities are validated on creation, update and deletion. If no Bean Validation provider is present, an exception is raised at initialization time.

properties

配置厂商的一些特定属性。

http://www.cnblogs.com/luxh/archive/2012/05/24/2516282.html