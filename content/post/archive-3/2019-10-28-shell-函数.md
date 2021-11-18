---
title: Shell 函数
author: "-"
date: 2019-10-28T09:43:40+00:00
url: /?p=15071
categories:
  - Uncategorized

---
## Shell 函数
```bash
[ function ] funname [()]
{
    action;
    [return int;]
}
```

```bash
# 定义函数 fun0
fun0(){
    echo "run fun0 "
}
# 调用函数 fun0
fun0

```

```bash
# 定义带参数的函数 fun0
fun0(){
    echo "run fun0 $1 "
}
# 调用带参数的函数 fun0
fun0 foo

```

https://www.runoob.com/linux/linux-shell-func.html
  
https://wiki.jikexueyuan.com/project/shell-tutorial/shell-function-parameter.html