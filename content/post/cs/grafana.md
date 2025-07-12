---
title: grafana
author: "-"
date: 2019-02-17T12:35:14+00:00
url: grafana
categories:
  - inbox
tags:
  - reprint
---
## grafana

```bash
docker pull grafana/grafana:12.0.2

docker run -d --name=grafana -e "GF_SECURITY_ADMIN_PASSWORD=password0" -p 3000:3000 -v grafana-storage:/var/lib/grafana -v /etc/localtime:/etc/localtime:ro grafana/grafana:12.0.2

# podman
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
-p 3100:3000 \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana:8.5.6

# in pod
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
--pod monitor \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana

```

### variable for host

```sql
SHOW TAG VALUES ON "telegraf" FROM "system" WITH KEY = "host"
```

Q. How do I use the second y axis, secondYAxis function does not work

A. You can switch any series to the second y axis by clicking on the colored line to left of the series name in the legend below the graph. Alternately, use the "Display Styles" > "Series Specific overrides" to define an alias or regex + "Y-axis: 2" to move metrics to the right Axis

[https://github.com/grafana/grafana/wiki/FAQ](https://github.com/grafana/grafana/wiki/FAQ)

## reset password

```bash
sqlite3 /var/lib/grafana/grafana.db
#查看数据库中包含的表
.tables

#查看user表内容
select * from user;

#重置admin用户的密码为默认admin
update user set password = '59acf18b94d7eb0694c61e60ce44c110c7a683ac6a8f09580d626f90f4a242000746579358d77dd9e570e83fa24faa88a8a6', salt = 'F3FAxVm33R' where login = 'admin';

# 退出
.exit
```

## prometheus

/usr/local/etc/prometheus/prometheus.yml

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['host.docker.internal:9100']

  - job_name: 'node_dynamic'
    file_sd_configs:
      - files:
          - /etc/prometheus/node_exporters.json
        refresh_interval: 15s
```

/usr/local/etc/prometheus/node_exporters.json

```json
[
  {
    "targets": ["192.168.50.150:9100"],
    "labels": {
      "instance": "ser8"
    }
  }
]
```


```bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v "/usr/local/etc/prometheus/:/etc/prometheus/" \
  -v "prometheus-data:/prometheus" \
  prom/prometheus:v3.4.2
```

## node_exporter

```bash
# 进入临时目录
cd /tmp

# 获取最新版（也可以访问 GitHub 获取具体版本号）
curl -s https://api.github.com/repos/prometheus/node_exporter/releases/latest \
  | grep browser_download_url \
  | grep linux-amd64.tar.gz \
  | cut -d '"' -f 4 \
  | wget -i -

# 解压
tar -xzf node_exporter-*.linux-amd64.tar.gz

# 移动到系统目录
sudo cp node_exporter-*/node_exporter /usr/local/bin/

sudo useradd -rs /bin/false node_exporter

sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=default.target
EOF


sudo systemctl daemon-reexec
sudo systemctl enable --now node_exporter

```

## loki

/usr/local/etc/loki-config.yaml

```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9095
  log_level: info

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 5m
  chunk_retain_period: 30s
  max_transfer_retries: 0

schema_config:
  configs:
    - from: 2022-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/boltdb-cache
    shared_store: filesystem

  filesystem:
    directory: /loki/chunks

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h  # 7 days

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 7d

ruler:
  storage:
    type: local
    local:
      directory: /loki/rules
  rule_path: /loki/rules-temp
  alertmanager_url: http://localhost:9093
  ring:
    kvstore:
      store: inmemory
  enable_api: true
```




```bash
docker run -d --name=loki \
  -p 3100:3100 \
  -v "/usr/local/etc/loki-config.yaml:/etc/loki/local-config.yaml" \
  grafana/loki:3.5 \
  -config.file=/etc/loki/local-config.yaml

```

/usr/local/etc/promtail-config.yaml

```bash
docker run -d \
  --name=promtail \
  -v /var/lib/docker:/var/lib/docker \
  -v /usr/local/etc/promtail-config.yaml:/etc/promtail/config.yaml \
  grafana/promtail:3.5 \
  -config.file=/etc/promtail/config.yaml

```
