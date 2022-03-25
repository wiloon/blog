---
title: "Spring Cloud"
author: "-"
date: "2021-09-14 20:38:24"
url: "Spring-Cloud"
categories:
  - inbox
tags:
  - inbox
---
## "Spring Cloud"

Eureka [jʊ'ri:kə]
Ribbon [ˈrɪbən]
Feign [fen]
Hystrix [hɪst'rɪks]
Zuul [zulu]
Sleuth [sluθ]
Turbine [ˈtɜ:rbaɪn]


Spring Cloud Netflix (Eureka、Hystrix、Zuul、Archaius) 、Spring Cloud Config、Spring Cloud Bus、Spring Cloud Cluster、Spring Cloud Consul、Spring Cloud Security、Spring Cloud Sleuth、Spring Cloud Data Flow、Spring Cloud Stream、Spring Cloud Task、Spring Cloud Zookeeper、Spring Cloud Connectors、Spring Cloud Starters、Spring Cloud CLI

- Eureka: 服务注册中心，一个基于REST的服务，用于定位服务，以实现微服务架构中服务发现和故障转移。
- Hystrix: 熔断器，容错管理工具，旨在通过熔断机制控制服务和第三方库的节点,从而对延迟和故障提供更强大的容错能力。

l Turbine: Turbine是聚合服务器发送事件流数据的一个工具，用来监控集群下Hystrix的Metrics情况。

l Zuul: API网关，Zuul是在微服务中提供动态路由、监控、弹性、安全等边缘服务的框架。

l Ribbon: 提供微服务中的负载均衡功能，有多种负载均衡策略可供选择，可配合服务发现和断路器使用。

l Feign: Feign是一种声明式、模板化的HTTP客户端。

l Spring Cloud Config: 配置管理工具包，让你可以把配置放到远程服务器，集中化管理集群配置，目前支持本地存储、Git以及Subversion。

l Spring Cloud Security: 基于Spring Security的安全工具包，为微服务的应用程序添加安全控制。

### Spring Cloud Sleuth
日志收集工具包，封装了Dapper和log-based追踪以及Zipkin和HTrace操作，为SpringCloud应用实现了一种分布式追踪解决方案。

除了上面介绍的基础组件外，常见的Spring Cloud组件还有非常多种，涉及到了微服务以及应用开发的方方面面: 

l Spring Cloud Starters: Spring Boot式的启动项目，为Spring Cloud提供开箱即用的依赖管理。

l Archaius: 配置管理API，包含一系列配置管理API，提供动态类型化属性、线程安全配置操作、轮询框架、回调机制等功能。

l Consul: 封装了Consul操作，Consul是一个服务发现与配置工具，与Docker容器可以无缝集成。

l Spring Cloud Stream: 数据流操作开发包，封装了与Redis,Rabbit、Kafka等发送接收消息。

l Spring Cloud CLI: 基于 Spring Boot CLI，可以让你以命令行方式快速建立云组件。

l Spring Cloud Task: 提供云端计划任务管理、任务调度。

l Spring Cloud Bus: 事件、消息总线，用于在集群 (例如，配置变化事件) 中传播状态变化，可与Spring Cloud Config联合实现热部署。

l Spring Cloud Data Flow: 大数据操作工具，作为Spring XD的替代产品，它是一个混合计算模型，结合了流数据与批量数据的处理方式。

l Spring Cloud Zookeeper: 操作Zookeeper的工具包，用于使用zookeeper方式的服务发现和配置管理。

l Spring Cloud Connectors: 便于云端应用程序在各种PaaS平台连接到后端，如: 数据库和消息代理服务。



>https://coolshell.me/articles/talking-about-service-governance-microservices-and-service-mesh.htmlSOA