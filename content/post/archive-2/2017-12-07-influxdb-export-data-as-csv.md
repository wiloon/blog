---
title: influxdb export data as csv
author: w1100n
type: post
date: 2017-12-07T04:16:16+00:00
url: /?p=11551
categories:
  - Uncategorized

---
https://stackoverflow.com/questions/27779472/export-data-from-influxdb

```bash
influx -host influxdb.mydomain.com -database primary -format csv -execute "select time,value from \"continuous\" where channel='ch123'" > outtest.csv

influx -database 'db0' -execute "select field0,\"field1\" from measurement0 where tag-name0='tag-value0' and time>'2018-05-05 02:00:00' and time<'2018-05-07 11:00:00' order by time tz('Etc/GMT-8')" -format 'csv' -precision 'rfc3339' > xxx.csv
# 使用 tz('Etc/GMT-8') 后,过滤条件中的time>'xxx' 填写东8区时间.
```

### 其它 influxdb相关命令

<https://blog.wiloon.com/?p=10979>