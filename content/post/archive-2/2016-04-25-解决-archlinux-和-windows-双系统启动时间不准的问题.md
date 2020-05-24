---
title: 解决 archlinux 和 windows 双系统启动时间不准的问题
author: wiloon
type: post
date: 2016-04-25T15:48:11+00:00
url: /?p=8956
categories:
  - Uncategorized

---
https://bbs.archlinuxcn.org/viewtopic.php?id=424

&nbsp;

<pre><code class="nginx">&lt;span class="title">pacman&lt;/span> -S openntpd
systemctl start openntpd```

<pre>ntpd -s -d</pre>

<pre><span class="n">hwclock</span> <span class="o">-</span><span class="n">w</span></pre>

<pre><code class="nginx">http://mindonmind.github.io/notes/linux/arch_time.html```