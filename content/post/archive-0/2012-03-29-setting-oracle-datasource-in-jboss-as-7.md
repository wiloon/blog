---
title: Setting Oracle Datasource in JBoss AS 7
author: "-"
type: post
date: 2012-03-29T09:12:18+00:00
url: /?p=2680
categories:
  - DataBase
  - Development
tags:
  - Jboss

---
## Setting Oracle Datasource in JBoss AS 7
srikanth.s.nair

  http://www.javaworld.com/community/node/8184


  
    Here are step by step directions on how to configure JBoss AS 7 to communicate with Oracle XE.
  
  
    1. Create directory for the oracle driver deployment
  
  
    <code>$ cd $JBOSS_HOME/modules

$ mkdir -p com/oracle/ojdbc6/main

$ vi module.xml</code>
  
  
    Add the following snippet to the newly created module.xml file
  
  
    <code><module xmlns="urn:jboss:module:1.0" name="com.oracle.ojdbc6">

<resources>

<resource-root path="ojdbc6.jar"/>

</resources>

<dependencies>

<module name="javax.api"/>

</dependencies>

</module></code>
  
  
    Copy the ojdbc6.jar to $JBOSS_HOME/modules/com/oracle/ojdbc6/main [make sure your jar META-INF folder is having a Services dir with a file called java.sql.Driver]
  
  
    Next, create the driver definition in the standalone configuration file
  
  
    <code>$ vi $JBOSS_HOME/standalone/configuration/standalone.xml</code>
  
  
    Look for
  
  
    <code><subsystem xmlns="urn:jboss:domain:datasources:1.0">  </code>
  
  
    this is where the datasource and driver configuration will go. Within this subsystem, look for the section and add the following:
  
  
    <code><driver name="oracle" module="com.oracle.ojdbc6">

<xa-datasource-class>

oracle.jdbc.OracleDriver

</xa-datasource-class>

</driver></code>
  
  
    Then create the datasource configuration, also in the standalone configuration file. The following block will go just below the<code> <datasources></code>element.
  
  
    <code><datasource jndi-name="WorkCenterDS" pool-name="OracleDS" enabled="true" jta="true" use-java-context="true" use-ccm="true">

<connection-url>jdbc:oracle:thin:@localhost:1521:oradb1</connection-url>

<driver>oracle</driver>

<transaction-isolation>TRANSACTION_READ_COMMITTED</transaction-isolation>

<pool>

true</prefill>

<use-strict-min>false</use-strict-min>

<flush-strategy>FailingConnectionOnly</flush-strategy>

</pool>

<security>

<user-name>user1</user-name>

<password>1234</password>

</security>

</datasource></code>
  
  
    Restart JBoss and look for the following lines in your log file to determine if the deployment succeeded.
  
