---
title: ﻿Web.config
author: "-"
date: 2012-11-14T02:38:33+00:00
url: /?p=4661
categories:
  - Inbox
tags:
  - reprint
---
## ﻿Web.config
Web.config文件
  
Web.config 文件是一个xml文本文件,它用来储存 asp.NET Web 应用程序的配置信息 (如最常用的设置asp.NET Web 应用程序的身份验证方式) ,它可以出现在应用程序的每一个目录中。当你通过.NET新建一个Web应用程序后,默认情况下会在根目录自动创建一个默认的Web.config文件,包括默认的配置设置,所有的子目录都继承它的配置设置。如果你想修改子目录的配置设置,你可以在该子目录下新建一个Web.config文件。它可以提供除从父目录继承的配置信息以外的配置信息,也可以重写或修改父目录中定义的设置。
  
(一).Web.Config是以xml文件规范存储,配置文件分为以下格式
  
1.配置节处理程序声明
  
特点: 位于配置文件的顶部,包含在<configSections>标志中。
  
2.特定应用程序配置
  
特点: 位于中。可以定义应用程序的全局常量设置等信息.
  
3.配置节设置
  
特点: 位于<system.Web>节中,控制asp.net运行时的行为.
  
4.配置节组
  
特点: 用<sectionGroup>标记,可以自定义分组,可以放到<configSections>内部或其它<sectionGroup>标记的内部.
  
(二).配置节的每一节
  
1.<configuration>节根元素,其它节都是在它的内部.
  
2.节此节用于定义应用程序设置项。对一些不确定设置,还可以让用户根据自己实际情况自己设置