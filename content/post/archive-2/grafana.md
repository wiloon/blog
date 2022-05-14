---
title: grafana
author: "-"
date: 2019-02-17T12:35:14+00:00
url: /?p=13621
categories:
  - inbox
tags:
  - reprint
---
## grafana
```bash
# podman
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
-p 3100:3000 \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana:8.4.4

# in pod
podman run \
-d \
--name=grafana \
-e "GF_SERVER_ROOT_URL=http://grafana.wiloon.com" \
-e "GF_SECURITY_ADMIN_PASSWORD=password0" \
--pod monitor \
-v grafana-storage:/var/lib/grafana \
-v /etc/localtime:/etc/localtime:ro \
grafana/grafana

```

### variable for host

```sql
SHOW TAG VALUES ON "telegraf" FROM "system" WITH KEY = "host"
```

Q. How do I use the second y axis, secondYAxis function does not work

A. You can switch any series to the second y axis by clicking on the colored line to left of the series name in the legend below the graph. Alternately, use the "Display Styles" > "Series Specific overrides" to define an alias or regex + "Y-axis: 2" to move metrics to the right Axis

https://github.com/grafana/grafana/wiki/FAQ