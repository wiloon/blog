---
title: archlinux ca-certificates update, 导入证书
author: "-"
date: 2018-11-14T02:55:52+00:00
url: /?p=12883
categories:
  - Inbox
tags:
  - reprint
---
## archlinux ca-certificates update, 导入证书
https://www.archlinux.org/news/ca-certificates-update/

```bash
# xxx.crt should export from sub ca
sudo cp xxx.crt /etc/ssl/certs/
sudo cp xxx.crt /etc/ca-certificates/trust-source/anchors/
sudo trust extract-compat

```


## archlinux add root ca
将 /usr/local/share/ca-certificates/_.crt 移动到 /etc/ca-certificates/trust-source/anchors/ 下
  
对 /etc/ssl/certs/_.pem 进行上述操作,并将它们重命名为 *.crt
  
运行 trust extract-compat

