---
title: 'TCP  Buffer'
author: wiloon
type: post
date: 2019-12-11T05:43:59+00:00
url: /?p=15178
categories:
  - Uncategorized

---
Buffer 指的是 sysctl 中的 rmem 或者 wmem，如果是代码中指定的话对应着 SO\_SNDBUF 或者 SO\_RCVBUF，从 TCP 的概念来看对应着发送窗口或者接收窗口。

```bash
sudo sysctl -a | egrep "rmem|wmem|adv_win|moderate"
```

https://www.infoq.cn/article/sFjkj1C5bz2kOXSxYbHO?utm\_source=rss&utm\_medium=article