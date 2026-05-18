---
title: Litestream
author: "-"
date: 2026-05-18T15:16:00+08:00
url: litestream
categories:
  - cloud
tags:
  - sqlite
  - s3
  - backup
  - AI-assisted
---

## 简介

[Litestream](https://litestream.io) 是一个开源工具，专为 SQLite 设计，以 **sidecar 进程**的方式运行，持续监听 SQLite 的 WAL（Write-Ahead Log），实时将变更流式同步到对象存储（S3、GCS、Azure Blob 等）。

核心特点：

- **不改应用代码**：应用仍然正常读写 SQLite，Litestream 在旁边透明工作
- **实时增量复制**：默认每秒同步一次 WAL frames，不是全量快照
- **RPO 秒级**：最多丢失几秒内的写入，远优于每日全量备份的 24 小时 RPO
- **可恢复到任意时间点**：S3 上保留完整的 WAL 历史，支持 point-in-time restore

## 工作原理

```
应用写 SQLite (enx.db)
  └─ SQLite WAL 机制产生变更帧
       └─ Litestream 监听 WAL
            └─ 定期上传 WAL frames 到 S3
                 └─ S3 保留完整变更历史
```

恢复时，Litestream 从 S3 下载快照 + WAL frames，重放到指定时间点。

## 安装

```bash
# Arch Linux
yay -S litestream-bin

# 直接下载二进制（Linux amd64）
wget https://github.com/benbjohnson/litestream/releases/latest/download/litestream-linux-amd64.tar.gz
tar -xzf litestream-linux-amd64.tar.gz
sudo mv litestream /usr/local/bin/
```

## 配置

创建配置文件 `/etc/litestream.yml`：

```yaml
dbs:
  - path: /var/lib/enx-api/enx.db
    replicas:
      - type: s3
        bucket: wiloon-enx-backup
        path: litestream/enx
        region: ap-northeast-1
```

AWS 鉴权优先使用 EC2 IAM Instance Profile，无需配置 Access Key。

## 运行

### 作为 systemd 服务

```ini
# /etc/systemd/system/litestream.service
[Unit]
Description=Litestream SQLite replication
After=network.target

[Service]
ExecStart=/usr/local/bin/litestream replicate -config /etc/litestream.yml
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now litestream
sudo systemctl status litestream
```

### 命令行手动运行

```bash
# 启动持续复制
litestream replicate -config /etc/litestream.yml

# 查看复制状态
litestream snapshots s3://wiloon-enx-backup/litestream/enx

# 列出可用的恢复时间点
litestream generations s3://wiloon-enx-backup/litestream/enx
```

## 恢复

```bash
# 停止应用
sudo systemctl stop enx-api

# 恢复到最新状态
litestream restore -config /etc/litestream.yml /var/lib/enx-api/enx.db

# 恢复到指定时间点
litestream restore \
  -timestamp "2026-05-18T10:00:00Z" \
  -config /etc/litestream.yml \
  /var/lib/enx-api/enx.db

# 重启应用
sudo systemctl start enx-api
```

## 与每日全量备份对比

| 维度 | 每日全量备份（shell + systemd） | Litestream |
|------|-------------------------------|------------|
| **RPO** | 24 小时 | 秒级 |
| **备份方式** | 全量快照 | WAL 增量流式 |
| **S3 存储量** | 每天一个完整 DB 文件 | 增量 frames（通常更小） |
| **恢复粒度** | 只能恢复到每天备份点 | 任意时间点 |
| **运维复杂度** | 低（一个 shell 脚本） | 低（一个进程 + 配置文件） |
| **改动应用代码** | 否 | 否 |
| **适用场景** | 数据变更不频繁，丢一天可接受 | 数据安全要求高 |

## 注意事项

- Litestream 运行期间会持有 SQLite 的共享锁，应用仍可正常读写，但**不能同时运行另一个 Litestream 实例**
- 恢复前必须先停止应用，避免写冲突
- S3 路径建议加子目录前缀（如 `litestream/enx`），与全量备份文件区分
- WAL 历史默认保留 24 小时，可通过 `retention` 参数调整

## 参考

- [官方文档](https://litestream.io/getting-started/)
- [GitHub](https://github.com/benbjohnson/litestream)
