---
title: archlinux add root ca
author: "-"
type: post
date: 2018-09-03T08:17:29+00:00
url: /?p=12633
categories:
  - Uncategorized

---
将 /usr/local/share/ca-certificates/_.crt 移动到 /etc/ca-certificates/trust-source/anchors/ 下
  
对 /etc/ssl/certs/_.pem 进行上述操作,并将它们重命名为 *.crt
  
运行 trust extract-compat