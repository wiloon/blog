---
title: linux ping 时间戳
author: wiloon
type: post
date: 2020-03-10T05:39:11+00:00
url: /?p=15720
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">ping 192.168.2.1 -c 10 | awk '{ print $0"\t" strftime("%H:%M:%S",systime()) } '
</code></pre>