---
title: http header
author: w1100n
type: post
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6798
categories:
  - Uncategorized
tags:
  - Network

---
### Connection
Connection 头（header） 决定当前的事务完成后，是否会关闭网络连接。如果该值是“keep-alive"，网络连接就是持久的，不会关闭，使得对同一个服务器的请求可以继续在该连接上完成。
### Content-Length
消息主体的大小

### Content-Transfer-Encoding
从它的命名就可以看出，这个head域是用来描述内容在传输过程中的编码格式。不同于Content-Type，这个域不是必须的。不过，仅仅定义一种Content-Transfer-Encoding也是不可以的。在有效地传输巨大的二进制数据和便于阅读的编码数据之间要有一个折中。所以，至少要有两种编码格式：易读的，和稠密的（高压缩率的）。Content-Transfer-Encoding就是为这个目的设计的。Content-Transfer-Encoding支持以下数据格式：BASE64, QUOTED-PRINTABLE, 8BIT, 7BIT, BINARY, X-TOKEN。这些值是大小写不敏感的。7BIT是默认值，当不设置Content-Transfer-Encoding的时候，默认就是7BIT。7BIT的含义是所有的数据以ASC-II格式的格式编码，8BIT则可能包含非ASCII字符。BINARY可能不止包含非ASCII字符，还可能不是一个短行（超过1000字符）。



### http header refer
http://baike.baidu.com/link?url=OfDRRcbOxy7ZiemI_UxhgunI1ZvvTZ3MDix3JGK-6bdZxHScOUykrcWDqGkbNy7KOr4tz5t8oWtymFMDbA2fr_

简而言之，HTTP Referer是header的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器我是从哪个页面链接过来的，服务器籍此可以获得一些信息用于处理。比如从我主页上链接到一个朋友那里，他的服务器就能够从HTTP Referer中统计出每天有多少用户点击我主页上的链接访问他的网站。
  
Referer的正确英语拼法是referrer。由于早期HTTP规范的拼写错误，为了保持向后兼容就将错就错了。其它网络技术的规范企图修正此问题，使用正确拼法，所以目前拼法不统一。
  
Request.ServerVariables("HTTP_REFERER")的用法(防外连接)


---

版权声明：本文为CSDN博主「hunter800421」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/foolish0421/article/details/73302336



https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Connection