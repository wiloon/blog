---
title: httpcomponent, httpclient proxy setting
author: "-"
date: 2015-01-16T02:53:10+00:00
url: /?p=7244
categories:
  - Uncategorized

tags:
  - reprint
---
## httpcomponent, httpclient proxy setting
http://www.jianshu.com/p/f38a62efaa96

```java
  
HttpHost proxy = new HttpHost("localhost",8888);
  
CloseableHttpClient httpclient = HttpClients.custom()
  
.setDefaultRequestConfig(RequestConfig.custom()
  
.setProxy(proxy).build()).build();
  
```