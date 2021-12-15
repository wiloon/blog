---
title: filter-mapping
author: "-"
date: 2012-11-21T13:16:35+00:00
url: /?p=4744
categories:
  - Java
  - Web
tags:
  - Servlet

---
## filter-mapping
filter-mapping元素用来声明Web应用中的过滤器映射。过滤器可被映射到一个servlet或一个URL模式。将过滤器映射到一个servlet中会造成过滤器作用于servlet上。将过滤器映射到一个URL模式中则可以将过滤器应用于任何资源，只要该资源的URL与URL模式匹配。过滤是按照部署描述符的filter-mapping元素出现的顺序执行的。

<!ELEMENT filter-mapping (filter-name,(url-pattern | servlet-name))>


<!ELEMENT filter-name (#PCDATA)>


<!ELEMENT url-pattern (#PCDATA)>


<!ELEMENT servlet-name (#PCDATA)>


filter-name值必须对应filter元素中声明的其中一个过滤器名称。下面是一个含有filter-mapping元素的部署描述符: 


<?xml version="1.0" encoding="ISO-8859-1">


<!DOCTYPE web-app


PUBLIC "-//Sun Microsystems,Inc.//DTD Web Application 2.3//EN"


<web-app>


<filter>


<filter-name>Encryption Filter</filter-name>


<filter-class>com.brainysoftware.EncryptionFilter</filter-class>


</filter>


<filter-mapping>


<filter-name>Encryption Filter</filter-name>


<servlet-name>EncryptionFilteredServlet</servlet-name>


</filter-mapping>


</web-app>

  < filter> 
  
  
  
    filter元素用来声明filter的相关设定.filter元素除了下面介绍的的子元素之外，还包括< servlet>；介绍过的< icon>,< display-name>,< description>,< init-param>；，其用途一样.
  
  
  
    < filter-name>Filter的名称< /filter-name>
  
  
  
    定义Filter的名称.
  
  
  
    < filter-class>Filter的类名称< /filter-class>
  
  
  
    定义Filter的类名称.例如: com.foo.hello
  
  
  
    范例: 
  
  
  
    < filter> < filter-name>setCharacterEncoding< /filter-name> < filter-class>coreservlet.SetCharacterEncodingFilter< /filter-class> < init-param> < param-name>encoding< /param-name> < param-value>GB2312< /param-value> < /init-param> < /filter> < filter-mapping>
  
  
  
    filter-mapping 元素的两个主要子元素filter-name和url-pattern.用来定义Filter所对应的URL.
  
  
  
    < filter-name>Filter的名称< /filter-name>
  
  
  
    定义Filter的名称.
  
  
  
    < url-pattern>URL< /url-pattern>
  
  
  
    Filter所对应的RUL.例如: < url-pattern>/Filter/Hello< /url-pattern>
  
  
  
    < servlet-name>Servlet的名称< servlet-name>
  
  
  
    定义servlet的名称.
  
