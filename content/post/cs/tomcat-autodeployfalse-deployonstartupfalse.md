---
title: 'tomcat autoDeploy="false"  deployOnStartup="false"'
author: "-"
date: 2018-09-19T04:48:43+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: tomcat-autodeployfalse-deployonstartupfalse
categories:
  - Web
tags:
  - tomcat
  - remix
  - AI-assisted
aliases:
  - /p12646/
  - /p13914/
---
## 'tomcat autoDeploy="false"  deployOnStartup="false"'
[https://stackoverflow.com/questions/26884335/tomcat-deploy-only-manager-on-startup](https://stackoverflow.com/questions/26884335/tomcat-deploy-only-manager-on-startup)

From the Apache 6 documentation: [https://tomcat.apache.org/tomcat-6.0-doc/config/context.html](https://tomcat.apache.org/tomcat-6.0-doc/config/context.html) in the Attributes section of Context, the documentation for the path attribute specifies:

This attribute must only be used when statically defining a Context in server.xml. In all other circumstances, the path will be inferred from the filenames used for either the .xml context file or the docBase.

Even when statically defining a Context in server.xml, this attribute must not be set unless either the docBase is not located under the Host's appBase or both deployOnStartup and autoDeploy are false. If this rule is not followed, double deployment is likely to result.

The same documentation exists in Tomcat 7, so I tried the following on Tomcat 7 and I managed to deploy only the manager application.

```xml
<Host appBase="webapps" autoDeploy="false" deployOnStartup="false" name="localhost" unpackWARs="true">
<Context docBase="manager" path="/manager" antiResourceLocking="false" privileged="true" />
</Host>
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Web | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
