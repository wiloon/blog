---
title: HTTP Header ETag
author: "-"
date: 2015-09-07T06:09:17+00:00
url: /?p=8221
categories:
  - Inbox
tags:
  - reprint
---
## HTTP Header ETag

HTTP Header中的ETag
  
分类:  java web2013-09-02 20:14 1375人阅读 评论(0) 收藏 举报

目录[?](+)

原文参考百度百科: [http://baike.baidu.com/view/3039264.htm](http://baike.baidu.com/view/3039264.htm)

概念
  
Etag[1] 是URL的Entity Tag,用于标示URL对象是否改变,区分不同语言和Session等等。具体内部含义是使服务器控制的,就像Cookie那样。
  
HTTP协议规格说明定义ETag为"被请求变量的实体值"。另一种说法是,ETag是一个可以与Web资源关联的记号 (token) 。典型的Web资源可以一个Web页,但也可能是JSON或XML文档。服务器单独负责判断记号是什么及其含义,并在HTTP响应头中将其传送到客户端,以下是服务器端返回的格式: ETag:"50b1c1d4f775c61:df3"客户端的查询更新格式是这样的: If-None-Match : W / "50b1c1d4f775c61:df3"如果ETag没改变,则返回状态304然后不返回,这也和Last-Modified一样。测试Etag主要在断点下载时比较有用。
  
性能
  
聪明的服务器开发者会把ETags和GET请求的"If-None-Match"头一起使用,这样可利用客户端 (例如浏览器) 的缓存。因为服务器首先产生ETag,服务器可在稍后使用它来判断页面是否已经被修改。本质上,客户端通过将该记号传回服务器要求服务器验证其 (客户端) 缓存。
  
其过程如下:
  
客户端请求一个页面 (A) 。 服务器返回页面A,并在给A加上一个ETag。 客户端展现该页面,并将页面连同ETag一起缓存。 客户再次请求页面A,并将上次请求时服务器返回的ETag一起传递给服务器。 服务器检查该ETag,并判断出该页面自上次客户端请求之后还未被修改,直接返回响应304 (未修改——Not Modified) 和一个空的响应体。
  
优势
  
1. 有些URL是多语言的网页,相同的URL会返回不同的东西。还有不同的Session有不同的Cookie也就有不同的内容。这种情况下如果过 Proxy,Proxy就无法区分导致串门,只能简单的取消cache功能。Etag解决了这个问题,因为它能区分相同URL不同的对象。
  
2. 老的HTTP标准里有个Last-Modified+If-Modified-Since表明URL对象是否改变。Etag也具有这种功能,因为对象改变也造成Etag改变,并且它的控制更加准确。Etag有两种用法 If-Match/If-None-Match,就是如果服务器的对象和客户端的对象ID (不) 匹配才执行。这里的If-Match/If-None- Match都能一次提交多个Etag。If-Match可以在Etag未改变时断线重传。If-None-Match可以刷新对象 (在有新的Etag时返回) 。
  
3. Etag中有种Weak Tag,值为 W/"xxxxx"。他声明Tag是弱匹配的,只能做模糊匹配,在差异达到一定阀值时才起作用。
  
4. Etag对于cache CGI页面很有用。特别是论坛,论坛有办法为每个帖子页面生成唯一的Etag,在帖子未改变时,查看话题属性比较Etag就能避免刷新帖子,减少CGI操作和网络传输。比如论坛中看帖就返回Etag,减少论坛负担。
  
5. Etag在不同URL之间没有可比性,也就是不同URL相同Etag没有特别意义。
  
原理
  
请求流程
  
Etag由服务器端生成,客户端通过If-Match或者说If-None-Match这个条件判断请求来验证资源是否修改。常见的是使用If-None-Match.请求一个文件的流程可能如下:
  
====第一次请求===
  
1.客户端发起 HTTP GET 请求一个文件；
  
2.服务器处理请求,返回文件内容和一堆Header,当然包括Etag(例如"2e681a-6-5d044840")(假设服务器支持Etag生成和已经开启了Etag).状态码200
  
====第二次请求===
  
1.客户端发起 HTTP GET 请求一个文件,注意这个时候客户端同时发送一个If-None-Match头,这个头的内容就是第一次请求时服务器返回的Etag: 2e681a-6-5d044840
  
2.服务器判断发送过来的Etag和计算出来的Etag匹配,因此If-None-Match为False,不返回200,返回304,客户端继续使用本地缓存；
  
流程很简单,问题是,如果服务器又设置了Cache-Control:max-age和Expires呢,怎么办？
  
答案是同时使用,也就是说在完全匹配If-Modified-Since和If-None-Match即检查完修改时间和Etag之后,服务器才能返回304.(不要陷入到底使用谁的问题怪圈)
  
作用
  
Etag 主要为了解决 Last-Modified 无法解决的一些问题。
  
1. 一些文件也许会周期性的更改,但是他的内容并不改变(仅仅改变的修改时间),这个时候我们并不希望客户端认为这个文件被修改了,而重新GET;
  
2. 某些文件修改非常频繁,比如在秒以下的时间内进行修改,(比方说1s内修改了N次),If-Modified-Since能检查到的粒度是s级的,这种修改无法判断(或者说UNIX记录MTIME只能精确到秒)
  
3. 某些服务器不能精确的得到文件的最后修改时间；
  
为此,HTTP/1.1引入了 Etag(Entity Tags).Etag仅仅是一个和文件相关的标记,可以是一个版本标记,比如说v1.0.0或者说"2e681a-6-5d044840"这么一串看起来很神秘的编码。但是HTTP/1.1标准并没有规定Etag的内容是什么或者说要怎么实现,唯一规定的是Etag需要放在""内。

Apache
  
Apache[2]首先判断是不是弱Etag,这个留在下面讲。如果不是,进入第二种情况:
  
强Etag根据配置文件中的配置来设置Etag值,默认的Apache的FileEtag设置为:
  
FileEtag INode Mtime Size
  
也就是根据这三个属性来生成Etag值,他们之间通过一些算法来实现,并输出成hex的格式,相邻属性之间用-分隔,比如:
  
Etag"2e681a-6-5d044840"
  
这里面的三个段,分别代表了INode,MTime,Size根据算法算出的值的Hex格式,(如果在这里看到了非Hex里面的字符(也就是0-f),那你可能看见神了:))
  
当然,可以改变Apache的FileEtag设置,比如设置成FileEtagSize,那么得到的Etag可能为:
  
Etag"6"
  
总之,设置了几个段,Etag值就有几个段。(不要误以为Etag就是固定的3段式)
  
说明: 这里说的都是Apache2.2里面的Etag实现,因为HTTP/1.1并没有规定Etag必须是什么样的实现或者格式,因此,也可以修改或者完全编写自己的算法得到Etag,比如"2e681a65d044840",客户端会记住并缓存下这个Etag(Windows里面保存在哪里,下次访问的时候直接拿这个值去和服务器生成的Etag对比。
  
注意: 不管怎么样的算法,在服务器端都要进行计算,计算就有开销,会带来性能损失。因此为了榨干这一点点性能,不少网站完全把Etag禁用了(比如Yahoo!),这其实不符合HTTP/1.1的规定,因为HTTP/1.1总是鼓励服务器尽可能的开启Etag。
