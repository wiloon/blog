---
title: RESTful API 设计
author: "-"
date: 2022-01-20 15:05:51
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


### RESTful API 设计指南
作者： 阮一峰
版权声明：自由转载-非商用-非衍生-保持署名（创意共享3.0许可证）
>https://www.ruanyifeng.com/blog/2014/05/restful_api.html
