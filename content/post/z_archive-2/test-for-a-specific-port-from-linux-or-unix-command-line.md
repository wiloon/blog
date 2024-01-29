---
title: test for a specific port from Linux or Unix command line
author: "-"
date: 2018-11-26T06:06:17+00:00
url: /?p=12935
categories:
  - Inbox
tags:
  - reprint
---
## test for a specific port from Linux or Unix command line
https://www.cyberciti.biz/faq/ping-test-a-specific-port-of-machine-ip-address-using-linux-unix/

```bash
  
# check for tcp port ##
  
## need bash shell
  
echo >/dev/tcp/{host}/{port}

(echo >/dev/tcp/{host}/{port}) &>/dev/null && echo "open" || echo "close"
  
(echo >/dev/udp/{host}/{port}) &>/dev/null && echo "open" || echo "close"
  
(echo >/dev/tcp/www.cyberciti.biz/22) &>/dev/null && echo "Open 22" || echo "Close 22"
  
(echo >/dev/tcp/www.cyberciti.biz/443) &>/dev/null && echo "Open 443" || echo "Close 443"

```