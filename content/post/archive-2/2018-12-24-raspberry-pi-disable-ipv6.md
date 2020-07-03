---
title: raspberry pi disable ipv6
author: wiloon
type: post
date: 2018-12-24T15:16:49+00:00
url: /?p=13205
categories:
  - Uncategorized

---
```bash/etc/modprobe.d/ipv6.conf
alias net-pf-10 off
alias ipv6 off
options ipv6 disable_ipv6=1
blacklist ipv6
```

<blockquote class="wp-embedded-content" data-secret="RVErZNYd3W">
  
    <a href="https://www.cesareriva.com/disable-ipv6-on-raspberry-pi3/">Disable IPv6 on Raspberry Pi3+</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://www.cesareriva.com/disable-ipv6-on-raspberry-pi3/embed/#?secret=RVErZNYd3W" data-secret="RVErZNYd3W" width="600" height="338" title="Embedded WordPress Post" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>