---
title: "将应用部署到 Tomcat 根目录的方法"
author: "-"
date: 2013-01-16T04:44:06+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: tomcat-root-deploy
categories:
  - Java
  - Web
tags:
  - Tomcat
  - remix
  - AI-assisted
aliases:
  - /将应用部署到tomcat根目录的方法/
---
## 将应用部署到Tomcat根目录的方法

[http://rongjih.blog.163.com/blog/static/335744612011426103345778/](http://rongjih.blog.163.com/blog/static/335744612011426103345778/)

将应用部署到Tomcat根目录的目的是可以通过 `http://[ip]:[port]` 直接访问应用，而不是使用 `http://[ip]:[port]/[appName]` 上下文路径进行访问。

方法一:  (最简单直接的方法)

删除原 webapps/ROOT 目录下的所有文件,将应用下的所有文件和文件夹复制到ROOT文件夹下。

方法二:

删除原 webapps/ROOT 目录下的所有文件,修改文件"conf/server.xml",在Host节点下增加如下Context的内容配置:

```xml
<Host name="localhost"  appBase="webapps" unpackWARs="true" autoDeploy="true"
    xmlValidation="false" xmlNamespaceAware="false">
    ......
    <Context path="" docBase="C:/apache-tomcat-6.0.32/myapps/bc.war"></Context>
</Host>
```

**注意:**

1) path 的值设置为空；

2) 应用不要放到tomcat的webapps目录下(如上述配置是放到自定义的文件夹myapps内的),否则访问时路径很有问题；

3) docBase指定到绝对路径。

如此设置后重启tomcat,如果docBase指向的是war文件,会自动将war解压到 webapps/ROOT 目录；如果docBase指向的是应用已解压好的目录,如 docBase="C:/apache-tomcat-6.0.32/myapps/bc",tomcat不会生成webapps/ROOT目录 (这种情况下之前可以不用删除webapps/ROOT目录,但webapps/ROOT目录内的内容是无法访问的) ,访问时将直接使用docBase指定的目录。

方法三:

与方法二类似,但不是修改全局配置文件"conf/server.xml",而是在"conf/Catalina/localhost"目录下增加新的文件"ROOT.xml" (注意大小写哦) ,文件内容如下:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Context path="" docBase="C:/apache-tomcat-6.0.32/myapps/bc.war"></Context>
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `tomcat-root-deploy.md`；title 改为「将应用部署到 Tomcat 根目录的方法」；url 改为 `tomcat-root-deploy`；旧 url 加入 aliases | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
