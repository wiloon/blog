---
title: go metrics
author: w1100n
type: post
date: 2020-04-15T10:43:23+00:00
url: /?p=15957
categories:
  - Uncategorized

---
```golang
import "    influxdb "github.com/vrischmann/go-metrics-influxdb""
    go influxdb.InfluxDB(
        metrics.DefaultRegistry,
        time.Duration(10)*time.Second,
        "http://192.168.50.244:8086",
        "database0",
        "measurement0",
        "",
        "",
        false,
    )

    go metrics.Log(
        metrics.DefaultRegistry,
        time.Duration(metricsOutputDuration)*time.Second,
        logger.GetLogger(),
    )

meter := metrics.GetOrRegisterMeter("foo", nil)
meter.Mark(1)

```