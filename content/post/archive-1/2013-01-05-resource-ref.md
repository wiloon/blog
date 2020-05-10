---
title: resource-ref
author: wiloon
type: post
date: 2013-01-05T02:22:14+00:00
url: /?p=4972
categories:
  - Java
  - Web
tags:
  - Servlet

---
resource-ref元素用于指定对外部资源的servlet引用的声明。

<div>
</div>

<!ELEMENT resource-ref (description?, res-ref-name,

<div>
</div>

res-type, res-auth, res-sharing-scope?)>

<div>
</div>

<!ELEMENT description (#PCDATA)>

<div>
</div>

<!ELEMENT res-ref-name (#PCDATA)>

<div>
</div>

<!ELEMENT res-type (#PCDATA)>

<div>
</div>

<!ELEMENT res-auth (#PCDATA)>

<div>
</div>

<!ELEMENT res-sharing-scope (#PCDATA)>

<div>
</div>

resource-ref子元素的描述如下：

<div>
</div>

● res-ref-name是资源工厂引用名的名称。该名称是一个与java:comp/env上下文相对应的JNDI名称，并且在整个Web应用中必须是惟一的。

<div>
</div>

● res-auth表明：servlet代码通过<a href="http://baike.baidu.com/view/3281.htm" target="_blank">编程</a>注册到资源管理器，或者是容器将代表servlet注册到资源管理器。该元素的值必须为Application或Container。

<div>
</div>

● res-sharing-scope表明：是否可以共享通过给定资源管理器连接工厂引用获得的连接。该元素的值必须为Shareable(默认值)或Unshareable。