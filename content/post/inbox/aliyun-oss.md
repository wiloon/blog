---
title: aliyun oss, 对象存储, ossutil
author: "-"
date: 2019-01-30T15:26:11+00:00
url: aliyun/oss
categories:
  - cloud
tags:
  - reprint
---
## aliyun oss, 对象存储, ossutil

## aliyun oss, ossutil

## install ossutil

```bash
sudo -v ; curl https://gosspublic.alicdn.com/ossutil/install.sh | sudo bash
```

```bash
# 生成配置文件, stsToken 可以置空
ossutil config

./ossutil cp a -f oss://my-bucket/path
./ossutil64 cp /root/tmp/wordpress.sql -f oss://wiloon-backup/
```

[https://help.aliyun.com/document_detail/50561.html?spm=a2c4g.11186623.6.1283.2e0655b7qtA1Md](https://help.aliyun.com/document_detail/50561.html?spm=a2c4g.11186623.6.1283.2e0655b7qtA1Md)

[https://help.aliyun.com/document_detail/120075.html](https://help.aliyun.com/document_detail/120075.html)
