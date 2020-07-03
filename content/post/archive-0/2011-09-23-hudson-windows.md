---
title: hudson windows
author: wiloon
type: post
date: 2011-09-23T07:31:37+00:00
url: /?p=881
views:
  - 2
bot_views:
  - 8
categories:
  - CI

---
download hundson from http://hudson-ci.org/
  
download jboss.
  
download UnxUtils.zip from http://code.google.com/p/gears/downloads/detail?name=UnxUtils.zip&can=2&q=
  
extract UnxUtils to a folder D:programUnxUtils
  
add path D:programUnxUtilsusrlocalwbin to system evn PATH
  
copy tomcat to D:programapache-tomcat-7.0.21
  
update file D:programapache-tomcat-7.0.21confserver.xml, add URIEncoding="UTF-8" in section ..connector port... as a attribute.
  
put hudson-2.1.1.war into D:programapache-tomcat-7.0.21webapps
  
add HUDSON_HOME=D:programhudson to system environment variable,
  
start tomcat
  
set up proxy for hudson:
  
hudson > plugin manager > advanced >
  
set up proxy and save.
  
#install plug in, hudson > plugin manager > available
  
Files Found Trigger
  
URL Change Trigger

git plug in
  
...
  
go to hudson>manage hudson> configure system >
  
#set up maven:
  
name=maven2.1
  
MAVEN_HOME=D:programapache-maven-2.1.0
  
#JDK
  
click add jdk
  
name jdk1.6
  
JAVA\_HOME=D:Program FilesJavajdk1.6.0\_26
  
#E-Mail Notification
  
smtp server:xxx.xxx.xxx.xxx
  
#create a new job...maven 2 job
  
input project name and description
  
[source code management] select Git, and input the URL of repository root@xxx.xxx.xxx.xxx:/xxx/xxx
  
Branch Specifier (blank for default):**
  
#build triggers
  
select build when a url's content changes
  
note: the url should like file://x:/xxx/xxxx.xxx