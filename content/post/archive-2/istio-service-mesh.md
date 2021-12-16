---
title: Istio, Service Mesh
author: "-"
date: 2018-06-28T04:55:10+00:00
url: /?p=12373
categories:
  - Uncategorized

---
## Istio, Service Mesh
service mesh是微服务时代的TCP协议

Istio是由Google/IBM/Lyft共同开发的新一代Service Mesh开源项目

容错: 当请求失败和重试的时候,使用它能够理解的响应状态码；
  
金丝雀发布: 只将特定百分比的请求转发到服务的新版本上；
  
监控和指标: 统计服务响应所耗费的时间；
  
跟踪和可观察性: 它在每个请求上添加了一个特殊的头部信息,并在集群中跟踪它们；
  
安全性: 抽取 JWT Token 并对用户进行认证和授权。

控制平面由三个组件组成: Pilot、Mixer 和 Citadel,它们组合配置 Envoy 以便于路由流量、执行策略和收集遥测数据。

[http://www.infoq.com/cn/articles/istio-future-service-mesh?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global][1]
  
<https://servicemesh.gitbooks.io/awesome-servicemesh/mesh/2017/service-mesh-next-generation-of-microservice/>

 [1]: http://www.infoq.com/cn/articles/istio-future-service-mesh?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global