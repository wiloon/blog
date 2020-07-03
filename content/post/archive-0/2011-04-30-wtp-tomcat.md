---
title: 'Eclipse WTP & Tomcat'
author: wiloon
type: post
date: 2011-04-30T06:22:49+00:00
url: /?p=130
bot_views:
  - 7
categories:
  - Eclipse
  - Web

---
download "Eclipse IDE for Java EE Developers" include WTP.
  
download tomcat

open eclipse
  
goto window> preference >server> runtime environment
  
add tomcat

goto "project explorer" or "navigator"
  
new > other > server> server

project facets , convert project to web project.

project properties > deployment assembly;  include webapp folder

项目转成web 项目之后 没有deployment assembly 的问题

在.project 里面添加

[xml]

<nature>org.eclipse.wst.common.modulecore.ModuleCoreNature</nature>

[/xml]

然后回到eclipse里刷新项目。

http://stackoverflow.com/questions/1581683/how-do-i-change-in-an-eclipse-web-project-the-webcontent-folder-to-something-dif

http://elf8848.iteye.com/blog/1684935

http://blog.sina.com.cn/s/blog_8ced01900101ed7b.html