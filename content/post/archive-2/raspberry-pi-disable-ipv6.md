---
title: raspberry pi disable ipv6
author: "-"
date: 2018-12-24T15:16:49+00:00
url: /?p=13205
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi disable ipv6
```bash
/etc/modprobe.d/ipv6.conf
alias net-pf-10 off
alias ipv6 off
options ipv6 disable_ipv6=1
blacklist ipv6
```


  
    Disable IPv6 on Raspberry Pi3+
  


https://www.cesareriva.com/disable-ipv6-on-raspberry-pi3/embed/#?secret=RVErZNYd3W