---
title: 'Invalid HTTP server response [411] – Length Required'
author: "-"
date: 2016-05-24T12:14:31+00:00
url: /?p=9015
categories:
  - Inbox
tags:
  - reprint
---
## 'Invalid HTTP server response [411] – Length Required'

[http://www.coderanch.com/t/625696/Web-Services/java/Invalid-HTTP-server-response-Length](http://www.coderanch.com/t/625696/Web-Services/java/Invalid-HTTP-server-response-Length)

As William asked, please share how you are setting content length in SOAP header.
  
I searched online for error and found that there can be one more reason for this failure.
  
Reason - The remote WSEndpoint did not like the HTTP Chunking feature activated. Try disabling this feature for WS client.

netty

HttpPostRequestEncoder bodyRequestEncoder = new HttpPostRequestEncoder(factory, request, false);
