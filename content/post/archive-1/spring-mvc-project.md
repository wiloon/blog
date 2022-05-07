---
title: Create spring mvc project
author: "-"
date: 2014-12-03T02:21:36+00:00
url: /?p=7079
categories:
  - Inbox
tags:
  - reprint
---
## Create spring mvc project
gradle plugin:

apply plugin: 'idea'

apply plugin: 'eclipse'

apply plugin: 'war'


**gradle dependencies:**

compile("org.springframework:spring-core:$versionSpring",
  
"org.springframework:spring-context:$versionSpring",
  
"org.springframework:spring-web:$versionSpring",
  
"org.springframework:spring-webmvc:$versionSpring",
  
"org.springframework:spring-jdbc:$versionSpring",
  
"org.springframework:spring-orm:$versionSpring"
  
)


**web.xml**

create web.xml in .../webapp/WEB-INF/

http://www.wiloon.com/?p=3459


**add context loader listener**

org.springframework.web.context.ContextLoaderListener


**spring schema index**

http://www.springframework.org/schema/beans/


Create controller

/JavaEEX/src/main/java/com/wiloon/javaeex/controller/FooController.java


create springMvc.xml


for eclipse project convert project to web project