---
title: DBCP
author: "-"
date: 2012-03-27T08:14:53+00:00
url: /?p=2661
categories:
  - DataBase
  - Java
tags:$
  - reprint
---
## DBCP
DBCP(DataBase connection pool),数据库连接池。是 apache 上的一个 java 连接池项目，也是 tomcat 使用的连接池组件。单独使用dbcp需要3个包: common-dbcp.jar,common-pool.jar,common-collections.jar由于建立数据库连接是一个非常耗时耗资源的行为，所以通过连接池预先同数据库建立一些连接，放在内存中，应用程序需要建立数据库连接时直接到连接池中申请一个就行，用完后再放回去。
  
```java
  
class JdbcUtil
  
{
  
private static BasicDataSource bds;
  
static
  
{
  
if(bds==null)
  
{
  
bds= new BasicDatasource();
  
}
  
//分别设置数据库的连接参数
  
bds.setDriverClass
  
bds.url
  
bds.user
  
bds.root
  
}
  
public staitc Connection getConnection()
  
{
  
return bds.getConnection();
  
}
  
```
  
在spring中配置dbcp:
  
beans.xml:
  
```xml
  
<bean
  
class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
  
<property name="locations">
  
<value>classpath:jdbc.properties</value>
  
</property>
  
</bean>
  
<bean id="dataSource" destroy-method="close"
  
class="org.apache.commons.dbcp.BasicDataSource">
  
<property name="driverClassName" value="${jdbc.driverClassName}" />
  
<property name="url" value="${jdbc.url}" />
  
<property name="username" value="${jdbc.username}" />
  
<property name="password" value="${jdbc.password}" />
  
</bean>
  
```
  
jdbc.properties: //放在classpath下
  
jdbc.driverClassName=com.MySQL.jdbc.Driver
  
jdbc.url=jdbc:MySQL://localhost:3306/数据库名
  
jdbc.username=root
  
jdbc.password=\***\*****