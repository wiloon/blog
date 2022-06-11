---
title: systemd timer
author: "-"
date: 2013-08-21T04:21:22+00:00
url: systemd/timer
categories:
  - OS
tags:
  - reprint
---
## systemd timer

```bash
systemctl list-timers
systemctl list-timers --all


```

```bash
/etc/systemd/system/foo.timer
[Unit]
Description=Run foo weekly

[Timer]
OnCalendar=Mon..Fri 21:00
OnCalendar=Sat,Sun 21:00
Persistent=true

[Install]
WantedBy=timers.target
```

<http://www.ruanyifeng.com/blog/2018/03/systemd-timer.html>