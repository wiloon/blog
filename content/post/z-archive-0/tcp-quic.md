---
title: tcp, quic, 流量复制
author: "-"
date: 2012-08-31T07:52:34+00:00
url: tcp-quic
categories:
  - network

---
## tcp, quic
```puml
@startuml
[tcp client] as tc
[tq] as tq
note left: tcp server:2000
[qt] as qt
note left: quic server: 2001
[tcp server] as ts
note left: tcp server: 2002

tc --> tq
tq --> qt
qt --> ts

@enduml
```

### t2q2t
>https://github.com/flano-yuki/t2q2t.git
### tcpcopoy
>https://github.com/session-replay-tools/tcpcopy
### goreplay
>https://github.com/buger/goreplay
### tcpcopy架构漫谈
>https://blog.csdn.net/wangbin579/article/details/8949315
>https://segmentfault.com/a/1190000039285429
>https://github.com/buger/goreplay

