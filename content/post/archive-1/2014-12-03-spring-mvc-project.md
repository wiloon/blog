---
title: Create spring mvc project
author: wiloon
type: post
date: 2014-12-03T02:21:36+00:00
url: /?p=7079
categories:
  - Uncategorized

---
gradle plugin:

apply plugin: &#8216;idea&#8217;

apply plugin: &#8216;eclipse&#8217;

apply plugin: &#8216;war&#8217;

&nbsp;

**gradle dependencies:**

compile(&#8220;org.springframework:spring-core:$versionSpring&#8221;,
  
&#8220;org.springframework:spring-context:$versionSpring&#8221;,
  
&#8220;org.springframework:spring-web:$versionSpring&#8221;,
  
&#8220;org.springframework:spring-webmvc:$versionSpring&#8221;,
  
&#8220;org.springframework:spring-jdbc:$versionSpring&#8221;,
  
&#8220;org.springframework:spring-orm:$versionSpring&#8221;
  
)

&nbsp;

**web.xml**

create web.xml in &#8230;/webapp/WEB-INF/

http://www.wiloon.com/wordpress/?p=3459

&nbsp;

**add context loader listener**

org.springframework.web.context.ContextLoaderListener

&nbsp;

**spring schema index**

http://www.springframework.org/schema/beans/

&nbsp;

Create controller

/JavaEEX/src/main/java/com/wiloon/javaeex/controller/FooController.java

&nbsp;

create springMvc.xml

&nbsp;

for eclipse project convert project to web project