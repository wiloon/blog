---
title: Shell 判断进程是否存在
author: "-"
date: 2020-02-19T02:27:59+00:00
url: /?p=15598
categories:
  - shell
tags:
  - reprint
---
## Shell 判断进程是否存在
```bash
#! /bin/bash
    function check(){
      count=`ps -ef |grep $1 |grep -v "grep" |wc -l`
      #echo $count
      if [ 0 == $count ];then
        nohup python /runscript/working/$1 &
      fi
    }

```

————————————————
  
版权声明: 本文为CSDN博主「栎枫」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/superbfly/article/details/52513765