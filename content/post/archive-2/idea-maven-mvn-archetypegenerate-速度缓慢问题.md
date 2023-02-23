---
title: idea maven mvn archetype,generate 速度缓慢问题
author: "-"
date: 2017-02-22T06:39:15+00:00
url: /?p=9856
categories:
  - Inbox
tags:
  - reprint
---
## idea maven mvn archetype,generate 速度缓慢问题

<https://my.oschina.net/u/225373/blog/468035>
  
maven生成项目速度慢的令人发指,都在Generating project in Batch mode等待,Idea状态显示栏还在不行runing,并没有卡死。查看debug信息发现,是maven获取archetype-catalog.xml导致。 (用浏览器打开<http://repo1.maven.org/maven2/archetype-catalog.xml>,需要等待很长时间才能获取到。)

解决方法:
  
加上-DarchetypeCatalog=internal 运行参数,archetype-catalog.xml本地获取。

对于intellij idea可以再Runner加上参数。

curl <http://repo1.maven.org/maven2/archetype-catalog.xml> > .m2/archetype-catalog.xml
  
-DarchetypeCatalog=local
