---
title: 'go > docker'
author: "-"
date: 2019-03-28T14:30:30+00:00
url: /?p=13990
categories:
  - container
tags:
  - reprint
---
## 'go > docker'

```bash
gOOS=linux GOARCH=arm go build .
docker build -t registry.wiloon.com/nj4xx-data:v0.1.0 .
docker push registry.wiloon.com/nj4xx-data:v0.1.0

docker pull registry.wiloon.com/nj4xx-data:v0.1.0
```
