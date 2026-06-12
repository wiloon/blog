---
title: Grafana Explore 与 Logs Drilldown 的区别
author: "-"
date: 2026-06-12T15:59:26+08:00
lastmod: 2026-06-12T15:59:26+08:00
url: grafana-explore-vs-drilldown
categories:
  - Cloud
tags:
  - grafana
  - loki
  - observability
  - remix
  - AI-assisted
---

用 Loki 收集日志后，Grafana 提供两个查看日志的入口：**Explore** 和 **Logs Drilldown**。Explore 页面上会有提示引导用户打开 Drilldown，两者功能互补，定位不同。

## Grafana Explore

Explore 是 Grafana 的**内置**数据探索工具，内置于 Grafana 核心，无需额外安装。

主要特点：

- 手动编写查询语句（Loki 使用 LogQL，Prometheus 使用 PromQL）
- 支持所有 Grafana 数据源（Loki、Prometheus、Tempo、Elasticsearch 等）
- 适合有一定查询语言基础的用户做临时分析、调试
- 支持 Split view（左右分屏对比两个查询结果）
- 支持 Live tail 实时追踪日志流
- 可快速从 Dashboard 面板跳转过来做深入分析

## Grafana Logs Drilldown

Logs Drilldown（插件 ID：`grafana-lokiexplore-app`）是 Grafana Labs 开发的**独立 App 插件**，需要单独安装。

> 它的前身叫 "Explore Logs"（这也是 GitHub 仓库名 `explore-logs` 和插件 ID 中含 `lokiexplore` 的由来），后来作为 "Drilldown" 系列产品之一改名为 Logs Drilldown。

主要特点：

- **无需写查询语言**，通过点击可视化界面即可过滤和钻取日志
- 自动为 Loki 数据生成可视化图表（按 label、field、pattern 分组）
- 支持按 volume（日志量）和 text pattern（文本规律）发现异常
- 每个面板都提供"在 Explore 中打开"的链接，方便切回手写查询
- 要求 Grafana ≥ 11.6，Loki ≥ 3.2

## 两者关系

| 对比维度   | Grafana Explore                | Logs Drilldown             |
| ---------- | ------------------------------ | -------------------------- |
| 是否内置   | 内置，无需安装                 | App 插件，需安装           |
| 查询方式   | 手写 LogQL                     | 点击界面，无需写查询       |
| 支持数据源 | 所有 Grafana 数据源            | 仅 Loki                    |
| 适合场景   | 熟悉 LogQL 的深度调试          | 快速浏览、发现规律         |
| 互通       | Drilldown 面板可跳转到 Explore | Explore 提示打开 Drilldown |

两者互为补充：**Drilldown 是低门槛的起点**，适合快速找到问题所在；**Explore 是全功能的工具箱**，适合写精确查询做深度分析。Explore 上的引导提示正是建议不熟悉 LogQL 的用户先去 Drilldown 上直观探索，找到感兴趣的范围后再回 Explore 精确查询。

## 安装 Logs Drilldown

自托管 Grafana 需要手动安装插件：

```bash
grafana-cli plugins install grafana-lokiexplore-app
```

或在 Grafana 配置文件中启用（kube-prometheus-stack 等 Helm chart 通常支持通过 `grafana.ini` 或 sidecar 自动安装插件）：

```ini
[plugins]
allow_loading_unsigned_plugins = grafana-lokiexplore-app
```

安装后在 Grafana 左侧菜单 → Drilldown → Logs 进入。
