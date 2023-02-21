---
title: "nats"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "nats"

### podman

podman run -d \
--name nats \
-p 4222:4222 \
-v /etc/localtime:/etc/localtime:ro \
nats

<https://zhuanlan.zhihu.com/p/40871363>

nats是一个开源的，云原生的消息系统。Apcera，百度，西门子，VMware，HTC和爱立信等公司都有在使用。

核心基于EventMachine开发，原理是基于消息发布订阅机制，每台服务器上的每个模块会根据自己的消息类别向MessageBus发布多个消息主题，而同时也向自己需要交互的模块，按照需要的主题订阅消息。能够达到每秒8-11百万个消息，整个程序很小只有3M Docker image，它不支持持久化消息，如果你离线，你就不能获得消息。使用nats streaming可以做到持久化，缓存等功能。

NATS server
nats提供了一个go编写的轻量级服务器。发行版包括二进制和docker镜像

NATS clients

nats官方提供的客户端有Go，Node，Ruby，Java，C，C＃，NGINX等。

NATS 设计目标

核心原则是性能，可伸缩和易用性。

高效
始终在线和可用
非常轻巧
支持多种质量的服务
支持各种消息传递模型和使用场景
NATS 使用场景
nats是一个简单且强大的消息系统，为支持现代云原生架构设计。由于可伸缩性的复杂性，nats旨在容易使用和实现，且能提供多种质量的服务。

一些适用nats的场景有:

高吞吐量的消息分散 —— 少数的生产者需要将数据发送给很多的消费者。
寻址和发现 —— 将数据发送给特定的应用实例，设备或者用户，也可用于发现并连接到基础架构中的实例，设备或用户。
命令和控制 (控制面板) —— 向程序或设备发送指令，并从程序/设备中接收状态，如SCADA，卫星遥感，物联网等。
负载均衡 —— 主要应用于程序会生成大量的请求，且可动态伸缩程序实例。
N路可扩展性 —— 通信基础架构能够充分利用go的高效并发/调度机制，以增强水平和垂直的扩展性。
位置透明 —— 程序在各个地理位置上分布者大量实例，且你无法了解到程序之间的端点配置详情，及他们所生产或消费的数据。
容错
使用nats-streaming的附加场景有:

从特定时间或顺序消费
持久性
有保证的消息投递

---

<https://docs.nats.io/>  
<https://github.com/nats-io/nats-server>  
<https://gcoolinfo.medium.com/comparing-nats-nats-streaming-and-nats-jetstream-ec2d9f426dc8>  
