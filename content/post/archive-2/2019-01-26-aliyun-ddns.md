---
title: aliyun ddns
author: "-"
type: post
date: 2019-01-26T09:51:46+00:00
url: /?p=13487
categories:
  - Uncategorized

---
## aliyun ddns
https://github.com/honwen/aliyun-ddns-cli

```bash
aliyun-ddns-cli --access-key-id=ak0 --access-key-secret=sk0  auto-update --domain=domain0.wiloon.com --redo=600

docker run -d \
    --name ddns
    -e "AKID=ak0" \
    -e "AKSCT=sk0" \
    -e "DOMAIN=foo.wiloon.com" \
    -e "REDO=600" \
    chenhw2/aliyun-ddns-cli

```

### jeessy2/ddns-go

    https://github.com/jeessy2/ddns-go