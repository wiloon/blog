---
title: journal suppressed N messages
author: "-"
date: 2019-07-29T01:36:52+00:00
url: /?p=14736
categories:
  - Inbox
tags:
  - reprint
---
## journal suppressed N messages

systemd-journal: Suppressed 9567 messages from /system.slice/
  
systemd-journal: Suppressed 6735 messages from /system.slice/
  
......
  
根据字面意思理解就是日志被丢弃了, 看来是由于 journald 服务的问题导致的日志问题

在 journald 中, 有如下两个参数跟此问题相关:

```bash
vim /etc/systemd/journald.conf
```

RateLimitInterval
  
RateLimitBurst
  
RateLimitInterval是指定时间间隔, 意思就是说, 在RateLimitInterval这段时间内的日志总量(总条数)控制在RateLimitBurst以内. 这两个参数搭配使用可以用来控制日志速率, 避免由于大量日志输出导致的一系列性能问题.

该问题的根源在于该主机目前日志输出的速率超出了 journald 默认的配置, 你可以自定定义该速率, 也可以将RateLimitInterval设置为0, 以禁用速率控制

接下来重启 journald 以生效配置

systemctl restart systemd-journald

<https://docs.lvrui.io/2018/11/22/systemd-journal-Suppressed-N-messages/>

systemd-journald这个服务重启的时候, 会给所有的进程发送SIGPIPE信号, 而在默认的 systemd 定义中, SIGPIPE 信号属于正常退出的范围. 所以即使 unit 文件配置了Restart on-failure也不会被重启

<https://docs.lvrui.io/2018/11/22/systemd-journald%E7%9A%84SIGPIPE%E4%BF%A1%E5%8F%B7BUG/>
