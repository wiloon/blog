---
title: Prometheus Pushgateway
author: "-"
date: 2026-04-03T14:56:54+08:00
url: prometheus-pushgateway
categories:
  - Linux
tags:
  - Prometheus
  - monitoring
  - AI-assisted
---

Prometheus 的拉取模型（pull model）要求被监控目标必须持续运行并暴露 HTTP `/metrics` 端点。但有些场景不适合这种模式：

- **批处理作业（Batch Job）**：运行几秒或几分钟就退出，Prometheus 来不及抓取
- **CronJob**：定时执行，完成后进程消失
- **短暂任务**：数据管道、一次性脚本

Pushgateway 就是为这类场景设计的中间缓冲层。

## 工作原理

```
Batch Job → POST metrics → Pushgateway ← scrape ← Prometheus → Grafana
```

1. 批处理作业完成后，主动将指标 **推送（push）** 到 Pushgateway
2. Pushgateway 将指标**持久保存**在内存中
3. Prometheus 按照正常 pull 机制定期抓取 Pushgateway 的 `/metrics` 端点
4. Grafana 查询 Prometheus 展示数据

## 安装（Kubernetes）

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pushgateway
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: pushgateway
        image: prom/pushgateway:v1.11.0
        ports:
        - containerPort: 9091
```

默认端口 `9091`，Web UI 可以查看当前存储的所有指标。

## 推送指标

指标格式遵循 [Prometheus text format](https://prometheus.io/docs/instrumenting/exposition_formats/)，通过 HTTP POST 推送：

```sh
# 推送单个指标
cat <<EOF | curl -sf --data-binary @- http://pushgateway:9091/metrics/job/my-job
# HELP batch_processed_total Total records processed
# TYPE batch_processed_total gauge
batch_processed_total 1234
EOF
```

URL 格式：`/metrics/job/<job_name>/[<label_name>/<label_value>...]`

`job` 是必填的分组标签，可以继续追加自定义标签：

```sh
# 带额外标签
curl -sf --data-binary @- \
  http://pushgateway:9091/metrics/job/my-job/instance/server-1 <<EOF
batch_duration_seconds 42.5
EOF
```

## 删除指标

```sh
# 删除某个 job 的所有指标
curl -sf -X DELETE http://pushgateway:9091/metrics/job/my-job
```

Pushgateway **不会自动过期**指标，如果不手动删除，旧数据会一直保留。这是常见的踩坑点。

## 让 Prometheus 发现 Pushgateway

使用 Prometheus Operator 时，通过 ServiceMonitor：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: pushgateway
  labels:
    release: kube-prometheus-stack   # 需与 Prometheus serviceMonitorSelector 匹配
spec:
  selector:
    matchLabels:
      app: pushgateway
  endpoints:
  - port: http
    interval: 60s
```

不使用 Operator 时，直接在 `prometheus.yml` 的 `scrape_configs` 中添加：

```yaml
scrape_configs:
  - job_name: pushgateway
    honor_labels: true               # 保留推送时的 job/instance 标签
    static_configs:
      - targets: ['pushgateway:9091']
```

`honor_labels: true` 很重要：让 Prometheus 使用推送指标中原有的 `job` 和 `instance` 标签，而不是用 Pushgateway 自身的地址覆盖掉。

## 注意事项

**不适合长期运行的服务**：Pushgateway 设计目标是批处理作业，不要用它替代正常的 exporter。对于长期运行的服务，应该直接暴露 `/metrics` 端点让 Prometheus 抓取。

**指标不会自动过期**：作业失败后指标依然存在，Prometheus 会持续抓到"成功"的旧数据。解决方案：
1. 每次运行时覆盖写入（同一 job 名）
2. 成功/失败时都推送，用 `batch_last_success_timestamp` 这类指标判断健康状态
3. 任务结束后主动 DELETE

**单点问题**：Pushgateway 本身没有高可用方案，它的内存数据不持久化。重启后所有推送的指标都会丢失，直到下一次任务重新推送。

**`honor_labels` 的副作用**：开启后，恶意（或误配置的）推送方可以伪造任意标签值，在多租户环境中需注意。

## 相关链接

- [官方文档](https://github.com/prometheus/pushgateway)
- [When to use Pushgateway](https://prometheus.io/docs/practices/pushing/)
