---
title: Grafana Alloy 介绍
author: "-"
date: 2026-06-12T08:54:47+08:00
lastmod: 2026-06-12T09:56:01+08:00
url: grafana-alloy
categories:
  - Cloud
tags:
  - AI-assisted
  - grafana
  - alloy
  - observability
  - remix
---

## Grafana Alloy 是什么

Grafana Alloy 是 Grafana Labs 推出的**开源可观测性采集器**（collector），用于采集 metrics、logs、traces 并转发到后端存储（Prometheus、Loki、Tempo 等）。

它是 [Grafana Agent](https://github.com/grafana/agent) 的继任产品，从 2024 年起 Grafana Agent 进入维护模式，Alloy 成为官方推荐替代。

## 核心能力

| 能力         | 说明                                                                                     |
| ------------ | ---------------------------------------------------------------------------------------- |
| Metrics 采集 | 兼容 Prometheus scrape，支持 remote_write 转发                                           |
| Logs 采集    | 支持 syslog receiver、file tail、journal、Docker 等，写入 Loki                           |
| Traces 采集  | 接收 OTLP、Jaeger 等，写入 Tempo                                                         |
| 统一入口     | 一个进程同时处理 metrics + logs + traces，替代 node_exporter + Promtail + OTel Collector |

## 与 Promtail 的关系

[Promtail](./promtail.md) 是 Grafana Labs 早期专门用于日志采集并写入 Loki 的 agent，功能单一（只做 logs）。Alloy 是它的功能超集：

| 对比项      | Promtail                                                                                    | Alloy                        |
| ----------- | ------------------------------------------------------------------------------------------- | ---------------------------- |
| 维护状态    | **维护模式**（不再新增功能）                                                                | **主动开发**                 |
| 功能范围    | 仅 logs → Loki                                                                              | metrics + logs + traces      |
| 配置语言    | YAML                                                                                        | River（DSL，类 HCL）         |
| syslog 接收 | 支持                                                                                        | 支持（`loki.source.syslog`） |
| 迁移        | 官方提供 [migrate 工具](https://grafana.com/docs/alloy/latest/tasks/migrate/from-promtail/) | —                            |

> **Promtail 已停止新功能开发（维护模式）**，Grafana Labs 官方建议将现有 Promtail 部署迁移到 Alloy。新项目请直接使用 Alloy，不再新建 Promtail 部署。

## 配置语言（River / Alloy syntax）

Alloy 使用自己的 DSL（早期叫 River，后改为 "Alloy configuration syntax"），类似 HCL，以组件（component）为基本单元，通过引用连接数据流：

```alloy
// 采集文件日志
loki.source.file "app_logs" {
  targets    = [{ __path__ = "/var/log/app.log" }]
  forward_to = [loki.write.default.receiver]
}

// 写入 Loki
loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```

## 接收 syslog

Alloy 支持作为 **syslog server** 接收远端设备（如 OpenWrt、路由器、交换机）推送的 UDP/TCP syslog，打上 label 后写入 Loki。

在这个模式下，Alloy 是**服务端**——启动后主动绑定并监听指定端口，等待远端设备推入数据。OpenWrt 是**客户端**，配置 `log_ip` / `log_port` 后主动发出 syslog 包。Alloy 收到后再 push 给 Loki，整条链路没有任何 pull 动作。

> 由于 Alloy Pod 需要对外暴露 UDP 端口，K8s 部署时需要配置 `hostPort` 或 `NodePort`（UDP NodePort 在部分 CNI 下有兼容性问题，优先 `hostPort`）。

```alloy
loki.source.syslog "openwrt" {
  listener {
    address  = "0.0.0.0:5140"
    protocol = "udp"
    labels   = {
      job  = "syslog",
      host = "openwrt",
    }
  }
  forward_to = [loki.write.default.receiver]
}
```

发送端（OpenWrt）只需配置：

```bash
uci set system.@system[0].log_ip='<alloy-host>'
uci set system.@system[0].log_port='5140'
uci set system.@system[0].log_proto='udp'
uci commit system
service log restart
```

## 工作模式：pull vs push

Alloy 支持两种工作模式，取决于信号类型和配置。

| 信号    | pull（被动暴露）                           | push（主动推送）        |
| ------- | ------------------------------------------ | ----------------------- |
| Metrics | ✅ 暴露 `/metrics` 端点供 Prometheus scrape | ✅ `remote_write` 主动推 |
| Logs    | ✗                                          | ✅ 推到 Loki             |
| Traces  | ✗                                          | ✅ 推到 Tempo            |

### Metrics pull 模式

Alloy 可以像 node_exporter 一样暴露 `/metrics` 端点，等 Prometheus 来 scrape。

### Metrics push 模式

Alloy 也可以主动 scrape 目标，再通过 `prometheus.remote_write` 推到 Prometheus / Mimir / VictoriaMetrics：

```alloy
// scrape 本机 node_exporter，再 remote_write 出去
prometheus.scrape "node" {
  targets    = [{"__address__" = "localhost:9100"}]
  forward_to = [prometheus.remote_write.default.receiver]
}

prometheus.remote_write "default" {
  endpoint { url = "http://prometheus:9090/api/v1/write" }
}
```

### Logs / Traces：只有 push

日志和链路追踪没有 pull 模式——Alloy 主动 tail 文件或接收 syslog/OTLP，然后推到 Loki / Tempo。

## 部署方式

- **Helm**（Kubernetes）：`helm install alloy grafana/alloy`
- **二进制**：直接下载运行，适合 VM / 物理机
- **systemd service**：Linux 上推荐

## 参考

- [官方文档](https://grafana.com/docs/alloy/latest/)
- [从 Promtail 迁移](https://grafana.com/docs/alloy/latest/tasks/migrate/from-promtail/)
- [组件参考](https://grafana.com/docs/alloy/latest/reference/components/)
