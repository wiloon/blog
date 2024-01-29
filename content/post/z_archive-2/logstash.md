---
title: logstash
author: "-"
date: 2018-01-18T09:05:15+00:00
url: /?p=11755
categories:
  - Inbox
tags:
  - reprint
---
## logstash

/etc/logstash/conf.d/logstash.conf

```bash/usr/share/logstash/bin/logstash --path.settings=/root/tmp/logstash/

input {
  redis {
    id => "system-log"
    data_type=>"list"
    host=>"127.0.0.1"
    port=>"6379"
    key=>"system-log"
  }
  redis {
    id => "app-log"
    data_type=>"list"
    host=>"127.0.0.1"
    port=>"6379"
    key=>"app-log"
  }
}

output {
  if "app-log" in [tags] {
    elasticsearch {
      id => "elk-es-app"
      hosts => "127.0.0.1:9200"
      index => "logstash-app-log-%{+YYYY.MM.dd}"
    }
  }else{
    elasticsearch {
       id => "elk-es-sys"
       hosts => "127.0.0.1:9200"
       index => "logstash-sys-log-%{+YYYY.MM.dd}"
    }
  }
}
```
