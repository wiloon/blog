---
title: Java Flight Recorder, jfr
author: "-"
date: 2018-05-29T10:05:18+00:00
url: /?p=12264
categories:
  - Inbox
tags:
  - reprint
---
## Java Flight Recorder, jfr
```bash
  
jcmd 40019 VM.check_commercial_features
  
jcmd 40019 VM.unlock_commercial_features
  
jcmd 40019 JFR.check
  
jcmd 40019 JFR.start name=jfr0 delay=10s duration=10s filename=jfr0.jfr

```