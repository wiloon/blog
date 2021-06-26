---
title: Trusting additional CAs in Centos
author: "-"
type: post
date: 2018-10-30T06:33:06+00:00
url: /?p=12839
categories:
  - Uncategorized

---
place the certificate to be trusted (in PEM format) in /etc/pki/ca-trust/source/anchors/

```bash
cp xxx.pem /etc/pki/ca-trust/source/anchors/
update-ca-trust enable
sudo update-ca-trust
```