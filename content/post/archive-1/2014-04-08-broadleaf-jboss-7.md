---
title: broadleaf jboss 7 ， linux
author: wiloon
type: post
date: 2014-04-08T09:24:47+00:00
url: /?p=6483
categories:
  - Uncategorized
tags:
  - Brodleaf

---
https://github.com/BroadleafCommerce/docs/blob/3.1/Tutorials/Getting-Started-Tutorials/JBoss-Tutorial.md

Our reference architecture specifies Tomcat as our default container. However, developers may wish to launch Broadleaf Commerce in JBoss for any number of reasons. This tutorial provides the steps necessary to use JBoss AS 7 as the container in which to launch an instance of Broadleaf Commerce version 3.1.x. Note, JBoss AS 7 compatibility for Broadleaf Commerce requires the latest 3.1.1-SNAPSHOT version (or 3.1.1-GA, when available)

Assumptions:

You&#8217;re using 3.1.1-SNAPSHOT (or 3.1.1-GA, when available)

You&#8217;re using MySql (you can swap out the instructions below with the driver and JDBC information applicable to your RDBMS)

You&#8217;re launching JBoss using the standalone configuration

You&#8217;re installing the Broadleaf Commerce Heat Clinic demo on JBoss (or a project based on the Heat Clinic demo)

If you&#8217;re using JRebel, make sure you&#8217;re using version 5.5.1 (or later), as earlier versions cause significant delays during JBoss startup

Configure JBoss

Download and install JBoss AS 7 (https://www.jboss.org/jbossas/downloads.html)

Setup datasources for Broadleaf Commerce.

Edit standalone.xml ([jboss installation]/standalone/configuration/standalone.xml)

Add datasource definitions to the datasources subsystem element (change JDBC connection information as appropriate for your environment)

<subsystem xmlns="urn:jboss:domain:datasources:1.0">

<datasources>

&#8230;

<datasource jndi-name="java:/jdbc/web" pool-name="webDS" enabled="true" use-java-context="true">

<connection-url>jdbc:mysql://localhost:3306/broadleaf</connection-url>

<driver>mysql</driver>

<security>

<user-name>root</user-name>

<password>sa</password>

</security>

</datasource>

<datasource jndi-name="java:/jdbc/storage" pool-name="storageDS" enabled="true" use-java-context="true">

<connection-url>jdbc:mysql://localhost:3306/broadleaf</connection-url>

<driver>mysql</driver>

<security>

<user-name>root</user-name>

<password>sa</password>

</security>

</datasource>

<datasource jndi-name="java:/jdbc/secure" pool-name="secureDS" enabled="true" use-java-context="true">

<connection-url>jdbc:mysql://localhost:3306/broadleaf</connection-url>

<driver>mysql</driver>

<security>

<user-name>root</user-name>

<password>sa</password>

</security>

</datasource>

&#8230;

Setup a database driver

Edit standalone.xml

Add a driver definition to the datasources subsystem element

<subsystem xmlns="urn:jboss:domain:datasources:1.0">

<datasources>

&#8230;

<drivers>

&#8230;

<driver name="mysql" module="com.mysql.jdbc">

<driver-class>com.mysql.jdbc.Driver</driver-class>

</driver>

</drivers>

</datasources>

</subsystem>

Install the driver jar file

Create a new directory structure for your driver in your JBoss installation ([jboss installation]/modules/com/mysql/jdbc/main)

Copy your JDBC driver jar into the "main" directory you just created

Create a module.xml file in the "main" directory. Here are its contents:

<?xml version="1.0" encoding="UTF-8"?>

<module xmlns="urn:jboss:module:1.0" name="com.mysql.jdbc">

<resources>

<resource-root path="mysql-connector-java-5.1.25.jar"/>

<!&#8211; Insert resources here &#8211;>

</resources>

<dependencies>

<module name="javax.api"/>

<module name="javax.transaction.api"/>

</dependencies>

</module>

Configure SSL (allows secure pages during checkout in Heat Clinic)

A mvn install on the Heat Clinic demo will cause a keystore file to be created in [heat clinic installation]/site/target/[module name]/WEB-INF/blc-example.keystore

You can use this sample keystore file to configure SSL for JBoss (or, you can use a keystore from a real certificate)

Copy blc-example.keystore to [jboss installation]/standalone/configuration/blc-example.keystore

Edit standalone.xml

Add a secure connector to the web subsystem element

<subsystem xmlns="urn:jboss:domain:web:1.1" native="false" default-virtual-server="default-host">

&#8230;

<connector name="https" protocol="HTTP/1.1" scheme="https" socket-binding="https" secure="true">

<ssl name="https" password="broadleaf" certificate-key-file="../standalone/configuration/blc-example.keystore"/>

</connector>

&#8230;

</subsystem>

Configure the Application

It&#8217;s best to avoid the JPA scanning done by JBoss. This can be achieved by making sure there are no files named persistence.xml in the codebase.

In older versions of Heat Clinic, there is a filed called persistence.xml in [heat clinic installation]/core/src/main/resources/META-INF/persistence.xml

If it&#8217;s not done already, rename this file persistence-core.xml

Change any spring application context elements pointing to this file to persistence-core.xml (see this example)

<bean id="blMergedPersistenceXmlLocations" class="org.springframework.beans.factory.config.ListFactoryBean">

<property name="sourceList">

<list>

<value>classpath*:/META-INF/persistence-core.xml</value>

</list>

</property>

</bean>

Here is the list of known files containing this persistence.xml reference

[heat clinic installation]/admin/src/main/webapp/WEB-INF/applicationContext-admin.xml

[heat clinic installation]/site/src/main/webapp/WEB-INF/applicationContext.xml

Remove any unused resource-ref elements in web.xml

In regard to Heat Clinic, if it&#8217;s not removed already, delete the resource-ref element from [heat clinic installation]/site/src/main/webapp/WEB-INF/web.xml

Configure the application to exclude some unwanted JBoss modules

Create a file called jboss-deployment-structure.xml at

[heat clinic installation]/site/src/main/webapp/WEB-INF/jboss-deployment-structure.xml

[heat clinic installation]/admin/src/main/webapp/WEB-INF/jboss-deployment-structure.xml

The contents of the file are:

<?xml version="1.0" encoding="UTF-8"?>

<jboss-deployment-structure>

<deployment>

<exclusions>

<module name="org.hibernate"/>

<module name="org.javassist"/>

<module name="org.apache.log4j" />

</exclusions>

<dependencies>

<module name="org.jboss.ironjacamar.jdbcadapters" slot="main"/>

</dependencies>

</deployment>

</jboss-deployment-structure>

Update the runtime properties to use the correct MySQL dialect.

In [heat clinic installation]/core/src/main/resources/runtime-properties/common-shared.properties, you will want to update the three persistence unit dialects to say:

blPU.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect

blSecurePU.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect

blCMSStorage.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect

(Optional) Make the site module deploy as ROOT.war (rather than mycompany.war)

This allows you to hit the Heat Clinic home page at http://localhost:8080 (rather than http://localhost:8080/mycompany)

Disable the default JBoss application

Edit standalone.xml

Change the enable-welcome-root param to false

<virtual-server name="default-host" enable-welcome-root="false">

Change site&#8217;s generated war file name

Edit [heat clinic installation]/site/pom.xml

Change the finalName element value to ROOT

&#8230;

<build>

<outputDirectory>${webappDirectory}/WEB-INF/classes</outputDirectory>

<finalName>ROOT</finalName>

<plugins>

<plugin>

&#8230;

At this point, you can perform a mvn install on your project and take the generated war files for admin and site and place them in [jboss installation]/standalone/deployments so that the JBoss deployment scanner can pick them up and perform the deployment. You may see the following exception during startup:

WARN \[org.jboss.as.ee\] (MSC service thread 1-1) JBAS011006: Not installing optional component org.springframework.web.context.request.async.StandardServletAsyncWebRequest due to exception: org.jboss.as.server.deployment.DeploymentUnitProcessingException: JBAS011054: Could not find default constructor for class org.springframework.web.context.request.async.StandardServletAsyncWebRequest

This warning is innocuous and can be ignored. This will likely be resolved in a future version of the Spring framework.



Jboss side change  in standlone.xml

Add datasource node

Add driver node

Add mysql driver into module

Add file blc-example.keystore

Mysql case sensitive in linux system

windows系统中导出的建表sql导出的表名都是小写的，

linux下的mysql大小写敏感，jboss7启动报错，找不到表