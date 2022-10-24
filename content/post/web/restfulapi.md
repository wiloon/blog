---
author: "-"
date: "2020-07-22 17:38:41" 
title: "RESTful api"
categories:
  - RESTful
tags:
  - reprint
---
## "RESTful api"

<http://www.ruanyifeng.com/blog/2014/05/restful_api.html>

路径 (Endpoint)
路径又称"终点" (endpoint) ，表示API的具体网址。

在RESTful架构中，每个网址代表一种资源 (resource) ，所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合" (collection) ，所以API中的名词也应该使用复数。

举例来说，有一个API提供动物园 (zoo) 的信息，还包括各种动物和雇员的信息，则它的路径应该设计成下面这样。

<https://api.example.com/v1/zoos>
<https://api.example.com/v1/animals>
<https://api.example.com/v1/employees>

HTTP动词
对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个 (括号里是对应的SQL命令) 。

GET (SELECT) : 从服务器取出资源 (一项或多项) 。
POST (CREATE) : 在服务器新建一个资源。
PUT (UPDATE) : 在服务器更新资源 (客户端提供改变后的完整资源) 。
PATCH (UPDATE) : 在服务器更新资源 (客户端提供改变的属性) 。
DELETE (DELETE) : 从服务器删除资源。
还有两个不常用的HTTP动词。

HEAD: 获取资源的元数据。
OPTIONS: 获取信息，关于资源的哪些属性是客户端可以改变的。

参数命名规范
query parameter可以采用驼峰命名法，也可以采用下划线命名的方式，推荐采用下划线命名的方式，据说后者比前者的识别度要高，其中，做前端开发基本都后后者，而做服务器接口开发基本用前者。
<http://example.com/api/users/today_login> 获取今天登陆的用户
<http://example.com/api/users/today_login&sort=login_desc> 获取今天登陆的用户、登陆时间降序排列

REST API规范
编写REST API，实际上就是编写处理HTTP请求的async函数，不过，REST请求和普通的HTTP请求有几个特殊的地方:

REST请求仍然是标准的HTTP请求，但是，除了GET请求外，POST、PUT等请求的body是JSON数据格式，请求的Content-Type为application/json；
REST响应返回的结果是JSON数据格式，因此，响应的Content-Type也是application/json。
REST规范定义了资源的通用访问格式，虽然它不是一个强制要求，但遵守该规范可以让人易于理解。

<https://www.liaoxuefeng.com/wiki/1022910821149312/1105003357927328>
<https://www.ruanyifeng.com/blog/2018/10/restful-api-best-practices.html>
