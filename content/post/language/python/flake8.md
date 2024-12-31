---
title: flake8
author: "-"
date: 2015-04-12T14:10:20+00:00
url: flake8
categories:
  - Python
tags:
  - reprint
  - remix
---
## flake8

```Bash
pip install flake8
flake8 --max-line-length=120 project_0
# 忽略掉 E501,E302,E122,E225,E303,W291,E221,E231
flake8 --max-line-length=120 --ignore=E501,E302,E122,E225,E303,W291,E221,E231 project_0

# 只检查 F821 undefined name
flake8 --select=F821 /path/to/project_0
```
