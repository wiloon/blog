---
title: shell 把命令输出结果存入变量
author: "-"
date: 2018-08-28T10:55:25+00:00
url: /?p=12596
categories:
  - shell
tags:
  - reprint
---
## shell 把命令输出结果存入变量

```bash
  
var=$(ls -lR|grep "^d"|wc -l)
  
或者另外一种 不建议的方式
  
var=\`ls -lR|grep "^d"|wc -l\`
  
```

<https://blog.csdn.net/baidu_35757025/article/details/64440047>
