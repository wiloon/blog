---
title: SSL 故障分析
author: "-"
date: 2019-03-15T07:41:58+00:00
url: /?p=13852
categories:
  - Inbox
tags:
  - reprint
---
## SSL 故障分析
```bash
openssl s_client -connect host0:port0 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p'

openssl verify foo.pem

openssl s_client  -connect host0:port0 -state -showcerts

解码根证书
openssl x509 -text -in roch.pem
```

https://www.ibm.com/developerworks/cn/linux/l-cn-sclient/index.html