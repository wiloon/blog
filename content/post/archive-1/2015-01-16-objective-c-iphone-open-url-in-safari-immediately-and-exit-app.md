---
title: httpcomponent, httpclient proxy setting
author: wiloon
type: post
date: 2015-01-16T02:53:10+00:00
url: /?p=7244
categories:
  - Uncategorized

---
http://www.jianshu.com/p/f38a62efaa96

[code lang=java]
  
HttpHost proxy = new HttpHost("localhost",8888);
  
CloseableHttpClient httpclient = HttpClients.custom()
  
.setDefaultRequestConfig(RequestConfig.custom()
  
.setProxy(proxy).build()).build();
  
```