---
title: spring mvc spring security
author: w1100n
type: post
date: 2014-04-29T03:45:23+00:00
url: /?p=6567
categories:
  - Uncategorized
tags:
  - Spring

---
http://www.cnblogs.com/Beyond-bit/p/SpringMVC\_And\_SpringSecurity.html


add maven dependancy

[xml]

<dependency>
  
<groupId>org.springframework</groupId>
  
<artifactId>spring-core</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>

<dependency>
  
<groupId>org.springframework</groupId>
  
<artifactId>spring-context</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>
  
<dependency>
  
<groupId>org.springframework</groupId>
  
<artifactId>spring-web</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>

[/xml]


add dispatcher servlet in web.xml

[xml]

<servlet>
  
<servlet-name>springDispatcherServlet</servlet-name>
  
<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
  
<init-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>classpath:spring-servlet.xml</param-value>
  
</init-param>
  
<load-on-startup>1</load-on-startup>
  
</servlet>
  
<servlet-mapping>
  
<servlet-name>springDispatcherServlet</servlet-name>
  
<url-pattern>/</url-pattern>
  
</servlet-mapping>

[/xml]