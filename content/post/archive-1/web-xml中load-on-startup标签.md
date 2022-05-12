---
title: web.xml中load-on-startup标签
author: "-"
date: 2012-10-31T09:02:06+00:00
url: /?p=4604
categories:
  - Java
  - Web
tags:$
  - reprint
---
## web.xml中load-on-startup标签
在servlet的配置当中，<load-on-startup>5</load-on-startup>的含义是: 

标记容器是否在启动的时候就加载这个servlet。

当值为0或者大于0时，表示容器在应用启动时就加载这个servlet；

当是一个负数时或者没有指定时，则指示容器在该servlet被选择时才加载。

正数的值越小，启动该servlet的优先级越高。
  
Servlet specification:

The load-on-startup element indicates that this servlet should be loaded (instantiated and have its init() called) on the startup of the web application. The optional contents of these element must be an integer indicating the order in which the servlet should be loaded. If the value is a negative integer, or the element is not present, the container is free to load the servlet whenever it chooses. If the value is a positive integer or 0, the container must load and initialize the servlet as the application is deployed. The container must guarantee that servlets marked with lower integers are loaded before servlets marked with higher integers. The container may choose the order of loading of servlets with the same load-on-start-up value.

example:

```xml

<servlet>

<servlet-name>initservlet</servlet-name>

<servlet-class>com.bb.eoa.util.initServlet</servlet-class>

<init-param>

<param-name>log4j-init-file</param-name>

<param-value>config/log.properties</param-value>

</init-param>

<load-on-startup>2</load-on-startup>

</servlet>

```