---
title: zkui
author: "-"
date: 2020-03-11T08:53:24+00:00
url: /?p=15724
categories:
  - Inbox
tags:
  - reprint
---
## zkui
修改zkui session 过期 时间

```bash
sed -i '/sessionTimeout/s/300/1440/g' /var/app/config.cfg
```