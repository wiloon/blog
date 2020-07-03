---
title: Increasing the amount of inotify watchers
author: wiloon
type: post
date: 2017-07-27T02:19:47+00:00
url: /?p=10927
categories:
  - Uncategorized

---
```bash
  
#archlinux
  
echo fs.inotify.max\_user\_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl -system

```