---
title: go metrics
author: "-"
date: 2020-04-15T10:43:23+00:00
url: go/metrics
categories:
  - Go
tags:$
  - reprint
---
## go metrics
```go
import "github.com/jregovic/go-metrics-influxdb"

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

>https://github.com/rcrowley/go-metrics

