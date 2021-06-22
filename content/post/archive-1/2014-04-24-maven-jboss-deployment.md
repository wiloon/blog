---
title: maven jboss deployment
author: "-"
type: post
date: 2014-04-24T06:56:39+00:00
url: /?p=6554
categories:
  - Uncategorized

---
[xml]

<plugin>
   
<groupId>org.jboss.as.plugins</groupId>
   
<artifactId>jboss-as-maven-plugin</artifactId>
   
<version>7.5.Final</version>
   
<configuration>
   
<hostname>127.0.0.1</hostname>
   
<port>9999</port>
   
<username>user0</username>
   
<password>password0</password>
   
</configuration>
   
</plugin>

[/xml]
  
[xml]

<management-interfaces>
   
<http-interface security-realm="ManagementRealm" http-upgrade-enabled="true">
   
<socket-binding http="management-http"/>
   
</http-interface>
   
<native-interface security-realm="ManagementRealm">
   
<socket interface="management" port="${jboss.management.native.port:9999}"/>
   
</native-interface>
   
</management-interfaces>

[/xml]

http://jbosscn.iteye.com/blog/1350214