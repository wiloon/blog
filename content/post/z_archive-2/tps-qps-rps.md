---
title: TPS、QPS、RPS
author: "-"
date: 2017-11-08T00:40:29+00:00
url: qps
categories:
  - inbox
tags:
  - reprint
---
## TPS、QPS、RPS
### PPS
PPS (Packet Per Second) 

### PCT (percentile)
PCT99: 99%的响应时间  
“90th pct/95th pct/99th pct”分别表示测试实例按响应时间从小到大排序后,第90/95/99个测试实例的响应时间。

95%percentile :  统计学术语,如果将一组数据从小到大排序,并计算相应的累计百分位,则某一百分位所对应数据的值就称为这一百分位的百分位数。可表示为: 一组 n 个观测值按数值大小排列。如,处于 p% 位置的值称第 p 百分位数。


QPS

Queries Per Second,每秒查询数。每秒能够响应的查询次数。

QPS是对一个特定的查询服务器在规定时间内所处理流量多少的衡量标准,在因特网上,作为域名系统服务器的机器的性能经常用每秒查询率来衡量。每秒的响应请求数,也即是最大吞吐能力。

TPS

Transactions Per Second 的缩写,每秒处理的事务数目。一个事务是指一个客户机向服务器发送请求然后服务器做出反应的过程。客户机在发送请求时开始计时,收到服务器响应后结束计时,以此来计算使用的时间和完成的事务个数,最终利用这些信息作出的评估分。

TPS 的过程包括: 客户端请求服务端、服务端内部处理、服务端返回客户端。

例如,访问一个 Index 页面会请求服务器 3 次,包括一次 html,一次 css,一次 js,那么访问这一个页面就会产生一个“T”,产生三个“Q”。

PV (page view) 即页面浏览量,通常是衡量一个网络新闻频道或网站甚至一条网络新闻的主要指标。

PV 即 page view,页面浏览量。用户每一次对网站中的每个页面访问均被记录 1 次。用户对同一页面的多次刷新,访问量累计。

根据这个特性,刷网站的 PV 就很好刷了。

与 PV 相关的还有 RV,即重复访问者数量 (repeat visitors) 。

UV 访问数 (Unique Visitor) 指独立访客访问数,统计1天内访问某站点的用户数(以 cookie 为依据),一台电脑终端为一个访客。

IP (Internet Protocol) 独立 IP 数,是指 1 天内多少个独立的 IP 浏览了页面,即统计不同的 IP 浏览用户数量。同一 IP 不管访问了几个页面,独立 IP 数均为 1；不同的 IP 浏览页面,计数会加 1。IP 是基于用户广域网 IP 地址来区分不同的访问者的,所以,多个用户 (多个局域网 IP) 在同一个路由器 (同一个广域网 IP) 内上网,可能被记录为一个独立 IP 访问者。如果用户不断更换 IP,则有可能被多次统计。

GMV,是 Gross Merchandise Volume 的简称。只要是订单,不管消费者是否付款、卖家是否发货、是否退货,都可放进 GMV 。

### RPS
RPS 代表吞吐率,即 Requests Per Second 的缩写。吞吐率是服务器并发处理能力的量化描述,单位是 reqs/s,指的是某个并发用户数下单位时间内处理的请求数。
某个并发用户数下单位时间内能处理的最大的请求数,称之为最大吞吐率。

有人把 RPS 说等效于 QPS。其实可以看作同一个统计方式,只是叫法不同而已。RPS/QPS,可以使用 apache ab 工具进行测量。

#### 另外一种RPS
rps(record per second)

几个相关的概念: TPS、QPS、RPS,TPS: Transactions Per Second (每秒事务处理数) ,指服务器每秒处理的事务次数。一般用于评估数据库、交易系统的基准性能。QPS: Queries Per Second (查询量/秒) ,是服务器每秒能够处理的查询次数,例如域名服务器、MySQL查询性能。RPS: Request Per Second (请求数/秒) RPS (Request Per Second) 和QPS可以认为是一回事。RT: Response Time (响应时间) : 客户端发一个请求开始计时,到客户端接收到从服务器端返回的响应结果结束所经历的时间,响应时间由请求发送时间、网络传输时间和服务器处理时间三部分组成。也叫Think Time。并发数与TPS/QPS的关系: QPS (TPS) = 并发数/平均响应时间这里的并发数如果为事务处理请求数,则为TPS,如果为查询请求数,则为QPS。

作者: 梁川
  
链接: https://www.zhihu.com/question/36734171/answer/68995124
  
来源: 知乎
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

QPS (TPS) = 并发数/平均响应时间 或者 并发数 = QPS_平均响应时间 这里响应时间的单位是秒
  
举例,我们一个HTTP请求的响应时间是20ms,在10个并发的情况下,QPS就是 QPS=10_1000/20=500。
  
这里有个关键的点就是QPS一定是跟并发数联系在一起的,离开并发数谈QPS是没意义的。

http://homuralovelive.com/sddtc/tech/2016/06/26/performance-test-qps-tps.html  

https://cloud.tencent.com/developer/article/1487536

