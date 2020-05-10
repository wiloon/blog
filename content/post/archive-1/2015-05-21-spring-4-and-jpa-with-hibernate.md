---
title: Spring 4 and JPA with Hibernate
author: wiloon
type: post
date: 2015-05-21T05:59:02+00:00
url: /?p=7699
categories:
  - Uncategorized
tags:
  - JPA
  - Spring

---
http://www.baeldung.com/2011/12/13/the-persistence-layer-with-spring-3-1-and-jpa/

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
  
1
  
2
  
3
  
4
  
5
  
6
  
7
  
8
  
9
  
10
  
11
  
12
  
13
  
14
  
15
  
16
  
17
  
18
  
19
  
20
  
21
  
22
  
23
  
24
  
25
  
26
  
27
  
28
  
29
  
30
  
31
  
32
  
33
  
34
  
35
  
36
  
37
  
38
  
39
  
40
  
41
  
42
  
43
  
44
  
45
  
46
  
47
  
@Configuration
  
@EnableTransactionManagement
  
public class PersistenceJPAConfig{

@Bean
  
public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
  
LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
  
em.setDataSource(dataSource());
  
em.setPackagesToScan(new String[] { &#8220;org.baeldung.persistence.model&#8221; });

JpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
  
em.setJpaVendorAdapter(vendorAdapter);
  
em.setJpaProperties(additionalProperties());

return em;
  
}

@Bean
  
public DataSource dataSource(){
  
DriverManagerDataSource dataSource = new DriverManagerDataSource();
  
dataSource.setDriverClassName(&#8220;com.mysql.jdbc.Driver&#8221;);
  
dataSource.setUrl(&#8220;jdbc:mysql://localhost:3306/spring_jpa&#8221;);
  
dataSource.setUsername( &#8220;tutorialuser&#8221; );
  
dataSource.setPassword( &#8220;tutorialmy5ql&#8221; );
  
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
  
properties.setProperty(&#8220;hibernate.hbm2ddl.auto&#8221;, &#8220;create-drop&#8221;);
  
properties.setProperty(&#8220;hibernate.dialect&#8221;, &#8220;org.hibernate.dialect.MySQL5Dialect&#8221;);
  
return properties;
  
}
  
}
  
Also, note that, before Spring 3.2, cglib had to be on the classpath for Java @Configurationclasses to work; to better understand the need for cglib as a dependency, see this discussion about the cglib artifact in Spring.

3. The JPA Spring Configuration with XML
  
The same Spring Configuration with XML:

?
  
1
  
2
  
3
  
4
  
5
  
6
  
7
  
8
  
9
  
10
  
11
  
12
  
13
  
14
  
15
  
16
  
17
  
18
  
19
  
20
  
21
  
22
  
23
  
24
  
25
  
26
  
27
  
28
  
29
  
30
  
31
  
32
  
33
  
34
  
35
  
36
  
37
  
38
  
39
  
40
  
<?xml version=&#8221;1.0&#8243; encoding=&#8221;UTF-8&#8243;?>
  
<beans xmlns=&#8221;http://www.springframework.org/schema/beans&#8221;
  
xmlns:xsi=&#8221;http://www.w3.org/2001/XMLSchema-instance&#8221;
  
xmlns:tx=&#8221;http://www.springframework.org/schema/tx&#8221;
  
xsi:schemaLocation=&#8221;
  
http://www.springframework.org/schema/beans
  
http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
  
http://www.springframework.org/schema/tx
  
http://www.springframework.org/schema/tx/spring-tx-3.2.xsd&#8221;>

<bean id=&#8221;myEmf&#8221; class=&#8221;org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean&#8221;>
  
<property name=&#8221;dataSource&#8221; ref=&#8221;dataSource&#8221; />
  
<property name=&#8221;packagesToScan&#8221; value=&#8221;org.baeldung.persistence.model&#8221; />
  
<property name=&#8221;jpaVendorAdapter&#8221;>
  
<bean class=&#8221;org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter&#8221; />
  
</property>
  
<property name=&#8221;jpaProperties&#8221;>
  
<props>
  
<prop key=&#8221;hibernate.hbm2ddl.auto&#8221;>create-drop</prop>
  
<prop key=&#8221;hibernate.dialect&#8221;>org.hibernate.dialect.MySQL5Dialect</prop>
  
</props>
  
</property>
  
</bean>

<bean id=&#8221;dataSource&#8221; class=&#8221;org.springframework.jdbc.datasource.DriverManagerDataSource&#8221;>
  
<property name=&#8221;driverClassName&#8221; value=&#8221;com.mysql.jdbc.Driver&#8221; />
  
<property name=&#8221;url&#8221; value=&#8221;jdbc:mysql://localhost:3306/spring_jpa&#8221; />
  
<property name=&#8221;username&#8221; value=&#8221;tutorialuser&#8221; />
  
<property name=&#8221;password&#8221; value=&#8221;tutorialmy5ql&#8221; />
  
</bean>

<bean id=&#8221;transactionManager&#8221; class=&#8221;org.springframework.orm.jpa.JpaTransactionManager&#8221;>
  
<property name=&#8221;entityManagerFactory&#8221; ref=&#8221;myEmf&#8221; />
  
</bean>
  
<tx:annotation-driven />

<bean id=&#8221;persistenceExceptionTranslationPostProcessor&#8221;
  
class=&#8221;org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor&#8221; />

</beans>
  
There is a relatively small difference between the way Spring is configured in XML and the new Java based configuration – in XML, a reference to another bean can point to either the bean or a bean factory for that bean. In Java however, since the types are different, the compiler doesn’t allow it, and so the EntityManagerFactory is first retrieved from it’s bean factory and then passed to the transaction manager:

txManager.setEntityManagerFactory( this.entityManagerFactoryBean().getObject() );

4. Going full XML-less
  
Usually JPA defines a persistence unit through the META-INF/persistence.xml file. Starting with Spring 3.1, the persistence.xml is no longer necessary – theLocalContainerEntityManagerFactoryBean now supports a ‘packagesToScan’ property where the packages to scan for @Entity classes can be specified.

This file was the last piece of XML to be removed – now, JPA can be fully set up with no XML.

4.1. The JPA Properties
  
JPA properties would usually be specified in the persistence.xml file; alternatively, the properties can be specified directly to the entity manager factory bean:

factoryBean.setJpaProperties( this.additionalProperties() );
  
As a side-note, if Hibernate would be the persistence provider, then this would be the way to specify Hibernate specific properties.

5. The Maven configuration
  
In addition to Spring Core and persistence dependencies – show in detail in the Spring with Maven tutorial – we also need to define JPA and Hibernate in the project, as well as a MySQL connector:

?
  
1
  
2
  
3
  
4
  
5
  
6
  
7
  
8
  
9
  
10
  
11
  
12
  
13
  
<dependency>
  
<groupId>org.hibernate</groupId>
  
<artifactId>hibernate-entitymanager</artifactId>
  
<version>4.3.5.Final</version>
  
<scope>runtime</scope>
  
</dependency>

<dependency>
  
<groupId>mysql</groupId>
  
<artifactId>mysql-connector-java</artifactId>
  
<version>5.1.30</version>
  
<scope>runtime</scope>
  
</dependency>
  
Note that the MySQL dependency is included as a reference – a driver is needed to configure the datasource, but any Hibernate supported database will do.

6. Conclusion
  
This tutorial illustrated how to configure JPA with Hibernate in Spring using both XML and Java configuration.

We also discussed how to get rid of the last piece of XML usually associated with JPA – thepersistence.xml. The final result is a lightweight, clean DAO implementation, with almost no compile-time reliance on Spring.

The implementation of this Spring JPA Tutorial can be downloaded as a working sample project.

This is an Eclipse based project, so it should be easy to import and run as it is.