---
title: curl websocket
author: wiloon
type: post
date: 2018-12-29T08:16:00+00:00
url: /?p=13237
categories:
  - Uncategorized

---
```bashcurl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host: example.com:80" \
     --header "Origin: http://example.com:80" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     http://example.com:80/

```

```bashcurl -v -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: 127.0.0.1:8088" -H "Sec-WebSocket-Key: lkUx3lTpjFwO5OI7xY3+1Q==" -H "Sec-WebSocket-Version: 13" http://127.0.0.1:8088/

```

Upgrade 表示升级到 WebSocket 协议，
  
Connection 表示这个 HTTP 请求是一次协议升级，
  
Origin 表示发请求的来源。

* * *

作者：sd2131512
  
来源：CSDN
  
原文：https://blog.csdn.net/sd2131512/article/details/74996577
  
版权声明：本文为博主原创文章，转载请附上博文链接！