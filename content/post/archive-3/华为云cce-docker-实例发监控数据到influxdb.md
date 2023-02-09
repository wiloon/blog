---
title: 华为云CCE, docker 实例发监控数据到influxdb
author: "-"
date: 2020-04-22T14:37:43+00:00
url: /?p=16053
categories:
  - Inbox
tags:
  - reprint
---
## 华为云CCE, docker 实例发监控数据到influxdb

docker集群内部新建telegraf实例

从官方repo取到的telegraf镜像 不是最新版本， 手动上传导出 的docker image 到华为云，并创建telegraf 实例

telegraf使用influxdb_listener input plugin
  
docker 实例 内的应用 用go metrics influxdb发数据到集群内的telegraf 的 influxdb listener
