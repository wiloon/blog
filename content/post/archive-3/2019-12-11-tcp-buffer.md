---
title: 'TCP  Buffer'
author: w1100n
type: post
date: 2019-12-11T05:43:59+00:00
url: /?p=15178
categories:
  - Uncategorized

---
Buffer 指的是 sysctl 中的 rmem 或者 wmem，如果是代码中指定的话对应着 SO_SNDBUF 或者 SO_RCVBUF，从 TCP 的概念来看对应着发送窗口或者接收窗口。

```bash
sudo sysctl -a | egrep "rmem|wmem|adv_win|moderate"
```

https://www.infoq.cn/article/sFjkj1C5bz2kOXSxYbHO?utm_source=rss&utm_medium=article