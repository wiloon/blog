---
title: Making ipset,iptables persistent
author: wiloon
type: post
date: 2019-09-09T09:57:13+00:00
url: /?p=14918
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">ipset save &gt; /etc/ipset.conf
systemctl enable ipset.service

iptables-save -f /etc/iptables/iptables.rules
systemctl enable iptables.service
</code></pre>

https://wiki.archlinux.org/index.php/Ipset
  
https://wiki.archlinux.org/index.php/Iptables