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

