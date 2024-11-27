---
title: 'go,  time.Tick, tick immediately'
author: "-"
date: 2017-11-23T05:28:42+00:00
url: /?p=11472
categories:
  - Inbox
tags:
  - reprint
---
## 'go,  time.Tick, tick immediately'
How to get time.Tick to tick immediately

```go
ticker := time.NewTicker(period)
for ; true; <-ticker.C {
    ...
}
```

https://stackoverflow.com/questions/32705582/how-to-get-time-tick-to-tick-immediately/47448177#47448177
  
https://github.com/golang/go/issues/17601