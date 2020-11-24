---
title: Java Flight Recorder, jfr
author: w1100n
type: post
date: 2018-05-29T10:05:18+00:00
url: /?p=12264
categories:
  - Uncategorized

---
```bash
  
jcmd 40019 VM.check\_commercial\_features
  
jcmd 40019 VM.unlock\_commercial\_features
  
jcmd 40019 JFR.check
  
jcmd 40019 JFR.start name=jfr0 delay=10s duration=10s filename=jfr0.jfr

```