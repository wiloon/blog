---
title: influxdb export data as csv
author: wiloon
type: post
date: 2017-12-07T04:16:16+00:00
url: /?p=11551
categories:
  - Uncategorized

---
https://stackoverflow.com/questions/27779472/export-data-from-influxdb

<pre><code class="language-bash line-numbers">influx -host influxdb.mydomain.com -database primary -format csv -execute "select time,value from \"continuous\" where channel='ch123'" &gt; outtest.csv

influx -database 'db0' -execute "select field0,\"field1\" from measurement0 where tag-name0='tag-value0' and time&gt;'2018-05-05 02:00:00' and time&lt;'2018-05-07 11:00:00' order by time tz('Etc/GMT-8')" -format 'csv' -precision 'rfc3339' &gt; xxx.csv
# 使用 tz('Etc/GMT-8') 后,过滤条件中的time&gt;'xxx' 填写东8区时间.
</code></pre>

### 其它 influxdb相关命令

<https://blog.wiloon.com/?p=10979>