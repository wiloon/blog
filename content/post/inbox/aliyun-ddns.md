---
title: aliyun ddns
author: "-"
date: 2019-01-26T09:51:46+00:00
url: ddns
categories:
  - network
tags:
  - reprint
---
## aliyun ddns

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

## jeessy2/ddns-go

[https://github.com/jeessy2/ddns-go](https://github.com/jeessy2/ddns-go)
