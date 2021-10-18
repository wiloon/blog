---
title: 应用springMVC时 JS等文件找不到错误
author: "-"
type: post
date: 2013-01-23T12:50:54+00:00
url: /?p=5061
categories:
  - Java
  - Web
tags:
  - Spring

---
# 应用springMVC时 JS等文件找不到错误
<http://samuel5-1.iteye.com/blog/727772>

应用springMVC时如果配置URL映射时如下配置

[xml]

<servlet>
   
<servlet-name>appServlet</servlet-name>
   
<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
   
<init-param>
   
<param-name>contextConfigLocation</param-name>
   
<param-value>/WEB-INF/spring/appServlet/servlet-context.xml</param-value>
   
</init-param>
   
<load-on-startup>1</load-on-startup>
   
</servlet>

<servlet-mapping>
   
<servlet-name>appServlet</servlet-name>
   
<url-pattern>/</url-pattern>
   
</servlet-mapping>


[/xml]

会导致页面引用的JS CSS发生找不到的错误
  
此时应在web.xml中添加

[xml]

<servlet-mapping>
   
<servlet-name>default</servlet-name>
   
<url-pattern>*.css</url-pattern>
   
</servlet-mapping>

<servlet-mapping>
   
<servlet-name>default</servlet-name>
   
<url-pattern>*.gif</url-pattern>
   
</servlet-mapping>

<servlet-mapping>
   
<servlet-name>default</servlet-name>
   
<url-pattern>*.jpg</url-pattern>
   
</servlet-mapping>

<servlet-mapping>
   
<servlet-name>default</servlet-name>
   
<url-pattern>*.js</url-pattern>
   
</servlet-mapping>

[/xml]