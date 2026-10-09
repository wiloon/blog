---
title: "两个 Tomcat 同时运行时修改 Tomcat 端口"
author: "-"
date: 2012-05-13T10:49:12+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: tomcat-port
categories:
  - Java
  - Web
tags:
  - Tomcat
  - remix
  - AI-assisted
aliases:
  - /当装了两个tomcat后，修改tomcat端口/
---
## 当装了两个tomcat后，修改tomcat端口

http://zfsn.iteye.com/blog/669901 

修改Tomcat的端口号: 

在默认情况下，tomcat的端口是8080，如果出现8080端口号冲突，用如下方法可以修改Tomcat的端口号: 

首先:  在Tomcat的根 (安装) 目录下，有一个conf文件夹，双击进入conf文件夹，在里面找到Server.xml文件，打开该文件。

其次: 在文件中找到如下文本:

```xml
<Connector port="8080" protocol="HTTP/1.1" maxThreads="150" connectionTimeout="20000" redirectPort="8443" />
```

也有可能是这样的:

```xml
<Connector port="8080" maxThreads="150" minSpareThreads="25" maxSpareThreads="75" enableLookups="false" redirectPort="8443" acceptCount="100" debug="0" connectionTimeout="20000"
 disableUploadTimeout="true" />
```

等等；

最后: 将 `port="8080"` 改为其它的就可以了。如 `port="8081"` 等。保存 server.xml 文件，重新启动 Tomcat 服务器，Tomcat 就可以使用 8081 端口了。

注意，有的时候要使用两个 tomcat，那么就需要修改其中的一个的端口号才能使得两个同时工作。

修改了上面的以后，还要修改两处:

1. 将 `<Connector port="8009" enableLookups="false" redirectPort="8443" debug="0" protocol="AJP/1.3" />` 的 8009 改为其它的端口。
1. 继续将 `<Server port="8005" shutdown="SHUTDOWN" debug="0">` 的 8005 改为其它的端口。

经过以上 3 个修改，应该就可以了。

    8443
  

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `tomcat-port.md`；title 改为「两个 Tomcat 同时运行时修改 Tomcat 端口」；url 改为 `tomcat-port`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
