---
title: http
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: http
categories:
  - Network
tags:
  - Network

---
## http
HTTP协议 (RFC2616）采用了请求/响应模型。客户端向服务器发送一个请求，请求头包含请求的方法、URI、协议版本、以及包含请求修饰符、客户信息和内容的类似于MIME的消息结构。服务器以一个状态行作为响应，相应的内容包括消息协议的版本，成功或者错误编码加上包含服务器信息、实体元信息以 及可能的实体内容。

通常HTTP消息由一个起始行，一个或者多个头域，一个只是头域结束的空行和可选的消息体组成。
HTTP的头域包括通用头，请求头，响应头和实体头四个部分。每个头域由一个域名，冒号 (:）和域值三部分组成。域名是大小写无关的，域值前可以添加任何数量的空格符，头域可以被扩展为多行，在每行开始处，使用至少一个空格或制表符。

请求消息和响应消息都可以包含实体信息，实体信息一般由实体头域和实体组成。实体头域包含关于实体的原信息，实体头包括Allow、Content- Base、Content-Encoding、Content-Language、 Content-Length、Content-Location、Content-MD5、Content-Range、Content-Type、 Etag、Expires、Last-Modified、extension-header。

Content-Type是返回消息中非常重要的内容，表示后面的文档属于什么MIME类型。Content-Type: [type]/[subtype]; parameter。例如最常见的就是text/html，它的意思是说返回的内容是文本类型，这个文本又是HTML格式的。原则上浏览器会根据Content-Type来决定如何显示返回的消息体内容。

2.Content-type与Accept
 (1）Accept属于请求头， Content-Type属于实体头。
Http报头分为通用报头，请求报头，响应报头和实体报头。
请求方的http报头结构：通用报头|请求报头|实体报头
响应方的http报头结构：通用报头|响应报头|实体报头

 (2）Accept代表发送端 (客户端）希望接受的数据类型。
比如：Accept：text/xml;
代表客户端希望接受的数据类型是xml类型

Content-Type代表发送端 (客户端|服务器）发送的实体数据的数据类型。
比如：Content-Type：text/html;
代表发送端发送的数据格式是html。

二者合起来，
Accept:text/xml；
Content-Type:text/html
即代表希望接受的数据类型是xml格式，本次请求发送的数据的数据格式是html。



### Connection
Connection 头 (header)  决定当前的事务完成后,是否会关闭网络连接。如果该值是 "keep-alive", 网络连接就是持久的,不会关闭,使得对同一个服务器的请求可以继续在该连接上完成。
### Content-Length
消息主体的大小

### Content-Transfer-Encoding
从它的命名就可以看出,这个 head 域是用来描述内容在传输过程中的编码格式。不同于 Content-Type, 这个域不是必须的。不过,仅仅定义一种Content-Transfer-Encoding 也是不可以的。在有效地传输巨大的二进制数据和便于阅读的编码数据之间要有一个折中。所以,至少要有两种编码格式: 易读的, 和稠密的 (高压缩率的) 。Content-Transfer-Encoding 就是为这个目的设计的。Content-Transfer-Encoding 支持以下数据格式: BASE64, QUOTED-PRINTABLE, 8BIT, 7BIT, BINARY, X-TOKEN。这些值是大小写不敏感的。7BIT是默认值,当不设置 Content-Transfer-Encoding 的时候,默认就是7BIT。7BIT 的含义是所有的数据以 ASC-II 格式的格式编码, 8BIT则可能包含非ASCII字符。BINARY 可能不止包含非ASCII字符, 还可能不是一个短行 (超过1000字符) 。

### http header refer
http://baike.baidu.com/link?url=OfDRRcbOxy7ZiemI_UxhgunI1ZvvTZ3MDix3JGK-6bdZxHScOUykrcWDqGkbNy7KOr4tz5t8oWtymFMDbA2fr_

简而言之,HTTP Referer是header的一部分,当浏览器向web服务器发送请求的时候,一般会带上Referer,告诉服务器我是从哪个页面链接过来的,服务器籍此可以获得一些信息用于处理。比如从我主页上链接到一个朋友那里,他的服务器就能够从HTTP Referer中统计出每天有多少用户点击我主页上的链接访问他的网站。
  
Referer的正确英语拼法是referrer。由于早期HTTP规范的拼写错误,为了保持向后兼容就将错就错了。其它网络技术的规范企图修正此问题,使用正确拼法,所以目前拼法不统一。
  
Request.ServerVariables("HTTP_REFERER")的用法(防外连接)


---

版权声明: 本文为CSDN博主「hunter800421」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/foolish0421/article/details/73302336



https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Connection

>https://segmentfault.com/a/1190000013056786

