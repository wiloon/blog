---
title: Conditional Get
author: "-"
date: 2011-10-23T01:30:12+00:00
url: /?p=1240
categories:
  - Network
tags:$
  - reprint
---
## Conditional Get
  
     HTTP条件Get
  
  
    HTTP条件Get是HTTP协议为了减少不必要的带宽浪费，提出的一种方案。详见http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html 
  


  
    HTTP条件Get使用的时机: 
  
  
    客户端之前已经访问过某网站，并打算再次访问该网站
  
  
    HTTP条件Get使用的方法: 
  
  
    客户端向服务器发送一个包询问是否在上一次访问网站的时间后是否更改了页面，如果服务器没有更新，显然不需要把整个网页传给客户端，客户端只要使用本地缓存即可，如果服务器对照客户端给出的时间已经更新了客户端请求的网页，则发送这个更新了的网页给用户。
  
  
    下面是具体的发送接受报文: 
  
  
    客户端发送查询请求: 
  
  
    ```java
 GET / HTTP/1.1
 Host: www.sina.com.cn:80
 If-Modified-Since:Thu, 4 Feb 2010 20:39:13 GMT
 Connection: Close
 ```
  
  
    下面是当没有更新时服务器的相应: 
  
  
    ```java
 HTTP/1.0 304 Not Modified
 Date: Thu, 04 Feb 2010 12:38:41 GMT
 Content-Type: text/html
 Expires: Thu, 04 Feb 2010 12:39:41 GMT
 Last-Modified: Thu, 04 Feb 2010 12:29:04 GMT
 Age: 28
 X-Cache: HIT from sy32-21.sina.com.cn
 Connection: close
 ```
  
  
    如果服务器网页已经更新就会发送把客户端的请求当作一个普通的Get请求发送相应报文
  
  
    ```java
 HTTP/1.0 200 OK
 Date: Thu, 04 Feb 2010 12:49:46 GMT
 Server: Apache
 Last-Modified: Thu, 04 Feb 2010 12:49:05 GMT
 Accept-Ranges: bytes
 X-Powered-By: mod_xlayout_jh/0.0.1vhs.markIII.remix
 Cache-Control: max-age=60
 Expires: Thu, 04 Feb 2010 12:50:46 GMT
 Vary: Accept-Encoding
 X-UA-Compatible: IE=EmulateIE7
 Content-Length: 452785
 Content-Type: text/html
 Age: 11
 X-Cache: HIT from sy32-27.sina.com.cn
 Connection: close
 /*.......网页内容....... */
 ```
  
