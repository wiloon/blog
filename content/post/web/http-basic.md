---
title: HTTP basic
author: "-"
date: 2011-10-23T04:26:37+00:00
url: /?p=1255
categories:
  - inbox
tags:
  - reprint
---
## HTTP basic

### get/post

1．HTTP请求格式:

在HTTP请求中，第一行必须是一个请求行 (request line) ，用来说明请求类型、要访问的资源以及使用的HTTP版本。紧接着是一个首部 (header) 小节，用来说明服务器要使用的附加信息。在首部之后是一个空行，再此之后可以添加任意的其他数据[称之为主体 (body) ]。

### 重定向
Redirect
重定向是指当浏览器请求一个URL时，服务器返回一个重定向指令，告诉浏览器地址已经变了，麻烦使用新的URL再重新发送新请求。

例如，我们已经编写了一个能处理/hello的HelloServlet，如果收到的路径为/hi，希望能重定向到/hello
如果浏览器发送GET /hi请求，RedirectServlet将处理此请求。由于RedirectServlet在内部又发送了重定向响应，因此，浏览器会收到如下响应: 

HTTP/1.1 302 Found
Location: /hello
当浏览器收到302响应后，它会立刻根据Location的指示发送一个新的GET /hello请求，这个过程就是重定向: 

┌───────┐   GET /hi     ┌───────────────┐
│Browser│ ────────────> │RedirectServlet│
│       │ <──────────── │               │
└───────┘   302         └───────────────┘


┌───────┐  GET /hello   ┌───────────────┐
│Browser│ ────────────> │ HelloServlet  │
│       │ <──────────── │               │
└───────┘   200 <html>  └───────────────┘
观察Chrome浏览器的网络请求，可以看到两次HTTP请求: 
并且浏览器的地址栏路径自动更新为/hello。

重定向有两种: 一种是302响应，称为临时重定向，一种是301响应，称为永久重定向。两者的区别是，如果服务器发送301永久重定向响应，浏览器会缓存/hi到/hello这个重定向的关联，下次请求/hi的时候，浏览器就直接发送/hello请求了。

重定向有什么作用？重定向的目的是当Web应用升级后，如果请求路径发生了变化，可以将原来的路径重定向到新路径，从而避免浏览器请求原路径找不到资源。

HttpServletResponse提供了快捷的redirect()方法实现302重定向。

### http2

>https://halfrost.com/http2-http-frames/

https://www.liaoxuefeng.com/wiki/1252599548343744/1328761739935778

[https://alanli7991.github.io/2016/10/26/HTTP%E8%AF%B7%E6%B1%82GETPOST%E4%B8%8E%E5%8F%82%E6%95%B0%E5%B0%8F%E7%BB%93/](https://alanli7991.github.io/2016/10/26/HTTP%E8%AF%B7%E6%B1%82GETPOST%E4%B8%8E%E5%8F%82%E6%95%B0%E5%B0%8F%E7%BB%93/)

## http basic

- HTTP 用什么请求和参数在哪里一点关系没有
- HTTP 协议对参数长度也没限制，大多数和服务器容器的配置有关
- HTTP 用什么方法都不安全，除非用 HTTPS

## url 参数

在 URL 里放参数最简单，就是问号加键值对，它存在于 HTTP 的 Header 中第一行

```bash
POST /psas/bug/image/confirm?key0=value0&key1=value1&key2=value2 HTTP/1.1
```

## http GET POST 长度

[http://blog.csdn.net/blueling51/article/details/6935901](http://blog.csdn.net/blueling51/article/details/6935901)

1. Get方法长度限制

Http Get方法提交的数据大小长度并没有限制,HTTP协议规范没有对URL长度进行限制。这个限制是特定的浏览器及服务器对它的限制。

如: IE对URL长度的限制是2083字节(2K+35)。

下面就是对各种浏览器和服务器的最大处理能力做一些说明.

Microsoft Internet Explorer (Browser)

IE浏览器对URL的最大限制为2083个字符,如果超过这个数字,提交按钮没有任何反应。

Firefox (Browser)

对于Firefox浏览器URL的长度限制为65,536个字符。

Safari (Browser)

URL最大长度限制为 80,000个字符。

Opera (Browser)

URL最大长度限制为190,000个字符。

Google (chrome)

URL最大长度限制为8182个字符。

Apache (Server)

能接受最大url长度为8,192个字符。

Microsoft Internet Information Server(IIS)

能接受最大url的长度为16,384个字符。

通过上面的数据可知,为了让所有的用户都能正常浏览, URL最好不要超过IE的最大长度限制(2083个字符) ,当然,如果URL不直接提供给用户,而是提供给程序调用,这时的长度就只受Web服务器影响了。

注: 对于中文的传递,最终会为urlencode后的编码形式进行传递,如果浏览器的编码为UTF8的话,一个汉字最终编码后的字符长度为9个字符。

因此如果使用的 GET 方法,最大长度等于URL最大长度减去实际路径中的字符数。

2. POST方法长度限制

理论上讲,POST是没有大小限制的。HTTP协议规范也没有进行大小限制,起限制作用的是服务器的处理程序的处理能力。

如: 在Tomcat下取消POST大小的限制 (Tomcat默认2M) ；

## HTTP 请求超时

请求超时，比如现在网络超级不好，当客户端发起一个请求，通信层开始请求与服务器建立连接（包括在重试），如果在5S之内还没有连接到服务器，那么认为超时。

响应超时，当我们连接到服务器时，一般比如url参数（url?key=value）会直接提交到服务器，比如body类型的参数（Form、JsonBody、key=value&key1=value1等）我们会通过连接中的stream再手动写出去，当服务器接受到请求数据后开始【处理数据->响应】，这个【处理数据->响应】阶段就可能会发生响应超时，比如服务器去执行数据库操作，在5S内还没有对stream做出反馈，那么客户端就认为超时（少部分人对下载有误解，下载则不一样，因为一直有输出数据，也就是对stream做了反馈），主动断开和服务器的连接。

作者：严振杰
链接：[https://www.zhihu.com/question/21609463/answer/160100810](https://www.zhihu.com/question/21609463/answer/160100810)
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
