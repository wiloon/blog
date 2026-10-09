---
title: resource-ref
author: "-"
date: 2013-01-05T02:22:14+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: resource-ref
categories:
  - Java
  - Web
tags:
  - Servlet
  - remix
  - AI-assisted
aliases:
  - /p4171/
  - /p4630/
  - /p4632/
  - /p4972/
---
## resource-ref

resource-ref元素用于指定对外部资源的servlet引用的声明。

```xml
<!ELEMENT resource-ref (description?, res-ref-name,
    res-type, res-auth, res-sharing-scope?)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT res-ref-name (#PCDATA)>
<!ELEMENT res-type (#PCDATA)>
<!ELEMENT res-auth (#PCDATA)>
<!ELEMENT res-sharing-scope (#PCDATA)>
```

resource-ref子元素的描述如下:

● res-ref-name是资源工厂引用名的名称。该名称是一个与java:comp/env上下文相对应的JNDI名称,并且在整个Web应用中必须是惟一的。

● res-auth表明: servlet代码通过编程注册到资源管理器,或者是容器将代表servlet注册到资源管理器。该元素的值必须为Application或Container。

● res-sharing-scope表明: 是否可以共享通过给定资源管理器连接工厂引用获得的连接。该元素的值必须为Shareable(默认值)或Unshareable。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码 | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
