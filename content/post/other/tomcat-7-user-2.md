---
title: tomcat config, server, user
author: "-"
date: 2011-11-12T08:09:38+00:00
url: /?p=1510
categories:
  - Java
  - Web
tags:
  - Tomcat

---
## tomcat config, server, user
server

Listener
  
监听器，用来监听某些事件的发生。



VersionLoggerListener，启动时对tomcat，java，操作系统信息打印日志。
  
JreMemoryLeakPreventionListener,
  
JreMemoryLeakPreventionListener，防止内存溢出的监听器。
  
http://liuxi.name/blog/20160608/jvm-full-gc-hourly.html



GlobalResourcesLifecycleListener，初始化定义在元素GlobalNamingResources下的全局JNDI资源
  


ThreadLocalLeakPreventionListener，防止ThreadLocal溢出监听器。

connectionTimeout - 网络连接超时，单位: 毫秒。设置为0表示永不超时，这样设置有隐患的。通常可设置为30000毫秒。
  
keepAliveTimeout - 长连接最大保持时间 (毫秒) 

# user config

Tomcat 6
  
```xml
  
<?xml version='1.0' encoding='utf-8'?>

<tomcat-users>
  
<role rolename="tomcat"/>
  
<role rolename="role1"/>
  
<role rolename="manager"/>
  
<role rolename="admin"/>
  
<user username="tomcat" password="tomcat" roles="tomcat"/>
  
<user username="both" password="tomcat" roles="tomcat,role1"/>
  
<user username="role1" password="tomcat" roles="role1"/>
  
<user username="admin" password="admin" roles="admin,manager"/>
  
<user username="hhh" password="123456" roles="role1,tomcat,admin,manager"/>
  
</tomcat-users>
  
```

Tomcat 7
  
```xml
  
<role rolename="manager"/>
  
<role rolename="manager-gui"/>
  
<role rolename="admin"/>
  
<role rolename="admin-gui"/>
  
<user username="tomcat" password="tomcat" roles="admin-gui,admin,manager-gui,manager"/>
  
```