---
title: URI, URL, URN
author: "-"
date: 2011-09-13T10:32:21+00:00
url: /?p=768
categories:
  - Development
tags:
  - reprint
---
## URI, URL, URN

[http://www.ibm.com/developerworks/cn/xml/x-urlni.html](http://www.ibm.com/developerworks/cn/xml/x-urlni.html)
  
-
  
[http://www.cisco.com/en/US/partners/index.html](http://www.cisco.com/en/US/partners/index.html) —— 是一个 URI
  
方案名 (http)
  
域名 (www.cisco.com)
  
路径 (/en/US/partners/index.html)
  
URI 按照 UNIX® 的惯例采用了正斜杠 (a/b/c)，因为在 20 世纪 80 年代后期设计 URI 的时候, 在 Internet 上， UNIX 文化比 PC 文化更流行。
  
URI 可以进一步分为定位器、名称，或者二者兼具。术语"Uniform Resource Locator" (URL) 涉及的是 URI 的子集，除识别资源外，它还通过描述其最初访问机制 (比如它的网络"位置") 来提供定位资源的方法。 术语"Uniform Resource Name" (URN) 在历史上曾用于引用"urn"方案 [RFC2141] 下的 URI，这个 URI 需要是全球惟一的，并且在资源不存在或不再可用时依然保持不变，对于其他任何拥有名称的一些属性的 URI，都需要使用这样的 URI。
  
对于单独的方案，没有必要将其分为仅仅是一个 "名称"或者是一个"定位器"。 来自任意特定方案的 URI 实例可能有名称或定位器的特征，或两者兼而有之， 这通常取决于标识符分配中的持久性和命名机构对其关注程度， 而不取决于其他方案的质量。未来的规范和相关的文档应当使用通用术语"URI"，而不是使用有更多限制的条目"URL"和"URN" [RFC3305]。
