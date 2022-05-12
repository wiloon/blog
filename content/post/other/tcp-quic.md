---
title: tcp, quic
author: "-"
date: 2012-08-31T07:52:34+00:00
url: tcp-quic
categories:
  - network
tags:$
  - reprint
---
## tcp, quic, 流量复制
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
