---
title: welcome-file-list
author: "-"
date: 2012-06-10T04:51:55+00:00
url: /?p=3479
categories:
  - Java
  - Web
tags:
  - Servlet

---
## welcome-file-list

  当用户在浏览器中输入的URL不包含某个servlet名或JSP页面时，welcome-file-list元素可指定显示的默认文件。


  
  
    <!ELEMENT welcome-file-list (welcome-file+)>
  
  
  
    <!ELEMENT welcome-file (#PCDATA)>
  
  
  
    举个例子说明，假设用户在浏览器的地址框中输入http://www.mycompany.com/appName/等地址。如果在Web应用的部署描述符中指定welcome-file-list元素，用户就会看到一个权限错误消息，或者是应用目录下的文件和目录列表。如果定义了welcome-file-list元素，用户就能看到由该元素指定的具体文件。
  
  
  
    welcome-file子元素用于指定默认文件的名称。welcome-file-list元素可以包含一个或多个welcome-file子元素。如果在第一个welcome-file元素中没有找到指定的文件，Web容器就会尝试显示第二个，以此类推。
  
  
  
    下面是一个包含welcome-file-list元素的部署描述符。该元素包含两个welcome-file元素: 第一个指定应用目录中的main.html文件，第二个定义jsp目录下的welcom.jsp文件，jsp目录也在应用目录下。
  
  
  
    <?xml version="1.0" encoding="ISO-8859-1"?>
  
  
  
    <!DOCTYPE web-app
  
  
  
    PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
  
  
  
    "http://java.sun.com/dtd/web-app_2_3.dtd">
  
  
  
    <web-app>
  
  
  
    <welcome-file-list>
  
  
  
    <welcome-file>main.html</welcome-file>
  
  
  
    <welcome-file>jsp/welcome.jsp</welcome-file>
  
  
  
    </welcome-file-list>
  
  
  
    </web-app>
  
  
  
    如果用户键入的URL不包含servlet名称、JSP页面或其他资源，则不会在应用目录中找到main.html文件，这时就会显示jsp目录下的welcome.jsp文件。
  
