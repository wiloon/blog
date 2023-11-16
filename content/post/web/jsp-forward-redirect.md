---
title: forward redirect
author: "-"
date: 2012-09-21T07:07:03+00:00
url: /?p=4153
categories:
  - Java
tags:
  - reprint
---
## forward redirect
## forward vs redirect
forward 是服务器内部重定向，程序收到请求后重新定向到另一个程序，而客户机并不知晓；

forward会将   request  state、bean、等信息带到下一个jsp页面；

使用getAttribute () 来取得前一个jsp所放的信息


redirect  是服务器收到请求后发送一个状态头给客户，客户将再次请求，就有两次网络通行的来往。

redirect 是送到客户端后再次request，因此上一个jsp的信息不被保留

效率:
  
Forward高,  Redirect低, 因为Redirect的流程是这样的,  request 1  sent to server,  server return back to client,  request 2 then sent to server. But Forward 仅在server side处理, 对client side 是透明的. 由于Redirect 有两次传输, 所以效率低.

范围:
  
由于对request.setAttribute() 来说, 它携带的对象生存范围只在request内, 所以Redirect方式会导致request携带的对象丢失.

[http://www.iteye.com/topic/3497](http://www.iteye.com/topic/3497)

[http://article2008.iteye.com/blog/173832](http://article2008.iteye.com/blog/173832)