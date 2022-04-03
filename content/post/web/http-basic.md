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
  
  
    2．GET与POST区别
  
  
    HTTP定义了与服务器交互的不同方法，最基本的方法是 GET 和 POST.
  
  
    HTTP-GET和HTTP-POST是使用HTTP的标准协议动词，用于编码和传送变量名/变量值对参数，并且使用相关的请求语义。每个HTTP-GET和HTTP-POST都由一系列HTTP请求头组成，这些请求头定义了客户端从服务器请求了什么，而响应则是由一系列HTTP应答头和应答数据组成，如果请求成功则返回应答。
 HTTP-GET以使用MIME类型application/x-www-form-urlencoded的urlencoded文本的格式传递参数。Urlencoding是一种字符编码，保证被传送的参数由遵循规范的文本组成，例如一个空格的编码是"%20"。附加参数还能被认为是一个查询字符串。
 与HTTP-GET类似，HTTP-POST参数也是被URL编码的。然而，变量名/变量值不作为URL的一部分被传送，而是放在实际的HTTP请求消息内部被传送。
  
  
    
      get是从服务器上获取数据，post是向服务器传送数据。
    
    
      在客户端，Get方式在通过URL提交数据，数据在URL中可以看到；数据的按照variable=value的形式，添加到action所指向的URL后面，并且两者使用"?"连接，而各个变量之间使用"&"连接；POST方式，数据放置在HTML HEADER内提交。
    
    
      对于get方式，服务器端用Request.QueryString获取变量的值，对于post方式，服务器端用Request.Form获取提交的数据。
    
    
      GET方式提交的数据最多只能有1024字节，而POST则没有此限制。上传文件只能使用Post.
    
    
      安全性问题。使用 Get 的时候，参数会显示在地址栏上，而 Post 不会。所以，如果这些数据是中文数据而且是非敏感数据，那么使用 get；如果用户输入的数据不是中文字符而且包含敏感数据，那么还是使用 post为好。
    
    
      Get限制Form表单的数据集的值必须为ASCII字符；而Post支持整个ISO10646字符集。默认是用ISO-8859-1编码
    
    
      Get是Form的默认方法。
    
    
      get方法没有请求实体，含有数据的url都在请求头里面.
    
  
  
    注: 所谓安全的意味着该操作用于获取信息而非修改信息。幂等的意味着对同一 URL 的多个请求应该返回同样的结果。完整的定义并不像看起来那样严格。换句话说，GET 请求一般不应产生副作用。从根本上讲，其目标是当用户打开一个链接时，她可以确信从自身的角度来看没有改变资源。比如，新闻站点的头版不断更新。虽然第二次请求会返回不同的一批新闻，该操作仍然被认为是安全的和幂等的，因为它总是返回当前的新闻。反之亦然。POST 请求就不那么轻松了。POST 表示可能改变服务器上的资源的请求。仍然以新闻站点为例，读者对文章的注解应该通过 POST 请求实现，因为在注解提交之后站点已经不同了 (比方说文章下面出现一条注解) 。
  
  
    下面举一个简单的例子来说明它们的区别: 
  
  
    ```html
 <!-分别通过get和post方式提交表单->
 <FORM ACTION="getpost.asp" METHOD="get">
 <INPUT TYPE="text" NAME="Text" VALUE="
 
 http://wxf0701.cnblogs.com/
 />
 <INPUT TYPE="submit" VALUE="Get方式"></INPUT>
 </FORM>
 

 <FORM ACTION="getpost.asp" METHOD="post">
 <INPUT TYPE="text" NAME="Text" VALUE="http://wxf0701.cnblogs.com/>
 <INPUT TYPE="submit" VALUE="Post方式"></INPUT>
 </FORM>
 
  
  
    <% If Request.QueryString("Text") <> "" Then %>
 通过get方式传递的字符串是:  "<%= Request.QueryString("Text") %>"

 <% End If %>
  
  
    <% If Request.Form("Text") <> "" Then %>
 通过Post方式传递的字符串是:  "<%= Request.Form("Text") %>"

 <% End If %>
 ```
  
  
    RFC2616 http://www.ietf.org/rfc/rfc2616.txt
  

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

---

https://www.liaoxuefeng.com/wiki/1252599548343744/1328761739935778