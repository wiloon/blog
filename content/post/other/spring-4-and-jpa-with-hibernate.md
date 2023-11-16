---
title: Spring 4 and JPA with Hibernate
author: "-"
date: 2015-05-21T05:59:02+00:00
url: /?p=7699
categories:
  - Inbox
tags:
  - JPA
  - Spring

---
## Spring 4 and JPA with Hibernate

[http://www.baeldung.com/2011/12/13/the-persistence-layer-with-spring-3-1-and-jpa/](http://www.baeldung.com/2011/12/13/the-persistence-layer-with-spring-3-1-and-jpa/)

Table of Contents
  
1. Overview
  
2. The JPA Spring Configuration with Java
  
3. The JPA Spring Configuration with XML
  
4. Going full XML-less
  
5. The Maven configuration
  
6. Conclusion
  
1. Overview
  
This is tutorial shows how to set up Spring with JPA, using Hibernate as a persistence provider.

For a step by step introduction about setting up the Spring context using Java based configuration and the basic Maven pom for the project, see this article.

NEW: Here is a video on setting up Hibernate 4 with Spring 4 (I recommend watching in in full 1080p):

2. The JPA Spring Configuration with Java
  
To use JPA in a Spring project, the EntityManager needs to be set up.

This is the main part of the configuration – and it is done via a Spring factory bean – either the simpler LocalEntityManagerFactoryBean or the more flexibleLocalContainerEntityManagerFactoryBean. The latter option is used here, so that additional properties can be configured on it:

?
  
@Configuration
  
@EnableTransactionManagement
  
public class PersistenceJPAConfig{

@Bean
  
public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
  
LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
  
em.setDataSource(dataSource());
  
em.setPackagesToScan(new String[] { "org.baeldung.persistence.model" });

JpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
  
em.setJpaVendorAdapter(vendorAdapter);
  
em.setJpaProperties(additionalProperties());

return em;
  
}

@Bean
  
public DataSource dataSource(){
  
DriverManagerDataSource dataSource = new DriverManagerDataSource();
  
dataSource.setDriverClassName("com.MySQL.jdbc.Driver");
  
dataSource.setUrl("jdbc:MySQL://localhost:3306/spring_jpa");
  
dataSource.setUsername( "tutorialuser" );
  
dataSource.setPassword( "tutorialmy5ql" );
  
return dataSource;
  
}

@Bean
  
public PlatformTransactionManager transactionManager(EntityManagerFactory emf){
  
JpaTransactionManager transactionManager = new JpaTransactionManager();
  
transactionManager.setEntityManagerFactory(emf);

return transactionManager;
  
}

@Bean
  
public PersistenceExceptionTranslationPostProcessor exceptionTranslation(){
  
return new PersistenceExceptionTranslationPostProcessor();
  
}

Properties additionalProperties() {
  
Properties properties = new Properties();
  
properties.setProperty("hibernate.hbm2ddl.auto", "create-drop");
  
properties.setProperty("hibernate.dialect", "org.hibernate.dialect.MySQL5Dialect");
  
return properties;
  
}
  
}
  
Also, note that, before Spring 3.2, cglib had to be on the classpath for Java @Configurationclasses to work; to better understand the need for cglib as a dependency, see this discussion about the cglib artifact in Spring.

3. The JPA Spring Configuration with XML
  
The same Spring Configuration with XML:

?
  
<?xml version="1.0" encoding="UTF-8"?>
  
<beans xmlns="http://www.springframework.org/schema/beans"
  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
xmlns:tx="http://www.springframework.org/schema/tx"
  
xsi:schemaLocation="
  
[http://www.springframework.org/schema/beans](http://www.springframework.org/schema/beans)
  
[http://www.springframework.org/schema/beans/spring-beans-3.2.xsd](http://www.springframework.org/schema/beans/spring-beans-3.2.xsd)
  
[http://www.springframework.org/schema/tx](http://www.springframework.org/schema/tx)
  
[http://www.springframework.org/schema/tx/spring-tx-3.2.xsd](http://www.springframework.org/schema/tx/spring-tx-3.2.xsd)">
[http://www.springframework.org/schema/tx/spring-tx-3.2.xsd>"](http://www.springframework.org/schema/tx/spring-tx-3.2.xsd>")

<bean id="myEmf" class="org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean">
  
<property name="dataSource" ref="dataSource" />
  
<property name="packagesToScan" value="org.baeldung.persistence.model" />
  
<property name="jpaVendorAdapter">
  
<bean class="org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter" />
  
</property>
  
<property name="jpaProperties">
  
<props>
  
<prop key="hibernate.hbm2ddl.auto">create-drop</prop>
  
<prop key="hibernate.dialect">org.hibernate.dialect.MySQL5Dialect</prop>
  
</props>
  
</property>
  
</bean>

<bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
  
<property name="driverClassName" value="com.MySQL.jdbc.Driver" />
  
<property name="url" value="jdbc:MySQL://localhost:3306/spring_jpa" />
  
<property name="username" value="tutorialuser" />
  
<property name="password" value="tutorialmy5ql" />
  
</bean>

<bean id="transactionManager" class="org.springframework.orm.jpa.JpaTransactionManager">
  
<property name="entityManagerFactory" ref="myEmf" />
  
</bean>
  
<tx:annotation-driven />

<bean id="persistenceExceptionTranslationPostProcessor"
  
class="org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor" />

</beans>
  
There is a relatively small difference between the way Spring is configured in XML and the new Java based configuration – in XML, a reference to another bean can point to either the bean or a bean factory for that bean. In Java however, since the types are different, the compiler doesn't allow it, and so the EntityManagerFactory is first retrieved from it's bean factory and then passed to the transaction manager:

txManager.setEntityManagerFactory( this.entityManagerFactoryBean().getObject() );

4. Going full XML-less
  
Usually JPA defines a persistence unit through the META-INF/persistence.xml file. Starting with Spring 3.1, the persistence.xml is no longer necessary – theLocalContainerEntityManagerFactoryBean now supports a 'packagesToScan' property where the packages to scan for @Entity classes can be specified.

This file was the last piece of XML to be removed – now, JPA can be fully set up with no XML.

4.1. The JPA Properties
  
JPA properties would usually be specified in the persistence.xml file; alternatively, the properties can be specified directly to the entity manager factory bean:

factoryBean.setJpaProperties( this.additionalProperties() );
  
As a side-note, if Hibernate would be the persistence provider, then this would be the way to specify Hibernate specific properties.

5. The Maven configuration
  
In addition to Spring Core and persistence dependencies – show in detail in the Spring with Maven tutorial – we also need to define JPA and Hibernate in the project, as well as a MySQL connector:

?
  
<dependency>
  
<groupId>org.hibernate</groupId>
  
hibernate-entitymanager</artifactId>
  
<version>4.3.5.Final</version>
  
<scope>runtime</scope>
  
</dependency>

<dependency>
  
<groupId>MySQL</groupId>
  
MySQL-connector-java</artifactId>
  
<version>5.1.30</version>
  
<scope>runtime</scope>
  
</dependency>
  
Note that the MySQL dependency is included as a reference – a driver is needed to configure the datasource, but any Hibernate supported database will do.

6. Conclusion
  
This tutorial illustrated how to configure JPA with Hibernate in Spring using both XML and Java configuration.

We also discussed how to get rid of the last piece of XML usually associated with JPA – thepersistence.xml. The final result is a lightweight, clean DAO implementation, with almost no compile-time reliance on Spring.

The implementation of this Spring JPA Tutorial can be downloaded as a working sample project.

This is an Eclipse based project, so it should be easy to import and run as it is.
