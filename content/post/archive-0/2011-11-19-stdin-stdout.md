---
title: STDIN STDOUT…
author: "-"
date: 2011-11-19T07:35:23+00:00
url: /?p=1543
views:
  - 5
categories:
  - Linux

---
## STDIN STDOUT…
Unix/Linux/BSD 都有三个特别文件，分别
1) 标准输入 即 STDIN , 在 /dev/stdin ,
   一般指键盘输入, shell里代号是 0
2) 标准输出 STDOUT, 在 /dev/stdout,
   一般指终端(terminal), 就是显示器, shell里代号是 1
3) 标准错误 STDERR, 在 /dev/stderr
   也是指终端(terminal), 不同的是, 错误信息送到这里
   shell里代号是 2