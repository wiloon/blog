---
title: Conditional Get
author: wiloon
type: post
date: 2011-10-23T01:30:12+00:00
url: /?p=1240
views:
  - 5
bot_views:
  - 12
categories:
  - Network

---
<div>
  <p>
     <span class="Apple-style-span" style="font-size: 15px; font-weight: bold;">HTTP条件Get</span>
  </p>
  
  <h3>
    <span class="Apple-style-span" style="font-size: 13px; font-weight: normal;">HTTP条件Get是HTTP协议为了减少不必要的带宽浪费，提出的一种方案。详见http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html</span><span class="Apple-style-span" style="font-size: 13px; font-weight: normal;"> </span>
  </h3>
</div>

<div id="article_content">
  <p>
    HTTP条件Get使用的时机：
  </p>
  
  <p>
    客户端之前已经访问过某网站，并打算再次访问该网站
  </p>
  
  <p>
    HTTP条件Get使用的方法：
  </p>
  
  <p>
    客户端向服务器发送一个包询问是否在上一次访问网站的时间后是否更改了页面，如果服务器没有更新，显然不需要把整个网页传给客户端，客户端只要使用本地缓存即可，如果服务器对照客户端给出的时间已经更新了客户端请求的网页，则发送这个更新了的网页给用户。
  </p>
  
  <p>
    下面是具体的发送接受报文：
  </p>
  
  <p>
    客户端发送查询请求：
  </p>
  
  <p>
    [java]<br /> GET / HTTP/1.1<br /> Host: www.sina.com.cn:80<br /> If-Modified-Since:Thu, 4 Feb 2010 20:39:13 GMT<br /> Connection: Close<br /> [/java]
  </p>
  
  <div>
    下面是当没有更新时服务器的相应：
  </div>
  
  <p>
    [java]<br /> HTTP/1.0 304 Not Modified<br /> Date: Thu, 04 Feb 2010 12:38:41 GMT<br /> Content-Type: text/html<br /> Expires: Thu, 04 Feb 2010 12:39:41 GMT<br /> Last-Modified: Thu, 04 Feb 2010 12:29:04 GMT<br /> Age: 28<br /> X-Cache: HIT from sy32-21.sina.com.cn<br /> Connection: close<br /> [/java]
  </p>
  
  <div>
    如果服务器网页已经更新就会发送把客户端的请求当作一个普通的Get请求发送相应报文
  </div>
  
  <p>
    [java]<br /> HTTP/1.0 200 OK<br /> Date: Thu, 04 Feb 2010 12:49:46 GMT<br /> Server: Apache<br /> Last-Modified: Thu, 04 Feb 2010 12:49:05 GMT<br /> Accept-Ranges: bytes<br /> X-Powered-By: mod_xlayout_jh/0.0.1vhs.markIII.remix<br /> Cache-Control: max-age=60<br /> Expires: Thu, 04 Feb 2010 12:50:46 GMT<br /> Vary: Accept-Encoding<br /> X-UA-Compatible: IE=EmulateIE7<br /> Content-Length: 452785<br /> Content-Type: text/html<br /> Age: 11<br /> X-Cache: HIT from sy32-27.sina.com.cn<br /> Connection: close<br /> /*&#8230;&#8230;.网页内容&#8230;&#8230;. */<br /> [/java]
  </p>
</div>