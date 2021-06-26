---
title: archlinux ca-certificates update, 导入证书
author: "-"
type: post
date: 2018-11-14T02:55:52+00:00
url: /?p=12883
categories:
  - Uncategorized

---
https://www.archlinux.org/news/ca-certificates-update/

```bash
# xxx.crt should export from sub ca
sudo cp xxx.crt /etc/ssl/certs/
sudo cp xxx.crt /etc/ca-certificates/trust-source/anchors/
sudo trust extract-compat

```