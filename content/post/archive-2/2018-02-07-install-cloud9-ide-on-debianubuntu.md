---
title: install cloud9 ide on debian/ubuntu
author: wiloon
type: post
date: 2018-02-07T15:53:29+00:00
url: /?p=11838
categories:
  - Uncategorized

---
https://github.com/c9

[code lang=shell]
  
git clone https://github.com/c9/core sdk
  
cd sdk/
  
./scripts/install-sdk.sh
  
node server.js -p 8181 -l 0.0.0.0 -w /our/project/directory/-a :
  
[/code]

https://www.vultr.com/docs/install-the-cloud9-ide-on-debian-wheezy