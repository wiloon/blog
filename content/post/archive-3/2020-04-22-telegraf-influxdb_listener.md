---
title: telegraf influxdb_listener
author: wiloon
type: post
date: 2020-04-22T10:24:37+00:00
url: /?p=16049
categories:
  - Uncategorized

---
<code class="line-numbers">vim  /etc/telegraf/telegraf.conf
[[outputs.influxdb]]
  urls = ["http://influxdb.wiloon.com"]
  database = "database0"

[[inputs.influxdb_listener]]
  service_address = ":8086"
  read_timeout = "10s"
  write_timeout = "10s"
  max_body_size = 0
```