---
title: spring生成EntityManagerFactory的三种方式
author: "-"
date: 2014-05-29T11:38:28+00:00
url: /?p=6695
categories:
  - Inbox
tags:
  - Spring

---
## spring生成EntityManagerFactory的三种方式
1.LocalEntityManagerFactoryBean
  
只是简单环境中使用。它使用JPA PersistenceProvider自动检测机制( according to JPA's Java SE bootstrapping ),并且大多数情况下,你只能定义一下persistence unit name

例如: 

<beans>
  
<bean id="myEmf" class="org.springframework.orm.jpa.LocalEntityManagerFactoryBean">
  
<property name="persistenceUnitName" value="myPersistenceUnit"/>
  
</bean>
  
</beans>
  
2.从JNDI获取EntityManagerFactory
  
这个选项是当你应用发布在javaee5的服务器中。你可以参阅自己应用服务器文档,如何发布一个自定义的JPA provider到你的应用服务器中。

例: 

<beans>
  
<jee:jndi-lookup id="myEmf" jndi-name="persistence/myPersistenceUnit"/>
  
</beans>
  
当javaee服务器启动时,会自动检测persistence units。实际上,是检测应用包中的META-INF/persistence.xml 文件和web.xml中的persistence-unit-ref,以及定义的environment naming。我理解就是JNDI的name。

一般应用情景是: 

在META-INF/persistence.xml中 使用<jta-data-source>java:/ MySQLDS</jta-data-source> 获取容器发布的Datesource。

transactions是使用的javaee容器支持的JTA系统,例如tomcat中,可以这样

如果你的项目准备部署在tomcat上,要支持jta,则需把相关的包放在tomcat/lib包下
  
1) jndi配置,可以把jndi的配置放置在 tomcat/conf/Catalina/域名(如localhost)/项目名.xml
  
文件的Context节点下,如下: 
  
<Resource name="" auth="Container" type="javax.sql.DataSource"
  
username=""
  
password=""
  
driveClassName="oracle.jdbc.driver.OracleDriver"
  
url="" maxActive="45" maxIdle="25"/>
  
jndi也可以配置在server.xml,context.xml中
  
2)jta UserTransaction配置
  
在server.xml文件GlobalNamingResources节点下配置如下: 
  
<!- Resource configuration for UserTransaction
  
use JOTM ->
  
<Resource name="UserTransaction" auth="Container"
  
type="javax.transaction.UserTransaction"
  
factory="org.objectweb.jotm.UserTransactionFactory"
  
jotm.timeout="60"/>
  
然后在 项目名.xml 文件的context节点下加: 
  
<ResourceLink name="UserTransaction"
  
global="UserTransaction"
  
type="javax.transaction.UserTransaction"/>

SPRING 仅仅做的是是把EntityManagerFactory通过依赖注入到应用的object中。如果要管理事务,则使用JtaTransactionManager。
  
3.LocalContainerEntityManagerFactoryBean
  
这个选项中,spring扮演了容器的角色。完全掌管JPA。

LocalContainerEntityManagerFactoryBean会根据persistence.xml创造一个PersistenceUnitInfo实现。

<beans>
  
<bean id="myEmf" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
  
<property name="dataSource" ref="someDataSource"/>
  
<property name="loadTimeWeaver">
  
<bean class="org.springframework.instrument.classloading.InstrumentationLoadTimeWeaver"/>
  
</property>
  
</bean>
  
</beans>
  
不是所有的JPA provider都需要load-time weaving。hibernate就不需要。呵呵。 <property name="loadTimeWeaver">这个就不是必须的了。。

Persistence.xml配置: 

<persistence xmlns="http://java.sun.com/xml/ns/persistence" version="1.0">
  
<persistence-unit name="myUnit" transaction-type="RESOURCE_LOCAL">
  
<mapping-file>META-INF/orm.xml</mapping-file>
  
<exclude-unlisted-classes/>
  
</persistence-unit>
  
</persistence>
  
如何处理多个persistence units。spring提供了PersistenceUnitManager统一管理。

<bean id="pum" class="org.springframework.orm.jpa.persistenceunit.DefaultPersistenceUnitManager">
  
<property name="persistenceXmlLocations">
  

  
<value>org/springframework/orm/jpa/domain/persistence-multi.xml</value>
  
<value>classpath:/my/package/**/custom-persistence.xml</value>
  
<value>classpath*:META-INF/persistence.xml</value>
  
</list>
  
</property>
  
<property name="dataSources">
  
<map>
  
<entry key="localDataSource" value-ref="local-db"/>
  
<entry key="remoteDataSource" value-ref="remote-db"/>
  
</map>
  
</property>
  
<!- if no datasource is specified, use this one ->
  
<property name="defaultDataSource" ref="remoteDataSource"/>
  
</bean>
  
<bean id="emf" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
  
<property name="persistenceUnitManager" ref="pum"/>
  
<property name="persistenceUnitName" value="myCustomUnit"/>
  
</bean>
  
dataSources中的key是persistence.xml中配置的datasource名字,value-ref是spring管理的数据源。


另外: 

EntityManagerFactory是线程安全的,但是EntityManager不是。

复制代码
  
public class ProductDaoImpl implements ProductDao {
  
private EntityManagerFactory emf;
  
@PersistenceUnit
  
public void setEntityManagerFactory(EntityManagerFactory emf) {
  
this.emf = emf;
  
}
  
public Collection loadProductsByCategory(String category) {
  
EntityManager em = this.emf.createEntityManager();
  
try {
  
Query query = em.createQuery("from Product as p where p.category = ?1");
  
query.setParameter(1, category);
  
return query.getResultList();
  
}
  
finally {
  
if (em != null) {
  
em.close();
  
}
  
}
  
}
  
}
  
复制代码
  
这样使用有个最大问题就是每次都要创建一个新的entityManager。那么该怎么办？

你可以通过@PersistenceContext获取一个transactional EntityManager("shared EntityManager")。为什么称它为transactional？因为它是一个共享的以及线程安全的当前的transactional EntityManager的一个代理。

复制代码
  
public class ProductDaoImpl implements ProductDao {
  
@PersistenceContext
  
private EntityManager em;
  
public Collection loadProductsByCategory(String category) {
  
Query query = em.createQuery("from Product as p where p.category = :category");
  
query.setParameter("category", category);
  
return query.getResultList();
  
}
  
}
  
复制代码
  
结束了。

http://www.cnblogs.com/beiyeren/archive/2013/01/23/2873210.html