---
title: jmeter beanshell 数字转字符串补零
author: "-"
date: 2015-10-23T07:02:28+00:00
url: /?p=8420
categories:
  - Inbox
tags:
  - reprint
---
## jmeter beanshell 数字转字符串补零

http://localhost:7000/?id=${__counter(FALSE,eIndex)}&p=prefix${__BeanShell(333+${eIndex})}sufix

```bash

http://localhost:7000/?id=${__BeanShell(String.format("%03d"\,new Object[]{1}))}
  
#逗号用反斜杠转换
  
#参数传Object数组
  
```

https://help.flood.io/docs/how-to-pad-strings-in-jmeter