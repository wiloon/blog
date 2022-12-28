---
title: RESTful API 设计
author: "-"
date: 2022-01-21 14:33:13
url: restful/api/design
categories:
  - RESTful
tags:
  - reprint
---
## RESTful API 设计

URI中不应包含结尾的正斜杠（/）。

## 域名

应该尽量将API部署在专用域名之下。 <https://api.example.com>

如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下。 <https://example.org/api/>

## 版本 (Versioning）

应该将API的版本号放入URL。

<https://api.example.com/v1/>
另一种做法是，将版本号放在HTTP头信息中，但不如放入URL方便和直观。Github采用这种做法。

## 路径 (Endpoint）

路径又称"终点" (endpoint），表示API的具体网址。

在RESTful架构中，每个网址代表一种资源 (resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合" (collection），所以API 中的名词也应该使用复数。

### HTTP动词

对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个 (括号里是对应的SQL命令）。

- GET (SELECT）：取出资源 (一项或多项）。
- POST (CREATE）：新建一个资源。
- PUT (UPDATE）：更新资源 (客户端提供改变后的完整资源）, Replace (Create or Update) 如果存在就替换, 没有就新增. 在HTTP中，PUT被定义为幂等(idempotent)的方法，POST 则不是，这是一个很重要的区别
- PATCH (UPDATE）：更新资源 (客户端提供改变的属性）。
- DELETE (DELETE）：删除资源。

#### 还有两个不常用的HTTP动词

- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

### 状态码 (Status Codes）

服务器向用户返回的状态码和提示信息，常见的有以下一些 (方括号中是该状态码对应的HTTP动词）。

- 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的 (Idempotent）。
- 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
- 202 Accepted - [*]：表示一个请求已经进入后台排队 (异步任务）
- 204 NO CONTENT - [DELETE]：用户删除数据成功。
- 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
- 401 Unauthorized - [*]：表示用户没有权限 (令牌、用户名、密码错误）,未登录或会话过期 (需要登录但未登录或会话过期）
- 403 Forbidden - [*] 表示用户得到授权 (与401错误相对），但是访问是被禁止的。没有权限访问、操作 (IP受限或已登录但没权限）
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得 (比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
- 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

### RESTful API 设计指南

作者： 阮一峰
版权声明：自由转载-非商用-非衍生-保持署名 (创意共享3.0许可证）

<https://www.ruanyifeng.com/blog/2014/05/restful_api.html>

登入/登出对应的服务端资源应该是session，所以相关api应该如下：

- GET /session # 获取会话信息
- POST /session # 创建新的会话 (登入）
- PUT /session # 更新会话信息
- DELETE /session # 销毁当前会话 (登出）

而注册对应的资源是user，api如下：
GET /user/:id # 获取id用户的信息
POST /user # 创建新的用户 (注册）
PUT /user/:id # 更新id用户的信息
DELETE /user/:id # 删除id用户 (注销）

作者：Abel Lee
链接：<https://www.zhihu.com/question/20346297/answer/589999953>
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<https://www.v2ex.com/t/118049>

1. 资源对象集
如果用来描述一种资源（一个资源的聚合），那么需要用复数形式表示，比如下面的例子：

<http://www.goodhr.com/api/v1/companies/66/employees>
2. 单独资源对象
如果用来描述一个资源，那么，这个资源肯定是可以有一个唯一标示的来确定这个资源，比如下面的例子：

<http://www.goodhr.com/api/v1/companies/66/employees/{员工id>}

<https://zhuanlan.zhihu.com/p/81723602>
