---
title: systemd timer
author: "-"
date: 2013-08-21T04:21:22+00:00
url: systemd/timer
categories:
  - Linux
tags:
  - reprint
---
## systemd timer

```bash
systemctl list-timers
systemctl list-timers --all
```

## /etc/systemd/system/foo.service

```bash
[Unit]
Description=foo service
[Service]
ExecStart=/path/to/foo.sh

[Install]
WantedBy=multi-user.target
```

## /etc/systemd/system/foo.timer

```bash
[Unit]
Description=foo timer

[Timer]
OnCalendar=*-*-* 12:00:00
Persistent=true
Unit=foo.service

[Install]
WantedBy=multi-user.target
```

```bash
systemctl --now enable foo.timer

```

<http://www.ruanyifeng.com/blog/2018/03/systemd-timer.html>

## the basic format of Oncalnedar event

```bash
* *-*-* *:*:*
```

It is divided into 3 parts -

- `*` To signify the day of the week eg:- Sat,Thu,Mon
- `*-*-*` To signify the calendar date. Which means it breaks down to - year-month-date.
  - `2021-10-15` is 15th of October
  - `*-10-15` means every year at 15th October
  - `*-01-01` means every new year.
- `*:*:*` is to signify the time component of the calnedar event. So it is - hour:minute:second

[[cron#cron crond crontab linux 定时任务 cronie]]

<https://silentlad.com/systemd-timers-oncalendar-(cron)-format-explained>

- Every day at 2am `*-*-* 02:00:00`

## systemd timer 相比 cron 的优点

- 日志更丰富 journald
- 可以设置内存和 CPU 的使用额度
- 任务可以拆分，依赖其他 Systemd 单元，完成非常复杂的任务