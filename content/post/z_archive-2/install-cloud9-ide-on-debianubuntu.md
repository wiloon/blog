---
title: install cloud9 ide on debian/ubuntu
author: "-"
date: 2018-02-07T15:53:29+00:00
url: /?p=11838
categories:
  - Inbox
tags:
  - reprint
---
## install cloud9 ide on debian/ubuntu
https://github.com/c9

```bash
  
git clone https://github.com/c9/core sdk
  
cd sdk/
  
./scripts/install-sdk.sh
  
node server.js -p 8181 -l 0.0.0.0 -w /our/project/directory/-a :
  
```

https://www.vultr.com/docs/install-the-cloud9-ide-on-debian-wheezy