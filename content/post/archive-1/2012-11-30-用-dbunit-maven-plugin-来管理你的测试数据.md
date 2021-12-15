---
title: 用 dbunit-maven-plugin 来管理你的测试数据
author: "-"
date: 2012-11-30T06:19:44+00:00
url: /?p=4807
categories:
  - Java
tags:
  - Maven

---
## 用 dbunit-maven-plugin 来管理你的测试数据
http://newwhx2011.iteye.com/blog/1089559

单元测试有人写过,也有人没做过,数据库的 dbunit 的用的人应该更少了,它可以用来给你做测试准备数据。一般我们做测试会在一个测试数据库中不停的测,自然会累积许多垃圾数据,给单元测试会造成不便,功能测试倒无太紧要。如果我们想在单元测试的时候有一份干净的数据,有个做法是搞个备用的数据库,测试前导到测试库的,或用某些数据库的导入导出功能。

这里我们来看 dbunit 怎么实现准备测试数据的,它可以用来导出数据库数据到数据文件中,从数据文件中导入干净的数据到数据库中,比较数据库与数据文件、或增量的插入记录等等。

dbunit 最初为 ant 提供了 antask,当然可以编程使用,如今 maven 大行其道,所以也就有了 maven 的 dbunit 插件,相似功能的插件有两个: 

1. dbunit-maven-plugin
  
2. maven-dbunit-plugin

就是 maven 和 dbunit 倒了一下,别晕了,第二个似乎提供了更多的 goal,但运行 mvn dbunit:xxxx,指向的是第一个 dbunit-maven-plugin,看来第一个要正统些。本文也就介绍下dbunit-maven-plugin 的用法,测试数据库是 MySQL。