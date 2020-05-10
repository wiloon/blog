---
title: 'Invalid HTTP server response [411] – Length Required'
author: wiloon
type: post
date: 2016-05-24T12:14:31+00:00
url: /?p=9015
categories:
  - Uncategorized

---
http://www.coderanch.com/t/625696/Web-Services/java/Invalid-HTTP-server-response-Length

&nbsp;

As William asked, please share how you are setting content length in SOAP header.
  
I searched online for error and found that there can be one more reason for this failure.
  
Reason &#8211; The remote WSEndpoint did not like the HTTP Chunking feature activated. Try disabling this feature for WS client.

&nbsp;

netty

<pre>HttpPostRequestEncoder bodyRequestEncoder = new HttpPostRequestEncoder(factory, request, false);</pre>