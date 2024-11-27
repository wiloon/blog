---
title: firewall 防火墙
author: "-"
date: 2020-03-01T03:54:44+00:00
url: firewall
categories:
  - Network
tags:
  - reprint
  - remix
---
## firewall 防火墙

### device 

物理设备

### context

物理设备上的虚拟防火墙, 类似于虚拟机的概念
每个 context 可以被看作是一个独立的防火墙实例。每个 context 拥有自己的配置文件、策略和规则集，使得单个物理设备能够同时作为多个独立的防火墙进行操作。

### VRF

VRF（Virtual Routing and Forwarding）
VRF 和 Context 是独立的概念

VRF 是一种在同一物理设备上创建多个虚拟路由表的方法，使得不同的网络流量可以在相同的物理接口上保持逻辑隔离。VRF 主要用于以下场景：


多租户环境：在服务提供商或大型企业网络中，VRF 允许不同的客户或部门共享相同的物理网络设备而保持独立的路由表。
安全隔离：VRF 可以将不同的业务流量在逻辑上隔离开，确保不同业务之间的安全性和隐私性。
灵活性和可扩展性：通过使用 VRF，可以在不增加额外硬件的情况下，灵活地管理和扩展网络。
