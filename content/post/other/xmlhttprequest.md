---
title: XMLHttpRequest, XHR
author: "-"
date: 2012-09-09T07:15:49+00:00
url: /?p=4021
categories:
  - Java
  - Web
tags:
  - reprint
---
## XMLHttpRequest, XHR
XMLHttpRequest可以提供不重新加载页面的情况下更新网页，在页面加载后在客户端向服务器请求数据，在页面加载后在服务器端接受数据，在后台向客户端发送数据。XMLHttpRequest 对象提供了对 HTTP 协议的完全的访问，包括做出 POST 和 HEAD 请求以及普通的 GET 请求的能力。XMLHttpRequest 可以同步或异步返回 Web 服务器的响应，并且能以文本或者一个 DOM 文档形式返回内容。尽管名为 XMLHttpRequest，它并不限于和 XML 文档一起使用: 它可以接收任何形式的文本文档。XMLHttpRequest 对象是名为 AJAX 的 Web 应用程序架构的一项关键功能。

浏览器支持

XMLHttpRequest 得到了所有现代浏览器较好的支持。唯一的浏览器依赖性涉及 XMLHttpRequest 对象的创建。在 IE 5 和 IE 6 中，必须使用特定于 IE 的 ActiveXObject() 构造函数。正如在 XMLHttpRequest 对象 这一节所介绍的。

W3C 标准化

XMLHttpRequest 对象还没有标准化，但是 W3C 已经开始了标准化的工作，本手册介绍的内容都是基于标准化的工作草案。

当前的 XMLHttpRequest 实现已经相当一致。但是和标准有细微的不同。例如，一个实现可能返回 null，而标准要求是空字符串，或者实现可能把 readyState 设置为 3 而不保证所有的响应头部都可用。

### readyState

HTTP 请求的状态.当一个 XMLHttpRequest 初次创建时，这个属性的值从 0 开始，直到接收到完整的 HTTP 响应，这个值增加到 4。



  
    
      状态
    
    
    
      名称
    
    
    
      描述
    
  
  
  
    
    
    
    
      Uninitialized
    
    
    
      初始化状态。XMLHttpRequest 对象已创建或已被 abort() 方法重置。
    
  
  
  
    
      1
    
    
    
      Open
    
    
    
      open() 方法已调用，但是 send() 方法未调用。请求还没有被发送。
    
  
  
  
    
      2
    
    
    
      Send
    
    
    
      Send() 方法已调用，HTTP 请求已发送到 Web 服务器。未接收到响应。
    
  
  
  
    
      3
    
    
    
      Receiving
    
    
    
      所有响应头部都已经接收到。响应体开始接收但未完成。
    
  
  
  
    
      4
    
    
    
      Loaded
    
    
    
      HTTP 响应已经完全接收。
    
  


5 个状态中每一个都有一个相关联的非正式的名称，下表列出了状态、名称和含义: 

   readyState 的值不会递减，除非当一个请求在处理过程中的时候调用了 abort() 或 open() 方法。每次这个属性的值增加的时候，都会触发 onreadystatechange 事件句柄。 
  
    responseText
  
  
    目前为止从服务器接收到的响应体 (不包括头部) ，或者如果还没有接收到数据的话，就是空字符串。
  
  
  
    如果 readyState 小于 3，这个属性就是一个空字符串。当 readyState 为 3，这个属性返回目前已经接收的响应部分。如果 readyState 为 4，这个属性保存了完整的响应体。
  
  
  
    如果响应包含了为响应体指定字符编码的头部，就使用该编码。否则，假定使用 Unicode UTF-8。
  

### statu

由服务器返回的 HTTP 状态代码，如 200 表示成功，而 404 表示 "Not Found" 错误。当 readyState 小于 3 的时候读取这一属性会导致一个异常。

### statusText

这个属性用名称而不是数字指定了请求的 HTTP 的状态代码。也就是说，当状态为 200 的时候它是 "OK"，当状态为 404 的时候它是 "Not Found"。和 status 属性一样，当 readyState 小于 3 的时候读取这一属性会导致一个异常。

**onreadystatechange: **


每次 readyState 属性改变的时候调用的事件句柄函数。当 readyState 为 3 时，它也可能调用多次。

**onreadystatechange: **


每次 readyState 属性改变的时候调用的事件句柄函数。当 readyState 为 3 时，它也可能调用多次。