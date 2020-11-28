---
title: TPS、QPS、RPS
author: w1100n
type: post
date: 2017-11-08T00:40:29+00:00
url: /?p=11375
categories:
  - Uncategorized

---
几个相关的概念：TPS、QPS、RPS,TPS：Transactions Per Second（每秒事务处理数），指服务器每秒处理的事务次数。一般用于评估数据库、交易系统的基准性能。QPS：Queries Per Second（查询量/秒），是服务器每秒能够处理的查询次数，例如域名服务器、Mysql查询性能。RPS：Request Per Second（请求数/秒）RPS（Request Per Second）和QPS可以认为是一回事。RT：Response Time（响应时间）：客户端发一个请求开始计时，到客户端接收到从服务器端返回的响应结果结束所经历的时间，响应时间由请求发送时间、网络传输时间和服务器处理时间三部分组成。也叫Think Time。并发数与TPS/QPS的关系：QPS（TPS）= 并发数/平均响应时间这里的并发数如果为事务处理请求数，则为TPS，如果为查询请求数，则为QPS。

作者：梁川
  
链接：https://www.zhihu.com/question/36734171/answer/68995124
  
来源：知乎
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

QPS（TPS）= 并发数/平均响应时间 或者 并发数 = QPS_平均响应时间 这里响应时间的单位是秒
  
举例，我们一个HTTP请求的响应时间是20ms，在10个并发的情况下，QPS就是 QPS=10_1000/20=500。
  
这里有个关键的点就是QPS一定是跟并发数联系在一起的，离开并发数谈QPS是没意义的。

http://homuralovelive.com/sddtc/tech/2016/06/26/performance-test-qps-tps.html