---
title: Repository write access denied
author: "-"
date: 2011-11-03T04:37:33+00:00
url: /?p=1438
categories:
  - Linux
  - VCS
tags:
  - Git

---
## Repository write access denied
Repository write access denied

manually add public key to /home/git/.ssh/authorized_keys

start with :

command="python /home/www/indefero/scripts/gitserve.py USER",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa\***\***