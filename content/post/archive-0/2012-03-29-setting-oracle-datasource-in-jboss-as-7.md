---
title: Setting Oracle Datasource in JBoss AS 7
author: wiloon
type: post
date: 2012-03-29T09:12:18+00:00
url: /?p=2680
categories:
  - DataBase
  - Development
tags:
  - Jboss

---
srikanth.s.nair

<div>
  <a href="http://www.javaworld.com/community/node/8184">http://www.javaworld.com/community/node/8184</a>
</div>

<div id="nodezone">
  <p>
    Here are step by step directions on how to configure JBoss AS 7 to communicate with Oracle XE.
  </p>
  
  <p>
    1. Create directory for the oracle driver deployment
  </p>
  
  <div>
    <code>$ cd $JBOSS_HOME/modules&lt;br />
$ mkdir -p com/oracle/ojdbc6/main&lt;br />
$ vi module.xml</code>
  </div>
  
  <p>
    Add the following snippet to the newly created module.xml file
  </p>
  
  <div>
    <code>&lt;module xmlns="urn:jboss:module:1.0" name="com.oracle.ojdbc6"&gt;&lt;br />
&lt;resources&gt;&lt;br />
&lt;resource-root path="ojdbc6.jar"/&gt;&lt;br />
&lt;/resources&gt;&lt;br />
&lt;dependencies&gt;&lt;br />
&lt;module name="javax.api"/&gt;&lt;br />
&lt;/dependencies&gt;&lt;br />
&lt;/module&gt;</code>
  </div>
  
  <p>
    Copy the ojdbc6.jar to $JBOSS_HOME/modules/com/oracle/ojdbc6/main [make sure your jar META-INF folder is having a Services dir with a file called java.sql.Driver]
  </p>
  
  <p>
    Next, create the driver definition in the standalone configuration file
  </p>
  
  <div>
    <code>$ vi $JBOSS_HOME/standalone/configuration/standalone.xml</code>
  </div>
  
  <p>
    Look for
  </p>
  
  <div>
    <code>&lt;subsystem xmlns="urn:jboss:domain:datasources:1.0"&gt;  </code>
  </div>
  
  <p>
    this is where the datasource and driver configuration will go. Within this subsystem, look for the section and add the following:
  </p>
  
  <div>
    <code>&lt;driver name="oracle" module="com.oracle.ojdbc6"&gt;&lt;br />
&lt;xa-datasource-class&gt;&lt;br />
oracle.jdbc.OracleDriver&lt;br />
&lt;/xa-datasource-class&gt;&lt;br />
&lt;/driver&gt;</code>
  </div>
  
  <p>
    Then create the datasource configuration, also in the standalone configuration file. The following block will go just below the<code> &lt;datasources&gt;</code>element.
  </p>
  
  <div>
    <code>&lt;datasource jndi-name="WorkCenterDS" pool-name="OracleDS" enabled="true" jta="true" use-java-context="true" use-ccm="true"&gt;&lt;br />
&lt;connection-url&gt;jdbc:oracle:thin:@localhost:1521:oradb1&lt;/connection-url&gt;&lt;br />
&lt;driver&gt;oracle&lt;/driver&gt;&lt;br />
&lt;transaction-isolation&gt;TRANSACTION_READ_COMMITTED&lt;/transaction-isolation&gt;&lt;br />
&lt;pool&gt;&lt;br />
&lt;prefill&gt;true&lt;/prefill&gt;&lt;br />
&lt;use-strict-min&gt;false&lt;/use-strict-min&gt;&lt;br />
&lt;flush-strategy&gt;FailingConnectionOnly&lt;/flush-strategy&gt;&lt;br />
&lt;/pool&gt;&lt;br />
&lt;security&gt;&lt;br />
&lt;user-name&gt;user1&lt;/user-name&gt;&lt;br />
&lt;password&gt;1234&lt;/password&gt;&lt;br />
&lt;/security&gt;&lt;br />
&lt;/datasource&gt;</code>
  </div>
  
  <p>
    Restart JBoss and look for the following lines in your log file to determine if the deployment succeeded.
  </p>
</div>