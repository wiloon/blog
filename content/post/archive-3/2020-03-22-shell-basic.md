---
title: shell basic
author: wiloon
type: post
date: 2020-03-22T10:27:45+00:00
url: /?p=15803
categories:
  - Uncategorized

---
### Shell中去除字符串前后空格的方法
    echo ' A B C ' | awk '{gsub(/^\s+|\s+$/, "");print}'

### 判断字符串为空
    #!/bin/sh

    STRING=

    if [ -z "$STRING" ]; then
        echo "STRING is empty"
    fi

    if [ -n "$STRING" ]; then
        echo "STRING is not empty"
    fi

#将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法：

value=`pwd`

#将pwd的执行结果放到变量value中保存，

value=$(pwd)

另一种方法：

value=`pwd`