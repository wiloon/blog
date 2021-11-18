---
title: 解决 archlinux 和 windows 双系统启动时间不准的问题
author: "-"
date: 2016-04-25T15:48:11+00:00
url: /?p=8956
categories:
  - Uncategorized

---
## 解决 archlinux 和 windows 双系统启动时间不准的问题
https://bbs.archlinuxcn.org/viewtopic.php?id=424

```
pacman -S openntpd
systemctl start openntpd
```

ntpd -s -d

<span class="n">hwclock <span class="o">-<span class="n">w

<code class="nginx">http://mindonmind.github.io/notes/linux/arch_time.html```