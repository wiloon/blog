---
title: gor
author: "-"
date: 2020-04-16T16:37:41+00:00
url: /?p=15965
categories:
  - Inbox
tags:
  - reprint
---
## gor

```bash
sudo ./gor --input-raw :8080 --output-stdout
sudo ./gor --input-raw :8000 --output-http="http://localhost:8001"
sudo ./gor --input-raw :8000 --output-file=requests.gor
sudo ./gor --input-file requests.gor --output-http="http://localhost:8001"
sudo ./gor --input-file requests.gor --output-stdout

```
