---
title: resource-ref
author: "-"
date: 2013-01-05T02:22:14+00:00
url: /?p=4972
categories:
  - Java
  - Web
tags:
  - Servlet

---
## resource-ref

resource-ref元素用于指定对外部资源的servlet引用的声明。

<!ELEMENT resource-ref (description?, res-ref-name,

res-type, res-auth, res-sharing-scope?)>

<!ELEMENT description (#PCDATA)>

<!ELEMENT res-ref-name (#PCDATA)>

<!ELEMENT res-type (#PCDATA)>

<!ELEMENT res-auth (#PCDATA)>

<!ELEMENT res-sharing-scope (#PCDATA)>

resource-ref子元素的描述如下:

● res-ref-name是资源工厂引用名的名称。该名称是一个与java:comp/env上下文相对应的JNDI名称,并且在整个Web应用中必须是惟一的。

● res-auth表明: servlet代码通过编程注册到资源管理器,或者是容器将代表servlet注册到资源管理器。该元素的值必须为Application或Container。

● res-sharing-scope表明: 是否可以共享通过给定资源管理器连接工厂引用获得的连接。该元素的值必须为Shareable(默认值)或Unshareable。
