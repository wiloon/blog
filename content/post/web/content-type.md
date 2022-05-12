---
title: content-type
author: "-"
date: 2012-03-20T07:07:03+00:00
url: content-type
categories:
  - Web
tags:$
  - reprint
---
## content-type
Content-Type 实体头部用于指示资源的MIME类型 media type 。
Content-Type (内容类型），一般是指网页中存在的 Content-Type，用于定义网络文件的类型和网页的编码，决定浏览器将以什么形式、什么编码读取这个文件

Content-Type 标头告诉客户端实际返回的内容的内容类型。

语法格式：

Content-Type: text/html; charset=utf-8
Content-Type: multipart/form-data; boundary=something


charset
字符编码标准。

常见的媒体格式类型如下：

- text/html ： HTML格式
- text/plain ：纯文本格式
- text/xml ： XML格式
- image/gif ：gif图片格式
- image/jpeg ：jpg图片格式
- image/png：png图片格式
- 以application开头的媒体格式类型：
- 
- application/xhtml+xml ：XHTML格式
- application/xml： XML数据格式
- application/atom+xml ：Atom XML聚合格式
- application/json： JSON数据格式
- application/pdf：pdf格式
- application/msword ： Word文档格式
- application/octet-stream ： 二进制流数据 (如常见的文件下载）
- application/x-www-form-urlencoded ： <form encType=””>中默认的encType，form表单数据被编码为key/value格式发送到服务器 (表单默认的提交数据的格式）
另外一种常见的媒体格式是上传文件之时使用的：

multipart/form-data ： 需要在表单中进行文件上传时，就需要使用该格式


application/json: Official MIME type for json

text/x-json: Experimental(unofficial) MIME type for json before application/json got officially registered

>https://stackoverflow.com/questions/22406077/what-is-the-exact-difference-between-content-type-text-json-and-application-jso
