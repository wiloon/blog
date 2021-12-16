---
title: getRequestDispatcher()， sendRedirect()
author: "-"
date: 2012-10-31T06:01:11+00:00
url: /?p=4582
categories:
  - Web
tags:
  - Servlet

---
## getRequestDispatcher()， sendRedirect()
1.getRequestDispatcher(url)是请求转发，前后页面共享一个request。

RequestDispatcher 对象从客户端获取请求request，并把它们传递给服务器上的servlet,html或jsp。

它有两个方法: forward()和include()具体如下

void forward(ServletRequest request,ServletResponse response) 用来传递request的，可以一个Servlet接收request请求，另一个Servlet用这个request请求来产生response。request传递的请求，response是客户端返回的信息。forward要在response到达客户端之前调用，也就是 before response body output has been flushed。如果不是的话，它会报出异常。

void include(ServletRequest request,ServletResponse response) 用来记录保留request和 response，以后不能再修改response里表示状态的信息。

request.getRequestDispatcher(url).forward(request,response)是直接将请求转发到指定URL，所以该请求能够直接获得上一个请求的数据，request对象始终存在，不会重新创建。

forward 发生在服务器内部, 在浏览器完全不知情的情况下发给了浏览器另外一个页面的response. 这时页面收到的request不是从浏览器直接发来了,可能己经放了数据。

请求转发时如果要传递参数可以这样用: 

request.setAttribute("name","Michael");

request.getAttribute("name");

2.sendRedirect(url)重定向到指定URL，会新建request对象。

这是因为 redirect 会首先发一个response给浏览器, 然后浏览器收到这个response后再发一个requeset给服务器,

然后服务器发新的response给浏览器,这时页面收到的request是从浏览器新发来的,所以上一个request的数据会丢失。

如果要传递参数只有在url后加参数的方式，比如url?type=test才能实现。

3.ServletContext.sendRedirect(String url)中的url只能使用绝对路径; 而ServletRequest.getRequestDispatcher(String url)中的url可以使用相对路径。h这是因为ServletRequest具有相对路径的概念;而ServletContext对象无此概念。

PS:如果需要把请求转移到另外一个WebApp中的某个地址，可以按下面的步骤做法: 

获得另外一个WebApp的ServletConext对象(currentServletContext.getContext(uripath)).

调用ServletContext.getRequestDispatcher(String url)方法。