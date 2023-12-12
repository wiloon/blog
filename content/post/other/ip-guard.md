---
title: "ip-guard, [0x7FFFBB83E044] ANOMALY: use of REX.w is meaningless (default operand size is 64)"
author: "-"
date: 2011-10-19T02:49:26+00:00
url: /?p=1190
categories:
  - Linux
tags:
  - reprint
---
## "ip-guard, [0x7FFFBB83E044] ANOMALY: use of REX.w is meaningless (default operand size is 64)"

HKEY_LOCAL_MACHINE\SOFTWARE\TEC\Ocular.3\agent\config 
字符串类型, key: hookapi_filterproc_external
value: cmd.exe;wsl.exe

## foo.reg

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\TEC\Ocular.3\agent\config]
"hookapi_filterproc_external"="cmd.exe;wsl.exe"
```