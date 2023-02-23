---
title: nuxus
author: "-"
date: 2011-10-19T07:10:57+00:00
url: /?p=1192
categories:
  - Inbox
tags:
  - Nexus

---
## nuxus

Nexus 是Maven仓库管理器，如果你使用Maven，你可以从Maven中央仓库 下载所需要的构件 (artifact) ，但这通常不是一个好的做法，你应该在本地架设一个Maven仓库服务器，在代理远程仓库的同时维护本地仓库，以节省带宽和时间，Nexus就可以满足这样的需要。此外，他还提供了强大的仓库管理功能，构件搜索功能，它基于REST，友好的UI是一个extjs的REST客户端，它占用较少的内存，基于简单文件系统而非数据库。这些优点使其日趋成为最流行的Maven仓库管理器。

## 下载和安装

你可以从 <http://nexus.sonatype.org/downloads/> 下载最新版本的Nexus，笔者使用的是1.9.2.3版本。

Nexus提供了两种安装方式，一种是内嵌Jetty的bundle，只要你有JRE就能直接运行。第二种方式是WAR，你只须简单的将其发布到web容器中即可使用。

WAR方式安装

你需要有一个能运行的web容器，这里以Tomcat为例，加入Tomcat的安装目录位于_D:programapache-tomcat-7.0.21_ ，首先我们将下载的_nexus-webapp-1.9.2.3.war_ 重命名为_nexus.war_ ，然后复制到__D:programapache-tomcat-7.0.21_webappsnexus.war_ ，然后运行**startup.bat**。访问<http://127.0.0.1:8080/nexus> .
