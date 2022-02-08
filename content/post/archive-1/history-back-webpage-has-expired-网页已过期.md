---
title: history.back() webpage has expired. 网页已过期
author: "-"
date: 2013-01-23T06:51:49+00:00
url: /?p=5059
categories:
  - Web

tags:
  - reprint
---
## history.back() webpage has expired. 网页已过期
http://blog.sina.com.cn/s/blog_4b3c4bfa0100vz7h.html

最近开发的时候,碰到了这个问题,就是在回到上一页的时候,IE出现了webpage has expired; Firefox会出现一个alert,是否重新提交表单.

  page A 提交表单给page B, 然后去到page C.   从page C回到page B的时候, 这个问题就出现了. 
  
    于是去查了一些资料,并好好检查了一下我的代码.发现了几个问题,得到一些启发,在这里总结一下.
  

  1.http头中 cache-control的使用.


  指示了浏览器的缓存的使用情况, 我是把缓存都关掉了, 导致从page C返回page B的时候,需要重新submit 表单,这是这个问题的起因之一. 介绍一篇博文: http://czy4411741.blog.163.com/blog/static/3420312720102931720414/ 对cache-control的介绍还挺好懂的.


  改了cache-control以后可以达到后退的时候不重新submit表单,而是从缓存里拿,其他情况重新submit.具体的请看链接的博文,系统的学习一下.


  'Spring 的 SimpleFormController里面, 把cache-control设成了no-cache no-store.'

  2.Redirect After Post.


  我的page A的表单提交方式是post.这本身没有问题,但是浏览器有一个机制防止重复提交表单(只针对post),于是在浏览器端会条出来什么网页过期啊,重复提交警告之类的.找了一下,有一个Post/Redirect/Get的设计模式.


Page A 把表单Post给Page B, Page B拿到后Redirect用户去Pace C.在Page C显示结果.


  从Page C返回的话,会回到Page A.(浏览器不记录Page B,因为对于浏览器来说,他只做了一个Redirect操作).


  这样做的好处是不会再去到Page B, 就不会重复提交表单了. 对于严格禁止重复提交表单的操作, 使用这个设计模式是很好的选择.

  解决方案 (任选其一):


  1.修改cache-control设置, 并将Expires 设为-1. 看上面的总结一中的博文. jsp可以用response.setHeader("cache-control","private"); 配合response.setHeader("Expires","-1"); 其他语言类似.

  2.将page A里表单提交方式改为get. 如果表单数据不敏感的话,可以使用. 谁叫浏览器只针对post.

  3.遵循Post/Redirect/Get的设计模式, 请看上面的总结二. 我看的是英文的wiki百科, 同志们可以自己百度一下. 这个方法需要的改动比较大.
