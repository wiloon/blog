---
title: RESTful API 设计
author: "-"
date: 2022-01-21 14:33:13
url: restful/api/design
categories:
  - restful

---
## RESTful API 设计

域名
应该尽量将API部署在专用域名之下。


https://api.example.com
如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下。

https://example.org/api/


版本（Versioning）
应该将API的版本号放入URL。


https://api.example.com/v1/
另一种做法是，将版本号放在HTTP头信息中，但不如放入URL方便和直观。Github采用这种做法。

路径（Endpoint）
路径又称"终点"（endpoint），表示API的具体网址。

在RESTful架构中，每个网址代表一种资源（resource），所以网址中不能有动词，只能有名词，而且所用的名词往往与数据库的表格名对应。一般来说，数据库中的表都是同种记录的"集合"（collection），所以API中的名词也应该使用复数。

### HTTP动词
对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
- DELETE（DELETE）：从服务器删除资源。
#### 还有两个不常用的HTTP动词。

- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

### RESTful API 设计指南
作者： 阮一峰
版权声明：自由转载-非商用-非衍生-保持署名（创意共享3.0许可证）
>https://www.ruanyifeng.com/blog/2014/05/restful_api.html



登入/登出对应的服务端资源应该是session，所以相关api应该如下：
GET /session # 获取会话信息
POST /session # 创建新的会话（登入）
PUT /session # 更新会话信息
DELETE /session # 销毁当前会话（登出）

而注册对应的资源是user，api如下：
GET /user/:id # 获取id用户的信息
POST /user # 创建新的用户（注册）
PUT /user/:id # 更新id用户的信息
DELETE /user/:id # 删除id用户（注销）

作者：Abel Lee
链接：https://www.zhihu.com/question/20346297/answer/589999953
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
>https://www.v2ex.com/t/118049

