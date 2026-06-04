---
title: ddns-go 与 aliyun-ddns-cli
author: "-"
date: 2019-01-26T09:51:46+00:00
lastmod: 2026-06-04T16:59:10+08:00
url: ddns-go-and-aliyun-ddns-cli
categories:
  - network
tags:
  - ddns
  - aliyun
  - cloudflare
  - remix
  - AI-assisted
---
## ddns-go

`ddns-go` 是一个轻量、可视化配置的 DDNS 工具，支持多家 DNS 服务商。这里主要用于检测家里公网 IP 变化后自动更新 Cloudflare 记录。

[https://github.com/jeessy2/ddns-go](https://github.com/jeessy2/ddns-go)

## aliyun-ddns-cli

[https://github.com/honwen/aliyun-ddns-cli](https://github.com/honwen/aliyun-ddns-cli)

```bash
aliyun-ddns-cli --access-key-id=ak0 --access-key-secret=sk0  auto-update --domain=domain0.wiloon.com --redo=600

docker run -d \
    -e "AKID=[ALIYUN's AccessKey-ID]" \
    -e "AKSCT=[ALIYUN's AccessKey-Secret]" \
    -e "DOMAIN=ddns.aliyun.win" \
    -e "REDO=600" \
    -e "TTL=600" \
    chenhw2/aliyun-ddns-cli
```
