---
title: install cloud9 ide on debian/ubuntu
author: "-"
date: 2018-02-07T15:53:29+00:00
url: install-cloud9-ide-on-debianubuntu
categories:
  - Inbox
tags:
  - reprint
aliases:
  - /p10819/
  - /p11838/
  - /p13731/
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