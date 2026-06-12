---
title: Promtail 介绍
author: "-"
date: 2026-06-12T08:54:47+08:00
lastmod: 2026-06-12T08:54:47+08:00
url: promtail
categories:
  - Cloud
tags:
  - AI-assisted
  - grafana
  - promtail
  - loki
  - observability
  - remix
---

## Promtail 是什么

Promtail 是 Grafana Labs 开发的**日志采集 agent**，专门用于从各种来源采集日志并将其发送到 [Loki](https://grafana.com/oss/loki/) 存储。名称来源于"Prometheus tail"——受 Prometheus 的 pull 模式启发，但针对日志场景做了适配。

## 主要功能

- **文件 tail**：监控本地文件（如 `/var/log/*.log`），实时采集新增内容
- **systemd journal**：采集 journald 日志
- **syslog 接收**：作为 syslog server，接收远端设备通过 UDP/TCP 推送的日志
- **Docker/Kubernetes**：采集容器日志
- **Label 打标**：通过 pipeline stages 对日志打 label、做正则提取、过滤等

## 与 Loki 的关系

Promtail 是 Loki 的配套 agent：

```
日志源（文件 / syslog / journal）
        ↓
    Promtail（采集、打标、转发）
        ↓
      Loki（存储）
        ↓
    Grafana（查询）
```

三者组合构成 Grafana 的日志技术栈（类比 Prometheus + node_exporter + Grafana 的 metrics 技术栈）。

## 配置示例

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # 采集本地文件
  - job_name: system
    static_configs:
      - targets: [localhost]
        labels:
          job: varlogs
          __path__: /var/log/*.log

  # 接收 syslog（UDP）
  - job_name: syslog
    syslog:
      listen_address: 0.0.0.0:5140
      listen_protocol: udp
      labels:
        job: syslog
    relabel_configs:
      - source_labels: [__syslog_message_hostname]
        target_label: host
```

## 维护状态

> **⚠️ Promtail 已进入维护模式**

Grafana Labs 在 2024 年宣布 Promtail 进入维护模式，不再新增功能，只做安全修复。**官方推荐迁移到 [Grafana Alloy](./grafana-alloy.md)**，Alloy 是 Promtail 的功能超集，同时支持 metrics、logs 和 traces。

| 项       | Promtail     | Grafana Alloy           |
| -------- | ------------ | ----------------------- |
| 维护状态 | 维护模式     | 主动开发                |
| 功能     | 仅 logs      | metrics + logs + traces |
| 推荐用于 | 已有部署维护 | 新建部署                |

## 参考

- [官方文档](https://grafana.com/docs/loki/latest/send-data/promtail/)
- [迁移到 Alloy](https://grafana.com/docs/alloy/latest/tasks/migrate/from-promtail/)
