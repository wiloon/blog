---
title: hudson linux
author: w1100n
type: post
date: 2011-09-26T03:42:25+00:00
url: /?p=920
bot_views:
  - 11
views:
  - 1
categories:
  - CI
  - Linux

---
  * download and copy jboss to /home/wyue/program/jboss-4.0.5-GA
  * download hudson and copy the war to /home/wyue/program/jboss-4.0.5.GA/server/default/deploy/
  * update /home/wyue/program/jboss-4.0.5.GA/server/default/deploy/jbossweb-tomcat55.sar/server.xml; add i18n config.

#start jboss
  
#open a browser ... http://localhots:xxxx/hudson-2.1.1
  
...
  
#go to Hudson>Manage Hudson>Configure System
  
[JDK]
  
input a jdk name :jdk1.6
  
input JAVA_HOME:/usr/java/jdk1.6.0_21
  
[Maven]
  
input a name : maven3
  
input MAVEN_HOME:/usr/apache-maven-3.0/bin
  
[Email Notification]
  
SMTP server:xxx.xxx.xxx.xxx
  
system admin email address xxx@xxx.xxx
  
Hudson URL: http://xxx.xxx.xxx.xxx:xxxx/hudson-2.1.1/

#go to Hudson>Manage Hudson>Manage Plugins>Available
  
#install plugin
  
email-ext: Hudson Email Extension Plugin
  
Files Found Trigger
  
URL Change Trigger
  
...
  
new project
  
input project name
  
[source code management]
  
select Git
  
input URL of repository xxx@xxx.xxx.xxx.xxx:/PROJECT_XXX/XXX
  
[Build Triggers]
  
Select Build when a URL's content changes
  
input URL file:/home/wyue/xxx/xxx